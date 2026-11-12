"""Campos de los símbolos: revisa su coherencia y los copia desde una tabla CSV.

Uso:
    python herramientas/kicad/campos.py revisar hardware/v2
    python herramientas/kicad/campos.py revisar hardware/v2/salidas.kicad_sch --tabla hardware/componentes/campos-salidas.csv
    python herramientas/kicad/campos.py aplicar hardware/componentes/campos-salidas.csv <hoja.kicad_sch> -o <destino.kicad_sch>

revisar: lista (1) campos que faltan (Value, Footprint, MPN, Fabricante, Datasheet, Description,
LCSC Part#; a lo que está fuera del BOM solo se le pide Value, Footprint y Description), (2) la misma pieza (mismo LCSC o MPN) con campos distintos, también entre hojas,
(3) los DNP y (4) las diferencias con la tabla. Sin --tabla busca
`../componentes/campos-<hoja>.csv` junto a la carpeta del proyecto. Sale con 1 si hay incidencias.

aplicar: escribe en -o una copia de la hoja con los campos y el DNP de la tabla. No toca la hoja
de origen (salvo que -o sea la misma ruta).

Tabla: CSV con cabecera `Refs` (R1, «R26-R31» o «C45, C46»), los nombres de los campos y `DNP`
(sí/no). Una celda vacía deja el campo como está.
"""
import argparse
import csv
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import (CAMPOS, Fallo, emitir, es_pieza, esc, hojas, leer, escribir, principal, proyecto,  # noqa: E402
                    simbolos_hoja)

MISMA_PIEZA = ("Value", "Footprint", "MPN", "Fabricante", "Datasheet", "LCSC Part#")
SIN_PIEZA = ("Value", "Footprint", "Description")  # lo exigible a lo que no va al BOM (TP, JP, taladros)
SI = {"si", "sí", "yes", "x", "1", "true", "dnp"}


def clave_ref(ref):
    m = re.match(r"([^\d]*)(\d*)(.*)", ref)
    return (m.group(1), int(m.group(2) or 0), m.group(3))


def rangos(refs):
    """['R1','R2','R3','C7'] → 'C7, R1–R3'."""
    refs = sorted(set(refs), key=clave_ref)
    salida, i = [], 0
    while i < len(refs):
        j = i
        while (j + 1 < len(refs) and clave_ref(refs[j + 1])[0] == clave_ref(refs[i])[0]
               and clave_ref(refs[j + 1])[1] == clave_ref(refs[j])[1] + 1):
            j += 1
        salida.append(refs[i] if j == i else f"{refs[i]}–{refs[j]}" if j > i + 1 else f"{refs[i]}, {refs[j]}")
        i = j + 1
    return ", ".join(salida)


def expandir(celda):
    """'R26–R31, C45 C46' → ['R26', …, 'R31', 'C45', 'C46']."""
    refs = []
    for trozo in re.split(r"[,;\s]+", celda.replace("–", "-").replace("—", "-").strip()):
        if not trozo:
            continue
        m = re.fullmatch(r"([A-Za-z#_]+)(\d+)-(?:\1)?(\d+)", trozo)
        if m:
            refs += [f"{m.group(1)}{n}" for n in range(int(m.group(2)), int(m.group(3)) + 1)]
        else:
            refs.append(trozo)
    return refs


def leer_tabla(ruta):
    """{ref: {campo: valor, 'DNP': bool|None}} de un CSV de campos."""
    texto = Path(ruta).read_text(encoding="utf-8-sig")
    separador = ";" if texto.split("\n", 1)[0].count(";") > texto.split("\n", 1)[0].count(",") else ","
    filas = list(csv.DictReader(io.StringIO(texto), delimiter=separador))
    if not filas:
        raise Fallo(f"{ruta}: tabla vacía")
    col_ref = next((c for c in filas[0] if c and c.strip().rstrip(".").lower() in ("refs", "ref", "reference", "referencia")), None)
    if not col_ref:
        raise Fallo(f"{ruta}: falta la columna Refs")
    tabla = {}
    for fila in filas:
        datos = {}
        for campo, valor in fila.items():
            if campo is None or campo == col_ref:
                continue
            valor = (valor or "").strip()
            if campo.strip().upper() == "DNP":
                datos["DNP"] = (valor.lower() in SI) if valor else None
            elif valor:
                datos[campo.strip()] = valor
        for ref in expandir(fila[col_ref] or ""):
            if ref in tabla:
                raise Fallo(f"{ruta}: {ref} aparece dos veces")
            tabla[ref] = datos
    return tabla


def piezas_de(archivos):
    """[(hoja, símbolo)] de todas las piezas de las hojas dadas."""
    salida = []
    for archivo in archivos:
        for s in simbolos_hoja(leer(archivo)):
            if es_pieza(s):
                salida.append((Path(archivo).name, s))
    return salida


def vacio(campo, valor):
    return not valor.strip() or (campo == "Datasheet" and valor.strip() == "~")


def revisar(archivos, tablas=None):
    """Incidencias de campos: dict con 'faltan', 'distintos', 'dnp', 'tabla' y 'piezas'."""
    piezas = piezas_de(archivos)
    faltan = defaultdict(list)       # (hoja, campo) -> refs
    for hoja, s in piezas:
        for campo in (CAMPOS if s["in_bom"] else SIN_PIEZA):
            if vacio(campo, s["props"].get(campo, "")):
                faltan[(hoja, campo)].append(s["ref"])
    grupos = defaultdict(list)       # pieza -> [(hoja, símbolo)]
    for hoja, s in piezas:
        clave = s["props"].get("LCSC Part#", "").strip() or s["props"].get("MPN", "").strip()
        if clave and s["in_bom"]:
            grupos[clave].append((hoja, s))
    distintos = []
    for clave, miembros in sorted(grupos.items()):
        for campo in MISMA_PIEZA:
            valores = defaultdict(list)
            for hoja, s in miembros:
                valores[s["props"].get(campo, "")].append(f"{s['ref']}")
            if len(valores) > 1:
                distintos.append({"pieza": clave, "campo": campo,
                                  "valores": {v: rangos(refs) for v, refs in valores.items()},
                                  "hojas": sorted({h for h, _ in miembros})})
    dnp = sorted((s["ref"] for _, s in piezas if s["dnp"]), key=clave_ref)
    de_tabla = []
    for hoja, s in piezas:
        fila = (tablas or {}).get(hoja, {}).get(s["ref"])
        if fila is None:
            if tablas and hoja in tablas:
                de_tabla.append(f"{s['ref']} ({hoja}): no está en la tabla")
            continue
        for campo, valor in fila.items():
            if campo == "DNP":
                if valor is not None and valor != s["dnp"]:
                    de_tabla.append(f"{s['ref']}: DNP {'sí' if s['dnp'] else 'no'} en la hoja y {'sí' if valor else 'no'} en la tabla")
            elif s["props"].get(campo, "") != valor:
                de_tabla.append(f"{s['ref']}: {campo} «{s['props'].get(campo, '')}» ≠ tabla «{valor}»")
    for hoja, tabla in (tablas or {}).items():
        refs = {s["ref"] for h, s in piezas if h == hoja}
        sobran = [r for r in tabla if r not in refs]
        if sobran:
            de_tabla.append(f"{hoja}: en la tabla y no en la hoja: {rangos(sobran)}")
    return {"piezas": len(piezas), "faltan": {f"{h}|{c}": rangos(r) for (h, c), r in sorted(faltan.items())},
            "n_faltan": sum(len(r) for r in faltan.values()), "distintos": distintos, "dnp": dnp, "tabla": de_tabla}


def corto(texto, n=46):
    return texto if len(texto) <= n else texto[:n - 1] + "…"


def informe(r, n_tablas):
    lineas = [f"{r['piezas']} piezas · campos que faltan {r['n_faltan']} · misma pieza con campos distintos "
              f"{len(r['distintos'])} · DNP {len(r['dnp'])} · diferencias con la tabla {len(r['tabla'])}"
              f"{'' if n_tablas else ' (sin tabla)'}"]
    for clave, refs in r["faltan"].items():
        hoja, campo = clave.split("|")
        lineas.append(f"FALTA {campo} en {hoja}: {corto(refs, 90)}")
    for d in r["distintos"]:
        partes = " | ".join(f"«{corto(v)}» {corto(refs, 30)}" for v, refs in d["valores"].items())
        lineas.append(f"DISTINTO {d['pieza']} {d['campo']}: {partes}")
    if r["dnp"]:
        lineas.append(f"DNP: {rangos(r['dnp'])}")
    lineas += [f"TABLA {t}" for t in r["tabla"]]
    return lineas


def _bloque_campo(nombre, valor, x, y, sangria, salto):
    t = sangria + "\t"
    return salto.join([
        f'{sangria}(property "{esc(nombre)}" "{esc(valor)}"', f"{t}(at {x} {y} 0)", f"{t}(hide yes)",
        f"{t}(show_name no)", f"{t}(do_not_autoplace no)", f"{t}(effects", f"{t}\t(font", f"{t}\t\t(size 1.27 1.27)",
        f"{t}\t)", f"{t})", f"{sangria})"]) + salto


def aplicar(texto, tabla):
    """Devuelve (texto nuevo, nº de campos cambiados, refs sin tocar por no estar en la tabla)."""
    salto = "\r\n" if "\r\n" in texto else "\n"
    cambios, fuera = 0, []
    for s in sorted(simbolos_hoja(texto), key=lambda s: -s["i"]):
        if not es_pieza(s):
            continue
        fila = tabla.get(s["ref"])
        if fila is None:
            fuera.append(s["ref"])
            continue
        bloque = texto[s["i"]:s["j"]]
        for campo, valor in fila.items():
            if campo == "DNP":
                if valor is not None and valor != s["dnp"]:
                    bloque, n = re.subn(r"\(dnp (yes|no)\)", f"(dnp {'yes' if valor else 'no'})", bloque, count=1)
                    cambios += n
                continue
            if s["props"].get(campo) == valor:
                continue
            patron = re.compile(r'(\(property\s+"' + re.escape(esc(campo)) + r'"\s+)"(?:\\.|[^"\\])*"')
            if patron.search(bloque):
                bloque = patron.sub(lambda m: m.group(1) + '"' + esc(valor) + '"', bloque, count=1)
            else:
                m = re.search(r"\n([ \t]*)\((pin|instances)\b", bloque)
                if not m:
                    raise Fallo(f"{s['ref']}: no sé dónde insertar el campo {campo}")
                x, y = re.search(r"\(at ([-\d.]+) ([-\d.]+)", bloque).groups()
                bloque = bloque[:m.start() + 1] + _bloque_campo(campo, valor, x, y, m.group(1), salto) + bloque[m.start() + 1:]
            cambios += 1
        texto = texto[:s["i"]] + bloque + texto[s["j"]:]
    return texto, cambios, sorted(fuera, key=clave_ref)


def tablas_por_defecto(archivos):
    tablas = {}
    for a in archivos:
        csv_ = Path(a).resolve().parent.parent / "componentes" / f"campos-{Path(a).stem}.csv"
        if csv_.is_file():
            tablas[Path(a).name] = leer_tabla(csv_)
    return tablas


def archivos_de(rutas):
    archivos = []
    for r in rutas:
        r = Path(r)
        if r.suffix == ".kicad_sch" and r.is_file() and len(rutas) > 1 or (r.suffix == ".kicad_sch" and not r.with_suffix(".kicad_pro").exists()):
            archivos.append(r.resolve())
        else:
            carpeta, nombre = proyecto(r)
            archivos += [h["archivo"] for h in hojas(carpeta / f"{nombre}.kicad_sch") if h["archivo"].is_file()]
    return list(dict.fromkeys(archivos))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="orden", required=True)
    r = sub.add_parser("revisar", help="lista las incoherencias de campos")
    r.add_argument("rutas", nargs="+", help="proyecto (carpeta o .kicad_pro) u hojas .kicad_sch")
    r.add_argument("--tabla", help="CSV de campos (para una sola hoja)")
    r.add_argument("--json", action="store_true")
    r.add_argument("--detalle", metavar="ARCHIVO", help="guarda la lista completa")
    a = sub.add_parser("aplicar", help="copia los campos de la tabla a una hoja")
    a.add_argument("tabla")
    a.add_argument("hoja")
    a.add_argument("-o", "--salida", required=True, help="hoja de destino")
    args = ap.parse_args()

    if args.orden == "aplicar":
        tabla = leer_tabla(args.tabla)
        texto, cambios, fuera = aplicar(leer(args.hoja), tabla)
        escribir(args.salida, texto)
        emitir([f"{args.salida}: {cambios} campos cambiados en {len(tabla)} referencias de la tabla",
                f"Piezas de la hoja que no están en la tabla: {rangos(fuera) or 'ninguna'}"])
        return 0
    archivos = archivos_de(args.rutas)
    if args.tabla:
        if len(archivos) != 1:
            raise Fallo("--tabla vale para una sola hoja")
        tablas = {archivos[0].name: leer_tabla(args.tabla)}
    else:
        tablas = tablas_por_defecto(archivos)
    res = revisar(archivos, tablas)
    if args.json:
        print(json.dumps(res, ensure_ascii=False))
    else:
        emitir(informe(res, len(tablas)), detalle=args.detalle)
    return 1 if res["n_faltan"] or res["distintos"] or res["tabla"] else 0


if __name__ == "__main__":
    principal(main)
