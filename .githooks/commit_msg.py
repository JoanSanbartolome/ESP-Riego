"""Valida el mensaje de commit (hook commit-msg de git). Convenciones en gestion/README.md.

- Asunto: <tipo>(<ámbito>): <resumen>
- Trailers leídos con `git interpret-trailers --parse`, el mismo criterio que usa
  herramientas/gestion.py para la trazabilidad: solo cuentan los del bloque final.
- En ramas spec/SPEC-NNNN-*: `Spec: SPEC-NNNN` (el de la rama) y `Agente: <agente>`.
- `Requisitos`: cada ID tiene que existir en docs/02-especificaciones-v2.md.
- `Log`: cada ruta tiene que existir en el árbol de trabajo.
- En merges a main: tipo `merge`, `Spec`, `Validacion: VAL-NNNN-NN` y `Rama: spec/SPEC-NNNN-...`
  del mismo número, y la carpeta del TFG sin cambios (herramientas/integridad_tfg.py).
"""
import re
import subprocess
import sys
from pathlib import Path

TIPOS = "feat|fix|docs|spec|val|lib|fab|fw|chore|merge|refactor|test|revert"
ASUNTO = re.compile(rf"^({TIPOS})(\([^)]+\))?!?: \S")
AGENTES = ("coordinador", "ing-esquematicos", "ing-layout", "jr-conformidad", "ing-validacion")
ID_REQUISITO = re.compile(r"[A-Z]{2,4}-\d{2}")


def git(*args, entrada=None):
    resultado = subprocess.run(["git", *args], capture_output=True, text=True, input=entrada,
                               encoding="utf-8", errors="replace")
    return resultado.returncode, resultado.stdout.strip()


def leer_trailers(texto):
    _, salida = git("interpret-trailers", "--parse", entrada=texto)
    trailers = {}
    for linea in salida.splitlines():
        if ":" in linea:
            clave, valor = linea.split(":", 1)
            trailers.setdefault(clave.strip().lower(), valor.strip())
    return trailers


def requisitos_conocidos(raiz):
    doc = raiz / "docs" / "02-especificaciones-v2.md"
    if not doc.exists():
        return None
    patron = re.compile(r"^\|\s*([A-Z]{2,4}-\d{2})\s*\|\s*[MSC]\s*\|")
    return {m.group(1) for l in doc.read_text(encoding="utf-8").splitlines() if (m := patron.match(l))}


def main():
    texto = Path(sys.argv[1]).read_text(encoding="utf-8")
    texto = texto.split("# ------------------------ >8 ------------------------")[0]
    lineas = [l.rstrip() for l in texto.splitlines() if not l.startswith("#")]
    while lineas and not lineas[0]:
        lineas.pop(0)
    if not lineas:
        return 0  # git ya rechaza los mensajes vacíos
    asunto = lineas[0]
    if asunto.startswith(("fixup! ", "squash! ", "amend! ")):
        return 0
    _, raiz_texto = git("rev-parse", "--show-toplevel")
    raiz = Path(raiz_texto)
    trailers = leer_trailers("\n".join(lineas) + "\n")

    errores = []
    if not ASUNTO.match(asunto):
        errores.append(f"el asunto debe ser `<tipo>(<ámbito>): <resumen>` con tipo en {TIPOS.replace('|', ', ')}")
    spec = trailers.get("spec", "")
    if spec and not re.fullmatch(r"SPEC-\d{4}", spec):
        errores.append("`Spec:` debe tener la forma SPEC-NNNN")
    if "agente" in trailers and trailers["agente"] not in AGENTES:
        errores.append(f"`Agente:` debe ser uno de: {', '.join(AGENTES)}")
    if "requisitos" in trailers:
        ids = ID_REQUISITO.findall(trailers["requisitos"])
        conocidos = requisitos_conocidos(raiz)
        if not ids:
            errores.append("`Requisitos:` no contiene ningún ID (p. ej. ALI-01)")
        elif conocidos is not None and (desconocidos := [i for i in ids if i not in conocidos]):
            errores.append(f"`Requisitos:` con IDs que no existen en docs/02: {', '.join(desconocidos)}")
    if "log" in trailers:
        for ruta in (r.strip() for r in trailers["log"].split(",") if r.strip()):
            if not (raiz / ruta).exists():
                errores.append(f"`Log:` apunta a {ruta}, que no existe")

    _, rama = git("rev-parse", "--abbrev-ref", "HEAD")
    m = re.match(r"^spec/(SPEC-\d{4})", rama)
    if m:
        if spec != m.group(1):
            errores.append(f"en la rama {rama} hace falta el trailer `Spec: {m.group(1)}` en el bloque final")
        if "agente" not in trailers:
            errores.append("hace falta el trailer `Agente:` en el bloque final")
    es_merge = git("rev-parse", "-q", "--verify", "MERGE_HEAD")[0] == 0
    if es_merge and rama == "main":
        numero = spec.removeprefix("SPEC-")
        if not asunto.startswith("merge("):
            errores.append("un merge a main usa el asunto `merge(SPEC-NNNN): <título>`")
        if not spec:
            errores.append("un merge a main necesita el trailer `Spec: SPEC-NNNN`")
        if not re.fullmatch(rf"VAL-{numero}-\d{{2}}", trailers.get("validacion", "")):
            errores.append(f"un merge a main necesita `Validacion: VAL-{numero or 'NNNN'}-NN` de la misma spec")
        if not re.fullmatch(rf"spec/SPEC-{numero}-[\w.-]+", trailers.get("rama", "")):
            errores.append(f"un merge a main necesita `Rama: spec/SPEC-{numero or 'NNNN'}-<slug>`")
        integridad = subprocess.run([sys.executable, str(raiz / "herramientas" / "integridad_tfg.py"), "verificar"],
                                    capture_output=True, text=True, encoding="utf-8", errors="replace")
        if integridad.returncode != 0:
            errores.append("la carpeta del TFG ha cambiado desde su huella (herramientas/integridad_tfg.py):\n    "
                           + (integridad.stdout + integridad.stderr).strip().replace("\n", "\n    "))

    if errores:
        print("commit-msg: mensaje rechazado.\n  - " + "\n  - ".join(errores)
              + "\nConvenciones: gestion/README.md (Commits).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.stderr.reconfigure(encoding="utf-8")  # en Windows, la tubería usaría cp1252
    sys.exit(main())
