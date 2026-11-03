"""Gestión de specs: crea specs y genera el tablero y la matriz de trazabilidad.

Uso:
    python herramientas/gestion.py nueva-spec --titulo "..." --fase 3 --responsable ing-esquematicos
        [--requisitos ALI-01,ALI-03] [--depende SPEC-0002] [--estado propuesta|abierta] [--slug texto]
    python herramientas/gestion.py tablero
    python herramientas/gestion.py trazabilidad

Solo usa la biblioteca estándar. Los archivos generados no se editan a mano.
"""
import argparse
import datetime
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
GESTION = RAIZ / "gestion"
SPECS = GESTION / "specs"
INFORMES = GESTION / "informes"
DECISIONES = GESTION / "decisiones"
DOC_REQUISITOS = RAIZ / "docs" / "02-especificaciones-v2.md"

AGENTES = ("coordinador", "ing-esquematicos", "ing-layout", "jr-conformidad", "ing-validacion")
ESTADOS = ("propuesta", "abierta", "cerrada", "descartada")
AVISO = "<!-- Generado por herramientas/gestion.py: no editar a mano. -->"


def leer_front_matter(ruta):
    """Lee el front matter simple de un .md: `clave: valor` y listas `[a, b]`."""
    texto = ruta.read_text(encoding="utf-8-sig")
    if not texto.startswith("---"):
        return {}
    fin = texto.find("\n---", 3)
    if fin < 0:
        return {}
    datos = {}
    for linea in texto[3:fin].splitlines():
        if ":" not in linea or linea.lstrip().startswith("#"):
            continue
        clave, valor = linea.split(":", 1)
        valor = valor.strip()
        if valor.startswith("[") and valor.endswith("]"):
            datos[clave.strip()] = [v.strip() for v in valor[1:-1].split(",") if v.strip()]
        else:
            datos[clave.strip()] = valor.strip("\"'")
    return datos


def cargar(carpeta, patron):
    elementos = []
    for ruta in sorted(carpeta.glob(patron)):
        datos = leer_front_matter(ruta)
        if datos.get("id"):
            datos["_ruta"] = ruta
            elementos.append(datos)
    return elementos


def leer_requisitos():
    """Devuelve [(id, prioridad, descripción)] a partir de las tablas de docs/02."""
    patron = re.compile(r"^\|\s*([A-Z]{2,4}-\d{2})\s*\|\s*([MSC])\s*\|\s*(.+?)\s*\|\s*$")
    requisitos = []
    for linea in DOC_REQUISITOS.read_text(encoding="utf-8").splitlines():
        m = patron.match(linea)
        if m:
            requisitos.append(m.groups())
    return requisitos


def git(*args):
    resultado = subprocess.run(["git", "-C", str(RAIZ), *args], capture_output=True,
                               text=True, encoding="utf-8", errors="replace")
    return resultado.returncode, resultado.stdout


def slug(texto):
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    texto = re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")
    return "-".join(texto.split("-")[:6])


def enlace(datos):
    return f"[{datos['id']}]({datos['_ruta'].relative_to(GESTION).as_posix()})"


def celda(texto):
    return str(texto).replace("|", "\\|")


def escribir(ruta, lineas):
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    print(f"Generado {ruta.relative_to(RAIZ).as_posix()}")


def nueva_spec(args):
    if args.responsable not in AGENTES:
        sys.exit(f"Responsable desconocido: {args.responsable}. Válidos: {', '.join(AGENTES)}")
    requisitos = [r.strip() for r in args.requisitos.split(",") if r.strip()]
    conocidos = {r[0] for r in leer_requisitos()}
    desconocidos = [r for r in requisitos if r not in conocidos]
    if desconocidos:
        sys.exit(f"Requisitos que no existen en docs/02: {', '.join(desconocidos)}")

    numeros = [int(m.group(1)) for r in SPECS.glob("SPEC-*.md") if (m := re.match(r"SPEC-(\d{4})", r.name))]
    id_spec = f"SPEC-{max(numeros, default=-1) + 1:04d}"
    nombre = f"{id_spec}-{args.slug or slug(args.titulo)}"
    rama = f"spec/{nombre}"
    plantilla = (GESTION / "plantillas" / "spec.md").read_text(encoding="utf-8")
    texto = plantilla.format(
        id=id_spec, titulo=args.titulo, fase=args.fase, estado=args.estado,
        responsable=args.responsable, rama=rama, requisitos=", ".join(requisitos),
        depende_de=", ".join(d.strip() for d in args.depende.split(",") if d.strip()),
        fecha=datetime.date.today().isoformat())
    ruta = SPECS / f"{nombre}.md"
    ruta.write_text(texto, encoding="utf-8", newline="\n")
    print(f"Creada {ruta.relative_to(RAIZ).as_posix()}")
    print(f"Rama: {rama}")


def tablero(_args):
    specs = cargar(SPECS, "SPEC-*.md")
    informes = cargar(INFORMES, "VAL-*.md")
    decisiones = cargar(DECISIONES, "DEC-*.md")
    ultimo_informe = {}
    for informe in sorted(informes, key=lambda d: d["id"]):
        ultimo_informe[informe.get("spec")] = informe

    resumen = " · ".join(f"{e} {sum(s.get('estado') == e for s in specs)}" for e in ESTADOS)
    lineas = ["# Tablero", "", AVISO, "", f"Specs por estado: {resumen}.", ""]
    grupos = [(e, [s for s in specs if s.get("estado") == e]) for e in ESTADOS]
    grupos.append(("otro estado", [s for s in specs if s.get("estado") not in ESTADOS]))
    for estado, grupo in grupos:
        if not grupo:
            continue
        lineas += [f"## {estado.capitalize()}s ({len(grupo)})", "",
                   "| Spec | Título | Fase | Responsable | Rama | Validación | Creada | Cerrada |",
                   "|---|---|---|---|---|---|---|---|"]
        for s in grupo:
            informe = ultimo_informe.get(s["id"])
            validacion = (f"{informe['id']} ({informe.get('veredicto', '?')})" if informe
                          else s.get("validacion") or "—")
            lineas.append(f"| {enlace(s)} | {celda(s.get('titulo', ''))} | {s.get('fase', '')} | "
                          f"{s.get('responsable', '')} | `{s.get('rama', '')}` | {validacion} | "
                          f"{s.get('creada', '')} | {s.get('cerrada') or '—'} |")
        lineas.append("")

    if decisiones:
        lineas += ["## Decisiones", "", "| Decisión | Título | Estado | Decide | Fecha |", "|---|---|---|---|---|"]
        lineas += [f"| {enlace(d)} | {celda(d.get('titulo', ''))} | {d.get('estado', '')} | "
                   f"{d.get('decide', '')} | {d.get('fecha', '')} |" for d in decisiones]
        lineas.append("")
    if informes:
        lineas += ["## Informes de validación", "", "| Informe | Spec | Veredicto | Commit revisado | Fecha |",
                   "|---|---|---|---|---|"]
        lineas += [f"| {enlace(i)} | {i.get('spec', '')} | {i.get('veredicto', '')} | "
                   f"`{i.get('commit_revisado', '')}` | {i.get('fecha', '')} |" for i in informes]
        lineas.append("")
    escribir(GESTION / "TABLERO.md", lineas)


def commits_por_requisito():
    refs = ["HEAD"]
    if git("rev-parse", "-q", "--verify", "MERGE_HEAD")[0] == 0:
        refs.append("MERGE_HEAD")
    codigo, salida = git("log", *refs,
                         "--format=%h%x1f%(trailers:key=Requisitos,valueonly,separator=%x2C)%x1e")
    resultado = {}
    if codigo != 0:
        return resultado
    for registro in salida.split("\x1e"):
        if "\x1f" not in registro:
            continue
        # strip() sin argumentos también quitaría \x1f, que Python trata como espacio.
        sha, trailers = registro.strip("\r\n ").split("\x1f", 1)
        for req in re.findall(r"[A-Z]{2,4}-\d{2}", trailers):
            resultado.setdefault(req, []).append(sha)
    return resultado


def trazabilidad(_args):
    requisitos = leer_requisitos()
    specs = cargar(SPECS, "SPEC-*.md")
    informes = cargar(INFORMES, "VAL-*.md")
    commits = commits_por_requisito()
    conocidos = {r[0] for r in requisitos}
    for s in specs:
        desconocidos = [r for r in s.get("requisitos", []) if r not in conocidos]
        if desconocidos:
            print(f"Aviso: {s['id']} cita requisitos que no existen en docs/02: {', '.join(desconocidos)}",
                  file=sys.stderr)
    veredicto = {}
    for informe in sorted(informes, key=lambda d: d["id"]):
        veredicto[informe.get("spec")] = f"{informe['id']} ({informe.get('veredicto', '?')})"

    filas, cuenta = [], {}
    for req, prioridad, descripcion in requisitos:
        relacionadas = [s for s in specs if req in s.get("requisitos", [])]
        estados = {s.get("estado") for s in relacionadas}
        if "cerrada" in estados:
            estado = "cubierto"
        elif "abierta" in estados:
            estado = "en curso"
        elif "propuesta" in estados:
            estado = "planificado"
        else:
            estado = "sin cubrir"
        cuenta[(prioridad, estado)] = cuenta.get((prioridad, estado), 0) + 1
        shas = commits.get(req, [])
        texto_commits = f"{len(shas)}: " + ", ".join(f"`{c}`" for c in shas[:3]) if shas else "—"
        validaciones = ", ".join(veredicto[s["id"]] for s in relacionadas if s["id"] in veredicto) or "—"
        breve = descripcion if len(descripcion) <= 70 else descripcion[:67].rstrip() + "…"
        filas.append(f"| {req} | {prioridad} | {celda(breve)} | "
                     f"{', '.join(enlace(s) for s in relacionadas) or '—'} | {texto_commits} | "
                     f"{validaciones} | {estado} |")

    estados_req = ("sin cubrir", "planificado", "en curso", "cubierto")
    lineas = ["# Trazabilidad de requisitos", "", AVISO, "",
              f"Requisitos de `docs/02-especificaciones-v2.md`: {len(requisitos)}.", "",
              "| Prioridad | " + " | ".join(estados_req) + " |", "|---|" + "---|" * len(estados_req)]
    for prioridad in ("M", "S", "C"):
        lineas.append(f"| {prioridad} | " + " | ".join(str(cuenta.get((prioridad, e), 0)) for e in estados_req) + " |")
    lineas += ["", "| Requisito | P | Descripción | Specs | Commits | Validación | Estado |",
               "|---|---|---|---|---|---|---|", *filas]
    escribir(GESTION / "TRAZABILIDAD.md", lineas)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Gestión de specs de ESP-Riego")
    sub = parser.add_subparsers(dest="orden", required=True)
    p = sub.add_parser("nueva-spec", help="Crea una spec con el siguiente ID libre")
    p.add_argument("--titulo", required=True)
    p.add_argument("--fase", required=True)
    p.add_argument("--responsable", required=True)
    p.add_argument("--requisitos", default="")
    p.add_argument("--depende", default="")
    p.add_argument("--estado", default="abierta", choices=("propuesta", "abierta"))
    p.add_argument("--slug")
    p.set_defaults(funcion=nueva_spec)
    sub.add_parser("tablero", help="Regenera gestion/TABLERO.md").set_defaults(funcion=tablero)
    sub.add_parser("trazabilidad", help="Regenera gestion/TRAZABILIDAD.md").set_defaults(funcion=trazabilidad)
    args = parser.parse_args()
    args.funcion(args)


if __name__ == "__main__":
    main()
