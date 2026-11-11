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
- un comando toca la carpeta del TFG (por ruta, por cd o en una tubería) y alguna de sus
  partes no está en la lista blanca de lectura: lo desconocido se bloquea;
- una herramienta del MCP recibe una ruta dentro del TFG (el MCP y kicad-cli reescriben
  archivos del proyecto que leen);
- un argumento de destino de una herramienta MCP de escritura apunta fuera de hardware/,
  fabricacion/, docs/diseno/, docs/validacion/, firmware/ o la carpeta temporal;
- ing-validacion usa una herramienta MCP que guardaría o modificaría el diseño.

Para resolver las rutas, sustituye en orden las variables que se asignan en el propio
comando (S=/ruta; mkdir $S/x) y no trata como órdenes el cuerpo de un heredoc que reciben
cat, tee o un intérprete, salvo que la línea lo pase a una shell o que, sin comillas en el
delimitador, lleve $(...) o `...`. El código en línea de python o node no se analiza,
igual que el de un script, salvo que el comando toque el TFG (DEC-0009, M9).

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
# GUARDIA_TEMPORAL cambia la carpeta temporal exenta: solo para probar las zonas en una copia
# del repositorio que está dentro de la carpeta temporal (herramientas/pruebas/test_gestion.py).
TEMPORAL = Path(os.environ.get("GUARDIA_TEMPORAL") or tempfile.gettempdir())

ZONAS = {
    "ing-diseno": ("hardware/", "docs/diseno/", "firmware/", "herramientas/kicad/"),
    "jr-conformidad": ("hardware/", "fabricacion/"),
    "ing-validacion": ("gestion/informes/", "docs/validacion/"),
}
# Carpetas que, aun estando en la zona, el agente no toca.
EXCLUIDAS = {
    "ing-diseno": ("hardware/v1-tfg/",),
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

PREFIJOS = {"&", ".", "sudo", "command", "exec", "time", "env", "nohup", "call",
            # palabras de control de la shell: la orden es lo que viene detrás
            "do", "then", "else", "elif", "if", "while", "until", "!"}
SHELLS = {"bash", "sh", "zsh", "dash", "ksh", "cmd", "pwsh", "powershell"}
# <<EOF, <<-EOF, <<'EOF', <<"EOF" y <<\EOF, con el delimitador completo (FIN-DE-TEXTO, EOF.1).
HEREDOC = re.compile(r"<<-?[ \t]*(?:'([^'\n]+)'|\"([^\"\n]+)\"|(\\?)([^\s;&|<>()'\"\\]+))")
# El cuerpo de un heredoc es texto solo para estos programas; para cualquier otro se analiza.
TEXTO_HEREDOC = {"cat", "tee", "python", "python3", "py", "node"}
# Órdenes que ejecutan lo que reciben por la entrada.
EJECUTAN_ENTRADA = SHELLS | {"source", "eval", "xargs", "iex", "invoke-expression"}
# Fin de una cadena de &&: ; salto de línea, ||, y | o & sueltos (no 2>&1 ni &>).
ROMPE_CADENA = re.compile(r";|\n|\|\||(?<![&>])&(?![&>])|(?<!\|)\|(?!\|)")
VALOR = r"(\"[^\"\n]*\"|'[^'\n]*'|[^\s;&|\n=\"']+)"
# S=/ruta (bash, sin espacios) y $S = 'C:\ruta' (PowerShell)
ASIGNACION = re.compile(r"(?:^|[;&|\n(]\s*|\bexport\s+)([A-Za-z_]\w*)=" + VALOR
                        + r"|(?:^|[;\n({]\s*)\$([A-Za-z_]\w*)\s*=\s*" + VALOR)
CARPETA_TEMPORAL = re.compile(r"^(\$\{?(?:TEMP|TMP|TMPDIR)\}?|\$env:(?:TEMP|TMP)|%(?:TEMP|TMP)%)(?=[\\/]|$)", re.I)
CAMBIO_DIRECTORIO = {"cd", "chdir", "set-location", "sl", "pushd", "push-location"}
BORRA_O_CREA = {"rm", "rmdir", "del", "erase", "rd", "ri", "remove-item", "mkdir", "md", "ni",
                "new-item", "touch", "truncate", "tee", "mv", "move", "mi", "move-item", "ren",
                "rename", "rni", "rename-item", "clear-item", "cli", "install", "ln", "mklink",
                "shred", "unlink", "patch"}
CONTENIDO = {"set-content", "sc", "add-content", "ac", "clear-content", "clc", "out-file",
             "export-csv", "epcsv", "export-clixml", "tee-object"}
# Órdenes permitidas en un comando que toca la carpeta del TFG: solo leen, o copian desde
# el TFG hacia fuera. Cualquier otra orden en ese comando se bloquea.
LECTURA_TFG = {"ls", "dir", "gci", "get-childitem", "cat", "type", "gc", "get-content", "head", "tail",
               "less", "more", "grep", "egrep", "fgrep", "rg", "findstr", "select-string", "sls", "wc",
               "uniq", "diff", "cmp", "md5sum", "sha1sum", "sha256sum", "get-filehash", "file", "stat",
               "du", "test-path", "resolve-path", "measure-object", "tree", "pwd", "realpath", "dirname",
               "basename", "echo", "printf", "write-output", "write-host", "get-item", "gi", "sort",
               "sort-object", "select-object", "select", "where-object", "where", "format-table", "ft",
               "format-list", "fl", "find", "popd", "pop-location"}
TFG_TEXTO = re.compile(r"(?:proyectos|proyec~\d)[\\/]+tfg(?![\w-])", re.I)
GIT_CONFIG_PELIGROSA = re.compile(r"pager|external|textconv|editor|sshcommand|fsmonitor|hookspath|^alias\.|"
                                  r"askpass|credential|gpg\.program|^filter\.|difftool|mergetool", re.I)
# Scripts del repositorio que escriben fuera de las zonas de los agentes.
SCRIPTS_REPO = {
    "integridad_tfg.py": {"crear": "gestion/tfg-manifiesto.json"},
    "gestion.py": {"tablero": "gestion/TABLERO.md", "trazabilidad": "gestion/TRAZABILIDAD.md",
                   "nueva-spec": "gestion/specs/nueva.md"},
}
# Argumentos de las herramientas MCP que nombran el archivo o la carpeta donde escriben.
CLAVES_DESTINO = {"schematicpath", "boardpath", "projectpath", "filename", "path", "output", "outputpath",
                  "outputdir", "outputdirectory", "outdir", "outputfile", "destination", "destinationpath",
                  "destpath", "destdir", "targetpath", "targetdir", "targetlibrarypath", "tablepath",
                  "librarypath", "footprintpath", "symbolpath", "file", "filepath", "savepath", "dir",
                  "directory", "projectdir", "newpath"}
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
                "where", "which", "tree", "pwd", "realpath", "dirname", "basename",
                "[", "[[", "test"}
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

DOTNET_ESCRITURA = re.compile(
    r"\[(?:system\.)?io\.(?:file|directory|fileinfo|directoryinfo)\]::\s*"
    r"(?:write|append|delete|move|copy|create|replace|setattributes|open|encrypt|decrypt)", re.I)
ESCRITURA_MCP = re.compile(
    r"^(?:add|align|annotate|assign|autoplace|autoroute|backannotate|batch_(?:add|connect|edit|move|set)|"
    r"clear|connect|copy|create|delete|discard|download|duplicate|edit|enrich|export|generate|group|"
    r"hierarchical_place|import|install|kicad_(?:gui_click|run|reload|pcb_snapshot)|launch|modify|move|"
    r"place|refill|register|reload|remove|rename|repair|replace|rotate|route|run_|save|set_|snap|"
    r"snapshot|sync|update|lint_|get_board_2d_view|get_schematic_view)")
EXTENSIONES_RUTA = (".kicad_pro", ".kicad_sch", ".kicad_pcb", ".kicad_sym", ".kicad_mod", ".kicad_dru",
                    ".kicad_prl", ".pretty", "lib-table", ".step", ".wrl", ".json", ".csv", ".pdf",
                    ".svg", ".zip", ".gbr", ".drl", ".dsn", ".ses", ".net", ".xml")


# --- Rutas ---------------------------------------------------------------------------

def normal(ruta):
    # realpath sigue enlaces y uniones, y en Windows deshace los nombres cortos 8.3 (PROYEC~1)
    return os.path.normcase(os.path.realpath(ruta))


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
    t = CARPETA_TEMPORAL.sub(lambda _: str(TEMPORAL), t)
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
    # Validación no escribe parte: su registro es el informe.
    if agente != "ing-validacion" and re.fullmatch(
            rf"gestion/logs/spec-\d{{4}}/\d{{2}}-{re.escape(agente)}\.md", rel):
        return None
    zonas = ZONAS.get(agente, ())
    if any(rel == z.rstrip("/") or rel.startswith(z) for z in zonas):
        if any(rel == x.rstrip("/") or rel.startswith(x) for x in EXCLUIDAS.get(agente, ())):
            return f"{rel} es de solo lectura para ti"
        return None
    propio = "tu memoria" if agente == "ing-validacion" else "tu parte y tu memoria"
    return f"{rel} está fuera de tu zona ({', '.join(zonas) or 'ninguna'}, {propio})"


# --- Troceado de comandos ------------------------------------------------------------

def heredocs_de(linea, comilla):
    """Heredocs que abre una línea fuera de comillas y de comentarios, [(posición, delimitador,
    literal)], y la comilla que queda abierta al acabar la línea. `literal`: el delimitador va
    entre comillas, así que la shell no expande $(...) ni `...` dentro del cuerpo."""
    abiertos, i = [], 0
    while i < len(linea):
        c = linea[i]
        if comilla:
            if c == "\\" and comilla == '"':
                i += 1
            elif c == comilla:
                comilla = None
        elif c == "\\":
            i += 1
        elif c in "\"'":
            comilla = c
        elif c == "#" and (i == 0 or linea[i - 1].isspace()):
            break
        elif linea.startswith("<<<", i):
            i += 2
        elif linea.startswith("<<", i):
            m = HEREDOC.match(linea, i)
            if m:
                abiertos.append((i, m.group(1) or m.group(2) or m.group(4),
                                 bool(m.group(1) or m.group(2) or m.group(3))))
                i = m.end() - 1
            else:
                i += 1
        i += 1
    return abiertos, comilla


def heredoc_es_texto(linea, posicion):
    """¿El heredoc que se abre en `posicion` es texto para un programa que no lo ejecuta?
    Lo es si lo recibe cat, tee o un intérprete y ningún tramo de la línea se lo pasa a una
    shell (`cat <<EOF | bash`, `source /dev/stdin <<EOF`)."""
    antes = partir(linea[:posicion])
    if not antes or orden(trocear(antes[-1]))[0] not in TEXTO_HEREDOC:
        return False
    for segmento in partir(linea):
        tokens = trocear(segmento)
        if tokens and (tokens[0] == "." or orden(tokens)[0] in EJECUTAN_ENTRADA):
            return False
    return True


def sin_heredocs(comando):
    """Quita el cuerpo de los heredocs (<<EOF ... EOF) que son texto o código para otro
    programa (cat, tee, python), no órdenes. La línea que lo abre se conserva, con sus
    redirecciones. Se conserva también, para analizarlo: el cuerpo que va a una shell o a un
    programa que no se conoce; las líneas con $(...) o `...` de un heredoc sin comillas, que
    la shell ejecuta; y todo lo que sigue a un << que no llega a cerrarse."""
    lineas, salida, comilla, i = comando.split("\n"), [], None, 0
    while i < len(lineas):
        linea = lineas[i]
        salida.append(linea)
        i += 1
        abiertos, comilla = heredocs_de(linea, comilla)
        for posicion, delimitador, literal in abiertos:
            fin = next((j for j in range(i, len(lineas)) if lineas[j].strip() == delimitador), None)
            if fin is None:
                break
            cuerpo = lineas[i:fin]
            if not heredoc_es_texto(linea, posicion):
                salida += cuerpo
            elif not literal:
                salida += [l for l in cuerpo if "$(" in l or "`" in l]
            i = fin + 1
    return "\n".join(salida)


def sustituir(texto, valores):
    """Cambia ${VAR} y $VAR por su valor, salvo donde $VAR es el destino de una asignación."""
    return re.sub(r"\$\{(\w+)\}|\$(\w+)(?!\w)(?!\s*=(?!=))",
                  lambda m: valores.get(m.group(1) or m.group(2), m.group(0)), texto)


def expandir(comando):
    """Sustituye, en orden, las variables que se asignan en el propio comando (S=/ruta; mkdir
    $S/x · $S = 'C:\\ruta'; New-Item $S), para resolver de verdad las rutas que las usan: cada
    $VAR toma el valor vigente en ese punto. Las que no se asignan aquí, o salen de $(...), se
    dejan como están. Una asignación tras &&, || o | puede no ejecutarse: solo vale hasta que
    acaba su cadena de && (A && S=/ruta && mkdir $S)."""
    valores, dudosas, salida, pos = {}, set(), [], 0

    def tramo(texto):
        corte = ROMPE_CADENA.search(texto) if dudosas else None
        if not corte:
            return sustituir(texto, valores)
        cabeza = sustituir(texto[:corte.start()], valores)
        for nombre in dudosas:
            valores.pop(nombre, None)
        dudosas.clear()
        return cabeza + sustituir(texto[corte.start():], valores)

    for m in ASIGNACION.finditer(comando):
        nombre, valor = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
        inicio = m.start(1) if m.group(1) else m.start(3) - 1
        salida.append(tramo(comando[pos:inicio]))
        salida.append(sustituir(comando[inicio:m.end()], valores))
        pos = m.end()
        previo = re.sub(r"\bexport\s*$", "", comando[:inicio]).rstrip()
        valor = valor.strip("\"'")
        if "$(" in valor or "`" in valor:
            valores.pop(nombre, None)
            dudosas.discard(nombre)
            continue
        valores[nombre] = sustituir(valor, valores)
        (dudosas.add if previo.endswith(("&", "|")) else dudosas.discard)(nombre)
    salida.append(tramo(comando[pos:]))
    return "".join(salida)


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
    """Rutas absolutas en las que escribiría (o borraría) el segmento, sin contar las redirecciones."""
    rutas = []
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
    elif nombre == "find" and any(a in ("-delete", "-exec", "-execdir", "-ok", "-okdir") for a in args):
        ejecutadas = [re.split(r"[\\/]", args[i + 1])[-1].lower() for i, a in enumerate(args[:-1])
                      if a in ("-exec", "-execdir", "-ok", "-okdir")]
        # uniq y tree están en SOLO_LECTURA, pero escriben con un segundo argumento o con -o
        if "-delete" in args or any(e not in SOLO_LECTURA or e in ("uniq", "tree") for e in ejecutadas):
            for a in args:  # las carpetas de partida van antes de la expresión
                if a.startswith(("-", "(", "!")):
                    break
                rutas.append(a)
    elif nombre == "rsync":
        rutas += posicionales[-1:]
    elif nombre in ("perl", "awk", "gawk") and any(re.fullmatch(r"-\w*i\w*", a) for a in args):
        rutas += posicionales if nombre == "perl" else posicionales[1:]
    elif nombre == "dd":
        rutas += [a[3:] for a in args if a.startswith("of=")]
    elif nombre in ("tar", "7z", "unzip", "expand-archive"):
        lista = (nombre == "tar" and any(re.fullmatch(r"-\w*t\w*|--list", a) for a in args)) or \
                (nombre == "7z" and args[:1] == ["l"]) or (nombre == "unzip" and "-l" in args)
        if not lista:
            rutas.append(destino_archivo(nombre, args, cwd))
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
        if args[i] in ("-c", "--config-env") and i + 1 < len(args):
            if GIT_CONFIG_PELIGROSA.search(args[i + 1].split("=")[0]):
                return f"`git -c {args[i + 1]}` puede ejecutar órdenes arbitrarias"
        i += 2 if args[i] in GIT_OPCIONES_CON_VALOR else 1
    if i >= len(args):
        return None
    sub, resto = args[i], args[i + 1:]
    claves = {a.split("=")[0] for a in resto}
    posicionales = [a for a in resto if not a.startswith("-")]
    if sub in GIT_LECTURA:
        if "-o" in claves or "--output" in claves:
            return f"`git {sub} --output` escribe archivos"
        if sub == "grep" and any(a.startswith(("-O", "--open-files-in-pager")) for a in resto):
            return "`git grep -O` ejecuta una orden arbitraria"
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
    """Red de seguridad: git en cualquier posición (envoltorios, comillas, $(...)), también
    con las ofuscaciones simples de bash (g\\it, $'git', "git")."""
    simplificado = re.sub(r"[\"'$]|\\(?=\w)", "", comando)
    for texto in (comando, simplificado):
        for m in re.finditer(r"(?<![\w.-])git(?:\.exe)?[\"']?(?=\s)", texto, re.I):
            resto = re.split(r"[;&|\n)`]|\$\(", texto[m.end():], maxsplit=1)[0]
            motivo = motivo_git(trocear(resto))
            if motivo:
                return motivo
    return None


def candidatas(token):
    """Partes de un token que pueden ser rutas: el token, lo que va tras '=' y tras -o (7z -oDIR)."""
    partes = [token]
    if "=" in token:
        partes.append(token.split("=", 1)[1])
    if re.match(r"-o\S", token):
        partes.append(token[2:])
    return partes


def toca_tfg(comando, segmentos, cwd):
    """¿Alguna parte del comando apunta a la carpeta del TFG (por ruta, por cd o por redirección)?"""
    if TFG_TEXTO.search(comando):
        return True
    for segmento in segmentos:
        nombre, args = orden(trocear(segmento))
        if dentro(cwd, TFG):
            return True
        for token in args + redirecciones(segmento):
            for parte in candidatas(token):
                ruta = resolver(parte, cwd)
                if ruta and dentro(ruta, TFG):
                    return True
        if nombre in CAMBIO_DIRECTORIO:
            posicionales, nombrados = separar(nombre, args)
            destino = (valores(nombrados, ("-path", "-literalpath")) or posicionales or [str(Path.home())])[0]
            cwd = resolver(destino, cwd) or cwd
    return dentro(cwd, TFG)


def destino_archivo(nombre, args, cwd):
    """Carpeta de extracción de tar, 7z, unzip o Expand-Archive (o el cwd si no se indica)."""
    posicionales, nombrados = separar(nombre, args)
    if nombre == "tar":
        destino = valor_de(args, ("-C", "--directory"))
    elif nombre == "7z":
        destino = next((a[2:] for a in args if re.match(r"-o\S", a)), None)
    elif nombre == "unzip":
        destino = valor_de(args, ("-d",))
    else:
        destino = (valores(nombrados, ("-destinationpath",)) or posicionales[1:2] or [None])[0]
    return resolver(destino, cwd) if destino else normal(cwd)


def motivo_tfg(segmentos, cwd):
    """Con un comando que toca el TFG, cada parte tiene que ser de lectura o copiar hacia fuera."""
    for segmento in segmentos:
        nombre, args = orden(trocear(segmento))
        if not nombre:
            continue
        if any(marca in segmento for marca in ("{", "$(", "`")):
            return "un comando que toca la carpeta del TFG no puede llevar bloques de código"
        if nombre in CAMBIO_DIRECTORIO:
            posicionales, nombrados = separar(nombre, args)
            destino = (valores(nombrados, ("-path", "-literalpath")) or posicionales or [str(Path.home())])[0]
            cwd = resolver(destino, cwd) or cwd
            continue
        if nombre in LECTURA_TFG:
            if nombre == "find" and any(a in ("-delete", "-exec", "-execdir", "-ok", "-okdir", "-fprint",
                                              "-fprint0", "-fprintf", "-fls") for a in args):
                return "`find` con acciones que modifican, en un comando que toca la carpeta del TFG"
            if nombre in ("sort", "sort-object") and any(a.startswith(("-o", "--output")) for a in args):
                return "`sort -o` escribe archivos, en un comando que toca la carpeta del TFG"
            continue
        if nombre in COPIA:
            if nombre == "robocopy" and any(a.lower() in ("/mov", "/move", "/purge", "/mir") for a in args):
                return "`robocopy` con /MOV, /MOVE, /PURGE o /MIR modificaría la carpeta del TFG"
            if any(dentro(r, TFG) for r in destinos(nombre, args, segmento, cwd)):
                return f"`{nombre}` copiaría dentro de la carpeta del TFG"
            continue
        if nombre in ("tar", "7z", "unzip", "expand-archive"):
            solo_lista = (nombre == "tar" and any(re.fullmatch(r"-\w*t\w*|--list", a) for a in args)) or \
                         (nombre == "7z" and args[:1] == ["l"]) or (nombre == "unzip" and "-l" in args)
            if solo_lista or not dentro(destino_archivo(nombre, args, cwd), TFG):
                continue
            return f"`{nombre}` extraería dentro de la carpeta del TFG"
        return (f"`{nombre}` no es una orden de lectura y el comando toca la carpeta del TFG "
                "(solo se permite leer o copiar desde el TFG hacia fuera)")
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
    original = comando
    if profundidad == 0:
        comando = expandir(comando)
    motivo = git_en_cualquier_parte(comando)  # con los heredocs: git se busca en todo el texto
    if motivo:
        return motivo
    if DOTNET_ESCRITURA.search(comando):
        return "las APIs de .NET que escriben archivos no se permiten: usa Write o los comandos estándar"
    comando = sin_heredocs(comando)
    interiores = re.findall(r"\$\(([^()]*(?:\([^()]*\)[^()]*)*)\)", comando) + re.findall(r"`([^`]+)`", comando)
    for interior in interiores:
        motivo = analizar(interior, agente, cwd, profundidad + 1)
        if motivo:
            return motivo
    segmentos = partir(comando)
    if TFG_TEXTO.search(original) or toca_tfg(comando, segmentos, cwd):
        motivo = motivo_tfg(segmentos, cwd)
        if motivo:
            return motivo
    for segmento in segmentos:
        nombre, args = orden(trocear(segmento))
        if not nombre:
            continue
        for destino in redirecciones(segmento):  # antes que nada: valen para cualquier orden
            ruta = resolver(destino, cwd)
            motivo = motivo_destino(agente, ruta) if ruta else None
            if motivo:
                return f"la redirección escribiría donde no puedes: {motivo}"
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
            # El código en línea (-c, heredoc) no se analiza, igual que el de un script: si el
            # comando toca el TFG ya se ha bloqueado arriba, y lo demás lo ve revisar_zonas.py.
            posicionales = [a for a in args if not a.startswith("-")]
            if posicionales:
                escrituras = SCRIPTS_REPO.get(re.split(r"[\\/]", posicionales[0])[-1].lower(), {})
                destino = escrituras.get(posicionales[1].lower()) if len(posicionales) > 1 else None
                motivo = motivo_destino(agente, normal(RAIZ / destino)) if destino else None
                if motivo:
                    return f"`{posicionales[0]} {posicionales[1]}` escribe en {destino}: {motivo}"
        if nombre == "kicad-cli" or "verificar.py" in segmento:
            rutas = [r for r in (resolver(a, cwd) for a in args) if r]
            if dentro(cwd, TFG) or any(dentro(r, TFG) for r in rutas):
                return "kicad-cli reescribe el .kicad_prl del proyecto que lee: trabaja sobre una copia del TFG"
        for destino in destinos(nombre, args, segmento, cwd):
            motivo = motivo_destino(agente, destino)
            if motivo:
                return f"`{nombre}` escribiría donde no puedes: {motivo}"
    return None


def cadenas(valor, clave=""):
    """Pares (clave, texto) de todos los valores de texto de la entrada, a cualquier profundidad."""
    if isinstance(valor, str):
        yield clave, valor
    elif isinstance(valor, dict):
        for k, v in valor.items():
            yield from cadenas(v, str(k).lower())
    elif isinstance(valor, list):
        for v in valor:
            yield from cadenas(v, clave)


def parece_ruta(texto):
    t = texto.strip().lower()
    return ("://" not in t and len(t) < 400 and not t.startswith(("${", "$("))
            and ("/" in t or "\\" in t or t.startswith(("~", ".")) or t.endswith(EXTENSIONES_RUTA)))


def motivo_mcp(agente, herramienta, entrada, cwd):
    nombre = herramienta.split("__")[-1]
    textos = list(cadenas(entrada))
    if any(TFG_TEXTO.search(v) for _, v in textos):
        return "el MCP no puede abrir ni escribir nada dentro de la carpeta del TFG: copia antes el proyecto a hardware/"
    rutas = [r for r in (resolver(v, cwd) for _, v in textos if parece_ruta(v)) if r]
    if any(dentro(r, TFG) for r in rutas):
        return "el MCP no puede abrir ni escribir nada dentro de la carpeta del TFG: copia antes el proyecto a hardware/"
    # La zona solo se comprueba en los argumentos que nombran el destino: los demás pueden
    # señalar orígenes de solo lectura (librería oficial, modelos 3D, plantillas) o ser textos.
    destinos_mcp = [r for r in (resolver(v, cwd) for k, v in textos if k in CLAVES_DESTINO and parece_ruta(v)) if r]
    if not escribe_mcp(nombre, entrada):
        return None
    if agente == "ing-validacion":
        if nombre == "close_project":
            return "close_project tiene que llevar save: false"
        return f"{nombre} modifica el diseño o escribe archivos"
    for ruta in destinos_mcp:
        if dentro(ruta, TEMPORAL):
            continue
        if not dentro(ruta, RAIZ):
            return f"{nombre} escribiría fuera del repositorio ({ruta})"
        if not relativa(ruta).startswith(ZONAS_MCP):
            return f"{nombre} escribiría en {relativa(ruta)}, fuera de {', '.join(ZONAS_MCP)}"
    return None


def escribe_mcp(nombre, entrada):
    """¿La llamada puede modificar archivos? Algunas herramientas solo escriben con ciertos parámetros."""
    if nombre == "lint_schematic_cosmetic":
        return entrada.get("dryRun") is not True
    if nombre == "lint_offgrid":
        return bool(entrada.get("fix"))
    if nombre == "close_project":
        return entrada.get("save") is not False
    return bool(ESCRITURA_MCP.match(nombre))


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
