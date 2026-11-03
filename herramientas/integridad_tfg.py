"""Huella SHA-256 de la carpeta del TFG, para detectar cualquier cambio en ella.

Uso:
    python herramientas/integridad_tfg.py crear       # escribe gestion/tfg-manifiesto.json
    python herramientas/integridad_tfg.py verificar   # 0 si nada ha cambiado; 1 si algo ha cambiado

La carpeta del TFG es de solo lectura (CLAUDE.md). La guardia bloquea las formas de
modificarla que reconoce; esta huella detecta cualquier otra, sea cual sea la herramienta.
El hook commit-msg la verifica en cada merge a main. Se excluye el repositorio git propio
del TFG (.git). Si el cambio es legítimo (del usuario), se regenera con `crear` y se explica
en el commit.
"""
import datetime
import hashlib
import json
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TFG = Path(r"C:\Users\josan\proyectos\TFG")
MANIFIESTO = RAIZ / "gestion" / "tfg-manifiesto.json"


def huella():
    archivos = {}
    for carpeta, subcarpetas, nombres in os.walk(TFG):
        subcarpetas[:] = sorted(d for d in subcarpetas if d != ".git")
        for nombre in sorted(nombres):
            ruta = Path(carpeta) / nombre
            sha = hashlib.sha256()
            with open(ruta, "rb") as f:
                for bloque in iter(lambda: f.read(1 << 20), b""):
                    sha.update(bloque)
            archivos[ruta.relative_to(TFG).as_posix()] = {"bytes": ruta.stat().st_size, "sha256": sha.hexdigest()}
    return archivos


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden not in ("crear", "verificar") or not TFG.is_dir():
        print(__doc__ if TFG.is_dir() else f"No existe la carpeta del TFG: {TFG}", file=sys.stderr)
        sys.exit(2)
    actual = huella()
    if orden == "crear":
        datos = {"carpeta": str(TFG), "creado": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
                 "archivos": actual}
        MANIFIESTO.write_text(json.dumps(datos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
        total = sum(a["bytes"] for a in actual.values())
        print(f"Huella creada: {len(actual)} archivos, {total / 1e6:.1f} MB → {MANIFIESTO.relative_to(RAIZ).as_posix()}")
        return
    if not MANIFIESTO.exists():
        print("No hay huella: crea una con `python herramientas/integridad_tfg.py crear`.", file=sys.stderr)
        sys.exit(2)
    esperado = json.loads(MANIFIESTO.read_text(encoding="utf-8"))["archivos"]
    nuevos = sorted(set(actual) - set(esperado))
    borrados = sorted(set(esperado) - set(actual))
    cambiados = sorted(r for r in set(actual) & set(esperado) if actual[r]["sha256"] != esperado[r]["sha256"])
    if not (nuevos or borrados or cambiados):
        print(f"TFG intacto: {len(actual)} archivos coinciden con la huella.")
        return
    for etiqueta, lista in (("nuevo", nuevos), ("borrado", borrados), ("cambiado", cambiados)):
        for ruta in lista:
            print(f"{etiqueta}: {ruta}")
    sys.exit(1)


if __name__ == "__main__":
    main()
