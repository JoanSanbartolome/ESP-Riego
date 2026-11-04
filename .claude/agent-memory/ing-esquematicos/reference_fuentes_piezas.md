---
name: reference-fuentes-piezas
description: Cómo obtener precio, stock y tipo Basic/Extended de LCSC/JLCPCB cuando la base local del MCP está vacía, y cómo leer PDFs de datasheets
metadata:
  type: reference
---

La base local de JLCPCB del MCP (`search_jlcpcb_parts`, `get_jlcpcb_part`) estaba vacía a 2026-11-04 (0 piezas), y `download_jlcpcb_database` no está en mi lista de herramientas.

Alternativas que funcionan con WebFetch:
- Precio, stock, parámetros y enlace al PDF: `https://wmsc.lcsc.com/ftps/wm/product/detail?productCode=Cxxxx` (JSON). La búsqueda `wmsc.../search/global` da 403, y `lcsc.com/search` no devuelve resultados.
- Tipo Basic/Extended: `https://jlcpcb.com/partdetail/Cxxxx`.
- Para encontrar el código Cxxxx: WebSearch con «<MPN> LCSC C number».
- Tarifas de montaje: `https://jlcpcb.com/help/article/pcb-assembly-price`.

Datasheets en PDF: WebFetch guarda el binario en `tool-results/` y no lo lee. Hay que extraer el texto con `pdftotext -layout <ruta> -` a la salida estándar. La guardia bloquea `mkdir` en el *scratchpad*, así que no se escribe en archivos intermedios.

Los PDF de LCSC de las PROFET clásicas de Infineon (BTS428L2, BSP752R, BSP762T) tienen la fuente codificada: `pdftotext` y PyMuPDF devuelven texto desplazado y sin cifras. Hay que buscar otra copia del datasheet. Con PyMuPDF, usar `sys.stdout.reconfigure(encoding='utf-8')`, porque con `-I` no se lee PYTHONIOENCODING.

`search_parts_registry` (PartReel) solo da huellas y símbolos, sin datos de compra.
