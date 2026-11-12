"""Aplica a la PCB una tabla de colocación (referencia, x, y, giro, cara) o la exporta.

Uso:
    python herramientas/kicad/colocar.py hardware/v2/esp-riego.kicad_pcb --exportar colocacion.csv
    python herramientas/kicad/colocar.py <copia>/esp-riego.kicad_pcb colocacion.csv -o <copia>/esp-riego.kicad_pcb

Tabla: CSV con cabecera `ref,x,y,giro,cara` (mm y grados, coordenadas de la placa; cara F o B).
Una celda vacía deja ese dato como está. Con --bloquear, las huellas de la tabla quedan bloqueadas.
Lee la PCB sobre una copia temporal y escribe solo el .kicad_pcb de -o (o el CSV de --exportar).
Imprime cuántas huellas mueve, las referencias que no existen y las huellas colocadas cuyo
patio queda fuera del contorno. Se relanza solo con el Python de KiCad si hace falta.
"""
import argparse
import csv
import io
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import Fallo, con_python_kicad, emitir, no_tfg, principal  # noqa: E402

CARAS = {"f": "F", "top": "F", "sup": "F", "superior": "F", "f.cu": "F", "b": "B", "bottom": "B", "inf": "B",
         "inferior": "B", "b.cu": "B"}


def leer_tabla(ruta):
    texto = Path(ruta).read_text(encoding="utf-8-sig")
    separador = ";" if texto.split("\n", 1)[0].count(";") > texto.split("\n", 1)[0].count(",") else ","
    filas = []
    for n, fila in enumerate(csv.DictReader(io.StringIO(texto), delimiter=separador), start=2):
        fila = {(k or "").strip().lower(): (v or "").strip() for k, v in fila.items()}
        if not fila.get("ref"):
            continue
        try:
            dato = {"ref": fila["ref"], "x": float(fila["x"]) if fila.get("x") else None,
                    "y": float(fila["y"]) if fila.get("y") else None,
                    "giro": float(fila["giro"]) if fila.get("giro") else None,
                    "cara": CARAS[fila["cara"].lower()] if fila.get("cara") else None}
        except (ValueError, KeyError) as e:
            raise Fallo(f"{ruta}, línea {n}: dato no válido ({e})")
        filas.append(dato)
    if not filas:
        raise Fallo(f"{ruta}: tabla vacía o sin la cabecera ref,x,y,giro,cara")
    return filas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pcb", help=".kicad_pcb de origen")
    ap.add_argument("tabla", nargs="?", help="CSV ref,x,y,giro,cara")
    ap.add_argument("-o", "--salida", help=".kicad_pcb de destino")
    ap.add_argument("--exportar", metavar="CSV", help="escribe la colocación actual en un CSV y termina")
    ap.add_argument("--bloquear", action="store_true", help="bloquea las huellas colocadas")
    args = ap.parse_args()
    if bool(args.exportar) == bool(args.tabla and args.salida):
        raise Fallo("indica una tabla y -o, o bien --exportar")
    filas = leer_tabla(args.tabla) if args.tabla else []
    con_python_kicad(__file__)
    import pcbnew

    origen = Path(args.pcb).resolve()
    if not origen.is_file():
        raise Fallo(f"no existe {origen}")
    with tempfile.TemporaryDirectory(prefix="colocar_") as tmp:
        copia = Path(tmp) / origen.name
        shutil.copyfile(origen, copia)
        board = pcbnew.LoadBoard(str(copia))
        huellas = {fp.GetReference(): fp for fp in board.GetFootprints()}
        if args.exportar:
            with open(args.exportar, "w", encoding="utf-8", newline="") as f:
                salida = csv.writer(f)
                salida.writerow(["ref", "x", "y", "giro", "cara"])
                for ref in sorted(huellas, key=lambda r: (r.rstrip("0123456789"), int("0" + r[len(r.rstrip("0123456789")):]))):
                    fp = huellas[ref]
                    salida.writerow([ref, "%g" % round(pcbnew.ToMM(fp.GetPosition().x), 4), "%g" % round(pcbnew.ToMM(fp.GetPosition().y), 4),
                                     "%g" % fp.GetOrientationDegrees(), "B" if fp.IsFlipped() else "F"])
            emitir([f"{args.exportar}: {len(huellas)} huellas"])
            return 0

        movidas, faltan, vueltas = 0, [], 0
        for d in filas:
            fp = huellas.get(d["ref"])
            if fp is None:
                faltan.append(d["ref"])
                continue
            if d["cara"] and (d["cara"] == "B") != fp.IsFlipped():
                fp.SetLayerAndFlip(pcbnew.B_Cu if d["cara"] == "B" else pcbnew.F_Cu)
                vueltas += 1
            if d["giro"] is not None:
                fp.SetOrientationDegrees(d["giro"])
            pos = fp.GetPosition()
            x = pcbnew.FromMM(d["x"]) if d["x"] is not None else pos.x
            y = pcbnew.FromMM(d["y"]) if d["y"] is not None else pos.y
            fp.SetPosition(pcbnew.VECTOR2I(x, y))
            if args.bloquear:
                fp.SetLocked(True)
            movidas += 1
        borde = board.GetBoardEdgesBoundingBox()
        fuera = []
        for d in filas:
            fp = huellas.get(d["ref"])
            if fp is None or not borde.GetWidth():
                continue
            patio = fp.GetCourtyard(pcbnew.B_CrtYd if fp.IsFlipped() else pcbnew.F_CrtYd)
            caja = patio.BBox() if patio.OutlineCount() else fp.GetBoundingBox(False)
            if not borde.Contains(caja):
                fuera.append(d["ref"])
        pcbnew.SaveBoard(str(copia), board)
        destino = Path(args.salida).resolve()
        no_tfg(destino)
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(copia, destino)
    emitir([f"{destino}: {movidas} huellas colocadas de {len(filas)} · cambiadas de cara {vueltas}",
            f"Referencias de la tabla que no están en la PCB: {' '.join(faltan) or 'ninguna'}",
            f"Con el patio fuera del contorno (caja): {' '.join(fuera) or 'ninguna'}"])
    return 1 if faltan else 0


if __name__ == "__main__":
    principal(main)
