---
name: reference-trucos-esquema
description: Límites del MCP de KiCad en esquemas (lo que no sabe borrar, textos multilínea), ancho de COMMENT1 en la hoja ESP-Riego y cómo exportar el PDF del cajetín sobre una copia
metadata:
  type: reference
---

- El MCP no tiene herramientas para borrar uniones (`junction`), *no-connect*, *netclass flags* ni `text_box`, y borra los cables de uno en uno. Para vaciar hojas (SPEC-0014) fue mejor un script de biblioteca estándar en el *scratchpad*: recorre los elementos de primer nivel de la *s-expression*, conserva el texto original y CRLF, y además limpia `lib_symbols`. Antes, se prueba sobre una copia.
- `add_schematic_text` escribe directamente en el `.kicad_sch` sin `open_project`. Los textos de varias líneas se justifican abajo (`justify left bottom`): el `at` es la base de la última línea y el bloque crece hacia arriba. Admite `≥ – … ² Ω`.
- Hoja de dibujo `ESP-Riego.kicad_wks`: `${COMMENT1}` va a 3,5 mm en negrita, en una casilla de ≈ 145 mm. Caben unos 50 caracteres; las mayúsculas ocupan más.
- PDF del cajetín sobre una copia: hay que copiar también `hardware/libraries/` al lado (como `../libraries`). Si no, `${KIPRJMOD}/../libraries/...` no resuelve, y KiCad usa sin avisar la hoja por defecto («Title:», «KiCad E.D.A.»).
- La guardia bloquea `cp` hacia el *scratchpad* si el destino va en una variable de shell (`"$S/x"`). Hay que escribir la ruta literal. Lo mismo con `kicad-cli -o` y con `python -c` que escriba: hay que usar scripts escritos con Write.

Dibujar una hoja entera (SPEC-0019, 2026-11-06, 55 piezas):
- Las llamadas *batch* del MCP **cortan a los 30 s** a medias: rinden ~4 s por pieza cuando la hoja crece. Lotes de ≤ 5–10, o colocar con el MCP y hacer etiquetas, campos y no-connect con un script propio (más rápido y reproducible).
- El MCP embebe en `lib_symbols` **copias antiguas** de símbolos simples (Device:R/C/L/LED/D_*, Fuse, Connector, Jumper, PWR_FLAG): `lib_symbol_mismatch` en el ERC. `update_symbol_from_library` no lo arregla. Solución: sustituir el bloque por el de `C:\Program Files\KiCad\10.0\share\kicad\symbols\<Lib>.kicad_sym` (renombrado `Lib:Nombre`).
- `batch_list_symbol_pins` da pines de esas copias: `Jumper:SolderJumper_2_Open` real tiene los pines a ± 5,08 mm (el MCP dice ± 3,81). Comprobar en la librería real.
- El MCP escribe los símbolos de alimentación en formato compacto e indentado con espacios. `kicad-cli sch upgrade --force <hoja>` normaliza el archivo (sobre una copia; conserva referencias y redes).
- Etiqueta local y jerárquica del mismo nombre en la misma hoja **se unen** (comprobado con la netlist).
- Pin de hoja sin destino: `pin_not_connected` (error); con etiqueta local, `label_dangling` (error). Una marca de no conexión sobre el pin de hoja deja el ERC a 0.
- Campos de símbolos girados 90/270: el ángulo del campo es relativo al símbolo (poner 90 para que se lea horizontal) y en giro 180 la justificación se invierte.
- Comprobar la hoja: netlist `kicadsexpr` frente al plan, y PDF → PNG con PyMuPDF (recortes en mm) para ver solapes.

Relacionado: [[reference-fuentes-piezas]]
