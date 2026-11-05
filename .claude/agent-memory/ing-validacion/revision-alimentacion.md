---
name: revision-alimentacion
description: Cómo validar el cálculo del bloque de alimentación (docs/diseno/alimentacion.md): qué recalcular, dónde mira el datasheet de TPS2663/LMR36520 y fallos típicos (separación de huecos, tolerancias puntuales, ADC)
metadata:
  type: feedback
---

El documento de alimentación (SPEC-0017, VAL-0017-01, 2026-11-05) salió bien en las cifras clave. Los fallos estaban en detalles de coherencia, no en la aritmética.

**Cómo aplicarlo:**
- Recalcular siempre: UVLO con k = 1 + R9/R10 y resistencias al 1 % (extremos 99/10,1 y 101/9,9); banda de I_OL con deriva de R_ILIM; error de VIN (ADC ± 10 mV a 6 dB + 0,954 × tolerancia + deriva); IPC-2221 (I = 0,048 ΔT^0,44 A^0,725 mil²; 3,0 mm 1 oz = 5,3 A con ΔT 10 °C).
- TPS2663 (SLVSE94G): la tabla da I_OL solo en R_ILIM = 3, 4,02, 9 y 30 kΩ (± 7, ± 7, ± 8, ± 10 %), y la nominal a 4,02 kΩ es 4,5 A (18,09/R, no 18/R). IMON 2–6 A: 26,22–29,58 µA/A. R_ON máx. 53 mΩ. Clamp OVC del 26632: 32–35 V.
- LMR36520: EN 1,157/1,231/1,3 V, histéresis 110 mV solo típica (la cota de bajada sin histéresis mínima es conservadora). I_LS-LIMIT 1,8–2,8 A. VFB ± 1,5 %.
- ESP32-S3 v2.2 tabla 5-6: ATTEN0 ± 5, ATTEN1 ± 6, ATTEN2 ± 10, ATTEN3 ± 50 mV (la extracción de texto desordena las filas: leer por orden). Se mide con 100 nF en el pin.
- Fallos que revisar en la próxima: huecos o puentes entre redes calculados con la tensión continua y no con Vc (VAL-0017-01-01); tolerancias de datasheet dadas en puntos de R sin interpolar; filtros RC al ADC distintos de la condición de medida; cerámicos sin curva de derating.
- Las extracciones de texto del autor están en el *scratchpad* compartido (`…/scratchpad/dl/*.txt`); sirven para releer el datasheet con Read. La guardia bloquea `python` en línea que escribe: usar Write para un script y `python -I` sobre él.
- LCSC: JSON de `wmsc.lcsc.com/ftps/wm/product/detail?productCode=Cxxxx` con `productPriceList` (ladder, usdPrice) y `stockNumber`.

Relacionado: [[revision-estudios]], [[revision-piezas]].
