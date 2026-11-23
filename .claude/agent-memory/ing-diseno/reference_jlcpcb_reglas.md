---
name: reference-jlcpcb-reglas
description: Dónde están (y dónde no) las reglas de fabricación, montaje Economic, serigrafía y precio por tamaño de JLCPCB, consultadas el 2026-11-19 para SPEC-0037
metadata:
  type: reference
---

Fuentes de JLCPCB que sirven con WebFetch (2026-11-19); las cifras ya están en `docs/diseno/colocacion-reglas.csv` (F01–F04, T01–T13, Z01):

- `jlcpcb.com/capabilities/pcb-capabilities`: pista 0,10/0,10 en 2 capas, cobre a borde fresado ≥ 0,2, serigrafía línea ≥ 0,15, alto ≥ 1,0 mm, proporción 1:6, pad a serigrafía 0,15. No da fecha en la página.
- `jlcpcb.com/capabilities/pcb-assembly-capabilities`: Economic = una cara, 0402 mínimo, paso 0,4 mm, «edge rails / fiducials: not necessary». No da separación entre piezas ni a borde.
- `help/article/pcb-assembly-faqs-part-2`, P14: en Economic, pistas y componentes a > 0,3 mm del borde (se paneliza y se fresa con ±0,2).
- `help/article/terms-and-conditions-of-jlcpcb-assembly-service` §2.2: densidad media o baja de IPC-7351B (= patios de KiCad sin solape); §2.3: 2,5 mm del cuerpo al borde, que choca con P14 y con FAB-07 (sin resolver, preguntar a JLCPCB).
- Precio: `help/article/In-what-cases-will-there-be-charged-extra` (precio especial ≤ 102 × 102 mm). Por encima **no hay tarifa publicada**; `jlcpcb.com/quote` redirige a una aplicación JS que WebFetch no lee. Pedir el presupuesto al usuario.

**How to apply:** antes de buscar otra vez, mirar las filas de la tabla de reglas; para una cifra nueva, estas páginas. Ninguna habla de antenas que sobresalen del borde.
