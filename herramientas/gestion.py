"""Gestión de specs: ciclo de una spec, tablero y matriz de trazabilidad.

Uso:
    python herramientas/gestion.py nueva-spec --titulo "..." --fase 3 --responsable ing-diseno
        [--requisitos ALI-01,ALI-03] [--depende SPEC-0002] [--estado propuesta|abierta] [--slug texto]
    python herramientas/gestion.py abrir SPEC-NNNN
    python herramientas/gestion.py revisar <agente> [--sin-verificar]
    python herramientas/gestion.py integrar SPEC-NNNN --agente <agente> --tipo feat --resumen "..."
        [--cuerpo "..."] [--requisitos ALI-01,ALI-03] [--rutas a b ...] [--forzar]
        [--tokens N] [--agent-id <id>] [--acciones N] [--min N] [--accion "..."] [--ref ...]
    python herramientas/gestion.py registrar SPEC-NNNN --agente <agente> --accion "..."
        [--ref <sha o VAL>] [--tokens N] [--acciones N] [--min N] [--agent-id <id>]
    python herramientas/gestion.py cerrar SPEC-NNNN
    python herramientas/gestion.py tablero
    python herramientas/gestion.py trazabilidad

`abrir`, `integrar` y `cerrar` hacen los commits del ciclo con sus trailers; `revisar` resume
en pocas líneas lo que el coordinador comprueba antes de integrar el trabajo de un agente;
`integrar --tokens` y `registrar` anotan en el registro de la spec lo que ha costado cada
arranque (DEC-0009). El tablero, la trazabilidad, ESTADO.md, el diario y las filas de
registro de la spec son del coordinador y no cuentan como cambios del agente.
Ninguna orden hace push. Solo usa la biblioteca estándar. Los archivos generados no se
editan a mano.
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
GESTION = RAIZ / "gestion"
SPECS = GESTION / "specs"
INFORMES = GESTION / "informes"
DECISIONES = GESTION / "decisiones"
AUDITORIA = GESTION / "logs" / "auditoria"
DOC_REQUISITOS = RAIZ / "docs" / "02-especificaciones-v2.md"

AGENTES = ("coordinador", "ing-diseno", "jr-conformidad", "ing-validacion")
ESTADOS = ("propuesta", "abierta", "cerrada", "descartada")
AVISO = "<!-- Generado por herramientas/gestion.py: no editar a mano. -->"
COAUTOR = os.environ.get("COAUTOR") or "Claude Fable 5.2 <noreply@anthropic.com>"
REGISTRO_ANTIGUO = "| Fecha | Agente | Acción | Referencia |\n|---|---|---|---|\n"
REGISTRO = "| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |\n|---|---|---|---|---|---|---|\n"
KICAD = (".kicad_sch", ".kicad_pcb", ".kicad_pro", ".kicad_dru")
LINEAS_PARTE = 40


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


def leer_retirados():
    """IDs de la tabla «Requisitos retirados» de docs/02 (filas `| ID | vX.Y | ...`)."""
    patron = re.compile(r"^\|\s*([A-Z]{2,4}-\d{2})\s*\|\s*v\d+\.\d+\s*\|")
    return {m.group(1) for linea in DOC_REQUISITOS.read_text(encoding="utf-8").splitlines()
            if (m := patron.match(linea))}


def git(*args, entrada=None):
    resultado = subprocess.run(["git", "-C", str(RAIZ), *args], capture_output=True, input=entrada,
                               text=True, encoding="utf-8", errors="replace")
    return resultado.returncode, resultado.stdout


def git_ok(*args, entrada=None):
    """Como git(), pero termina con el error de git si la orden falla."""
    resultado = subprocess.run(["git", "-C", str(RAIZ), *args], capture_output=True, input=entrada,
                               text=True, encoding="utf-8", errors="replace")
    if resultado.returncode != 0:
        sys.exit(f"`git {' '.join(args[:3])}` ha fallado:\n{(resultado.stdout + resultado.stderr).strip()}")
    return resultado.stdout.strip()


def slug(texto):
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    texto = re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")
    return "-".join(texto.split("-")[:6])


def enlace(datos):
    return f"[{datos['id']}]({datos['_ruta'].relative_to(GESTION).as_posix()})"


def celda(texto):
    return str(texto).replace("|", "\\|")


def miles(numero):
    return f"{numero:,}".replace(",", " ") if numero else "—"


def escribir(ruta, lineas):
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    print(f"Generado {ruta.relative_to(RAIZ).as_posix()}")


def hoy():
    return datetime.date.today().isoformat()


# --- Specs: lectura y edición ----------------------------------------------------------

def buscar_spec(id_spec):
    rutas = list(SPECS.glob(f"{id_spec}-*.md"))
    if len(rutas) != 1:
        sys.exit(f"No hay una spec única con el ID {id_spec} en gestion/specs/.")
    return rutas[0], leer_front_matter(rutas[0])


def poner_campos(ruta, **campos):
    """Cambia valores del front matter y deja igual el resto del archivo."""
    texto = ruta.read_text(encoding="utf-8")
    fin = texto.find("\n---", 3)
    cabecera, resto = texto[:fin], texto[fin:]
    for clave, valor in campos.items():
        cabecera, n = re.subn(rf"(?m)^{clave}:.*$", lambda _: f"{clave}: {valor}", cabecera)
        if not n:
            cabecera += f"\n{clave}: {valor}"
    ruta.write_text(cabecera + resto, encoding="utf-8", newline="\n")


def anotar(ruta, agente, accion, referencia="", tokens="", acciones="", minutos=""):
    """Añade una fila al registro de la spec (la última sección del archivo)."""
    texto = ruta.read_text(encoding="utf-8").replace(REGISTRO_ANTIGUO, REGISTRO)
    if "\n## Registro" not in texto:
        texto = texto.rstrip("\n") + "\n\n## Registro\n\n" + REGISTRO
    fila = (f"| {hoy()} | {agente} | {celda(accion)} | {celda(referencia)} | "
            f"{tokens} | {acciones} | {minutos} |")
    ruta.write_text(texto.rstrip("\n") + "\n" + fila + "\n", encoding="utf-8", newline="\n")


def filas_registro(ruta):
    """Filas del registro con medida: [(agente, tokens, acciones, minutos)]."""
    texto = ruta.read_text(encoding="utf-8")
    filas = []
    for linea in texto[texto.find("\n## Registro"):].splitlines():
        celdas = [c.strip() for c in re.split(r"(?<!\\)\|", linea)[1:-1]]
        if len(celdas) < 7 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", celdas[0]):
            continue
        numeros = [int(c) if c.isdigit() else 0 for c in celdas[4:7]]
        if any(numeros):
            filas.append((celdas[1], *numeros))
    return filas


# --- Git: estado del árbol y commits ---------------------------------------------------

def rama_actual():
    return git_ok("rev-parse", "--abbrev-ref", "HEAD")


def cambios():
    """Rutas modificadas, nuevas o borradas del árbol de trabajo, con / como separador."""
    sys.path.insert(0, str(RAIZ / "herramientas"))
    import revisar_zonas
    return [r.replace("\\", "/") for r in revisar_zonas.cambios()]


def solo_registro(ruta):
    """¿Los cambios sin confirmar de una spec son solo filas de tabla (su registro)?"""
    codigo, salida = git("diff", "-U0", "HEAD", "--", ruta)
    lineas = [l for l in salida.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    return codigo == 0 and bool(lineas) and all(l[1:].startswith("|") for l in lineas)


def del_coordinador(ruta, spec):
    """Cambios del coordinador que conviven en el árbol con el trabajo de un agente: el
    tablero, la trazabilidad, el estado, su diario y las filas de registro de la spec."""
    if ruta in ("gestion/TABLERO.md", "gestion/TRAZABILIDAD.md", "gestion/ESTADO.md"):
        return True
    if ruta.startswith("gestion/logs/coordinador/"):
        return True
    return bool(spec) and ruta.startswith(f"gestion/specs/{spec}-") and solo_registro(ruta)


def fuera_de_zona(agente, rutas, spec=""):
    """[(ruta, motivo)] de los cambios que el agente no podría haber escrito."""
    if agente == "coordinador":
        return []
    sys.path.insert(0, str(RAIZ / "herramientas"))
    import revisar_zonas
    guardia = revisar_zonas.guardia
    return [(r, m) for r in rutas
            if not r.startswith("gestion/logs/auditoria/") and not del_coordinador(r, spec)
            and (m := guardia.motivo_destino(agente, guardia.normal(RAIZ / r)))]


def commit(asunto, trailers, cuerpo=""):
    """Commit de lo que hay en el índice, con los trailers del proyecto. Devuelve el sha corto."""
    bloque = "\n".join(f"{clave}: {valor}" for clave, valor in trailers.items() if valor)
    mensaje = asunto + "\n\n" + (cuerpo.strip() + "\n\n" if cuerpo.strip() else "") \
        + bloque + f"\nCo-Authored-By: {COAUTOR}\n"
    git_ok("commit", "-q", "-F", "-", entrada=mensaje)
    return git_ok("rev-parse", "--short", "HEAD")


def auditoria_nueva():
    """Líneas de la auditoría que todavía no están en HEAD (la auditoría solo crece)."""
    nuevas = []
    for ruta in sorted(AUDITORIA.glob("*.jsonl")):
        codigo, salida = git("show", f"HEAD:{ruta.relative_to(RAIZ).as_posix()}")
        ya = len(salida.splitlines()) if codigo == 0 else 0
        for linea in ruta.read_text(encoding="utf-8").splitlines()[ya:]:
            try:
                nuevas.append(json.loads(linea))
            except ValueError:
                pass
    return nuevas


def auditoria_de(agent_id):
    """(acciones, minutos) de una instancia de agente según la auditoría."""
    marcas = []
    for ruta in sorted(AUDITORIA.glob("*.jsonl")):
        for linea in ruta.read_text(encoding="utf-8").splitlines():
            if agent_id not in linea:
                continue
            try:
                registro = json.loads(linea)
            except ValueError:
                continue
            if str(registro.get("agent_id", "")).startswith(agent_id):
                marcas.append(datetime.datetime.fromisoformat(registro["ts"]))
    if not marcas:
        return 0, 0
    return len(marcas), round((max(marcas) - min(marcas)).total_seconds() / 60)


# --- Órdenes del ciclo -----------------------------------------------------------------

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
        fecha=hoy())
    ruta = SPECS / f"{nombre}.md"
    ruta.write_text(texto, encoding="utf-8", newline="\n")
    print(f"Creada {ruta.relative_to(RAIZ).as_posix()}")
    print(f"Rama: {rama}")


def abrir(args):
    """Pasos de «Abrir»: estado, registro, tablero, commit en main y rama de la spec."""
    ruta, datos = buscar_spec(args.spec)
    if rama_actual() != "main":
        sys.exit("`abrir` se ejecuta en main.")
    if datos.get("estado") not in ("propuesta", "abierta"):
        sys.exit(f"{args.spec} está {datos.get('estado')}: no se puede abrir.")
    ajenos = [r for r in cambios() if not r.startswith("gestion/")]
    if ajenos:
        sys.exit("Hay cambios fuera de gestion/; intégralos o descártalos antes de abrir:\n  "
                 + "\n  ".join(ajenos[:10]))
    poner_campos(ruta, estado="abierta")
    anotar(ruta, "coordinador", "Abre la spec")
    tablero(None)
    git_ok("add", "--", "gestion")
    requisitos = datos.get("requisitos") or []  # la trazabilidad lee este trailer
    sha = commit(f"spec({args.spec}): abrir — {datos.get('titulo', '')}",
                 {"Spec": args.spec, "Agente": "coordinador",
                  "Requisitos": requisitos if isinstance(requisitos, str) else ", ".join(requisitos)})
    git_ok("switch", "-q", "-c", datos["rama"])
    print(f"{args.spec} abierta en {sha}. Rama actual: {datos['rama']}")


def revisar(args):
    """Lo que el coordinador mira antes de integrar el trabajo de un agente, en pocas líneas."""
    agente = args.agente
    if agente not in AGENTES[1:]:
        sys.exit(f"Agente desconocido: {agente}. Válidos: {', '.join(AGENTES[1:])}")
    rama = rama_actual()
    spec = (re.search(r"SPEC-\d{4}", rama) or [""])[0]
    rutas = [r for r in cambios() if not r.startswith("gestion/logs/auditoria/")]
    print(f"{agente} · {rama} · {len(rutas)} archivos cambiados")
    for r in rutas[:8]:
        print(f"  {r}")
    if len(rutas) > 8:
        print(f"  … y {len(rutas) - 8} más")

    fuera = fuera_de_zona(agente, rutas, spec)
    print("Zonas: todo dentro" if not fuera else f"Zonas: {len(fuera)} archivos FUERA")
    for r, motivo in fuera[:4]:
        print(f"  FUERA: {r}")
    import revisar_zonas  # ya está en sys.path por cambios()
    alterada = revisar_zonas.auditoria_alterada()
    for archivo in alterada[:2]:
        print(f"AUDITORÍA ALTERADA: {archivo}")

    falta = False
    if agente == "ing-validacion":
        informes = [r for r in rutas if re.fullmatch(rf"gestion/informes/VAL-{spec[5:]}-\d\d\.md", r)]
        falta = not informes
        veredicto = leer_front_matter(RAIZ / informes[-1]).get("veredicto", "?") if informes else ""
        print(f"Informe: {informes[-1]} ({veredicto})" if informes else "Informe: FALTA")
    else:
        partes = [r for r in rutas if re.fullmatch(rf"gestion/logs/{spec}/\d\d-{agente}\.md", r)]
        falta = not partes
        if partes:
            lineas = len((RAIZ / partes[-1]).read_text(encoding="utf-8").splitlines())
            aviso = f" — pasa de {LINEAS_PARTE}" if lineas > LINEAS_PARTE else ""
            print(f"Parte: {partes[-1]} ({lineas} líneas{aviso})")
        else:
            print("Parte: FALTA")

    nuevas = [l for l in auditoria_nueva() if l.get("agente") == agente]
    incidencias = [l for l in nuevas if l.get("bloqueado") or l.get("ok") is False]
    instancias = Counter(str(l.get("agent_id", ""))[:6] for l in nuevas)
    print(f"Auditoría: {len(nuevas)} acciones nuevas, {sum(1 for l in nuevas if l.get('bloqueado'))} bloqueos, "
          f"{sum(1 for l in incidencias if not l.get('bloqueado'))} fallos"
          + (" · instancias: " + ", ".join(f"{i} ({n})" for i, n in instancias.items()) if instancias else ""))
    for l in incidencias[:6]:
        motivo = str(l.get("bloqueado") or l.get("error") or "falló")
        print(f"  {'BLOQ' if l.get('bloqueado') else 'FALLO'} {l.get('herramienta', '')}: "
              f"{motivo[:70]} · {str(l.get('objetivo', ''))[:50]}")
    if len(incidencias) > 6:
        print(f"  … y {len(incidencias) - 6} más")

    sucio = False
    if not args.sin_verificar and any(r.startswith("hardware/v2/") and r.endswith(KICAD) for r in rutas):
        r = subprocess.run([sys.executable, str(RAIZ / "herramientas" / "verificar.py"), "hardware/v2", "--json"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=RAIZ)
        try:
            v = json.loads(r.stdout)
            erc, drc, paridad = v.get("erc", {}), v.get("drc", {}), v.get("paridad", {})
            sucio = not v.get("limpio")
            print(f"Verificación: ERC {erc.get('errores', '—')} errores y {erc.get('avisos', '—')} avisos · "
                  f"DRC {drc.get('errores', '—')} errores, {drc.get('sin_conectar', '—')} sin conectar · "
                  f"paridad {paridad.get('total', '—')} · {'LIMPIO' if not sucio else 'CON INCIDENCIAS'}")
        except ValueError:
            sucio = True
            print(f"Verificación: verificar.py ha fallado — {(r.stderr or r.stdout).strip()[:120]}")
    sys.exit(1 if fuera or falta or alterada else 0)


def anotar_arranque(ruta, args, accion, referencia):
    """Fila del registro con lo que ha costado un arranque: tokens (los da el resultado del
    agente) y acciones y minutos (dados, o contados en la auditoría con --agent-id)."""
    acciones, minutos = args.acciones, args.min
    if args.agent_id:
        contadas, duracion = auditoria_de(args.agent_id)
        acciones = acciones if acciones is not None else contadas
        minutos = minutos if minutos is not None else duracion
    anotar(ruta, args.agente, accion, referencia,
           *("" if n is None else n for n in (args.tokens, acciones, minutos)))


def registrar(args):
    """Fila suelta en el registro de la spec (un arranque sin commit, una corrección)."""
    ruta, _ = buscar_spec(args.spec)
    if args.agente not in AGENTES:
        sys.exit(f"Agente desconocido: {args.agente}. Válidos: {', '.join(AGENTES)}")
    anotar_arranque(ruta, args, args.accion, args.ref)
    print(f"Anotado en {ruta.relative_to(RAIZ).as_posix()}")


def integrar(args):
    """Commit del trabajo de un agente en la rama de la spec, con sus trailers. Con --tokens
    o --agent-id, anota además el arranque en el registro de la spec, en el mismo commit."""
    ruta_spec, datos = buscar_spec(args.spec)
    if args.agente not in AGENTES:
        sys.exit(f"Agente desconocido: {args.agente}. Válidos: {', '.join(AGENTES)}")
    if rama_actual() != datos.get("rama"):
        sys.exit(f"`integrar` se ejecuta en la rama de la spec ({datos.get('rama')}).")
    rutas = cambios()
    if not rutas:
        sys.exit("No hay cambios que integrar.")
    fuera = fuera_de_zona(args.agente, args.rutas or rutas, args.spec)
    if fuera and not args.forzar:
        sys.exit(f"Hay archivos fuera de la zona de {args.agente} (usa --forzar si es correcto):\n  "
                 + "\n  ".join(f"{r} — {m}" for r, m in fuera[:10]))
    partes = sorted(r for r in rutas if re.fullmatch(rf"gestion/logs/{args.spec}/\d\d-{args.agente}\.md", r))
    informes = sorted(r for r in rutas if re.fullmatch(rf"gestion/informes/VAL-{args.spec[5:]}-\d\d\.md", r))
    if args.tokens is not None or args.agent_id:
        candidatos = informes if args.agente == "ing-validacion" else partes
        referencia = args.ref or (Path(candidatos[-1]).stem if candidatos else "")
        anotar_arranque(ruta_spec, args, args.accion or args.resumen, referencia)
    if args.rutas:
        git_ok("add", "--", *args.rutas, ruta_spec.relative_to(RAIZ).as_posix(),
               *(["gestion/logs/auditoria"] if AUDITORIA.exists() else []))
    else:
        git_ok("add", "-A")
    requisitos = ", ".join(r.strip() for r in args.requisitos.split(",") if r.strip())
    sha = commit(f"{args.tipo}({args.ambito or args.spec}): {args.resumen}",
                 {"Spec": args.spec, "Agente": args.agente, "Requisitos": requisitos,
                  "Log": partes[-1] if partes else ""}, args.cuerpo)
    print(f"{sha} {args.tipo}({args.ambito or args.spec}): {args.resumen}")


def cerrar(args):
    """Pasos de «Cerrar»: spec cerrada, merge --no-ff a main, tablero, trazabilidad y rama borrada."""
    ruta, datos = buscar_spec(args.spec)
    rama = datos.get("rama", "")
    if rama_actual() != rama:
        sys.exit(f"`cerrar` se ejecuta en la rama de la spec ({rama}).")
    informes = [i for i in cargar(INFORMES, f"VAL-{args.spec[5:]}-*.md")]
    if not informes:
        sys.exit(f"{args.spec} no tiene informe de validación.")
    informe = informes[-1]
    veredicto = informe.get("veredicto", "")
    if not veredicto.startswith("APROBADO"):
        sys.exit(f"{informe['id']} es {veredicto or 'sin veredicto'}: no se puede cerrar.")
    ajenos = [r for r in cambios() if not r.startswith("gestion/")]
    if ajenos:
        sys.exit("Hay cambios sin integrar fuera de gestion/:\n  " + "\n  ".join(ajenos[:10]))

    poner_campos(ruta, estado="cerrada", cerrada=hoy(), validacion=informe["id"])
    anotar(ruta, "coordinador", "Cierra la spec", f"{informe['id']} ({veredicto})")
    git_ok("add", "--", "gestion")
    commit(f"spec({args.spec}): cerrar — {informe['id']} {veredicto}", {"Spec": args.spec, "Agente": "coordinador"})
    git_ok("switch", "-q", "main")
    codigo, salida = git("merge", "--no-ff", "--no-commit", rama)
    if codigo != 0:
        sys.exit(f"El merge de {rama} tiene conflictos; resuélvelos a mano:\n{salida.strip()}")
    tablero(None)
    trazabilidad(None)
    git_ok("add", "--", "gestion/TABLERO.md", "gestion/TRAZABILIDAD.md")
    sha = commit(f"merge({args.spec}): {datos.get('titulo', '')}",
                 {"Spec": args.spec, "Validacion": informe["id"], "Rama": rama, "Agente": "coordinador"})
    git_ok("branch", "-d", rama)
    print(f"{args.spec} fusionada en main ({sha}) y rama borrada.")
    print("Falta: `git push origin main` y recordar al usuario que abra sesión nueva o compacte.")


# --- Tablero y trazabilidad ------------------------------------------------------------

def coste(specs):
    """Tablas de coste por spec y por agente a partir de los registros de las specs."""
    por_spec, por_agente = [], {}
    for s in specs:
        filas = filas_registro(s["_ruta"])
        if not filas:
            continue
        por_spec.append((s, len(filas), *(sum(f[i] for f in filas) for i in (1, 2, 3))))
        for agente, tokens, acciones, minutos in filas:
            total = por_agente.setdefault(agente, [0, 0, 0, 0])
            for i, valor in enumerate((1, tokens, acciones, minutos)):
                total[i] += valor
    if not por_spec:
        return []
    lineas = ["## Coste por spec", "", "| Spec | Arranques | Tokens | Acciones | Min |", "|---|---|---|---|---|"]
    lineas += [f"| {enlace(s)} | {n} | {miles(t)} | {miles(a)} | {miles(m)} |" for s, n, t, a, m in por_spec]
    lineas += ["", "## Coste por agente", "", "| Agente | Arranques | Tokens | Acciones | Min |", "|---|---|---|---|---|"]
    lineas += [f"| {agente} | {n} | {miles(t)} | {miles(a)} | {miles(m)} |"
               for agente, (n, t, a, m) in sorted(por_agente.items())]
    return lineas + [""]


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

    lineas += coste(specs)
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
    # Un ID retirado (§9) sigue siendo válido en las specs que lo trataron.
    conocidos = {r[0] for r in requisitos} | leer_retirados()
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

    p = sub.add_parser("abrir", help="Abre una spec: commit en main y rama")
    p.add_argument("spec")
    p.set_defaults(funcion=abrir)

    p = sub.add_parser("revisar", help="Resumen de lo que hay que mirar antes de integrar el trabajo de un agente")
    p.add_argument("agente")
    p.add_argument("--sin-verificar", action="store_true", help="No ejecuta verificar.py aunque haya cambios de KiCad")
    p.set_defaults(funcion=revisar)

    p = sub.add_parser("registrar", help="Anota en el registro de la spec lo que ha costado un arranque")
    p.add_argument("spec")
    p.add_argument("--agente", required=True)
    p.add_argument("--accion", required=True)
    p.add_argument("--ref", default="")
    p.add_argument("--tokens", type=int)
    p.add_argument("--acciones", type=int)
    p.add_argument("--min", type=int)
    p.add_argument("--agent-id", help="Cuenta las acciones y los minutos de esa instancia en la auditoría")
    p.set_defaults(funcion=registrar)

    p = sub.add_parser("integrar", help="Commit del trabajo de un agente en la rama de la spec")
    p.add_argument("spec")
    p.add_argument("--agente", required=True)
    p.add_argument("--tipo", required=True)
    p.add_argument("--resumen", required=True)
    p.add_argument("--ambito", help="Por defecto, el ID de la spec")
    p.add_argument("--cuerpo", default="")
    p.add_argument("--requisitos", default="")
    p.add_argument("--rutas", nargs="+", help="Por defecto, todos los cambios")
    p.add_argument("--forzar", action="store_true", help="Integra aunque haya archivos fuera de la zona")
    p.add_argument("--accion", help="Texto de la fila del registro (por defecto, el resumen)")
    p.add_argument("--ref", default="", help="Referencia de la fila (por defecto, el parte o el informe)")
    p.add_argument("--tokens", type=int)
    p.add_argument("--acciones", type=int)
    p.add_argument("--min", type=int)
    p.add_argument("--agent-id", help="Cuenta las acciones y los minutos de esa instancia en la auditoría")
    p.set_defaults(funcion=integrar)

    p = sub.add_parser("cerrar", help="Cierra una spec validada: merge a main y rama borrada")
    p.add_argument("spec")
    p.set_defaults(funcion=cerrar)

    sub.add_parser("tablero", help="Regenera gestion/TABLERO.md").set_defaults(funcion=tablero)
    sub.add_parser("trazabilidad", help="Regenera gestion/TRAZABILIDAD.md").set_defaults(funcion=trazabilidad)
    args = parser.parse_args()
    args.funcion(args)


if __name__ == "__main__":
    main()
