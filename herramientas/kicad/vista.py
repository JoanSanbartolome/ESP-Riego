"""Imagen PNG de una hoja del esquema, de la placa, de una zona o de una huella.

Uso:
    python herramientas/kicad/vista.py hoja hardware/v2 --hoja MCU -o mcu.png
    python herramientas/kicad/vista.py hoja hardware/v2 --hoja MCU --zona 150,95,280,190 -o u5.png
    python herramientas/kicad/vista.py placa hardware/v2 -o placa.png [--todo | --zona 0,0,50,35] [--capas F.Cu,Edge.Cuts]
    python herramientas/kicad/vista.py huella esp-riego:ESP32-S3-WROOM-1 --proyecto hardware/v2 -o huella.png [--3d]
    python herramientas/kicad/vista.py 3d hardware/v2 -o placa3d.png [--cara bottom]

hoja y placa aceptan la carpeta del proyecto, el .kicad_pro o el archivo. --zona va en mm, en las
coordenadas de la hoja o de la placa (x0,y0,x1,y1). placa enseña por defecto el contorno con 5 mm
de margen; --todo incluye las huellas que están fuera. huella monta la pieza en una placa de prueba
(origen en 50,50): en 2D enseña cobre, pasta, serigrafía y patio, y con --3d el modelo sobre los pads. kicad-cli exporta a SVG sobre una copia
temporal del proyecto y la imagen se rasteriza con el wx del Python de KiCad (se relanza solo).
Escribe únicamente el PNG de -o e imprime su ruta y tamaño: después hay que mirarlo.
"""
import argparse
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import (Fallo, cli, con_python_kicad, copia_trabajo, emitir, hojas, leer, parse,  # noqa: E402
                    principal, proyecto, ruta_huella, trozos, uno)

CAPAS_PLACA = "B.Cu,F.Cu,B.SilkS,F.SilkS,F.Fab,F.CrtYd,Edge.Cuts"
CAPAS_INFERIOR = "F.Cu,B.Cu,F.SilkS,B.SilkS,B.Fab,B.CrtYd,Edge.Cuts"
CAPAS_HUELLA = "B.Cu,F.Cu,F.Paste,F.SilkS,F.CrtYd"


def rasterizar(svg, png, ancho, zona=None, fondo=(255, 255, 255)):
    """SVG → PNG de `ancho` píxeles, recortado a `zona` (unidades del viewBox, mm)."""
    import wx

    app = wx.App(False)  # noqa: F841
    wx.Log.EnableLogging(False)
    texto = Path(svg).read_text(encoding="utf-8")
    m = re.search(r'viewBox="\s*([-\d.]+)[ ,]+([-\d.]+)[ ,]+([-\d.]+)[ ,]+([-\d.]+)"', texto)
    if not m:
        raise Fallo("el SVG no tiene viewBox")
    x0, y0, w, h = map(float, m.groups())
    if zona:
        x0, y0, w, h = zona[0], zona[1], zona[2] - zona[0], zona[3] - zona[1]
        if w <= 0 or h <= 0:
            raise Fallo("--zona: x1 > x0 e y1 > y0")
        i = texto.index("<svg")
        j = texto.index(">", i)
        cab = re.sub(r'viewBox="[^"]+"', f'viewBox="{x0:g} {y0:g} {w:g} {h:g}"', texto[i:j])
        cab = re.sub(r'\bwidth="[^"]+"', f'width="{w:g}mm"', cab)
        cab = re.sub(r'\bheight="[^"]+"', f'height="{h:g}mm"', cab)
        texto = texto[:i] + cab + texto[j:]
    alto = max(1, round(ancho * h / w))
    lote = wx.BitmapBundle.FromSVG(texto.encode("utf-8"), wx.Size(ancho, alto))
    if not lote.IsOk():
        raise Fallo("wx no ha podido leer el SVG")
    lienzo = wx.Bitmap(ancho, alto)
    dc = wx.MemoryDC(lienzo)
    dc.SetBackground(wx.Brush(wx.Colour(*fondo)))
    dc.Clear()
    dc.DrawBitmap(lote.GetBitmap(wx.Size(ancho, alto)), 0, 0, True)
    dc.SelectObject(wx.NullBitmap)
    Path(png).parent.mkdir(parents=True, exist_ok=True)
    if not lienzo.ConvertToImage().SaveFile(str(png), wx.BITMAP_TYPE_PNG):
        raise Fallo(f"no se pudo escribir {png}")
    return ancho, alto, (x0, y0, x0 + w, y0 + h)


def caja_placa(pcb, todo=False):
    """Caja (x0, y0, x1, y1) del contorno o, con `todo`, del contorno y todas las huellas."""
    texto = leer(pcb)
    xs, ys = [], []
    for nombre, i, j in trozos(texto):
        if nombre.startswith("gr_") and '"Edge.Cuts"' in texto[i:j]:
            nodo = parse(texto[i:j])
            for k in ("start", "end", "mid", "center"):
                if uno(nodo, k):
                    xs.append(float(uno(nodo, k)[1])); ys.append(float(uno(nodo, k)[2]))
            for xy in [p for p in (uno(nodo, "pts") or []) if isinstance(p, list) and p[0] == "xy"]:
                xs.append(float(xy[1])); ys.append(float(xy[2]))
        elif nombre == "footprint" and (todo or not xs):
            m = re.search(r"\(at ([-\d.]+) ([-\d.]+)", texto[i:i + 400])
            if m and todo:
                xs += [float(m.group(1)) - 8, float(m.group(1)) + 8]; ys += [float(m.group(2)) - 8, float(m.group(2)) + 8]
    if not xs:
        raise Fallo("la placa no tiene contorno ni huellas: usa --zona")
    margen = 5.0
    return (min(xs) - margen, min(ys) - margen, max(xs) + margen, max(ys) + margen)


def zona_de(texto):
    if not texto:
        return None
    try:
        z = [float(v) for v in texto.split(",")]
        assert len(z) == 4
        return z
    except (ValueError, AssertionError):
        raise Fallo("--zona x0,y0,x1,y1 en mm")


def orden_hoja(args, tmp):
    carpeta, nombre = proyecto(args.origen)
    lista = hojas(carpeta / f"{nombre}.kicad_sch")
    elegida = lista[0]
    if args.hoja:
        elegida = next((h for h in lista if args.hoja.lower() in (h["nombre"].lower(), h["archivo"].name.lower(), h["archivo"].stem.lower())), None)
        if elegida is None:
            raise Fallo(f"no hay ninguna hoja «{args.hoja}»: {', '.join(h['nombre'] for h in lista)}")
    with copia_trabajo(carpeta) as copia:
        cli("sch", "export", "svg", "-o", tmp, copia / f"{nombre}.kicad_sch")
    sufijo = elegida["nombres"].strip("/").replace("/", "-")
    svg = Path(tmp) / (f"{nombre}-{sufijo}.svg" if sufijo else f"{nombre}.svg")
    if not svg.is_file():
        raise Fallo(f"kicad-cli no ha generado {svg.name}: {', '.join(p.name for p in Path(tmp).glob('*.svg'))}")
    return svg, zona_de(args.zona), f"hoja {elegida['nombre']}"


def orden_placa(args, tmp):
    carpeta, nombre = proyecto(args.origen)
    capas = args.capas or (CAPAS_INFERIOR if args.cara == "inferior" else CAPAS_PLACA)
    svg = Path(tmp) / "placa.svg"
    with copia_trabajo(carpeta) as copia:
        pcb = copia / f"{nombre}.kicad_pcb"
        zona = zona_de(args.zona) or caja_placa(pcb, args.todo)
        cli("pcb", "export", "svg", "--mode-single", "--page-size-mode", "1", "--exclude-drawing-sheet", "-l", capas,
            "-o", svg, pcb, comprobar=svg)
    return svg, zona, f"placa, capas {capas}"


CABECERA_BANCO = (
    '(kicad_pcb\n\t(version 20260206)\n\t(generator "pcbnew")\n\t(generator_version "10.0")\n'
    '\t(general (thickness 1.6) (legacy_teardrops no))\n\t(paper "A4")\n'
    '\t(layers\n\t\t(0 "F.Cu" signal)\n\t\t(2 "B.Cu" signal)\n\t\t(9 "F.Adhes" user "F.Adhesive")\n'
    '\t\t(11 "B.Adhes" user "B.Adhesive")\n\t\t(13 "F.Paste" user)\n\t\t(15 "B.Paste" user)\n'
    '\t\t(5 "F.SilkS" user "F.Silkscreen")\n\t\t(7 "B.SilkS" user "B.Silkscreen")\n\t\t(1 "F.Mask" user)\n'
    '\t\t(3 "B.Mask" user)\n\t\t(17 "Dwgs.User" user "User.Drawings")\n\t\t(19 "Cmts.User" user "User.Comments")\n'
    '\t\t(25 "Edge.Cuts" user)\n\t\t(27 "Margin" user)\n\t\t(31 "F.CrtYd" user "F.Courtyard")\n'
    '\t\t(29 "B.CrtYd" user "B.Courtyard")\n\t\t(35 "F.Fab" user)\n\t\t(33 "B.Fab" user)\n\t)\n'
    '\t(setup (pad_to_mask_clearance 0))\n\t(net 0 "")\n')


def banco(archivo, tmp, margen=2.0):
    """Placa de prueba con la huella en (50, 50); devuelve (pcb, caja de la huella con margen)."""
    import uuid

    import huella as _huella

    r = _huella.analizar(archivo)
    cajas = list(r["patio"].values()) or [[-5, -5, 5, 5]]
    caja = (50 + min(c[0] for c in cajas) - margen, 50 + min(c[1] for c in cajas) - margen,
            50 + max(c[2] for c in cajas) + margen, 50 + max(c[3] for c in cajas) + margen)
    libs = archivo.parent.parent  # .../libraries/<lib>.pretty/<huella>.kicad_mod
    texto = leer(archivo).replace("\r\n", "\n")
    texto = re.sub(r"^\t\((version|generator|generator_version) [^\n]*\n", "", texto, flags=re.M)
    m = re.match(r'\((?:footprint|module) "([^"]+)"', texto)
    texto = texto.replace(m.group(0), f'(footprint "banco:{m.group(1)}"', 1)
    texto = texto.replace('\t(layer "F.Cu")\n', f'\t(layer "F.Cu")\n\t(uuid "{uuid.uuid4()}")\n\t(at 50 50)\n', 1)
    texto = texto.replace("${KIPRJMOD}/../libraries", str(libs).replace("\\", "/"))
    borde = (f'\t(gr_rect (start {caja[0]:g} {caja[1]:g}) (end {caja[2]:g} {caja[3]:g}) (stroke (width 0.05) (type solid)) '
             f'(fill no) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))\n')
    carpeta = Path(tmp) / "banco"
    carpeta.mkdir()
    pcb = carpeta / "banco.kicad_pcb"
    pcb.write_text(CABECERA_BANCO + borde + texto.rstrip() + "\n)\n", encoding="utf-8", newline="\n")
    return pcb, caja


def localizar_huella(args):
    carpeta = Path(args.proyecto).resolve() if args.proyecto else None
    archivo = Path(args.origen)
    if not archivo.is_file():
        archivo = ruta_huella(args.origen, carpeta)
        if archivo is None or not archivo.is_file():
            raise Fallo(f"no se encuentra la huella {args.origen}")
    return archivo.resolve()


def orden_huella(args, tmp):
    archivo = localizar_huella(args)
    pcb, caja = banco(archivo, tmp)
    svg = Path(tmp) / "huella.svg"
    cli("pcb", "export", "svg", "--mode-single", "--page-size-mode", "1", "--exclude-drawing-sheet", "-l",
        args.capas or CAPAS_HUELLA, "-o", svg, pcb, comprobar=svg)
    return svg, zona_de(args.zona) or caja, f"huella {archivo.stem} (origen en 50,50)"


def orden_huella_3d(args):
    archivo = localizar_huella(args)
    destino = Path(args.salida).resolve()
    destino.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="vista_") as tmp:
        pcb, _ = banco(archivo, tmp, margen=3.0)
        png = Path(tmp) / "h3d.png"
        cli("pcb", "render", "--side", "bottom" if args.cara == "inferior" else "top", "--width", args.ancho,
            "--height", args.ancho, "--background", "opaque", "-o", png, pcb, comprobar=png)
        shutil.copyfile(png, destino)
    emitir([f"{destino}: render 3D de la huella {archivo.stem}, cara {args.cara}, {args.ancho} × {args.ancho} px"])
    return 0


def orden_3d(args):
    carpeta, nombre = proyecto(args.origen)
    destino = Path(args.salida).resolve()
    destino.parent.mkdir(parents=True, exist_ok=True)
    with copia_trabajo(carpeta, con_3d=True) as copia:
        png = copia / "_3d.png"
        cli("pcb", "render", "--side", args.cara, "--width", args.ancho, "--height", round(args.ancho * 0.7), "--zoom", args.zoom,
            "--background", "opaque", "-o", png, copia / f"{nombre}.kicad_pcb", comprobar=png)
        shutil.copyfile(png, destino)
    emitir([f"{destino}: render 3D, cara {args.cara}, {args.ancho} × {round(args.ancho * 0.7)} px"])
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="orden", required=True)
    for nombre, ayuda in (("hoja", "una hoja del esquema"), ("placa", "la placa en 2D, por capas"),
                          ("huella", "una huella de librería"), ("3d", "render 3D de la placa")):
        p = sub.add_parser(nombre, help=ayuda)
        p.add_argument("origen", help="proyecto, archivo o «Lib:Nombre»")
        p.add_argument("-o", "--salida", required=True, help="PNG de destino")
        p.add_argument("--ancho", type=int, default=2000, help="ancho en píxeles (por defecto, 2000)")
        if nombre != "3d":
            p.add_argument("--zona", metavar="x0,y0,x1,y1", help="recorte en mm")
        if nombre == "hoja":
            p.add_argument("--hoja", help="nombre de la hoja o de su archivo (por defecto, la raíz)")
        if nombre in ("placa", "huella"):
            p.add_argument("--capas", help="lista de capas separadas por comas")
        if nombre == "placa":
            p.add_argument("--todo", action="store_true", help="incluye las huellas que están fuera del contorno")
            p.add_argument("--cara", choices=("superior", "inferior"), default="superior", help="capas por defecto de esa cara")
        if nombre == "huella":
            p.add_argument("--proyecto", help="carpeta del proyecto (fp-lib-table)")
            p.add_argument("--3d", dest="tres_d", action="store_true", help="render 3D sobre una placa de prueba (pin 1 del modelo)")
            p.add_argument("--cara", choices=("superior", "inferior"), default="superior")
        if nombre == "3d":
            p.add_argument("--cara", choices=("top", "bottom", "left", "right", "front", "back"), default="top")
            p.add_argument("--zoom", type=float, default=1.0)
    args = ap.parse_args()
    if args.orden == "3d":
        return orden_3d(args)
    if args.orden == "huella" and args.tres_d:
        return orden_huella_3d(args)
    con_python_kicad(__file__, "wx")
    with tempfile.TemporaryDirectory(prefix="vista_") as tmp:
        svg, zona, que = {"hoja": orden_hoja, "placa": orden_placa, "huella": orden_huella}[args.orden](args, tmp)
        destino = Path(args.salida).resolve()
        ancho, alto, caja = rasterizar(svg, destino, args.ancho, zona)
    emitir([f"{destino}: {que}, {ancho} × {alto} px, zona {caja[0]:g},{caja[1]:g} a {caja[2]:g},{caja[3]:g} mm"])
    return 0


if __name__ == "__main__":
    principal(main)
