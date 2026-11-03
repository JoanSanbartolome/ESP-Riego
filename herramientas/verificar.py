"""Verificación estándar de un proyecto KiCad: ERC, DRC y paridad esquema↔PCB con kicad-cli.

Uso:
    python herramientas/verificar.py <proyecto.kicad_pro | .kicad_sch | .kicad_pcb | carpeta> [--salida DIR] [--json]

Códigos de salida: 0 si no hay errores de ERC ni de DRC, elementos sin conectar ni incidencias
de paridad; 1 si los hay; 2 si no se pudo verificar. Los informes JSON de kicad-cli se guardan
en --salida (por defecto, una carpeta temporal fuera del repositorio).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

KICAD_CLI_DEFECTO = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"


def fallar(mensaje):
    print(mensaje, file=sys.stderr)
    sys.exit(2)


def kicad_cli():
    for candidato in (os.environ.get("KICAD_CLI"), KICAD_CLI_DEFECTO, shutil.which("kicad-cli")):
        if candidato and Path(candidato).is_file():
            return candidato
    fallar("No se encuentra kicad-cli. Define la variable KICAD_CLI con su ruta.")


def localizar(ruta):
    ruta = Path(ruta).resolve()
    if ruta.is_dir():
        proyectos = sorted(ruta.glob("*.kicad_pro"))
        if len(proyectos) != 1:
            fallar(f"Se esperaba un único .kicad_pro en {ruta} y hay {len(proyectos)}.")
        ruta = proyectos[0]
    if not ruta.exists():
        fallar(f"No existe {ruta}.")
    sch = ruta.with_suffix(".kicad_sch")
    pcb = ruta.with_suffix(".kicad_pcb")
    return (sch if sch.exists() else None), (pcb if pcb.exists() else None)


def ejecutar(cli, argumentos, informe):
    resultado = subprocess.run([cli, *argumentos], capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
    if not informe.exists():
        fallar(f"kicad-cli no generó {informe.name}:\n{resultado.stdout}\n{resultado.stderr}")
    return json.loads(informe.read_text(encoding="utf-8"))


def contar(violaciones):
    por_tipo = Counter(f"{v.get('type')} [{v.get('severity')}]" for v in violaciones)
    return {
        "total": len(violaciones),
        "errores": sum(v.get("severity") == "error" for v in violaciones),
        "avisos": sum(v.get("severity") == "warning" for v in violaciones),
        "por_tipo": dict(por_tipo.most_common()),
    }


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="ERC, DRC y paridad con kicad-cli")
    parser.add_argument("proyecto")
    parser.add_argument("--salida", help="Carpeta para los informes JSON de kicad-cli")
    parser.add_argument("--json", action="store_true", help="Imprime el resumen en JSON")
    args = parser.parse_args()

    cli = kicad_cli()
    sch, pcb = localizar(args.proyecto)
    if not sch and not pcb:
        fallar("No hay esquema ni PCB que verificar.")
    salida = Path(args.salida).resolve() if args.salida else Path(tempfile.mkdtemp(prefix="verificar_"))
    salida.mkdir(parents=True, exist_ok=True)

    resumen = {"esquema": str(sch) if sch else None, "pcb": str(pcb) if pcb else None,
               "informes": str(salida)}
    if sch:
        erc = ejecutar(cli, ["sch", "erc", "--format", "json", "--severity-all",
                             "-o", str(salida / "erc.json"), str(sch)], salida / "erc.json")
        resumen["erc"] = contar([v for hoja in erc.get("sheets", []) for v in hoja.get("violations", [])])
    if pcb:
        argumentos = ["pcb", "drc", "--format", "json", "--severity-all", "-o", str(salida / "drc.json")]
        if sch:
            argumentos.append("--schematic-parity")
        drc = ejecutar(cli, [*argumentos, str(pcb)], salida / "drc.json")
        resumen["drc"] = contar(drc.get("violations", []))
        resumen["drc"]["sin_conectar"] = len(drc.get("unconnected_items", []))
        if sch:
            paridad = drc.get("schematic_parity", [])
            resumen["paridad"] = {"total": len(paridad),
                                  "por_tipo": dict(Counter(v.get("type") for v in paridad).most_common())}

    limpio = (resumen.get("erc", {}).get("errores", 0) == 0
              and resumen.get("drc", {}).get("errores", 0) == 0
              and resumen.get("drc", {}).get("sin_conectar", 0) == 0
              and resumen.get("paridad", {}).get("total", 0) == 0)
    resumen["limpio"] = limpio

    if args.json:
        print(json.dumps(resumen, ensure_ascii=False, indent=2))
    else:
        if "erc" in resumen:
            e = resumen["erc"]
            print(f"ERC      {e['total']:>4}  (errores {e['errores']}, avisos {e['avisos']})")
            for tipo, n in e["por_tipo"].items():
                print(f"  {n:>4}  {tipo}")
        if "drc" in resumen:
            d = resumen["drc"]
            print(f"DRC      {d['total']:>4}  (errores {d['errores']}, avisos {d['avisos']}, "
                  f"sin conectar {d['sin_conectar']})")
            for tipo, n in d["por_tipo"].items():
                print(f"  {n:>4}  {tipo}")
        if "paridad" in resumen:
            p = resumen["paridad"]
            print(f"Paridad  {p['total']:>4}")
            for tipo, n in p["por_tipo"].items():
                print(f"  {n:>4}  {tipo}")
        print(f"Resultado: {'LIMPIO' if limpio else 'CON INCIDENCIAS'} · informes en {salida}")
    sys.exit(0 if limpio else 1)


if __name__ == "__main__":
    main()
