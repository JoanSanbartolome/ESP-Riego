"""Registro de auditoría de los subagentes de ESP-Riego.

Se usa desde tres sitios:
- PostToolUse, en el frontmatter de cada agente: `python .../auditoria.py <agente>`;
- PostToolUseFailure, en .claude/settings.json, sin argumento: el agente sale del campo
  agent_type del hook y, si no lo hay (la sesión principal), no se registra nada;
- guardia.py, que llama a registrar() para anotar las acciones bloqueadas, que no
  llegan a ningún hook posterior.

Añade una línea JSON por acción a gestion/logs/auditoria/AAAA-MM-DD.jsonl con
{ts, agente, agent_id, rama, spec, herramienta, objetivo, ok, sesion} y, según el caso,
`error` o `bloqueado`. AUDITORIA_DIR cambia la carpeta (solo para pruebas).
Nunca bloquea: ante cualquier error sale con 0.
"""
import datetime
import json
import os
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]


def rama():
    try:
        head = (RAIZ / ".git" / "HEAD").read_text(encoding="utf-8").strip()
    except OSError:
        return ""
    return head.removeprefix("ref: refs/heads/") if head.startswith("ref:") else head[:10]


def recortar(texto, limite):
    texto = " ".join(str(texto).replace("\n", " ⏎ ").split())
    return texto if len(texto) <= limite else texto[:limite - 1] + "…"


def ruta_legible(ruta_texto, cwd):
    ruta = Path(ruta_texto)
    if not ruta.is_absolute():
        ruta = Path(cwd) / ruta
    ruta = os.path.abspath(ruta)
    if os.path.normcase(ruta).startswith(os.path.normcase(str(RAIZ)) + os.sep):
        return os.path.relpath(ruta, RAIZ).replace("\\", "/")
    return ruta


def objetivo(entrada, cwd):
    if not isinstance(entrada, dict):
        return recortar(entrada, 300)
    for clave in ("file_path", "notebook_path"):
        if entrada.get(clave):
            return ruta_legible(entrada[clave], cwd)
    for clave, limite in (("command", 300), ("url", 300), ("query", 200), ("skill", 100)):
        if entrada.get(clave):
            return recortar(entrada[clave], limite)
    compacto = {k: recortar(v, 80) if isinstance(v, str) else v for k, v in entrada.items()}
    return recortar(json.dumps(compacto, ensure_ascii=False, default=str), 400)


def exito(respuesta):
    if isinstance(respuesta, dict):
        if respuesta.get("is_error") or respuesta.get("error") or respuesta.get("interrupted"):
            return False
        if respuesta.get("success") is False:
            return False
        for clave in ("exit_code", "exitCode", "returncode"):
            if isinstance(respuesta.get(clave), int) and respuesta[clave] != 0:
                return False
    if isinstance(respuesta, str) and respuesta.lstrip().lower().startswith(("error", "<error")):
        return False
    return True


def registrar(agente, datos, **extra):
    rama_actual = rama()
    spec = re.search(r"SPEC-\d{4}", rama_actual)
    registro = {
        "ts": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "agente": agente,
        "agent_id": str(datos.get("agent_id", "")),
        "rama": rama_actual,
        "spec": spec.group(0) if spec else "",
        "herramienta": datos.get("tool_name", ""),
        "objetivo": objetivo(datos.get("tool_input"), datos.get("cwd") or str(RAIZ)),
        "ok": exito(datos.get("tool_response")),
        "sesion": str(datos.get("session_id", ""))[:8],
        **extra,
    }
    carpeta = Path(os.environ.get("AUDITORIA_DIR") or RAIZ / "gestion" / "logs" / "auditoria")
    carpeta.mkdir(parents=True, exist_ok=True)
    with open(carpeta / f"{datetime.date.today().isoformat()}.jsonl", "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")


def main():
    datos = json.loads(sys.stdin.read() or "{}")
    agente = sys.argv[1] if len(sys.argv) > 1 else datos.get("agent_type", "")
    if not agente or not datos.get("tool_name"):
        return  # sesión principal o entrada sin acción: nada que registrar
    if datos.get("hook_event_name") == "PostToolUseFailure":
        registrar(agente, datos, ok=False, error=recortar(datos.get("error", ""), 300))
    else:
        registrar(agente, datos)


if __name__ == "__main__":
    sys.stderr.reconfigure(encoding="utf-8")  # en Windows, la tubería usaría cp1252
    try:
        main()
    except Exception as error:  # el registro nunca debe interrumpir el trabajo del agente
        print(f"auditoria: no se pudo registrar ({error!r})", file=sys.stderr)
    sys.exit(0)
