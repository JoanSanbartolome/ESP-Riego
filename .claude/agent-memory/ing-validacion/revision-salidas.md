---
name: revision-salidas
description: Cómo validar salidas.md (high-side BTT6050, IS al ADC, R_OL, E_AS, umbrales de firmware): fórmulas cerradas, datos del datasheet y fallos típicos (separación de clase de red frente a pads, carga mínima sin bobina caliente)
metadata:
  type: feedback
---

VAL-0023-01 (2026-11-07): las cifras gruesas cuadraban; los fallos estaban en el cruce con el layout y en los umbrales del firmware.

**Por qué:** el autor fija clases de red (Salidas ≥ 1 mm) sin mirar los huecos de las huellas, y toma la carga mínima de la válvula sin calentamiento.

**Cómo aplicarlo:**
- Fórmula cerrada de la ec. 5.1 con I_L = V_S/R_L: E = V_AZ·(L/R²)·[V_S − (V_AZ − V_S)·ln(1 + V_S/(V_AZ − V_S))]. Con V_AZ 66 V: 540·L/R² a 30 V, 331·L/R² a 24 V. La curva de la Fig. 12 (p. 13) empieza en 1 A (≈ 155 mJ).
- BTT6050 p. 30: k_ILIS ± 50/25/12/9/8 % a 0,05/0,5/1/2/4 A; V_S − V_IS(RANGE) de 1–3,5 V **solo a I_IS = 6 mA** (la cota física es V_IS ≤ V_S, p. 6); V_S − V_OL(OFF) 4–6 V; I_L(OL) 4–25 mA. La Fig. 52 (p. 47) pone R_IS en el lado del ADC.
- Huecos entre pads: PG-TDSO-14 propia, OUT→EP 0,735 mm y OUT→NC 0,62 mm; KiCad R_0805 0,80, C_0805 0,90, R_1206 1,80 mm. Se cruzan con FAB-03.
- Umbrales del firmware: recalcularlos con la bobina caliente a 17,5 V (carga abierta en ON) y fría a 30 V (sobrecarga), con k interpolado en log y ± 10 mV del ADC.
- Datasheet de PDF de texto: `pdftotext -layout` separado por `\f` da las páginas; las tablas desordenadas, renderizarlas.

Relacionado: [[revision-alimentacion]], [[revision-estudios]].
