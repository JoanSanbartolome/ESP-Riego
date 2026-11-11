"""Batería de regresión de .githooks/commit_msg.py.

Uso: python herramientas/pruebas/test_commit_msg.py

Crea un repositorio git temporal con una copia del hook, de docs/02 y un sustituto de
herramientas/integridad_tfg.py (STUB_TFG=1 simula un TFG modificado), y prueba mensajes
en una rama spec/* y en un merge a main simulado con MERGE_HEAD.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CA = "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


def preparar():
    tmp = Path(tempfile.mkdtemp(prefix="commit_msg_"))
    for carpeta in (".githooks", "docs", "herramientas", "gestion/logs/SPEC-0007"):
        (tmp / carpeta).mkdir(parents=True)
    shutil.copy(REPO / ".githooks" / "commit_msg.py", tmp / ".githooks")
    shutil.copy(REPO / "docs" / "02-especificaciones-v2.md", tmp / "docs")
    (tmp / "herramientas" / "integridad_tfg.py").write_text(
        "import os, sys\nprint('cambiado: x.pdf') if os.environ.get('STUB_TFG') == '1' else None\n"
        "sys.exit(int(os.environ.get('STUB_TFG', '0')))\n", encoding="utf-8")
    (tmp / "gestion" / "logs" / "SPEC-0007" / "01-ing-esquematicos.md").write_text("log\n", encoding="utf-8")
    git(tmp, "init", "-q", "-b", "main")
    git(tmp, "config", "user.email", "prueba@example.com")
    git(tmp, "config", "user.name", "prueba")
    git(tmp, "add", "-A")
    git(tmp, "commit", "-q", "-m", "inicio")
    git(tmp, "switch", "-q", "-c", "spec/SPEC-0007-entrada")
    git(tmp, "commit", "-q", "--allow-empty", "-m", "trabajo")
    (tmp / "gestion" / "logs" / "SPEC-0007" / "02-sin-versionar.md").write_text("log\n", encoding="utf-8")
    return tmp


def probar(tmp, mensaje, stub="0"):
    archivo = tmp / "MSG.txt"
    archivo.write_text(mensaje, encoding="utf-8")
    r = subprocess.run([sys.executable, str(tmp / ".githooks" / "commit_msg.py"), str(archivo)], cwd=tmp,
                       capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, STUB_TFG=stub))
    return r.returncode, r.stderr.strip()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    tmp = preparar()
    t = "Spec: SPEC-0007\nAgente: ing-esquematicos"
    en_rama = [
        ("R01", "mensaje malo\n", 1),
        ("R02", "feat(sch): entrada\n", 1),
        ("R03", f"feat(sch): entrada\n\n{t}\n{CA}\n", 0),
        ("R04", f"feat(sch): entrada\n\n{t}\n\nTexto después de los trailers.\n", 1),
        ("R05", f"feat(sch): entrada\n{t}\n", 1),
        ("R06", f"feat(sch): entrada\n\nSpec: SPEC-0009\nAgente: ing-esquematicos\n", 1),
        ("R07", f"feat(sch): entrada\n\nSpec: SPEC-0007\nAgente: becario\n", 1),
        ("R08", f"feat(sch): entrada\n\n{t}\nRequisitos: ALI-01, XYZ-99\n", 1),
        ("R09", f"feat(sch): entrada\n\n{t}\nRequisitos: ALI-01, MCU-05\n", 0),
        ("R10", f"feat(sch): entrada\n\n{t}\nRequisitos: ninguno\n", 1),
        ("R11", f"feat(sch): entrada\n\n{t}\nLog: gestion/logs/SPEC-0007/01-ing-esquematicos.md\n", 0),
        ("R12", f"feat(sch): entrada\n\n{t}\nLog: gestion/logs/SPEC-0007/09-nadie.md\n", 1),
        ("R13", f"fixup! feat(sch): entrada\n", 0),
        # VAL-0001-02-08
        ("R14", f"feat(sch): entrada\n\n{t}\nLog: gestion/logs/SPEC-0007/02-sin-versionar.md\n", 1),
        ("R15", f"feat(sch): entrada\n\n{t}\nSpec: SPEC-0009\n", 1),
        ("R16", f"feat(sch): entrada\n\n{t}\nRequisitos: ALI-01, foo\n", 1),
        ("R17", f"feat(sch): entrada\n\n{t}\nRequisitos: ALI-011\n", 1),
        # DEC-0009: agente nuevo
        ("R18", "feat(sch): entrada\n\nSpec: SPEC-0007\nAgente: ing-diseno\n", 0),
    ]
    m = "Spec: SPEC-0007\nValidacion: VAL-0007-01\nRama: spec/SPEC-0007-entrada\nAgente: coordinador"
    en_merge = [
        ("M01", f"merge(SPEC-0007): entrada\n\n{m}\n{CA}\n", 0, "0"),
        ("M02", f"merge(SPEC-0007): entrada\n\n{m}\n", 1, "1"),
        ("M03", "merge(SPEC-0007): entrada\n\nSpec: SPEC-0007\nValidacion: lo que sea\nRama: spec/SPEC-0007-entrada\n", 1, "0"),
        ("M04", "merge(SPEC-0007): entrada\n\nSpec: SPEC-0007\nValidacion: VAL-0008-01\nRama: spec/SPEC-0007-entrada\n", 1, "0"),
        ("M05", "merge(SPEC-0007): entrada\n\nSpec: SPEC-0007\nValidacion: VAL-0007-01\n", 1, "0"),
        ("M06", f"chore: entrada\n\n{m}\n", 1, "0"),
    ]
    fallos = []
    for cid, mensaje, esperado in en_rama:
        codigo, error = probar(tmp, mensaje)
        if (codigo != 0) != (esperado != 0):
            fallos.append(cid)
            print(f"XX {cid}: salida {codigo}, esperada {esperado}\n   {error[:300]}")
    rama_head = git(tmp, "rev-parse", "HEAD")
    git(tmp, "switch", "-q", "main")
    (tmp / ".git" / "MERGE_HEAD").write_text(rama_head + "\n", encoding="utf-8")
    for cid, mensaje, esperado, stub in en_merge:
        codigo, error = probar(tmp, mensaje, stub)
        if (codigo != 0) != (esperado != 0):
            fallos.append(cid)
            print(f"XX {cid}: salida {codigo}, esperada {esperado}\n   {error[:300]}")
    (tmp / ".git" / "MERGE_HEAD").unlink()
    codigo, _ = probar(tmp, "docs: cambio sin spec en main\n")
    if codigo != 0:
        fallos.append("N01")
    total = len(en_rama) + len(en_merge) + 1
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"{total - len(fallos)}/{total} casos correctos" + (f"; fallan: {', '.join(fallos)}" if fallos else ""))
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
