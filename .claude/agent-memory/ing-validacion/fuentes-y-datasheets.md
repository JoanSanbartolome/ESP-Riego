---
name: fuentes-y-datasheets
description: Cómo leer datasheets difíciles (tablas desordenadas, fuentes codificadas, escaneados) y de dónde bajar PDF y datos de LCSC, TI, Infineon, Samsung y Espressif
metadata:
  type: reference
---

- Tablas que `pdftotext` desordena (TI, ESP32-S3 tabla 2-1, Hongjiacheng, figuras del M7) o PDF sin texto útil (fuentes chinas, PROFET clásicas de Infineon en LCSC: BSP752R, BTS428L2): se renderiza la página (`pdftoppm -r 200` o PyMuPDF con `clip`) y se lee la imagen. Por qué: las columnas salen mezcladas o vacías. Fuente: VAL-0005-01, VAL-0020-01, VAL-0034-01, VAL-0037-01, VAL-0038-01.
- Dibujos escaneados (hojas de una imagen): `fitz.Pixmap(doc, xref)`, a PDF y render con `set_rotation(270)` y recorte; `file` puede dar mal el número de páginas y `pypdf` lo da bien. Por qué: es la forma de leer cotas de esas hojas. Fuente: VAL-0005-01, VAL-0015-01.
- Con `python -I` se ignora `PYTHONIOENCODING`: `sys.stdout.reconfigure(encoding="utf-8")` en el script o `-X utf8`. Por qué: «µ», «Ω» o «±» rompen la salida. Fuente: VAL-0004-01, VAL-0018-01.
- Datasheet de LCSC: el `pdfUrl` del JSON de `wmsc.lcsc.com/ftps/wm/product/detail?productCode=Cxxxx` se baja con `curl -L -A "Mozilla/5.0"`; el clasificador deniega `curl` con *referer* al CDN de LCSC. Por qué: la ficha web es dinámica y WebFetch no ve nada útil. Fuente: VAL-0005-01, VAL-0022-01; comprobado con C150716 en SPEC-0039.
- TI: `https://www.ti.com/lit/ds/symlink/<pieza>.pdf`. Por qué: da la revisión vigente. Fuente: VAL-0006-01.
- Infineon: `curl -A Mozilla` a `infineon.com/package/<encapsulado>` trae `assets.infineon.com/is/image/infineon/infineon-<pkg>-png-footprint-en.png` (es JPEG); el nombre exacto (PG-TDSO-14-11, no «-1») sale de los distribuidores. Por qué: WebFetch no ve la página (JS) y un nombre inventado da 404. Fuente: VAL-0015-01, VAL-0024-01.
- SimSurfing: `curl` o urllib a `product.samsungsem.com/mlcc/<MPN sin la última letra>.do`; el HTML trae el JSON `"graphType" : "DCBias"` → `"data"` (x en V, y en ΔC %). Por qué: weblib.samsungsem.com no responde. Fuente: VAL-0018-01, VAL-0020-01.
- WebFetch: OpenSprinkler da 403 y KinCony 429; Robotshop responde. Por qué: no se pierde tiempo reintentando. Fuente: VAL-0006-01.
- HDG de Espressif (*release master*): página impresa = página física − 3. Por qué: las citas del autor usan una u otra. Fuente: VAL-0020-01.
- Datasheets antiguos de BCD/Diodes (AP2114H): la tabla sin negrita vale solo a 25 °C (nota 3, «over temperature by design»), y la cifra en caliente se escala con la figura de temperatura. Por qué: la caída a 125 °C no está en la tabla. Fuente: VAL-0038-01; `hardware/componentes/datasheets/AP2114H-3.3TRG1.pdf`.
- Cuando un estudio cita una tabla de «valores típicos», se busca en el texto un «must» o «required». Por qué: en el LMR36520 (p. 20) el mínimo de entrada es obligatorio. Fuente: VAL-0037-01.
- El stock cambia en días: se vuelve a consultar con `jlc.py` el de las piezas de la placa que cite el estudio. Por qué: el fusible C44479 pasó de 22 770 a 0 en 10 días. Fuente: VAL-0006-01.
- Los datasheets locales están en `hardware/componentes/datasheets/`: los pines se cotejan con `pdftotext -layout` de su pinout, y para el cajetín basta `Read` del PDF exportado con `pages`. Por qué: evita descargas. Fuente: VAL-0016-01, VAL-0019-01.
