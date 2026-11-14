---
spec: SPEC-0029
agente: jr-conformidad
n: 01
fecha: 2026-11-14
estado: completado
---

# SPEC-0029 · 01 · jr-conformidad

## Hecho

- `hardware/componentes/campos-sensores.csv`: U13 (SHT40-AD1B-R3, C2848306) y C46 (100n, C14663), formato de `campos-salidas.csv`.
- `hardware/componentes/stock-sensores.csv`: las tres variantes de la ficha, SHT40-AD1B-R2 (alternativa) y el 100 nF, consulta 2026-11-14 con `jlc.py`.
- `hardware/componentes/SHT4x.md`: `stock_consultado`, tabla de aprovisionamiento y stock de alternativas al día.

## Decisiones y desviaciones

- Se mantiene SHT40-AD1B-R3 (C2848306): Extended, stock 13 207, el más barato de las R2/R3 de la familia SHT40 salvo la R2 (1,7491 $). Sin cambio de compra: no hay equivalente Basic.
- C14663 es Basic (stock 34 639 344); sin cambio.
- El stock del SHT40-R3 bajó de 15 537 (2026-11-05) a 13 207; sin riesgo.
- Datasheet de U13: URL de Sensirion de la ficha (V7.3); la de C46, la de LCSC ya usada en `campos-salidas.csv`.

## Para validación

- De la ficha solo se tocó el aprovisionamiento; el resto no se ha reverificado contra el PDF.

## Pendiente

- Ninguno.
