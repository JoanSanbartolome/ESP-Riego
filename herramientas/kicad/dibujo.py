"""Ayuda para dibujar hojas con cables (descripciones de hoja.py) y comprobar su conectividad (SPEC-0035).

Uso:
    python herramientas/kicad/dibujo.py comprobar nueva.json hardware/v2/mcu.kicad_sch --proyecto hardware/v2
    python herramientas/kicad/dibujo.py comprobar nueva.json original.json --proyecto <copia>/v2 [--detalle F]

comprobar: grupos de pines de la descripción nueva (cables, etiquetas, alimentación y pines de subhoja, por
geometría) frente a los de la original (hoja .kicad_sch o descripción JSON), solo con los pines que están en las
dos. Una red renombrada no es diferencia; una red partida o unida sí. Avisa de los pines «W» sin cable y de las
etiquetas sueltas. Sale con 1 si hay diferencias o avisos.

Como módulo, desde un script de dibujo (en la carpeta temporal):
    from dibujo import Dibujo
    d = Dibujo("hardware/v2/salidas.kicad_sch", proyecto="<copia>/v2")  # campos y símbolos de la original
    d.pieza("R44", 50.8, 50.8, giro=90, pines={"2": "P:GND"})          # el resto de pines, «W»
    d.pieza("U7", 139.7, 88.9, refs={"Salidas/Canal1": "U7", ...})      # hoja repetida
    d.w("R44.1", (40.64, 50.8)); d.hv("R44.2", "C45.1"); d.vh(a, b)     # «REF.n» = punta del pin
    d.lab("H:OUT_DEN:input", (40.64, 50.8), "L"); d.pwr("GND", (50.8, 60.96))
    d.txt(x, y, "nota"); d.box(x, y, ancho, alto, "Título: R44 (REL-04)"); d.hoja(nombre, archivo, ...)
    dif = d.guardar("nueva.json")    # escribe la descripción y devuelve las diferencias con la original
Formato de la descripción en herramientas/kicad/README.md (hoja.py).
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import Fallo, emitir, parse, principal  # noqa: E402
import hoja as _hoja  # noqa: E402

SIN_RED = ("", "W", "NC")


def r(v):
    """Redondeo a 0,01 mm (las cotas de la rejilla de 1,27 mm quedan exactas)."""
    return round(float(v) * 100) / 100


def cargar(original):
    """Descripción de una hoja: JSON de `hoja.py extraer` o la propia hoja .kicad_sch."""
    original = Path(original)
    if original.suffix == ".kicad_sch":
        desc, _ = _hoja.extraer(original, forzar=True)
        return desc
    return json.loads(original.read_text(encoding="utf-8"))


class Pines:
    """Pines visibles de cada símbolo de librería, con caché."""

    def __init__(self, carpeta):
        self.carpeta, self._c = (Path(carpeta) if carpeta else None), {}

    def __call__(self, spec):
        if spec not in self._c:
            pines, _, _ = _hoja.pines_y_caja(parse(_hoja.bloque_libreria(spec, self.carpeta)))
            self._c[spec] = {p["num"]: p for p in pines if not p["oculto"]}
        return self._c[spec]

    def punta(self, pz, numero):
        p = self(pz["simbolo"])[str(numero)]
        x, y = _hoja.girar(p["x"], p["y"], float(pz["x"]), float(pz["y"]), int(pz.get("giro", 0)))
        return (r(x), r(y))


def _ref(pz):
    return pz.get("ref") or next(iter((pz.get("refs") or {}).values()))


def red_de(con):
    """Nombre de red de una conexión: L y H por nombre (se unen en la hoja), G y P aparte; None si no tiene."""
    if con in SIN_RED:
        return None
    t = con.split(":")
    return t[1] if t[0] in ("L", "H") else f"{t[0]}:{t[1]}"


def grupos(desc, pines):
    """(grupos de pines conectados [frozenset «REF.n» o «Subhoja:PIN»], avisos). Un pin cuenta si llega a algo."""
    padre = {}

    def f(a):
        padre.setdefault(a, a)
        while padre[a] != a:
            padre[a] = padre[padre[a]]
            a = padre[a]
        return a

    def u(a, b):
        padre[f(a)] = f(b)

    puntas, avisos, nombres = {}, [], {}
    for pz in desc.get("piezas", []):
        for n, con in pz.get("pines", {}).items():
            q = f"{_ref(pz)}.{n}"
            puntas[q] = pines.punta(pz, n)
            nombres[q] = red_de(con)
    for hj in desc.get("hojas", []):
        for p in hj.get("pines", []):
            q = f"{hj['nombre']}:{p['nombre']}"
            puntas[q] = (r(hj["x"] if p["lado"] == "L" else hj["x"] + hj["ancho"]), r(p["y"]))
            nombres[q] = None
    etiquetas = [((r(e["x"]), r(e["y"])), red_de(e["con"])) for e in desc.get("etiquetas", [])]
    etiquetas += [((r(x), r(y)), "P:PWR_FLAG") for x, y in desc.get("banderas", [])]
    tramos, _, _ = _hoja.tramos_y_uniones(desc.get("cables", []), list(puntas.values()) + [k for k, _ in etiquetas])
    for a, b in tramos:
        u(("P",) + a, ("P",) + b)
    tocados = {p for t in tramos for p in t}
    for q, k in puntas.items():
        u(("N", q), ("P",) + k)
        if nombres[q]:
            u(("N", q), ("R", nombres[q]))
    for k, nombre in etiquetas:
        if k not in tocados and k not in puntas.values():
            avisos.append(f"etiqueta {nombre} suelta en {k}")
        if nombre != "P:PWR_FLAG":
            u(("P",) + k, ("R", nombre))
    for pz in desc.get("piezas", []):
        for n, con in pz.get("pines", {}).items():
            if con == "W" and puntas[f"{_ref(pz)}.{n}"] not in tocados:
                avisos.append(f"{_ref(pz)}.{n}: «W» sin cable en {puntas[f'{_ref(pz)}.{n}']}")
    por_raiz = {}
    for q in puntas:
        por_raiz.setdefault(f(("N", q)), set()).add(q)
    # un pin solo, sin red ni cable, no está conectado a nada
    con_red = {f(m) for m in list(padre) if m[0] == "R"}
    conectados = []
    for raiz, g in por_raiz.items():
        if len(g) > 1 or raiz in con_red or puntas[next(iter(g))] in tocados:
            conectados.append(frozenset(g))
    return conectados, avisos


def comparar(original, nueva, pines):
    """Diferencias de conectividad (por grupos de pines) de `nueva` frente a `original`, en los pines comunes."""
    go, _ = grupos(original, pines)
    gn, avisos = grupos(nueva, pines)
    refs = {_ref(pz) for pz in nueva.get("piezas", [])}
    todos_o = {q for pz in original.get("piezas", []) for q in (f"{_ref(pz)}.{n}" for n in pz.get("pines", {}))}
    en_o = {q: g for g in go for q in g}
    en_n = {q: g for g in gn for q in g}
    dif = []
    for q in sorted(set(en_o) - set(en_n)):
        if q.split(".")[0] in refs:
            dif.append(f"{q}: conectado en la original y suelto en la nueva")
    for q in sorted(set(en_n) - set(en_o)):
        if q in todos_o:
            dif.append(f"{q}: suelto en la original y conectado en la nueva")
    comunes = set(en_o) & set(en_n)
    vistos = set()
    for q in sorted(comunes):
        a, b = en_o[q] & comunes, en_n[q] & comunes
        if a != b and (a, b) not in vistos:
            vistos.add((a, b))
            dif.append(f"{q}: con {', '.join(sorted(a - {q})) or 'nada'} en la original y con "
                       f"{', '.join(sorted(b - {q})) or 'nada'} en la nueva")
    return dif, avisos, len({en_n[q] for q in comunes})


class Dibujo:
    """Construye una descripción de hoja.py con las piezas (campos, símbolo, DNP) de una hoja original."""

    def __init__(self, original, proyecto=None, papel=None):
        self.orig = cargar(original)
        self.o = {_ref(p): p for p in self.orig["piezas"]}
        self.pines = Pines(proyecto)
        self.papel = papel or self.orig.get("papel", "A4")
        self.piezas, self.cables, self.etiquetas, self.textos, self.recuadros = {}, [], [], [], []
        self.banderas, self.hojas = [], []

    def pieza(self, ref, x, y, giro=0, pines=None, ref_pos=None, val_pos=None, refs=None):
        """Pieza `ref` de la original en (x, y); todos sus pines a «W» salvo los de `pines`. `ref_pos`/`val_pos`:
        (x, y[, giro[, justify]]) del campo; `refs`: referencias por instancia (hoja repetida)."""
        if ref not in self.o:
            raise Fallo(f"{ref} no está en la hoja original")
        o = self.o[ref]
        pz = {"ref": ref, "simbolo": o["simbolo"], "x": x, "y": y, "giro": giro, "dnp": o.get("dnp", False),
              "en_bom": o.get("en_bom", True), "campos": o["campos"], "pines": {n: "W" for n in o["pines"]}}
        for n, c in (pines or {}).items():
            if str(n) not in pz["pines"]:
                raise Fallo(f"{ref}: no tiene el pin {n}")
            pz["pines"][str(n)] = c
        pos = {}
        for campo, p in (("Reference", ref_pos), ("Value", val_pos)):
            if p:
                p = list(p)
                pos[campo] = p + [0, "left"][len(p) - 2:] if len(p) < 4 else p
        if pos:
            pz["pos"] = pos
        if refs:
            pz["refs"] = dict(refs)
        self.piezas[ref] = pz
        return pz

    def p(self, rp):
        """Punta del pin «REF.n»."""
        ref, n = rp.split(".")
        return self.pines.punta(self.piezas[ref], n)

    def _pt(self, a):
        return self.p(a) if isinstance(a, str) else (r(a[0]), r(a[1]))

    def w(self, *pts):
        """Cable por los puntos dados («REF.n» o (x, y))."""
        self.cables.append([list(self._pt(a)) for a in pts])

    def hv(self, a, b):
        """De a en horizontal y luego en vertical hasta b."""
        a, b = self._pt(a), self._pt(b)
        self.w(a, (b[0], a[1]), b)

    def vh(self, a, b):
        """De a en vertical y luego en horizontal hasta b."""
        a, b = self._pt(a), self._pt(b)
        self.w(a, (a[0], b[1]), b)

    def lab(self, con, a, lado="R"):
        x, y = self._pt(a)
        e = {"x": x, "y": y, "con": con}
        if not con.startswith("P:"):
            e["lado"] = lado
        self.etiquetas.append(e)

    def pwr(self, nombre, a, giro=None):
        self.lab(f"P:{nombre}" + (f":{giro}" if giro else ""), a)

    def txt(self, x, y, texto, justify="left bottom"):
        self.textos.append({"x": x, "y": y, "tam": 1.27, "negrita": False, "texto": texto, "justify": justify})

    def box(self, x, y, ancho, alto, titulo):
        self.recuadros.append({"x": x, "y": y, "ancho": ancho, "alto": alto, "titulo": titulo})

    def hoja(self, nombre, archivo, x, y, ancho, alto, pines):
        """Subhoja; `pines` = [(nombre, forma, lado, y)]. Devuelve {nombre del pin: (x, y)} para cablear."""
        self.hojas.append({"nombre": nombre, "archivo": archivo, "x": x, "y": y, "ancho": ancho, "alto": alto,
                           "pines": [{"nombre": n, "forma": f, "lado": l, "y": py} for n, f, l, py in pines]})
        return {n: (r(x if l == "L" else x + ancho), r(py)) for n, f, l, py in pines}

    def descripcion(self, cajetin=None):
        caj = dict(self.orig.get("cajetin", {}))
        caj.update(cajetin or {})
        return {"papel": self.papel, "cajetin": caj, "piezas": list(self.piezas.values()), "banderas": self.banderas,
                "textos": self.textos, "etiquetas": self.etiquetas, "cables": self.cables, "uniones": [],
                "recuadros": self.recuadros, "hojas": self.hojas}

    def guardar(self, ruta, cajetin=None, todas=True):
        """Escribe la descripción y devuelve las diferencias de conectividad y los avisos frente a la original.
        `todas`: falla si falta alguna pieza de la original."""
        falta = sorted(set(self.o) - set(self.piezas))
        if todas and falta:
            raise Fallo(f"faltan piezas de la original: {', '.join(falta)}")
        desc = self.descripcion(cajetin)
        Path(ruta).write_text(json.dumps(desc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        dif, avisos, _ = comparar(self.orig, desc, self.pines)
        return dif + avisos


def orden_comprobar(args):
    pines = Pines(args.proyecto)
    nueva, original = cargar(args.nueva), cargar(args.original)
    dif, avisos, n = comparar(original, nueva, pines)
    emitir([f"{args.nueva} frente a {args.original}: {n} grupos de pines comunes; {len(dif)} diferencias, "
            f"{len(avisos)} avisos"] + dif + avisos, detalle=args.detalle)
    return 1 if dif or avisos else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="orden", required=True)
    c = sub.add_parser("comprobar", help="conectividad de una descripción frente a la hoja original")
    c.add_argument("nueva", help="descripción JSON nueva")
    c.add_argument("original", help="hoja .kicad_sch o descripción JSON original")
    c.add_argument("--proyecto", help="carpeta del proyecto (sym-lib-table)")
    c.add_argument("--detalle", metavar="ARCHIVO")
    c.set_defaults(f=orden_comprobar)
    args = ap.parse_args()
    return args.f(args)


if __name__ == "__main__":
    principal(main)
