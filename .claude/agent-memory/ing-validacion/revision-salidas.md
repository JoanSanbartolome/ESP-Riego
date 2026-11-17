---
name: revision-salidas
description: Cómo validar salidas.md (high-side BTT6050, IS al ADC, R_OL, rueda libre M7, límites de uso REL-11, umbrales de firmware): fórmulas cerradas, datos del datasheet y fallos típicos (enclavamiento térmico, clase de red frente a pads, aviso de suma con ± 7 %)
metadata:
  type: feedback
---

VAL-0023-01 (2026-11-07) y VAL-0034-01 (2026-11-17): las cifras gruesas cuadran siempre. Los fallos aparecen en el cruce con el layout, en los umbrales del firmware y en el comportamiento de protección del BTT.

**Por qué:** el autor fija clases de red sin mirar los huecos de las huellas, toma la carga mínima sin el calentamiento de la bobina y, en SPEC-0034, supuso que el BTT «conmuta por temperatura» (no lo hace: se enclava).

**Cómo aplicarlo:**
- **El BTT6050 se enclava** tras el apagado térmico, sin reintento (§6.5.2, p. 21; §7.3.5, p. 29). La subtensión sí se rearma sola (§6.2, p. 17). El I_L(RMS) de la Tabla 7 (p. 22) no implica conmutación autónoma.
- Desde DEC-0014, D12–D17 (M7) van montados y E_AS ya no aplica. M7 (`datasheets/M7.pdf`): I_FSM 30 A (8,3 ms) → I²t de 3,75 A²s. I_R de 5/50 µA a 25/125 °C y 1000 V. R_θJA 75 K/W solo con pads de 2 × 2″ (nota 2, p. 1). Fig. 2: ≈ 0,2 µA a 75 °C y ≈ 1–1,5 µA a 100 °C. Fig. 6: Z_th ≈ 11–12 K/W a 50 ms. Hay que renderizar la p. 2: el texto de las figuras sale desordenado.
- Límites de REL-11 (§0): carga mínima I_L ≥ 34,5 µA × k_max(I_L), con k interpolado en logaritmo entre 50 mA (1600 ± 50 %) y 0,5 A (1500 ± 25 %) → 79 mA; 17,5 V / 80 mA = 218 Ω. En reposo: R_L < R_OL,mín·(V_S − 6)/6. Aislamiento: (V_S − 4)/(84,3 µA − I_diodo).
- El aviso de suma por LIM_IMON (± 7 % y ± 36 mA) no separa 3,5 de 3,6 A: con el umbral de 3,3 A puede avisar desde ≈ 3,0 A. Mirar que §0 lo diga.
- BTT p. 30: k_ILIS ± 50/25/12/9/8 % a 0,05/0,5/1/2/4 A; V_S − V_OL(OFF) 4–6 V; I_L(OL) 4–25 mA; P_7.5.2 «8 mA» se lee como 8 µA.
- Huecos entre pads: PG-TDSO-14 propia, OUT→EP 0,735 mm; R_0805 0,80; C_0805 0,90; D_SMA 1,5 mm.
- Umbrales del firmware: bobina caliente a 17,5 V para la carga abierta en ON y fría a 30 V para la sobrecarga, con k interpolado y ± 10 mV del ADC.
- `kicad-cli sch export netlist` sobre una copia, y un script con `re` que trocee por `(net` y lea `(ref)(pin)(pinfunction)`: sale la polaridad K/A de cada diodo sin el MCP.

Relacionado: [[revision-alimentacion]], [[revision-estudios]].
