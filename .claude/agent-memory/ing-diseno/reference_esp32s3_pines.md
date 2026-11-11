---
name: reference-esp32s3-pines
description: Qué GPIO del ESP32-S3-WROOM-1 sirven para salidas activas altas (REL-04) y dónde están los datos de reset/glitch/descarga; trucos de fuentes de Espressif
metadata:
  type: reference
---

Datos sacados en SPEC-0020 (2026-11-05):

- **Estados de reset:** tabla 2-1 del ESP32-S3 Series Datasheet v2.2 (pp. 16-17). `pdftotext` desordena las columnas: hay que renderizar la página con PyMuPDF.
  - GPIO1–21 y 35–42: sin *pull* al reset.
  - GPIO0: WPU. GPIO45/46: WPD. TXD0/RXD0: WPU.
  - GPIO39 (MTCK): WPU tras el reset (nota 7).
- **Pulsos al arrancar** (tabla 2-2, pp. 18-19):
  - GPIO1–17: solo pulsos bajos de 60 µs;
  - **GPIO18: pulso alto**;
  - GPIO19/20: USB.
- **Descarga USB-OTG** (HDG tabla 12, p. 19): MTDO (GPIO40) se pone **alto**; MTCK (39) y GPIO38 se ponen bajos.
- **Pines aptos para salidas activas altas:** 1–17, 21, 35–38, 41, 42, 47 y 48. Se excluyen 0, 3, 18, 19, 20, 39, 40, 43, 44, 45 y 46.
- Las variantes R8/R16V del WROOM-1 solo llegan a 65 °C. Con la caja a 60 °C se usa N8.
- **HDG en PDF:** `docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/esp-hardware-design-guidelines-en-master-esp32s3.pdf` (se descarga con urllib). Datasheet: `espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf`.
- **Footers de BTT6050.pdf:** en algunas páginas, `pdftotext` muestra el pie de un borrador antiguo («*Target Data Sheet 30*»). Se cita la página del PDF.

Relacionado: [[reference-fuentes-piezas]], [[project-salidas-d8]]
