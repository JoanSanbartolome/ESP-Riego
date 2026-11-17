---
name: revision-estudios
description: Cómo validar estudios de diseño de docs/diseno/ sin KiCad (p. ej. SPEC-0005, tecnología de salidas): costes, datasheets de PDF codificados, LCSC por JSON y fallos típicos de protección y hold-up
metadata:
  type: feedback
---

Un estudio comparativo se valida recalculando sus cifras y releyendo cada dato clave en el datasheet. No basta con que el razonamiento «suene bien».

**Por qué:** en VAL-0005-01 (2026-11-04), todas las cifras de coste cuadraban, pero salieron 4 problemas:
- el *hold-up* de 60 ms de la lógica olvidaba el UVLO de ALI-06 y la entrada mínima de 18 V: eran 5–15 ms;
- «sin fusible por canal» con un *high-side* cuya limitación (≥ 38 A) supera la de la fuente: la protección real es la fuente más el firmware, y el bus cae para todos los canales;
- un descarte del usuario (BTS428L2) se daba por «válido eléctricamente», pero tiene V_IN(T+) de 3,2 V y protección de corto solo hasta 24 V;
- el coste de la segunda fuente usaba el tramo de 30 unidades para comprar 15.

**Cómo aplicarlo:**
- **LCSC:** `https://wmsc.lcsc.com/ftps/wm/product/detail?productCode=Cxxxx` devuelve un JSON con el MPN, el stock, los tramos de precio y `pdfUrl`. La ficha web es dinámica y WebFetch no ve los precios. JLCPCB `partdetail` sí muestra Basic/Extended en WebFetch.
- **PDF de LCSC con fuente codificada** (PROFET clásicas de Infineon: BSP752R, BTS428L2, BTS4140N): `pdftotext` da texto desplazado y sin cifras. Hay que renderizar las páginas a PNG con PyMuPDF y leer la imagen. La orden `file` da mal el número de páginas; `pypdf` lo da bien.
- **Costes:** reconstruyo la lista de materiales por canal hasta cuadrar al céntimo y compruebo que el tramo de precio corresponde a la cantidad real (piezas por placa × placas).
- **Protección de salidas:** comparo el límite del chip con el de la fuente, qué ve el resto de canales, si el diagnóstico sigue vivo con V_S colapsada (UV), y cuánto tarda el firmware en reaccionar.
- **Hold-up:** desde la VIN mínima menos el diodo hasta el umbral de bajada del UVLO, con la potencia de pico y C −20 %.
- **Energía inductiva (histórico desde DEC-0014, 2026-11-17: rueda libre D12–D17 montada, sin curva E_AS; ahora se comprueba el diodo M7, 1 A / I_FSM 30 A):** con el número máximo de cargas por canal y la ecuación del fabricante, que incluye la energía de V_S durante el *clamp*. Se compara con la curva E_AS(I_L), no con el E_AS a corriente nominal.
- **Salidas analógicas de diagnóstico** (IS) hacia el ADC: tensión en fallo frente al máximo del pin.
- **Rutas en Bash:** literales, sin `$S/…`, porque la guardia no expande variables y bloquea el `mkdir`.

**Estudios de viabilidad con un conector (VAL-0006-01, 2026-11-15):**
- `jlc.py --buscar` sirve para buscar alternativas con stock (el fusible C44479 pasó de 22 770 a 0 en 10 días: volver a consultar el stock de las piezas de la placa que cite el estudio).
- Pedir la lista de piezas por variante: sin ella, los totales solo se aproximan desde las cantidades del CSV.
- TPS2553 (SLVS841G): ecuaciones en las pp. 17 y 20; R_ILIM 15–232 kΩ; EN activo alto (p. 4); TSD en límite 135 °C. TI da los PDF en `ti.com/lit/ds/symlink/<pieza>.pdf`.
- Fallos típicos: la térmica en fallo calculada solo con el buck (falta el USB a 5,25 V); el margen de I²C en un solo sentido; señales activas a nivel bajo (OE del 74HC595) colgadas de una línea con *pull-down*; la lista para la spec siguiente sin las barreras de firmware de REL-04 (OTA, `esp_restart`).
- OpenSprinkler da 403 y KinCony 429 a WebFetch; Robotshop sí responde.
- Antes de dar una caída en una resistencia en serie de I²C, mirar a qué lado está el *pull-up*: si está en el lado del conector, el receptor no ve caída (VAL-0006-02, mi 0,25 V era 0,40 V).
- Inversores de ejemplo con 2N7002 a ≈ 2,4 V de puerta: V_GS(th) máx. 2,1–2,5 V, la conmutación no está garantizada.

Relacionado: [[revision-requisitos]], [[comprobaciones-utiles]].
