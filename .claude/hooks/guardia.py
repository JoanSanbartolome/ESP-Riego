"""Guarda de los subagentes de ESP-Riego (hook PreToolUse).

Se declara en el frontmatter de cada agente:
    python "$CLAUDE_PROJECT_DIR/.claude/hooks/guardia.py" <agente>

Lee de stdin el JSON del hook y sale con código 2 (bloquea la acción y muestra el motivo
al agente) cuando:
- un comando usa git para escribir, también dentro de bash -c, cmd /c, pwsh -Command,
  iex, xargs o $(...), o usa gh;
- Write/Edit/NotebookEdit o un comando de la terminal escriben fuera de la zona del
  agente. Las rutas se resuelven de verdad (relativas, ~, /c/..., siguiendo los cd), y
  la carpeta del TFG, la configuración del sistema y la auditoría quedan siempre fuera;
- un comando o una herramienta del MCP toca la carpeta del TFG de una forma que puede
  modificarla, incluido kicad-cli, que reescribe el .kicad_prl del proyecto que lee;
- una herramienta MCP de escritura apunta fuera de hardware/, fabricacion/, docs/diseno/,
  docs/validacion/, firmware/ o la carpeta temporal;
- ing-validacion usa una herramienta MCP que guardaría o modificaría el diseño.

Es una red de seguridad, no un sandbox: lo que escribe un script de Python o de
PowerShell no se puede analizar desde el comando. Lo que se escape lo detectan
herramientas/revisar_zonas.py, herramientas/integridad_tfg.py y la revisión del
coordinador. Qué herramientas MCP puede usar cada agente lo fija disallowedTools.

Cada bloqueo queda en la auditoría con `ok: false` y el motivo en `bloqueado`. Si la
propia guarda falla, bloquea (falla en cerrado) y lo dice.
"""
import json
import os
import re
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
TFG = Path(r"C:\Users\josan\proyectos\TFG")
TEMPORAL = Path(tempfile.gettempdir())

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
# Dónde puede escribir una herramienta MCP de escritura, sea cual sea el agente.
ZONAS_MCP = ("hardware/", "fabricacion/", "docs/diseno/", "docs/validacion/", "firmware/")

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

PREFIJOS = {"&", ".", "sudo", "command", "exec", "time", "env", "nohup", "call"}
CAMBIO_DIRECTORIO = {"cd", "chdir", "set-location", "sl", "pushd", "push-location"}
BORRA_O_CREA = {"rm", "rmdir", "del", "erase", "rd", "ri", "remove-item", "mkdir", "md", "ni",
                "new-item", "touch", "truncate", "tee", "mv", "move", "mi", "move-item", "ren",
                "rename", "rni", "rename-item", "clear-item", "cli", "install"}
CONTENIDO = {"set-content", "sc", "add-content", "ac", "clear-content", "clc", "out-file"}
COPIA = {"cp", "copy", "xcopy", "cpi", "copy-item", "robocopy"}
PERMISOS = {"chmod", "chown", "attrib", "icacls"}
# Órdenes de cmd.exe cuyas opciones empiezan por "/".
CMD_BARRA = {"del", "erase", "rd", "rmdir", "copy", "xcopy", "move", "ren", "md", "robocopy", "attrib"}
# Órdenes que no escriben aunque lleven -o (ls -o, grep -o...).
SOLO_LECTURA = {"ls", "dir", "gci", "get-childitem", "cat", "type", "gc", "get-content", "head",
                "tail", "less", "more", "grep", "egrep", "fgrep", "rg", "find", "findstr",
                "select-string", "sls", "wc", "uniq", "diff", "cmp", "md5sum", "sha1sum",
                "sha256sum", "get-filehash", "file", "stat", "du", "df", "echo", "printf",
                "write-output", "write-host", "test-path", "resolve-path", "measure-object",
                "where", "which", "tree", "pwd", "realpath", "dirname", "basename"}
INTERPRETES = {"python", "python3", "py", "node"}
# Parámetros de PowerShell que no llevan valor detrás.
INTERRUPTORES = {"-recurse", "-force", "-confirm", "-whatif", "-passthru", "-nonewline", "-append",
                 "-noclobber", "-container", "-verbose", "-debug", "-raw", "-wait", "-file",
                 "-directory", "-hidden", "-readonly", "-system", "-asbytestream", "-literal"}
# Parámetros cuyo valor no es una ruta.
NO_RUTA = {"-value", "-encoding", "-itemtype", "-type", "-filter", "-include", "-exclude",
           "-delimiter", "-stream", "-erroraction", "-ea", "-warningaction", "-outvariable",
           "-errorvariable", "-width", "-inputobject", "-depth"}
OPCIONES_SALIDA = {"-o", "--output", "-outfile", "--outfile", "--output-dir", "--outdir", "-od",
                   "--salida", "-outputdirectory"}
ESPECIALES = {"/dev/null", "nul", "$null", "/dev/stdout", "/dev/stderr", "con"}

ESCRITURA_CODIGO = re.compile(
    r"open\s*\([^)]*['\"][rbt]*[wxa+]|\.write(?:_text|_bytes)?\s*\(|"
    r"\b(?:os|shutil|pathlib)\.\w*(?:remove|unlink|rmdir|rmtree|rename|replace|move|copy|makedirs|mkdir|truncate|chmod)|"
    r"\.(?:unlink|rmdir|rename|replace|touch|mkdir|write_text|write_bytes)\s*\(|"
    r"\bfs\.(?:write|append|rm|unlink|rename|mkdir|copy|cp)", re.I)
DOTNET_ESCRITURA = re.compile(
    r"\[(?:system\.)?io\.(?:file|directory|fileinfo|directoryinfo)\]::\s*"
    r"(?:write|append|delete|move|copy|create|replace|setattributes|open|encrypt|decrypt)", re.I)
ESCRITURA_MCP = re.compile(
    r"^(?:add|align|annotate|assign|autoplace|autoroute|backannotate|batch_(?:add|connect|edit|move|set)|"
    r"clear|connect|copy|create|delete|discard|download|duplicate|edit|enrich|export|generate|group|"
    r"hierarchical_place|import|install|kicad_(?:gui_click|run|reload|pcb_snapshot)|launch|modify|move|"
    r"place|refill|register|reload|remove|rename|repair|replace|rotate|route|run_|save|set_|snap|"
    r"snapshot|sync|update|get_board_2d_view|get_schematic_view)")
EXTENSIONES_RUTA = (".kicad_pro", ".kicad_sch", ".kicad_pcb", ".kicad_sym", ".kicad_mod", ".kicad_dru",
                    ".kicad_prl", ".pretty", "lib-table", ".step", ".wrl", ".json", ".csv", ".pdf",
                    ".svg", ".zip", ".gbr", ".drl", ".dsn", ".ses", ".net", ".xml")


# --- Rutas ---------------------------------------------------------------------------

def normal(ruta):
    return os.path.normcase(os.path.abspath(ruta))


def dentro(ruta, carpeta):
    ruta, carpeta = normal(ruta), normal(carpeta).rstrip("\\/")
    return ruta == carpeta or ruta.startswith(carpeta + os.sep)


def resolver(texto, cwd):
    """Ruta absoluta normalizada de un token (Windows, Git Bash /c/..., ~, /tmp) o None."""
    t = (texto or "").strip()
    if not t or t.lower() in ESPECIALES or t.startswith("-") or "://" in t:
        return None
    m = re.match(r"^/([a-zA-Z])(/.*)?$", t)
    if m:
        t = f"{m.group(1)}:{m.group(2) or '/'}"
    elif t == "/tmp" or t.startswith("/tmp/"):
        t = str(TEMPORAL) + t[4:]
    t = re.sub(r"^(~|\$HOME|\$env:USERPROFILE|%USERPROFILE%)(?=[\\/]|$)",
               lambda _: str(Path.home()), t, flags=re.I)
    ruta = Path(t)
    if not ruta.is_absolute():
        ruta = Path(cwd) / ruta
    return normal(ruta)


def relativa(ruta):
    return os.path.relpath(ruta, normal(RAIZ)).replace("\\", "/").lower()


def motivo_destino(agente, ruta):
    """Por qué el agente no puede escribir en `ruta` (absoluta), o None si puede."""
    if dentro(ruta, TEMPORAL):
        return None
    if dentro(ruta, TFG):
        return "la carpeta del TFG es de solo lectura"
    if not dentro(ruta, RAIZ):
        return f"{ruta} está fuera del repositorio"
    rel = relativa(ruta)
    memoria = f".claude/agent-memory/{agente}"
    if rel == memoria or rel.startswith(memoria + "/"):
        return None
    if re.fullmatch(rf"gestion/logs/spec-\d{{4}}/\d{{2}}-{re.escape(agente)}\.md", rel):
        return None
    zonas = ZONAS.get(agente, ())
    if any(rel == z.rstrip("/") or rel.startswith(z) for z in zonas):
        if rel.endswith(AJENOS.get(agente, ())):
            return f"{rel} pertenece a otro agente"
        return None
    return f"{rel} está fuera de tu zona ({', '.join(zonas) or 'ninguna'}, tu log y tu memoria)"


# --- Troceado de comandos ------------------------------------------------------------

def partir(comando):
    """Segmentos separados por ; && || | & y saltos de línea, respetando las comillas."""
    segmentos, actual, comilla, i = [], [], None, 0
    while i < len(comando):
        c = comando[i]
        if comilla:
            actual.append(c)
            if c == comilla:
                comilla = None
        elif c in "\"'":
            comilla = c
            actual.append(c)
        elif comando.startswith(("&&", "||"), i):
            segmentos.append("".join(actual))
            actual = []
            i += 1
        elif c in ";|\n" or (c == "&" and 0 < i < len(comando) - 1 and comando[i - 1].isspace()
                              and comando[i + 1].isspace() and "".join(actual).strip()):
            segmentos.append("".join(actual))
            actual = []
        else:
            actual.append(c)
        i += 1
    segmentos.append("".join(actual))
    return [s.strip().strip("(){}").strip() for s in segmentos if s.strip().strip("(){}").strip()]


def trocear(segmento):
    tokens = re.findall(r"(?:\"[^\"]*\"|'[^']*'|[^\s\"'])+", segmento)
    return [re.sub(r"\"([^\"]*)\"|'([^']*)'",
                   lambda m: m.group(1) if m.group(1) is not None else m.group(2), t) for t in tokens]


def orden(tokens):
    """Devuelve (nombre del programa en minúsculas, argumentos)."""
    i = 0
    while i < len(tokens) and (tokens[i].lower() in PREFIJOS or re.fullmatch(r"\w+=\S*", tokens[i])):
        i += 1
    if i >= len(tokens):
        return "", []
    nombre = re.split(r"[\\/]", tokens[i].strip("\\/"))[-1].lower()
    return nombre.removesuffix(".exe"), tokens[i + 1:]


def es_powershell(nombre):
    return "-" in nombre or nombre in {"ri", "mi", "rni", "sc", "ac", "ni", "cpi", "clc", "cli", "sl", "gc", "gci"}


def sin_redirecciones(args):
    """Quita <, >, 2>&1... y sus destinos: las salidas se analizan aparte, con redirecciones()."""
    limpios, i = [], 0
    while i < len(args):
        m = re.fullmatch(r"(\d|\*)?(<{1,3}|>{1,2}\|?)(&\d)?(.*)", args[i])
        if m:
            i += 1 if (m.group(3) or m.group(4)) else 2
            continue
        limpios.append(args[i])
        i += 1
    return limpios


def separar(nombre, args):
    """Argumentos posicionales y valores de los parámetros con nombre."""
    args = sin_redirecciones(args)
    posicionales, nombrados, i = [], {}, 0
    powershell = es_powershell(nombre)
    while i < len(args):
        a, bajo = args[i], args[i].lower()
        if powershell and re.fullmatch(r"-[a-z][\w-]*", bajo):
            if bajo in INTERRUPTORES or i + 1 >= len(args):
                i += 1
                continue
            nombrados.setdefault(bajo, []).append(args[i + 1])
            i += 2
            continue
        if not powershell and a.startswith("-"):
            if (nombre == "sed" and bajo in ("-e", "-f")) or (nombre == "truncate" and bajo == "-s"):
                nombrados.setdefault(bajo, []).append(args[i + 1] if i + 1 < len(args) else "")
                i += 2
                continue
            if nombre in ("cp", "mv", "install") and bajo in ("-t", "--target-directory"):
                posicionales.append(args[i + 1] if i + 1 < len(args) else "")
                i += 2
                continue
            i += 1
            continue
        if nombre in CMD_BARRA and re.fullmatch(r"/[A-Za-z]{1,6}(:\S*)?", a):
            i += 1
            continue
        posicionales.append(a)
        i += 1
    return posicionales, nombrados


def valores(nombrados, claves):
    return [v for k in claves for v in nombrados.get(k, [])]


def redirecciones(segmento):
    """Destinos de >, >>, 2>, *> fuera de comillas (sin contar >&1 ni >&2)."""
    objetivos, comilla, i = [], None, 0
    while i < len(segmento):
        c = segmento[i]
        if comilla:
            if c == comilla:
                comilla = None
        elif c in "\"'":
            comilla = c
        elif c == ">":
            j = i + 1
            if j < len(segmento) and segmento[j] in ">|":
                j += 1
            if j < len(segmento) and segmento[j] == "&":
                i = j + 1
                continue
            m = re.match(r"\s*(\"[^\"]*\"|'[^']*'|[^\s;|&()<>]+)", segmento[j:])
            if m:
                objetivos.append(m.group(1).strip("\"'"))
                i = j + m.end()
                continue
        i += 1
    return objetivos


def destinos(nombre, args, segmento, cwd):
    """Rutas absolutas en las que escribiría (o borraría) el segmento."""
    rutas = redirecciones(segmento)
    posicionales, nombrados = separar(nombre, args)
    rutas_param = valores(nombrados, ("-path", "-literalpath", "-filepath", "-destination", "-name"))
    if nombre in BORRA_O_CREA:
        rutas += posicionales + rutas_param
    elif nombre in CONTENIDO:
        rutas += rutas_param or posicionales[:1]
    elif nombre in COPIA:
        destino = valores(nombrados, ("-destination",))
        if not destino:
            destino = posicionales[-1:] if nombre in ("cp", "copy", "xcopy") else posicionales[1:2]
        rutas += destino
        if nombre == "robocopy" and any(a.lower() in ("/mov", "/move", "/purge", "/mir") for a in args):
            rutas += posicionales[:1]
    elif nombre == "sed" and any(a == "--in-place" or re.fullmatch(r"-i\S*", a) for a in args):
        rutas += posicionales if "-e" in nombrados or "-f" in nombrados else posicionales[1:]
    elif nombre in PERMISOS:
        rutas += [p for p in posicionales if not re.fullmatch(r"[+-]?[0-7]{3,4}|[+-][a-zA-Z]+|[ugoa]*[+=-][rwxXst]+", p)]
    elif nombre not in SOLO_LECTURA:
        for i, a in enumerate(args):
            bajo = a.lower()
            if bajo in OPCIONES_SALIDA and i + 1 < len(args):
                rutas.append(args[i + 1])
            elif "=" in bajo and bajo.split("=", 1)[0] in OPCIONES_SALIDA:
                rutas.append(a.split("=", 1)[1])
    return [r for r in (resolver(x, cwd) for x in rutas) if r]


# --- Análisis --------------------------------------------------------------------------

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
        if "-o" in claves or "--output" in claves:
            return f"`git {sub} --output` escribe archivos"
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


def git_en_cualquier_parte(comando):
    """Red de seguridad: git en cualquier posición (envoltorios, comillas, $(...))."""
    for m in re.finditer(r"(?<![\w.-])git(?:\.exe)?[\"']?(?=\s)", comando, re.I):
        resto = re.split(r"[;&|\n)`]|\$\(", comando[m.end():], maxsplit=1)[0]
        motivo = motivo_git(trocear(resto))
        if motivo:
            return motivo
    return None


def orden_interior(nombre, args):
    """Orden que ejecuta un envoltorio ("" si no se puede analizar, None si no es envoltorio)."""
    bajos = [a.lower() for a in args]
    if nombre in ("bash", "sh", "zsh", "dash", "ksh") and "-c" in bajos:
        i = bajos.index("-c")
        return args[i + 1] if i + 1 < len(args) else ""
    if nombre == "cmd":
        for i, b in enumerate(bajos):
            if b in ("/c", "/k", "/r"):
                return " ".join(args[i + 1:])
        return None
    if nombre in ("pwsh", "powershell"):
        for i, b in enumerate(bajos):
            if b == "-c" or (len(b) >= 4 and "-command".startswith(b)):
                return " ".join(args[i + 1:])
            if b in ("-e", "-ec", "-en") or (len(b) >= 4 and "-encodedcommand".startswith(b)):
                return ""
        return None
    if nombre in ("iex", "invoke-expression"):
        return " ".join(a for a in args if a.lower() != "-command")
    if nombre == "xargs":
        i = 0
        while i < len(args) and args[i].startswith("-"):
            i += 2 if args[i] in ("-n", "-I", "-d", "-P", "-L", "-s", "-E") else 1
        return " ".join(args[i:])
    if nombre in ("start-process", "saps", "start", "wsl"):
        return " ".join(args)
    return None


def valor_de(args, opciones):
    for i, a in enumerate(args):
        if a in opciones and i + 1 < len(args):
            return args[i + 1]
    return None


def analizar(comando, agente, cwd, profundidad=0):
    """Motivo de bloqueo de un comando de Bash o PowerShell, o None."""
    if profundidad > 3:
        return "comando anidado demasiado profundo para analizarlo"
    motivo = git_en_cualquier_parte(comando)
    if motivo:
        return motivo
    if DOTNET_ESCRITURA.search(comando):
        return "las APIs de .NET que escriben archivos no se permiten: usa Write o los comandos estándar"
    interiores = re.findall(r"\$\(([^()]*(?:\([^()]*\)[^()]*)*)\)", comando) + re.findall(r"`([^`]+)`", comando)
    for interior in interiores:
        motivo = analizar(interior, agente, cwd, profundidad + 1)
        if motivo:
            return motivo
    for segmento in partir(comando):
        nombre, args = orden(trocear(segmento))
        if not nombre:
            continue
        if nombre in CAMBIO_DIRECTORIO:
            posicionales, nombrados = separar(nombre, args)
            destino = (valores(nombrados, ("-path", "-literalpath")) or posicionales or [str(Path.home())])[0]
            cwd = resolver(destino, cwd) or cwd
            continue
        if nombre == "gh":
            return "`gh` queda reservado al coordinador"
        if nombre == "git":
            motivo = motivo_git(args)
            if motivo:
                return motivo
            continue
        interior = orden_interior(nombre, args)
        if interior is not None:
            if not interior.strip():
                return f"`{nombre}` con una orden que no se puede analizar"
            motivo = analizar(interior, agente, cwd, profundidad + 1)
            if motivo:
                return motivo
            continue
        if nombre in INTERPRETES:
            codigo = valor_de(args, ("-c", "-e", "--eval"))
            if codigo and ESCRITURA_CODIGO.search(codigo):
                return f"`{nombre}` con código en línea que escribe archivos: usa Write o un script revisado"
        if nombre == "kicad-cli" or "verificar.py" in segmento:
            rutas = [r for r in (resolver(a, cwd) for a in args) if r]
            if dentro(cwd, TFG) or any(dentro(r, TFG) for r in rutas):
                return "kicad-cli reescribe el .kicad_prl del proyecto que lee: trabaja sobre una copia del TFG"
        for destino in destinos(nombre, args, segmento, cwd):
            motivo = motivo_destino(agente, destino)
            if motivo:
                return f"`{nombre}` escribiría donde no puedes: {motivo}"
    return None


def cadenas(valor):
    if isinstance(valor, str):
        yield valor
    elif isinstance(valor, dict):
        for v in valor.values():
            yield from cadenas(v)
    elif isinstance(valor, list):
        for v in valor:
            yield from cadenas(v)


def parece_ruta(texto):
    t = texto.strip().lower()
    return ("://" not in t and len(t) < 400
            and ("/" in t or "\\" in t or t.startswith(("~", ".")) or t.endswith(EXTENSIONES_RUTA)))


def motivo_mcp(agente, herramienta, entrada, cwd):
    nombre = herramienta.split("__")[-1]
    rutas = [r for r in (resolver(v, cwd) for v in cadenas(entrada) if parece_ruta(v)) if r]
    if any(dentro(r, TFG) for r in rutas):
        return "el MCP no puede abrir ni escribir nada dentro de la carpeta del TFG: copia antes el proyecto a hardware/"
    if agente == "ing-validacion":
        if nombre == "close_project":
            return None if entrada.get("save") is False else "close_project tiene que llevar save: false"
        if nombre == "lint_schematic_cosmetic" and entrada.get("dryRun") is not True:
            return "lint_schematic_cosmetic sin dryRun: true modificaría el esquema"
        if nombre == "lint_offgrid" and entrada.get("fix"):
            return "lint_offgrid con fix modificaría el esquema"
        if ESCRITURA_MCP.match(nombre):
            return f"{nombre} modifica el diseño o escribe archivos"
    if ESCRITURA_MCP.match(nombre):
        for ruta in rutas:
            if dentro(ruta, TEMPORAL):
                continue
            if not dentro(ruta, RAIZ):
                return f"{nombre} escribiría fuera del repositorio ({ruta})"
            if not relativa(ruta).startswith(ZONAS_MCP):
                return f"{nombre} escribiría en {relativa(ruta)}, fuera de {', '.join(ZONAS_MCP)}"
    return None


def bloquear(agente, datos, motivo, consejo):
    try:  # los bloqueos no llegan a PostToolUse: se registran aquí
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import auditoria
        auditoria.registrar(agente or "?", datos, ok=False, bloqueado=motivo)
    except Exception:
        pass  # el bloqueo no depende de que el registro funcione
    print(f"BLOQUEADO por la guardia ({agente or 'agente desconocido'}): {motivo}. {consejo}",
          file=sys.stderr)
    sys.exit(2)


def main():
    agente = sys.argv[1] if len(sys.argv) > 1 else ""
    texto = sys.stdin.read()
    if not texto.strip():
        bloquear(agente, {}, "la guarda no ha recibido datos del hook", "Avisa al coordinador.")
    datos = json.loads(texto)
    herramienta = datos.get("tool_name", "")
    entrada = datos.get("tool_input") or {}
    cwd = datos.get("cwd") or str(RAIZ)
    motivo, consejo = None, "Indica en tu respuesta lo que necesitas y el coordinador lo hará."
    if herramienta in ("Write", "Edit", "NotebookEdit"):
        ruta = entrada.get("file_path") or entrada.get("notebook_path") or ""
        destino = resolver(ruta, cwd)
        motivo = motivo_destino(agente, destino) if destino else "escritura sin ruta"
        consejo = "Si hace falta ese cambio, pídeselo al coordinador en PENDIENTE."
    elif herramienta in ("Bash", "PowerShell"):
        motivo = analizar(entrada.get("command", ""), agente, cwd)
        consejo += " Para buscar texto, usa la herramienta Grep."
    elif herramienta.startswith("mcp__"):
        motivo = motivo_mcp(agente, herramienta, entrada, cwd)
    if motivo:
        bloquear(agente, datos, motivo, consejo)


if __name__ == "__main__":
    sys.stderr.reconfigure(encoding="utf-8")  # en Windows, la tubería usaría cp1252
    try:
        main()
    except SystemExit:
        raise
    except Exception as error:  # falla en cerrado: mejor bloquear que dejar pasar sin revisar
        print(f"BLOQUEADO: la guardia ha fallado ({error!r}). Avisa al coordinador.", file=sys.stderr)
        sys.exit(2)
