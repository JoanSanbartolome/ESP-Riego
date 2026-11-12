"""Anchos, separaciones y vías por red de la PCB frente a una tabla de restricciones.

Uso:
    python herramientas/kicad/restricciones.py hardware/v2 docs/diseno/restricciones.csv
    python herramientas/kicad/restricciones.py placa.kicad_pcb tabla.md --json

Tabla: CSV (coma o punto y coma) o tabla Markdown con las columnas de los documentos de bloque:
`Red | Corriente | Ancho mín. | Separación | Ubicación / keepout | Notas`, y opcionalmente `Vía`
(taladro/corona, p. ej. «0,3/0,6»). `Red` admite varios nombres separados por comas y comodines
(`OUT*`); se compara con el nombre completo de la red y con su último tramo (`/Salidas/OUT1` → `OUT1`).
Cotas en mm. Por cada fila comprueba:
  - ancho: la pista más estrecha de esas redes frente a «Ancho mín.»;
  - separación: la regla que aplicará el DRC (clase de red del .kicad_pro o regla del .kicad_dru
    con `A.NetClass == '…'` o `A.NetName == '…'`) y la distancia medida entre pistas y vías de
    redes distintas en la misma capa (los pads y las zonas los mide el DRC);
  - vías: taladro y corona de cada vía frente a «Vía» o, si no hay columna, a FAB-02 (0,3 / 0,6).
Una fila sin redes en la PCB o sin pistas todavía se da como «sin datos», no como fallo.
Solo lee. Sale con 1 si alguna fila falla.
"""
import argparse
import csv
import fnmatch
import io
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import Fallo, emitir, leer, parse, principal, proyecto, trozos, uno, val  # noqa: E402

FAB02 = (0.3, 0.6)
EPS = 1e-6


def numero(celda):
    """Primer número de una celda («≥ 1,2 mm» → 1.2); None si no hay."""
    m = re.search(r"\d+(?:[.,]\d+)?", celda or "")
    return float(m.group(0).replace(",", ".")) if m else None


def leer_tabla(ruta):
    """Filas de la tabla: dict con redes (patrones), ancho, separacion, via (taladro, corona) y texto."""
    texto = Path(ruta).read_text(encoding="utf-8-sig")
    lineas = [l for l in texto.splitlines() if l.strip()]
    md = [l for l in lineas if l.strip().startswith("|")]
    if md:
        celdas = [[c.strip() for c in l.strip().strip("|").split("|")] for l in md]
        celdas = [f for f in celdas if not all(re.fullmatch(r":?-{2,}:?", c) for c in f)]
    else:
        sep = ";" if lineas[0].count(";") > lineas[0].count(",") else ","
        celdas = [[c.strip() for c in f] for f in csv.reader(io.StringIO(texto), delimiter=sep) if f]
    if not celdas:
        raise Fallo(f"{ruta}: tabla vacía")
    cab = [re.sub(r"[^a-záéíóúñ]", "", c.lower()) for c in celdas[0]]

    def col(*nombres):
        return next((i for i, c in enumerate(cab) if any(c.startswith(n) for n in nombres)), None)

    i_red, i_ancho, i_sep, i_via = col("red", "net"), col("ancho"), col("separaci", "clearance"), col("vía", "via")
    if i_red is None or (i_ancho is None and i_sep is None):
        raise Fallo(f"{ruta}: faltan las columnas Red y Ancho mín. o Separación")
    filas = []
    for f in celdas[1:]:
        f = f + [""] * (len(cab) - len(f))
        redes = [re.sub(r"^\*\*(.*)\*\*$", r"\1", r.strip()) for r in re.split(r"[,;]\s*", f[i_red].replace("`", "")) if r.strip()]
        if not redes:
            continue
        via = None
        if i_via is not None and numero(f[i_via]) is not None:
            nums = [float(x.replace(",", ".")) for x in re.findall(r"\d+(?:[.,]\d+)?", f[i_via])]
            via = (nums[0], nums[1] if len(nums) > 1 else FAB02[1])
        filas.append({"redes": redes, "ancho": numero(f[i_ancho]) if i_ancho is not None else None,
                      "separacion": numero(f[i_sep]) if i_sep is not None else None, "via": via, "texto": f[i_red]})
    return filas


def leer_pcb(pcb):
    """Pistas (con arcos) y vías: listas de dict con red, ancho, capa y extremos."""
    texto = leer(pcb)
    pistas, vias, redes = [], [], set(re.findall(r'\(net "((?:\\.|[^"\\])*)"\)', texto))
    for nombre, i, j in trozos(texto):
        if nombre in ("segment", "arc"):
            n = parse(texto[i:j])
            a, b = uno(n, "start"), uno(n, "end")
            pistas.append({"red": val(n, "net"), "ancho": float(val(n, "width", "0")), "capa": val(n, "layer"),
                           "a": (float(a[1]), float(a[2])), "b": (float(b[1]), float(b[2]))})
        elif nombre == "via":
            n = parse(texto[i:j])
            at = uno(n, "at")
            vias.append({"red": val(n, "net"), "corona": float(val(n, "size", "0")), "taladro": float(val(n, "drill", "0")),
                         "a": (float(at[1]), float(at[2])), "b": (float(at[1]), float(at[2]))})
    return pistas, vias, redes - {""}


def casa(patron, red):
    return fnmatch.fnmatchcase(red, patron) or fnmatch.fnmatchcase(red.rsplit("/", 1)[-1], patron)


def reglas_separacion(carpeta, nombre):
    """Función red → (separación que aplicará el DRC, origen) según el .kicad_pro y el .kicad_dru."""
    clases, patrones, asignadas, por_clase, por_red = {"Default": 0.0}, [], {}, {}, {}
    pro = Path(carpeta) / f"{nombre}.kicad_pro"
    if pro.is_file():
        ns = json.loads(pro.read_text(encoding="utf-8")).get("net_settings") or {}
        clases = {c["name"]: float(c.get("clearance", 0)) for c in ns.get("classes") or []} or clases
        patrones = [(p.get("pattern", ""), p.get("netclass", "")) for p in ns.get("netclass_patterns") or []]
        asignadas = ns.get("netclass_assignments") or {}
    dru = Path(carpeta) / f"{nombre}.kicad_dru"
    if dru.is_file():
        texto = leer(dru)
        for n, i, j in trozos("(x " + texto + ")"):
            if n != "rule":
                continue
            regla = parse(("(x " + texto + ")")[i:j])
            cond = val(regla, "condition")
            minimo = next((numero(val(c, "min")) for c in regla if isinstance(c, list) and c[:2] == ["constraint", "clearance"]), None)
            if minimo is None:
                continue
            for clase in re.findall(r"[AB]\.NetClass\s*==\s*'([^']+)'", cond):
                por_clase[clase] = max(por_clase.get(clase, 0), minimo)
            for red in re.findall(r"[AB]\.NetName\s*==\s*'([^']+)'", cond):
                por_red[red] = max(por_red.get(red, 0), minimo)

    def de(red):
        mias = list(asignadas.get(red) or [])
        for patron, clase in patrones:
            try:
                if fnmatch.fnmatchcase(red, patron) or re.fullmatch(patron, red):
                    mias.append(clase)
            except re.error:
                pass
        mias = mias or ["Default"]
        mejor, origen = max(((clases.get(c, 0.0), f"clase {c}") for c in mias), key=lambda t: t[0])
        for c in mias:
            if por_clase.get(c, 0) > mejor:
                mejor, origen = por_clase[c], f"regla .kicad_dru de la clase {c}"
        if por_red.get(red, 0) > mejor:
            mejor, origen = por_red[red], "regla .kicad_dru de la red"
        return mejor, origen

    return de


def _dist_punto(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    l2 = dx * dx + dy * dy
    t = 0.0 if l2 == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / l2))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def _cortan(a, b, c, d):
    def lado(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return lado(a, b, c) * lado(a, b, d) < 0 and lado(c, d, a) * lado(c, d, b) < 0


def distancia(s, t):
    """Separación entre cobres de dos pistas o vías (negativa si se solapan)."""
    if _cortan(s["a"], s["b"], t["a"], t["b"]):
        centro = 0.0
    else:
        centro = min(_dist_punto(s["a"], t["a"], t["b"]), _dist_punto(s["b"], t["a"], t["b"]),
                     _dist_punto(t["a"], s["a"], s["b"]), _dist_punto(t["b"], s["a"], s["b"]))
    return centro - s.get("ancho", s.get("corona", 0)) / 2 - t.get("ancho", t.get("corona", 0)) / 2


def separacion_medida(mias, otras, limite):
    """Menor separación entre los elementos `mias` y los de otras redes en la misma capa, hasta `limite` + 1 mm."""
    celda, rejilla = 2.0, {}
    for k, t in enumerate(otras):
        for cx in range(int(min(t["a"][0], t["b"][0]) // celda) - 1, int(max(t["a"][0], t["b"][0]) // celda) + 2):
            for cy in range(int(min(t["a"][1], t["b"][1]) // celda) - 1, int(max(t["a"][1], t["b"][1]) // celda) + 2):
                rejilla.setdefault((cx, cy), []).append(k)
    menor, vistos = None, set()
    alcance = int((limite + 1.0) // celda) + 1
    for n, s in enumerate(mias):
        cerca = set()
        for cx in range(int(min(s["a"][0], s["b"][0]) // celda) - alcance, int(max(s["a"][0], s["b"][0]) // celda) + alcance + 1):
            for cy in range(int(min(s["a"][1], s["b"][1]) // celda) - alcance, int(max(s["a"][1], s["b"][1]) // celda) + alcance + 1):
                cerca.update(rejilla.get((cx, cy), ()))
        for k in cerca:
            t = otras[k]
            if t["red"] == s["red"] or (s.get("capa") and t.get("capa") and s["capa"] != t["capa"]):
                continue
            d = distancia(s, t)
            if menor is None or d < menor[0]:
                menor = (d, s["red"], t["red"])
    return menor


def comprobar(pcb, tabla, carpeta=None, nombre=None):
    """Resultado por fila y global: dict con 'filas' y 'vias_fab02'."""
    pistas, vias, redes = leer_pcb(pcb)
    regla = reglas_separacion(carpeta or Path(pcb).parent, nombre or Path(pcb).stem)
    todo = pistas + vias
    filas = []
    for fila in tabla:
        mias = sorted(r for r in redes if any(casa(p, r) for p in fila["redes"]))
        r = {"red": fila["texto"], "redes": mias, "estado": "OK", "motivos": []}
        mis_pistas = [p for p in pistas if p["red"] in mias]
        mis_vias = [v for v in vias if v["red"] in mias]
        r["pistas"], r["vias"] = len(mis_pistas), len(mis_vias)
        if not mias:
            r["estado"], r["motivos"] = "SIN DATOS", ["ninguna red de la PCB casa con la fila"]
            filas.append(r)
            continue
        if fila["ancho"] is not None and mis_pistas:
            r["ancho_min"] = min(p["ancho"] for p in mis_pistas)
            estrechas = sum(p["ancho"] < fila["ancho"] - EPS for p in mis_pistas)
            if estrechas:
                r["motivos"].append(f"{estrechas} pistas de menos de {fila['ancho']:g} (mín. {r['ancho_min']:g})")
        if fila["separacion"] is not None:
            peor = min((regla(red) + (red,) for red in mias), key=lambda t: t[0])
            r["separacion_regla"] = peor[0]
            if peor[0] < fila["separacion"] - EPS:
                r["motivos"].append(f"el DRC aplicará {peor[0]:g} a {peor[2]} ({peor[1]}) y se piden {fila['separacion']:g}")
            medida = separacion_medida(mis_pistas + mis_vias, todo, fila["separacion"])
            if medida:
                r["separacion_medida"] = round(medida[0], 4)
                if medida[0] < fila["separacion"] - EPS:
                    r["motivos"].append(f"{medida[1]} queda a {medida[0]:.3f} de {medida[2]} y se piden {fila['separacion']:g}")
        taladro, corona = fila["via"] or FAB02
        malas = [v for v in mis_vias if v["taladro"] < taladro - EPS or v["corona"] < corona - EPS]
        if malas:
            r["motivos"].append(f"{len(malas)} vías de menos de {taladro:g}/{corona:g}")
        if r["motivos"]:
            r["estado"] = "FALLA"
        elif not mis_pistas and not mis_vias:
            r["estado"], r["motivos"] = "SIN DATOS", ["redes sin pistas todavía"]
        filas.append(r)
    fuera = [v for v in vias if v["taladro"] < FAB02[0] - EPS or v["corona"] < FAB02[1] - EPS]
    return {"filas": filas, "pistas": len(pistas), "vias": len(vias), "vias_bajo_fab02": len(fuera),
            "fallan": sum(f["estado"] == "FALLA" for f in filas), "sin_datos": sum(f["estado"] == "SIN DATOS" for f in filas)}


def informe(r):
    lineas = [f"{len(r['filas'])} filas · fallan {r['fallan']} · sin datos {r['sin_datos']} · PCB con {r['pistas']} pistas y "
              f"{r['vias']} vías ({r['vias_bajo_fab02']} por debajo de FAB-02 0,3/0,6)"]
    for f in r["filas"]:
        datos = []
        if "ancho_min" in f:
            datos.append(f"ancho mín. {f['ancho_min']:g}")
        if "separacion_regla" in f:
            datos.append(f"regla {f['separacion_regla']:g}")
        if "separacion_medida" in f:
            datos.append(f"medida {f['separacion_medida']:g}")
        datos.append(f"{f['pistas']} pistas, {f['vias']} vías")
        lineas.append(f"{f['estado']:<9} {f['red'][:28]:<28} {' · '.join(datos)}" + (f" — {'; '.join(f['motivos'])}" if f["motivos"] else ""))
    return lineas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pcb", help=".kicad_pcb, .kicad_pro o carpeta del proyecto")
    ap.add_argument("tabla", help="tabla de restricciones (CSV o Markdown)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--detalle", metavar="ARCHIVO", help="guarda todas las filas")
    args = ap.parse_args()
    carpeta, nombre = proyecto(args.pcb)
    pcb = carpeta / f"{nombre}.kicad_pcb"
    if not pcb.is_file():
        raise Fallo(f"no existe {pcb}")
    r = comprobar(pcb, leer_tabla(args.tabla), carpeta, nombre)
    if args.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        emitir(informe(r), detalle=args.detalle)
    return 1 if r["fallan"] or r["vias_bajo_fab02"] else 0


if __name__ == "__main__":
    principal(main)
