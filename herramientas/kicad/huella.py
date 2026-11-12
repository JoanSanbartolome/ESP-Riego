"""Cotas de un .kicad_mod: pads, paso, taladros, vías y pasta del pad expuesto, patio, serigrafía y 3D.

Uso:
    python herramientas/kicad/huella.py hardware/libraries/esp-riego.pretty/<huella>.kicad_mod
    python herramientas/kicad/huella.py esp-riego:<huella> --proyecto hardware/v2
    python herramientas/kicad/huella.py Package_TO_SOT_SMD:SOT-23-6 --simbolo Power_Protection:USBLC6-2SC6
    python herramientas/kicad/huella.py <huella> --json

La huella se da como ruta o como «Lib:Nombre» (librerías del proyecto de --proyecto y oficiales
de KiCad 10). Cotas en mm. El pad expuesto es el pad SMD mayor que comparte número con vías o
lleva `pad_prop_heatsink`; su pasta es la unión de las ventanas de F.Paste que caen dentro.
--simbolo cruza los números de pin del símbolo con los pads. Solo lee.
"""
import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import (Fallo, MODELOS, emitir, hijos, leer, parse, principal, ruta_huella,  # noqa: E402
                    ruta_simbolos, trozos, uno, val)

FAB02 = (0.3, 0.6)  # taladro y corona mínimos de una vía (FAB-02)
MARGEN_PATIO = 0.1  # margen mínimo del patio a los pads (KLC: 0,25 nominal; 0,15 en piezas pequeñas)


def f(x):
    return ("%.3f" % x).rstrip("0").rstrip(".").replace(".", ",") or "0"


def _capas(pad):
    return set(uno(pad, "layers", ["layers"])[1:])


def _en(capas, capa):
    return capa in capas or ("*." + capa.split(".")[1]) in capas or ("F&B." + capa.split(".")[1]) in capas


def leer_pads(nodo):
    pads = []
    for p in hijos(nodo, "pad"):
        at = uno(p, "at", ["at", "0", "0"])
        size = uno(p, "size", ["size", "0", "0"])
        drill = uno(p, "drill")
        taladro = None
        if drill:
            nums = [float(x) for x in drill[1:] if isinstance(x, str) and re.fullmatch(r"-?[\d.]+", x)]
            taladro = max(nums) if nums else None
            taladro_min = min(nums) if nums else None
        props = [c[1] for c in hijos(p, "property") if len(c) > 1]
        pads.append({
            "num": p[1], "tipo": p[2], "forma": p[3], "x": float(at[1]), "y": float(at[2]),
            "giro": float(at[3]) if len(at) > 3 else 0.0, "w": float(size[1]), "h": float(size[2]),
            "taladro": taladro, "taladro_min": taladro_min if drill else None, "capas": _capas(p),
            "props": props, "custom": p[3] == "custom",
        })
    return pads


def caja(pad, extra=0.0):
    """Caja envolvente (x0, y0, x1, y1) del pad, con su giro."""
    a = math.radians(pad["giro"])
    w = abs(pad["w"] * math.cos(a)) + abs(pad["h"] * math.sin(a))
    h = abs(pad["w"] * math.sin(a)) + abs(pad["h"] * math.cos(a))
    return (pad["x"] - w / 2 - extra, pad["y"] - h / 2 - extra, pad["x"] + w / 2 + extra, pad["y"] + h / 2 + extra)


def dentro_pad(pad, x, y, extra=0.0):
    a = math.radians(pad["giro"])
    dx, dy = x - pad["x"], y - pad["y"]
    lx, ly = dx * math.cos(a) - dy * math.sin(a), dx * math.sin(a) + dy * math.cos(a)
    if pad["forma"] == "circle":
        return math.hypot(lx, ly) < pad["w"] / 2 + extra
    return abs(lx) < pad["w"] / 2 + extra and abs(ly) < pad["h"] / 2 + extra


def area_union(rects):
    """Área de la unión de rectángulos (x0, y0, x1, y1) alineados con los ejes."""
    xs = sorted({r[0] for r in rects} | {r[2] for r in rects})
    ys = sorted({r[1] for r in rects} | {r[3] for r in rects})
    area = 0.0
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            cx, cy = (xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2
            if any(r[0] < cx < r[2] and r[1] < cy < r[3] for r in rects):
                area += (xs[i + 1] - xs[i]) * (ys[j + 1] - ys[j])
    return area


def _puntos(nodo, capa):
    """Puntos de muestra (x, y, medio ancho, índice de gráfico) de los gráficos de una capa."""
    salida, n = [], 0
    for tipo in ("fp_line", "fp_rect", "fp_circle", "fp_arc", "fp_poly"):
        for g in hijos(nodo, tipo):
            if val(g, "layer") != capa:
                continue
            n += 1
            ancho = float(val(uno(g, "stroke", []), "width", "0.12") or 0.12) / 2
            xy = lambda k: tuple(float(v) for v in uno(g, k)[1:3])  # noqa: E731
            tramos = []
            if tipo == "fp_line":
                tramos = [(xy("start"), xy("end"))]
            elif tipo == "fp_rect":
                (x0, y0), (x1, y1) = xy("start"), xy("end")
                e = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
                tramos = [(e[k], e[(k + 1) % 4]) for k in range(4)]
            elif tipo == "fp_poly":
                pts = [tuple(float(v) for v in p[1:3]) for p in hijos(uno(g, "pts", []), "xy")]
                tramos = [(pts[k], pts[(k + 1) % len(pts)]) for k in range(len(pts))]
            elif tipo == "fp_circle":
                (cx, cy), (ex, ey) = xy("center"), xy("end")
                r = math.hypot(ex - cx, ey - cy)
                pts = [(cx + r * math.cos(t / 60 * 2 * math.pi), cy + r * math.sin(t / 60 * 2 * math.pi)) for t in range(61)]
                tramos = [(pts[k], pts[k + 1]) for k in range(60)]
            elif tipo == "fp_arc":
                tramos = [(xy("start"), xy("mid")), (xy("mid"), xy("end"))]
            for (ax, ay), (bx, by) in tramos:
                pasos = max(1, int(math.hypot(bx - ax, by - ay) / 0.05))
                for k in range(pasos + 1):
                    salida.append((ax + (bx - ax) * k / pasos, ay + (by - ay) * k / pasos, ancho, n))
    return salida, n


def resolver_modelo(ruta, kiprjmod):
    ruta = re.sub(r"\$\{KICAD\d+_3DMODEL_DIR\}", str(MODELOS).replace("\\", "/"), ruta)
    ruta = ruta.replace("${KIPRJMOD}", str(kiprjmod).replace("\\", "/"))
    return Path(ruta)


def analizar(archivo, kiprjmod=None):
    """Todas las cotas de la huella, como dict."""
    archivo = Path(archivo)
    nodo = parse(leer(archivo))
    if nodo[0] not in ("footprint", "module"):
        raise Fallo(f"{archivo.name} no es una huella de KiCad")
    kiprjmod = Path(kiprjmod) if kiprjmod else archivo.parent.parent.parent / "_"
    pads = leer_pads(nodo)
    cobre = [p for p in pads if any(c.endswith(".Cu") for c in p["capas"])]
    numerados = [p for p in cobre if p["num"]]
    r = {"nombre": nodo[1], "archivo": str(archivo), "attr": " ".join(uno(nodo, "attr", ["attr", "—"])[1:]),
         "pads": len(pads), "numeros": sorted({p["num"] for p in numerados}, key=lambda s: (len(s), s))}

    grupos = Counter()
    nums = {}
    for p in cobre:
        clave = (p["tipo"], p["forma"], p["w"], p["h"], p["taladro"], "F.Cu" if "F.Cu" in p["capas"] else
                 "B.Cu" if "B.Cu" in p["capas"] else "*.Cu")
        grupos[clave] += 1
        nums.setdefault(clave, []).append(p["num"] or "—")
    r["grupos"] = [{"n": n, "tipo": k[0], "forma": k[1], "w": k[2], "h": k[3], "taladro": k[4], "capa": k[5],
                    "nums": sorted(set(nums[k]), key=lambda s: (len(s), s))} for k, n in grupos.most_common()]

    # paso: distancia mínima entre centros de pads del grupo de señal más numeroso
    senal = [p for p in numerados if (p["w"], p["h"]) == max(Counter((q["w"], q["h"]) for q in numerados).items(),
                                                             key=lambda kv: kv[1])[0]] if numerados else []
    dist = [math.hypot(a["x"] - b["x"], a["y"] - b["y"]) for i, a in enumerate(senal) for b in senal[i + 1:]]
    r["paso"] = round(min(dist), 4) if dist else None
    r["filas_x"] = sorted({round(p["x"], 3) for p in senal})[:6] if senal else []
    r["filas_y"] = sorted({round(p["y"], 3) for p in senal})[:6] if senal else []
    r["taladros"] = dict(Counter(p["taladro"] for p in pads if p["taladro"]))

    # pad expuesto, vías y pasta
    smd = [p for p in cobre if p["tipo"] == "smd" and "F.Cu" in p["capas"]]
    con_vias = {p["num"] for p in cobre if p["tipo"] == "thru_hole" and p["num"]}
    candidatos = [p for p in smd if p["num"] and (p["num"] in con_vias or "pad_prop_heatsink" in p["props"])]
    ep = max(candidatos, key=lambda p: p["w"] * p["h"]) if candidatos else None
    if ep is None and len(smd) > 2:
        mayor = max(smd, key=lambda p: p["w"] * p["h"])
        resto = sorted(q["w"] * q["h"] for q in smd if q is not mayor)
        if mayor["w"] * mayor["h"] > 4 * resto[len(resto) // 2]:
            ep = mayor
    r["ep"] = None
    r["vias"] = []
    if ep:
        cx0, cy0, cx1, cy1 = caja(ep)
        vias = [p for p in cobre if p["tipo"] == "thru_hole" and p["num"] == ep["num"]
                and cx0 <= p["x"] <= cx1 and cy0 <= p["y"] <= cy1]
        ventanas = [caja(p) for p in pads if p["tipo"] == "smd" and _en(p["capas"], "F.Paste")
                    and cx0 - 1e-6 <= p["x"] <= cx1 + 1e-6 and cy0 - 1e-6 <= p["y"] <= cy1 + 1e-6
                    and (p is ep or not any(c.endswith(".Cu") for c in p["capas"]))]
        ventanas = [(max(a, cx0), max(b, cy0), min(c, cx1), min(d, cy1)) for a, b, c, d in ventanas]
        area_ep = ep["w"] * ep["h"]
        pasta = area_union(ventanas) if ventanas else 0.0
        sobre_taladro = sum(1 for v in vias for a, b, c, d in ventanas
                            if a - v["taladro"] / 2 < v["x"] < c + v["taladro"] / 2
                            and b - v["taladro"] / 2 < v["y"] < d + v["taladro"] / 2)
        r["ep"] = {"num": ep["num"], "w": ep["w"], "h": ep["h"], "area": round(area_ep, 3),
                   "ventanas_pasta": len(ventanas), "pasta": round(pasta, 3),
                   "pasta_pct": round(100 * pasta / area_ep, 1), "pasta_sobre_taladro": sobre_taladro,
                   "cobre_inferior": any(p["tipo"] == "smd" and p["num"] == ep["num"] and "B.Cu" in p["capas"] for p in cobre)}
        r["vias"] = [{"x": v["x"], "y": v["y"], "taladro": v["taladro"], "corona": min(v["w"], v["h"])} for v in vias]
    # vías térmicas sin pad expuesto reconocido: pads pasantes que comparten número con un pad SMD
    nums_smd = {p["num"] for p in smd if p["num"]}
    todas = [p for p in cobre if p["tipo"] == "thru_hole" and p["num"] in nums_smd]
    r["vias_fab02"] = all(p["taladro_min"] is not None and p["taladro_min"] >= FAB02[0] - 1e-9
                          and min(p["w"], p["h"]) >= FAB02[1] - 1e-9 for p in todas)
    r["n_vias"] = len(todas)
    r["vias_tipos"] = dict(Counter(f"{f(p['taladro_min'])}/{f(min(p['w'], p['h']))}" for p in todas))

    # patio
    patio = {}
    for capa in ("F.CrtYd", "B.CrtYd"):
        pts, _ = _puntos(nodo, capa)
        if pts:
            patio[capa] = (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))
    r["patio"] = {k: [round(v, 3) for v in c] for k, c in patio.items()}
    r["patio_margen"] = None
    if patio and cobre:
        c = next(iter(patio.values()))
        cajas = [caja(p) for p in cobre]
        px = (min(b[0] for b in cajas), min(b[1] for b in cajas), max(b[2] for b in cajas), max(b[3] for b in cajas))
        r["patio_margen"] = round(min(px[0] - c[0], px[1] - c[1], c[2] - px[2], c[3] - px[3]), 3)

    # serigrafía sobre pads con apertura de máscara
    malos = set()
    for capa, mascara in (("F.SilkS", "F.Mask"), ("B.SilkS", "B.Mask")):
        pts, _ = _puntos(nodo, capa)
        expuestos = [p for p in pads if _en(p["capas"], mascara)]
        for x, y, ancho, n in pts:
            if (capa, n) not in malos and any(dentro_pad(p, x, y, ancho - 0.01) for p in expuestos):
                malos.add((capa, n))
    r["serigrafia_sobre_pads"] = len(malos)
    r["pads_custom"] = sum(p["custom"] for p in pads)

    # modelos 3D
    r["modelos"] = []
    for m in hijos(nodo, "model"):
        ruta = resolver_modelo(m[1], kiprjmod)
        r["modelos"].append({"ruta": m[1], "existe": ruta.is_file(), "ext": ruta.suffix,
                             "absoluta": bool(re.match(r"^([A-Za-z]:|/|\\\\)", m[1])),
                             "offset": uno(uno(m, "offset", []), "xyz", ["xyz", "0", "0", "0"])[1:],
                             "rotate": uno(uno(m, "rotate", []), "xyz", ["xyz", "0", "0", "0"])[1:]})
    return r


def pines_simbolo(spec, carpeta=None):
    """Números de pin de «Lib:Nombre» (sigue `extends`)."""
    apodo, nombre = spec.split(":", 1)
    texto = leer(ruta_simbolos(apodo, carpeta))
    bloques = {parse_nombre(texto, i): (i, j) for n, i, j in trozos(texto) if n == "symbol"}
    if nombre not in bloques:
        raise Fallo(f"no existe el símbolo {spec}")
    i, j = bloques[nombre]
    padre = re.search(r'\(extends "([^"]+)"\)', texto[i:j])
    if padre:
        i, j = bloques[padre.group(1)]
    return re.findall(r'\(number "([^"]*)"', texto[i:j])


def parse_nombre(texto, i):
    return re.match(r'\(symbol\s+"((?:\\.|[^"\\])*)"', texto[i:i + 300]).group(1)


def informe(r):
    lineas = [f"{r['nombre']} · attr {r['attr']} · {r['pads']} pads · números {r['numeros'][0] if r['numeros'] else '—'}"
              f"…{r['numeros'][-1] if r['numeros'] else '—'} ({len(r['numeros'])})"]
    for g in r["grupos"][:8]:
        tal = f", taladro {f(g['taladro'])}" if g["taladro"] else ""
        ns = g["nums"] if len(g["nums"]) <= 4 else [g["nums"][0], "…", g["nums"][-1]]
        lineas.append(f"  {g['n']:>3} × {g['tipo']} {g['forma']} {f(g['w'])} × {f(g['h'])}{tal} [{g['capa']}] nº {' '.join(ns)}")
    if len(r["grupos"]) > 8:
        lineas.append(f"  … y {len(r['grupos']) - 8} grupos más (--json)")
    if r["paso"]:
        lineas.append(f"Paso {f(r['paso'])} · columnas x {' '.join(f(v) for v in r['filas_x'])}"
                      f" · filas y {' '.join(f(v) for v in r['filas_y'])}")
    if r["taladros"]:
        lineas.append("Taladros: " + ", ".join(f"{n} × {f(d)}" for d, n in sorted(r["taladros"].items())))
    if r["ep"]:
        e = r["ep"]
        lineas.append(f"Pad expuesto nº {e['num']}: {f(e['w'])} × {f(e['h'])} = {f(e['area'])} mm²"
                      f"{' · cobre también en B.Cu' if e['cobre_inferior'] else ''}")
        if r["vias"]:
            tipos = Counter((v["taladro"], v["corona"]) for v in r["vias"])
            lineas.append("  Vías: " + ", ".join(f"{n} de {f(t)} / {f(c)}" for (t, c), n in tipos.items())
                          + f" · FAB-02 (≥ 0,3 / 0,6): {'cumple' if r['vias_fab02'] else 'NO CUMPLE'}")
        else:
            lineas.append("  Vías: ninguna")
        lineas.append(f"  Pasta: {e['ventanas_pasta']} ventanas, {f(e['pasta'])} mm² = {e['pasta_pct']:.0f} % del pad"
                      f" · ventanas sobre taladros: {e['pasta_sobre_taladro']}")
    elif r["n_vias"]:
        lineas.append(f"Vías en pads SMD: {r['vias_tipos']} · FAB-02: {'cumple' if r['vias_fab02'] else 'NO CUMPLE'}")
    if r["patio"]:
        capa, c = next(iter(r["patio"].items()))
        lineas.append(f"Patio {capa}: {f(c[2] - c[0])} × {f(c[3] - c[1])} · margen mínimo a los pads {f(r['patio_margen'])}"
                      f"{'' if r['patio_margen'] >= MARGEN_PATIO else ' (INSUFICIENTE)'}")
    else:
        lineas.append("Patio: NO HAY")
    lineas.append(f"Serigrafía sobre pads: {r['serigrafia_sobre_pads']} gráficos"
                  + (f" · {r['pads_custom']} pads custom (medidos por su ancla)" if r["pads_custom"] else ""))
    for m in r["modelos"] or [None]:
        lineas.append("Modelo 3D: NO HAY" if m is None else
                      f"Modelo 3D: {m['ruta']} · {'existe' if m['existe'] else 'NO EXISTE'}"
                      f" · offset {' '.join(m['offset'])} · giro {' '.join(m['rotate'])}")
    return lineas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("huella", help="ruta de un .kicad_mod o «Lib:Nombre»")
    ap.add_argument("--proyecto", help="carpeta del proyecto (fp-lib-table y ${KIPRJMOD})")
    ap.add_argument("--simbolo", metavar="Lib:Nombre", help="cruza los pines de este símbolo con los pads")
    ap.add_argument("--json", action="store_true", help="todas las cotas en JSON")
    args = ap.parse_args()

    archivo = Path(args.huella)
    if not archivo.is_file():
        archivo = ruta_huella(args.huella, Path(args.proyecto).resolve() if args.proyecto else None)
        if archivo is None or not archivo.is_file():
            raise Fallo(f"no se encuentra la huella {args.huella}")
    r = analizar(archivo, Path(args.proyecto).resolve() if args.proyecto else None)
    if args.simbolo:
        pines = set(pines_simbolo(args.simbolo, Path(args.proyecto).resolve() if args.proyecto else None))
        pads = set(r["numeros"])
        r["cruce"] = {"simbolo": args.simbolo, "pines": len(pines), "pines_sin_pad": sorted(pines - pads),
                      "pads_sin_pin": sorted(pads - pines)}
    if args.json:
        print(json.dumps(r, ensure_ascii=False))
        return 0
    lineas = informe(r)
    if args.simbolo:
        c = r["cruce"]
        lineas.append(f"Cruce con {c['simbolo']}: {c['pines']} pines · sin pad {c['pines_sin_pad'] or 'ninguno'}"
                      f" · pads sin pin {c['pads_sin_pin'] or 'ninguno'}")
    emitir(lineas, pista="--json")
    return 0


if __name__ == "__main__":
    principal(main)
