"""Aplica a la PCB una tabla de colocación (referencia, x, y, giro, cara y referencia de serigrafía) o la exporta.

Uso:
    python herramientas/kicad/colocar.py hardware/v2/esp-riego.kicad_pcb --exportar colocacion.csv [--con-referencias]
    python herramientas/kicad/colocar.py <copia>/esp-riego.kicad_pcb colocacion.csv -o <copia>/esp-riego.kicad_pcb [--placa 100x80]

Tabla: CSV `ref,x,y,giro,cara` (mm y grados; cara F o B) y, opcional, `rx,ry,rgiro,ralto,rtrazo`: la
referencia, a (rx, ry) mm del ancla en los ejes de la placa, con giro absoluto y alto y trazo en mm. Una
celda vacía deja el dato como está. La fila `PLACA,<ancho>,<alto>` o --placa ponen un contorno rectangular
con la misma esquina superior izquierda y llevan los taladros (MountingHole) con su esquina.
Escribe solo el .kicad_pcb de -o (o el CSV de --exportar) y dice lo que mueve y lo que queda fuera.
"""
import argparse
import csv
import io
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import Fallo, con_python_kicad, emitir, no_tfg, principal  # noqa: E402

CARAS = {"f": "F", "top": "F", "sup": "F", "superior": "F", "f.cu": "F", "b": "B", "bottom": "B", "inf": "B",
         "inferior": "B", "b.cu": "B"}
COLUMNAS_REF = ("rx", "ry", "rgiro", "ralto", "rtrazo")


def placa(texto):
    """«100x80» → (100.0, 80.0)."""
    m = re.fullmatch(r"\s*(\d+(?:[.,]\d+)?)\s*[x×X]\s*(\d+(?:[.,]\d+)?)\s*", str(texto or ""))
    if not m:
        raise Fallo(f"tamaño de placa «{texto}»: se espera ANCHOxALTO en mm (p. ej. 100x80)")
    return float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", "."))


def leer_tabla(ruta, con_placa=False):
    """Filas de la tabla. Con con_placa=True devuelve (filas, (ancho, alto) o None)."""
    texto = Path(ruta).read_text(encoding="utf-8-sig")
    separador = ";" if texto.split("\n", 1)[0].count(";") > texto.split("\n", 1)[0].count(",") else ","
    filas, tam = [], None
    for n, fila in enumerate(csv.DictReader(io.StringIO(texto), delimiter=separador), start=2):
        fila = {(k or "").strip().lower(): (v or "").strip() for k, v in fila.items()}
        if not fila.get("ref"):
            continue
        try:
            if fila["ref"].upper() == "PLACA":
                tam = (float(fila["x"]), float(fila["y"]))
                continue
            dato = {"ref": fila["ref"], "x": float(fila["x"]) if fila.get("x") else None,
                    "y": float(fila["y"]) if fila.get("y") else None,
                    "giro": float(fila["giro"]) if fila.get("giro") else None,
                    "cara": CARAS[fila["cara"].lower()] if fila.get("cara") else None}
            for c in COLUMNAS_REF:
                dato[c] = float(fila[c]) if fila.get(c) else None
        except (ValueError, KeyError) as e:
            raise Fallo(f"{ruta}, línea {n}: dato no válido ({e})")
        filas.append(dato)
    if not filas:
        raise Fallo(f"{ruta}: tabla vacía o sin la cabecera ref,x,y,giro,cara")
    return (filas, tam) if con_placa else filas


def es_taladro(fp):
    return "MountingHole" in fp.GetFPIDAsString()


def contorno(board, ancho, alto):
    """Cambia el rectángulo de Edge.Cuts a ancho × alto (misma esquina superior izquierda) y mueve los taladros con
    su esquina. Devuelve las referencias de los taladros movidos."""
    import pcbnew
    bordes = [d for d in board.GetDrawings() if d.GetLayer() == pcbnew.Edge_Cuts]
    if len(bordes) != 1 or bordes[0].GetClass() != "PCB_SHAPE" or bordes[0].GetShape() != pcbnew.SHAPE_T_RECT:
        raise Fallo("--placa solo admite un contorno de un único rectángulo en Edge.Cuts")
    r = bordes[0]
    a, b = r.GetStart(), r.GetEnd()
    x0, y0, x1, y1 = min(a.x, b.x), min(a.y, b.y), max(a.x, b.x), max(a.y, b.y)
    nx1, ny1 = x0 + pcbnew.FromMM(ancho), y0 + pcbnew.FromMM(alto)
    r.SetStart(pcbnew.VECTOR2I(x0, y0))
    r.SetEnd(pcbnew.VECTOR2I(nx1, ny1))
    movidos = []
    for fp in board.GetFootprints():
        if not es_taladro(fp):
            continue
        p = fp.GetPosition()
        nx = p.x if p.x - x0 <= x1 - p.x else nx1 - (x1 - p.x)
        ny = p.y if p.y - y0 <= y1 - p.y else ny1 - (y1 - p.y)
        if (nx, ny) != (p.x, p.y):
            fp.SetPosition(pcbnew.VECTOR2I(nx, ny))
            movidos.append(fp.GetReference())
    return movidos


def aplicar(board, filas, bloquear=False):
    """Coloca en `board` (pcbnew) las filas de `leer_tabla`. Devuelve (movidas, referencias que faltan, vueltas).
    La usa también colocacion.py evaluar, para medir exactamente lo que dejaría este script."""
    import pcbnew
    huellas = {fp.GetReference(): fp for fp in board.GetFootprints()}
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
        ref = fp.Reference()
        if d.get("ralto"):
            ref.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(d["ralto"]), pcbnew.FromMM(d["ralto"])))
        if d.get("rtrazo"):
            ref.SetTextThickness(pcbnew.FromMM(d["rtrazo"]))
        if d.get("rgiro") is not None:
            ref.SetTextAngleDegrees(d["rgiro"])
        if d.get("rx") is not None or d.get("ry") is not None:
            rp = ref.GetPosition()
            ref.SetPosition(pcbnew.VECTOR2I(x + pcbnew.FromMM(d["rx"]) if d.get("rx") is not None else rp.x,
                                            y + pcbnew.FromMM(d["ry"]) if d.get("ry") is not None else rp.y))
        if bloquear:
            fp.SetLocked(True)
        movidas += 1
    return movidas, faltan, vueltas


def _clave(r):
    base = r.rstrip("0123456789")
    return base, int("0" + r[len(base):])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pcb", help=".kicad_pcb de origen")
    ap.add_argument("tabla", nargs="?", help="CSV ref,x,y,giro,cara[,rx,ry,rgiro,ralto,rtrazo]")
    ap.add_argument("-o", "--salida", help=".kicad_pcb de destino")
    ap.add_argument("--exportar", metavar="CSV", help="escribe la colocación actual en un CSV y termina")
    ap.add_argument("--con-referencias", action="store_true", help="con --exportar, añade rx,ry,rgiro,ralto,rtrazo")
    ap.add_argument("--placa", metavar="ANCHOxALTO", help="contorno rectangular de ese tamaño (mueve los taladros)")
    ap.add_argument("--bloquear", action="store_true", help="bloquea las huellas colocadas")
    args = ap.parse_args()
    if bool(args.exportar) == bool(args.tabla and args.salida):
        raise Fallo("indica una tabla y -o, o bien --exportar")
    filas, tam = leer_tabla(args.tabla, con_placa=True) if args.tabla else ([], None)
    if args.placa:
        tam = placa(args.placa)
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
                salida.writerow(["ref", "x", "y", "giro", "cara"] + (list(COLUMNAS_REF) if args.con_referencias else []))
                for ref in sorted(huellas, key=_clave):
                    fp = huellas[ref]
                    p = fp.GetPosition()
                    fila = [ref, "%g" % round(pcbnew.ToMM(p.x), 4), "%g" % round(pcbnew.ToMM(p.y), 4),
                            "%g" % fp.GetOrientationDegrees(), "B" if fp.IsFlipped() else "F"]
                    if args.con_referencias:
                        r = fp.Reference()
                        rp = r.GetPosition()
                        fila += ["%g" % round(pcbnew.ToMM(rp.x - p.x), 4), "%g" % round(pcbnew.ToMM(rp.y - p.y), 4),
                                 "%g" % r.GetTextAngleDegrees(), "%g" % round(pcbnew.ToMM(r.GetTextHeight()), 4),
                                 "%g" % round(pcbnew.ToMM(r.GetTextThickness()), 4)]
                    salida.writerow(fila)
            emitir([f"{args.exportar}: {len(huellas)} huellas"])
            return 0

        taladros = contorno(board, *tam) if tam else []
        movidas, faltan, vueltas = aplicar(board, filas, args.bloquear)
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
    lineas = [f"{destino}: {movidas} huellas colocadas de {len(filas)} · cambiadas de cara {vueltas}",
              f"Referencias de la tabla que no están en la PCB: {' '.join(faltan) or 'ninguna'}",
              f"Con el patio fuera del contorno (caja): {' '.join(fuera) or 'ninguna'}"]
    if tam:
        lineas.append(f"Placa {tam[0]:g} × {tam[1]:g} mm · taladros movidos: {' '.join(taladros) or 'ninguno'}")
    emitir(lineas)
    return 1 if faltan else 0


if __name__ == "__main__":
    principal(main)
