"""Guarda de los subagentes de ESP-Riego (hook PreToolUse).

Se declara en el frontmatter de cada agente:
    python "$CLAUDE_PROJECT_DIR/.claude/hooks/guardia.py" <agente>

Lee de stdin el JSON del hook y sale con código 2 (bloquea la acción y muestra el motivo
al agente) cuando:
- un comando usa git para escribir o usa gh (solo el coordinador gestiona git);
- Write/Edit/NotebookEdit apunta fuera de la zona del agente;
- un comando modifica la carpeta del proyecto del TFG o la configuración del sistema
  (.claude/agents, .claude/hooks, .claude/settings*, .githooks, .git).
Si la propia guarda falla, bloquea (falla en cerrado) y lo dice.
"""
import json
import os
import re
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

ZONAS = {
    "ing-esquematicos": ("hardware/v2/", "docs/diseno/", "firmware/"),
    "ing-layout": ("hardware/v2/", "docs/diseno/"),
    "jr-conformidad": ("hardware/", "fabricacion/"),
    "ing-validacion": ("gestion/informes/", "docs/validacion/"),
}
# Archivos que, aun estando en la zona, pertenecen a otro agente.
AJENOS = {
    "ing-esquematicos": (".kicad_pcb", ".kicad_dru"),
    "ing-layout": (".kicad_sch",),
}

GIT_LECTURA = {
    "status", "log", "diff", "show", "blame", "ls-files", "ls-tree", "rev-parse", "describe",
    "grep", "shortlog", "cat-file", "rev-list", "for-each-ref", "show-ref", "name-rev",
    "merge-base", "whatchanged", "count-objects", "check-ignore", "version", "help",
    "ls-remote", "show-branch", "cherry", "range-diff",
}
GIT_OPCIONES_CON_VALOR = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"}
BRANCH_ESCRITURA = {"-d", "-D", "--delete", "-m", "-M", "--move", "-c", "-C", "--copy", "-f",
                    "--force", "-u", "--set-upstream-to", "--unset-upstream", "--edit-description",
                    "-t", "--track", "--no-track"}
BRANCH_LISTADO = {"-l", "--list", "-a", "--all", "-r", "--remotes", "--contains", "--no-contains",
                  "--merged", "--no-merged", "--points-at"}
TAG_LISTADO = {"-l", "--list", "--contains", "--no-contains", "--merged", "--no-merged", "--points-at"}

ESCRITURA = {
    "rm", "rmdir", "del", "erase", "rd", "mv", "move", "ren", "rename", "tee", "touch", "truncate",
    "chmod", "attrib", "mkdir", "md", "remove-item", "move-item", "rename-item", "set-content",
    "add-content", "out-file", "new-item", "clear-content", "set-itemproperty", "clear-item",
    "ri", "mi", "rni", "ac", "ni",
}
COPIA = {"cp", "copy", "xcopy", "robocopy", "copy-item", "cpi"}
PREFIJOS = {"&", "sudo", "command", "exec", "time", "env", "nohup"}

TFG = re.compile(r"proyectos[\\/]+TFG\b", re.I)
SISTEMA = re.compile(r"\.claude[\\/]+(agents|hooks|settings)|\.githooks|(^|[\\/\s\"'])\.git([\\/]|$)", re.I)


def relativa(ruta_texto, cwd):
    """Ruta relativa al repositorio con '/' y en minúsculas, o None si está fuera."""
    ruta = Path(ruta_texto)
    if not ruta.is_absolute():
        ruta = Path(cwd) / ruta
    ruta = os.path.normcase(os.path.abspath(ruta))
    raiz = os.path.normcase(str(RAIZ))
    if os.path.commonpath([ruta, raiz]) != raiz:
        return None
    return os.path.relpath(ruta, raiz).replace("\\", "/")


def en_temporal(ruta_texto, cwd):
    ruta = Path(ruta_texto)
    if not ruta.is_absolute():
        ruta = Path(cwd) / ruta
    ruta = os.path.normcase(os.path.abspath(ruta))
    temporal = os.path.normcase(os.path.abspath(tempfile.gettempdir()))
    return os.path.commonpath([ruta, temporal]) == temporal


def motivo_escritura(agente, ruta_texto, cwd):
    if en_temporal(ruta_texto, cwd):
        return None
    rel = relativa(ruta_texto, cwd)
    if rel is None:
        return f"{ruta_texto} está fuera del repositorio"
    if rel.startswith(f".claude/agent-memory/{agente}/"):
        return None
    if re.fullmatch(rf"gestion/logs/spec-\d{{4}}/\d{{2}}-{re.escape(agente)}\.md", rel):
        return None
    zonas = ZONAS.get(agente, ())
    if any(rel.startswith(z) for z in zonas):
        if rel.endswith(AJENOS.get(agente, ())):
            return f"{rel} pertenece a otro agente"
        return None
    permitido = ", ".join(zonas) or "ninguna"
    return f"{rel} está fuera de tu zona ({permitido}, tu log y tu memoria)"


def segmentos(comando):
    return [s.strip() for s in re.split(r"&&|\|\||[;|\n]", comando) if s.strip()]


def trocear(segmento):
    tokens = re.findall(r"\"[^\"]*\"|'[^']*'|\S+", segmento)
    return [t[1:-1] if len(t) >= 2 and t[0] == t[-1] and t[0] in "\"'" else t for t in tokens]


def orden(tokens):
    """Devuelve (nombre del programa en minúsculas, argumentos)."""
    i = 0
    while i < len(tokens) and (tokens[i].lower() in PREFIJOS or re.fullmatch(r"\w+=\S*", tokens[i])):
        i += 1
    if i >= len(tokens):
        return "", []
    nombre = re.split(r"[\\/]", tokens[i])[-1].lower()
    return nombre.removesuffix(".exe"), tokens[i + 1:]


def motivo_git(args):
    i = 0
    while i < len(args) and args[i].startswith("-"):
        i += 2 if args[i] in GIT_OPCIONES_CON_VALOR else 1
    if i >= len(args):
        return None
    sub, resto = args[i], args[i + 1:]
    claves = {a.split("=")[0] for a in resto}
    posicionales = [a for a in resto if not a.startswith("-")]
    if sub in GIT_LECTURA:
        return None
    if sub == "branch" and not claves & BRANCH_ESCRITURA and (not posicionales or claves & BRANCH_LISTADO):
        return None
    if sub == "tag" and (not resto or claves & TAG_LISTADO or resto[0].startswith("-n")):
        return None
    if sub == "remote" and (not resto or resto[0] in ("-v", "--verbose", "show", "get-url")):
        return None
    if sub == "config" and claves & {"--get", "--get-all", "--get-regexp", "--list", "-l"}:
        return None
    if sub in ("stash", "notes") and resto[:1] in (["list"], ["show"]):
        return None
    if sub == "worktree" and resto[:1] == ["list"]:
        return None
    if sub == "reflog" and resto[:1] not in (["expire"], ["delete"]):
        return None
    return f"`git {sub}` modifica el repositorio: solo el coordinador usa git para escribir"


def destino_copia(nombre, args):
    if nombre in ("copy-item", "cpi"):
        for i, a in enumerate(args):
            if a.lower().startswith("-d") and i + 1 < len(args):
                return args[i + 1]
        posicionales = [a for a in args if not a.startswith("-")]
        return posicionales[1] if len(posicionales) > 1 else ""
    posicionales = [a for a in args if not a.startswith("-") and not re.fullmatch(r"/[A-Za-z]{1,3}(:\S*)?", a)]
    if nombre == "robocopy":
        return posicionales[1] if len(posicionales) > 1 else ""
    return posicionales[-1] if posicionales else ""


def motivo_comando(comando):
    for segmento in segmentos(comando):
        nombre, args = orden(trocear(segmento))
        if nombre == "git":
            motivo = motivo_git(args)
            if motivo:
                return motivo
        if nombre == "gh":
            return "`gh` queda reservado al coordinador"
        for patron, que in ((TFG, "la carpeta del TFG (solo lectura)"),
                            (SISTEMA, "la configuración del sistema (.claude, .githooks, .git)")):
            if not patron.search(segmento):
                continue
            if nombre in ESCRITURA or (nombre == "sed" and "-i" in args):
                return f"`{nombre}` modificaría {que}"
            if nombre in COPIA and patron.search(destino_copia(nombre, args)):
                return f"`{nombre}` copiaría dentro de {que}"
            for destino in re.findall(r">{1,2}\s*[\"']?([^\s\"']+)", segmento):
                if patron.search(destino):
                    return f"la redirección escribiría en {que}"
    return None


def main():
    agente = sys.argv[1] if len(sys.argv) > 1 else ""
    datos = json.loads(sys.stdin.read() or "{}")
    herramienta = datos.get("tool_name", "")
    entrada = datos.get("tool_input") or {}
    cwd = datos.get("cwd") or str(RAIZ)
    motivo = None
    if herramienta in ("Write", "Edit", "NotebookEdit"):
        ruta = entrada.get("file_path") or entrada.get("notebook_path") or ""
        motivo = motivo_escritura(agente, ruta, cwd)
        consejo = "Si hace falta ese cambio, pídeselo al coordinador en PENDIENTE."
    elif herramienta in ("Bash", "PowerShell"):
        motivo = motivo_comando(entrada.get("command", ""))
        consejo = "Indica en tu respuesta lo que necesitas y el coordinador lo hará."
    if motivo:
        print(f"BLOQUEADO por la guardia ({agente or 'agente desconocido'}): {motivo}. {consejo}",
              file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    sys.stderr.reconfigure(encoding="utf-8")  # en Windows, la tubería usaría cp1252
    try:
        main()
    except Exception as error:  # falla en cerrado: mejor bloquear que dejar pasar sin revisar
        print(f"BLOQUEADO: la guardia ha fallado ({error!r}). Avisa al coordinador.", file=sys.stderr)
        sys.exit(2)
