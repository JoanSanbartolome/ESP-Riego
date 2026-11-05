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

**Why:** el diff del `.kicad_pro` se infla con ruido y validación revisa restos (`.lck`, `-backups/`, `.kicad_prl`).

**How to apply:** probar primero el MCP sobre una copia en el scratchpad (con `hardware/libraries` al lado); si se abre el proyecto real, revisar después el diff del `.kicad_pro` y borrar `.kicad_prl` y `.mcp-backups/` de `hardware/v2`. Para campos de huella que faltan, añadirlos por script o con otra herramienta y comprobar con `verificar.py`.
