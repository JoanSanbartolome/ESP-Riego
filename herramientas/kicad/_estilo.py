"""Geometría aproximada de una hoja de esquema para los puntos de estilo de comprobar.py (KIC-06, DEC-0015).

Cajas de símbolos (una por primitiva de dibujo, el núcleo entre los extremos interiores de los pines y los pines), de textos (campos visibles, etiquetas, notas, títulos de recuadro y de
subhoja), cables, recuadros (text_box de trazo y punto) y subhojas. Los textos se miden por una caja
aproximada: 0,8 × alto por carácter, interlínea 1,6 × alto. Los campos de un símbolo se colocan con su
ángulo y su justificación y luego se giran con el símbolo, como hace KiCad; las etiquetas y las notas se
leen siempre de izquierda a derecha o de abajo arriba. Solo lee el archivo.
"""
import math

from _comun import hijos, leer, parse, simbolos_hoja, trozos, uno, val
import hoja as _hoja

LETRA = 0.8            # ancho de un carácter / alto de letra
INTERLINEA = 1.6       # paso entre líneas / alto de letra
HOLGURA_TEXTO = 0.15   # cada caja de texto se encoge esto por lado antes de comparar (mm)
HOLGURA_SIMBOLO = 0.05
NUCLEO = 0.1           # el núcleo entre los extremos interiores de los pines se ensancha esto por lado (mm)


def _rot(dx, dy, ang):
    """Giro antihorario en pantalla (y hacia abajo)."""
    a = math.radians(ang)
    c, s = round(math.cos(a), 9), round(math.sin(a), 9)
    return dx * c + dy * s, -dx * s + dy * c


def caja_texto(x, y, texto, tam, ang, hj, vj, legible=True, extra=0.0, alto=None, desplazar=0.0):
    """Caja (x0, y0, x1, y1) de un texto anclado en (x, y). `legible`: etiquetas y notas (ángulo módulo 180).
    `extra`: largo añadido (forma de una etiqueta global o jerárquica); `alto`: alto de la caja si no es el de
    las líneas; `desplazar`: separación del texto sobre su ancla (etiquetas locales)."""
    lineas = str(texto).split("\n") or [""]
    largo = max(len(l) for l in lineas) * LETRA * tam + extra
    h = alto if alto is not None else tam * (1 + INTERLINEA * (len(lineas) - 1))
    x0 = {"left": 0.0, "right": -largo}.get(hj, -largo / 2)
    y0 = {"top": desplazar, "bottom": -h - desplazar}.get(vj, -h / 2)
    ang = ang % 180 if legible else ang % 360
    pts = [_rot(px, py, ang) for px in (x0, x0 + largo) for py in (y0, y0 + h)]
    return (x + min(p[0] for p in pts), y + min(p[1] for p in pts), x + max(p[0] for p in pts), y + max(p[1] for p in pts))


def _justify(nodo):
    j = uno(uno(nodo, "effects", []), "justify", ["justify"])[1:]
    hj = "left" if "left" in j else "right" if "right" in j else "center"
    vj = "top" if "top" in j else "bottom" if "bottom" in j else "center"
    return hj, vj


def _tam(nodo):
    tam = uno(uno(uno(nodo, "effects", []), "font", []), "size")
    return float(tam[1]) if tam else 1.27


def _oculto(prop):
    efectos = uno(prop, "effects", [])
    return val(prop, "hide") == "yes" or val(efectos, "hide") == "yes" or "hide" in efectos or "hide" in prop


def encoger(caja, d):
    return (caja[0] + d, caja[1] + d, caja[2] - d, caja[3] - d)


def solapan(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def contiene(grande, chica, tol=0.01):
    return (grande[0] - tol <= chica[0] and grande[1] - tol <= chica[1]
            and chica[2] <= grande[2] + tol and chica[3] <= grande[3] + tol)


def cruza(a, b, caja):
    """El segmento a-b pasa por el interior de la caja (recorte de Liang-Barsky)."""
    (x0, y0), (x1, y1) = a, b
    dx, dy = x1 - x0, y1 - y0
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x0 - caja[0]), (dx, caja[2] - x0), (-dy, y0 - caja[1]), (dy, caja[3] - y0)):
        if abs(p) < 1e-12:
            if q <= 0:
                return False
            continue
        t = q / p
        if p < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
        if t0 >= t1:
            return False
    return (t1 - t0) * math.hypot(dx, dy) > 0.01


def pt(x, y):
    return (round(float(x), 3), round(float(y), 3))


def analizar(archivo):
    """Elementos de una hoja con sus cajas, en mm y coordenadas de la hoja."""
    texto = leer(archivo)
    libs = {}
    for n, i, j in trozos(texto):
        if n == "lib_symbols":
            for n2, a, b in trozos(texto, i):
                if n2 == "symbol":
                    nodo = parse(texto[a:b])
                    libs[nodo[1]] = _hoja.pines_y_caja(nodo) + (_hoja.cuerpos(nodo),)
    h = {"simbolos": [], "textos": [], "cables": [], "etiquetas": [], "recuadros": [], "hojas": []}
    for s in simbolos_hoja(texto):
        if s["lib_id"] not in libs:
            continue
        pines, caja, _, primitivas = libs[s["lib_id"]]

        def a_hoja(c):
            esq = [_hoja.girar(cx, cy, s["x"], s["y"], s["giro"]) for cx in (c[0], c[2]) for cy in (c[1], c[3])]
            return (min(p[0] for p in esq), min(p[1] for p in esq), max(p[0] for p in esq), max(p[1] for p in esq))

        tramos_pin = []
        for p in pines:   # tramo del pin, de la punta hacia el cuerpo, sin la punta (ahí llegan cables y etiquetas)
            if p["largo"] <= 0.1:
                continue
            dx, dy = {0: (1, 0), 90: (0, 1), 180: (-1, 0), 270: (0, -1)}.get(p["ang"] % 360, (0, 0))
            x0, y0 = p["x"] + 0.1 * dx, p["y"] + 0.1 * dy
            x1, y1 = p["x"] + p["largo"] * dx, p["y"] + p["largo"] * dy
            tramos_pin.append(a_hoja((min(x0, x1) - 0.05, min(y0, y1) - 0.05, max(x0, x1) + 0.05, max(y0, y1) + 0.05)))
        # cuerpo: una caja por primitiva de dibujo (las flechas de un LED no tapan el cable del cátodo) y el núcleo
        # entre los extremos interiores de los pines (un cable entre las placas de un condensador cruza el símbolo)
        cuerpo = [a_hoja(c) for c in primitivas] or [a_hoja(caja)]
        interiores = [(p["x"] + p["largo"] * dx, p["y"] + p["largo"] * dy) for p in pines
                      for dx, dy in [{0: (1, 0), 90: (0, 1), 180: (-1, 0), 270: (0, -1)}.get(p["ang"] % 360, (0, 0))]]
        if len(pines) >= 2 and all(p["largo"] > 0.5 for p in pines):
            n = (min(x for x, _ in interiores), min(y for _, y in interiores), max(x for x, _ in interiores), max(y for _, y in interiores))
            cuerpo.append(encoger(a_hoja(n), -NUCLEO))
        sim = {"ref": s["ref"], "lib": s["lib_id"], "pieza": not s["ref"].startswith("#") and not s["lib_id"].startswith("power:"),
               "cuerpo": cuerpo, "total": a_hoja(caja), "tramos_pin": tramos_pin,
               "pines": [pt(*_hoja.girar(p["x"], p["y"], s["x"], s["y"], s["giro"])) for p in pines]}
        h["simbolos"].append(sim)
        for prop in hijos(s["nodo"], "property"):
            if len(prop) < 3 or not prop[2] or _oculto(prop):
                continue
            at = uno(prop, "at")
            hj, vj = _justify(prop)
            ang = (float(at[3]) if len(at) > 3 else 0) + s["giro"]
            h["textos"].append({"texto": prop[2], "de": s["ref"], "caja": caja_texto(
                float(at[1]), float(at[2]), prop[2], _tam(prop), ang, hj, vj, legible=False)})
    for n, i, j in trozos(texto):
        if n not in ("wire", "label", "global_label", "hierarchical_label", "text", "text_box", "sheet"):
            continue
        nodo = parse(texto[i:j])
        at = uno(nodo, "at")
        if n == "wire":
            xy = hijos(uno(nodo, "pts", []), "xy")
            h["cables"] += [(pt(xy[k][1], xy[k][2]), pt(xy[k + 1][1], xy[k + 1][2])) for k in range(len(xy) - 1)]
        elif n in ("label", "global_label", "hierarchical_label"):
            tam, (hj, vj) = _tam(nodo), _justify(nodo)
            ang = float(at[3]) if len(at) > 3 else 0
            if n == "label":
                caja = caja_texto(float(at[1]), float(at[2]), nodo[1], tam, ang, hj, vj, desplazar=0.25)
            else:
                caja = caja_texto(float(at[1]), float(at[2]), nodo[1], tam, ang, hj, "center", extra=1.2 * tam, alto=1.4 * tam)
            e = {"tipo": n, "nombre": nodo[1], "pt": pt(at[1], at[2]), "caja": caja}
            h["etiquetas"].append(e)
            h["textos"].append({"texto": nodo[1], "de": n, "caja": caja})
        elif n == "text":
            hj, vj = _justify(nodo)
            h["textos"].append({"texto": nodo[1], "de": "nota", "caja": caja_texto(
                float(at[1]), float(at[2]), nodo[1], _tam(nodo), float(at[3]) if len(at) > 3 else 0, hj, vj)})
        elif n == "text_box":
            tam_box = uno(nodo, "size")
            x, y, w, alto = float(at[1]), float(at[2]), float(tam_box[1]), float(tam_box[2])
            m = uno(nodo, "margins")
            mx, my = (float(m[1]), float(m[2])) if m else (0.9525, 0.9525)
            titulo = nodo[1].strip()
            h["recuadros"].append({"caja": (x, y, x + w, y + alto), "titulo": titulo,
                                   "trazo": val(uno(nodo, "stroke", []), "type")})
            if titulo:
                h["textos"].append({"texto": titulo, "de": "recuadro", "caja": caja_texto(
                    x + mx, y + my, titulo, _tam(nodo), 0, "left", "top")})
        elif n == "sheet":
            tam_box = uno(nodo, "size")
            x, y = float(at[1]), float(at[2])
            props = {p[1]: p for p in hijos(nodo, "property") if len(p) > 2}
            nombre = props["Sheetname"][2] if "Sheetname" in props else ""
            h["hojas"].append({"nombre": nombre, "caja": (x, y, x + float(tam_box[1]), y + float(tam_box[2])),
                               "pines": [pt(*uno(p, "at")[1:3]) for p in hijos(nodo, "pin")]})
            for prop in props.values():
                if _oculto(prop) or not prop[2]:
                    continue
                pa = uno(prop, "at")
                hj, vj = _justify(prop)
                h["textos"].append({"texto": prop[2], "de": f"hoja {nombre}", "caja": caja_texto(
                    float(pa[1]), float(pa[2]), prop[2], _tam(prop), float(pa[3]) if len(pa) > 3 else 0, hj, vj)})
    return h


def _nombre(t):
    s = t["texto"].split("\n")[0]
    return s if len(s) <= 30 else s[:29] + "…"


def _p(p):
    return f"({p[0]:g}, {p[1]:g})"


def cruces(h):
    """Cables que cruzan símbolos, subhojas o textos; textos que se solapan entre sí o con un símbolo."""
    malas = []
    obst = [(s["ref"], encoger(c, HOLGURA_SIMBOLO)) for s in h["simbolos"] for c in s["cuerpo"]]
    obst += [(f"un pin de {s['ref']}", c) for s in h["simbolos"] for c in s["tramos_pin"]]
    obst += [(f"la subhoja {x['nombre']}", encoger(x["caja"], HOLGURA_SIMBOLO)) for x in h["hojas"]]
    textos = [(t, encoger(t["caja"], HOLGURA_TEXTO)) for t in h["textos"]]
    for a, b in h["cables"]:
        malas += [f"cable {_p(a)}–{_p(b)} cruza {quien}" for quien, c in obst if cruza(a, b, c)]
        malas += [f"cable {_p(a)}–{_p(b)} cruza el texto «{_nombre(t)}»" for t, c in textos if cruza(a, b, c)]
    for k, (t, c) in enumerate(textos):
        malas += [f"«{_nombre(t)}» ({t['de']}) se solapa con «{_nombre(u)}» ({u['de']})"
                  for u, d in textos[k + 1:] if solapan(c, d)]
        malas += [f"«{_nombre(t)}» ({t['de']}) se solapa con {quien}" for quien, d in obst if solapan(c, d)]
    return list(dict.fromkeys(malas))


def sueltas(h):
    """Etiquetas y símbolos de alimentación que no están en un pin, en un pin de subhoja ni sobre un cable."""
    pines = {p for s in h["simbolos"] if not s["lib"].startswith("power:") for p in s["pines"]}
    pines |= {p for x in h["hojas"] for p in x["pines"]}
    potencia = [s for s in h["simbolos"] if s["lib"].startswith("power:")]
    anclas = {e["pt"] for e in h["etiquetas"]}

    def unido(p, propios=(), con_etiquetas=False):
        return p in pines or any(_hoja.en_tramo(p, a, b) for a, b in h["cables"]) or (con_etiquetas and p in anclas) or \
            any(p in s["pines"] for s in potencia if s["ref"] not in propios)

    malas = [f"{e['tipo'].replace('_', ' ')} «{e['nombre']}» suelta en {_p(e['pt'])}" for e in h["etiquetas"] if not unido(e["pt"])]
    malas += [f"{s['ref']} ({s['lib']}) suelto en {_p(s['pines'][0])}" for s in potencia
              if s["pines"] and not any(unido(p, (s["ref"],), True) for p in s["pines"])]
    return malas


def recuadros_de(h):
    return [r for r in h["recuadros"] if r["trazo"] == "dash_dot" and r["titulo"]]


def fuera_de_recuadro(h):
    """Piezas que no están enteras dentro de un recuadro de trazo y punto con título; recuadros sin título."""
    buenos = recuadros_de(h)
    malas = [f"{s['ref']} fuera de un recuadro" for s in h["simbolos"] if s["pieza"]
             and not any(contiene(r["caja"], s["total"]) for r in buenos)]
    malas += [f"recuadro en {_p(r['caja'][:2])} sin título o sin trazo y punto" for r in h["recuadros"] if r not in buenos]
    return malas


def etiquetas_repetidas(h):
    """Etiquetas con el mismo nombre dos o más veces dentro de un mismo recuadro (unen piezas del bloque)."""
    malas = []
    for r in recuadros_de(h):
        cuenta = {}
        for e in h["etiquetas"]:
            x0, y0, x1, y1 = r["caja"]
            if x0 <= e["pt"][0] <= x1 and y0 <= e["pt"][1] <= y1:
                cuenta[e["nombre"]] = cuenta.get(e["nombre"], 0) + 1
        titulo = r["titulo"].split("\n")[0][:40]
        malas += [f"«{n}» {c} veces en el recuadro «{titulo}»" for n, c in sorted(cuenta.items()) if c > 1]
    return malas
