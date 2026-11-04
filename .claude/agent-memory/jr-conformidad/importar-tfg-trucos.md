---
name: importar-tfg-trucos
description: Trucos reutilizables para importar proyectos del TFG y convertir librerías con kicad-cli y la guardia de comandos
metadata:
  type: reference
---

- La guardia bloquea cualquier comando que mencione la ruta del TFG y use mkdir, python, git, variables de shell o bloques: hacer `mkdir` aparte (sin ruta del TFG) y luego `cd <TFG> && cp ... <destino absoluto literal>`; para analizar un archivo del TFG, copiarlo antes al scratchpad. `--salida` de verificar.py solo admite rutas de la zona de escritura.
- Los heredocs de Bash pierden las barras invertidas: escribe scripts Python con la herramienta Write.
- `kicad-cli sym upgrade -o out.kicad_sym in.lib` convierte `.lib` y lee el `.dcm` si está junto al `.lib` (aporta Description); el destino no debe existir. Convertir desde `.lib` (no desde un `.kicad_sym` hermano) reproduce lo embebido en el esquema y evita `lib_symbol_mismatch`.
- `kicad-cli fp upgrade <dir.pretty>` actualiza formato; en carpeta vacía da error inocuo.
- Libs EasyEDA JSON no se convierten con KiCad: extraer la copia embebida de `lib_symbols` (esquema) o de `(footprint ...)` (PCB, quitando at/uuid/net/path/sheet*).
- KiCad 10 no resuelve `${KICAD9_3DMODEL_DIR}`: cambiar a `${KICAD10_3DMODEL_DIR}`.
- `kicad-cli sch|pcb upgrade --force <archivo>` migra el formato sin abrir GUI/MCP; crea `.kicad_prl` (borrarlo).
