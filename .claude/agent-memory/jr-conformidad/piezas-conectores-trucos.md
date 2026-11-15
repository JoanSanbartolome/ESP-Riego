---
name: piezas-conectores-trucos
description: Trucos del bloque de conectores (SPEC-0031): fichas de bloque, símbolos que faltan, datasheets TI, heredocs largos
metadata:
  type: reference
---

- `librerias.fichas` acepta una ficha de bloque (`bloque-<x>.md`, tabla con columna LCSC, tipo, fecha y la palabra «datasheet»): vale para cubrir pasivos sueltos (p. ej. C19666) sin una ficha por código.
- KiCad 10.0.6 no trae símbolo TPS2553/TPS2552; sí `Interface_Expansion:TCA9554PW`. Mirar con Grep en `share/kicad/symbols` antes de prometer «oficial».
- Datasheets TI: `https://www.ti.com/lit/ds/symlink/<pieza>.pdf` descarga con urllib y User-Agent «Mozilla/5.0». Para conectores sin PDF de fabricante, `dataManualFileAccessIdUrl` de la API de JLCPCB (firmado, caduca en 30 min: descargar en el acto).
- El TCA9554 de TI SÍ tiene pull-up interno de 100 kΩ (p. 16 de SCPS233E); DEC-0013 decía lo contrario. Comprobar siempre el datasheet antes de dar por buena una afirmación de la SPEC.
- Un heredoc de bash con varias fichas largas falló con «unexpected EOF»: escribir cada ficha con Write.
- No imprimir la respuesta entera de la API de JLCPCB: las URL firmadas ocupan miles de caracteres; filtrar los campos.
