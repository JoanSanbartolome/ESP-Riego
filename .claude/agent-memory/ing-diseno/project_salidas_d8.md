---
name: project-salidas-d8
description: Salidas vigentes (DEC-0003/0004/0014): BTT6050 + limitador común 3,5–4,9 A, sin válvula de referencia, límites de uso REL-11, rueda libre M7 montada; piezas descartadas y lecciones del bloque
metadata:
  type: project
---

**Estado vigente (2026-11-17, DEC-0014, `docs/02` v0.7):**

- DEC-0003: *high-side* BTT6050-1ERA (C534868); BTT6030-2ERA (C534865) segunda fuente; BSP752R (C112644) reserva. 24 V DC detrás de un limitador común (U1). Sin relé ni contacto libre.
- DEC-0004: fuente LED 24 V 5 A de fábrica; banda del limitador 3,5–4,9 A; pistas, bornes y retornos para 4,9 A.
- **DEC-0014: no hay válvula de diseño.** Una carga por salida, 1 A por salida, suma ≤ 3,5 A (límite de uso, no «12 válvulas de 0,25 A»). Tabla de límites de uso REL-11 en `salidas.md` §0 (R ≥ 30 Ω, I_min 80 mA ⇔ ≤ 218 Ω para la carga abierta en ON, ≤ 89 kΩ en OFF, fuga ≤ 0,65 mA, aislamiento del cable ≥ 400 kΩ). Los 156 Ω de la Bermad de DC (DEC-0002) son históricos; la instalada (S-390-3-D, 24 V AC alimentada en DC, DEC-0011) solo aparece como ejemplo.
- **D12–D17 (M7) montados** (sustituye el DNP de DEC-0008 punto 2): sin límite de inductancia; la comprobación es REL-03 (V_R, I_F(AV) = 1 A, corto 56 A × 62,5 µs = 0,098 A²s frente a I_FSM 3,75 A²s, fuga 50 µA < 84 µA). La validación pidió explícitamente I_FSM frente al pico y la duración del corto (VAL-0033-02).

**Why:** el usuario cambió los datos de partida de las salidas cinco veces (SPEC-0005…0034) y al final pidió no diseñar para una válvula.

**How to apply:** antes de tocar salidas, limitador o alimentación, leer DEC-0014 y `docs/02`; cualquier cálculo de salidas va con la carga como parámetro entre los límites de uso. Escribir «válvula concreta» como dato de diseño hace fallar el punto [juicio] de la checklist de esquema.

Piezas descartadas (estudio SPEC-0005), y por qué:
- BTS4140N: 0,2 A y entrada activa baja. VN7 y TPS1HC100: 12 V. NCV8460A: V_IH 3,25 V.
- VN5 y BSP762T: 41 V < 53,3 V de la SMBJ33A. BTS428L2: V_IN(T+) hasta 3,2 V y corto solo hasta 24 V.
- BTT6030-2ERA: 4 A por canal con los dos activos, k_ILIS 2240. AO3400A y SS14 en el bus: < 53 V.
- Sin stock: Z0109MN, IPS160HFTR, ISP752R, LT925, G3VM-61HR.

LED de canal (SPEC-0023): LED + 1 kΩ desde el GPIO IN_n, 1,5 mA. KT-0603R (C2286): ② del datasheet = cátodo = pad 1 (VAL-0022-01-01). Un LED en OUT enmascara la carga abierta en OFF.

Lecciones del bloque (`docs/diseno/salidas.md`):
- IS: R_SENSE 10 kΩ 1206 → R_IS 820 Ω al ADC (Fig. 52); el divisor acota el fallo sin diodo. Techo del pin: V_IS ≤ V_S (VAL-0023-01-03).
- BTT6050 p. 30, P_7.5.2: «I_IS(OL) = 8 mA» es 8 µA (errata).
- Separación de cada clase de red frente al hueco entre pads de las huellas (BTT OUT 0,62–0,735 mm): excepción de 0,6 mm (DEC-0008 punto 3, vigente).
- k_ILIS: interpolación logarítmica entre 50 mA (±50 %) y 0,5 A (±25 %), Tabla 9 p. 30; la corriente mínima del diagnóstico sale de I/k_max·812 Ω − 10 mV ≥ 18 mV.
- I_L5(SC) 38–56 A está en la Tabla 7, p. 22 (I_L28(SC) 22 A típ.). Cable del ensayo de corto del BTT: 16 mΩ/m, 1 µH/m (P_4.1.3): τ = 62,5 µs, independiente de la longitud.
- Pines «P_x.y.z» del BTT: la numeración no siempre cuadra en `pdftotext`; citar «Tabla N, p. X».

Relacionado: [[reference-fuentes-piezas]], [[reference-trucos-esquema]]
