---
name: fuentes-datos
description: Cómo leer datasheets en PDF y de dónde bajar datos de piezas (LCSC, JLCPCB, TI, Samsung, Espressif, ESPHome) cuando jlc.py no basta
metadata:
  type: reference
---

- WebFetch no lee los PDF (guarda el binario): el texto sale con `pdftotext -layout <ruta> -`. Por qué: WebFetch no devuelve nada útil. Fuente: SPEC-0017.
- `pdftotext` desordena las tablas de TI, la tabla 2-1 del ESP32-S3 y los «P_x.y.z» del BTT6050: se renderiza la página con PyMuPDF (`clip`) y se cita «Tabla N, p. X» del PDF. Por qué: las columnas salen mezcladas. Fuente: SPEC-0006, SPEC-0020, SPEC-0023.
- Los PDF de LCSC de las PROFET clásicas de Infineon (BTS428L2, BSP752R, BSP762T) tienen la fuente codificada: solo se leen renderizados a imagen. Por qué: `pdftotext` y PyMuPDF dan texto desplazado y sin cifras. Fuente: VAL-0005-01.
- Con `python -I`, PyMuPDF necesita `sys.stdout.reconfigure(encoding='utf-8')`. Por qué: con `-I` no se lee PYTHONIOENCODING. Fuente: SPEC-0017.
- Datasheets por curl: el `pdfUrl` (en `datasheet.lcsc.com`) del JSON de `https://wmsc.lcsc.com/ftps/wm/product/detail?productCode=Cxxxx`; el `dataManualUrl` vale como campo `Datasheet`, pero no para bajarlo. Por qué: el `dataManualUrl` devuelve HTML a curl. Fuente: SPEC-0017.
- TI: `curl -L -A "Mozilla/5.0" https://www.ti.com/lit/ds/symlink/<pieza>.pdf`. Por qué: da la versión inglesa vigente, y la copia de LCSC puede estar en chino. Fuente: SPEC-0017.
- st.com, nxp.com y mouser.com no responden a curl y el clasificador bloquea insistir: se usa la copia de LCSC. Por qué: se pierde tiempo reintentando. Fuente: SPEC-0006, SPEC-0017.
- El JSON de LCSC da `result: null` en los códigos retirados. Por qué: no es un fallo de la consulta. Fuente: SPEC-0017.
- El stock que cuenta es el de JLCPCB (`jlc.py`): el de LCSC puede ser 0 con millones en JLCPCB (C14663, C28323). Por qué: C14663 salía sin stock en LCSC y tenía 34,75 M en JLCPCB. Fuente: SPEC-0017.
- La API de JLCPCB (`selectSmtComponentList`) filtra con `"componentLibraryType":"base"` o `"preferredComponentFlag":true` en el cuerpo, solo con palabras sueltas o un MPN; `jlc.py` no lo expone. Por qué: así se buscan las Basic o las Extended preferidas de un valor. Fuente: SPEC-0037 paso 6.
- SimSurfing (DC bias de MLCC Samsung): `curl -L` a `product.samsungsem.com/mlcc/<MPN sin la última letra>.do` y Grep en el HTML de `"graphType" : "DCBias"` o `"TCC"` (puntos `x`/`y`). Por qué: es la fuente de las capacidades efectivas de `docs/diseno`. Fuente: SPEC-0017.
- PDF de Espressif con urllib: HDG en `docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/esp-hardware-design-guidelines-en-master-esp32s3.pdf` y datasheet en `espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf`. Por qué: son las direcciones que bajan el PDF entero. Fuente: SPEC-0020.
- ESPHome: `curl -sL https://esphome.io/components/<x>/` y se lee el `<main>`. Por qué: WebFetch falla por límite de uso. Fuente: SPEC-0031.
- *Pull-ups* de I²C: la sección «Pull-Up Resistor Calculation» de cualquier expansor de TI (TCA9535 p. 27). Por qué: sirvió para los *pull-ups* del bus de expansión. Fuente: SPEC-0006.
- Búsquedas por fuerza bruta de valores (escaleras de resistencias): ≤ 13 valores por tramo. Por qué: 25^5 combinaciones no terminan en 5 min. Fuente: SPEC-0006.
