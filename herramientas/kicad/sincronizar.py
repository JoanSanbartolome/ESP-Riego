"""Netlist → PCB con pcbnew (equivale a «Actualizar PCB desde el esquema», F8) y paridad al terminar.

Uso:
    python herramientas/kicad/sincronizar.py <copia>/v2 -o <copia>/v2/esp-riego.kicad_pcb
    python herramientas/kicad/sincronizar.py hardware/v2 -o <temporal>/esp-riego.kicad_pcb --actualizar U7,U8

Añade las huellas que faltan (sin colocar: en filas bajo el contorno, por tipo), borra las que ya
no tienen símbolo (salvo --conservar) y pone en todas valor, campos, ruta, hoja, atributos (DNP,
fuera de BOM y de posiciones) y la red de cada pad. «Fuera de posiciones» no se quita de una huella
que ya lo lleva (se avisa). Una huella cuyo identificador cambió, o pedida con --actualizar
(referencias o «todas»), se recarga de la librería en su posición, giro y cara. Al cargar una huella,
un modelo 3D de la librería que no existe se sustituye por el de ../libraries/3d con el mismo nombre.
Trabaja sobre una copia: solo escribe el .kicad_pcb de -o. Da los cambios y la paridad del
resultado (sale con 1 si no es cero). Se relanza con el Python de KiCad si hace falta.
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import (Fallo, cli, con_python_kicad, copia_trabajo, emitir, leer_netlist,  # noqa: E402
                    modelo_de_respaldo, principal, proyecto, ruta_huella)

ORDEN = ["J", "F", "D", "Q", "U", "L", "JP", "SW", "C", "R", "TP", "H"]
PROPIOS = ("Reference", "Value", "Footprint", "Datasheet", "Description")


def prefijo(ref):
    return re.match(r"[^\d]*", ref).group(0)


def orden_ref(ref):
    pre = prefijo(ref)
    n = re.search(r"\d+", ref)
    return (ORDEN.index(pre) if pre in ORDEN else 99, pre, int(n.group(0)) if n else 0)


def sincronizar(pcb_entrada, pcb_salida, net, carpeta, conservar=False, actualizar=(), libs3d=None):
    import pcbnew

    board = pcbnew.LoadBoard(str(pcb_entrada))
    comps, redes = net["comps"], net["redes"]
    red_de = {nodo: nombre for nombre, nodos in redes.items() for nodo in nodos}
    informe = {"nuevas": [], "borradas": [], "recargadas": [], "redes": [], "campos": [], "sobrantes": [], "avisos": [],
               "modelos": []}

    def ruta_de(c):
        return c["ruta"] + c["uuid"]

    def cargar(fpid, ref):
        archivo = ruta_huella(fpid, carpeta)
        if archivo is None or not archivo.is_file():
            raise Fallo(f"no se encuentra la huella {fpid}")
        fp = pcbnew.FootprintLoad(str(archivo.parent), archivo.stem)
        if fp is None:
            raise Fallo(f"pcbnew no carga la huella {fpid}")
        apodo, nombre = fpid.split(":", 1)
        fp.SetFPID(pcbnew.LIB_ID(apodo, nombre))
        modelos = fp.Models()  # por índice: iterar da copias
        for i in range(len(modelos)):
            nueva = modelo_de_respaldo(modelos[i].m_Filename, libs3d)
            if nueva:
                modelos[i].m_Filename = nueva
                informe["modelos"].append(ref)
        return fp

    por_ruta = {fp.GetPath().AsString(): fp for fp in board.GetFootprints()}
    por_ref = {fp.GetReference(): fp for fp in board.GetFootprints()}
    asignada = {}
    for ref, c in comps.items():
        fp = por_ruta.get(ruta_de(c)) or por_ref.get(ref)
        if fp is not None and fp.GetReference() not in asignada.values():
            asignada[ref] = fp.GetReference()
    usadas = set(asignada.values())
    for fp in list(board.GetFootprints()):
        if fp.GetReference() not in usadas:
            if conservar or not fp.GetPath().AsString().strip("/"):
                informe["sobrantes"].append(fp.GetReference())   # sin símbolo: huellas solo de placa o conservadas
            else:
                informe["borradas"].append(fp.GetReference())
                board.RemoveNative(fp)  # Remove() pasa la huella a Python y, al destruirla, pcbnew queda inestable
    huellas = {ref: por_ref[vieja] for ref, vieja in asignada.items()}

    netinfo = {}
    for nombre in redes:
        ni = board.FindNet(nombre)
        if ni is None:
            ni = pcbnew.NETINFO_ITEM(board, nombre)
            board.Add(ni)
        netinfo[nombre] = ni

    todas = "todas" in actualizar
    for ref, c in comps.items():
        fp = huellas.get(ref)
        if fp is not None and (fp.GetFPIDAsString() != c["footprint"] or todas or ref in actualizar):
            nueva = cargar(c["footprint"], ref)
            vuelta, giro, pos, bloqueada = fp.IsFlipped(), fp.GetOrientationDegrees(), fp.GetPosition(), fp.IsLocked()
            board.RemoveNative(fp)
            board.Add(nueva)  # antes de girarla: SetLayerAndFlip sobre una huella sin placa cuelga pcbnew
            if vuelta:
                nueva.SetLayerAndFlip(pcbnew.B_Cu)
            nueva.SetOrientationDegrees(giro)
            nueva.SetPosition(pcbnew.VECTOR2I(pos.x, pos.y))
            nueva.SetLocked(bloqueada)
            informe["recargadas"].append(ref)
            fp = huellas[ref] = nueva
        elif fp is None:
            fp = huellas[ref] = cargar(c["footprint"], ref)
            board.Add(fp)
            informe["nuevas"].append(ref)
        if fp.GetReference() != ref:
            fp.SetReference(ref)
        if fp.GetValue() != c["value"]:
            if ref not in informe["nuevas"] and ref not in informe["recargadas"]:
                informe["campos"].append(f"{ref}: Value «{fp.GetValue()}» → «{c['value']}»")
            fp.SetValue(c["value"])
        fp.SetPath(pcbnew.KIID_PATH(ruta_de(c)))
        fp.SetSheetname(c["nombres"])
        fp.SetSheetfile(c["props"].get("Sheetfile", ""))
        fp.SetExcludedFromBOM("exclude_from_bom" in c["props"])
        if fp.IsExcludedFromPosFiles() and "exclude_from_pos_files" not in c["props"]:
            # la huella (o su librería) se excluye de las posiciones y el símbolo no: se conserva y se avisa
            informe["avisos"].append(f"{ref}: fuera de los archivos de posición en la huella y no en el símbolo (se conserva)")
        else:
            fp.SetExcludedFromPosFiles("exclude_from_pos_files" in c["props"])
        fp.SetDNP("dnp" in c["props"])
        for campo, valor in c["campos"].items():
            if campo in ("Reference", "Value", "Footprint"):
                continue
            if (fp.GetFieldText(campo) if fp.HasField(campo) else None) != valor:
                if ref not in informe["nuevas"] and ref not in informe["recargadas"]:
                    informe["campos"].append(f"{ref}: {campo}")
                fp.SetField(campo, valor)
        for campo in fp.GetFields():
            if campo.GetName() not in ("Reference", "Value"):
                campo.SetVisible(False)
            if campo.GetName() not in PROPIOS:
                campo.SetLayer(pcbnew.B_Fab if fp.IsFlipped() else pcbnew.F_Fab)
        for pad in fp.Pads():
            numero = pad.GetNumber()
            if not numero:
                continue
            red = red_de.get((ref, numero), "")
            if pad.GetNetname() != red:
                if ref not in informe["nuevas"] and ref not in informe["recargadas"]:
                    informe["redes"].append(f"{ref}.{numero}: «{pad.GetNetname()}» → «{red}»")
                if red:
                    pad.SetNet(netinfo[red])
                else:
                    pad.SetNetCode(0)

    # huellas nuevas: en filas debajo de todo lo que ya hay, sin tocar lo colocado
    if informe["nuevas"]:
        fondo = board.GetBoardEdgesBoundingBox()
        x0 = pcbnew.ToMM(fondo.GetX()) if fondo.GetWidth() else 20.0
        x1 = max(x0 + 80.0, pcbnew.ToMM(fondo.GetRight()) if fondo.GetWidth() else 0)
        y = pcbnew.ToMM(fondo.GetBottom()) if fondo.GetHeight() else 20.0
        for fp in board.GetFootprints():
            if fp.GetReference() not in informe["nuevas"]:
                y = max(y, pcbnew.ToMM(fp.GetBoundingBox(False).GetBottom()))
        x, y, fila, grupo_ant, sep = x0, y + 10.0, 0.0, None, 1.5
        for ref in sorted(informe["nuevas"], key=orden_ref):
            fp = huellas[ref]
            fp.SetPosition(pcbnew.VECTOR2I(0, 0))
            caja = fp.GetBoundingBox(False)
            ancho, alto = pcbnew.ToMM(caja.GetWidth()), pcbnew.ToMM(caja.GetHeight())
            if grupo_ant is not None and prefijo(ref) != grupo_ant:
                x, y, fila = x0, y + fila + 4.0, 0.0
            if x + ancho > x1 and x > x0:
                x, y, fila = x0, y + fila + sep, 0.0
            fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x - pcbnew.ToMM(caja.GetX())), pcbnew.FromMM(y - pcbnew.ToMM(caja.GetY()))))
            x, fila, grupo_ant = x + ancho + sep, max(fila, alto), prefijo(ref)

    board.BuildConnectivity()
    pcbnew.SaveBoard(str(pcb_salida), board)
    informe["huellas"] = len(board.GetFootprints())
    return informe


def paridad(pcb, tmp):
    salida = Path(tmp) / "_drc.json"
    cli("pcb", "drc", "--format", "json", "--severity-all", "--schematic-parity", "-o", salida, pcb, comprobar=salida)
    drc = json.loads(salida.read_text(encoding="utf-8"))
    return drc.get("schematic_parity", []), len(drc.get("unconnected_items", []))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("proyecto", help="carpeta del proyecto, .kicad_pro o .kicad_pcb")
    ap.add_argument("-o", "--salida", required=True, help=".kicad_pcb de destino")
    ap.add_argument("--conservar", action="store_true", help="no borra las huellas sin símbolo")
    ap.add_argument("--actualizar", default="", metavar="REFS", help="recarga de la librería estas huellas (R1,U3 o «todas»)")
    ap.add_argument("--detalle", metavar="ARCHIVO", help="guarda la lista completa de cambios")
    args = ap.parse_args()
    con_python_kicad(__file__)

    carpeta, nombre = proyecto(args.proyecto)
    if not (carpeta / f"{nombre}.kicad_pcb").is_file() or not (carpeta / f"{nombre}.kicad_sch").is_file():
        raise Fallo(f"faltan {nombre}.kicad_sch o {nombre}.kicad_pcb en {carpeta}")
    with copia_trabajo(carpeta) as copia:
        red = copia / "_netlist.net"
        cli("sch", "export", "netlist", "--format", "kicadsexpr", "-o", red, copia / f"{nombre}.kicad_sch", comprobar=red)
        pcb = copia / f"{nombre}.kicad_pcb"
        r = sincronizar(pcb, pcb, leer_netlist(red), copia, conservar=args.conservar,
                        actualizar=tuple(x for x in args.actualizar.split(",") if x),
                        libs3d=carpeta.parent / "libraries" / "3d")
        incidencias, sin_conectar = paridad(pcb, copia)
        destino = Path(args.salida).resolve()
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(pcb, destino)

    tipos = {}
    for v in incidencias:
        tipos[v.get("type")] = tipos.get(v.get("type"), 0) + 1
    lineas = [f"{destino}: {r['huellas']} huellas · nuevas {len(r['nuevas'])} · borradas {len(r['borradas'])} · recargadas "
              f"{len(r['recargadas'])} · redes cambiadas {len(r['redes'])} · campos cambiados {len(r['campos'])}",
              f"Paridad {len(incidencias)}" + (f" {tipos}" if tipos else "") + f" · sin conectar {sin_conectar}"]
    for clave, titulo in (("nuevas", "Nuevas (sin colocar)"), ("borradas", "Borradas"), ("recargadas", "Recargadas"),
                          ("sobrantes", "Sin símbolo, conservadas"),
                          ("modelos", "Modelo 3D de respaldo (${KIPRJMOD}/../libraries/3d)")):
        if r[clave]:
            lineas.append(f"{titulo}: {' '.join(sorted(r[clave], key=orden_ref))}"[:400])
    lineas += r["avisos"] + r["redes"] + r["campos"]
    emitir(lineas, detalle=args.detalle)
    return 1 if incidencias else 0


if __name__ == "__main__":
    principal(main)
