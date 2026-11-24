"""Batería de regresión de las órdenes del ciclo de herramientas/gestion.py.

Uso: python herramientas/pruebas/test_gestion.py [-v]

Crea un repositorio git temporal con copias de gestion.py, revisar_zonas.py, los hooks, el
hook commit-msg activado, docs/02 y las plantillas, y recorre el ciclo de una spec: nueva,
abrir, revisar, integrar, registrar y cerrar. Cada commit pasa por el commit-msg real, así
que la batería comprueba también que los trailers que escribe gestion.py son los que exige.
integridad_tfg.py se sustituye por uno que siempre da el TFG por intacto. GUARDIA_TEMPORAL
anula la exención de la carpeta temporal para que las zonas se comprueben de verdad.
"""
import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = "SPEC-0000"
RAMA = "spec/SPEC-0000-prueba"


def git(tmp, *args):
    return subprocess.run(["git", *args], cwd=tmp, capture_output=True, text=True, encoding="utf-8",
                          errors="replace").stdout.strip()


def gestion(tmp, *args):
    entorno = dict(os.environ, GUARDIA_TEMPORAL=str(tmp / "no-existe"), COAUTOR="Prueba <prueba@example.com>")
    r = subprocess.run([sys.executable, str(tmp / "herramientas" / "gestion.py"), *args], cwd=tmp,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=entorno)
    return r.returncode, (r.stdout + r.stderr).strip()


def escribir(tmp, ruta, texto="x\n"):
    destino = tmp / ruta
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(texto, encoding="utf-8", newline="\n")


def preparar():
    tmp = Path(tempfile.mkdtemp(prefix="gestion_"))
    for carpeta in ("herramientas", ".claude/hooks", ".githooks", "docs", "gestion/plantillas",
                    "gestion/specs", "gestion/informes", "gestion/decisiones", "gestion/logs/auditoria"):
        (tmp / carpeta).mkdir(parents=True)
    for origen in ("herramientas/gestion.py", "herramientas/revisar_zonas.py", ".claude/hooks/guardia.py",
                   ".claude/hooks/auditoria.py", ".githooks/commit_msg.py", ".githooks/commit-msg",
                   "docs/02-especificaciones-v2.md", "gestion/plantillas/spec.md"):
        shutil.copy(REPO / origen, tmp / origen)
    escribir(tmp, "herramientas/integridad_tfg.py", "import sys\nsys.exit(0)\n")
    for carpeta in ("gestion/specs", "gestion/informes", "gestion/decisiones"):
        escribir(tmp, carpeta + "/.gitkeep", "")
    git(tmp, "init", "-q", "-b", "main")
    git(tmp, "config", "user.email", "prueba@example.com")
    git(tmp, "config", "user.name", "prueba")
    git(tmp, "config", "core.autocrlf", "false")
    git(tmp, "add", "-A")
    git(tmp, "commit", "-q", "-m", "chore: inicio")
    git(tmp, "config", "core.hooksPath", ".githooks")
    return tmp


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    detalle = "-v" in sys.argv
    tmp = preparar()
    fallos, total = [], 0

    def caso(cid, condicion, contexto=""):
        nonlocal total
        total += 1
        if not condicion:
            fallos.append(cid)
        if detalle or not condicion:
            print(f"{'OK' if condicion else 'XX'} {cid}" + (f"\n     {str(contexto)[:400]}" if not condicion else ""))

    ruta_spec = tmp / "gestion" / "specs" / f"{SPEC}-prueba.md"

    # --- nueva-spec y abrir
    codigo, salida = gestion(tmp, "nueva-spec", "--titulo", "Prueba: del ciclo", "--fase", "0",
                             "--responsable", "ing-diseno", "--estado", "propuesta", "--slug", "prueba",
                             "--requisitos", "ALI-01,MCU-05")
    caso("A01 nueva-spec crea la spec con plan de validación y registro de 7 columnas",
         codigo == 0 and "## Plan de validación" in ruta_spec.read_text(encoding="utf-8")
         and "| Tokens | Acciones | Min |" in ruta_spec.read_text(encoding="utf-8"), salida)
    codigo, salida = gestion(tmp, "nueva-spec", "--titulo", "x", "--fase", "0", "--responsable", "ing-layout")
    caso("A02 nueva-spec rechaza un agente retirado", codigo != 0, salida)

    escribir(tmp, "hardware/x.txt")
    codigo, salida = gestion(tmp, "abrir", SPEC)
    caso("A03 abrir se niega con cambios fuera de gestion/", codigo != 0 and git(tmp, "branch", "--show-current") == "main", salida)
    (tmp / "hardware" / "x.txt").unlink()
    codigo, salida = gestion(tmp, "abrir", SPEC)
    asunto = git(tmp, "log", "-1", "--format=%s")
    caso("A04 abrir deja estado abierta, commit con el asunto del ciclo y la rama de la spec",
         codigo == 0 and "estado: abierta" in ruta_spec.read_text(encoding="utf-8")
         and asunto == f"spec({SPEC}): abrir — Prueba: del ciclo" and git(tmp, "branch", "--show-current") == RAMA,
         f"{salida}\n{asunto}")
    caso("A05 el commit de abrir lleva Spec, Agente y Co-Authored-By",
         git(tmp, "log", "-1", "--format=%(trailers:key=Spec,valueonly)%(trailers:key=Agente,valueonly)"
             "%(trailers:key=Co-Authored-By,valueonly)").split() == [SPEC, "coordinador", "Prueba", "<prueba@example.com>"])
    caso("A06 el commit de abrir lleva los Requisitos de la spec, que es el trailer que lee la trazabilidad",
         git(tmp, "log", "-1", "--format=%(trailers:key=Requisitos,valueonly)").strip() == "ALI-01, MCU-05")

    # --- revisar e integrar
    escribir(tmp, "hardware/v2/notas.md")
    escribir(tmp, "docs/02-especificaciones-v2.md", "cambiado\n")
    escribir(tmp, "gestion/logs/auditoria/2026-01-01.jsonl", "".join(json.dumps(l) + "\n" for l in (
        {"ts": "2026-01-01T10:00:00+01:00", "agente": "ing-diseno", "agent_id": "abc123def", "herramienta": "Bash",
         "objetivo": "ls", "ok": True},
        {"ts": "2026-01-01T10:07:00+01:00", "agente": "ing-diseno", "agent_id": "abc123def", "herramienta": "Bash",
         "objetivo": "rm docs/x", "ok": False, "bloqueado": "`rm` escribiría donde no puedes"},
        {"ts": "2026-01-01T10:09:00+01:00", "agente": "jr-conformidad", "agent_id": "zzz999", "herramienta": "Write",
         "objetivo": "hardware/x", "ok": True})))
    codigo, salida = gestion(tmp, "revisar", "ing-diseno")
    caso("R01 revisar avisa del archivo fuera de zona y del parte que falta, y sale con 1",
         codigo == 1 and "1 archivos FUERA" in salida and "FUERA: docs/02" in salida and "Parte: FALTA" in salida, salida)
    caso("R02 revisar resume la auditoría nueva del agente: 2 acciones, 1 bloqueo",
         "2 acciones nuevas, 1 bloqueos, 0 fallos" in salida and "abc123 (2)" in salida and "BLOQ Bash" in salida, salida)
    caso("R03 revisar cabe en 25 líneas", len(salida.splitlines()) <= 25, len(salida.splitlines()))
    codigo, salida = gestion(tmp, "integrar", SPEC, "--agente", "ing-diseno", "--tipo", "feat", "--resumen", "notas")
    caso("I01 integrar se niega con un archivo fuera de zona",
         codigo != 0 and git(tmp, "log", "-1", "--format=%s").startswith("spec("), salida)

    git(tmp, "checkout", "--", "docs/02-especificaciones-v2.md")
    escribir(tmp, f"gestion/logs/{SPEC}/01-ing-diseno.md", "parte\n" * 45)
    codigo, salida = gestion(tmp, "revisar", "ing-diseno")
    caso("R04 revisar pasa con todo en zona y avisa de un parte de más de 40 líneas",
         codigo == 0 and "Zonas: todo dentro" in salida and "pasa de 40" in salida, salida)
    codigo, salida = gestion(tmp, "integrar", SPEC, "--agente", "ing-diseno", "--tipo", "feat", "--resumen", "notas",
                             "--requisitos", "ALI-01,MCU-05")
    trailers = git(tmp, "log", "-1", "--format=%(trailers:only,unfold)")
    caso("I02 integrar hace el commit con Spec, Agente, Requisitos y Log",
         codigo == 0 and git(tmp, "log", "-1", "--format=%s") == f"feat({SPEC}): notas"
         and f"Spec: {SPEC}" in trailers and "Agente: ing-diseno" in trailers
         and "Requisitos: ALI-01, MCU-05" in trailers and f"Log: gestion/logs/{SPEC}/01-ing-diseno.md" in trailers,
         f"{salida}\n{trailers}")
    caso("I03 integrar deja el árbol limpio", git(tmp, "status", "--porcelain") == "")
    codigo, salida = gestion(tmp, "integrar", SPEC, "--agente", "ing-diseno", "--tipo", "feat", "--resumen", "nada")
    caso("I04 integrar sin cambios no hace commit", codigo != 0, salida)

    # --- coste: en el commit de integrar, en una fila suelta y en el tablero
    escribir(tmp, "hardware/v2/mas.md")
    escribir(tmp, f"gestion/logs/{SPEC}/02-ing-diseno.md", "parte\n")
    codigo, salida = gestion(tmp, "integrar", SPEC, "--agente", "ing-diseno", "--tipo", "feat", "--resumen", "Entrega | hoja",
                             "--tokens", "152000", "--agent-id", "abc123")
    texto = ruta_spec.read_text(encoding="utf-8")
    caso("G01 integrar --tokens anota la fila (tokens, y acciones y minutos de la auditoría) en el mismo commit",
         codigo == 0 and "| ing-diseno | Entrega \\| hoja | 02-ing-diseno | 152000 | 2 | 7 |" in texto
         and git(tmp, "status", "--porcelain") == ""
         and f"gestion/specs/{SPEC}-prueba.md" in git(tmp, "show", "--stat", "--format=", "HEAD"), f"{salida}\n{texto[-300:]}")
    codigo, salida = gestion(tmp, "registrar", SPEC, "--agente", "ing-validacion", "--accion", "Valida",
                             "--tokens", "48000", "--acciones", "30")
    caso("G02 registrar añade una fila suelta", codigo == 0 and "| ing-validacion | Valida |  | 48000 | 30 |  |"
         in ruta_spec.read_text(encoding="utf-8"), salida)
    codigo, salida = gestion(tmp, "tablero")
    tabla = (tmp / "gestion" / "TABLERO.md").read_text(encoding="utf-8")
    caso("G03 el tablero suma el coste por spec y por agente",
         codigo == 0 and "| 2 | 200 000 | 32 | 7 |" in tabla and "| ing-validacion | 1 | 48 000 | 30 | — |" in tabla, tabla[-700:])
    codigo, salida = gestion(tmp, "revisar", "jr-conformidad")
    caso("G04 las filas de registro y el tablero son del coordinador: no cuentan como fuera de zona",
         "Zonas: todo dentro" in salida, salida)
    original = ruta_spec.read_text(encoding="utf-8")
    ruta_spec.write_text(original.replace("- [ ]", "- [x] hecho"), encoding="utf-8", newline="\n")
    codigo, salida = gestion(tmp, "revisar", "jr-conformidad")
    caso("G05 cualquier otro cambio en la spec sí cuenta como fuera de zona",
         codigo == 1 and f"FUERA: gestion/specs/{SPEC}-prueba.md" in salida, salida)
    ruta_spec.write_text(original, encoding="utf-8", newline="\n")
    auditoria = tmp / "gestion" / "logs" / "auditoria" / "2026-01-01.jsonl"
    lineas = auditoria.read_text(encoding="utf-8")
    auditoria.write_text(lineas.split("\n", 1)[1], encoding="utf-8", newline="\n")
    codigo, salida = gestion(tmp, "revisar", "jr-conformidad")
    caso("G06 revisar avisa si a la auditoría versionada le falta una línea",
         codigo == 1 and "AUDITORÍA ALTERADA" in salida, salida)
    auditoria.write_text(lineas, encoding="utf-8", newline="\n")

    # --- instancia continuada: integrar solo cuenta la tanda nueva (VAL-0037-01-05)
    ahora = datetime.datetime.now().astimezone()
    escribir(tmp, "gestion/logs/auditoria/2026-01-02.jsonl", "".join(json.dumps(
        {"ts": (ahora + datetime.timedelta(minutes=m)).isoformat(timespec="seconds"), "agente": "ing-diseno",
         "agent_id": "abc123def", "herramienta": "Bash", "objetivo": "ls", "ok": True}) + "\n" for m in (1, 4)))
    escribir(tmp, "hardware/v2/otra.md")
    escribir(tmp, f"gestion/logs/{SPEC}/03-ing-diseno.md", "parte\n")
    codigo, salida = gestion(tmp, "integrar", SPEC, "--agente", "ing-diseno", "--tipo", "fix", "--resumen", "Corrige",
                             "--tokens", "1000", "--agent-id", "abc123")
    texto = ruta_spec.read_text(encoding="utf-8")
    caso("G07 integrar de una instancia continuada anota solo la tanda nueva: 2 acciones y 3 min, no 4 y 7",
         codigo == 0 and "| ing-diseno | Corrige | 03-ing-diseno | 1000 | 2 | 3 |" in texto, f"{salida}\n{texto[-300:]}")
    caso("G08 el commit de integrar lleva el trailer Agent-Id",
         git(tmp, "log", "-1", "--format=%(trailers:key=Agent-Id,valueonly)").strip() == "abc123")

    # --- cerrar
    codigo, salida = gestion(tmp, "cerrar", SPEC)
    caso("C01 cerrar se niega sin informe", codigo != 0 and git(tmp, "branch", "--show-current") == RAMA, salida)
    informe = "---\nid: VAL-0000-01\nspec: SPEC-0000\nfecha: 2026-01-01\ncommit_revisado: abc\nveredicto: {}\n---\n"
    escribir(tmp, "gestion/informes/VAL-0000-01.md", informe.format("RECHAZADO"))
    codigo, salida = gestion(tmp, "revisar", "ing-validacion")
    caso("R05 revisar de validación encuentra el informe y su veredicto",
         codigo == 0 and "Informe: gestion/informes/VAL-0000-01.md (RECHAZADO)" in salida, salida)
    codigo, salida = gestion(tmp, "cerrar", SPEC)
    caso("C02 cerrar se niega con un informe RECHAZADO", codigo != 0 and "RECHAZADO" in salida, salida)
    escribir(tmp, "gestion/informes/VAL-0000-01.md", informe.format("APROBADO_CON_OBSERVACIONES"))
    codigo, salida = gestion(tmp, "integrar", SPEC, "--agente", "ing-validacion", "--tipo", "val",
                             "--resumen", "VAL-0000-01 — APROBADO_CON_OBSERVACIONES")
    caso("C03 integrar el informe de validación", codigo == 0, salida)
    escribir(tmp, "gestion/ESTADO.md", "# Estado\n")
    codigo, salida = gestion(tmp, "cerrar", SPEC)
    trailers = git(tmp, "log", "-1", "--format=%(trailers:only,unfold)")
    texto = ruta_spec.read_text(encoding="utf-8")
    caso("C04 cerrar fusiona en main con el asunto y los trailers del merge",
         codigo == 0 and git(tmp, "branch", "--show-current") == "main"
         and git(tmp, "log", "-1", "--format=%s") == f"merge({SPEC}): Prueba: del ciclo"
         and len(git(tmp, "log", "-1", "--format=%P").split()) == 2
         and "Validacion: VAL-0000-01" in trailers and f"Rama: {RAMA}" in trailers, f"{salida}\n{trailers}")
    caso("C05 cerrar deja la spec cerrada, con fecha e informe, y la rama borrada",
         "estado: cerrada" in texto and "validacion: VAL-0000-01" in texto and "cerrada: 20" in texto
         and git(tmp, "branch", "--list", RAMA) == "", texto[:400])
    caso("C06 el merge incluye ESTADO.md, el tablero y la trazabilidad, y el árbol queda limpio",
         (tmp / "gestion" / "ESTADO.md").exists() and (tmp / "gestion" / "TRAZABILIDAD.md").exists()
         and "## Cerradas (1)" in (tmp / "gestion" / "TABLERO.md").read_text(encoding="utf-8")
         and git(tmp, "status", "--porcelain") == "", git(tmp, "status", "--porcelain"))
    caso("C07 el commit de cierre en la rama precede al merge",
         f"spec({SPEC}): cerrar — VAL-0000-01 APROBADO_CON_OBSERVACIONES" in git(tmp, "log", "--format=%s", "-4"))

    # --- guarda: script en la carpeta temporal que escribe fuera de la zona (VAL-0038-01-04)
    temporal = tmp / "no-existe"
    temporal.mkdir()

    def guarda(agente, comando):
        datos = {"tool_name": "Bash", "tool_input": {"command": comando}, "cwd": str(tmp)}
        r = subprocess.run([sys.executable, str(tmp / ".claude" / "hooks" / "guardia.py"), agente],
                           input=json.dumps(datos), capture_output=True, text=True, encoding="utf-8",
                           errors="replace", env=dict(os.environ, GUARDIA_TEMPORAL=str(temporal),
                                                      AUDITORIA_DIR=str(tmp / "auditoria-pruebas")))
        return r.returncode, r.stderr.strip()

    docs = (tmp / "docs" / "diseno" / "x.md").as_posix()
    escribir(tmp, "no-existe/estudio.py", f"from pathlib import Path\np = Path(r'{docs}')\n"
                                          "t = p.read_text(encoding='utf-8')\np.write_text(t + 'a', encoding='utf-8')\n")
    escribir(tmp, "no-existe/lee.py", f"from pathlib import Path\nt = Path(r'{docs}').read_text()\n"
                                      f"open(r'{(tmp / 'hardware' / 'y.md').as_posix()}', 'w').write(t)\n")
    comando = f"S={temporal.as_posix()}; cd $S && PYTHONUTF8=1 python -I estudio.py"
    codigo, salida = guarda("jr-conformidad", comando)
    caso("Z01 la guarda bloquea a jr-conformidad un script de la carpeta temporal que escribe en docs/ "
         "(el caso de VAL-0038-01-04)", codigo == 2 and "docs/diseno/x.md" in salida, salida)
    codigo, salida = guarda("ing-diseno", comando)
    caso("Z02 el mismo script pasa para ing-diseno, que tiene docs/diseno/ en su zona", codigo == 0, salida)
    codigo, salida = guarda("jr-conformidad", f"cd {temporal.as_posix()} && python lee.py")
    caso("Z03 un script que lee docs/ y escribe en hardware/ pasa para jr-conformidad", codigo == 0, salida)
    codigo, salida = guarda("jr-conformidad", "python - <<'EOF'\nprint(1)\nEOF")
    caso("Z04 el código en línea sigue sin analizarse (DEC-0009, M9)", codigo == 0, salida)

    # --- comprobar: VIGENTES.md frente a los DEC y forma de las memorias (SPEC-0039)
    dec = "---\nid: {id}\ntitulo: x\nfecha: 2026-01-01\nestado: {estado}\n{por}---\n# x\n"
    escribir(tmp, "gestion/decisiones/DEC-0001-a.md", dec.format(id="DEC-0001", estado="modificada",
                                                                 por="modificada_por: [DEC-0002]\n"))
    escribir(tmp, "gestion/decisiones/DEC-0002-b.md", dec.format(id="DEC-0002", estado="aceptada", por=""))
    escribir(tmp, "gestion/decisiones/DEC-0003-c.md", dec.format(id="DEC-0003", estado="sustituida",
                                                                 por="modificada_por: [DEC-0002]\n"))
    vigentes = ("# Vigentes\n\n| tema | regla vigente | DEC | requisitos |\n|---|---|---|---|\n"
                "| orquestación | Una rama por spec. | DEC-0001 | — |\n| alimentación | 24 V. | DEC-0002 | ALI-01 |\n")
    escribir(tmp, "gestion/decisiones/VIGENTES.md", vigentes)
    memoria = ".claude/agent-memory/ing-diseno/"
    escribir(tmp, memoria + "MEMORY.md", "- [A](a.md) — tema a\n")
    escribir(tmp, memoria + "a.md", "# A\n\n- Un hecho. Por qué: un motivo. Fuente: SPEC-0039.\n")
    codigo, salida = gestion(tmp, "comprobar")
    caso("K01 comprobar pasa con VIGENTES.md y una memoria correctos", codigo == 0, salida)
    escribir(tmp, "gestion/decisiones/VIGENTES.md", vigentes.replace("| alimentación | 24 V. | DEC-0002 | ALI-01 |\n", ""))
    codigo, salida = gestion(tmp, "comprobar")
    caso("K02 comprobar avisa de un DEC aceptado que VIGENTES.md no cita", codigo == 1 and "no cita DEC-0002" in salida, salida)
    escribir(tmp, "gestion/decisiones/VIGENTES.md", vigentes + "| salidas | x. | DEC-0003 | — |\n")
    codigo, salida = gestion(tmp, "comprobar")
    caso("K03 comprobar avisa de un DEC sustituido usado como regla vigente",
         codigo == 1 and "DEC-0003 está sustituida" in salida, salida)
    escribir(tmp, "gestion/decisiones/VIGENTES.md", vigentes)
    escribir(tmp, memoria + "b.md", "# B\n\n- Otro hecho sin fuente, de ayer.\n")
    codigo, salida = gestion(tmp, "comprobar")
    caso("K04 comprobar avisa de un archivo de memoria que MEMORY.md no enlaza, de la forma y de la fecha relativa",
         codigo == 1 and "no enlaza b.md" in salida and "b.md l. 3 no tiene la forma" in salida
         and "fecha relativa" in salida, salida)

    shutil.rmtree(tmp, ignore_errors=True)
    print(f"{total - len(fallos)}/{total} casos correctos" + (f"; fallan: {', '.join(f.split()[0] for f in fallos)}" if fallos else ""))
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
