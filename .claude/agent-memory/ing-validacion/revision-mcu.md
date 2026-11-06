---
name: revision-mcu
description: Cómo validar docs/diseno/mcu.md (ESP32-S3-WROOM-1, GPIO, EN, USB, REL-04): dónde están los datos en S3/WROOM/HDG, SimSurfing, fallos típicos (referencias duplicadas entre bloques, 15 mm de la HDG)
metadata:
  type: feedback
---

El estudio del bloque MCU (SPEC-0020, VAL-0020-01, 2026-11-06) salió bien en lo técnico. Los fallos estaban en la coherencia entre documentos.

**Por qué:** C22 quedó duplicada. SPEC-0018 la añadió a `alimentacion.md` y se trajo a la rama después de que el autor escribiera `mcu.md`.

**Cómo aplicarlo:**
- **Referencias provisionales:** comprobar siempre que no chocan con las de los otros `docs/diseno/*.md` en el HEAD actual, después de traer `main`. Usar Grep `\b(R1[6-9]|C2[2-5]|…)\b`.
- **Datos del S3 y del módulo:**
  - la tabla 2-1 del S3 v2.2 (pp. 16-17) se desordena en texto: renderizar con PyMuPDF;
  - GPIO39 tiene WPU después del reset (nota 7);
  - la tabla 2-2 da pulso alto solo en GPIO18–20;
  - el pin del módulo frente al GPIO está en la WROOM-1 tabla 3-1 (p. 11) y en el símbolo `RF_Module:ESP32-S3-WROOM-1`.
- **HDG *release master*:** página impresa = página física − 3. La tabla 12 (p. 19) da el estado de 21/38/39/40/41/42 en la descarga USB-OTG. Los 15 mm de la p. 30 son la zona libre **en la caja**, no la distancia a otras piezas de la PCB.
- **SimSurfing:** `https://product.samsungsem.com/mlcc/<PN sin la E final>.do` (urllib); el JSON `graphType` está dentro del HTML. weblib.samsungsem.com no responde. Con un X5R de ±20 %, aplicar la tolerancia además de la polarización.
- **EN RC:** simular τ con la polarización de C. El TPS2116 en modo prioridad solo conecta VIN1 por encima del umbral de PR1, así que el *soft-start* del buck solo es conservador.
- **USBLC6-2SC6:** V_CL = 12 V a 1 A y 17 V a 5 A (tabla 2, p. 2).
- **Antes de dar la revisión por empezada,** mirar si el coordinador ha hecho commits en la rama durante la revisión (p. ej. una DEC) y citar el HEAD final.

Relacionado: [[revision-alimentacion]], [[revision-estudios]], [[comprobaciones-utiles]].
