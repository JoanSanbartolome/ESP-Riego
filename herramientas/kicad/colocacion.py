"""Colocación en texto: extrae las huellas de la PCB en formato compacto, puntúa una colocación y coloca las referencias.

Uso:
    python herramientas/kicad/colocacion.py extraer hardware/v2 -o huellas.txt [--refs U5,J4]
    python herramientas/kicad/colocacion.py evaluar hardware/v2 colocacion.csv [--placa 100x80] [--detalle informe.txt]
    python herramientas/kicad/colocacion.py referencias hardware/v2 colocacion.csv -o con_refs.csv [--todas]

extraer: por huella y bloque, ref, valor, x, y, giro, patio sin girar y redes de los pads (--refs: con pads).
evaluar: aplica la tabla de colocar.py (referencias rx,ry,rgiro,ralto,rtrazo y fila PLACA o --placa) a una
  copia de la PCB y da, en ≤ 30 líneas, placa y precio, solapes, contorno, zonas, serigrafía, térmico, reglas
  incumplidas y longitud sin rutar. PUNTOS = 1000 × obligatorias + 100 × objetivos + longitud / 10.
referencias: coloca las referencias junto a su patio, con vuelta atrás (--sin-vuelta: solo la pasada voraz).
Formato de la tabla y de las reglas, en herramientas/kicad/README.md.
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
         "libre", "opuesto", "sale", "clase", "separacion", "borde_min", "cobre_borde", "serigrafia", "calor",
         "reparto", "precio", "ras", "rieles", "lazo", "largo", "pasillo", "corte", "margen"}
NUMERICOS = {"borde", "fila", "zona", "cerca", "cerca_par", "lejos", "libre", "clase", "separacion", "borde_min",
             "cobre_borde", "serigrafia", "calor", "reparto", "precio", "ras", "rieles", "lazo", "largo", "pasillo",
             "corte", "margen"}
PASO_PISTA = 0.4  # mm: pista de 0,2 + separación de 0,2 (FAB-02), para la capacidad de los pasillos (`corte`)
RODEO = 0.5  # mm: una pista que rodea una pieza pasa a esta distancia de su patio (`corte`)
SERIGRAFIA = {"alto", "trazo", "proporcion", "alto_textos", "texto", "pad", "mascara", "contorno", "pieza", "silk",
              "junto", "ambigua", "visible"}
PESO_OBLIGATORIA, PESO_OBJETIVO, DIVISOR_LONGITUD = 1000, 100, 10
EPS_AREA = 0.01  # mm²: por debajo, dos patios solo se tocan
MARGEN_PATIO = 0.25  # mm: exceso de patio IPC-7351B nominal; el cuerpo para el borde es el patio menos esto


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
    Las piezas se separan con espacios; `*` son todas; `!REF` (o `!J4-J6`) excluye."""
    salida = []
    for trozo in str(texto or "").split():
        if trozo.startswith("!") or trozo == "*":
            continue
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


def excluidas(texto):
    """Referencias excluidas con `!` en una lista de piezas."""
    return {o[0] for t in str(texto or "").split() if t.startswith("!") for o in expandir(t[1:])}


def tam_placa(texto):
    m = re.fullmatch(r"\s*(\d+(?:[.,]\d+)?)\s*[x×X]\s*(\d+(?:[.,]\d+)?)\s*", str(texto or ""))
    if not m:
        return None
    return numero(m.group(1)), numero(m.group(2))


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
        if tipo in ("borde", "hacia", "ras") and r["objetivo"] not in LADOS:
            raise Fallo(f"{ruta}: regla {r['id']}: borde «{r['objetivo']}» ({', '.join(sorted(LADOS))})")
        if tipo == "hacia" and r["valor"] not in DIRECCIONES:
            raise Fallo(f"{ruta}: regla {r['id']}: dirección «{r['valor']}» ({', '.join(DIRECCIONES)})")
        if tipo == "serigrafia" and r["objetivo"] not in SERIGRAFIA:
            raise Fallo(f"{ruta}: regla {r['id']}: serigrafía «{r['objetivo']}» ({', '.join(sorted(SERIGRAFIA))})")
        if tipo == "serigrafia" and r["objetivo"] == "visible" and not r["valor"]:
            r["valor"] = "0"
        if tipo in NUMERICOS:
            try:
                r["mm"] = numero(r["valor"])
            except ValueError:
                raise Fallo(f"{ruta}: regla {r['id']}: valor «{r['valor']}» no es un número")
        if tipo == "lazo" and any(p is None for _, p, _ in expandir(r["piezas"])):
            raise Fallo(f"{ruta}: regla {r['id']}: un lazo es una lista de pads (REF.PAD), en orden")
        if tipo in ("calor", "reparto", "rieles", "corte"):
            try:
                r["aux"] = numero(r["objetivo"] or 0)
            except ValueError:
                raise Fallo(f"{ruta}: regla {r['id']}: objetivo «{r['objetivo']}» no es un número")
        if tipo == "precio":
            r["tam"] = tam_placa(r["piezas"])
            if not r["tam"]:
                raise Fallo(f"{ruta}: regla {r['id']}: piezas «{r['piezas']}» (precio: ANCHOxALTO máximo)")
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


def cifra(v, lim, minimo=True, dec=1):
    """v con los decimales justos para que se vea de qué lado del límite queda: si incumple (v < lim con
    minimo, v > lim sin él), la cifra que se muestra no puede ser igual al límite (300 → 299.6)."""
    cumple = v >= lim - 1e-6 if minimo else v <= lim + 1e-6
    for d in range(dec, 5):
        s = f(v, d)
        x = float(s)
        if cumple and (x >= lim - 1e-9 if minimo else x <= lim + 1e-9):
            return s
        if not cumple and (x < lim - 1e-9 if minimo else x > lim + 1e-9):
            return s
    return f(v, 6)


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


def anillo_caja(c):
    return [(c[0], c[1]), (c[2], c[1]), (c[2], c[3]), (c[0], c[3])]


def dist_cajas(a, b):
    """Distancia entre dos cajas alineadas con los ejes (0 si se tocan o se solapan)."""
    dx = max(a[0] - b[2], b[0] - a[2], 0)
    dy = max(a[1] - b[3], b[1] - a[3], 0)
    return math.hypot(dx, dy)


def area_comun(a, b):
    return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))


def a_caja_interior(c, caja_placa):
    """Margen de la caja c dentro de la caja de la placa (negativo si sale)."""
    return min(c[0] - caja_placa[0], c[1] - caja_placa[1], caja_placa[2] - c[2], caja_placa[3] - c[3])


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


class Rejilla:
    """Índice espacial de cajas (celdas de 5 mm)."""
    CELDA = 5.0

    def __init__(self):
        self.celdas, self.items = {}, {}

    def _celdas(self, c, m=0.0):
        k = self.CELDA
        for i in range(math.floor((c[0] - m) / k), math.floor((c[2] + m) / k) + 1):
            for j in range(math.floor((c[1] - m) / k), math.floor((c[3] + m) / k) + 1):
                yield i, j

    def poner(self, clave, caja, item):
        self.quitar(clave)
        self.items[clave] = (caja, item)
        for c in self._celdas(caja):
            self.celdas.setdefault(c, set()).add(clave)

    def quitar(self, clave):
        if clave in self.items:
            for c in self._celdas(self.items[clave][0]):
                self.celdas.get(c, set()).discard(clave)
            del self.items[clave]

    def cerca(self, caja, m):
        vistos = set()
        for c in self._celdas(caja, m):
            vistos |= self.celdas.get(c, set())
        for clave in sorted(vistos, key=str):  # orden fijo: los empates salen igual en cada ejecución
            cj, item = self.items[clave]
            if dist_cajas(cj, caja) <= m:
                yield clave, cj, item


# ------------------------------------------------------------------ modelo de la placa (pcbnew)

def _anillos(poly, pcbnew):
    salida = []
    for i in range(poly.OutlineCount()):
        o = poly.Outline(i)
        salida.append([(pcbnew.ToMM(o.CPoint(k).x), pcbnew.ToMM(o.CPoint(k).y)) for k in range(o.PointCount())])
    return salida


def _caja_bb(bb, pcbnew):
    return (pcbnew.ToMM(bb.GetLeft()), pcbnew.ToMM(bb.GetTop()), pcbnew.ToMM(bb.GetRight()), pcbnew.ToMM(bb.GetBottom()))


def caja_tinta(t, pcbnew):
    """Caja de la tinta de un texto de la PCB (trazos reales), en mm; None si no tiene."""
    poly = pcbnew.SHAPE_POLY_SET()
    t.TransformTextToPolySet(poly, 0, pcbnew.FromMM(0.01), pcbnew.ERROR_INSIDE)
    return _caja_bb(poly.BBox(), pcbnew) if poly.OutlineCount() else None


def cargar(pcb, tabla=None, placa=None, extra=None):
    """Carga la PCB en una copia temporal, cambia el contorno si hay placa (o fila PLACA en la tabla) y aplica la
    tabla con colocar.aplicar. `extra(board, pcbnew, modelo)` se llama con la placa abierta. Devuelve (modelo, info)."""
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
    filas, tam = colocar.leer_tabla(tabla, con_placa=True) if tabla else ([], None)
    if placa:
        tam = placa
    with tempfile.TemporaryDirectory(prefix="colocacion_") as tmp:
        copia = Path(tmp) / origen.name
        shutil.copyfile(origen, copia)
        board = pcbnew.LoadBoard(str(copia))
        taladros = colocar.contorno(board, *tam) if tam else []
        antes = {fp.GetReference(): (pcbnew.ToMM(fp.GetPosition().x), pcbnew.ToMM(fp.GetPosition().y),
                                     fp.GetOrientationDegrees(), fp.IsFlipped()) for fp in board.GetFootprints()}
        movidas, faltan, _ = colocar.aplicar(board, filas)
        modelo = modelo_de(board, pcbnew)
        if extra:
            extra(board, pcbnew, modelo)
    for ref, h in modelo["huellas"].items():
        h["antes"] = antes[ref]
    return modelo, {"pcb": origen, "filas": len(filas), "movidas": movidas, "faltan": faltan, "filas_tabla": filas,
                    "placa": tam, "taladros": taladros}


def _textos_de(fp, ref, pcbnew):
    salida = []
    for t in [fp.Reference()] + [c for c in fp.GetFields() if not c.IsReference()] + \
             [g for g in fp.GraphicalItems() if g.GetClass() == "PCB_TEXT"]:
        if t.GetLayer() not in (pcbnew.F_SilkS, pcbnew.B_SilkS):
            continue
        es_ref = t.GetClass() == "PCB_FIELD" and t.IsReference()
        if not t.IsVisible() and not es_ref:
            continue
        caja = caja_tinta(t, pcbnew) if t.IsVisible() else None
        salida.append({"dueño": ref, "tipo": "ref" if es_ref else "texto", "texto": t.GetShownText(False),
                       "caja": caja, "visible": bool(t.IsVisible() and caja), "alto": pcbnew.ToMM(t.GetTextHeight()),
                       "trazo": pcbnew.ToMM(t.GetTextThickness()), "giro": t.GetTextAngleDegrees(),
                       "nombre": ref if es_ref else f"{ref}:«{t.GetShownText(False)}»"})
    if not any(t["tipo"] == "ref" for t in salida):
        salida.append({"dueño": ref, "tipo": "ref", "texto": ref, "caja": None, "visible": False, "alto": 0, "trazo": 0,
                       "giro": 0, "nombre": ref})
    return salida


def modelo_de(board, pcbnew):
    contorno = pcbnew.SHAPE_POLY_SET()
    if not board.GetBoardPolygonOutlines(contorno, False) or not contorno.OutlineCount():
        raise Fallo("la PCB no tiene un contorno cerrado en Edge.Cuts")
    err = pcbnew.FromMM(0.02)
    huellas, redes, textos = {}, {}, []
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
        fab_capa, silk_capa, mask_capa, cu = ((pcbnew.B_Fab, pcbnew.B_SilkS, pcbnew.B_Mask, pcbnew.B_Cu) if b else
                                              (pcbnew.F_Fab, pcbnew.F_SilkS, pcbnew.F_Mask, pcbnew.F_Cu))
        fab = [g.GetBoundingBox() for g in fp.GraphicalItems() if g.GetLayer() == fab_capa and g.GetClass() == "PCB_SHAPE"]
        pos = (pcbnew.ToMM(fp.GetPosition().x), pcbnew.ToMM(fp.GetPosition().y))
        pads, mascara, silk = [], [], []
        for p in fp.Pads():
            num = p.GetNumber()
            if p.IsOnLayer(mask_capa):
                pm = pcbnew.SHAPE_POLY_SET()
                p.TransformShapeToPolygon(pm, mask_capa, max(0, p.GetSolderMaskExpansion(mask_capa)), err, pcbnew.ERROR_OUTSIDE)
                if pm.OutlineCount():
                    a = _anillos(pm, pcbnew)
                    mascara.append({"anillos": a, "caja": caja_de(a), "nombre": f"{ref}.{num or 'pasta'}"})
            if not num:
                continue  # ventanas de pasta
            red = p.GetNetname()
            pp = pcbnew.SHAPE_POLY_SET()
            p.TransformShapeToPolygon(pp, cu if p.IsOnLayer(cu) else (pcbnew.B_Cu if b else pcbnew.F_Cu), 0,
                                      err, pcbnew.ERROR_INSIDE)
            rel = p.GetFPRelativePosition()
            an = _anillos(pp, pcbnew)
            pads.append({"num": num, "red": red, "x": pcbnew.ToMM(p.GetPosition().x), "y": pcbnew.ToMM(p.GetPosition().y),
                         "lx": pcbnew.ToMM(rel.x), "ly": pcbnew.ToMM(rel.y), "anillos": an,
                         "caja": caja_de(an) if an else None, "cobre": p.IsOnLayer(cu) and bool(an)})
            if red and not red.startswith("unconnected-"):
                redes.setdefault(red, {}).setdefault((ref, num), (pads[-1]["x"], pads[-1]["y"]))
        for g in fp.GraphicalItems():
            if g.GetClass() != "PCB_SHAPE" or g.GetLayer() not in (silk_capa, mask_capa):
                continue
            pg = pcbnew.SHAPE_POLY_SET()
            g.TransformShapeToPolygon(pg, g.GetLayer(), 0, err, pcbnew.ERROR_INSIDE)
            if pg.OutlineCount():
                a = _anillos(pg, pcbnew)
                (silk if g.GetLayer() == silk_capa else mascara).append({"anillos": a, "caja": caja_de(a),
                                                                       "nombre": f"{ref} (serigrafía)" if g.GetLayer() == silk_capa else f"{ref} (máscara)"})
        h = {"ref": ref, "valor": fp.GetValue(), "bloque": fp.GetSheetname().strip("/").split("/")[-1] or "/",
             "x": pos[0], "y": pos[1], "giro": fp.GetOrientationDegrees(), "cara": "B" if b else "F",
             "fija": fp.IsLocked(), "patio_poly": patio, "patio": _anillos(patio, pcbnew), "pads": pads,
             "zonas_poly": zonas, "zonas": _anillos(zonas, pcbnew), "mascara": mascara, "silk": silk,
             "taladro": "MountingHole" in fp.GetFPIDAsString()}
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
        h["cuerpo"] = _anillos(h["cuerpo_poly"], pcbnew) or h["patio"]
        cp = caja_de(h["cuerpo"])
        dentro = (cp[0] + MARGEN_PATIO, cp[1] + MARGEN_PATIO, cp[2] - MARGEN_PATIO, cp[3] - MARGEN_PATIO)
        cajas_pads = [p["caja"] for p in pads if p["caja"]]
        h["caja_borde"] = tuple(m([dentro[k]] + [c[k] for c in cajas_pads]) for k, m in
                                ((0, min), (1, min), (2, max), (3, max)))
        # cuerpo visible (para la serigrafía): caja de Fab, o el patio menos su margen
        h["caja_cuerpo"] = (_caja_bb(fab[0], pcbnew) if len(fab) == 1 else
                            (min(pcbnew.ToMM(c.GetLeft()) for c in fab), min(pcbnew.ToMM(c.GetTop()) for c in fab),
                             max(pcbnew.ToMM(c.GetRight()) for c in fab), max(pcbnew.ToMM(c.GetBottom()) for c in fab))
                            ) if fab else dentro
        huellas[ref] = h
        textos += _textos_de(fp, ref, pcbnew)
    for d in board.GetDrawings():
        if d.GetClass() == "PCB_TEXT" and d.GetLayer() in (pcbnew.F_SilkS, pcbnew.B_SilkS) and d.IsVisible():
            caja = caja_tinta(d, pcbnew)
            if caja:
                textos.append({"dueño": None, "tipo": "texto", "texto": d.GetShownText(False), "caja": caja,
                               "visible": True, "alto": pcbnew.ToMM(d.GetTextHeight()),
                               "trazo": pcbnew.ToMM(d.GetTextThickness()), "giro": d.GetTextAngleDegrees(),
                               "nombre": f"placa:«{d.GetShownText(False)[:12]}»"})
    caja = caja_de(_anillos(contorno, pcbnew))
    return {"huellas": huellas, "redes": redes, "contorno_poly": contorno, "contorno": _anillos(contorno, pcbnew),
            "caja": caja, "textos": textos, "pcbnew": pcbnew}


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


# ------------------------------------------------------------------ serigrafía

def param_serigrafia(reglas):
    """Cifras de las reglas `serigrafia` (la más estricta de cada objetivo) y las que usa `referencias`."""
    p = {"alto": 1.0, "trazo": 0.15, "proporcion": 6.0, "texto": 0.15, "pad": 0.15, "contorno": 0.3, "junto": 1.0,
         "ambigua": 0.25}
    vistos = set()
    for r in reglas:
        if r["tipo"] == "serigrafia" and r["objetivo"] in p and r["objetivo"] != "alto_textos":
            k = r["objetivo"]
            mas_estricto = max if k in ("alto", "trazo", "texto", "pad", "contorno", "ambigua") else min
            p[k] = r["mm"] if k not in vistos else mas_estricto(p[k], r["mm"])
            vistos.add(k)
    p["trazo_ref"] = max(p["trazo"], p["alto"] / p["proporcion"])
    return p


class Indices:
    """Rejillas de lo que la serigrafía no puede pisar."""

    def __init__(self, modelo):
        H = modelo["huellas"]
        self.pads, self.mascara, self.cuerpo, self.silk, self.patio, self.textos = (Rejilla() for _ in range(6))
        for r, h in H.items():
            for i, p in enumerate(h["pads"]):
                if p["cobre"]:
                    self.pads.poner((r, i), p["caja"], (f"{r}.{p['num']}", p["anillos"]))
            for i, m in enumerate(h["mascara"]):
                self.mascara.poner((r, i), m["caja"], (m["nombre"], m["anillos"]))
            for i, s in enumerate(h["silk"]):
                self.silk.poner((r, i), s["caja"], (r, s["anillos"]))
            self.cuerpo.poner(r, h["caja_cuerpo"], r)
            self.patio.poner(r, caja_de(h["cuerpo"]), (r, h["cuerpo"]))
        for i, t in enumerate(modelo["textos"]):
            if t["visible"]:
                self.textos.poner(("t", i), t["caja"], t)


def medir_caja(modelo, idx, caja, dueño, yo=None):
    """Medidas de un texto con caja `caja` de la pieza `dueño` (yo = clave del propio texto en idx.textos)."""
    H = modelo["huellas"]
    rect = [anillo_caja(caja)]
    m = {"texto": (math.inf, None), "pad": (math.inf, None), "mascara": None, "pieza": None, "silk": None}
    for clave, cj, t in idx.textos.cerca(caja, 1.0):
        if clave != yo:
            d = round(dist_cajas(caja, cj), 3)
            if d < m["texto"][0]:
                m["texto"] = (d, t["nombre"])
    for _, cj, (nombre, an) in idx.pads.cerca(caja, 1.0):
        d = round(distancia(rect, an), 3)
        if d < m["pad"][0]:
            m["pad"] = (d, nombre)
    for _, cj, (nombre, an) in idx.mascara.cerca(caja, 0.0):
        if distancia(rect, an) == 0:
            m["mascara"] = nombre
            break
    for _, cj, r in idx.cuerpo.cerca(caja, 0.0):
        if area_comun(caja, cj) > EPS_AREA:
            m["pieza"] = r
            break
    for _, cj, (r, an) in idx.silk.cerca(caja, 0.0):
        if distancia(rect, an) == 0:
            m["silk"] = r
            break
    m["contorno"] = a_caja_interior(caja, modelo["caja"])
    propio = round(distancia(rect, H[dueño]["cuerpo"]), 3) if dueño in H else math.inf
    m["junto"] = propio
    otro = (math.inf, None)
    for _, cj, (r, an) in idx.patio.cerca(caja, min(propio, 5.0) + 1.0):
        if r != dueño:
            d = round(distancia(rect, an), 3)
            if d < otro[0]:
                otro = (d, r)
    m["ambigua"] = otro
    return m


def fallos_caja(m, p):
    """Lista de fallos de un texto según las cifras p (param_serigrafia)."""
    salida = []
    if m["texto"][0] < p["texto"] - 1e-6:
        salida.append("texto")
    if m["pad"][0] < p["pad"] - 1e-6:
        salida.append("pad")
    for k in ("mascara", "pieza", "silk"):
        if m[k]:
            salida.append(k)
    if m["contorno"] < p["contorno"] - 1e-6:
        salida.append("contorno")
    if m["junto"] > p["junto"] + 1e-6:
        salida.append("junto")
    if m["ambigua"][0] < m["junto"] + p["ambigua"] - 1e-6:
        salida.append("ambigua")
    return salida


def medir_textos(modelo):
    """{ref: medidas de su referencia} y el índice. Las referencias ocultas no tienen medidas."""
    idx = Indices(modelo)
    medidas = {}
    for i, t in enumerate(modelo["textos"]):
        if t["tipo"] == "ref" and t["visible"]:
            medidas[t["dueño"]] = medir_caja(modelo, idx, t["caja"], t["dueño"], ("t", i))
    return medidas, idx


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
    fuera = excluidas(texto)
    if "*" in texto.split():
        return [Operando(modelo, r, None, None) for r in sorted(modelo["huellas"], key=_clave_ref) if r not in fuera]
    for ref, pad, suf in expandir(texto):
        if ref in fuera:
            continue
        try:
            salida.append(Operando(modelo, ref, pad, suf))
        except KeyError as e:
            errores.append(f"{regla['id']}: {e.args[0]} no existe en la PCB")
    return salida


def _area(poly):
    return poly.Area() / 1e12


def caja_fisica(h):
    """Caja del cuerpo visible (F.Fab) unida a la de los pads: lo que de verdad no puede salir de la placa."""
    cajas = [h["caja_cuerpo"]] + [p["caja"] for p in h["pads"] if p["caja"]]
    return (min(c[0] for c in cajas), min(c[1] for c in cajas), max(c[2] for c in cajas), max(c[3] for c in cajas))


def centro_pad(o):
    """Centro de un operando de pad (media de los centros de los pads con ese número, p. ej. un EP con vías)."""
    cs = [((min(p[0] for p in a) + max(p[0] for p in a)) / 2, (min(p[1] for p in a) + max(p[1] for p in a)) / 2)
          for a in o.anillos]
    return sum(c[0] for c in cs) / len(cs), sum(c[1] for c in cs) / len(cs)


def aristas_minimas(puntos):
    """Aristas (i, j) del árbol de expansión mínimo (Prim) entre puntos (x, y)."""
    if len(puntos) < 2:
        return []
    dist, padre = [math.inf] * len(puntos), [0] * len(puntos)
    dentro, actual, salida = [False] * len(puntos), 0, []
    dentro[0] = True
    for _ in range(len(puntos) - 1):
        px, py = puntos[actual]
        mejor, k = math.inf, -1
        for i, (x, y) in enumerate(puntos):
            if dentro[i]:
                continue
            d = math.hypot(x - px, y - py)
            if d < dist[i]:
                dist[i], padre[i] = d, actual
            if dist[i] < mejor:
                mejor, k = dist[i], i
        dentro[k], actual = True, k
        salida.append((padre[k], k))
    return salida


def huecos_pista(libres):
    """Pistas de 0,2 mm con 0,2 de separación que caben en una lista de tramos libres (mm)."""
    return sum(int((L + 0.2 + 1e-9) / PASO_PISTA) for L in libres if L > 0)


def medir_cortes(modelo, refs, clases, tramo):
    """Capacidad de los pasillos: líneas de corte cada 1 mm en x y en y, en tramos de `tramo` mm (paso la mitad).
    Demanda de un tramo = suma de los pesos de clase de las aristas del árbol mínimo de cada red (sin GND) que lo
    cruzan; oferta = pistas que caben en lo que el tramo no pisa de patios (sin zonas) ni zonas prohibidas, en la cara
    superior. Una arista que cruza el corte por dentro de otra pieza cuenta en el borde más cercano de esa pieza (la
    pista la rodea). Devuelve [(eje, c, s0, s1, demanda, oferta, redes)] de los tramos con demanda."""
    H = modelo["huellas"]
    X0, Y0, X1, Y1 = modelo["caja"]
    obst = [(caja_de(H[r]["cuerpo"]), r) for r in refs]
    obst += [(caja_de([a]), h["ref"]) for h in H.values() for a in h["zonas"]]
    aristas = []
    for red, nodos in modelo["redes"].items():
        if len(nodos) < 2:
            continue
        _, peso = clase_de(red, clases)
        if peso <= 0:
            continue
        claves = list(nodos)
        pts = [nodos[k] for k in claves]
        aristas += [(pts[i], pts[j], peso, red, {claves[i][0], claves[j][0]}) for i, j in aristas_minimas(pts)]
    salida = []
    for eje in ("x", "y"):
        a, b = (0, 1) if eje == "x" else (1, 0)  # a: coordenada del corte; b: a lo largo del corte
        lo, hi = (X0, X1) if eje == "x" else (Y0, Y1)
        lo_b, hi_b = (Y0, Y1) if eje == "x" else (X0, X1)
        c = math.floor(lo) + 1.0
        while c < hi - 0.5:
            tapan = sorted((o[b], o[b + 2], r) for o, r in obst if o[a] < c < o[a + 2])
            grupos = []  # lo que tapa, con los huecos de menos de 2 × RODEO cerrados (una pista larga no los enhebra)
            for t0, t1, _r in tapan:
                if grupos and t0 - grupos[-1][1] < 2 * RODEO:
                    grupos[-1][1] = max(grupos[-1][1], t1)
                else:
                    grupos.append([t0, t1])
            cruces = []
            for p, q, peso, red, suyas in aristas:
                if (p[a] - c) * (q[a] - c) < 0:
                    u = (c - p[a]) / (q[a] - p[a])
                    s = p[b] + u * (q[b] - p[b])
                    # la salida de una pista por el patio de su propia pieza no gasta pasillo
                    if any(t0 <= s <= t1 and r in suyas for t0, t1, r in tapan):
                        continue
                    # la pista que cruza otra pieza la rodea: el cruce pasa al borde más cercano de lo que tapa
                    for _ in range(8):
                        tapa = next(((t0, t1) for t0, t1 in grupos if t0 < s < t1), None)
                        if not tapa:
                            break
                        bordes = [x for x in (tapa[0] - RODEO, tapa[1] + RODEO) if lo_b < x < hi_b]
                        if not bordes:
                            break
                        s = min(bordes, key=lambda x: abs(x - s))
                    cruces.append((s, peso, red))
            s0 = lo_b
            while s0 < hi_b - 1e-6:
                s1 = min(s0 + tramo, hi_b)
                dentro = [x for x in cruces if s0 <= x[0] < s1]
                if dentro:
                    # oferta: lo libre del tramo, alargado RODEO × 2 por cada lado (un hueco que el borde del
                    # tramo corta por la mitad sigue sirviendo a las pistas que lo cruzan)
                    e0, e1 = max(lo_b, s0 - 2 * RODEO), min(hi_b, s1 + 2 * RODEO)
                    libres, pos = [], e0
                    for t0, t1, _ in tapan:
                        if t1 <= e0 or t0 >= e1:
                            continue
                        if t0 > pos:
                            libres.append(t0 - pos)
                        pos = max(pos, t1)
                    if pos < e1:
                        libres.append(e1 - pos)
                    salida.append((eje, c, s0, s1, sum(x[1] for x in dentro), huecos_pista(libres),
                                   sorted({x[2] for x in dentro})))
                if s1 >= hi_b:
                    break
                s0 += tramo / 2
            c += 1.0
    return salida


def medir_calor(modelo, reglas, errores):
    """Fuentes de calor de las reglas `calor`: P (W), cobre necesario A (mm²) y cobre libre medido (mm²): zona a
    √A/2 del patio, dentro de la placa, sin patios ni zonas prohibidas, y la parte que comparte con otra fuente,
    a medias."""
    pcbnew = modelo["pcbnew"]
    H = modelo["huellas"]
    fuentes = []
    for r in reglas:
        if r["tipo"] == "calor":
            for o in _operandos(modelo, r["piezas"], errores, r):
                fuentes.append({"ref": o.h["ref"], "P": r["mm"], "A": r["aux"], "regla": r, "libre": None})
    if not fuentes:
        return fuentes
    ocupado = pcbnew.SHAPE_POLY_SET()
    for h in H.values():
        ocupado.BooleanAdd(h["cuerpo_poly"])
        if h["zonas_poly"].OutlineCount():
            ocupado.BooleanAdd(h["zonas_poly"])
    con_area = [f_ for f_ in fuentes if f_["A"] > 0]
    for f_ in con_area:
        yo = H[f_["ref"]]
        reg = pcbnew.SHAPE_POLY_SET(yo["cuerpo_poly"])
        reg.Inflate(pcbnew.FromMM(math.sqrt(f_["A"]) / 2), pcbnew.CORNER_STRATEGY_ROUND_ALL_CORNERS, pcbnew.FromMM(0.05))
        anillo = pcbnew.SHAPE_POLY_SET(reg)
        anillo.BooleanSubtract(yo["cuerpo_poly"])
        bruto = _area(anillo)
        reg.BooleanIntersection(modelo["contorno_poly"])
        anillo.BooleanIntersection(modelo["contorno_poly"])
        # qué ocupa el anillo (para --detalle): fuera de la placa, patios y zonas prohibidas de otras piezas
        ocupan = [("borde", bruto - _area(anillo))]
        cr = _caja_bb(anillo.BBox(), pcbnew) if anillo.OutlineCount() else None
        for r2, h2 in H.items():
            if r2 == f_["ref"] or cr is None:
                continue
            for poly in (h2["cuerpo_poly"], h2["zonas_poly"]):
                if not poly.OutlineCount() or dist_cajas(_caja_bb(poly.BBox(), pcbnew), cr) > 0:
                    continue
                s = pcbnew.SHAPE_POLY_SET(anillo)
                s.BooleanIntersection(poly)
                a = _area(s)
                if a > 0.5:
                    ocupan.append((r2 if poly is h2["cuerpo_poly"] else f"{r2}/zona", a))
        reg.BooleanSubtract(ocupado)
        f_["region"] = reg
        f_["libre"] = _area(reg)
        f_["anillo"] = bruto
        f_["ocupan"] = ocupan
    for i, a in enumerate(con_area):
        for b in con_area[i + 1:]:
            s = pcbnew.SHAPE_POLY_SET(a["region"])
            s.BooleanIntersection(b["region"])
            comun = _area(s)
            a["libre"] -= comun / 2
            b["libre"] -= comun / 2
            if comun > 0.5:
                a["ocupan"].append((f"½ {b['ref']}", comun / 2))
                b["ocupan"].append((f"½ {a['ref']}", comun / 2))
    return fuentes


def medir_precio(modelo, reglas):
    """(ancho, alto, regla que casa o None, precio base, regla base)."""
    X0, Y0, X1, Y1 = modelo["caja"]
    w, h = X1 - X0, Y1 - Y0
    filas = [r for r in reglas if r["tipo"] == "precio"]
    casa = next((r for r in filas if (w <= r["tam"][0] + 1e-6 and h <= r["tam"][1] + 1e-6)
                 or (w <= r["tam"][1] + 1e-6 and h <= r["tam"][0] + 1e-6)), None)
    return w, h, casa, (filas[0] if filas else None)


def evaluar(modelo, reglas, clases):
    """(incidencias, errores, {clase: [longitud, peso]}, {red: longitud}). Cada incidencia: clase (solape, fuera,
    zona, regla), nivel, regla (id), cab (la regla en pocas palabras), item (la pieza y la cifra) y exceso."""
    pcbnew = modelo["pcbnew"]
    H, caja = modelo["huellas"], modelo["caja"]
    inc, errores = [], []

    def anota(clase, nivel, item, regla="", exceso=0.0, cab="", grupo=""):
        inc.append({"clase": clase, "nivel": nivel, "item": item, "regla": regla, "exceso": exceso, "cab": cab,
                    "grupo": grupo})

    salen, al_ras = set(), set()
    for r in reglas:
        if r["tipo"] == "sale":
            salen |= {o[0] for o in expandir(r["piezas"])}
        if r["tipo"] == "ras":
            al_ras |= {o[0] for o in expandir(r["piezas"])}

    refs = sorted(H, key=_clave_ref)
    cajas = {r: caja_de(H[r]["patio"]) for r in refs}
    ccuerpo = {r: caja_de(H[r]["cuerpo"]) for r in refs}
    solapes = set()
    # solapes de patio (misma cara; el patio de una pieza con zona prohibida se mide sin la zona)
    for i, a in enumerate(refs):
        for b in refs[i + 1:]:
            if H[a]["cara"] != H[b]["cara"]:
                continue
            ca, cb = ccuerpo[a], ccuerpo[b]
            if ca[2] <= cb[0] or cb[2] <= ca[0] or ca[3] <= cb[1] or cb[3] <= ca[1]:
                continue
            s = pcbnew.SHAPE_POLY_SET(H[a]["cuerpo_poly"])
            s.BooleanIntersection(H[b]["cuerpo_poly"])
            if _area(s) > EPS_AREA:
                anota("solape", "obligatoria", f"{a}/{b} {f(_area(s), 1)} mm²", exceso=_area(s))
                solapes.add((a, b))
    # fuera del contorno
    X0, Y0, X1, Y1 = caja
    for r in refs:
        h = H[r]
        if r in al_ras:  # al ras del borde: cuenta el cuerpo (F.Fab) con los pads, no el exceso del patio
            m = a_caja_interior(caja_fisica(h), caja)
            if m < -0.01:
                anota("fuera", "obligatoria", f"{r} {f(-m, 2)} mm (cuerpo)", exceso=-m)
            continue
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

    medidas = idx = None
    modelo["calor"] = medir_calor(modelo, reglas, errores)
    for r in reglas:
        t, nivel, rid, lim = r["tipo"], r["nivel"], r["id"], r.get("mm")
        if t in ("sale", "calor", "precio", "margen", "rieles"):
            continue
        piezas = _operandos(modelo, r["piezas"], errores, r) if t not in ("reparto", "largo") else []
        destino = (_operandos(modelo, r["objetivo"], errores, r)
                   if t in ("cerca", "cerca_par", "lejos", "entre", "opuesto") or (t == "separacion" and r["objetivo"])
                   else [])

        def mal(item, exceso=0.0, cab=None, grupo=""):
            anota("regla", nivel, item, rid, exceso, cab or f"{rid} {t} {r['piezas']}", grupo)

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
                    mal(f"{o.nombre} {cifra(d, lim, False)}" + (f" ({lado})" if lado != r["objetivo"] else ""), d - lim, cab)
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
                    mal(f"{o.nombre} {cifra(d, lim, False)}", d - lim, cab)
                if t == "lejos" and d < lim - 1e-6:
                    mal(f"{o.nombre} {cifra(d, lim, True)}", lim - d, cab)
        elif t == "cerca_par":
            if len(piezas) != len(destino):
                errores.append(f"{rid}: {len(piezas)} piezas y {len(destino)} objetivos (cerca_par los empareja)")
            cab = f"{rid} {r['piezas']} ≤ {f(lim)} de {r['objetivo']} (por pares)"
            for o, d in zip(piezas, destino):
                dd = distancia(o.anillos, d.anillos)
                if dd > lim + 1e-6:
                    mal(f"{o.nombre}–{d.nombre} {cifra(dd, lim, False)}", dd - lim, cab)
        elif t == "libre":
            cab = f"{rid} Ø {f(2 * lim)} libre en {r['piezas']}"
            for o in piezas:
                c = (o.h["x"], o.h["y"])
                for otro in refs:
                    if otro != o.h["ref"]:
                        d = distancia([[c]], H[otro]["patio"])
                        if d < lim - 1e-6:
                            mal(f"{otro} a {cifra(d, lim, True)} de {o.nombre}", lim - d, cab)
        elif t == "opuesto":
            medio = (caja[0] + caja[2]) / 2
            for o in piezas:
                for d in destino:
                    ca, cb = caja_de(o.anillos), caja_de(d.anillos)
                    if ((ca[0] + ca[2]) / 2 - medio) * ((cb[0] + cb[2]) / 2 - medio) > 0:
                        mal(f"{o.nombre} y {d.nombre} en la misma mitad", cab=f"{rid} {r['piezas']} en el lateral opuesto a {r['objetivo']}")
        elif t == "separacion":
            cab = f"{rid} patio a patio ≥ {f(lim)}"
            a_set = [o.h["ref"] for o in piezas]
            b_set = {o.h["ref"] for o in destino} if destino else set(a_set)
            vistos = set()
            for a in a_set:
                for b in b_set:
                    par = tuple(sorted((a, b), key=_clave_ref))
                    if a == b or par in vistos or H[a]["cara"] != H[b]["cara"]:
                        continue
                    vistos.add(par)
                    if dist_cajas(ccuerpo[a], ccuerpo[b]) >= lim or par in solapes:
                        continue
                    d = distancia(H[a]["cuerpo"], H[b]["cuerpo"])
                    if d < lim - 1e-6:
                        mal(f"{par[0]}/{par[1]} {cifra(d, lim, True, 2)}", lim - d, cab)
        elif t == "borde_min":
            cab = f"{rid} cuerpo a borde ≥ {f(lim)}"
            for o in piezas:
                d = a_caja_interior(o.h["caja_borde"], caja)
                if d < lim - 1e-6:
                    mal(f"{o.nombre} {cifra(d, lim, True, 2 if abs(d) < 1 else 1)}", lim - d, cab)
        elif t == "cobre_borde":
            cab = f"{rid} pad a borde ≥ {f(lim)}"
            for o in piezas:
                cp = [p for p in o.h["pads"] if p["caja"]]
                if cp:
                    p = min(cp, key=lambda p: a_caja_interior(p["caja"], caja))
                    d = a_caja_interior(p["caja"], caja)
                    if d < lim - 1e-6:
                        mal(f"{o.nombre}.{p['num']} {cifra(d, lim, True, 2 if abs(d) < 1 else 1)}", lim - d, cab)
        elif t == "reparto":
            cab = f"{rid} fuentes de ≥ {f(r['aux'])} W a ≥ {f(lim)} (patio)"
            fu = [x for x in modelo["calor"] if x["P"] >= r["aux"] - 1e-9]
            for i, a in enumerate(fu):
                for b in fu[i + 1:]:
                    if a["ref"] == b["ref"]:
                        continue
                    d = distancia(H[a["ref"]]["cuerpo"], H[b["ref"]]["cuerpo"])
                    if d < lim - 1e-6:
                        mal(f"{a['ref']}/{b['ref']} {cifra(d, lim, True)}", lim - d, cab)
        elif t == "ras":
            cab = f"{rid} al ras del borde {r['objetivo']} (0…{f(lim)}, sin salir)"
            for o in piezas:
                an = o.anillos if (o.nombre.count("/") or o.nombre.count(".")) else [anillo_caja(o.h["caja_cuerpo"])]
                d, lado = a_borde(an, caja, r["objetivo"])
                if d < -1e-6:
                    mal(f"{o.nombre} sale {cifra(-d, 0, False, 2)} ({lado})", -d, cab)
                elif d > lim + 1e-6:
                    mal(f"{o.nombre} {cifra(d, lim, False, 2)} ({lado})", d - lim, cab)
        elif t == "lazo":
            cab = f"{rid} lazo {r['piezas']} ≤ {f(lim)} (centro a centro)"
            if len(piezas) >= 2:
                cs = [centro_pad(o) for o in piezas]
                tramos = [(math.hypot(cs[i][0] - cs[i - 1][0], cs[i][1] - cs[i - 1][1]), piezas[i - 1].nombre,
                           piezas[i].nombre) for i in range(len(cs))]
                largo = sum(t_[0] for t_ in tramos)
                if largo > lim + 1e-6:
                    peor = max(tramos)
                    mal(f"{cifra(largo, lim, False)} (tramo más largo {peor[1]}→{peor[2]} {f(peor[0], 1)})", largo - lim, cab)
        elif t == "largo":
            patrones = r["piezas"].split()
            cab = f"{rid} {'+'.join(patrones)} sin rutar ≤ {f(lim)}"
            total, vistas = 0.0, []
            for red, nodos in sorted(modelo["redes"].items()):
                nombres = {red, red.lstrip("/"), red.rstrip("/").split("/")[-1]}
                if any(fnmatch.fnmatchcase(n, p) for p in patrones for n in nombres):
                    total += arbol_minimo(list(nodos.values()))
                    vistas.append(red)
            if not vistas:
                errores.append(f"{rid}: ninguna red casa con «{r['piezas']}»")
            elif total > lim + 1e-6:
                mal(f"{'+'.join(alias_redes(vistas).values())} {cifra(total, lim, False)}", total - lim, cab)
        elif t == "pasillo":
            cab = f"{rid} patio a patio entre bloques ≥ {f(lim)}"
            refs_p = [o.h["ref"] for o in piezas]
            for i, a in enumerate(refs_p):
                for b in refs_p[i + 1:]:
                    if H[a]["bloque"] == H[b]["bloque"] or H[a]["cara"] != H[b]["cara"]:
                        continue
                    if dist_cajas(ccuerpo[a], ccuerpo[b]) >= lim:
                        continue
                    d = distancia(H[a]["cuerpo"], H[b]["cuerpo"])
                    if d < lim - 1e-6:
                        par = sorted((a, b), key=_clave_ref)
                        mal(f"{par[0]}/{par[1]} {cifra(d, lim, True, 2)}", lim - d, cab)
        elif t == "corte":
            cab = f"{rid} pasillos: pistas que caben ≥ {f(lim)} × las que cruzan, en tramos de {f(r['aux'])} mm"
            refs_c = [o.h["ref"] for o in piezas]
            malos = sorted((x for x in medir_cortes(modelo, refs_c, clases, r["aux"]) if x[5] < lim * x[4] - 1e-6),
                           key=lambda x: (-(lim * x[4] - x[5]), x[0], x[1], x[2]))
            focos = []
            for x in malos:
                if any(x[0] == y[0] and abs(x[1] - y[1]) < r["aux"] and abs(x[2] - y[2]) < r["aux"] for y in focos):
                    continue
                focos.append(x)
            nombres = alias_redes(sorted(modelo["redes"]))
            for eje, c, s0, s1, dem, of, redes in focos:
                otro = "y" if eje == "x" else "x"
                mal(f"{eje} {f(c)} {otro} {f(s0)}…{f(s1)}: {f(dem)} pistas, caben {of} "
                    f"({' '.join(nombres.get(n, n) for n in redes[:4])}{' …' if len(redes) > 4 else ''})", lim * dem - of, cab)
        elif t == "serigrafia":
            k = r["objetivo"]
            if medidas is None:
                medidas, idx = medir_textos(modelo)
            p = param_serigrafia([r])
            refs_regla = {o.h["ref"] for o in piezas}
            cabs = {"alto": f"{rid} referencia alto ≥ {f(lim)}", "trazo": f"{rid} referencia trazo ≥ {f(lim)}",
                    "proporcion": f"{rid} alto/trazo ≤ {f(lim)}", "alto_textos": f"{rid} textos de huella alto ≥ {f(lim)}",
                    "texto": f"{rid} texto a texto ≥ {f(lim)}", "pad": f"{rid} texto a pad ≥ {f(lim)}",
                    "mascara": f"{rid} texto sobre máscara abierta", "contorno": f"{rid} texto a borde ≥ {f(lim)}",
                    "pieza": f"{rid} texto bajo una pieza", "silk": f"{rid} texto sobre serigrafía",
                    "junto": f"{rid} referencia a ≤ {f(lim)} de su patio",
                    "ambigua": f"{rid} otra pieza a < {f(lim)} más cerca que la propia",
                    "visible": f"{rid} referencia visible en serigrafía"}
            cab = cabs[k]
            for tx in modelo["textos"]:
                if tx["dueño"] not in refs_regla:
                    continue
                if k == "alto_textos":
                    if tx["tipo"] == "texto" and tx["visible"] and tx["alto"] < lim - 1e-6:
                        mal(f"{tx['nombre']} {f(tx['alto'])}", lim - tx["alto"], cab, k)
                    continue
                if tx["tipo"] != "ref":
                    continue
                if k == "visible":
                    if not tx["visible"]:
                        mal(f"{tx['dueño']} oculta", 1.0, cab, k)
                    continue
                if not tx["visible"]:
                    continue
                m = medidas[tx["dueño"]]
                if k == "alto" and tx["alto"] < lim - 1e-6:
                    mal(f"{tx['dueño']} {f(tx['alto'])}", lim - tx["alto"], cab, k)
                elif k == "trazo" and tx["trazo"] < lim - 1e-6:
                    mal(f"{tx['dueño']} {f(tx['trazo'], 3)}", lim - tx["trazo"], cab, k)
                elif k == "proporcion" and tx["trazo"] > 0 and tx["alto"] / tx["trazo"] > lim + 1e-6:
                    mal(f"{tx['dueño']} {f(tx['alto'] / tx['trazo'], 1)}", tx["alto"] / tx["trazo"] - lim, cab, k)
                elif k == "texto" and m["texto"][0] < p["texto"] - 1e-6:
                    otro = m["texto"][1]
                    if not (otro in refs_regla and _clave_ref(otro) < _clave_ref(tx["dueño"]) and otro in medidas
                            and medidas[otro]["texto"][1] == tx["dueño"]):
                        mal(f"{tx['dueño']}/{otro} {f(m['texto'][0], 2)}", p["texto"] - m["texto"][0], cab, k)
                elif k == "pad" and m["pad"][0] < p["pad"] - 1e-6:
                    mal(f"{tx['dueño']} {f(m['pad'][0], 2)} de {m['pad'][1]}", p["pad"] - m["pad"][0], cab, k)
                elif k in ("mascara", "pieza", "silk") and m[k]:
                    mal(f"{tx['dueño']} sobre {m[k]}", 1.0, cab, k)
                elif k == "contorno" and m["contorno"] < p["contorno"] - 1e-6:
                    mal(f"{tx['dueño']} {f(m['contorno'], 2)}", p["contorno"] - m["contorno"], cab, k)
                elif k == "junto" and m["junto"] > p["junto"] + 1e-6:
                    mal(f"{tx['dueño']} {f(m['junto'], 1)}", m["junto"] - p["junto"], cab, k)
                elif k == "ambigua" and m["ambigua"][0] < m["junto"] + p["ambigua"] - 1e-6:
                    mal(f"{tx['dueño']} {f(m['junto'], 2)} ({m['ambigua'][1]} {f(m['ambigua'][0], 2)})",
                        m["junto"] + p["ambigua"] - m["ambigua"][0], cab, k)

    # térmico: cobre libre de cada fuente
    for x in modelo["calor"]:
        if x["libre"] is not None and x["libre"] < x["A"] - 1e-6:
            r = x["regla"]
            anota("regla", r["nivel"], f"{x['ref']} {cifra(x['libre'], x['A'], True, 0)}/{f(x['A'], 0)}", r["id"],
                  x["A"] - x["libre"], f"{r['id']} cobre libre a √A/2 (mm², libre/necesario)", "calor")
    # margen del cobre: libre ≥ factor × necesario (las pistas y las vías se comen parte del cobre libre)
    for r in reglas:
        if r["tipo"] != "margen":
            continue
        quien = {o.h["ref"] for o in _operandos(modelo, r["piezas"], errores, r)}
        for x in modelo["calor"]:
            if x["ref"] in quien and x["libre"] is not None and x["A"] > 0:
                pide = x["A"] * r["mm"]
                if x["libre"] < pide - 1e-6:
                    anota("regla", r["nivel"], f"{x['ref']} {cifra(x['libre'], pide, True, 0)}/{f(pide, 0)}", r["id"],
                          pide - x["libre"], f"{r['id']} cobre libre ≥ {f(r['mm'])} × necesario (mm²)", "calor")
    # zona prohibida dentro de la placa (lo que la antena quita de placa)
    zonas_dentro = {}
    for z in refs:
        if H[z]["zonas_poly"].OutlineCount():
            s = pcbnew.SHAPE_POLY_SET(H[z]["zonas_poly"])
            s.BooleanIntersection(modelo["contorno_poly"])
            zonas_dentro[z] = _area(s)
    modelo["zonas_dentro"] = zonas_dentro
    # bordes auxiliares (edge rails) de JLCPCB por piezas a menos de la distancia de montaje del borde
    modelo["rieles"] = None
    for r in reglas:
        if r["tipo"] != "rieles":
            continue
        lados = {}
        for o in _operandos(modelo, r["piezas"], errores, r):
            c = caja_fisica(o.h)
            if c[2] < X0 or c[0] > X1 or c[3] < Y0 or c[1] > Y1:
                continue  # fuera de la placa: no cuenta para los rieles
            for lado, d in (("izq", c[0] - X0), ("sup", c[1] - Y0), ("der", X1 - c[2]), ("inf", Y1 - c[3])):
                if d < r["aux"] - 1e-6:
                    lados.setdefault(lado, []).append(f"{o.h['ref']} {f(max(d, 0), 1)}")
        if not lados:
            continue
        ancho = (X1 - X0) + (2 * r["mm"] if {"izq", "der"} & set(lados) else 0)
        alto = (Y1 - Y0) + (2 * r["mm"] if {"sup", "inf"} & set(lados) else 0)
        w0, h0, casa0, base = medir_precio({"caja": (0, 0, X1 - X0, Y1 - Y0)}, reglas)
        _, _, casa, _ = medir_precio({"caja": (0, 0, ancho, alto)}, reglas)
        quien = " · ".join(f"{lado}: {', '.join(v)}" for lado, v in sorted(lados.items()))
        if casa:
            coste = f"{f(casa['mm'])} $ ({casa['id']})" + (f", +{f(casa['mm'] - casa0['mm'])} $" if casa0 and casa is not casa0 else "")
        else:
            coste = f"sin tarifa publicada por encima de {base['piezas']} ({base['id']}): presupuesto" if base else "sin tarifa"
        modelo["rieles"] = (ancho, alto, quien, coste, r)
        if not casa0 or casa is not casa0:
            anota("regla", r["nivel"], f"panel {f(ancho, 1)}×{f(alto, 1)} con rieles de {f(r['mm'])} mm ({quien}): {coste}",
                  r["id"], max(ancho, alto) - max(w0, h0), f"{r['id']} rieles de JLCPCB por piezas a < {f(r['aux'])} mm del borde")
    # precio de la PCB
    w, hh, casa, base = medir_precio(modelo, reglas)
    modelo["precio"] = (w, hh, casa, base)
    if base and casa is not base:
        r = base
        if casa:
            item = (f"placa {f(w, 1)}×{f(hh, 1)} > {r['piezas']}: {f(casa['mm'])} $ ({casa['objetivo']} uds), "
                    f"+{f(casa['mm'] - r['mm'])} $ ({casa['id']}); OK del usuario (DEC-0016)")
        else:
            item = (f"placa {f(w, 1)}×{f(hh, 1)} > {r['piezas']}: fuera del precio especial, sobrecoste sin tarifa "
                    f"en la tabla (presupuesto en JLCPCB y OK del usuario, DEC-0016)")
        anota("regla", r["nivel"], item, r["id"], max(w, hh) - max(r["tam"]), f"{r['id']} precio de la PCB", "precio")

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


NOMBRES_SERIGRAFIA = {"alto": "alto", "trazo": "trazo", "proporcion": "proporción", "alto_textos": "alto de huella",
                      "texto": "texto-texto", "pad": "sobre pad", "mascara": "máscara", "contorno": "borde",
                      "pieza": "bajo pieza", "silk": "sobre serigrafía", "junto": "lejos de su pieza",
                      "ambigua": "ambiguas", "visible": "ocultas"}


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
    w, hh, casa, base = modelo.get("precio", (0, 0, None, None))
    placa = f"Placa {f(w, 1)}×{f(hh, 1)} mm" + (f" (taladros movidos: {' '.join(info['taladros'])})" if info.get("taladros") else "")
    if casa:
        placa += f" · PCB {f(casa['mm'])} $ por {casa['objetivo']} uds (≤ {casa['piezas']}, {casa['id']})"
        if base and casa is not base:
            placa += f" · AVISO: +{f(casa['mm'] - base['mm'])} $ sobre ≤ {base['piezas']}, consultar al usuario"
    elif base:
        placa += f" · AVISO: > {base['piezas']}, sobrecoste de JLCPCB sin tarifa publicada ({base['id']}): presupuesto y OK del usuario"
    rieles = modelo.get("rieles")
    if rieles:
        placa += f" · rieles ({rieles[2]}): panel {f(rieles[0], 1)}×{f(rieles[1], 1)}, {rieles[3]}"
    lineas.append(placa)
    for clase, titulo in (("solape", "Solapes de patio"), ("fuera", "Fuera del contorno"), ("zona", "En zona prohibida")):
        items = de(clase)
        extra = ""
        if clase == "zona" and modelo.get("zonas_dentro"):
            extra = " · zona dentro de la placa: " + " ".join(f"{z} {f(a, 0)} mm²" for z, a in modelo["zonas_dentro"].items())
        lineas.append(f"{titulo}: {len(items)}" + (" · " + _lista(items) if items else "") + extra)
    seri = {}
    for i in inc:
        if i["grupo"] in NOMBRES_SERIGRAFIA:
            seri[i["grupo"]] = seri.get(i["grupo"], 0) + 1
    nref = sum(1 for t in modelo["textos"] if t["tipo"] == "ref")
    lineas.append(f"Serigrafía ({nref} referencias): " + (" · ".join(f"{NOMBRES_SERIGRAFIA[k]} {n}" for k, n in
                                                                   sorted(seri.items(), key=lambda kv: -kv[1])) or "sin fallos"))
    cal = modelo.get("calor") or []
    if cal:
        peores = sorted((x for x in cal if x["libre"] is not None), key=lambda x: x["libre"] / x["A"])
        lineas.append(f"Térmico: {f(sum(x['P'] for x in cal), 2)} W en {len(cal)} fuentes · cobre libre/necesario (mm²): "
                      + _lista([f"{x['ref']} {cifra(x['libre'], x['A'], True, 0)}/{f(x['A'], 0)}" for x in peores], 6, 110))
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
    completo += [f"calor\t{x['ref']}\t{f(x['P'], 2)} W\t" + (f"libre {cifra(x['libre'], x['A'], True, 0)} / {f(x['A'], 0)} mm²"
                                                             if x["libre"] is not None else "sin cobre pedido")
                 + f"\t{x['regla']['id']}"
                 + (f"\tanillo {f(x['anillo'], 0)} mm², ocupan: " + " · ".join(f"{q} {f(a, 0)}" for q, a in
                                                                               sorted(x["ocupan"], key=lambda t: -t[1]) if a >= 0.5)
                    if x.get("ocupan") is not None else "") for x in cal]
    if base:
        completo.append(f"precio\t{f(w, 1)}x{f(hh, 1)}\t" + (f"{casa['id']} {f(casa['mm'])} $ / {casa['objetivo']} uds\t{casa['origen']}"
                                                            if casa else f"sin tarifa\t{base['origen']}"))
    clase_red = modelo.get("clase_red", {})
    completo += [f"red\t{r}\t{clase_red.get(r, 'Default')}\t{f(l, 1)}" for r, l in sorted(por_red.items(), key=lambda kv: -kv[1])]
    return lineas, completo, (0 if not obl and not fallos else 1)


# ------------------------------------------------------------------ referencias (colocación automática)

LADOS_TEXTO = ("sup", "inf", "izq", "der")


def candidatos(cp, ofs, gaps=(0.15, 0.35, 0.7)):
    """Cajas candidatas para un texto alrededor de la caja de patio cp; ofs = {giro: caja de la tinta respecto del
    ancla del texto}. Devuelve (orden de preferencia, giro, ancla, caja)."""
    salida = []
    cx, cy = (cp[0] + cp[2]) / 2, (cp[1] + cp[3]) / 2
    n = 0
    for g in gaps:
        for giro, o in sorted(ofs.items()):
            w, h = o[2] - o[0], o[3] - o[1]
            for lado in LADOS_TEXTO:
                if lado in ("sup", "inf"):
                    y0 = cp[1] - g - h if lado == "sup" else cp[3] + g
                    xs = [cx - w / 2, cp[0], cp[2] - w]
                    cajas = [(x, y0, x + w, y0 + h) for x in xs]
                else:
                    x0 = cp[0] - g - w if lado == "izq" else cp[2] + g
                    ys = [cy - h / 2, cp[1], cp[3] - h]
                    cajas = [(x0, y, x0 + w, y + h) for y in ys]
                for c in cajas:
                    n += 1
                    salida.append((n + (0 if giro == 0 else 0.5), giro, (c[0] - o[0], c[1] - o[1]), c))
    return salida


def colocar_referencias(modelo, ofs, reglas, fijas, vuelta_atras=3):
    """Elige la posición de las referencias que no están en `fijas`, con `vuelta_atras` pasadas que deshacen las vecinas
    de las que no tienen sitio. Devuelve ({ref: (giro, ancla, caja)}, sin_sitio, referencias recolocadas)."""
    p = param_serigrafia(reglas)
    H = modelo["huellas"]
    idx = Indices(modelo)
    # las referencias que se van a colocar no cuentan como obstáculo hasta que se colocan
    claves_ref = {}
    for i, t in enumerate(modelo["textos"]):
        if t["tipo"] == "ref":
            claves_ref[t["dueño"]] = ("t", i)
            if t["dueño"] not in fijas:
                idx.textos.quitar(("t", i))
    pendientes = [r for r in H if r not in fijas and ofs.get(r)]
    cand = {r: candidatos(caja_de(H[r]["cuerpo"]), ofs[r]) for r in pendientes}

    def coste(r, c):
        m = medir_caja(modelo, idx, c[3], r)
        malos = fallos_caja(m, p)
        return len(malos), m["junto"] + c[0] * 0.001, malos

    def elegir(r):
        mejor, valor = None, None
        for c in cand[r]:  # en orden de preferencia: la primera sin fallos es la más cercana
            n, d, malos = coste(r, c)
            if valor is None or (n, d) < valor[:2]:
                mejor, valor = c, (n, d, malos)
            if n == 0:
                break
        return mejor, valor[2]

    def poner(r, c):
        t = modelo["textos"][claves_ref[r][1]]
        t.update({"caja": c[3], "visible": True})
        idx.textos.poner(claves_ref[r], c[3], t)

    # primero las más rodeadas (patios a ≤ 1,5 mm): son las que tienen menos sitio
    vecinas = {r: sum(1 for x in idx.patio.cerca(caja_de(H[r]["cuerpo"]), 1.5) if x[2][0] != r) for r in pendientes}
    elegida, fallos = {}, {}
    for r in sorted(pendientes, key=lambda r: (-vecinas[r], _clave_ref(r))):
        elegida[r], fallos[r] = elegir(r)
        poner(r, elegida[r])

    # vuelta atrás: cada referencia sin sitio quita las de sus vecinas (a ≤ 2 mm de su patio), se coloca primero
    # y las vuelve a colocar; se queda el cambio si bajan los fallos del grupo
    recolocadas = 0
    for _ in range(vuelta_atras):
        cambio = False
        for r in sorted((r for r in elegida if fallos[r]), key=_clave_ref):
            if not fallos[r]:
                continue
            cp = caja_de(H[r]["cuerpo"])
            grupo = [r] + sorted((v for v in elegida if v != r and dist_cajas(elegida[v][3], cp) <= 2.0),
                                 key=lambda v: (-vecinas[v], _clave_ref(v)))[:6]
            antes = {}
            for v in grupo:
                antes[v] = (elegida[v], fallos_caja(medir_caja(modelo, idx, elegida[v][3], v, claves_ref[v]), p))
            for v in grupo:
                idx.textos.quitar(claves_ref[v])
            nuevo = {}
            for v in grupo:
                nuevo[v] = elegir(v)
                poner(v, nuevo[v][0])
            if sum(len(m) for _, m in nuevo.values()) < sum(len(m) for _, m in antes.values()):
                for v in grupo:
                    elegida[v], fallos[v] = nuevo[v]
                recolocadas += len(grupo)
                cambio = True
            else:
                for v in grupo:
                    idx.textos.quitar(claves_ref[v])
                for v in grupo:
                    elegida[v], fallos[v] = antes[v]
                    poner(v, elegida[v])
        if not cambio:
            break
    salida = {r: (c[1], c[2], c[3]) for r, c in elegida.items()}
    sin_sitio = [f"{r} ({', '.join(NOMBRES_SERIGRAFIA[k] for k in fallos[r])})"
                 for r in sorted(elegida, key=_clave_ref) if fallos[r]]
    return salida, sin_sitio, recolocadas


def _desplazamientos(board, pcbnew, alto, trazo, refs):
    """Caja de la tinta de cada referencia respecto de su ancla, para giro 0 y 90, con alto y trazo dados."""
    ofs = {}
    for fp in board.GetFootprints():
        if fp.GetReference() not in refs:
            continue
        t = fp.Reference()
        t.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(alto), pcbnew.FromMM(alto)))
        t.SetTextThickness(pcbnew.FromMM(trazo))
        t.SetVisible(True)
        pos = t.GetPosition()
        px, py = pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y)
        ofs[fp.GetReference()] = {}
        for giro in (0, 90):
            t.SetTextAngleDegrees(giro)
            c = caja_tinta(t, pcbnew)
            if c:
                ofs[fp.GetReference()][giro] = (c[0] - px, c[1] - py, c[2] - px, c[3] - py)
    return ofs


# ------------------------------------------------------------------ principal

def _ruta_reglas(args):
    ruta = Path(args.reglas) if args.reglas else (raiz_repo() or Path.cwd()) / "docs" / "diseno" / "colocacion-reglas.csv"
    if not ruta.is_file():
        raise Fallo(f"no existe la tabla de reglas {ruta} (--reglas)")
    return ruta


def _placa(args):
    if not getattr(args, "placa", None):
        return None
    t = tam_placa(args.placa)
    if not t:
        raise Fallo(f"tamaño de placa «{args.placa}»: se espera ANCHOxALTO en mm (p. ej. 100x80)")
    return t


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="orden", required=True)
    e = sub.add_parser("extraer", help="huellas en formato compacto")
    e.add_argument("pcb", help=".kicad_pcb o carpeta del proyecto")
    e.add_argument("-o", "--salida", help="archivo de texto con el listado")
    e.add_argument("--refs", help="solo estas referencias (separadas por comas o espacios), con sus pads")
    v = sub.add_parser("evaluar", help="puntúa una colocación")
    v.add_argument("pcb", help=".kicad_pcb o carpeta del proyecto")
    v.add_argument("tabla", nargs="?", help="CSV de colocar.py (sin ella, la PCB tal cual)")
    v.add_argument("--reglas", help="CSV de reglas (por defecto docs/diseno/colocacion-reglas.csv)")
    v.add_argument("--placa", metavar="ANCHOxALTO", help="contorno rectangular de ese tamaño (mueve los taladros)")
    v.add_argument("--detalle", metavar="ARCHIVO", help="lista completa de incidencias y longitudes")
    v.add_argument("--omitir", metavar="TIPOS", help="no evalúa las reglas de estos tipos (p. ej. serigrafia), para iterar")
    rf = sub.add_parser("referencias", help="coloca las referencias de serigrafía y escribe la tabla con rx,ry,rgiro")
    rf.add_argument("pcb", help=".kicad_pcb o carpeta del proyecto")
    rf.add_argument("tabla", nargs="?", help="CSV de colocar.py (sin ella, la PCB tal cual)")
    rf.add_argument("-o", "--salida", required=True, help="CSV de salida, con rx,ry,rgiro,ralto,rtrazo")
    rf.add_argument("--reglas", help="CSV de reglas (por defecto docs/diseno/colocacion-reglas.csv)")
    rf.add_argument("--placa", metavar="ANCHOxALTO", help="contorno rectangular de ese tamaño")
    rf.add_argument("--todas", action="store_true", help="recoloca también las que ya traen rx,ry en la tabla")
    rf.add_argument("--sin-vuelta", action="store_true", help="una sola pasada voraz, sin deshacer vecinas")
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

    ruta_reglas = _ruta_reglas(args)
    reglas, clases = leer_reglas(ruta_reglas)

    if args.orden == "referencias":
        import colocar
        p = param_serigrafia(reglas)
        filas, tam = colocar.leer_tabla(args.tabla, con_placa=True) if args.tabla else ([], None)
        fijas = set() if args.todas else {d["ref"] for d in filas if d.get("rx") is not None and d.get("ry") is not None}
        guardado = {}

        def extra(board, pcbnew, modelo):
            refs = {fp.GetReference() for fp in board.GetFootprints()} - fijas
            guardado["ofs"] = _desplazamientos(board, pcbnew, p["alto"], p["trazo_ref"], refs)

        modelo, info = cargar(args.pcb, args.tabla, _placa(args), extra)
        elegidas, sin_sitio, recolocadas = colocar_referencias(modelo, guardado["ofs"], reglas, fijas,
                                                               0 if args.sin_vuelta else 3)
        por_ref = {d["ref"]: d for d in filas}
        H = modelo["huellas"]
        for r in sorted(H, key=_clave_ref):
            if r not in por_ref and r in elegidas:
                por_ref[r] = {"ref": r, "x": None, "y": None, "giro": None, "cara": None}
        for r, (giro, ancla, _) in elegidas.items():
            d = por_ref[r]
            d.update({"rx": ancla[0] - H[r]["x"], "ry": ancla[1] - H[r]["y"], "rgiro": giro, "ralto": p["alto"],
                      "rtrazo": p["trazo_ref"]})
        salida = Path(args.salida)
        salida.parent.mkdir(parents=True, exist_ok=True)
        with open(salida, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["ref", "x", "y", "giro", "cara"] + list(colocar.COLUMNAS_REF))
            if info["placa"]:
                w.writerow(["PLACA", f(info["placa"][0], 3), f(info["placa"][1], 3), "", ""])
            for r in sorted(por_ref, key=_clave_ref):
                d = por_ref[r]
                w.writerow([r] + ["" if d.get(k) is None else (d[k] if k == "cara" else f(d[k], 4))
                                  for k in ("x", "y", "giro", "cara") + colocar.COLUMNAS_REF])
        emitir([f"{salida}: {len(elegidas)} referencias colocadas (alto {f(p['alto'])} mm, trazo {f(p['trazo_ref'], 3)} mm)"
                f" · {len(fijas)} fijas de la tabla · vuelta atrás: {recolocadas} recolocadas",
                f"Sin sitio que cumpla todo ({len(sin_sitio)}): " + (_lista(sin_sitio, 12, 600) if sin_sitio else "ninguna")])
        return 1 if sin_sitio else 0

    if args.omitir:
        omitir = {x.strip() for x in args.omitir.split(",")}
        if omitir - TIPOS:
            raise Fallo(f"--omitir: tipos desconocidos {', '.join(sorted(omitir - TIPOS))}")
        reglas = [r for r in reglas if r["tipo"] not in omitir]
    modelo, info = cargar(args.pcb, args.tabla, _placa(args))
    info["tabla"] = Path(args.tabla).name if args.tabla else None
    inc, errores, por_clase, por_red = evaluar(modelo, reglas, clases)
    lineas, completo, codigo = informe(modelo, info, reglas, ruta_reglas.name, inc, errores, por_clase, por_red)
    if args.detalle:
        Path(args.detalle).write_text("\n".join(lineas + ["", "# detalle"] + completo) + "\n", encoding="utf-8")
    emitir(lineas)
    return codigo


if __name__ == "__main__":
    principal(main)
