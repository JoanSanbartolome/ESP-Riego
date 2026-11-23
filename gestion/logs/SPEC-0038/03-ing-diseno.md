---
spec: SPEC-0038
agente: ing-diseno
n: 03
fecha: 2026-11-23
estado: completado
---

# SPEC-0038 · 03 · ing-diseno (paso 3)

## Hecho

- **Propuesta de jr-conformidad** (`scratchpad/propuesta-docs/`): revisada contra `02-jr-conformidad.md`, `fabricacion/v2.0-prueba/bom.csv` y `campos-alimentacion.csv`, y aplicada entera.
  - `alimentacion.md`: C3 vuelve a 220 nF C513710; D1, D2 y D3 pasan a Hongjiacheng (§0, §3.3, §3.5, §3.13.6, §7, §10.8 y Anexo A).
  - `estudio-coste.md`: §0, §2 y §9 con 41,96 / 23,95 $ y P4 con cifra. `estudio-coste-bom.csv` al 2026-11-23, con la columna `montaje`.
- **Añadido a `alimentacion.md`** con las fichas de P1 (VAL-0037-01-09):
  - §3.3: P_D1 de 5,7 mW frente a 350 mW;
  - §3.4: Vc de 53,3 V a 11,26 A y fuga de 5 µA de la nueva D2;
  - §3.13.6: fuga de D3, 10 mA a 100 °C: 0,24 W, +19 °C, sin embalamiento con 60 °C de aire; 2,8 mV en LIM_IMON.
- **`salidas.md`:** l. 371 sin «; línea de C3». En la l. 381, C28233 pasa a 12 por placa y C513710 queda para C3 y C8.

## Verificación

- **Estudio de coste:** `estudio-coste-bom.csv` coincide con `bom.csv` en las 187 referencias, en código, precio de 5 y 50 uds, tipo y montaje. Tiene 54 líneas, 20 Extended con cargo y 585 juntas SMT.
- **Coste por placa con el modelo de §1 (E2):**
  - 5 uds: 26,40 + 20 × 3,07 / 5 + 585 × 0,0016 + 9,71 / 5 + 2 / 5 = **41,96 $**;
  - 50 uds: 21,29 + 61,4 / 50 + 0,94 + 9,71 / 50 + 15 / 50 = **23,95 $**;
  - la tabla de diferencias de §9 cuadra.
- **`docs/diseno`:** sin menciones de C3 en C28233 ni de los códigos antiguos de D1–D3 como pieza principal. `hardware/v2` no se toca en este paso.

## Para validación

- El ahorro de P4 se mide frente a los precios de TI del 2026-11-20 que trae el CSV (0,3967 / 0,2645 $). Con los del 2026-11-23 (0,3977 / 0,2651 $), con 50 uds sale 0,08 $ en lugar de 0,07; el total no cambia.
