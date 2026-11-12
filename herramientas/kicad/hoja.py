"""Genera o actualiza una hoja de esquema desde una descripción JSON de piezas y redes.

Uso:
    python herramientas/kicad/hoja.py pines RF_Module:ESP32-S3-WROOM-1 [--proyecto hardware/v2]
    python herramientas/kicad/hoja.py extraer hardware/v2/mcu.kicad_sch -o mcu.json
    python herramientas/kicad/hoja.py generar mcu.json --proyecto <copia>/v2 -o <copia>/v2/mcu.kicad_sch
    python herramientas/kicad/hoja.py netlist hardware/v2 <copia>/v2 [--hoja MCU]

Descripción (JSON): {"papel", "cajetin": {title, date, rev, company, comment: {"1": …}},
"piezas": [{"ref", "simbolo": "Lib:Nombre", "x", "y", "giro", "campos": {…}, "dnp", "pines": {"nº": conexión}}],
"banderas": [[x, y]], "textos": [{"x", "y", "tam", "negrita", "texto"}]}. Conexión de un pin, dibujada
en su extremo y sin cables: "L:RED" etiqueta local · "H:RED:forma" jerárquica (input, output,
bidirectional, passive, tri_state) · "G:RED:forma" global · "P:GND" símbolo de `power` · "NC" · "" nada.
Todo pin visible debe tener conexión declarada.

generar escribe solo en -o. Si -o (o --base) ya existe, conserva sus UUID (hoja, símbolos, pines,
etiquetas) y las referencias #PWR, para no romper la paridad con la PCB; se niega a sustituir una
hoja con cables u otros elementos que no sabe representar, salvo con --forzar. Los símbolos de
`lib_symbols` se copian de las librerías (oficiales o del sym-lib-table del proyecto), con los
derivados (`extends`) aplanados. No admite símbolos de varias unidades ni espejados.
netlist compara las netlists de dos proyectos (exportadas sobre copias). Los pines de hoja de la
raíz no se tocan: si cambian las etiquetas jerárquicas, hay que actualizarlos aparte.
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
from _comun import (CAMPOS, Fallo, comparar_netlists, emitir, esc, escribir, exportar_netlist, hijos, hojas,  # noqa: E402
                    leer, num, parse, parse_cabecera, principal, proyecto, ruta_simbolos, simbolos_hoja,
                    trozos, uno, val)
import campos as _campos  # noqa: E402

NO_REPRESENTABLE = ("wire", "junction", "bus", "bus_entry", "polyline", "rectangle", "circle", "arc", "text_box",
                    "netclass_flag", "image", "sheet", "bezier", "rule_area", "table")
ANGULO = {"R": 0, "U": 90, "L": 180, "D": 270}


def U():
    return str(_uuid.uuid4())


def clave(x, y):
    return (round(float(x), 3), round(float(y), 3))


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


def girar(px, py, X, Y, giro):
    """Punto de librería (y hacia arriba) → hoja (y hacia abajo), con el giro del símbolo."""
    a = math.radians(giro)
    return (round(X + px * math.cos(a) - py * math.sin(a), 4), round(Y - (px * math.sin(a) + py * math.cos(a)), 4))


def lado(ang_pin, giro):
    """Hacia dónde sale el pin en la hoja: R, U, L o D."""
    return {0: "R", 90: "U", 180: "L", 270: "D"}[int((ang_pin + giro + 180) % 360)]


# ------------------------------------------------------------------ extraer

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
    for n, i, j in trozos(texto):
        if n in NO_REPRESENTABLE:
            perdidos.append(n)
        elif n in ("label", "hierarchical_label", "global_label"):
            nodo = parse(texto[i:j])
            at = uno(nodo, "at")
            con = {"label": f"L:{nodo[1]}", "hierarchical_label": f"H:{nodo[1]}:{val(nodo, 'shape')}",
                   "global_label": f"G:{nodo[1]}:{val(nodo, 'shape')}"}[n]
            puntos.setdefault(clave(at[1], at[2]), []).append(con)
        elif n == "no_connect":
            at = uno(parse(texto[i:j]), "at")
            puntos.setdefault(clave(at[1], at[2]), []).append("NC")
        elif n == "text":
            nodo = parse(texto[i:j])
            at, fuente = uno(nodo, "at"), uno(uno(nodo, "effects", []), "font", [])
            textos.append({"x": float(at[1]), "y": float(at[2]), "tam": float(val(fuente, "size", "1.27")),
                           "negrita": val(fuente, "bold", "no") == "yes", "texto": nodo[1]})
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
                puntos.setdefault(clave(x, y), []).append(f"P:{nombre}")
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
                perdidos.append(f"{s['ref']}.{p['num']}: varias conexiones en el mismo punto {cons}")
            pines[p["num"]] = cons[0] if cons else ""
            usados.add(k)
        pos = {}
        for prop in hijos(s["nodo"], "property"):
            if prop[1] in ("Reference", "Value"):
                at = uno(prop, "at")
                just = uno(uno(prop, "effects", []), "justify")
                pos[prop[1]] = [float(at[1]), float(at[2]), int(float(at[3])), " ".join(just[1:]) if just else ""]
        campos = {k: v for k, v in s["props"].items() if k != "Reference"}
        piezas.append({"ref": s["ref"], "simbolo": s["lib_id"], "x": s["x"], "y": s["y"], "giro": s["giro"],
                       "dnp": s["dnp"], "en_bom": s["in_bom"], "campos": campos, "pos": pos, "pines": pines})
    for k, cons in puntos.items():
        if k not in usados and not any(abs(k[0] - b[0]) < 1e-3 and abs(k[1] - b[1]) < 1e-3 for b in banderas):
            perdidos.append(f"{cons[0]} suelta en {k}")
    tb = uno(cab, "title_block", [])
    cajetin = {k: val(tb, k) for k in ("title", "date", "rev", "company") if val(tb, k)}
    cajetin["comment"] = {c[1]: c[2] for c in hijos(tb, "comment")}
    desc = {"papel": val(cab, "paper", "A4"), "cajetin": cajetin, "piezas": piezas, "banderas": banderas, "textos": textos}
    return desc, perdidos


# ------------------------------------------------------------------ generar

def _prop(nombre, valor, x, y, ang=0, oculto=False, just=None):
    h = "\n\t\t\t(hide yes)" if oculto else ""
    j = f"\n\t\t\t\t(justify {just})" if just else ""
    return (f'\t\t(property "{esc(nombre)}" "{esc(valor)}"\n\t\t\t(at {num(x)} {num(y)} {int(ang)}){h}\n'
            "\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n"
            f"\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t){j}\n\t\t\t)\n\t\t)\n")


def _simbolo(lib, ref, x, y, giro, props, pines, ruta, nombre_proy, uid, en_bom=True, dnp=False):
    sn = lambda b: "yes" if b else "no"  # noqa: E731
    s = (f'\t(symbol\n\t\t(lib_id "{esc(lib)}")\n\t\t(at {num(x)} {num(y)} {int(giro)})\n\t\t(unit 1)\n\t\t(body_style 1)\n'
         f"\t\t(exclude_from_sim no)\n\t\t(in_bom {sn(en_bom)})\n\t\t(on_board yes)\n\t\t(in_pos_files {sn(en_bom)})\n"
         f'\t\t(dnp {sn(dnp)})\n\t\t(uuid "{uid}")\n') + "".join(props)
    for numero, upin in pines:
        s += f'\t\t(pin "{esc(numero)}"\n\t\t\t(uuid "{upin}")\n\t\t)\n'
    return s + (f'\t\t(instances\n\t\t\t(project "{esc(nombre_proy)}"\n\t\t\t\t(path "{ruta}"\n'
                f'\t\t\t\t\t(reference "{esc(ref)}")\n\t\t\t\t\t(unit 1)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n')


def _viejos(base):
    """UUID y referencias de la hoja que se sustituye, para conservarlos."""
    v = {"hoja": None, "sim": {}, "pin": {}, "pwr": {}, "otros": {}, "no_rep": []}
    if not base or not Path(base).is_file():
        return v
    texto = leer(base)
    v["hoja"] = val(parse_cabecera(texto), "uuid") or None
    for s in simbolos_hoja(texto):
        pins = {p[1]: val(p, "uuid") for p in hijos(s["nodo"], "pin")}
        if s["lib_id"].startswith("power:"):
            v["pwr"][(s["lib_id"],) + clave(s["x"], s["y"])] = (s["uuid"], s["ref"], pins.get("1"))
        else:
            v["sim"][s["ref"]] = s["uuid"]
            v["pin"].update({(s["ref"], n): u for n, u in pins.items()})
    for n, i, j in trozos(texto):
        if n in NO_REPRESENTABLE:
            v["no_rep"].append(n)
        elif n in ("label", "hierarchical_label", "global_label", "no_connect", "text"):
            nodo = parse(texto[i:j])
            at = uno(nodo, "at")
            v["otros"][(n, nodo[1] if n != "no_connect" else "") + clave(at[1], at[2])] = val(nodo, "uuid")
    return v


def _pwr_usados(carpeta, nombre, excluir):
    usados = set()
    for h in hojas(Path(carpeta) / f"{nombre}.kicad_sch"):
        if h["archivo"].is_file() and h["archivo"].name != excluir:
            usados |= set(re.findall(r'\(reference "(#(?:PWR|FLG)\d+)"\)', leer(h["archivo"])))
    return usados


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


def generar(desc, carpeta, nombre_proy, nombre_hoja, base=None, tabla=None, forzar=False):
    """Texto de la hoja y resumen. `carpeta`/`nombre_proy`: proyecto al que pertenece la hoja."""
    viejos = _viejos(base)
    if viejos["no_rep"] and not forzar:
        raise Fallo(f"la hoja que se sustituye tiene {len(viejos['no_rep'])} elementos que se perderían "
                    f"({', '.join(sorted(set(viejos['no_rep'])))}); usa --forzar si es lo que quieres")
    hoja = next((h for h in hojas(Path(carpeta) / f"{nombre_proy}.kicad_sch")[1:] if h["archivo"].name == nombre_hoja), None)
    if hoja is None:
        raise Fallo(f"{nombre_hoja} no cuelga de {nombre_proy}.kicad_sch: no se puede saber su ruta de instancia")
    ruta = hoja["ruta"]
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
    puntos = {}

    def alimentacion(nombre, x, y, bandera=False):
        spec = f"power:{nombre}"
        _, _, props = lib(spec)
        uid, ref, upin = viejos["pwr"].get((spec,) + clave(x, y), (None, None, None))
        ref = ref or ref_nueva("#FLG" if bandera else "#PWR")

        def en(nombre_prop, defecto):
            at = uno(props.get(nombre_prop, []), "at", ["at", *defecto])
            return x + float(at[1]), y - float(at[2])

        desc_ = props["Description"][2] if "Description" in props else ""
        ps = [_prop("Reference", ref, *en("Reference", ("0", "-6.35")), oculto=True), _prop("Value", nombre, *en("Value", ("0", "-3.81"))),
              _prop("Footprint", "", x, y, oculto=True), _prop("Datasheet", "~" if bandera else "", x, y, oculto=True),
              _prop("Description", desc_, x, y, oculto=True)]
        pwr.append(_simbolo(spec, ref, x, y, 0, ps, [("1", upin or U())], ruta, nombre_proy, uid or U()))

    refs_vistas = set()
    for pz in desc.get("piezas", []):
        ref, spec, X, Y, giro = pz["ref"], pz["simbolo"], float(pz["x"]), float(pz["y"]), int(pz.get("giro", 0))
        if ref in refs_vistas:
            raise Fallo(f"{ref}: referencia repetida en la descripción")
        refs_vistas.add(ref)
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
        simbolos.append(_simbolo(spec, ref, X, Y, giro, ps, upins, ruta, nombre_proy, viejos["sim"].get(ref) or U(),
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
            sd = lado(p["ang"], giro)
            partes = con.split(":")
            if con == "":
                continue
            if con == "NC":
                uid = viejos["otros"].get(("no_connect", "") + clave(x, y)) or U()
                ncs.append(f'\t(no_connect\n\t\t(at {num(x)} {num(y)})\n\t\t(uuid "{uid}")\n\t)\n')
            elif partes[0] == "P" and len(partes) == 2:
                alimentacion(partes[1], x, y)
            elif partes[0] == "L" and len(partes) == 2:
                uid = viejos["otros"].get(("label", partes[1]) + clave(x, y)) or U()
                just = "left bottom" if sd in "RU" else "right bottom"
                etiquetas.append(f'\t(label "{esc(partes[1])}"\n\t\t(at {num(x)} {num(y)} {ANGULO[sd]})\n\t\t(effects\n\t\t\t(font\n'
                                 f'\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify {just})\n\t\t)\n\t\t(uuid "{uid}")\n\t)\n')
            elif partes[0] in "HG" and len(partes) == 3:
                tipo = "hierarchical_label" if partes[0] == "H" else "global_label"
                uid = viejos["otros"].get((tipo, partes[1]) + clave(x, y)) or U()
                just = "left" if sd in "RU" else "right"
                (jerarquicas if partes[0] == "H" else globales).append(
                    f'\t({tipo} "{esc(partes[1])}"\n\t\t(shape {partes[2]})\n\t\t(at {num(x)} {num(y)} {ANGULO[sd]})\n\t\t(effects\n'
                    f'\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify {just})\n\t\t)\n\t\t(uuid "{uid}")\n\t)\n')
            else:
                raise Fallo(f"{ref}.{numero}: conexión «{con}» no reconocida")
    for x, y in desc.get("banderas", []):
        alimentacion("PWR_FLAG", float(x), float(y), bandera=True)
    for k, quienes in puntos.items():
        if len(quienes) > 1:
            avisos.append(f"pines en el mismo punto {k}: {' '.join(quienes)} (quedan unidos)")

    textos = []
    for t in desc.get("textos", []):
        uid = viejos["otros"].get(("text", t["texto"]) + clave(t["x"], t["y"])) or U()
        negrita = "\n\t\t\t\t(bold yes)" if t.get("negrita") else ""
        tam = num(t.get("tam", 1.27))
        textos.append(f'\t(text "{esc(t["texto"])}"\n\t\t(exclude_from_sim no)\n\t\t(at {num(t["x"])} {num(t["y"])} 0)\n\t\t(effects\n'
                      f'\t\t\t(font\n\t\t\t\t(size {tam} {tam}){negrita}\n\t\t\t)\n\t\t\t(justify left bottom)\n\t\t)\n\t\t(uuid "{uid}")\n\t)\n')

    caj = desc.get("cajetin", {})
    tb = "".join(f'\t\t({k} "{esc(caj[k])}")\n' for k in ("title", "date", "rev", "company") if caj.get(k))
    tb += "".join(f'\t\t(comment {n} "{esc(c)}")\n' for n, c in sorted(caj.get("comment", {}).items()))
    cab = ('(kicad_sch\n\t(version 20260306)\n\t(generator "eeschema")\n\t(generator_version "10.0")\n'
           f'\t(uuid "{viejos["hoja"] or U()}")\n\t(paper "{desc.get("papel", "A4")}")\n'
           + (f"\t(title_block\n{tb}\t)\n" if tb else ""))
    cuerpo = ("\t(lib_symbols\n" + "\n".join(libs_txt[k] for k in libs_txt) + "\n\t)\n" + "".join(ncs) + "".join(etiquetas)
              + "".join(globales) + "".join(jerarquicas) + "".join(textos) + "".join(simbolos) + "".join(pwr))
    resumen = {"piezas": len(simbolos), "etiquetas": len(etiquetas), "jerarquicas": len(jerarquicas), "globales": len(globales),
               "nc": len(ncs), "alimentacion": len(pwr), "textos": len(textos), "avisos": avisos,
               "uuid_conservados": sum(1 for pz in desc.get("piezas", []) if pz["ref"] in viejos["sim"])}
    return cab + cuerpo + ")\n", resumen


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
    emitir([f"{args.salida}: {len(desc['piezas'])} piezas, {len(desc['textos'])} textos, {len(desc['banderas'])} banderas"
            f" · no representado: {len(perdidos)}"] + sorted(set(perdidos))[:20])
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
            f"{r['textos']} textos · avisos {len(r['avisos'])}"] + r["avisos"], pista=None)
    return 0


def orden_netlist(args):
    with tempfile.TemporaryDirectory(prefix="netlist_") as tmp:
        redes = []
        for k, ruta in enumerate((args.a, args.b)):
            carpeta, nombre = proyecto(ruta)
            redes.append(exportar_netlist(carpeta, nombre, Path(tmp) / f"{k}.net"))
    dif = comparar_netlists(redes[0], redes[1], args.hoja)
    ambito = f"hoja {args.hoja}" if args.hoja else "proyecto"
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
    n = sub.add_parser("netlist", help="compara las netlists de dos proyectos")
    n.add_argument("a")
    n.add_argument("b")
    n.add_argument("--hoja", help="solo las piezas de esta hoja (nombre de la hoja, p. ej. MCU)")
    n.add_argument("--detalle", metavar="ARCHIVO")
    n.set_defaults(f=orden_netlist)
    args = ap.parse_args()
    return args.f(args)


if __name__ == "__main__":
    principal(main)
