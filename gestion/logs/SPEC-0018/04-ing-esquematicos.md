---
spec: SPEC-0018
agente: ing-esquematicos
n: 04
fecha: 2026-11-05
estado: completado
---

# SPEC-0018 · 04 · ing-esquematicos

## Orden recibida

SPEC-0018 · rama spec/SPEC-0018-piezas-alimentacion (activa en C:\Users\josan\proyectos\KICAD_mcp) · Lee: gestion/informes/VAL-0018-01.md (hallazgo 03, y 04/05 para contexto) + docs/diseno/alimentacion.md §3.6 y §8 · Haz: corregir el CIN de U2 (LMR36520) en alimentacion.md: ≥ 4,7 µF efectivos a 24–30 V junto a U2, siguiendo la Tabla 8-1 (p. 18; 2 × 4,7 µF + 220 nF), sin mover C2 del nodo de entrada; actualiza lista de piezas y LCSC (preferir Basic) y aplica de paso 04 (C10 → C28323) y 05 (C3 → 220 nF C513710). Solo texto: no uses KiCad ni toques hardware/ (otro agente trabaja ahí). · Entrega: docs/diseno/alimentacion.md + log gestion/logs/SPEC-0018/04-ing-esquematicos.md. Brevedad: solo contrato de salida; log telegráfico.

## Contexto consultado

- `gestion/informes/VAL-0018-01.md` (03, 04, 05).
- `docs/diseno/alimentacion.md` §3.5, §3.6, §3.13.6, §7, §8, §9.
- `hardware/componentes/bloque-alimentacion.md` §3 (tabla de *derating*).
- `LMR36520.pdf` (SNVSBF0C): nota p. 17; Tabla 8-1 p. 18; §8.2.1.2.5 y ec. 8 p. 20; §8.2.1.2.7 p. 21.
- LCSC JSON (C381466, C28323, C513710); JLCPCB API `selectSmtComponentList` (tipo y stock; búsqueda «4.7uF 100V»).
- SimSurfing: `CL21B105KBFNNN.do` (DC bias, TCC), `CL32B475KCJZ4N.do` (rizado).

## Acciones

- `docs/diseno/alimentacion.md`:
  - cabecera: nota de revisión;
  - §3.5: filas C2/C7/C22 (C381466) y C3/C8 (C513710);
  - §3.6: filas CIN, CBOOT, CVCC; subapartados «CIN de U2» y «CVCC: C10»;
  - §3.13.6: C3 = 220 nF 0805 C513710;
  - §7: C22 en la línea C381466; C3 → C513710 0805; C10 → C28323 0805; viñeta de cambios;
  - §8: fila VIN_PROT → U2 (C7 + C22 junto a U2, C2 en el nodo de entrada, 1,0 A eficaz); fila nueva C10/C3;
  - §9: ALI-05.
- Sin KiCad; nada en `hardware/`.

## Decisiones y justificación

- CIN = C7 + C22, 2 × 4,7 µF 100 V X7R 1210 (C381466) + C8 220 nF. Peor caso 5,1 µF efectivos (30 V, 85 °C, −10 %): +8 %; con proxy KCIZNW a 60 °C, 4,9 µF (+4 %). Tabla 8-1, p. 18.
- C381466: Extended, pero línea ya existente (no añade cargo). JLCPCB: ningún 4,7 µF ≥ 100 V Basic (2026-11-05).
- I_RMS ≈ I_OUT/2 = 1,0 A con 2 A (ec. 8); ≤ 0,5 A por condensador; ΔT < 1 °C (SimSurfing, 1,07 A a 500 kHz → 0,95 °C).
- C10 → C28323 (Basic, JLCPCB 3,50 M; LCSC 0): 0,96 µF típ. a 60 °C; 0,85 µF con −10 % y 85 °C. Aceptado (VAL-0018-01-04).
- C3 → C513710 (misma línea que C8): 0,15–0,17 µF efectivos ≥ 0,1 µF. Sale C15725: una línea Extended menos.
- Referencia C22 provisional (siguiente libre tras C21); la fija la anotación de SPEC-0019.

## Verificación

- Sin cambios en KiCad: `verificar.py` no aplica.
- Checklist `esquema.md` v5 (solo puntos que toca el cambio):
  - Cálculos con fórmula, fuente y margen: cumple (§3.6, §3.13.6).
  - Tensiones nominales ≥ nodo: cumple (§3.5; 100 V ≥ 58,6 V y ≥ 2 × 30 V).
  - *Derating* DC y temperatura de cerámicos: cumple para C7/C22, C10, C3.
  - Campos de símbolo, huella existente (`C_0805_2012Metric`, `C_1210_3225Metric` oficiales): pendiente de SPEC-0019 (esquema).
  - Tabla de restricciones de layout: cumple (§8 actualizada).
  - Resto: no aplica (sin cambios).

## Pendiente

- jr-conformidad: actualizar `hardware/componentes/bloque-alimentacion.md` (§1 líneas C2/C6/C7 → + C22; C3 → C513710; C10 → C28323; recuento Extended/Basic; §3 puntos 3–5). Fuera de mi zona.
- SPEC-0019: dibujar C22; C3 y C10 con huella 0805 y nuevos LCSC.

## Notas para el siguiente agente

- C2 no forma parte del CIN de U2; no acercarlo a U2 en layout.
- C15 (VIN2 de U3) sigue en C15849 (1 µF X5R 0603); no se tocó.
