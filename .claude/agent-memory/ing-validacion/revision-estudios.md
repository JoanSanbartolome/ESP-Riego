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
- **Energía inductiva:** con el número máximo de cargas por canal y la ecuación del fabricante, que incluye la energía de V_S durante el *clamp*. Se compara con la curva E_AS(I_L), no con el E_AS a corriente nominal.
- **Salidas analógicas de diagnóstico** (IS) hacia el ADC: tensión en fallo frente al máximo del pin.
- **Rutas en Bash:** literales, sin `$S/…`, porque la guardia no expande variables y bloquea el `mkdir`.

Relacionado: [[revision-requisitos]], [[comprobaciones-utiles]].
