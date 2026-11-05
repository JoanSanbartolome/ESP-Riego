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
- La guardia bloquea `cp` hacia el *scratchpad* si el destino va en una variable de shell (`"$S/x"`). Hay que escribir la ruta literal.

Relacionado: [[reference-fuentes-piezas]]
