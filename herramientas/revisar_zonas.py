"""Comprueba que los cambios del árbol de trabajo están en la zona de un agente.

Uso: python herramientas/revisar_zonas.py <agente>

Lista los archivos modificados, nuevos o borrados (git status) que el agente no podría
escribir según las zonas de .claude/hooks/guardia.py, y sale con 1 si hay alguno. El
coordinador lo ejecuta antes de hacer commit del trabajo de un agente: detecta lo que se
escapa de la guardia, como las escrituras por el MCP o desde scripts. Los registros de
auditoría los escriben los hooks y no cuentan.
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / ".claude" / "hooks"))
import guardia  # noqa: E402  (mismas zonas que la guarda)


def cambios():
    salida = subprocess.run(["git", "-C", str(RAIZ), "status", "--porcelain=v1", "-z", "--untracked-files=all"],
                            capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    partes, rutas, i = salida.split("\0"), [], 0
    while i < len(partes):
        entrada = partes[i]
        if len(entrada) > 3:
            rutas.append(entrada[3:])
            if entrada[0] in "RC":  # renombrado o copiado: la siguiente parte es el origen
                i += 1
                rutas.append(partes[i])
        i += 1
    return rutas


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2 or sys.argv[1] not in guardia.ZONAS:
        print(f"Uso: python herramientas/revisar_zonas.py <{'|'.join(guardia.ZONAS)}>", file=sys.stderr)
        sys.exit(2)
    agente = sys.argv[1]
    fuera = []
    for ruta in cambios():
        if ruta.replace("\\", "/").startswith("gestion/logs/auditoria/"):
            continue
        motivo = guardia.motivo_destino(agente, guardia.normal(RAIZ / ruta))
        if motivo:
            fuera.append((ruta, motivo))
    for ruta, motivo in fuera:
        print(f"FUERA DE ZONA: {ruta} — {motivo}")
    print(f"{agente}: {'todo dentro de su zona' if not fuera else f'{len(fuera)} archivos fuera de su zona'}")
    sys.exit(1 if fuera else 0)


if __name__ == "__main__":
    main()
