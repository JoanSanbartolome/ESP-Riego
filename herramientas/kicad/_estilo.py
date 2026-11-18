"""Geometría aproximada de una hoja de esquema para los puntos de estilo de comprobar.py (KIC-06, DEC-0015).

Cajas de símbolos (una por primitiva de dibujo, el núcleo entre los extremos interiores de los pines y los pines), de textos (campos visibles, etiquetas, notas, títulos de recuadro y de
subhoja), cables, recuadros (text_box de trazo y punto) y subhojas. Los textos se miden por la tinta de la
fuente de KiCad (newstroke): avance, tinta y alto de cada glifo, línea base según la justificación y trazo,
medidos en el SVG de `kicad-cli sch export svg` (KiCad 10.0, SPEC-0035, VAL-0035-01-01). Los campos de un
símbolo se colocan con su ángulo y su justificación y luego se giran con el símbolo, como hace KiCad; las
etiquetas y las notas se leen siempre de izquierda a derecha o de abajo arriba. Solo lee el archivo.
"""
import math

from _comun import hijos, leer, parse, simbolos_hoja, trozos, uno, val
import hoja as _hoja

# Glifos de newstroke, en unidades del alto de letra: (avance, borde izquierdo y derecho de la tinta desde el
# origen del glifo, sin el trazo). Medidos con un texto de 1 y de 10 repeticiones de cada carácter.
_GLIFOS = {
    '`': (0.381, 0.174, 0.317), 'j': (0.476, 0.126, 0.365), "!',.:;i": (0.476, 0.269, 0.365), 'í': (0.476, 0.269, 0.412),
    'I': (0.476, 0.317, 0.317), 'l': (0.524, 0.317, 0.46), '^ft–': (0.571, 0.174, 0.555), 'r': (0.619, 0.317, 0.603),
    '\\': (0.667, -0.016, 0.841), ')': (0.667, 0.222, 0.507), ']': (0.667, 0.222, 0.46), '}': (0.667, 0.222, 0.555),
    'º': (0.667, 0.222, 0.603), '{': (0.667, 0.269, 0.603), '(': (0.667, 0.317, 0.603), '[': (0.667, 0.365, 0.603),
    '~': (0.714, 0.174, 0.65), '_': (0.762, 0.079, 0.841), 'T': (0.762, 0.174, 0.746), '*vy': (0.762, 0.222, 0.698),
    'J': (0.762, 0.222, 0.603), '"²': (0.762, 0.269, 0.65), '°': (0.762, 0.317, 0.603), '·': (0.762, 0.412, 0.507),
    'xz': (0.81, 0.222, 0.746), 's': (0.81, 0.269, 0.698), 'L': (0.81, 0.317, 0.793), 'k': (0.81, 0.317, 0.698),
    'AVY': (0.857, 0.174, 0.841), '?ceé': (0.857, 0.269, 0.746), 'F': (0.857, 0.317, 0.793), '§': (0.857, 0.317, 0.698),
    'adgqá': (0.905, 0.269, 0.746), 'oó': (0.905, 0.269, 0.793), 'Ebp': (0.905, 0.317, 0.793),
    'hnuú': (0.905, 0.317, 0.746), '23': (0.952, 0.222, 0.841), '7XZ': (0.952, 0.222, 0.888),
    '$015689Sτ': (0.952, 0.269, 0.841), '4': (0.952, 0.269, 0.888), '|': (0.952, 0.555, 0.555),
    '#': (1.0, 0.174, 0.984), 'CG': (1.0, 0.269, 0.888), 'BDKPR': (1.0, 0.317, 0.888), '/': (1.048, 0.174, 1.031),
    'wØ': (1.048, 0.222, 0.984), 'O': (1.048, 0.269, 0.936), 'Q': (1.048, 0.269, 0.984), 'HNU': (1.048, 0.317, 0.888),
    'µ': (1.048, 0.317, 0.936), 'W': (1.143, 0.222, 1.079), '%Ω': (1.143, 0.269, 1.031), 'M': (1.143, 0.317, 0.984),
    '&': (1.238, 0.317, 1.126), '+-<=>±÷→−≈≤≥': (1.238, 0.317, 1.079), '×': (1.238, 0.412, 0.984),
    '@': (1.286, 0.269, 1.174), 'm': (1.333, 0.317, 1.174), '…': (1.429, 0.269, 1.317),
}
GLIFOS = {c: v for cs, v in _GLIFOS.items() for c in cs}
ESPACIO = 0.762                        # avance de un espacio (sin tinta)
DESCONOCIDO = (1.25, 0.1, 1.2)         # carácter que no está en la tabla: como el más ancho
COLA = 0.16             # KiCad justifica con la suma de avances + COLA (el `textLength` del SVG), en alto de letra
BASE = {"top": 0.844, "center": 0.259, "bottom": -0.326}   # línea base de una línea, desde el ancla, en alto de letra
# tinta por encima de la altura de las mayúsculas (alto total sobre la línea base) y por debajo de la línea base,
# en alto de letra; el resto de glifos, entre la línea base y la altura de las mayúsculas
_SUBEN = {'#[\\]|º': 1.095, '$(){}': 1.143, '/4^`áéíóú': 1.048, '²': 1.286}
_BAJAN = {'#\\': 0.19, '$,;@§': 0.143, '(){}': 0.381, '/': 0.238, 'Q_': 0.095, '[]gjpqy|µ': 0.333}
SUBEN = {c: v for cs, v in _SUBEN.items() for c in cs}
BAJAN = {c: v for cs, v in _BAJAN.items() for c in cs}
INTERLINEA = 1.61       # paso entre líneas / alto de letra
TRAZO = 0.1524          # grosor del trazo de un texto de 1,27 mm (negrita: alto / 5)
HOLGURA_TEXTO = 0.05    # cada caja de tinta se encoge esto por lado antes de comparar (mm)
HOLGURA_SIMBOLO = 0.05
NUCLEO = 0.1           # el núcleo entre los extremos interiores de los pines se ensancha esto por lado (mm)


def ancho_texto(linea, tam):
    """Ancho con el que KiCad justifica una línea (mm): suma de avances más la cola."""
    return (sum(ESPACIO if c == " " else GLIFOS.get(c, DESCONOCIDO)[0] for c in linea) + COLA) * tam


def tinta_linea(linea, tam):
    """(x0, x1) de la tinta de una línea desde su origen, sin el trazo (mm); None si no tiene tinta."""
    x, x0, x1 = 0.0, None, None
    for c in linea:
        if c == " ":
            x += ESPACIO
            continue
        adv, izq, der = GLIFOS.get(c, DESCONOCIDO)
        x0 = x + izq if x0 is None else x0
        x1 = x + der
        x += adv
    return None if x0 is None else (x0 * tam, x1 * tam)


def _rot(dx, dy, ang):
    """Giro antihorario en pantalla (y hacia abajo)."""
    a = math.radians(ang)
    c, s = round(math.cos(a), 9), round(math.sin(a), 9)
    return dx * c + dy * s, -dx * s + dy * c


def caja_texto(x, y, texto, tam, ang, hj, vj, legible=True, extra=0.0, alto=None, desplazar=0.0, trazo=TRAZO):
    """Caja (x0, y0, x1, y1) de la tinta de un texto anclado en (x, y). `legible`: etiquetas y notas (ángulo
    módulo 180). `extra` y `alto`: etiqueta global o jerárquica, caja de su forma (largo añadido y alto) con el
    ancho de justificación del texto; `desplazar`: separación del texto sobre su ancla (etiquetas locales)."""
    lineas = str(texto).split("\n") or [""]
    if alto is not None:
        largo = max(ancho_texto(l, tam) for l in lineas) + extra
        x0 = {"left": 0.0, "right": -largo}.get(hj, -largo / 2)
        cajas = [(x0, -alto / 2, x0 + largo, alto / 2)]
    else:
        paso, n = INTERLINEA * tam, len(lineas)
        base = BASE.get(vj, BASE["center"]) * tam - (n - 1) * paso * {"top": 0, "bottom": 1}.get(vj, 0.5)
        base += {"top": desplazar, "bottom": -desplazar}.get(vj, 0.0)
        cajas = []
        for k, l in enumerate(lineas):
            t = tinta_linea(l, tam)
            if t is None:
                continue
            w = ancho_texto(l, tam)
            dx = {"left": 0.0, "right": -w}.get(hj, -w / 2)
            b = base + k * paso
            arriba = b - max([1.0] + [SUBEN.get(c, 1.3 if c not in GLIFOS and c != " " else 1.0) for c in l]) * tam
            abajo = b + max([0.0] + [BAJAN.get(c, 0.4 if c not in GLIFOS and c != " " else 0.0) for c in l]) * tam
            cajas.append((dx + t[0] - trazo / 2, arriba - trazo / 2, dx + t[1] + trazo / 2, abajo + trazo / 2))
        if not cajas:
            return (x, y, x, y)
    ang = ang % 180 if legible else ang % 360
    pts = [_rot(px, py, ang) for c in cajas for px in (c[0], c[2]) for py in (c[1], c[3])]
    return (x + min(p[0] for p in pts), y + min(p[1] for p in pts), x + max(p[0] for p in pts), y + max(p[1] for p in pts))


def _justify(nodo):
    j = uno(uno(nodo, "effects", []), "justify", ["justify"])[1:]
    hj = "left" if "left" in j else "right" if "right" in j else "center"
    vj = "top" if "top" in j else "bottom" if "bottom" in j else "center"
    return hj, vj


def _tam(nodo):
    tam = uno(uno(uno(nodo, "effects", []), "font", []), "size")
    return float(tam[1]) if tam else 1.27


def _trazo(nodo):
    fuente = uno(uno(nodo, "effects", []), "font", [])
    return _tam(nodo) / 5 if val(fuente, "bold") == "yes" or "bold" in fuente else TRAZO


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
                float(at[1]), float(at[2]), prop[2], _tam(prop), ang, hj, vj, legible=False, trazo=_trazo(prop))})
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
                caja = caja_texto(float(at[1]), float(at[2]), nodo[1], tam, ang, hj, vj, desplazar=0.1)
            else:
                caja = caja_texto(float(at[1]), float(at[2]), nodo[1], tam, ang, hj, "center", extra=1.2 * tam, alto=1.4 * tam)
            e = {"tipo": n, "nombre": nodo[1], "pt": pt(at[1], at[2]), "caja": caja}
            h["etiquetas"].append(e)
            h["textos"].append({"texto": nodo[1], "de": n, "caja": caja})
        elif n == "text":
            hj, vj = _justify(nodo)
            h["textos"].append({"texto": nodo[1], "de": "nota", "caja": caja_texto(
                float(at[1]), float(at[2]), nodo[1], _tam(nodo), float(at[3]) if len(at) > 3 else 0, hj, vj,
                trazo=_trazo(nodo))})
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
                    x + mx, y + my, titulo, _tam(nodo), 0, "left", "top", trazo=_trazo(nodo))})
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
