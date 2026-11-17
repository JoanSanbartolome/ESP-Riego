"""Genera o actualiza una hoja de esquema desde una descripción JSON de piezas y redes.

Uso:
    python herramientas/kicad/hoja.py pines RF_Module:ESP32-S3-WROOM-1 [--proyecto hardware/v2]
    python herramientas/kicad/hoja.py extraer hardware/v2/mcu.kicad_sch -o mcu.json
    python herramientas/kicad/hoja.py generar mcu.json --proyecto <copia>/v2 -o <copia>/v2/mcu.kicad_sch
    python herramientas/kicad/hoja.py raiz raiz.json --proyecto <copia>/v2 -o <copia>/v2/esp-riego.kicad_sch
    python herramientas/kicad/hoja.py netlist hardware/v2 <copia>/v2 [--hoja MCU] [--grupos]
    python herramientas/kicad/hoja.py netlist hardware/v2 --plan docs/diseno/conectores.md [--seccion "Anexo A"]

Formatos en herramientas/kicad/README.md. Conexión de un pin o de un punto de `etiquetas`: "L:RED" local ·
"H:RED:forma" jerárquica · "G:RED:forma" global · "P:GND[:giro]" símbolo de `power` · "NC" · "W" cable · "".
Cables, uniones (automáticas), recuadros con título y subhojas, también repetidas (`refs` por instancia).
generar escribe solo en -o y conserva los UUID y las #PWR de la hoja que sustituye. Sin varias unidades.
raiz: pines de hoja y sus etiquetas o NC en la raíz (--extraer saca la descripción de la raíz actual).
"""
import argparse
import json
import math
import re
import sys
import tempfile
import uuid as _uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import (CAMPOS, Fallo, comparar_grupos, comparar_netlists, emitir, esc, escribir,  # noqa: E402
                    exportar_netlist, hijos, hojas, leer, num, parse, parse_cabecera, principal, proyecto,
                    ruta_simbolos, simbolos_hoja, trozos, uno, val)
import campos as _campos  # noqa: E402

NO_REPRESENTABLE = ("bus", "bus_entry", "polyline", "rectangle", "circle", "arc", "netclass_flag", "image", "bezier",
                    "rule_area", "table")
ANGULO = {"R": 0, "U": 90, "L": 180, "D": 270}
LADO_DE = {0: "R", 90: "U", 180: "L", 270: "D"}
FORMAS = ("input", "output", "bidirectional", "tri_state", "passive")
TOL = 1e-3


def U():
    return str(_uuid.uuid4())


def clave(x, y):
    return (round(float(x), 3), round(float(y), 3))


# ------------------------------------------------------------------ cables y uniones

def en_tramo(p, a, b):
    """El punto p está en el segmento a-b (extremos incluidos)."""
    (px, py), (ax, ay), (bx, by) = p, a, b
    largo = math.hypot(bx - ax, by - ay)
    if largo < TOL or abs((bx - ax) * (py - ay) - (by - ay) * (px - ax)) > TOL * largo:
        return False
    return min(ax, bx) - TOL <= px <= max(ax, bx) + TOL and min(ay, by) - TOL <= py <= max(ay, by) + TOL


def tramos_y_uniones(cables, pines=()):
    """Cables (polilíneas [[x, y], …]) → tramos partidos en los extremos de otros tramos y en los pines que caen en
    su interior (como hace KiCad al guardar), y uniones donde se juntan tres o más extremos (los pines cuentan)."""
    segs = []
    for c in cables:
        if len(c) < 2:
            raise Fallo(f"cable con menos de dos puntos: {c}")
        pts = [clave(*p) for p in c]
        segs += [(pts[k], pts[k + 1]) for k in range(len(pts) - 1) if pts[k] != pts[k + 1]]
    pin_pts = [clave(*p) for p in pines]
    interes = {p for s in segs for p in s} | set(pin_pts)
    tramos = []
    for a, b in segs:
        medio = sorted((p for p in interes if p != a and p != b and en_tramo(p, a, b)),
                       key=lambda p: (p[0] - a[0]) ** 2 + (p[1] - a[1]) ** 2)
        cadena = [a] + medio + [b]
        tramos += [tuple(sorted((cadena[k], cadena[k + 1]))) for k in range(len(cadena) - 1)]
    tramos = list(dict.fromkeys(tramos))
    grado = {}
    for t in tramos:
        for p in t:
            grado[p] = grado.get(p, 0) + 1
    for p in pin_pts:
        if p in grado:
            grado[p] += 1
    return tramos, sorted(p for p, g in grado.items() if g >= 3), grado


def toca(p, tramos):
    return any(en_tramo(p, a, b) for a, b in tramos)


# ------------------------------------------------------------------ símbolos de librería

def _nombre_simbolo(texto, i):
    return re.match(r'\(symbol\s+"((?:\\.|[^"\\])*)"', texto[i:i + 300]).group(1)


def bloque_libreria(spec, carpeta=None):
    """Texto del símbolo «Lib:Nombre» listo para `lib_symbols` (derivados aplanados)."""
    apodo, nombre = spec.split(":", 1)
    archivo = ruta_simbolos(apodo, carpeta)
    if not archivo.is_file():
        raise Fallo(f"no existe la librería de símbolos {archivo}")
    texto = leer(archivo).replace("\r\n", "\n")
    bloques = {_nombre_simbolo(texto, i): (i, j) for n, i, j in trozos(texto) if n == "symbol"}
    if nombre not in bloques:
        raise Fallo(f"no existe el símbolo {spec}")
    blk = texto[slice(*bloques[nombre])]
    m = re.search(r'\(extends "([^"]+)"\)', blk)
    if m:
        padre = m.group(1)
        pblk = texto[slice(*bloques[padre])]
        props_hijo = [blk[i:j] for n, i, j in trozos(blk) if n == "property"]
        props_padre = [(i, j) for n, i, j in trozos(pblk) if n == "property"]
        blk = pblk[:props_padre[0][0]] + "\n\t\t".join(props_hijo) + pblk[props_padre[-1][1]:]
        blk = blk.replace(f'(symbol "{padre}"', f'(symbol "{nombre}"', 1).replace(f'(symbol "{padre}_', f'(symbol "{nombre}_')
    blk = blk.replace(f'(symbol "{nombre}"', f'(symbol "{spec}"', 1)
    return "\t" + "\n".join(("\t" + ln) if ln else ln for ln in blk.split("\n"))


def pines_y_caja(nodo):
    """Pines (unidad 1, estilo 1) y caja del cuerpo de un símbolo de librería ya analizado."""
    pines, xs, ys, unidades = [], [], [], set()
    for sub in hijos(nodo, "symbol"):
        m = re.search(r"_(\d+)_(\d+)$", sub[1])
        unidad, estilo = (int(m.group(1)), int(m.group(2))) if m else (0, 1)
        unidades.add(unidad)
        if unidad > 1 or estilo > 1:
            continue
        for p in hijos(sub, "pin"):
            at = uno(p, "at")
            pines.append({"num": val(p, "number"), "nombre": val(p, "name"), "tipo": p[1],
                          "x": float(at[1]), "y": float(at[2]), "ang": int(float(at[3])) if len(at) > 3 else 0,
                          "largo": float(val(p, "length", "0")),
                          "oculto": val(p, "hide", "no") == "yes" or "hide" in p})
        for g in sub[2:]:
            if not isinstance(g, list):
                continue
            for k in ("start", "end", "center", "mid"):
                if uno(g, k):
                    xs.append(float(uno(g, k)[1])); ys.append(float(uno(g, k)[2]))
            for xy in hijos(uno(g, "pts", []), "xy"):
                xs.append(float(xy[1])); ys.append(float(xy[2]))
    for p in pines:
        xs.append(p["x"]); ys.append(p["y"])
    if max(unidades | {0}) > 1:
        raise Fallo(f"{nodo[1]}: los símbolos de varias unidades no están soportados")
    caja = (min(xs), min(ys), max(xs), max(ys)) if xs else (0, 0, 0, 0)
    props = {p[1]: p for p in hijos(nodo, "property")}
    return pines, caja, props


def cuerpo(nodo):
    """Caja del dibujo de un símbolo de librería (unidad 1), sin los pines; None si no tiene dibujo."""
    xs, ys = [], []
    for sub in hijos(nodo, "symbol"):
        m = re.search(r"_(\d+)_(\d+)$", sub[1])
        if m and (int(m.group(1)) > 1 or int(m.group(2)) > 1):
            continue
        for g in sub[2:]:
            if not isinstance(g, list) or g[0] in ("pin", "text"):
                continue
            r = float(val(g, "radius", "0"))
            w = float(val(uno(g, "stroke", []), "width", "0") or 0) / 2   # medio trazo
            for k in ("start", "end", "center", "mid"):
                if uno(g, k):
                    cx, cy = float(uno(g, k)[1]), float(uno(g, k)[2])
                    xs += [cx - r - w, cx + r + w]
                    ys += [cy - r - w, cy + r + w]
            for xy in hijos(uno(g, "pts", []), "xy"):
                xs += [float(xy[1]) - w, float(xy[1]) + w]
                ys += [float(xy[2]) - w, float(xy[2]) + w]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None


def girar(px, py, X, Y, giro):
    """Punto de librería (y hacia arriba) → hoja (y hacia abajo), con el giro del símbolo."""
    a = math.radians(giro)
    return (round(X + px * math.cos(a) - py * math.sin(a), 4), round(Y - (px * math.sin(a) + py * math.cos(a)), 4))


def lado(ang_pin, giro):
    """Hacia dónde sale el pin en la hoja: R, U, L o D."""
    return {0: "R", 90: "U", 180: "L", 270: "D"}[int((ang_pin + giro + 180) % 360)]


# ------------------------------------------------------------------ extraer

def _claves_instancia(archivo):
    """{ruta de instancia: «Hoja/Subhoja»} del proyecto al que pertenece la hoja (vacío si no se encuentra)."""
    try:
        carpeta, nombre = proyecto(archivo)
        return {h["ruta"]: h["nombres"].strip("/") for h in hojas(carpeta / f"{nombre}.kicad_sch")[1:]}
    except (Fallo, OSError):
        return {}


def extraer(archivo, forzar=False):
    """Descripción de una hoja existente y lista de lo que no se puede representar."""
    texto = leer(archivo)
    cab = parse_cabecera(texto)
    libs = {}
    for n, i, j in trozos(texto):
        if n == "lib_symbols":
            for n2, a, b in trozos(texto, i):
                if n2 == "symbol":
                    nodo = parse(texto[a:b])
                    libs[nodo[1]] = pines_y_caja(nodo)
    perdidos, puntos, textos, banderas = [], {}, [], []
    cables, uniones, recuadros, subhojas = [], [], [], []
    for n, i, j in trozos(texto):
        if n in NO_REPRESENTABLE:
            perdidos.append(n)
            continue
        if n not in ("label", "hierarchical_label", "global_label", "no_connect", "text", "wire", "junction",
                     "text_box", "sheet"):
            continue
        nodo = parse(texto[i:j])
        at = uno(nodo, "at")
        if n in ("label", "hierarchical_label", "global_label"):
            con = {"label": f"L:{nodo[1]}", "hierarchical_label": f"H:{nodo[1]}:{val(nodo, 'shape')}",
                   "global_label": f"G:{nodo[1]}:{val(nodo, 'shape')}"}[n]
            lado_ = LADO_DE.get(int(float(at[3])) % 360 if len(at) > 3 else 0, "R")
            puntos.setdefault(clave(at[1], at[2]), []).append((con, lado_))
        elif n == "no_connect":
            puntos.setdefault(clave(at[1], at[2]), []).append(("NC", None))
        elif n == "text":
            fuente = uno(uno(nodo, "effects", []), "font", [])
            textos.append({"x": float(at[1]), "y": float(at[2]), "tam": float(val(fuente, "size", "1.27")),
                           "negrita": val(fuente, "bold", "no") == "yes", "texto": nodo[1]})
        elif n == "wire":
            cables.append([[float(p[1]), float(p[2])] for p in hijos(uno(nodo, "pts", []), "xy")])
        elif n == "junction":
            uniones.append([float(at[1]), float(at[2])])
        elif n == "text_box":
            tam = uno(nodo, "size")
            if val(uno(nodo, "stroke", []), "type") != "dash_dot":
                perdidos.append("text_box sin trazo y punto")
                continue
            recuadros.append({"x": float(at[1]), "y": float(at[2]), "ancho": float(tam[1]), "alto": float(tam[2]),
                              "titulo": nodo[1]})
        elif n == "sheet":
            tam = uno(nodo, "size")
            props = {p[1]: p[2] for p in hijos(nodo, "property") if len(p) > 2}
            pines_h = []
            for p in hijos(nodo, "pin"):
                pa = uno(p, "at")
                lado_ = {180: "L", 0: "R"}.get(int(float(pa[3])) if len(pa) > 3 else 0)
                if lado_ is None:
                    perdidos.append(f"pin de hoja {p[1]} arriba o abajo")
                    continue
                pines_h.append({"nombre": p[1], "forma": p[2], "lado": lado_, "y": float(pa[2])})
            subhojas.append({"nombre": props.get("Sheetname", ""), "archivo": props.get("Sheetfile", ""),
                             "x": float(at[1]), "y": float(at[2]), "ancho": float(tam[1]), "alto": float(tam[2]),
                             "pines": pines_h})
    simbolos = simbolos_hoja(texto)
    for s in simbolos:
        if s["espejo"]:
            raise Fallo(f"{s['ref']}: símbolo espejado, no soportado")
        if s["lib_id"] == "power:PWR_FLAG":
            banderas.append([s["x"], s["y"]])
        elif s["lib_id"].startswith("power:"):
            for p in libs[s["lib_id"]][0]:
                x, y = girar(p["x"], p["y"], s["x"], s["y"], s["giro"])
                nombre = s["lib_id"].split(":", 1)[1]
                if s["props"].get("Value", nombre) != nombre:
                    raise Fallo(f"{s['ref']}: símbolo de alimentación con Value distinto de su nombre, no soportado")
                puntos.setdefault(clave(x, y), []).append((f"P:{nombre}" + (f":{s['giro']}" if s["giro"] else ""), None))
    tramos, _, _ = tramos_y_uniones(cables)
    rutas = _claves_instancia(archivo)
    piezas, usados = [], set()
    for s in simbolos:
        if s["lib_id"].startswith("power:"):
            continue
        pines = {}
        for p in libs[s["lib_id"]][0]:
            if p["oculto"]:
                continue
            k = clave(*girar(p["x"], p["y"], s["x"], s["y"], s["giro"]))
            cons = puntos.get(k, [])
            if len(cons) > 1:
                perdidos.append(f"{s['ref']}.{p['num']}: varias conexiones en el mismo punto {[c for c, _ in cons]}")
            pines[p["num"]] = cons[0][0] if cons else ("W" if toca(k, tramos) else "")
            usados.add(k)
        pos = {}
        for prop in hijos(s["nodo"], "property"):
            if prop[1] in ("Reference", "Value"):
                at = uno(prop, "at")
                just = uno(uno(prop, "effects", []), "justify")
                pos[prop[1]] = [float(at[1]), float(at[2]), int(float(at[3])), " ".join(just[1:]) if just else ""]
        campos = {k: v for k, v in s["props"].items() if k != "Reference"}
        pieza = {"ref": s["ref"], "simbolo": s["lib_id"], "x": s["x"], "y": s["y"], "giro": s["giro"],
                 "dnp": s["dnp"], "en_bom": s["in_bom"], "campos": campos, "pos": pos, "pines": pines}
        if len({r for _, r in s["instancias"]}) > 1:
            pieza["refs"] = {rutas.get(ruta, ruta): r for ruta, r in s["instancias"]}
        piezas.append(pieza)
    etiquetas = []
    for k, cons in puntos.items():
        if k in usados:
            continue
        for con, lado_ in cons:
            if con == "NC":
                perdidos.append(f"NC suelta en {k}")
                continue
            e = {"x": k[0], "y": k[1], "con": con}
            if lado_:
                e["lado"] = lado_
            etiquetas.append(e)
    tb = uno(cab, "title_block", [])
    cajetin = {k: val(tb, k) for k in ("title", "date", "rev", "company") if val(tb, k)}
    cajetin["comment"] = {c[1]: c[2] for c in hijos(tb, "comment")}
    desc = {"papel": val(cab, "paper", "A4"), "cajetin": cajetin, "piezas": piezas, "banderas": banderas,
            "textos": textos, "etiquetas": etiquetas, "cables": cables, "uniones": uniones, "recuadros": recuadros,
            "hojas": subhojas}
    return desc, perdidos


# ------------------------------------------------------------------ generar

def _prop(nombre, valor, x, y, ang=0, oculto=False, just=None):
    h = "\n\t\t\t(hide yes)" if oculto else ""
    j = f"\n\t\t\t\t(justify {just})" if just else ""
    return (f'\t\t(property "{esc(nombre)}" "{esc(valor)}"\n\t\t\t(at {num(x)} {num(y)} {int(ang)}){h}\n'
            "\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n"
            f"\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t){j}\n\t\t\t)\n\t\t)\n")


def _simbolo(lib, x, y, giro, props, pines, instancias, nombre_proy, uid, en_bom=True, dnp=False):
    """Bloque `symbol`; `instancias` = [(ruta, referencia)], una por cada instancia de la hoja."""
    sn = lambda b: "yes" if b else "no"  # noqa: E731
    s = (f'\t(symbol\n\t\t(lib_id "{esc(lib)}")\n\t\t(at {num(x)} {num(y)} {int(giro)})\n\t\t(unit 1)\n\t\t(body_style 1)\n'
         f"\t\t(exclude_from_sim no)\n\t\t(in_bom {sn(en_bom)})\n\t\t(on_board yes)\n\t\t(in_pos_files {sn(en_bom)})\n"
         f'\t\t(dnp {sn(dnp)})\n\t\t(uuid "{uid}")\n') + "".join(props)
    for numero, upin in pines:
        s += f'\t\t(pin "{esc(numero)}"\n\t\t\t(uuid "{upin}")\n\t\t)\n'
    rutas = "".join(f'\t\t\t\t(path "{ruta}"\n\t\t\t\t\t(reference "{esc(ref)}")\n\t\t\t\t\t(unit 1)\n\t\t\t\t)\n'
                    for ruta, ref in instancias)
    return s + f'\t\t(instances\n\t\t\t(project "{esc(nombre_proy)}"\n{rutas}\t\t\t)\n\t\t)\n\t)\n'


def _viejos(base):
    """UUID, referencias y páginas de la hoja que se sustituye, para conservarlos."""
    v = {"hoja": None, "sim": {}, "pin": {}, "pwr": {}, "otros": {}, "hojas": {}, "no_rep": []}
    if not base or not Path(base).is_file():
        return v
    texto = leer(base)
    v["hoja"] = val(parse_cabecera(texto), "uuid") or None
    for s in simbolos_hoja(texto):
        pins = {p[1]: val(p, "uuid") for p in hijos(s["nodo"], "pin")}
        if s["lib_id"].startswith("power:"):
            v["pwr"][(s["lib_id"],) + clave(s["x"], s["y"])] = (s["uuid"], s["ref"], pins.get("1"))
        else:
            for ref in {s["ref"]} | {r for _, r in s["instancias"]}:
                v["sim"][ref] = s["uuid"]
                v["pin"].update({(ref, n): u for n, u in pins.items()})
    for n, i, j in trozos(texto):
        if n in NO_REPRESENTABLE:
            v["no_rep"].append(n)
        elif n in ("label", "hierarchical_label", "global_label", "no_connect", "text"):
            nodo = parse(texto[i:j])
            at = uno(nodo, "at")
            v["otros"][(n, nodo[1] if n != "no_connect" else "") + clave(at[1], at[2])] = val(nodo, "uuid")
        elif n == "sheet":
            nodo = parse(texto[i:j])
            props = {p[1]: p[2] for p in hijos(nodo, "property") if len(p) > 2}
            v["hojas"][props.get("Sheetname", "")] = {
                "uuid": val(nodo, "uuid"), "pines": {p[1]: val(p, "uuid") for p in hijos(nodo, "pin")},
                "paginas": {pa[1]: val(pa, "page") for pr in hijos(uno(nodo, "instances", []), "project")
                            for pa in hijos(pr, "path")}}
    return v


def _pwr_usados(carpeta, nombre, excluir):
    usados = set()
    for h in hojas(Path(carpeta) / f"{nombre}.kicad_sch"):
        if h["archivo"].is_file() and h["archivo"].name != excluir:
            usados |= set(re.findall(r'\(reference "(#(?:PWR|FLG)\d+)"\)', leer(h["archivo"])))
    return usados


def _paginas_usadas(carpeta, nombre, excluir):
    usadas = {1}
    for h in hojas(Path(carpeta) / f"{nombre}.kicad_sch"):
        if h["archivo"].is_file() and h["archivo"].name != excluir:
            usadas |= {int(p) for p in re.findall(r'\(page "(\d+)"\)', leer(h["archivo"]))}
    return usadas


def _pos_defecto(X, Y, giro, pines, caja):
    pts = [girar(p["x"], p["y"], X, Y, giro) for p in pines] or [(X, Y)]
    esq = [girar(cx, cy, X, Y, giro) for cx in (caja[0], caja[2]) for cy in (caja[1], caja[3])]
    y0, y1 = min(p[1] for p in esq + pts), max(p[1] for p in esq + pts)
    ancho_p, alto_p = max(p[0] for p in pts) - min(p[0] for p in pts), max(p[1] for p in pts) - min(p[1] for p in pts)
    if len(pines) <= 3 and ancho_p < 1:      # pasivo vertical
        return {"Reference": [X + 2.54, Y - 1.27, 0, "left"], "Value": [X + 2.54, Y + 1.27, 0, "left"]}
    if len(pines) <= 3 and alto_p < 1:       # pasivo horizontal
        return {"Reference": [X, Y - 3.81, 0, ""], "Value": [X, Y + 3.81, 0, ""]}
    # cuerpo grande: a la derecha del eje, para no pisar los símbolos de alimentación de los pines centrales
    return {"Reference": [X + 3.81, y0 - 1.27, 0, "left"], "Value": [X + 3.81, y1 + 2.54, 0, "left"]}


def _etiqueta(tipo, nombre, forma, x, y, sd, uid):
    if tipo == "label":
        just = "left bottom" if sd in "RU" else "right bottom"
        return (f'\t(label "{esc(nombre)}"\n\t\t(at {num(x)} {num(y)} {ANGULO[sd]})\n\t\t(effects\n\t\t\t(font\n'
                f'\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify {just})\n\t\t)\n\t\t(uuid "{uid}")\n\t)\n')
    just = "left" if sd in "RU" else "right"
    return (f'\t({tipo} "{esc(nombre)}"\n\t\t(shape {forma})\n\t\t(at {num(x)} {num(y)} {ANGULO[sd]})\n\t\t(effects\n'
            f'\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify {just})\n\t\t)\n\t\t(uuid "{uid}")\n\t)\n')


def _recuadro(r):
    for k in ("x", "y", "ancho", "alto", "titulo"):
        if k not in r:
            raise Fallo(f"recuadro sin «{k}»: {r}")
    return (f'\t(text_box "{esc(r["titulo"])}"\n\t\t(exclude_from_sim no)\n\t\t(at {num(r["x"])} {num(r["y"])} 0)\n'
            f'\t\t(size {num(r["ancho"])} {num(r["alto"])})\n\t\t(margins 0.9525 0.9525 0.9525 0.9525)\n'
            "\t\t(stroke\n\t\t\t(width 0)\n\t\t\t(type dash_dot)\n\t\t)\n\t\t(fill\n\t\t\t(type none)\n\t\t)\n"
            "\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify left top)\n\t\t)\n"
            f'\t\t(uuid "{U()}")\n\t)\n')


def generar(desc, carpeta, nombre_proy, nombre_hoja, base=None, tabla=None, forzar=False):
    """Texto de la hoja y resumen. `carpeta`/`nombre_proy`: proyecto al que pertenece la hoja."""
    viejos = _viejos(base)
    if viejos["no_rep"] and not forzar:
        raise Fallo(f"la hoja que se sustituye tiene {len(viejos['no_rep'])} elementos que se perderían "
                    f"({', '.join(sorted(set(viejos['no_rep'])))}); usa --forzar si es lo que quieres")
    instancias = [h for h in hojas(Path(carpeta) / f"{nombre_proy}.kicad_sch")[1:] if h["archivo"].name == nombre_hoja]
    if not instancias:
        raise Fallo(f"{nombre_hoja} no cuelga de {nombre_proy}.kicad_sch: no se puede saber su ruta de instancia")
    rutas = [h["ruta"] for h in instancias]
    claves_inst = [h["nombres"].strip("/") for h in instancias]
    varias = len(instancias) > 1
    usados = _pwr_usados(carpeta, nombre_proy, nombre_hoja)
    contador = {"#PWR": 0, "#FLG": 0}

    def ref_nueva(prefijo):
        while True:
            contador[prefijo] += 1
            r = f"{prefijo}{contador[prefijo]:0{3 if prefijo == '#PWR' else 2}d}"
            if r not in usados:
                usados.add(r)
                return r

    libs_txt, libs = {}, {}

    def lib(spec):
        if spec not in libs:
            libs_txt[spec] = bloque_libreria(spec, carpeta)
            libs[spec] = pines_y_caja(parse(libs_txt[spec]))
        return libs[spec]

    reservadas = {r for (_, r, _) in viejos["pwr"].values()}
    usados |= reservadas
    simbolos, pwr, etiquetas, jerarquicas, globales, ncs, avisos = [], [], [], [], [], [], []
    puntos, pines_pts, cableados, anclas = {}, [], [], []

    def alimentacion(nombre, x, y, bandera=False, giro=0):
        spec = f"power:{nombre}"
        _, _, props = lib(spec)
        uid, ref, upin = viejos["pwr"].get((spec,) + clave(x, y), (None, None, None))
        refs = [ref or ref_nueva("#FLG" if bandera else "#PWR")]
        refs += [ref_nueva("#FLG" if bandera else "#PWR") for _ in rutas[1:]]

        def en(nombre_prop, defecto):
            at = uno(props.get(nombre_prop, []), "at", ["at", *defecto])
            return girar(float(at[1]), float(at[2]), x, y, giro)

        # Value horizontal y alejado del símbolo, como lo deja KiCad al girar (campo a 90° en los giros de 90 y 270;
        # en los de 90 y 180 KiCad invierte la justificación)
        vx, vy = en("Value", ("0", "-3.81"))
        just = None
        if abs(vx - x) > 0.01:
            just = "right" if vx < x else "left"
            if giro in (90, 180):
                just = {"right": "left", "left": "right"}[just]
        desc_ = props["Description"][2] if "Description" in props else ""
        ps = [_prop("Reference", refs[0], *en("Reference", ("0", "-6.35")), oculto=True),
              _prop("Value", nombre, vx, vy, 90 if giro in (90, 270) else 0, just=just),
              _prop("Footprint", "", x, y, oculto=True), _prop("Datasheet", "~" if bandera else "", x, y, oculto=True),
              _prop("Description", desc_, x, y, oculto=True)]
        pwr.append(_simbolo(spec, x, y, giro, ps, [("1", upin or U())], list(zip(rutas, refs)), nombre_proy, uid or U()))
        pines_pts.append((x, y))

    def poner(con, x, y, sd, quien):
        """Dibuja la conexión `con` en (x, y); `sd`: hacia dónde va la etiqueta (R, U, L, D)."""
        partes = con.split(":")
        if con in ("", "W"):
            return
        if con == "NC":
            uid = viejos["otros"].get(("no_connect", "") + clave(x, y)) or U()
            ncs.append(f'\t(no_connect\n\t\t(at {num(x)} {num(y)})\n\t\t(uuid "{uid}")\n\t)\n')
        elif partes[0] == "P" and len(partes) in (2, 3):
            if len(partes) == 3 and partes[2] not in ("0", "90", "180", "270"):
                raise Fallo(f"{quien}: giro «{partes[2]}» del símbolo de alimentación (0, 90, 180 o 270)")
            alimentacion(partes[1], x, y, giro=int(partes[2]) if len(partes) == 3 else 0)
        elif partes[0] == "L" and len(partes) == 2:
            uid = viejos["otros"].get(("label", partes[1]) + clave(x, y)) or U()
            etiquetas.append(_etiqueta("label", partes[1], None, x, y, sd, uid))
        elif partes[0] in "HG" and len(partes) == 3:
            if partes[2] not in FORMAS:
                raise Fallo(f"{quien}: forma «{partes[2]}» ({', '.join(FORMAS)})")
            tipo = "hierarchical_label" if partes[0] == "H" else "global_label"
            uid = viejos["otros"].get((tipo, partes[1]) + clave(x, y)) or U()
            (jerarquicas if partes[0] == "H" else globales).append(_etiqueta(tipo, partes[1], partes[2], x, y, sd, uid))
        else:
            raise Fallo(f"{quien}: conexión «{con}» no reconocida")

    refs_vistas = set()
    for pz in desc.get("piezas", []):
        spec, X, Y, giro = pz["simbolo"], float(pz["x"]), float(pz["y"]), int(pz.get("giro", 0))
        if varias:
            refs_i = pz.get("refs") or {}
            faltan = [c for c in claves_inst if c not in refs_i]
            if faltan:
                raise Fallo(f"{pz.get('ref', spec)}: la hoja tiene {len(rutas)} instancias y faltan las referencias de "
                            f"{', '.join(faltan)} en «refs»")
            inst = [(r, refs_i[c]) for r, c in zip(rutas, claves_inst)]
        else:
            inst = [(rutas[0], pz["ref"])]
        ref = pz.get("ref") or inst[0][1]
        for _, r in inst:
            if r in refs_vistas:
                raise Fallo(f"{r}: referencia repetida en la descripción")
            refs_vistas.add(r)
        pines, caja, props_lib = lib(spec)
        campos = dict(pz.get("campos", {}))
        fila = (tabla or {}).get(ref, {})
        campos.update({k: v for k, v in fila.items() if k != "DNP"})
        dnp = fila["DNP"] if fila.get("DNP") is not None else bool(pz.get("dnp", False))
        pos_dada, pos_def = pz.get("pos", {}), _pos_defecto(X, Y, giro, pines, caja)
        ps = []
        for nombre_c, valor in [("Reference", ref), ("Value", campos.get("Value", spec.split(":")[1]))]:
            if nombre_c in pos_dada:
                px, py, pa, pj = pos_dada[nombre_c]
            else:  # el ángulo del campo es relativo al símbolo: así se lee horizontal
                (px, py, _, pj), pa = pos_def[nombre_c], (360 - giro) % 360
            ps.append(_prop(nombre_c, valor, px, py, pa, just=pj or None))
        orden = ["Footprint", "Datasheet", "Description"] + [k for k in campos if k not in ("Value", "Footprint", "Datasheet", "Description")]
        for nombre_c in orden:
            ps.append(_prop(nombre_c, campos.get(nombre_c, ""), X, Y, oculto=True))
        faltan = [c for c in CAMPOS if not campos.get(c)] if pz.get("en_bom", True) else []
        if faltan:
            avisos.append(f"{ref}: campos vacíos {', '.join(faltan)}")
        upins = [(p["num"], viejos["pin"].get((ref, p["num"])) or U()) for p in pines]
        simbolos.append(_simbolo(spec, X, Y, giro, ps, upins, inst, nombre_proy, viejos["sim"].get(ref) or U(),
                                 en_bom=pz.get("en_bom", True), dnp=dnp))
        visibles = {p["num"]: p for p in pines if not p["oculto"]}
        conexiones = pz.get("pines", {})
        sin_declarar = sorted(set(visibles) - set(conexiones))
        if sin_declarar:
            raise Fallo(f"{ref}: pines sin conexión declarada: {', '.join(sin_declarar)}")
        for numero, con in conexiones.items():
            if numero not in visibles:
                raise Fallo(f"{ref}: el símbolo {spec} no tiene el pin {numero}")
            p = visibles[numero]
            x, y = girar(p["x"], p["y"], X, Y, giro)
            puntos.setdefault(clave(x, y), []).append(f"{ref}.{numero}")
            pines_pts.append((x, y))
            if con == "W":
                cableados.append((f"{ref}.{numero}", clave(x, y)))
            poner(con, x, y, lado(p["ang"], giro), f"{ref}.{numero}")
    for x, y in desc.get("banderas", []):
        alimentacion("PWR_FLAG", float(x), float(y), bandera=True)
    for e in desc.get("etiquetas", []):
        quien = f"etiqueta {e.get('con')} en ({num(e['x'])}, {num(e['y'])})"
        sd = e.get("lado", "R")
        if sd not in ANGULO:
            raise Fallo(f"{quien}: lado «{sd}» (R, U, L o D)")
        if e.get("con", "") in ("", "W", "NC"):
            raise Fallo(f"{quien}: en `etiquetas` solo L, H, G o P")
        poner(e["con"], float(e["x"]), float(e["y"]), sd, quien)
        anclas.append((quien, clave(e["x"], e["y"])))
    for k, quienes in puntos.items():
        if len(quienes) > 1:
            avisos.append(f"pines en el mismo punto {k}: {' '.join(quienes)} (quedan unidos)")

    # subhojas (también varias instancias de un mismo archivo)
    hojas_txt, paginas = [], _paginas_usadas(carpeta, nombre_proy, nombre_hoja)
    nombres_h = set()
    for hj in desc.get("hojas", []):
        nombre, archivo_h = hj["nombre"], hj["archivo"]
        if nombre in nombres_h:
            raise Fallo(f"subhoja «{nombre}» repetida")
        nombres_h.add(nombre)
        x0, y0, ancho, alto = (float(hj[k]) for k in ("x", "y", "ancho", "alto"))
        viejo = viejos["hojas"].get(nombre, {})
        pines_txt, vistos = "", set()
        for p in hj.get("pines", []):
            if p.get("lado") not in ("L", "R") or p.get("forma") not in FORMAS or p["nombre"] in vistos:
                raise Fallo(f"{nombre}.{p.get('nombre')}: pin de subhoja repetido o con lado (L o R) o forma no válidos")
            vistos.add(p["nombre"])
            px, py = (x0 if p["lado"] == "L" else x0 + ancho), float(p["y"])
            if not y0 < py < y0 + alto:
                raise Fallo(f"{nombre}.{p['nombre']}: y = {num(py)} fuera del borde de la subhoja")
            ang, just = (180, "left") if p["lado"] == "L" else (0, "right")
            pines_txt += (f'\t\t(pin "{esc(p["nombre"])}" {p["forma"]}\n\t\t\t(at {num(px)} {num(py)} {ang})\n'
                          f'\t\t\t(uuid "{viejo.get("pines", {}).get(p["nombre"]) or U()}")\n'
                          f"\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(justify {just})\n\t\t\t)\n\t\t)\n")
            pines_pts.append((px, py))
        paths = ""
        for ruta in rutas:
            pagina = viejo.get("paginas", {}).get(ruta)
            if not pagina or int(pagina) in paginas:
                pagina = str(max(paginas) + 1)
            paginas.add(int(pagina))
            paths += f'\t\t\t\t(path "{ruta}"\n\t\t\t\t\t(page "{pagina}")\n\t\t\t\t)\n'
        hojas_txt.append(
            f"\t(sheet\n\t\t(at {num(x0)} {num(y0)})\n\t\t(size {num(ancho)} {num(alto)})\n\t\t(exclude_from_sim no)\n"
            "\t\t(in_bom yes)\n\t\t(on_board yes)\n\t\t(dnp no)\n\t\t(fields_autoplaced yes)\n"
            "\t\t(stroke\n\t\t\t(width 0.1524)\n\t\t\t(type solid)\n\t\t)\n\t\t(fill\n\t\t\t(color 0 0 0 0.0000)\n\t\t)\n"
            f'\t\t(uuid "{viejo.get("uuid") or U()}")\n'
            + _prop("Sheetname", nombre, x0, y0 - 0.7116, just="left bottom")
            + _prop("Sheetfile", archivo_h, x0, y0 + alto + 0.5846, just="left top")
            + pines_txt + f'\t\t(instances\n\t\t\t(project "{esc(nombre_proy)}"\n{paths}\t\t\t)\n\t\t)\n\t)\n')

    # cables, uniones automáticas y comprobaciones de conexión
    tramos, uniones, grado = tramos_y_uniones(desc.get("cables", []), pines_pts)
    uniones = sorted(set(uniones) | {clave(*u) for u in desc.get("uniones", [])})
    for quien, k in cableados:
        if k not in grado:
            raise Fallo(f"{quien}: conexión «W» sin cable en ({num(k[0])}, {num(k[1])})")
    pin_set = {clave(*p) for p in pines_pts}
    for quien, k in anclas:
        if k not in pin_set and not toca(k, tramos):
            avisos.append(f"{quien}: suelta (ni en un pin ni en un cable)")
    ancla_set = {k for _, k in anclas}
    sueltos = sorted(p for p, g in grado.items() if g == 1 and p not in pin_set and p not in ancla_set)
    avisos += [f"extremo de cable suelto en ({num(p[0])}, {num(p[1])})" for p in sueltos]
    cables_txt = "".join(f"\t(wire\n\t\t(pts\n\t\t\t(xy {num(a[0])} {num(a[1])}) (xy {num(b[0])} {num(b[1])})\n\t\t)\n"
                         f'\t\t(stroke\n\t\t\t(width 0)\n\t\t\t(type default)\n\t\t)\n\t\t(uuid "{U()}")\n\t)\n'
                         for a, b in tramos)
    uniones_txt = "".join(f"\t(junction\n\t\t(at {num(x)} {num(y)})\n\t\t(diameter 0)\n\t\t(color 0 0 0 0)\n"
                          f'\t\t(uuid "{U()}")\n\t)\n' for x, y in uniones)
    recuadros_txt = "".join(_recuadro(r) for r in desc.get("recuadros", []))

    textos = []
    for t in desc.get("textos", []):
        uid = viejos["otros"].get(("text", t["texto"]) + clave(t["x"], t["y"])) or U()
        negrita = "\n\t\t\t\t(bold yes)" if t.get("negrita") else ""
        tam = num(t.get("tam", 1.27))
        textos.append(f'\t(text "{esc(t["texto"])}"\n\t\t(exclude_from_sim no)\n\t\t(at {num(t["x"])} {num(t["y"])} 0)\n\t\t(effects\n'
                      f'\t\t\t(font\n\t\t\t\t(size {tam} {tam}){negrita}\n\t\t\t)\n\t\t\t(justify {t.get("justify", "left bottom")})\n\t\t)\n'
                      f'\t\t(uuid "{uid}")\n\t)\n')

    caj = desc.get("cajetin", {})
    tb = "".join(f'\t\t({k} "{esc(caj[k])}")\n' for k in ("title", "date", "rev", "company") if caj.get(k))
    tb += "".join(f'\t\t(comment {n} "{esc(c)}")\n' for n, c in sorted(caj.get("comment", {}).items()))
    cab = ('(kicad_sch\n\t(version 20260306)\n\t(generator "eeschema")\n\t(generator_version "10.0")\n'
           f'\t(uuid "{viejos["hoja"] or U()}")\n\t(paper "{desc.get("papel", "A4")}")\n'
           + (f"\t(title_block\n{tb}\t)\n" if tb else ""))
    cuerpo = ("\t(lib_symbols\n" + "\n".join(libs_txt[k] for k in libs_txt) + "\n\t)\n" + uniones_txt + "".join(ncs)
              + cables_txt + "".join(etiquetas) + "".join(globales) + "".join(jerarquicas) + "".join(textos)
              + recuadros_txt + "".join(simbolos) + "".join(pwr) + "".join(hojas_txt))
    resumen = {"piezas": len(simbolos), "etiquetas": len(etiquetas), "jerarquicas": len(jerarquicas), "globales": len(globales),
               "nc": len(ncs), "alimentacion": len(pwr), "textos": len(textos), "cables": len(tramos),
               "uniones": len(uniones), "recuadros": len(desc.get("recuadros", [])), "hojas": len(hojas_txt),
               "instancias": len(rutas), "avisos": avisos,
               "uuid_conservados": sum(1 for pz in desc.get("piezas", []) if (pz.get("ref") or "") in viejos["sim"])}
    return cab + cuerpo + ")\n", resumen


# ------------------------------------------------------------------ raíz: pines de hoja y sus conexiones

LADO_PIN = {"L": (180, "left"), "R": (0, "right")}   # lado → (ángulo del pin y de su etiqueta, justify del pin)


def _hojas_raiz(texto):
    """Hojas de la raíz: nombre → dict con i, j, x, y, ancho, alto, archivo y pines (nombre, forma, x, y, ang, uuid, i, j)."""
    salida = {}
    for n, i, j in trozos(texto):
        if n != "sheet":
            continue
        nodo = parse(texto[i:j])
        props = {p[1]: p[2] for p in hijos(nodo, "property") if len(p) > 2}
        at, tam = uno(nodo, "at"), uno(nodo, "size")
        pines = []
        for n2, a, b in trozos(texto, i):
            if n2 == "pin":
                p = parse(texto[a:b])
                pa = uno(p, "at")
                pines.append({"nombre": p[1], "forma": p[2], "x": float(pa[1]), "y": float(pa[2]),
                              "ang": int(float(pa[3])) if len(pa) > 3 else 0, "uuid": val(p, "uuid"), "i": a, "j": b})
        salida[props.get("Sheetname", "")] = {"i": i, "j": j, "x": float(at[1]), "y": float(at[2]), "ancho": float(tam[1]),
                                              "alto": float(tam[2]), "archivo": props.get("Sheetfile", ""), "pines": pines}
    return salida


def _conexiones_raiz(texto):
    """Etiquetas locales y globales y NC de primer nivel de la raíz: punto → lista de (tipo, nombre, forma, uuid, i, j)."""
    puntos = {}
    for n, i, j in trozos(texto):
        if n in ("label", "global_label", "no_connect"):
            nodo = parse(texto[i:j])
            at = uno(nodo, "at")
            nombre = nodo[1] if n != "no_connect" else ""
            puntos.setdefault(clave(at[1], at[2]), []).append((n, nombre, val(nodo, "shape"), val(nodo, "uuid"), i, j))
    return puntos


def extraer_raiz(archivo):
    """Descripción de los pines de hoja de la raíz y de lo que hay en cada uno (etiqueta, global, NC o nada)."""
    texto = leer(archivo)
    conexiones = _conexiones_raiz(texto)
    desc = {"hojas": []}
    for nombre, h in _hojas_raiz(texto).items():
        pines = []
        for p in h["pines"]:
            lado = {180: "L", 0: "R"}.get(p["ang"])
            if lado is None:
                raise Fallo(f"{nombre}.{p['nombre']}: pin de hoja arriba o abajo, no soportado")
            cons = conexiones.get(clave(p["x"], p["y"]), [])
            if len(cons) > 1:
                raise Fallo(f"{nombre}.{p['nombre']}: varias conexiones en el mismo punto")
            con = ""
            if cons:
                t, n, forma = cons[0][:3]
                con = {"label": f"L:{n}", "global_label": f"G:{n}:{forma}", "no_connect": "NC"}[t]
            pines.append({"nombre": p["nombre"], "forma": p["forma"], "lado": lado, "y": p["y"], "conexion": con})
        desc["hojas"].append({"nombre": nombre, "archivo": h["archivo"], "pines": pines})
    return desc


def generar_raiz(desc, raiz_sch):
    """Texto de la raíz con los pines de hoja de `desc` y sus conexiones; las hojas que no están en `desc` no se tocan."""
    original = leer(raiz_sch)
    nl = "\r\n" if "\r\n" in original else "\n"
    texto = original.replace("\r\n", "\n")
    hojas_ = _hojas_raiz(texto)
    conexiones = _conexiones_raiz(texto)
    cortes, insertos, nuevas, avisos, vistas = [], [], [], [], set()
    for h in desc.get("hojas", []):
        nombre = h["nombre"]
        if nombre in vistas:
            raise Fallo(f"hoja «{nombre}» repetida en la descripción")
        vistas.add(nombre)
        if nombre not in hojas_:
            raise Fallo(f"la raíz no tiene ninguna hoja «{nombre}» (hay: {', '.join(hojas_)})")
        hj = hojas_[nombre]
        viejos = {p["nombre"]: p for p in hj["pines"]}
        for p in hj["pines"]:                       # fuera los pines viejos y lo que había en sus extremos
            cortes.append((texto.rfind("\n", 0, p["i"]), p["j"]))
            for c in conexiones.get(clave(p["x"], p["y"]), []):
                cortes.append((texto.rfind("\n", 0, c[4]), c[5]))
        hijas = set()
        archivo = Path(raiz_sch).parent / hj["archivo"]
        if archivo.is_file():
            hijas = {parse(leer(archivo)[a:b])[1] for n, a, b in trozos(leer(archivo)) if n == "hierarchical_label"}
        nombres, puntos, bloque = set(), set(), ""
        for p in h.get("pines", []):
            if p["nombre"] in nombres:
                raise Fallo(f"{nombre}.{p['nombre']}: pin repetido")
            nombres.add(p["nombre"])
            if p.get("lado") not in LADO_PIN:
                raise Fallo(f"{nombre}.{p['nombre']}: lado «{p.get('lado')}» (L o R)")
            if p.get("forma") not in ("input", "output", "bidirectional", "tri_state", "passive"):
                raise Fallo(f"{nombre}.{p['nombre']}: forma «{p.get('forma')}» no válida")
            ang, just = LADO_PIN[p["lado"]]
            x, y = (hj["x"] if p["lado"] == "L" else hj["x"] + hj["ancho"]), float(p["y"])
            if not hj["y"] < y < hj["y"] + hj["alto"]:
                raise Fallo(f"{nombre}.{p['nombre']}: y = {num(y)} fuera del borde de la hoja ({num(hj['y'])}…{num(hj['y'] + hj['alto'])})")
            if clave(x, y) in puntos:
                raise Fallo(f"{nombre}.{p['nombre']}: dos pines en el mismo punto")
            puntos.add(clave(x, y))
            if hijas and p["nombre"] not in hijas:
                avisos.append(f"{nombre}.{p['nombre']}: {hj['archivo']} no tiene esa etiqueta jerárquica")
            uid = viejos[p["nombre"]]["uuid"] if p["nombre"] in viejos else U()
            bloque += (f'\n\t\t(pin "{esc(p["nombre"])}" {p["forma"]}\n\t\t\t(at {num(x)} {num(y)} {ang})\n\t\t\t(uuid "{uid}")\n'
                       f"\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(justify {just})\n\t\t\t)\n\t\t)")
            con, partes = p.get("conexion", ""), p.get("conexion", "").split(":")
            antiguo = {(c[0], c[1]): c[3] for c in conexiones.get(clave(x, y), [])}
            if con == "":
                continue
            if con == "NC":
                nuevas.append(f'\t(no_connect\n\t\t(at {num(x)} {num(y)})\n\t\t(uuid "{antiguo.get(("no_connect", "")) or U()}")\n\t)')
            elif partes[0] == "L" and len(partes) == 2:
                uid = antiguo.get(("label", partes[1])) or U()
                nuevas.append(f'\t(label "{esc(partes[1])}"\n\t\t(at {num(x)} {num(y)} {ang})\n\t\t(effects\n\t\t\t(font\n'
                              f'\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify {"right" if ang == 180 else "left"} bottom)\n\t\t)\n'
                              f'\t\t(uuid "{uid}")\n\t)')
            elif partes[0] == "G" and len(partes) == 3:
                uid = antiguo.get(("global_label", partes[1])) or U()
                nuevas.append(f'\t(global_label "{esc(partes[1])}"\n\t\t(shape {partes[2]})\n\t\t(at {num(x)} {num(y)} {ang})\n'
                              f'\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify {"right" if ang == 180 else "left"})\n'
                              f'\t\t)\n\t\t(uuid "{uid}")\n\t)')
            else:
                raise Fallo(f"{nombre}.{p['nombre']}: conexión «{con}» no reconocida (L:RED, G:RED:forma, NC o \"\")")
        avisos += [f"{nombre}: la etiqueta jerárquica {e} de {hj['archivo']} no tiene pin" for e in sorted(hijas - nombres)]
        insertos.append((texto.rfind("\n", hj["i"], hj["j"] - 1), bloque))   # antes del «\t)» que cierra la hoja
    fin_hojas = texto.index("\n\t(sheet_instances") if "\n\t(sheet_instances" in texto else texto.rstrip().rindex(")")
    insertos.append((fin_hojas, "".join("\n" + n for n in nuevas)))
    ediciones = sorted([(i, j, "") for i, j in set(cortes)] + [(k, k, s) for k, s in insertos], key=lambda e: (e[0], e[1]))
    for i, j, s in reversed(ediciones):
        texto = texto[:i] + s + texto[j:]
    resumen = {"hojas": len(vistas), "pines": sum(len(h.get("pines", [])) for h in desc.get("hojas", [])),
               "conexiones": len(nuevas), "avisos": avisos}
    return texto.replace("\n", nl), resumen


# ------------------------------------------------------------------ netlist frente a un plan de conexiones

_ENTRADA = re.compile(r"`?(?P<red>[^\s`{}=|,;:()]+)`?\s*=?\s*\{(?P<nodos>[^{}]*)\}")
_NODO = re.compile(r"^([A-Za-z]+\d+)-([A-Za-z0-9_]+)$")


def leer_plan(texto, seccion=None):
    """Redes de un documento de diseño escritas como `RED = {R1-2, U5-34}` o RED {…}; «NC {…}» = sin conectar.
    Con `seccion`, solo las líneas desde el título que la contiene hasta el siguiente del mismo nivel o superior."""
    lineas = texto.splitlines()
    if seccion:
        ini = next((k for k, l in enumerate(lineas) if l.startswith("#") and seccion.lower() in l.lower()), None)
        if ini is None:
            raise Fallo(f"no hay ningún título con «{seccion}»")
        nivel = len(lineas[ini]) - len(lineas[ini].lstrip("#"))
        fin = next((k for k in range(ini + 1, len(lineas)) if lineas[k].startswith("#")
                    and len(lineas[k]) - len(lineas[k].lstrip("#")) <= nivel), len(lineas))
        lineas = lineas[ini:fin]
    plan, ignoradas = [], []
    for m in _ENTRADA.finditer("\n".join(lineas)):
        nodos = [n.strip() for n in m.group("nodos").split(",") if n.strip()]
        partes = [_NODO.match(n) for n in nodos]
        if not nodos or not all(partes):
            ignoradas.append(m.group(0)[:60])
            continue
        plan.append((m.group("red"), [(p.group(1), p.group(2)) for p in partes]))
    return plan, ignoradas


def comparar_plan(net, plan):
    """Diferencias entre la netlist y el plan: cada red del plan, con exactamente esos pines."""
    redes = net["redes"]
    red_de = {nodo: nombre for nombre, nodos in redes.items() for nodo in nodos}
    dif = []
    for red, nodos in plan:
        quiere = set(nodos)
        if red == "NC":
            dif += [f"NC: {r}-{p} está en «{red_de[(r, p)]}»" for r, p in nodos
                    if red_de.get((r, p)) and not red_de[(r, p)].startswith("unconnected-")]
            continue
        candidatas = [n for n in redes if n == red or (not red.startswith("/") and n.endswith("/" + red))]
        if not candidatas:
            donde = sorted({red_de.get(n, "—") for n in nodos})
            dif.append(f"{red}: no está en la netlist (sus pines están en {', '.join(donde)})"[:200])
            continue
        real = max(candidatas, key=lambda n: (len(redes[n] & quiere), n == red))
        for r, p in sorted(quiere - redes[real]):
            dif.append(f"{red}: falta {r}-{p} (está en «{red_de.get((r, p), '—')}»)")
        sobran = sorted(redes[real] - quiere)
        if sobran:
            dif.append(f"{red}: pines de más {', '.join(f'{r}-{p}' for r, p in sobran)}"[:200])
    return dif


# ------------------------------------------------------------------ órdenes

def orden_pines(args):
    carpeta = Path(args.proyecto).resolve() if args.proyecto else None
    pines, caja, _ = pines_y_caja(parse(bloque_libreria(args.simbolo, carpeta)))
    celdas = [f"{p['num']:>3} {p['nombre'][:12]:<12} {p['tipo'][:9]:<9} ({num(p['x'])},{num(p['y'])}) {lado(p['ang'], 0)}"
              f"{' oculto' if p['oculto'] else ''}" for p in pines]
    por_linea = max(1, math.ceil(len(celdas) / 27))
    lineas = [f"{args.simbolo}: {len(pines)} pines · cuerpo x {num(caja[0])}…{num(caja[2])}, y {num(caja[1])}…{num(caja[3])} "
              "(mm, y hacia arriba; R/L/U/D = lado por el que sale el pin)"]
    lineas += [" | ".join(celdas[i:i + por_linea]) for i in range(0, len(celdas), por_linea)]
    emitir(lineas)
    return 0


def orden_extraer(args):
    desc, perdidos = extraer(args.hoja)
    if perdidos and not args.forzar:
        emitir([f"{args.hoja}: {len(perdidos)} elementos no representables; no se escribe nada (--forzar para seguir)"]
               + sorted(set(perdidos))[:20], pista=None)
        return 1
    Path(args.salida).parent.mkdir(parents=True, exist_ok=True)
    Path(args.salida).write_text(json.dumps(desc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    emitir([f"{args.salida}: {len(desc['piezas'])} piezas, {len(desc['textos'])} textos, {len(desc['banderas'])} banderas, "
            f"{len(desc['cables'])} cables, {len(desc['etiquetas'])} etiquetas sueltas de pin, {len(desc['recuadros'])} recuadros, "
            f"{len(desc['hojas'])} subhojas · no representado: {len(perdidos)}"] + sorted(set(perdidos))[:20])
    return 0


def orden_generar(args):
    carpeta, nombre = proyecto(args.proyecto)
    salida = Path(args.salida).resolve()
    nombre_hoja = args.como or salida.name
    base = args.base or (salida if salida.is_file() else carpeta / nombre_hoja)
    tabla = _campos.leer_tabla(args.campos) if args.campos else None
    texto, r = generar(json.loads(Path(args.descripcion).read_text(encoding="utf-8")), carpeta, nombre, nombre_hoja,
                       base=base, tabla=tabla, forzar=args.forzar)
    escribir(salida, texto)
    emitir([f"{salida}: {r['piezas']} piezas ({r['uuid_conservados']} con su UUID), {r['etiquetas']} etiquetas, "
            f"{r['jerarquicas']} jerárquicas, {r['globales']} globales, {r['nc']} NC, {r['alimentacion']} de alimentación, "
            f"{r['textos']} textos, {r['cables']} tramos de cable, {r['uniones']} uniones, {r['recuadros']} recuadros, "
            f"{r['hojas']} subhojas; {r['instancias']} instancias de la hoja · avisos {len(r['avisos'])}"] + r["avisos"], pista=None)
    return 0


def orden_raiz(args):
    carpeta, nombre = proyecto(args.proyecto)
    raiz = carpeta / f"{nombre}.kicad_sch"
    salida = Path(args.salida)
    if args.extraer:
        desc = extraer_raiz(raiz)
        salida.parent.mkdir(parents=True, exist_ok=True)
        salida.write_text(json.dumps(desc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        emitir([f"{salida}: {len(desc['hojas'])} hojas, {sum(len(h['pines']) for h in desc['hojas'])} pines de hoja"])
        return 0
    if not args.descripcion:
        raise Fallo("falta la descripción (o --extraer)")
    texto, r = generar_raiz(json.loads(Path(args.descripcion).read_text(encoding="utf-8")), raiz)
    escribir(salida, texto)
    emitir([f"{salida}: {r['hojas']} hojas, {r['pines']} pines de hoja, {r['conexiones']} etiquetas o NC · avisos "
            f"{len(r['avisos'])}"] + r["avisos"], pista=None)
    return 1 if r["avisos"] else 0


def orden_netlist(args):
    if args.plan:
        if args.b:
            raise Fallo("con --plan se compara un solo proyecto")
        plan, ignoradas = leer_plan(Path(args.plan).read_text(encoding="utf-8"), args.seccion)
        if not plan:
            raise Fallo(f"{args.plan}: ninguna red con la forma `RED = {{REF-PIN, …}}`")
        with tempfile.TemporaryDirectory(prefix="netlist_") as tmp:
            carpeta, nombre = proyecto(args.a)
            net = exportar_netlist(carpeta, nombre, Path(tmp) / "a.net")
        dif = comparar_plan(net, plan)
        donde = f" ({args.seccion})" if args.seccion else ""
        emitir([f"Plan {args.plan}{donde}: {len(plan)} redes, {sum(len(n) for _, n in plan)} pines; {len(dif)} diferencias; "
                f"{len(ignoradas)} entradas sin interpretar"] + dif + [f"sin interpretar: {e}" for e in ignoradas],
               detalle=args.detalle)
        return 1 if dif else 0
    if not args.b:
        raise Fallo("faltan los dos proyectos (o --plan DOCUMENTO)")
    with tempfile.TemporaryDirectory(prefix="netlist_") as tmp:
        redes = []
        for k, ruta in enumerate((args.a, args.b)):
            carpeta, nombre = proyecto(ruta)
            redes.append(exportar_netlist(carpeta, nombre, Path(tmp) / f"{k}.net"))
    dif = (comparar_grupos if args.grupos else comparar_netlists)(redes[0], redes[1], args.hoja)
    ambito = (f"hoja {args.hoja}" if args.hoja else "proyecto") + (", por grupos de pines" if args.grupos else "")
    emitir([f"Netlist A ({len(redes[0]['comps'])} piezas, {len(redes[0]['redes'])} redes) frente a B "
            f"({len(redes[1]['comps'])} piezas, {len(redes[1]['redes'])} redes), {ambito}: {len(dif)} diferencias"] + dif,
           detalle=args.detalle)
    return 1 if dif else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="orden", required=True)
    p = sub.add_parser("pines", help="pines de un símbolo de librería, con sus coordenadas")
    p.add_argument("simbolo", metavar="Lib:Nombre")
    p.add_argument("--proyecto", help="carpeta del proyecto (sym-lib-table)")
    p.set_defaults(f=orden_pines)
    e = sub.add_parser("extraer", help="descripción JSON de una hoja existente")
    e.add_argument("hoja")
    e.add_argument("-o", "--salida", required=True)
    e.add_argument("--forzar", action="store_true", help="escribe aunque haya elementos no representables")
    e.set_defaults(f=orden_extraer)
    g = sub.add_parser("generar", help="escribe la hoja desde la descripción")
    g.add_argument("descripcion")
    g.add_argument("-o", "--salida", required=True, help="hoja .kicad_sch de destino")
    g.add_argument("--proyecto", required=True, help="proyecto al que pertenece la hoja (carpeta o .kicad_pro)")
    g.add_argument("--como", help="nombre de la hoja en el proyecto, si -o tiene otro nombre")
    g.add_argument("--base", help="hoja de la que conservar los UUID (por defecto, la de destino o la del proyecto)")
    g.add_argument("--campos", help="CSV de campos que completa o sustituye los de la descripción")
    g.add_argument("--forzar", action="store_true", help="sustituye aunque la hoja tenga cables u otros elementos")
    g.set_defaults(f=orden_generar)
    r = sub.add_parser("raiz", help="pines de hoja y sus etiquetas o NC en la raíz, desde una descripción")
    r.add_argument("descripcion", nargs="?")
    r.add_argument("--proyecto", required=True, help="proyecto cuya raíz se lee (carpeta o .kicad_pro)")
    r.add_argument("-o", "--salida", required=True, help="raíz .kicad_sch de destino (o JSON con --extraer)")
    r.add_argument("--extraer", action="store_true", help="escribe en -o la descripción de la raíz actual")
    r.set_defaults(f=orden_raiz)
    n = sub.add_parser("netlist", help="compara la netlist con la de otro proyecto o con un plan")
    n.add_argument("a")
    n.add_argument("b", nargs="?")
    n.add_argument("--plan", metavar="DOC", help="documento con las redes como `RED = {REF-PIN, …}`")
    n.add_argument("--seccion", help="con --plan, solo la sección cuyo título contiene este texto")
    n.add_argument("--hoja", help="solo las piezas de esta hoja (nombre de la hoja, p. ej. MCU)")
    n.add_argument("--grupos", action="store_true", help="compara las redes por grupos de pines, no por nombre")
    n.add_argument("--detalle", metavar="ARCHIVO")
    n.set_defaults(f=orden_netlist)
    args = ap.parse_args()
    return args.f(args)


if __name__ == "__main__":
    principal(main)
