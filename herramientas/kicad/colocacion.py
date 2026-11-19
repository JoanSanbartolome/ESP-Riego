"""Colocación en texto: extrae las huellas de la PCB en formato compacto y puntúa una colocación.

Uso:
    python herramientas/kicad/colocacion.py extraer hardware/v2 -o huellas.txt
    python herramientas/kicad/colocacion.py extraer hardware/v2 --refs U5,J4      (con pads; en pantalla)
    python herramientas/kicad/colocacion.py evaluar hardware/v2 colocacion.csv [--detalle informe.txt]

extraer: por huella, ref, valor, x y giro (b = cara inferior), patio sin girar (AxB centrado en el
  ancla, o x0,y0,x1,y1) y las redes de sus pads, agrupadas por bloque (hoja). --refs añade la
  posición de cada pad, sin girar. Sin --refs, el listado va a -o y en pantalla sale el tamaño.
evaluar: aplica la tabla de colocar.py (ref,x,y,giro,cara; opcional) a una copia de la PCB con el
  mismo código que colocar.py y da, en ≤ 30 líneas: solapes de patio, piezas fuera del contorno,
  piezas en una zona prohibida (áreas de regla con «no footprints», p. ej. la antena de U5), reglas
  de colocación incumplidas (--reglas; por defecto docs/diseno/colocacion-reglas.csv) y la longitud
  de las conexiones sin rutar (árbol mínimo por red, centros de pad), total y por clase.
  PUNTOS = 1000 × obligatorias + 100 × objetivos + longitud ponderada / 10: menor es mejor.
  Código 0 sin incumplimientos obligatorios; 1 si los hay. --detalle guarda la lista completa.
Reglas: CSV `id;tipo;piezas;objetivo;valor;nivel;origen;nota` (formato en el README).
"""
import argparse
import csv
import fnmatch
import io
import math
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import MAX_LINEAS, Fallo, con_python_kicad, emitir, raiz_repo, principal  # noqa: E402

LADOS = {"sup", "inf", "izq", "der", "lateral", "largo"}
DIRECCIONES = {"+x": (1, 0), "-x": (-1, 0), "+y": (0, 1), "-y": (0, -1)}
TIPOS = {"cara", "fija", "borde", "hacia", "orden", "entre", "fila", "zona", "cerca", "cerca_par", "lejos",
         "libre", "opuesto", "sale", "clase"}
PESO_OBLIGATORIA, PESO_OBJETIVO, DIVISOR_LONGITUD = 1000, 100, 10
EPS_AREA = 0.01  # mm²: por debajo, dos patios solo se tocan


# ------------------------------------------------------------------ utilidades sin pcbnew

def estimar_tokens(texto):
    """Tokens aproximados de un texto: palabras de 4 letras por token, cifras de 3 en 3, cada signo 1."""
    n = 0
    for m in re.finditer(r"[^\W\d]+|\d+|[^\w\s]|\n", texto):
        t = m.group()
        if t[0].isdigit():
            n += math.ceil(len(t) / 3)
        elif t[0].isalpha() or t[0] == "_":
            n += max(1, math.ceil(len(t) / 4))
        else:
            n += 1
    return n


def numero(texto):
    return float(str(texto).strip().replace(",", "."))


def _clave_ref(r):
    base = r.rstrip("0123456789")
    return base, int("0" + r[len(base):])


def expandir(texto):
    """«J4-J6 U5.2 U7-U12.6 U5/antena» → operandos (ref, pad o None, sufijo o None), en orden.
    Las piezas se separan con espacios; `*` son todas."""
    salida = []
    for trozo in str(texto or "").split():
        sufijo = None
        if "/" in trozo:
            trozo, sufijo = trozo.split("/", 1)
        pad = None
        m = re.fullmatch(r"([A-Za-z_#]+)(\d+)-(?:[A-Za-z_#]+)?(\d+)(?:\.(\w+))?", trozo)
        if m:
            base, a, b, pad = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
            paso = 1 if b >= a else -1
            salida += [(f"{base}{k}", pad, sufijo) for k in range(a, b + paso, paso)]
            continue
        if "." in trozo:
            trozo, pad = trozo.split(".", 1)
        salida.append((trozo, pad, sufijo))
    return salida


def leer_reglas(ruta):
    """Filas del CSV de reglas, comprobadas. Devuelve (reglas, clases)."""
    texto = Path(ruta).read_text(encoding="utf-8-sig")
    lineas = [l for l in texto.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not lineas:
        raise Fallo(f"{ruta}: tabla de reglas vacía")
    sep = ";" if lineas[0].count(";") >= lineas[0].count(",") else ","
    reglas, clases = [], []
    for n, fila in enumerate(csv.DictReader(io.StringIO("\n".join(lineas)), delimiter=sep), start=2):
        fila = {(k or "").strip().lower(): (v or "").strip() for k, v in fila.items()}
        tipo = fila.get("tipo", "").lower()
        if tipo not in TIPOS:
            raise Fallo(f"{ruta}: regla {fila.get('id') or n}: tipo «{tipo}» desconocido ({', '.join(sorted(TIPOS))})")
        nivel = fila.get("nivel", "obligatoria").lower() or "obligatoria"
        if nivel not in ("obligatoria", "objetivo"):
            raise Fallo(f"{ruta}: regla {fila.get('id')}: nivel «{nivel}» (obligatoria u objetivo)")
        if not fila.get("origen"):
            raise Fallo(f"{ruta}: regla {fila.get('id')}: sin origen")
        r = {"id": fila.get("id") or f"L{n}", "tipo": tipo, "piezas": fila.get("piezas", ""),
             "objetivo": fila.get("objetivo", ""), "valor": fila.get("valor", ""), "nivel": nivel,
             "origen": fila["origen"], "nota": fila.get("nota", "")}
        if tipo in ("borde", "hacia") and r["objetivo"] not in LADOS:
            raise Fallo(f"{ruta}: regla {r['id']}: borde «{r['objetivo']}» ({', '.join(sorted(LADOS))})")
        if tipo == "hacia" and r["valor"] not in DIRECCIONES:
            raise Fallo(f"{ruta}: regla {r['id']}: dirección «{r['valor']}» ({', '.join(DIRECCIONES)})")
        if tipo in ("borde", "fila", "zona", "cerca", "cerca_par", "lejos", "libre", "clase"):
            try:
                r["mm"] = numero(r["valor"])
            except ValueError:
                raise Fallo(f"{ruta}: regla {r['id']}: valor «{r['valor']}» no es un número")
        (clases if tipo == "clase" else reglas).append(r)
    return reglas, clases


def clase_de(red, clases):
    """(clase, peso) de una red según las filas `clase` (primera que casa); si no, Default con peso 1."""
    nombres = {red, red.lstrip("/"), red.rstrip("/").split("/")[-1]}
    for c in clases:
        for patron in c["piezas"].split():
            if any(fnmatch.fnmatchcase(n, patron) for n in nombres):
                return c["objetivo"], c["mm"]
    return "Default", 1.0


def alias_redes(redes):
    """{red: nombre corto único}: el último tramo de la ruta si no se repite; si no, los dos últimos."""
    ultimos = {}
    for r in redes:
        ultimos.setdefault(r.rstrip("/").split("/")[-1], set()).add(r)
    salida = {}
    for r in redes:
        partes = r.strip("/").split("/")
        salida[r] = partes[-1] if len(ultimos[partes[-1]]) == 1 else "/".join(partes[-2:])
    return salida


def rangos(numeros):
    """[1, 2, 3, 7] → «1-3,7» (los pads no numéricos van al final, tal cual)."""
    nums = sorted({int(n) for n in numeros if n.isdigit()})
    otros = sorted({n for n in numeros if not n.isdigit()})
    trozos, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        trozos.append(f"{nums[i]}-{nums[j]}" if j > i + 1 else ",".join(map(str, nums[i:j + 1])))
        i = j + 1
    return ",".join(trozos + otros)


def f(x, dec=2):
    s = "%.*f" % (dec, x)
    s = s.rstrip("0").rstrip(".") if "." in s else s
    return "0" if s in ("-0", "") else s


# ------------------------------------------------------------------ geometría (anillos de puntos en mm)

def _dist_punto_seg(p, a, b):
    ax, ay, bx, by = a[0], a[1], b[0], b[1]
    dx, dy = bx - ax, by - ay
    l2 = dx * dx + dy * dy
    t = 0 if l2 == 0 else max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / l2))
    return math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy)


def _cruzan(a, b, c, d):
    def o(p, q, r):
        v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        return (v > 1e-12) - (v < -1e-12)
    return o(a, b, c) * o(a, b, d) < 0 and o(c, d, a) * o(c, d, b) < 0


def dentro_anillo(p, anillo):
    x, y, dentro = p[0], p[1], False
    for i in range(len(anillo)):
        (x1, y1), (x2, y2) = anillo[i - 1], anillo[i]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            dentro = not dentro
    return dentro


def distancia(A, B):
    """Distancia mínima entre dos conjuntos de anillos (polígonos sin agujeros); 0 si se tocan o se contienen."""
    if not A or not B:
        return math.inf
    for a in A:
        for b in B:
            if dentro_anillo(a[0], b) or dentro_anillo(b[0], a):
                return 0.0
    mejor = math.inf
    for a in A:
        for b in B:
            for i in range(len(a)):
                p, q = a[i - 1], a[i]
                for j in range(len(b)):
                    r, s = b[j - 1], b[j]
                    if _cruzan(p, q, r, s):
                        return 0.0
                    mejor = min(mejor, _dist_punto_seg(p, r, s), _dist_punto_seg(r, p, q))
    return mejor


def caja_de(anillos):
    xs = [p[0] for a in anillos for p in a]
    ys = [p[1] for a in anillos for p in a]
    return min(xs), min(ys), max(xs), max(ys)


def a_borde(anillos, caja_placa, lado):
    """Distancia del objeto al borde `lado` de la caja de la placa (negativa si lo cruza) y el lado más cercano."""
    x0, y0, x1, y1 = caja_de(anillos)
    X0, Y0, X1, Y1 = caja_placa
    d = {"sup": y0 - Y0, "inf": Y1 - y1, "izq": x0 - X0, "der": X1 - x1}
    if lado in d:
        return d[lado], lado
    opciones = ("izq", "der") if lado == "lateral" else ("sup", "inf")
    k = min(opciones, key=lambda o: d[o])
    return d[k], k


def girar(v, grados):
    """Vector de la huella (sin girar) al de la placa con el giro de KiCad (antihorario en pantalla, y hacia abajo)."""
    t = math.radians(grados)
    return v[0] * math.cos(t) + v[1] * math.sin(t), -v[0] * math.sin(t) + v[1] * math.cos(t)


def a_local(p, ancla, grados):
    t = math.radians(grados)
    dx, dy = p[0] - ancla[0], p[1] - ancla[1]
    return dx * math.cos(t) - dy * math.sin(t), dx * math.sin(t) + dy * math.cos(t)


def arbol_minimo(puntos):
    """Longitud del árbol de expansión mínimo (Prim) entre puntos (x, y)."""
    if len(puntos) < 2:
        return 0.0
    dist = [math.inf] * len(puntos)
    dentro, total, actual = [False] * len(puntos), 0.0, 0
    dentro[0] = True
    for _ in range(len(puntos) - 1):
        px, py = puntos[actual]
        mejor, k = math.inf, -1
        for i, (x, y) in enumerate(puntos):
            if dentro[i]:
                continue
            d = math.hypot(x - px, y - py)
            if d < dist[i]:
                dist[i] = d
            if dist[i] < mejor:
                mejor, k = dist[i], i
        dentro[k], total, actual = True, total + mejor, k
    return total


# ------------------------------------------------------------------ modelo de la placa (pcbnew)

def _anillos(poly, pcbnew):
    salida = []
    for i in range(poly.OutlineCount()):
        o = poly.Outline(i)
        salida.append([(pcbnew.ToMM(o.CPoint(k).x), pcbnew.ToMM(o.CPoint(k).y)) for k in range(o.PointCount())])
    return salida


def cargar(pcb, tabla=None):
    """Carga la PCB en una copia temporal y aplica la tabla con colocar.aplicar. Devuelve (modelo, info)."""
    con_python_kicad(__file__)
    import pcbnew
    import colocar

    origen = Path(pcb).resolve()
    if origen.is_dir():
        pcbs = sorted(origen.glob("*.kicad_pcb"))
        if len(pcbs) != 1:
            raise Fallo(f"se esperaba un único .kicad_pcb en {origen} y hay {len(pcbs)}")
        origen = pcbs[0]
    if not origen.is_file():
        raise Fallo(f"no existe {origen}")
    filas = colocar.leer_tabla(tabla) if tabla else []
    with tempfile.TemporaryDirectory(prefix="colocacion_") as tmp:
        copia = Path(tmp) / origen.name
        shutil.copyfile(origen, copia)
        board = pcbnew.LoadBoard(str(copia))
        antes = {fp.GetReference(): (pcbnew.ToMM(fp.GetPosition().x), pcbnew.ToMM(fp.GetPosition().y),
                                     fp.GetOrientationDegrees(), fp.IsFlipped()) for fp in board.GetFootprints()}
        movidas, faltan, _ = colocar.aplicar(board, filas)
        modelo = modelo_de(board, pcbnew)
    for ref, h in modelo["huellas"].items():
        h["antes"] = antes[ref]
    return modelo, {"pcb": origen, "filas": len(filas), "movidas": movidas, "faltan": faltan}


def modelo_de(board, pcbnew):
    contorno = pcbnew.SHAPE_POLY_SET()
    if not board.GetBoardPolygonOutlines(contorno, False) or not contorno.OutlineCount():
        raise Fallo("la PCB no tiene un contorno cerrado en Edge.Cuts")
    huellas, redes = {}, {}
    for fp in board.GetFootprints():
        fp.BuildCourtyardCaches()
        ref = fp.GetReference()
        b = fp.IsFlipped()
        patio = pcbnew.SHAPE_POLY_SET(fp.GetCourtyard(pcbnew.B_CrtYd if b else pcbnew.F_CrtYd))
        if not patio.OutlineCount():
            caja = fp.GetBoundingBox(False)
            patio.NewOutline()
            for x, y in ((caja.GetLeft(), caja.GetTop()), (caja.GetRight(), caja.GetTop()),
                         (caja.GetRight(), caja.GetBottom()), (caja.GetLeft(), caja.GetBottom())):
                patio.Append(x, y)
        zonas = pcbnew.SHAPE_POLY_SET()
        for z in fp.Zones():
            if z.GetIsRuleArea() and (z.GetDoNotAllowFootprints() or z.GetDoNotAllowPads()):
                zonas.BooleanAdd(z.Outline())
        fab = [g.GetBoundingBox() for g in fp.GraphicalItems()
               if g.GetLayer() in (pcbnew.F_Fab, pcbnew.B_Fab) and g.GetClass() == "PCB_SHAPE"]
        pos = (pcbnew.ToMM(fp.GetPosition().x), pcbnew.ToMM(fp.GetPosition().y))
        pads = []
        for p in fp.Pads():
            num = p.GetNumber()
            if not num:
                continue  # ventanas de pasta
            red = p.GetNetname()
            pp = pcbnew.SHAPE_POLY_SET()
            p.TransformShapeToPolygon(pp, pcbnew.B_Cu if b and not p.IsOnLayer(pcbnew.F_Cu) else pcbnew.F_Cu, 0,
                                      pcbnew.FromMM(0.02), pcbnew.ERROR_INSIDE)
            rel = p.GetFPRelativePosition()
            pads.append({"num": num, "red": red, "x": pcbnew.ToMM(p.GetPosition().x), "y": pcbnew.ToMM(p.GetPosition().y),
                         "lx": pcbnew.ToMM(rel.x), "ly": pcbnew.ToMM(rel.y), "anillos": _anillos(pp, pcbnew)})
            if red and not red.startswith("unconnected-"):
                redes.setdefault(red, {}).setdefault((ref, num), (pads[-1]["x"], pads[-1]["y"]))
        h = {"ref": ref, "valor": fp.GetValue(), "bloque": fp.GetSheetname().strip("/").split("/")[-1] or "/",
             "x": pos[0], "y": pos[1], "giro": fp.GetOrientationDegrees(), "cara": "B" if b else "F",
             "fija": fp.IsLocked(), "patio_poly": patio, "patio": _anillos(patio, pcbnew), "pads": pads,
             "zonas_poly": zonas, "zonas": _anillos(zonas, pcbnew)}
        h["cuerpo_poly"] = pcbnew.SHAPE_POLY_SET(patio)
        if zonas.OutlineCount():
            h["cuerpo_poly"].BooleanSubtract(zonas)
            if fab:
                x0 = min(pcbnew.ToMM(c.GetLeft()) for c in fab)
                y0 = min(pcbnew.ToMM(c.GetTop()) for c in fab)
                x1 = max(pcbnew.ToMM(c.GetRight()) for c in fab)
                y1 = max(pcbnew.ToMM(c.GetBottom()) for c in fab)
                cuerpo = pcbnew.SHAPE_POLY_SET()
                cuerpo.NewOutline()
                for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
                    cuerpo.Append(pcbnew.FromMM(x), pcbnew.FromMM(y))
                cuerpo.BooleanIntersection(zonas)
                h["antena"] = _anillos(cuerpo, pcbnew)
        huellas[ref] = h
    caja = caja_de(_anillos(contorno, pcbnew))
    return {"huellas": huellas, "redes": redes, "contorno_poly": contorno, "contorno": _anillos(contorno, pcbnew),
            "caja": caja, "pcbnew": pcbnew}


# ------------------------------------------------------------------ extraer

def texto_extraer(modelo, nombre, refs=None):
    H, caja = modelo["huellas"], modelo["caja"]
    utiles = {r for r, nodos in modelo["redes"].items() if len(nodos) >= 2}
    nombres = alias_redes(sorted(utiles))
    lineas = []
    if not refs:
        lineas += [
            f"# colocacion.py extraer · {nombre} · {len(H)} huellas · {len(utiles)} redes de ≥ 2 pads",
            f"# contorno x {f(caja[0])}…{f(caja[2])}, y {f(caja[1])}…{f(caja[3])} ({f(caja[2] - caja[0])}×{f(caja[3] - caja[1])} mm);"
            " y crece hacia abajo; giro en grados, antihorario",
            "# REF valor x y giro[b = cara inferior] patio sin girar (AxB centrado en el ancla, o x0,y0,x1,y1) [* = fija]"
            " | redes de los pads en orden (- sin red), o red:pads con más de 4 pads",
        ]
    bloques = {}
    for h in H.values():
        if refs and h["ref"] not in refs:
            continue
        bloques.setdefault(h["bloque"], []).append(h)
    for bloque in sorted(bloques, key=lambda b: (b.startswith("Canal"), b)):
        if not refs:
            lineas.append(f"## {bloque} ({len(bloques[bloque])})")
        for h in sorted(bloques[bloque], key=lambda h: _clave_ref(h["ref"])):
            loc = [a_local(p, (h["x"], h["y"]), h["giro"]) for a in h["patio"] for p in a]
            x0, y0 = min(p[0] for p in loc), min(p[1] for p in loc)
            x1, y1 = max(p[0] for p in loc), max(p[1] for p in loc)
            if abs(x0 + x1) < 0.06 and abs(y0 + y1) < 0.06:
                patio = f"{f(x1 - x0, 1)}x{f(y1 - y0, 1)}"
            else:
                patio = ",".join(f(v, 1) for v in (x0, y0, x1, y1))
            giro = f(h["giro"], 1) + ("b" if h["cara"] == "B" else "")
            valor = re.sub(r"\s+", "_", h["valor"])[:14]
            linea = f"{h['ref']} {valor} {f(h['x'])} {f(h['y'])} {giro} {patio}{' *' if h['fija'] else ''}"
            pads = {}
            for p in h["pads"]:
                pads.setdefault(p["num"], p)
            if h["zonas"]:
                loc = [a_local(q, (h["x"], h["y"]), h["giro"]) for a in h["zonas"] for q in a]
                linea += " zona " + ",".join(f(v, 1) for v in (min(q[0] for q in loc), min(q[1] for q in loc),
                                                                 max(q[0] for q in loc), max(q[1] for q in loc)))
            if refs:
                linea += " | " + " ".join(f"{n}({f(p['lx'])},{f(p['ly'])}){nombres.get(p['red'], '-')}"
                                          for n, p in sorted(pads.items(), key=lambda kv: _clave_ref("P" + kv[0])))
            elif len(pads) <= 4:
                orden = sorted(pads, key=lambda n: _clave_ref("P" + n))
                linea += " | " + " ".join(nombres.get(pads[n]["red"], "-") for n in orden)
            else:
                grupos = {}
                for n, p in pads.items():
                    if p["red"] in nombres:
                        grupos.setdefault(nombres[p["red"]], []).append(n)
                sin = sum(1 for p in pads.values() if p["red"] not in nombres)
                linea += " | " + " ".join(f"{r}:{rangos(ns)}" for r, ns in sorted(grupos.items(), key=lambda kv: _clave_ref("P" + sorted(kv[1], key=lambda n: _clave_ref('P' + n))[0])))
                if sin:
                    linea += f" (sin red {sin})"
            lineas.append(linea)
    return "\n".join(lineas) + "\n"


# ------------------------------------------------------------------ evaluar

class Operando:
    def __init__(self, modelo, ref, pad, sufijo):
        h = modelo["huellas"].get(ref)
        self.nombre = ref + (f".{pad}" if pad else "") + (f"/{sufijo}" if sufijo else "")
        self.h = h
        if h is None:
            raise KeyError(self.nombre)
        if pad:
            self.anillos = [a for p in h["pads"] if p["num"] == pad for a in p["anillos"]]
            if not self.anillos:
                raise KeyError(self.nombre)
        elif sufijo == "antena":
            self.anillos = h.get("antena") or h["zonas"]
        elif sufijo == "zona":
            self.anillos = h["zonas"]
        else:
            self.anillos = h["patio"]
        if not self.anillos:
            raise KeyError(self.nombre)


def _operandos(modelo, texto, errores, regla):
    salida = []
    if texto.strip() == "*":
        return [Operando(modelo, r, None, None) for r in sorted(modelo["huellas"], key=_clave_ref)]
    for ref, pad, suf in expandir(texto):
        try:
            salida.append(Operando(modelo, ref, pad, suf))
        except KeyError as e:
            errores.append(f"{regla['id']}: {e.args[0]} no existe en la PCB")
    return salida


def _area(poly):
    return poly.Area() / 1e12


def evaluar(modelo, reglas, clases):
    """(incidencias, errores, {clase: [longitud, peso]}, {red: longitud}). Cada incidencia: clase (solape, fuera,
    zona, regla), nivel, regla (id), cab (la regla en pocas palabras), item (la pieza y la cifra) y exceso."""
    pcbnew = modelo["pcbnew"]
    H, caja = modelo["huellas"], modelo["caja"]
    inc, errores = [], []

    def anota(clase, nivel, item, regla="", exceso=0.0, cab=""):
        inc.append({"clase": clase, "nivel": nivel, "item": item, "regla": regla, "exceso": exceso, "cab": cab})

    salen = set()
    for r in reglas:
        if r["tipo"] == "sale":
            salen |= {o[0] for o in expandir(r["piezas"])}

    refs = sorted(H, key=_clave_ref)
    cajas = {r: caja_de(H[r]["patio"]) for r in refs}
    # solapes de patio (misma cara; el patio de una pieza con zona prohibida se mide sin la zona)
    for i, a in enumerate(refs):
        for b in refs[i + 1:]:
            if H[a]["cara"] != H[b]["cara"]:
                continue
            ca, cb = cajas[a], cajas[b]
            if ca[2] <= cb[0] or cb[2] <= ca[0] or ca[3] <= cb[1] or cb[3] <= ca[1]:
                continue
            s = pcbnew.SHAPE_POLY_SET(H[a]["cuerpo_poly"])
            s.BooleanIntersection(H[b]["cuerpo_poly"])
            if _area(s) > EPS_AREA:
                anota("solape", "obligatoria", f"{a}/{b} {f(_area(s), 1)} mm²", exceso=_area(s))
    # fuera del contorno
    X0, Y0, X1, Y1 = caja
    for r in refs:
        h = H[r]
        s = pcbnew.SHAPE_POLY_SET(h["patio_poly"])
        s.BooleanSubtract(modelo["contorno_poly"])
        if r in salen and h["zonas_poly"].OutlineCount():
            s.BooleanSubtract(h["zonas_poly"])
        if _area(s) > EPS_AREA:
            x0, y0, x1, y1 = cajas[r]
            sale = max(X0 - x0, Y0 - y0, x1 - X1, y1 - Y1, 0)
            anota("fuera", "obligatoria", f"{r} {f(sale, 1)} mm" if sale else f"{r} {f(_area(s), 1)} mm²", exceso=sale)
    # zonas prohibidas de las huellas (áreas de regla sin huellas o sin pads), dentro de la placa
    for z in refs:
        if not H[z]["zonas_poly"].OutlineCount():
            continue
        zc = caja_de(H[z]["zonas"])
        for r in refs:
            c = cajas[r]
            if r == z or c[2] <= zc[0] or zc[2] <= c[0] or c[3] <= zc[1] or zc[3] <= c[1]:
                continue
            s = pcbnew.SHAPE_POLY_SET(H[r]["patio_poly"])
            s.BooleanIntersection(H[z]["zonas_poly"])
            s.BooleanIntersection(modelo["contorno_poly"])
            if _area(s) > EPS_AREA:
                anota("zona", "obligatoria", f"{r} en {z}/zona {f(_area(s), 1)} mm²", exceso=_area(s))
    # bloqueadas en la PCB
    for r in refs:
        h = H[r]
        x, y, g, b = h["antes"]
        if h["fija"] and (abs(h["x"] - x) > 0.005 or abs(h["y"] - y) > 0.005 or abs(h["giro"] - g) > 0.01
                          or (h["cara"] == "B") != b):
            anota("regla", "obligatoria", f"{r} movida de {f(x)},{f(y)}", "bloqueada", cab="bloqueada en la PCB")

    def en_placa(anillos):
        x0, y0, x1, y1 = caja_de(anillos)
        return x0 <= X1 + 0.01 and x1 >= X0 - 0.01 and y0 <= Y1 + 0.01 and y1 >= Y0 - 0.01

    for r in reglas:
        t, nivel, rid, lim = r["tipo"], r["nivel"], r["id"], r.get("mm")
        if t == "sale":
            continue
        piezas = _operandos(modelo, r["piezas"], errores, r)
        destino = _operandos(modelo, r["objetivo"], errores, r) if t in ("cerca", "cerca_par", "lejos", "entre", "opuesto") else []

        def mal(item, exceso=0.0, cab=None):
            anota("regla", nivel, item, rid, exceso, cab or f"{rid} {t} {r['piezas']}")

        if t == "cara":
            for o in piezas:
                if o.h["cara"] != (r["objetivo"] or "F").upper():
                    mal(f"{o.nombre} en {o.h['cara']}", cab=f"{rid} cara {r['objetivo'] or 'F'}")
        elif t == "fija":
            for o in piezas:
                x, y, g, b = o.h["antes"]
                if abs(o.h["x"] - x) > 0.005 or abs(o.h["y"] - y) > 0.005 or abs(o.h["giro"] - g) > 0.01:
                    mal(f"{o.nombre} movida de {f(x)},{f(y)}")
        elif t == "borde":
            cab = f"{rid} borde {r['objetivo']} ≤ {f(lim)}"
            for o in piezas:
                d, lado = a_borde(o.anillos, caja, r["objetivo"])
                if not en_placa(o.anillos):
                    mal(f"{o.nombre} fuera de la placa", 100.0, cab)
                elif d > lim + 1e-6:
                    mal(f"{o.nombre} {f(d, 1)}" + (f" ({lado})" if lado != r["objetivo"] else ""), d - lim, cab)
        elif t == "hacia":
            v = DIRECCIONES[r["valor"]]
            cab = f"{rid} {r['valor']} hacia {r['objetivo']}"
            for o in piezas:
                if o.h["cara"] != "F":
                    mal(f"{o.nombre} en B", cab=cab)
                    continue
                wx, wy = girar(v, o.h["giro"])
                _, lado = a_borde(o.h["patio"], caja, r["objetivo"])
                quiere = {"sup": (0, -1), "inf": (0, 1), "izq": (-1, 0), "der": (1, 0)}[lado]
                if wx * quiere[0] + wy * quiere[1] < 0.99:
                    mal(f"{o.nombre} giro {f(o.h['giro'], 1)}", cab=cab)
        elif t == "orden":
            xs = [(o.nombre, o.h["x"]) for o in piezas]
            for (a, xa), (b, xb) in zip(xs, xs[1:]):
                if xa >= xb:
                    mal(f"{a} x {f(xa, 1)} ≥ {b} x {f(xb, 1)}", cab=f"{rid} orden {r['piezas']} (izquierda a derecha)")
        elif t == "entre":
            if len(destino) == 2:
                a, b = sorted(d.h["x"] for d in destino)
                for o in piezas:
                    if not a < o.h["x"] < b:
                        mal(f"{o.nombre} x {f(o.h['x'], 1)} fuera de {f(a, 1)}…{f(b, 1)}", cab=f"{rid} {r['piezas']} entre {r['objetivo']}")
        elif t == "fila":
            cab = f"{rid} fila {r['piezas']} paso ≥ {f(lim)}"
            ys = [o.h["y"] for o in piezas]
            xs = [o.h["x"] for o in piezas]
            if ys and max(ys) - min(ys) > 0.5:
                mal(f"Δy {f(max(ys) - min(ys), 1)} (≤ 0,5)", max(ys) - min(ys), cab)
            for o, a, b in zip(piezas[1:], xs, xs[1:]):
                if b - a < lim - 1e-6:
                    mal(f"{o.nombre} paso {f(b - a, 2)}", lim - (b - a), cab)
        elif t == "zona":
            if r["objetivo"] == "centro":
                alto = caja[3] - caja[1]
                ya, yb = caja[1] + alto * (1 - lim / 100) / 2, caja[3] - alto * (1 - lim / 100) / 2
                cab = f"{rid} {r['piezas']} en la franja y {f(ya, 1)}…{f(yb, 1)}"
                for o in piezas:
                    x0, y0, x1, y1 = caja_de(o.anillos)
                    if y0 < ya - 1e-6 or y1 > yb + 1e-6 or not en_placa(o.anillos):
                        mal(f"{o.nombre} y {f(y0, 1)}…{f(y1, 1)}", max(ya - y0, y1 - yb), cab)
        elif t in ("cerca", "lejos"):
            signo = "≤" if t == "cerca" else "≥"
            cab = f"{rid} {r['piezas']} {signo} {f(lim)} de {r['objetivo']}"
            for o in piezas:
                d = distancia(o.anillos, [a for dd in destino if dd.h is not o.h for a in dd.anillos])
                if t == "cerca" and d > lim + 1e-6:
                    mal(f"{o.nombre} {f(d, 1)}", d - lim, cab)
                if t == "lejos" and d < lim - 1e-6:
                    mal(f"{o.nombre} {f(d, 1)}", lim - d, cab)
        elif t == "cerca_par":
            if len(piezas) != len(destino):
                errores.append(f"{rid}: {len(piezas)} piezas y {len(destino)} objetivos (cerca_par los empareja)")
            cab = f"{rid} {r['piezas']} ≤ {f(lim)} de {r['objetivo']} (por pares)"
            for o, d in zip(piezas, destino):
                dd = distancia(o.anillos, d.anillos)
                if dd > lim + 1e-6:
                    mal(f"{o.nombre}–{d.nombre} {f(dd, 1)}", dd - lim, cab)
        elif t == "libre":
            cab = f"{rid} Ø {f(2 * lim)} libre en {r['piezas']}"
            for o in piezas:
                c = (o.h["x"], o.h["y"])
                for otro in refs:
                    if otro != o.h["ref"]:
                        d = distancia([[c]], H[otro]["patio"])
                        if d < lim - 1e-6:
                            mal(f"{otro} a {f(d, 1)} de {o.nombre}", lim - d, cab)
        elif t == "opuesto":
            medio = (caja[0] + caja[2]) / 2
            for o in piezas:
                for d in destino:
                    ca, cb = caja_de(o.anillos), caja_de(d.anillos)
                    if ((ca[0] + ca[2]) / 2 - medio) * ((cb[0] + cb[2]) / 2 - medio) > 0:
                        mal(f"{o.nombre} y {d.nombre} en la misma mitad", cab=f"{rid} {r['piezas']} en el lateral opuesto a {r['objetivo']}")

    # longitud sin rutar: árbol mínimo por red entre los centros de sus pads
    por_clase, por_red, clase_red = {}, {}, {}
    for red, nodos in modelo["redes"].items():
        if len(nodos) < 2:
            continue
        largo = arbol_minimo(list(nodos.values()))
        clase, peso = clase_de(red, clases)
        por_clase.setdefault(clase, [0.0, peso])[0] += largo
        por_red[red] = largo
        clase_red[red] = clase
    modelo["clase_red"] = clase_red
    return inc, errores, por_clase, por_red


def puntuar(inc, por_clase):
    obl = sum(1 for i in inc if i["nivel"] == "obligatoria")
    obj = sum(1 for i in inc if i["nivel"] == "objetivo")
    pond = sum(v[0] * v[1] for v in por_clase.values())
    return PESO_OBLIGATORIA * obl + PESO_OBJETIVO * obj + pond / DIVISOR_LONGITUD, obl, obj, pond


def _lista(items, n=8, ancho=150):
    txt = ""
    for k, i in enumerate(items):
        trozo = (" · " if txt else "") + i
        if k >= n or len(txt) + len(trozo) > ancho:
            return txt + f" · +{len(items) - k}"
        txt += trozo
    return txt


def informe(modelo, info, reglas, ruta_reglas, inc, errores, por_clase, por_red):
    puntos, obl, obj, pond = puntuar(inc, por_clase)
    total = sum(v[0] for v in por_clase.values())

    def de(clase):
        return [i["item"] for i in sorted((i for i in inc if i["clase"] == clase), key=lambda i: -i["exceso"])]

    tabla = f" + {info['tabla']} ({info['filas']} filas, {info['movidas']} aplicadas)" if info.get("tabla") else ""
    lineas = [
        f"evaluar: {info['pcb'].name}{tabla} · {len(modelo['huellas'])} huellas · {len(reglas)} reglas de {ruta_reglas}",
        f"PUNTOS {f(puntos, 0)} = {PESO_OBLIGATORIA}×{obl} obligatorias + {PESO_OBJETIVO}×{obj} objetivos"
        f" + {f(pond, 0)}/{DIVISOR_LONGITUD} de longitud ponderada (menor es mejor)",
    ]
    for clase, titulo in (("solape", "Solapes de patio"), ("fuera", "Fuera del contorno"), ("zona", "En zona prohibida")):
        items = de(clase)
        lineas.append(f"{titulo}: {len(items)}" + (" · " + _lista(items) if items else ""))
    lineas.append(f"Sin rutar {f(total, 0)} mm (longitud × peso): " + " · ".join(
        f"{c} {f(v[0], 0)}×{f(v[1], 1)}" for c, v in sorted(por_clase.items(), key=lambda kv: (-kv[1][0] * kv[1][1], -kv[1][0]))))
    nombres = alias_redes(sorted(por_red))
    lineas.append("Redes más largas (mm): " + _lista([f"{nombres[r]} {f(l, 0)}" for r, l in sorted(por_red.items(), key=lambda kv: -kv[1])], 8))
    fallos = [f"{r} de la tabla no está en la PCB" for r in info.get("faltan", [])] + errores
    if fallos:
        lineas.append("Errores: " + _lista(fallos, 6))
    por_regla = {}
    for i in inc:
        if i["clase"] == "regla":
            por_regla.setdefault((i["nivel"] != "obligatoria", i["regla"]), []).append(i)
    n_obl = sum(len(v) for (o, _), v in por_regla.items() if not o)
    lineas.append(f"Reglas incumplidas: {n_obl} obligatorias en {sum(1 for o, _ in por_regla if not o)} reglas (!) · "
                  f"{sum(len(v) for v in por_regla.values()) - n_obl} objetivos en {sum(1 for o, _ in por_regla if o)} reglas (~)")
    claves = sorted(por_regla, key=lambda k: k[0])  # obligatorias primero, en el orden de la tabla
    hueco = MAX_LINEAS - len(lineas)
    for k, clave in enumerate(claves):
        if k == hueco - 1 and len(claves) > hueco:
            ids = [("!" if not c[0] else "~") + c[1] for c in claves[k:]]
            lineas.append(f"… y {len(ids)} reglas más: {' '.join(ids[:24])}{' …' if len(ids) > 24 else ''} (--detalle ARCHIVO)")
            break
        items = sorted(por_regla[clave], key=lambda i: -i["exceso"])
        lineas.append(f"{'~' if clave[0] else '!'} {items[0]['cab']}: " + _lista([i["item"] for i in items], 6, 120))
    completo = [f"{i['nivel']}\t{i['clase']}\t{i['regla']}\t{i['cab']}\t{i['item']}" for i in inc]
    completo += [f"error\t{e}" for e in fallos]
    completo += [f"red\t{r}\t{clase_de(r, [])[0]}\t{f(l, 1)}" for r, l in sorted(por_red.items(), key=lambda kv: -kv[1])]
    return lineas, completo, (0 if not obl and not fallos else 1)


# ------------------------------------------------------------------ principal

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="orden", required=True)
    e = sub.add_parser("extraer", help="huellas en formato compacto")
    e.add_argument("pcb", help=".kicad_pcb o carpeta del proyecto")
    e.add_argument("-o", "--salida", help="archivo de texto con el listado")
    e.add_argument("--refs", help="solo estas referencias (separadas por comas o espacios), con sus pads")
    v = sub.add_parser("evaluar", help="puntúa una colocación")
    v.add_argument("pcb", help=".kicad_pcb o carpeta del proyecto")
    v.add_argument("tabla", nargs="?", help="CSV ref,x,y,giro,cara de colocar.py (sin ella, la PCB tal cual)")
    v.add_argument("--reglas", help="CSV de reglas (por defecto docs/diseno/colocacion-reglas.csv)")
    v.add_argument("--detalle", metavar="ARCHIVO", help="lista completa de incidencias y longitudes")
    args = ap.parse_args()

    if args.orden == "extraer":
        if not args.salida and not args.refs:
            raise Fallo("indica -o ARCHIVO (o --refs para ver unas pocas huellas en pantalla)")
        modelo, info = cargar(args.pcb)
        refs = None
        if args.refs:
            refs = {o[0] for o in expandir(args.refs.replace(",", " "))}
            faltan = sorted(refs - set(modelo["huellas"]), key=_clave_ref)
            if faltan:
                raise Fallo(f"no están en la PCB: {' '.join(faltan)}")
        texto = texto_extraer(modelo, info["pcb"].name, refs)
        if args.salida:
            Path(args.salida).parent.mkdir(parents=True, exist_ok=True)
            Path(args.salida).write_text(texto, encoding="utf-8", newline="\n")
            n = sum(1 for l in texto.splitlines() if l and not l.startswith("#"))
            emitir([f"{args.salida}: {len(refs) if refs else len(modelo['huellas'])} huellas en {n} líneas · "
                    f"{len(texto)} caracteres · ≈ {estimar_tokens(texto)} tokens (estimación)"])
        else:
            emitir(texto.rstrip("\n").splitlines())
        return 0

    ruta_reglas = Path(args.reglas) if args.reglas else (raiz_repo() or Path.cwd()) / "docs" / "diseno" / "colocacion-reglas.csv"
    if not ruta_reglas.is_file():
        raise Fallo(f"no existe la tabla de reglas {ruta_reglas} (--reglas)")
    reglas, clases = leer_reglas(ruta_reglas)
    modelo, info = cargar(args.pcb, args.tabla)
    info["tabla"] = Path(args.tabla).name if args.tabla else None
    inc, errores, por_clase, por_red = evaluar(modelo, reglas, clases)
    lineas, completo, codigo = informe(modelo, info, reglas, ruta_reglas.name, inc, errores, por_clase, por_red)
    if args.detalle:
        Path(args.detalle).write_text("\n".join(lineas + ["", "# detalle"] + completo) + "\n", encoding="utf-8")
    emitir(lineas)
    return codigo


if __name__ == "__main__":
    principal(main)
