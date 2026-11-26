---
name: mcp-kicad
description: Lo que el MCP de KiCad (backend swig) hace mal o no hace en proyectos, esquemas y sincronización, y con qué se sustituye
metadata:
  type: reference
---

- `open_project` + `close_project(save=false)` ya reescribe el `.kicad_pro` (≈ 60 líneas por defecto, `top_level_sheets`) y deja `.kicad_prl` y `.mcp-backups/`: se abren copias, o se revisa el diff del `.kicad_pro` y se borran esos restos de `hardware/v2`. Por qué: validación revisa los restos y el diff del `.kicad_pro`. Fuente: SPEC-0014.
- Una PCB con el formato de pcbnew (tabulaciones, CRLF) sale igual byte a byte tras open, sync y save del MCP. Por qué: se puede abrir para consultar sin ruido en el diff. Fuente: SPEC-0014.
- `sync_schematic_to_board` no copia campos de símbolo a huella y, con hojas jerárquicas, deja las huellas en (0,0) y las redes sin prefijo (`net_conflict`): la PCB se sincroniza con `sincronizar.py`. Por qué: con el MCP no se llega a paridad 0. Fuente: SPEC-0014, SPEC-0019.
- El MCP no borra uniones, *no-connect*, *netclass flags* ni `text_box`, y borra los cables de uno en uno: para vaciar o rehacer una hoja, `hoja.py`. Por qué: vaciar una hoja con el MCP no era viable. Fuente: SPEC-0014.
- `add_schematic_text` y `edit_schematic_component` escriben el `.kicad_sch` sin `open_project`; un texto de varias líneas se justifica abajo (el `at` es la base de la última línea) y `edit_schematic_component` no toca el `Footprint` de la caché `lib_symbols`. Por qué: si cambiara la caché, el ERC daría `lib_symbol_mismatch`. Fuente: SPEC-0019.
- Las llamadas *batch* del MCP se cortan a los 30 s a medias (≈ 4 s por pieza en una hoja grande): lotes de 5 a 10 como mucho. Por qué: dejaban la hoja a medio escribir. Fuente: SPEC-0019.
- El MCP embebe en `lib_symbols` copias antiguas de los símbolos simples (Device:R/C/L/LED/D, Fuse, Connector, Jumper, PWR_FLAG) y `update_symbol_from_library` no lo arregla: se sustituye el bloque por el de `C:\Program Files\KiCad\10.0\share\kicad\symbols\<Lib>.kicad_sym`. Por qué: el ERC da `lib_symbol_mismatch`. Fuente: SPEC-0019.
- `batch_list_symbol_pins` da los pines de esas copias (`Jumper:SolderJumper_2_Open`: ± 3,81 mm en vez de ± 5,08): se comprueban con `hoja.py pines`. Por qué: un cable al punto equivocado no conecta. Fuente: SPEC-0019.
- El MCP escribe los símbolos de alimentación compactos e indentados con espacios; `kicad-cli sch upgrade --force <hoja>` sobre una copia los normaliza y conserva referencias y redes. Por qué: el archivo queda con dos formatos. Fuente: SPEC-0019.
- `search_parts_registry` (PartReel) da solo huellas y símbolos, sin datos de compra: tipo, stock y precio salen de `jlc.py`. Por qué: no sirve para elegir piezas por coste. Fuente: SPEC-0017.
