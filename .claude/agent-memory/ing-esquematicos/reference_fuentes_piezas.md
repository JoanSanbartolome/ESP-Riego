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

Los PDF de LCSC de las PROFET clásicas de Infineon (BTS428L2, BSP752R, BSP762T) tienen la fuente codificada: `pdftotext` y PyMuPDF devuelven texto desplazado y sin cifras. Se leen renderizando las páginas a imagen con PyMuPDF (así lo hizo VAL-0005-01).

Desde Bash, curl descarga al *scratchpad* los PDF de `datasheet.lcsc.com` y lee el JSON de `wmsc.lcsc.com` (campo `pdfUrl`). st.com no responde a curl, y el clasificador bloquea forzarlo con cabeceras de navegador: usar la copia de LCSC. Para descargar: `cd` al *scratchpad* y `curl -o` con nombre relativo. La guardia lee `<…>` y `>` dentro de un comando como redirección aunque vayan dentro de una cadena de Python: para cambiar textos con esos signos, usar Edit. Con PyMuPDF, usar `sys.stdout.reconfigure(encoding='utf-8')`, porque con `-I` no se lee PYTHONIOENCODING.

Tipo Basic/Extended y stock de JLCPCB por curl (2026-11-05): POST JSON `{"keyword":"Cxxxx" o "4.7uF 100V","currentPage":1,"pageSize":100}` a `https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList`; campos `data.componentPageInfo.list[].componentLibraryType` (`base`/`expand`) y `stockCount`. El stock de LCSC puede ser 0 con miles en JLCPCB (C28323). No hay 4,7 µF ≥ 100 V Basic.
SimSurfing: `curl -L` a `product.samsungsem.com/mlcc/<MPN sin última letra>.do` al *scratchpad* y Grep sobre el HTML (`"graphType" : "DCBias"|"TCC"|"RippleCurr"`, puntos `"x"`/`"y"`). La guardia bloqueó un `python -c` que leía ese HTML con `.replace(`: usar Grep/Read.

`search_parts_registry` (PartReel) solo da huellas y símbolos, sin datos de compra.

Lo que funcionó en SPEC-0017 (2026-11-05):
- Scripts propios del *scratchpad* escritos con Write (no con heredoc: la guardia lee el `>` como redirección). Un `lcsc.py` que recorre códigos C y descarga el `pdfUrl` con urllib, y otro que pasa una página de PDF a PNG con PyMuPDF para leer curvas. Write crea las carpetas, así que no hace falta `mkdir`.
- `curl -L -A "Mozilla/5.0"` sobre `https://www.ti.com/lit/ds/symlink/<pieza>.pdf` descarga la versión inglesa vigente. La copia de LCSC de TI puede estar en chino.
- El JSON de LCSC devuelve `result: null` para códigos retirados, como algunos Sunlord SWPA/MWSA.
- ESP32-S3 (datasheet v2.2, tabla 5-6): error total del ADC de ± 50 mV a 12 dB y ± 10 mV a 6 dB. Para medidas de ± 3 %, usar 6 dB.
- **El *scratchpad* lo comparten otros agentes en paralelo:** otro agente sobrescribió mi `dl.py` (2026-11-05). Hay que usar nombres con prefijo de la spec (`s20_*.py`).
- **Worktrees:** la guardia bloquea la escritura en `C:\Users\josan\proyectos\KICAD_mcp-SPEC-NNNN` («fuera del repositorio»; SPEC-0020). Si la orden pide trabajar en un worktree, hay que comprobar antes que se puede escribir. Si no, los borradores van al *scratchpad* y se responde `bloqueado`.
- **Stock a 0 (2026-11-05):** C15849 (1 µF 0603), C72043 (LED verde) y C14663 (100 nF Yageo). Sustituto de 1 µF 0603: C106248.
- **Modelos 3D que faltan en KiCad 10.0:** `SW_Push_1P1T_XKB_TS-1187A` (la huella sí está).
- **`hardware/componentes/` no es de mi zona.** La guardia bloquea las fichas: van como anexo en `docs/diseno/` y se piden en PENDIENTE.
