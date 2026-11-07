---
spec: SPEC-0023
agente: ing-esquematicos
n: 03
fecha: 2026-11-07
estado: completado
---

# SPEC-0023 · 03 · ing-esquematicos

## Orden recibida

«SPEC-0023 · rama spec/SPEC-0023-calculos-salidas (activa) · Lee: gestion/informes/VAL-0023-01.md + docs/diseno/salidas.md + tu log gestion/logs/SPEC-0023/01-ing-esquematicos.md · Haz: corregir en salidas.md las dos M (afectan a SPEC-0024): -01, separación de la clase Salidas: fija en §11 la excepción de 0,6 mm dentro de las huellas U7–U12, R57–R62 y C33–C38 y 1 mm en el resto de OUT_n, o pasa R_OL y C_OUT a 1206 si hay pieza Basic sin empeorar el coste (DEC-0007), justificándolo; -02, recalcula la fila de corriente mínima de §3.2 con R a 20 °C (156 Ω), la temperatura de la bobina en marcha (justificada o supuesta y marcada) y 17,5 V, y ajusta el umbral de carga abierta en ON de §12 (≈ 18 mV, o deja el margen como punto a medir en §13). Corrige también las B -03 a -06 con lo que propone el informe. Mantén la coherencia de §0, la lista de piezas y la trazabilidad. Sin KiCad · Entrega: docs/diseno/salidas.md + log gestion/logs/SPEC-0023/03-ing-esquematicos.md con cada hallazgo y su corrección.»

- Rama `spec/SPEC-0023-calculos-salidas` ✔. Sin KiCad: no aplica la comprobación de `.lck`.

## Contexto consultado

- `gestion/informes/VAL-0023-01.md`; `docs/diseno/salidas.md`; log 01.
- `docs/02` FAB-03 y REL-10; `estudio-salidas.md` §1.2 (l. 108, 135).
- BTT6050-1ERA Rev. 1.00: p. 6 (Tabla 3, P_4.1.12, P_4.1.19), p. 8 (Tabla 4, V_S(OP)), p. 15 (Tabla 6, I_L(NOM)), p. 22 (Tabla 7), p. 24 (Tabla 8), p. 27 (§7.3.3.1, Fig. 24), p. 30 (Tabla 9, renderizada: P_7.5.2 «I_IS(OL) = 8 mA»), p. 47 (Fig. 52, Tabla 11).
- Script de cálculo en el *scratchpad* (`s23b_calc.py`).

## Acciones

Todo en `docs/diseno/salidas.md`:

| Hallazgo | Corrección | Secciones |
|---|---|---|
| **-01 (M)** separación `Salidas` | Excepción fijada: 1 mm en pistas, polígonos y pads fuera de las huellas; **0,6 mm dentro de U7–U12, R57–R62 y C33–C38 y en sus pads** (regla propia del DRC). Nota 1 con los huecos (BTT 0,735 mm al EP y 0,62 mm a NC 9/13; R_OL 0,80; C_OUT 0,90), tensión ≤ 75 V (V_DS(AZ), p. 15) e IPC-2221 B2 (0,6 mm hasta 100 V). 1206 descartado: no quita la excepción (la impone el BTT, DEC-0003) y en C_OUT cambiaría la línea existente C513710 por una nueva (DEC-0007). Lista de piezas sin cambios | §0, §11 (filas OUT_n, C_OUT, R_OL y nota 1), §13.8, §14 FAB-03 |
| **-02 (M)** corriente mínima y umbral de carga abierta en ON | Fila nueva: 156 Ω a 20 °C → **205 Ω a 100 °C (supuesto marcado:** 40 °C de arqueta + 60 K de una bobina de ≈ 4 W en continuo) + 3,5 Ω de cable, 17,5 V → **84 mA**; k 1578 ± 44,4 % → V_ADC ≥ 29,9 mV, **≥ 19,9 mV con el ADC**. Sensibilidad: 80 °C → 22,0 mV; 120 °C → 18,1 mV. Carga abierta: I_IS(OL) leído como 8 µA (el PDF pone 8 mA, incoherente con I_IS(FAULT) ≥ 6 mA y con I_L(OL)/k = 2,5–16 µA) → ≤ 16,6 mV. **Umbral: 18 mV** (márgenes 1,4 / 1,9 mV) y **punto a medir en §13.7** (R de la bobina en caliente, V_ADC con válvula a 17,5 V y con borne abierto) | §0, §3.2, §3.4, §12, §13.7, §14 REL-10 |
| -03 (B) V_S − 1 V | §3.1: la cota de 1 V solo vale con I_IS = 6 mA; techo = V_IS ≤ V_S (P_4.1.19, p. 6). Tabla de fallo con columna V_IS = V_S: 2,32 V a 30 V, 2,83 V a 36,7 V, 4,11 V en el impulso (inyección 0,8 mA); R_SENSE 77 / 115 mW (31–46 %); margen al pin ≥ 0,68 V | §0, §3.1, §3.2, §13.2, §14 |
| -04 (B) E_AS | «Cumple en la cota baja de L; en la alta (3 %), margen dentro de la incertidumbre de la figura»; curva extrapolada bajo 1 A no especificada; condicionado a medir L (§13.1) | §0, §5, §14 REL-03 |
| -05 (B) sobrecarga a 30 V | Nota en §12: 450 mV vale sin falso aviso con 0,56 A a ≤ 24,5 V (≤ 422 mV). A 30 V, 2 válvulas de diseño (0,69 A) dan ≤ 478 mV y 1 A ≥ 473 mV: no hay umbral fijo; se prioriza avisar con ≥ 1 A. Bermad a 30 V: ≤ 337 mV, sin falso aviso. La calibración por canal lo resuelve | §12, §14 |
| -06 (B) citas | (a) «abre a > 15 V» → «muy por debajo de su tensión de apertura» (`estudio-salidas.md` §1.2); (b) §0: 0,08 → 0,10 V a 30 V (y «a 24 V» en la nota de JP1); (c) desmagnetización 14 → **11–12 ms** (t = τ·ln(1 + R·I/(V_DS(AZ) − V_S)), τ en frío 18–19 ms, 66 V); 9–10 ms a 75 V; (d) R_IS 1,2 kΩ: la Fig. 52 usa la misma topología; motivo real, el divisor (3,16 V con V_S − 1 V, 3,27 V con V_S a 30 V); (e) V_S(OP) → Tabla 4, p. 8; I_L(NOM) → Tabla 6, p. 15 | §0, §2.1, §3.1, §3.3, §5 |

## Decisiones y justificación

- Excepción de 0,6 mm frente a 1206: la excepción es inevitable por el BTT; 1206 solo añadiría coste en C_OUT. Contradice la letra de FAB-03 (M) → **propuesta de DEC** (Pendiente).
- Temperatura de la bobina: sin dato de Bermad; supuesto de 100 °C marcado en §3.2 y medible en el prototipo.
- I_IS(OL) = 8 µA: errata evidente del datasheet; anotado con el razonamiento en §3.2.
- Umbral de sobrecarga: se mantiene 450 mV (REL-10 obliga a avisar con > 1 A); falso aviso a 30 V solo con válvulas de 0,25 A, aceptado y documentado.

## Verificación

- `verificar.py`: no ejecutado (orden sin KiCad; sin cambios en `hardware/`). ERC/DRC/paridad: sin objeto.
- Recalculado con script propio: cifras de VAL-0023-01 reproducidas (85,3 mA → 30,5 mV sin cable; 0,686 A → 468 mV; desmagnetización 11,1–11,5 ms; divisor 1,2 kΩ 3,16 V).
- Repaso de `gestion/checklists/esquema.md` en los puntos tocados:
  - Cada valor con fórmula, fuente y margen: **cumple** (§3.2, §5, §11 nota 1, §12).
  - Tabla de restricciones de layout coherente con las huellas: **cumple** con la excepción (nota 1); pendiente de DEC.
  - IS acotada ≤ 3,1 V con el límite físico: **cumple** (2,32 V a 30 V).
  - Umbrales de diagnóstico con carga mínima y máxima: **cumple con condición** (margen de la carga abierta en ON a medir, §13.7; sobrecarga a 30 V documentada).
  - E_AS: **cumple con condición** (medida de L, sin cambios).
  - Lista de piezas y totales: sin cambios (43 R, 20 C).

## Pendiente

- **Coordinador / usuario (DEC):** fijar la excepción de FAB-03: `Salidas` ≥ 1 mm salvo 0,6 mm (IPC-2221 B2, ≤ 100 V) dentro de las huellas cuyo paso no lo permite (U7–U12, R57–R62, C33–C38). Necesaria antes del layout.
- **Usuario (prototipo):** §13.7 (temperatura de la bobina y margen del umbral de 18 mV); REL-03, medir L (sin cambios).
- **Validación:** revalidar -01 a -06 (nivel ligero).
- **Propuesta para el datasheet/ficha BTT6050-1ERA:** anotar la errata de P_7.5.2 (I_IS(OL) = 8 µA).

## Notas para el siguiente agente

- Layout: la regla de 0,6 mm de `Salidas` se limita a los pads y patios de U7–U12, R57–R62 y C33–C38; fuera, 1 mm.
- Firmware (SPEC-0025): umbral de carga abierta en ON 18 mV; sobrecarga 450 mV (falso aviso posible a > 24,5 V con 2 válvulas de 0,25 A).
