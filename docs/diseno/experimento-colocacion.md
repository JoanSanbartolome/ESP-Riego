# Experimento de colocación en texto (SPEC-0037, M10)

Pregunta (usuario, 2026-11-19): ¿qué cuesta menos en tokens para iterar la colocación, KiCad con imágenes o una herramienta en texto? El coste de desarrollar la herramienta no cuenta.

## Brazos

- **B (texto):** `colocacion.py evaluar` sobre el CSV de `colocar.py`. Informe de ≤ 30 líneas y una sola imagen al final (`vista.py placa`).
- **A (imágenes):** no se hizo. El usuario decidió el 2026-11-19 «probar con una herramienta en texto», en vista del paso 2. La estimación de abajo es la cota del brazo A.

## Resultados (registro de la spec y auditoría)

| Paso | Qué | Tokens | Acciones | Min | Iteraciones | Resultado de `evaluar` |
|---|---|---|---|---|---|---|
| 1 | Herramienta (`extraer`, `evaluar`) y 65 reglas | 296 093 | 86 | 26 | — | — |
| 2 | Brazo B, 100 × 70 | 173 296 | 25 | 18 | 6 | 0 incumplimientos con las 65 reglas |
| 3 | Criterios de DEC-0016 en la herramienta | 329 532 | 109 | 47 | — | — |
| 4 | Brazo B', tamaño variable | 305 463 | 83 | 51 | 25 | 100 × 100, 0 obligatorias, 46 objetivos |
| 5 | J2 y U5 al ras; 119 reglas | 517 342 | 148 | 70 | 23 | 0 obligatorias, 61 objetivos |
| 6 | Estudio de coste y J10 horizontal | 375 851 | 127 | 35 | 10 | 0 obligatorias, 58 objetivos |

Solo de colocar (pasos 2, 4 y 6, contando lo que en el paso 5 corresponde a recolocar):
- en los pasos 2 y 4, unos 7–12 k tokens por iteración;
- cada iteración en texto lee un informe de ≤ 30 líneas, menos de 1 k tokens;
- una imagen de la placa a 2000 px ronda los 5 k tokens de entrada, sin contar el contexto que se acumula entre una imagen y la siguiente.

## Cota del brazo A

Con una imagen por iteración y las mismas 25 iteraciones del paso 4, solo las imágenes suman ≈ 125 k tokens de entrada, y cada una se arrastra en el contexto de las siguientes. Además, la imagen no mide lo que sí comprueba `evaluar`: patios a 0,05 mm, serigrafía de 1,0 mm, anillos de cobre (U10 330/330 mm²), longitud sin rutar y rieles. Esas comprobaciones exigirían mediciones aparte con el MCP. En el paso 2, la imagen sí enseñó lo que las reglas no medían (serigrafía, pasillos, desacoplos). Por eso se sigue haciendo una imagen al final de cada colocación.

## Recomendación para la fase 4

- Iterar en texto con `colocacion.py` y una imagen al final, para que el usuario apruebe. Lo que la imagen enseñe se convierte en regla, como se hizo en los pasos 3 y 5.
- El rutado y la cara inferior no se pueden comprobar en texto (la regla `corte` es una estimación en línea recta): van a KiCad, con DRC.
- Las reglas de `colocacion-reglas.csv` que citan JLCPCB pasan a `.kicad_dru` y a la tabla de restricciones (DEC-0016, consecuencias).
