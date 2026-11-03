"""Valida el mensaje de commit (hook commit-msg de git). Convenciones en gestion/README.md.

- Asunto: <tipo>(<ámbito>): <resumen>
- En ramas spec/SPEC-NNNN-*: trailers `Spec: SPEC-NNNN` (el de la rama) y `Agente: <agente>`.
- En merges a main: tipo `merge`, trailers `Spec` y `Validacion`.
"""
import re
import subprocess
import sys
from pathlib import Path

TIPOS = "feat|fix|docs|spec|val|lib|fab|fw|chore|merge|refactor|test|revert"
ASUNTO = re.compile(rf"^({TIPOS})(\([^)]+\))?!?: \S")
AGENTES = ("coordinador", "ing-esquematicos", "ing-layout", "jr-conformidad", "ing-validacion")


def git(*args):
    resultado = subprocess.run(["git", *args], capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
    return resultado.returncode, resultado.stdout.strip()


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

    trailers = {}
    for linea in lineas[1:]:
        m = re.match(r"^([A-Za-z][A-Za-z-]*):\s*(.+)$", linea.strip())
        if m:
            trailers.setdefault(m.group(1).lower(), m.group(2).strip())

    errores = []
    if not ASUNTO.match(asunto):
        errores.append(f"el asunto debe ser `<tipo>(<ámbito>): <resumen>` con tipo en {TIPOS.replace('|', ', ')}")
    if "spec" in trailers and not re.fullmatch(r"SPEC-\d{4}", trailers["spec"]):
        errores.append("`Spec:` debe tener la forma SPEC-NNNN")
    if "agente" in trailers and trailers["agente"] not in AGENTES:
        errores.append(f"`Agente:` debe ser uno de: {', '.join(AGENTES)}")

    _, rama = git("rev-parse", "--abbrev-ref", "HEAD")
    m = re.match(r"^spec/(SPEC-\d{4})", rama)
    if m:
        if trailers.get("spec") != m.group(1):
            errores.append(f"en la rama {rama} hace falta el trailer `Spec: {m.group(1)}`")
        if "agente" not in trailers:
            errores.append("hace falta el trailer `Agente:`")
    es_merge = git("rev-parse", "-q", "--verify", "MERGE_HEAD")[0] == 0
    if es_merge and rama == "main":
        if not asunto.startswith("merge("):
            errores.append("un merge a main usa el asunto `merge(SPEC-NNNN): <título>`")
        if "spec" not in trailers:
            errores.append("un merge a main necesita el trailer `Spec: SPEC-NNNN`")
        if "validacion" not in trailers:
            errores.append("un merge a main necesita el trailer `Validacion: VAL-NNNN-NN`")

    if errores:
        print("commit-msg: mensaje rechazado.\n  - " + "\n  - ".join(errores)
              + "\nConvenciones: gestion/README.md (Commits).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.stderr.reconfigure(encoding="utf-8")  # en Windows, la tubería usaría cp1252
    sys.exit(main())
