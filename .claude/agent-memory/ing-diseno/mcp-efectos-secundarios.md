---
name: mcp-efectos-secundarios
description: Efectos del MCP de KiCad (backend swig) al abrir/sincronizar/cerrar un proyecto: reescribe .kicad_pro, crea .kicad_prl y .mcp-backups, y sync no copia campos
metadata:
  type: project
---

Observado en SPEC-0014 (2026-11-05), KiCad 10 + MCP backend swig:

- `open_project` + `close_project(save=false)` ya reescribe el `.kicad_pro` (añade ≈ 60 líneas de valores por defecto de KiCad 10, incl. `top_level_sheets` con UUID `00000000-…` escrito por pcbnew) y deja `.kicad_prl` y `.mcp-backups/` en la carpeta del proyecto.
- `sync_schematic_to_board` solo informa de huellas añadidas, redes y pads; **no copia campos de símbolo a huella** (la paridad `footprint_symbol_field_mismatch` sigue). No se ha comprobado si borra huellas sobrantes.
- Una PCB escrita a mano con el formato de pcbnew (tabs, CRLF) sale byte a byte igual tras open/sync/save del MCP.

SPEC-0019 (2026-11-06), esquema jerárquico: `sync_schematic_to_board` deja las huellas nuevas en (0,0), pone redes sin prefijo de hoja (`VIN_PROT` en vez de `/Alimentacion/VIN_PROT` → `net_conflict`), no copia campos, escribe el `.kicad_pcb` por su cuenta y luego rechaza el autoguardado. Inservible para paridad 0. Alternativa que dio ERC/DRC/paridad 0: `kicad-cli sch export netlist --format kicadsexpr` + script con `C:\Program Files\KiCad\10.0\bin\python.exe -I` (`pcbnew.FootprintLoad`, `SetPath(KIID_PATH(tstamps+uuid))`, `SetSheetname/Sheetfile`, `SetField`, `SetExcludedFromBOM/PosFiles`, `NETINFO_ITEM` incl. `unconnected-(…)`), sobre copia, y copiar solo el `.kicad_pcb` al repo (pcbnew reescribe el `.kicad_pro`).

SPEC-0022 (2026-11-07): el mismo script reasigna también redes renombradas en huellas existentes (pad.SetNet en todas) y las redes huérfanas desaparecen al guardar (KiCad 10 no lista redes en la cabecera). Los scratchpads de sesiones anteriores siguen en `%TEMP%\claude\<id>\<sesión>\scratchpad\` (buscar `sync.py`). Para revisar el diff del `.kicad_pcb` usar `git diff --patience` (el algoritmo por defecto infla las líneas borradas).

**Why:** el diff del `.kicad_pro` se infla con ruido y validación revisa restos (`.lck`, `-backups/`, `.kicad_prl`).

**How to apply:** probar primero el MCP sobre una copia en el scratchpad (con `hardware/libraries` al lado); si se abre el proyecto real, revisar después el diff del `.kicad_pro` y borrar `.kicad_prl` y `.mcp-backups/` de `hardware/v2`. Para campos de huella que faltan, añadirlos por script o con otra herramienta y comprobar con `verificar.py`.
