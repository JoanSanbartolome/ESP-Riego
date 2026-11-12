"""Tipo (Basic/Extended), stock y precio de N códigos LCSC en JLCPCB, en una llamada.

Uso:
    python herramientas/kicad/jlc.py C534868 C8465 C25804
    python herramientas/kicad/jlc.py --de docs/diseno/salidas.md --csv stock.csv
    python herramientas/kicad/jlc.py --de hardware/v2/mcu.kicad_sch --cantidad 10

Los códigos se dan sueltos o se sacan de cualquier archivo de texto con --de (todo lo que
tenga forma de «C» + 3 a 9 cifras). La tabla lleva la fecha de la consulta; --csv guarda
además todas las filas (código, MPN, fabricante, tipo, stock, precio, fecha). El precio es
el del tramo que corresponde a --cantidad (por defecto, el primero). Necesita red: consulta
la API pública de JLCPCB. Sale con 1 si algún código no aparece o no tiene stock.
"""
import argparse
import csv
import datetime
import json
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import Fallo, emitir, principal  # noqa: E402

URL = "https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList"
TIPOS = {"base": "Basic", "expand": "Extended"}
CODIGO = re.compile(r"(?<![A-Za-z0-9])C\d{3,9}(?![A-Za-z0-9])")


def codigos_de(texto):
    """Códigos LCSC de un texto, en orden de aparición y sin repetir."""
    return list(dict.fromkeys(CODIGO.findall(texto)))


def interpretar(codigo, respuesta, cantidad=1):
    """Fila de la tabla a partir del JSON de la API (None si el código no está)."""
    lista = (((respuesta.get("data") or {}).get("componentPageInfo") or {}).get("list")) or []
    pieza = next((x for x in lista if x.get("componentCode") == codigo), None)
    if pieza is None:
        return None
    tipo = TIPOS.get(pieza.get("componentLibraryType"), pieza.get("componentLibraryType") or "?")
    if tipo == "Extended" and pieza.get("preferredComponentFlag"):
        tipo = "Extended (preferida)"
    precio = None
    for tramo in pieza.get("componentPrices") or []:
        desde, hasta = tramo.get("startNumber") or 0, tramo.get("endNumber") or -1
        if precio is None or (desde <= cantidad and (hasta < 0 or cantidad <= hasta)):
            precio = tramo.get("productPrice")
    return {"codigo": codigo, "mpn": pieza.get("componentModelEn") or "", "fabricante": pieza.get("componentBrandEn") or "",
            "tipo": tipo, "stock": int(pieza.get("stockCount") or 0), "precio": precio,
            "encapsulado": pieza.get("componentSpecificationEn") or ""}


def consultar(codigo, cantidad=1, intentos=2):
    cuerpo = json.dumps({"keyword": codigo, "currentPage": 1, "pageSize": 25}).encode()
    peticion = urllib.request.Request(URL, data=cuerpo, headers={"Content-Type": "application/json",
                                                                 "User-Agent": "Mozilla/5.0"})
    error = None
    for _ in range(intentos):
        try:
            with urllib.request.urlopen(peticion, timeout=30) as r:
                return interpretar(codigo, json.load(r), cantidad)
        except Exception as e:  # red, JSON o límite de la API: se reintenta una vez
            error = e
    return {"codigo": codigo, "error": f"{type(error).__name__}: {error}"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("codigos", nargs="*", help="códigos LCSC (C534868 …)")
    ap.add_argument("--de", action="append", default=[], metavar="ARCHIVO", help="saca los códigos de un archivo de texto")
    ap.add_argument("--cantidad", type=int, default=1, help="unidades, para elegir el tramo de precio")
    ap.add_argument("--csv", metavar="ARCHIVO", help="guarda todas las filas en CSV, con la fecha")
    args = ap.parse_args()

    codigos = list(args.codigos)
    for archivo in args.de:
        codigos += codigos_de(Path(archivo).read_text(encoding="utf-8", errors="replace"))
    codigos = list(dict.fromkeys(c.upper() for c in codigos))
    if not codigos:
        raise Fallo("no hay códigos que consultar")
    malos = [c for c in codigos if not CODIGO.fullmatch(c)]
    if malos:
        raise Fallo(f"no son códigos LCSC: {', '.join(malos)}")

    fecha = datetime.date.today().isoformat()
    with ThreadPoolExecutor(max_workers=6) as hilos:
        filas = list(hilos.map(lambda c: consultar(c, args.cantidad), codigos))

    lineas = [f"JLCPCB · {fecha} · {len(codigos)} códigos · precio en USD para {args.cantidad} ud.",
              f"{'Código':<10} {'Tipo':<20} {'Stock':>10} {'Precio':>8}  MPN · fabricante"]
    tabla, problemas = [], 0
    for codigo, fila in zip(codigos, filas):
        if fila is None or "error" in fila:
            problemas += 1
            motivo = "SIN RESULTADO" if fila is None else fila["error"]
            lineas.append(f"{codigo:<10} {motivo}")
            tabla.append([codigo, "", "", motivo, "", "", fecha])
            continue
        problemas += fila["stock"] == 0
        precio = "" if fila["precio"] is None else f"{fila['precio']:.4f}"
        lineas.append(f"{codigo:<10} {fila['tipo']:<20} {fila['stock']:>10} {precio:>8}  "
                      f"{fila['mpn']} · {fila['fabricante']}"[:118])
        tabla.append([codigo, fila["mpn"], fila["fabricante"], fila["tipo"], fila["stock"], precio, fecha])
    if args.csv:
        with open(args.csv, "w", encoding="utf-8", newline="") as f:
            salida = csv.writer(f)
            salida.writerow(["LCSC", "MPN", "Fabricante", "Tipo", "Stock", "Precio_USD", "Fecha"])
            salida.writerows(tabla)
        lineas.append(f"CSV: {args.csv}")
    lineas.append(f"Sin resultado o sin stock: {problemas}")
    emitir(lineas, pista="--csv ARCHIVO")
    return 1 if problemas else 0


if __name__ == "__main__":
    principal(main)
