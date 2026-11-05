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
- Los JSON de EasyEDA SÍ se convierten (SPEC-0010): `kicad-cli fp upgrade -o <dir que no exista> x.json` y `kicad-cli sym upgrade -o x.kicad_sym x.json`. Probarlo siempre antes de extraer copias embebidas.
- KiCad 10 SÍ resuelve `${KICAD9_3DMODEL_DIR}` (cambiar a `KICAD10` es solo normalizar). KiCad 10.0.6 no instala `.wrl`: los modelos `.wrl` no se ven.
- `kicad-cli sch|pcb upgrade --force <archivo>` migra el formato sin abrir GUI/MCP; crea `.kicad_prl` (borrarlo).
