# Bloque de salidas: 6 canales *high-side* BTT6050-1ERA y bornes (SPEC-0023)

**Estado:** **SPEC-0038 (DEC-0018 P3): C_VS y C_OUT (C27–C38) pasan a 100 nF 100 V X7R 0805 Basic (C28233), §4.3, §4.4 y §9**. Revisado tras VAL-0023-01 (M-01, M-02, B-03…B-06); actualizado en SPEC-0025 (cambios propuestos en SPEC-0024 y DEC-0008); **rehecho en SPEC-0034 sin válvula de referencia (DEC-0014): límites de uso en §0, rueda libre montada en §5**. **Autor:** ing-esquematicos; ing-diseno (SPEC-0025, SPEC-0034) · **Fecha:** 2026-11-07; 2026-11-13; 2026-11-17.
**Requisitos:** REL-01, REL-03…REL-11; además ALI-01, ALI-12, ALI-13, FAB-03, FAB-07, FAB-09 y §6 de `docs/02` v0.7; DEC-0003, DEC-0004, DEC-0006, DEC-0007, DEC-0008 (salvo su punto 2), DEC-0014.
**Precios y stock:** API de JLCPCB (`selectSmtComponentList`), consulta del 2026-11-06. El tipo Basic/Extended y los códigos LCSC definitivos fueron confirmados por jr-conformidad el 2026-11-10 (SPEC-0024). Stock de §9 del 2026-11-12 (`hardware/componentes/stock-salidas.csv`, SPEC-0025).

> Datasheets (páginas del PDF):
> - **BTT:** Infineon BTT6050-1ERA Rev. 1.00, 2019-03-09 (`hardware/componentes/datasheets/BTT6050-1ERA.pdf`). En pp. 23-32 el pie dice «*Target Data Sheet 30*»: se cita la página del PDF.
> - **BTT30:** BTT6030-2ERA Rev. 1.00 (`datasheets/BTT6030-2ERA.pdf`).
> - **S:** ESP32-S3 Series Datasheet v2.2 (espressif.com): tabla 5-4, p. 65; tabla 5-6, p. 66.
> - **WJ:** WJ500V-5.08-2P (ficha y `datasheets/WJ500V-5.08-2P.pdf`).
> - **M7:** MDD «M1 THRU M7», Rev. 2025A5 (`datasheets/M7.pdf`): tabla de la p. 1 y figuras 1–6 de la p. 2.
> - `alimentacion.md` (BUS_24V, U1 TPS26632, JP1) y `mcu.md` (§9.2, §10.2, Anexo C).

## 0. Resumen

```
BUS_24V ─┬─ C_VS ─ GND            (por canal; C45/C46 a granel, uno por borde)
         ├─ VS(tab) U(n) BTT6050 OUT ─┬─ OUT_n ─ C_OUT ─ GND ─ J(n) pin 1   ── carga (1) ── J(n) pin 2 = GND
         └─ R_OL 47 kΩ ───────────────┘          (D M7, rueda libre: ánodo GND → cátodo OUT_n)
GPIO IN_n ─┬─ R_PD 100 kΩ ─ GND ;  ├─ R_LED 1 kΩ ─ LED ─ GND ;  └─ R_IN 10 kΩ ─ IN
OUT_DEN (GPIO38) ─ R_PD 100 kΩ ─ GND ;  ─ 6 × R_DEN 10 kΩ ─ DEN de cada BTT
IS (pin) ─ R_SENSE 10 kΩ 1206 ─┬─ IS_n → ADC1 (6 dB)
                               ├─ R_IS 820 Ω ─ GND
                               └─ C_IS 100 nF ─ GND
BTT GND (pin 3) ─ GND directo (sin R_GND ni diodo, §4.4)
```

| Función | Pieza principal | Alternativa | Requisito |
|---|---|---|---|
| *High-side* (×6) | Infineon BTT6050-1ERA, C534868 (Extended, 1 628) | BTT6030-2ERA, C534865 (otro *routing*, §10) | REL-01, REL-03, REL-08 |
| Borne (×6) | Kangnex WJ500V-5.08-2P, C8465 | — (ficha existente; misma línea que J1) | REL-05, REL-06, REL-09, FAB-07 |
| Medida IS | R_SENSE 10 kΩ 1206 + R_IS 820 Ω + C_IS 100 nF; **el divisor acota V_ADC sin diodo** | — | REL-10 |
| Carga abierta en OFF | R_OL 47 kΩ 0805 de BUS_24V a OUT_n | 56 kΩ (§3.3) | REL-10 |
| Entradas | R_IN = R_DEN = 10 kΩ; R_PD 100 kΩ en cada IN y una en OUT_DEN | — | REL-03, REL-04 |
| LED de canal | KT-0603R (C2286, Basic) + 1 kΩ desde el GPIO IN_n | KT-0603YG (C2289) | REL-07 |
| Desacoplo | C_VS y C_OUT 100 nF 100 V X7R 0805 (Samsung CL21B104KCFNNNE, C28233, Basic; SPEC-0038); 2 × 4,7 µF 100 V 1210 (C381466, línea existente) | — | — |
| Rueda libre (×6) | MDD M7, C95872 (Basic), **montada** (DEC-0014) | — | REL-03 (§5) |

### Límites de uso de las salidas (REL-11)

La placa no se diseña para una válvula concreta (DEC-0014): admite cualquier carga que cumpla esta tabla. «Entrada» es la tensión del borne J1. Las cifras salen de las secciones citadas; el texto de la serigrafía, en §8.

| Límite | Valor | Origen | Si se supera |
|---|---|---|---|
| Tensión de salida | La de la entrada menos ≈ 0,1–0,5 V: **18–30 V DC** (24 V ± 2 % con la fuente en su ajuste de fábrica). La carga tiene que admitir la tensión máxima de la entrada | ALI-01, REL-02; `alimentacion.md` §1 | Por encima de 30 V la carga recibe la tensión de la entrada (aviso de sobretensión a 32,5 V, ALI-09; U1 la recorta a 32–35 V durante ≤ 162 ms) |
| Tipo de carga | **Bobina DC** (electroválvula, relé o contactor de continua). Una bobina AC alimentada en continua, solo si su resistencia DC cumple la fila de resistencia mínima y su fabricante admite DC. Sin PWM. Nada de 230 V AC ni de fuentes externas en el borne | REL-02, REL-03, REL-11; DEC-0014 | Bobina AC en DC: disipa V²/R_DC, varias veces lo que en alterna (daño de la bobina, fuera de la placa). Solenoide biestable (*latching*): no conmuta, necesita invertir la polaridad. Lámpara, motor o carga capacitiva: el pico de arranque puede llevar el BTT a su limitación (22–56 A, Tabla 7, p. 22) o disparar U1, y el diagnóstico no vale. **230 V AC o fuente externa en el borne:** en el semiciclo o la polaridad negativos, la fuente queda en corto por D12–D17 (I_FSM 30 A); en el positivo, por encima de V_S, la corriente vuelve al bus por el diodo interno del BTT (corriente inversa sin protecciones, §5.4, p. 14) y la tensión supera V_S(LD) = 65 V (Tabla 3, p. 6). Se destruyen el diodo y el BTT, y la tensión puede llegar al bus y al resto de la placa |
| Cargas por salida | **1** | REL-05, DEC-0014 | Las corrientes se suman (el límite de 1 A es del total) y la desconexión de una de ellas no se detecta (§3.3) |
| Corriente continua por salida | **≤ 1 A** a la tensión máxima de la entrada | REL-05. La soportan el M7 (I_F(AV) 1 A, p. 1; §5.2), el BTT (T_J 77 °C a 60 °C, §6), la pista (ΔT ≈ 1 °C, §4.2) y la IS (lineal hasta 1,73 A, §3.2) | Aviso de sobrecarga del firmware, sin cortar (seguro a ≥ 1 A, §12). Por encima de ≈ 1,7 A la IS satura; a ≥ ≈ 4,0 A (60 °C) el BTT se apaga y se enclava por temperatura (REL-08). El diodo pasa de su I_F(AV) en cada apagado (impulso dentro de su I_FSM) |
| Suma de las salidas activas a la vez | **≤ 3,5 A** | ALI-12, ALI-13: U1 no corta por debajo de 3,86 A (`alimentacion.md` §3.13.2) | Aviso del firmware por LIM_IMON: seguro a ≥ 3,6 A y puede saltar desde ≈ 3,0 A por la tolerancia de la medida (§12). Por encima de 3,86 A U1 puede cortar el bus: se apagan todas las salidas y el firmware rearma (REL-08); si la sobrecarga sigue, vuelve a cortar |
| Resistencia mínima de la carga (bobina + cable, a su temperatura más baja) | **≥ 30 Ω** (30 V / 1 A). Para una bobina de cobre que pueda estar a −10 °C: ≥ 34 Ω a 20 °C | R = V_máx (ALI-01) / I_máx (REL-05); α_Cu = 0,00393 /K, −10 °C (§5 de `docs/02`) | Como la fila de 1 A. Con 30 Ω y la fuente en su ajuste de fábrica (24,5 V), 0,82 A |
| Corriente mínima para detectar la carga abierta con la salida encendida | **≥ 80 mA** con la entrada a 18 V y la bobina caliente ⇔ **R_carga (caliente) + R_cable ≤ 218 Ω**. Para una bobina que llegue a 100 °C: ≤ 166 Ω a 20 °C (≥ 0,145 A a 24 V) | §3.2: k_ILIS (Tabla 9, p. 30), ADC ± 10 mV (S tabla 5-6), umbral de 18 mV (§12) | La lectura puede quedar por debajo de 18 mV: aviso falso de «carga abierta» con la carga conectada. El firmware avisa de «carga baja» (§12); la calibración por canal baja el mínimo |
| Resistencia máxima para detectar la carga abierta en reposo | R_carga + R_cable ≤ 89 kΩ (entrada a 18 V) | §3.3: V_S − V_OL(OFF) 4–6 V (P_7.5.1, p. 30), R_OL 47 kΩ − 1 % | La carga presente se lee como abierta en reposo. Cualquier carga que cumpla la fila anterior queda × 400 por debajo |
| Fuga por la carga en reposo | **≤ 0,65 mA** a 30 V (0,79 mA a 36,7 V con JP1 cerrado); ≤ 0,14 V sobre una carga de ≤ 218 Ω. Solo con el bus habilitado (riego o comprobación; siempre, con JP1 cerrado) | REL-10 (≤ 1 mA); §3.3 | Una carga que reaccione a menos de 1 mA (indicador LED, carga electrónica, relé de alta impedancia) puede lucir o quedar activada en reposo: fuera de uso |
| Cable: sección | La que admite el borne, AWG 30–14 (hasta 2,08 mm²); recomendada **≥ 0,5 mm²** | WJ500V (WJ); 1 A por salida | Sección menor: más caída y más resistencia dentro de la fila de 218 Ω |
| Cable: longitud y aislamiento | **Sin límite propio de la protección** (el corto lo prueba `docs/02` §6 con ≥ 10 m; la energía del cable va al diodo, §5.3). Lo limitan: R_cable (ida y vuelta) = 2·ℓ·0,0175/S Ω (0,07 Ω por metro de tendido con 0,5 mm²) dentro de la fila de 218 Ω, y la caída que admita la válvula (recomendado ≤ 5 % de R_carga). Aislamiento del cable (humedad) **≥ 400 kΩ** | §3.3, §5.3, §5.4 | Caída excesiva: la válvula puede no abrir (dato de la válvula). Aislamiento por debajo de 160–400 kΩ: en reposo, el cable cortado se lee como «carga presente»; con la salida encendida sí se detecta |

Ejemplos, no datos de diseño: una válvula de 24 V DC de 0,25 A (96 Ω) cumple todas las filas. Una bobina de 24 V AC alimentada en continua con R_DC = 36–42 Ω (dato de ficha, sin medir; DEC-0011) toma 0,57 A (42 Ω, 24 V) a 0,94 A (36 Ω a −10 °C, 30 V): cabe en 1 A por salida, la suma deja 3–6 encendidas a la vez según la tensión y la temperatura (6 × 0,57 A = 3,43 A; 3 × 0,94 A = 2,84 A), y en continua disipa 14–16 W a 24 V, que tiene que admitirlo la válvula.

Resultados clave:

- **IS (REL-10):** V_ADC ≤ **2,32 V a 30 V** en fallo con la cota física V_IS ≤ V_S (≤ 2,83 V hasta 36,7 V, la V_BR mínima de la TVS), siempre por debajo de VDD mín. (3,211 V): **no entra corriente al pin** del ESP32-S3. Lectura lineal hasta ≥ 1,7 A con el bus a 17,5 V; 547 mV a 1 A.
- **Carga abierta en ON:** umbral de **18 mV**. La carga abierta da ≤ 16,6 mV y una carga de ≥ 80 mA (límite de uso) ≥ 18,4 mV en el peor caso, ADC incluido (§3.2).
- **Carga abierta en OFF:** fuga por la carga **≤ 0,64 mA a 30 V** (0,79 mA a 36,7 V) ≤ 1 mA; ≤ 0,14 V sobre una carga de ≤ 218 Ω. Detección con la carga presente hasta 89 kΩ y de la carga ausente con un aislamiento del cable ≥ 394 kΩ (fuga máxima del M7) a 17,5 V (§3.3, §5.4).
- **Rueda libre (REL-03, §5):** D12–D17 (M7) montados. La energía de la bobina no pasa por el BTT (≤ 1,5 mJ de conmutación): **sin límite de inductancia**. V_RRM 1000 V frente a ≤ 53,3 V; I_F(AV) 1 A = REL-05; en un corto del cable, ≤ 56 A durante τ ≤ 62,5 µs: 0,098 A²s frente a 3,75 A²s de la I_FSM (× 38); fuga ≤ 50 µA < 84 µA del presupuesto de R_OL. La carga se desmagnetiza en 2,5–3,7·L/R.
- **Layout (FAB-03):** clase `Salidas` con 1 mm de separación, salvo **0,6 mm dentro de las huellas U7–U12, R57–R62 y C33–C38**, que no permiten 1 mm (§11). Fijada por DEC-0008.
- **Térmica:** T_J = 77 °C a 1 A y 60 °C (R_thJA 50 K/W, con 300 mm² de cobre en VS). Sin enclavamiento hasta ≈ 4,0 A a 60 °C; a 4,57–4,9 A el BTT llega al apagado térmico y se enclava (previsto en DEC-0004 y REL-08).
- **Piezas nuevas:** ningún símbolo ni huella; las del BTT6050 y el WJ500V existen (`esp-riego`). Líneas de BOM nuevas: C534868 (Extended), tres resistencias Basic (C17902, C17713, C23253) y, desde SPEC-0034, el M7 (C95872, Basic) de D12–D17.

## 1. Datos de partida

| Dato | Valor | Origen |
|---|---|---|
| Bus de salidas | `BUS_24V` (salida de U1): 18–30 V en el borne (ALI-01) → ≈ 17,5–30 V en el bus; *clamp* de U1 a 32–35 V durante ≤ 162 ms; con JP1 cerrado, hasta la OVP de la fuente (33,6 V supuestos) y la V_BR de la TVS (36,7 V mín.); pico de 53,3 V (Vc) solo durante un impulso | `alimentacion.md` §1, §3.13.1, §3.13.9 |
| Limitador común | U1: I_OL = 3,86–4,57 A, *fast-trip* 2 × I_OL, *latch-off*; habilitación LIM_EN, fallo LIM_FLT, medida LIM_IMON | `alimentacion.md` §3.13 |
| Carga por salida | Una carga (bobina DC), como parámetro: de la resistencia mínima que da 1 A a 30 V a la carga mínima que detecta el diagnóstico (límites de uso de §0). Sin válvula de referencia | REL-05, REL-11, DEC-0014 |
| Parámetro de la placa | 1 A continuo por salida; suma de las activas ≤ 3,5 A; pista, borne y retorno para 4,9 A | REL-05, ALI-12, DEC-0004 |
| Cable de campo | ≥ 10 m (prueba de corto de §6) | `docs/02` §6 |
| Pines | IN1–6: GPIO11, 12, 13, 15, 16, 17; OUT_DEN: GPIO38; IS1–6: GPIO4–9 (ADC1_CH3–CH8) | `mcu.md` §9.2 |
| GPIO | V_OH ≥ 0,8·VDD = 2,64 V; fuga ≤ 50 nA; máximo VDD + 0,3 V; VDD = 3,211–3,389 V | S tabla 5-4, p. 65; `mcu.md` §1 |
| ADC1 | ATTEN2 (6 dB): 0–1600 mV, ± 10 mV; ATTEN3 (12 dB): 0–2900 mV, ± 50 mV (con 100 nF en el pin) | S tabla 5-6, p. 66 |
| Ambiente | 50 °C + 10 °C en la caja = **60 °C**; mínimo −10 °C (resistencia mínima de la carga) | §5 de `docs/02`, checklist de esquema |

**Nota sobre «U5» y «U6» de `estudio-salidas.md`:** en la tabla de datos de entrada de ese estudio (línea 31), U5 y U6 son identificadores de observaciones de VAL-0004-01, no referencias de piezas. Este documento no los usa como designadores: U5 y U6 son el ESP32-S3 y el USBLC6 (`mcu.md` §11), y los *high-side* son U7–U12.

## 2. *High-side* y entradas (REL-03, REL-04)

### 2.1 Pieza

BTT6050-1ERA (DEC-0003): V_S(OP) 5–48 V (Tabla 4, p. 8), V_S(LD) 65 V (Tabla 3, p. 6), R_DS(on) ≤ 100 mΩ a 150 °C (P_5.5.1, p. 15), I_L(NOM) 4,5 A (Tabla 6, p. 15), I_L5(SC) 38–56 A (Tabla 7, p. 22), entradas para 3,3 V (p. 2). Pinout: 3 GND, 4 IN, 5 DEN, 6 IS, 10-12 OUT, *tab* VS; NC 1, 2, 7, 8, 9, 13, 14 (Tabla 2, p. 4). Símbolo `esp-riego:BTT6050-1ERA` y huella `esp-riego:Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm` (con 10 vías de 0,3 / 0,6 mm en el EP, numeradas 15, desde SPEC-0024; §11).

### 2.2 Niveles de entrada

Datos: V_IN(H) ≥ 2,0 V, V_IN(L) ≤ 0,8 V, I_IN(H) ≤ 25 µA, I_IN(L) ≥ 1 µA a 0,8 V (Tabla 10, P_8.4.1–8.4.5, p. 34); DEN igual (P_8.4.6–8.4.10). Máximos: V_IN, V_DEN ≤ 6 V; I_IN, I_DEN ≤ ± 2 mA (Tabla 3, p. 6).

| Comprobación | Cálculo | Resultado |
|---|---|---|
| IN alto | V_IN ≥ V_OH − I_IN(H)·R_IN = 2,64 − 25 µA × 10,1 kΩ | **2,39 V** ≥ 2,0 V (margen 0,39 V); con VDD = 3,211 V: 2,32 V ✔ |
| IN alto con el LED (§7) | 1,4 mA de LED + 33 µA de R_PD + 25 µA: la V_OH de 2,64 V la garantiza S con 40 mA típicos (tabla 5-4); con 1,5 mA la caída es de decenas de mV | ≥ 2,3 V ✔ |
| IN bajo, GPIO en Z (REL-04) | 50 nA × 100 kΩ; la corriente interna de IN (≥ 1 µA) tira hacia abajo | **≤ 5 mV** ≪ 0,8 V ✔ (`mcu.md` §10.2) |
| DEN común (6 entradas) | Cada R_DEN lleva su I_DEN(H) ≤ 25 µA: V_DEN ≥ 2,39 V. Carga del GPIO38: 6 × 25 + 33 = 183 µA | ✔ (`mcu.md` §9.2) |
| Corriente con el bus apagado e IN alto | BTT sin alimentar: (3,3 − 0,6 V)/10 kΩ | ≤ 0,27 mA ≤ 2 mA ✔ |
| Pérdida de la masa del BTT | R_IN y R_DEN limitan la corriente hacia el GPIO a ≤ (30 − 3,3)/10 kΩ = 2,7 mA (fallo); Infineon recomienda 10 kΩ para esto (§6.1, p. 17; Tabla 11, p. 47) | Aceptado (caso de fallo) |

- R_IN = R_DEN = R_SENSE = 10 kΩ: valor recomendado (§6.4, p. 19; Tabla 11, p. 47-48).
- R_PD = 100 kΩ (C25803) en el lado del GPIO de cada R_IN, y una sola en OUT_DEN: coherente con `mcu.md` §10.2. Con JP1 cerrado, son la única barrera de REL-04 (DEC-0006).

### 2.3 Retroalimentación del bus apagado (checklist de esquema, `alimentacion.md` §10.7)

- IN y DEN solo tienen protección ESD hacia GND (Fig. 28, §8.1-8.2, p. 33; Fig. 14, p. 17): no hay camino de IN/DEN a VS. Con LIM_EN bajo e IN/DEN altos, el bus no se alimenta.
- IS tiene un diodo hacia VS (Z_IS(AZ), Fig. 20, p. 23), pero el nodo IS solo lo excita el propio BTT: R_IS va a GND y el ADC es una entrada. No hay fuente que lo suba por encima de VS.
- **Prototipo:** con LIM_EN bajo, IN1–6 y OUT_DEN altos, medir BUS_24V ≤ 0,5 V.

## 3. Diagnóstico (REL-10)

### 3.1 Medida IS: topología

Datos del BTT (Tabla 9, p. 30): k_ILIS = 1600 ± 50 % (50 mA), 1500 ± 25 % (0,5 A), ± 12 % (1 A), ± 9 % (2 A), ± 8 % (4 A); I_IS(FAULT) = 6 / 15 / 40 mA; V_S − V_IS(RANGE) = 1–3,5 V (saturación: el pin IS es una fuente de corriente hasta V_S − 3,5 V; la cota de 1 V solo está especificada con I_IS = 6 mA, y aquí circulan 1,3–3,3 mA, así que **como techo se usa el límite físico V_IS ≤ V_S** del máximo absoluto, P_4.1.19, p. 6; Fig. 46, p. 44); fuga con DEN bajo ≤ 1 µA; I_IS sin carga ≤ 2 µA (Fig. 44, p. 43). Máximo del pin IS: −0,3 V…V_S, −25…50 mA (Tabla 3, p. 6).

Elección: **IS → R_SENSE (10 kΩ, 1206) → nodo del ADC, con R_IS = 820 Ω y C_IS = 100 nF a GND en ese nodo.** Toda I_IS circula por la serie R_SENSE + R_IS, así que:

- en funcionamiento normal, V_ADC = I_IS · R_IS (transimpedancia de 820 Ω) y V_IS = I_IS · 10,82 kΩ;
- en fallo, el pin IS satura (entre V_S − 3,5 V y V_S) y R_SENSE/R_IS es un divisor que acota V_ADC. **No hace falta diodo de *clamp*:** un Schottky a +3V3 recortaría a 3,39 + 0,45 = 3,84 V, por encima de 3,1 V, y además inyectaría corriente en +3V3.
- La señal viaja en corriente: R_SENSE va junto al BTT y R_IS + C_IS junto al módulo, de modo que la caída en la masa entre ambos no entra en la lectura (§11).

Es la topología de la Fig. 52 (p. 47): R_SENSE en serie con el pin IS y R_IS en el lado del ADC. Descartado el valor R_IS = 1,2 kΩ de la Tabla 11 (p. 48): con R_SENSE = 10 kΩ, el divisor (1,212/11,11 = 0,109 con tolerancias) daría en fallo a 30 V 3,16 V con V_IS = V_S − 1 V y 3,27 V con V_IS = V_S, por encima de 3,1 V (REL-10). Con 820 Ω, 2,32 V (§3.2).

### 3.2 Cálculos de IS

**Fallo** (I_IS(FAULT) ≥ 6 mA × 10,82 kΩ = 65 V > V_S: siempre satura). Divisor con tolerancia del 1 %: 0,0744–0,0772 (nominal 0,0758). V_ADC = V_IS × divisor, con V_IS entre V_S − 3,5 V (mínimo) y V_S (techo físico, §3.1). La columna «V_S − 1 V» es la del primer cálculo, que solo vale a I_IS = 6 mA; la comprobación se hace con la de V_IS = V_S. Corriente y potencia, también con V_IS = V_S.

| V_S | Caso | V_ADC en fallo (V_S − 3,5 V … V_S − 1 V) | **V_ADC máx. (V_IS = V_S)** | Corriente | P en R_SENSE | Comprobación |
|---|---|---|---|---|---|---|
| 17,5 V | ALI-01 mín. menos las caídas | 1,04–1,27 V | 1,35 V | 1,6 mA | 26 mW | Mínimo 1,04 V, por encima del umbral de fallo de 0,9 V (§12) |
| 24 V | Nominal | 1,53–1,78 V | 1,85 V | 2,2 mA | 49 mW | — |
| **30 V** | **ALI-01 máx. (peor caso de la spec)** | 1,97–2,24 V | **2,32 V** | 2,8 mA | 77 mW | **≤ 3,1 V ✔** (margen 0,78 V) |
| 33,6 V | OVP de la fuente con JP1 cerrado | ≤ 2,52 V | 2,59 V | 3,1 mA | 96 mW | ✔ |
| 35 V | *Clamp* de U1 (≤ 162 ms) | ≤ 2,62 V | 2,70 V | 3,2 mA | 105 mW | ✔ |
| 36,7 V | V_BR mín. de la TVS (techo en régimen con JP1 cerrado) | ≤ 2,76 V | 2,83 V | 3,4 mA | 115 mW | ✔ |
| 53,3 V | Impulso con JP1 cerrado (µs–ms) | ≤ 4,04 V | 4,11 V | 4,9 mA | 243 mW (impulso) | ✘ durante el impulso: inyección ≤ (4,11 − 3,51)/758 Ω = 0,8 mA, filtrada por C_IS (τ = 76 µs). Fuera de ALI-01; residual (§13) |

- **Corriente en el pin del ESP32-S3:** en régimen, V_ADC ≤ 2,83 V < VDD mín. 3,211 V: el diodo de protección del pin no conduce y la corriente es la de fuga (≤ 50 nA, S tabla 5-4). Margen frente a VDD + 0,3 V (3,51 V): ≥ 0,68 V ✔.
- **R_SENSE:** 77 mW a 30 V y 115 mW a 36,7 V en fallo continuo → **1206 de 0,25 W** (31–46 %). Tensión de trabajo 200 V ≥ 53 V ✔. R_IS: ≤ 10 mW (0603).
- **BTT:** el fallo cuesta (V_S − V_IS)·I_IS ≤ 3,5 V × 4,9 mA = 17 mW.

**Funcionamiento normal** (V_ADC = I_IS × 820 Ω; rango con k_ILIS y R al 1 %):

| I_L | I_IS (k nominal) | V_ADC nominal | Rango | Uso |
|---|---|---|---|---|
| 0,05 A | 31 µA | 26 mV | 17–52 mV | Referencia (k ± 50 %) |
| **0,080 A** | 51 µA (k 1580) | 41,5 mV | **28,4–76 mV** (≥ 18,4 mV con el ADC) | **Carga mínima de uso** (§0; k ± 45 % interpolado) |
| 0,25 A | 0,167 mA | 137 mV | 104–197 mV | — |
| 0,5 A | 0,333 mA | 273 mV | 217–368 mV | — |
| 1 A | 0,667 mA | 547 mV | 483–627 mV | REL-05 (límite de uso) |
| 1,2 A | 0,800 mA | 656 mV | ≤ 744 mV | — |
| 1,5 A | 1,000 mA | 820 mV | ≤ 920 mV | — |

**Corriente mínima de uso para la carga abierta en ON (REL-10, REL-11; SPEC-0034).** La carga es un parámetro (DEC-0014): se busca la corriente más baja cuya lectura, en el peor caso, aún supera el umbral de 18 mV.

- Condición: I_L / k_max(I_L) × R_IS mín. (812 Ω) − 10 mV (ADC) ≥ 18 mV ⇔ I_L ≥ 34,5 µA × k_max(I_L).
- k_ILIS por interpolación logarítmica entre 50 mA (1600 ± 50 %) y 0,5 A (1500 ± 25 %) (Tabla 9, p. 30). Iterando: **I_L ≥ 79,0 mA** (k = 1580 ± 45 %, k_max = 2292). **Límite de uso: 80 mA**, que da ≥ 18,4 mV en el peor caso.
- Vale para la corriente en la peor condición: entrada a 18 V (bus a **17,5 V**; la caída en el BTT, 8 mV, no cuenta) y bobina caliente. En resistencia: **R_carga (caliente) + R_cable ≤ 17,5 V / 80 mA = 218 Ω**. Con la fuente en su ajuste de fábrica (bus ≈ 23,5 V) serían 294 Ω.
- Para una bobina de cobre que llegue a 100 °C en marcha (supuesto: 40 °C en la arqueta + 60 K de calentamiento propio; α = 0,00393 /K): R_20 ≤ 218 / (1 + 0,00393 × 80) = **166 Ω**, es decir, ≥ 0,145 A a 24 V y 20 °C. Con otra temperatura, se recalcula con la misma fórmula; el usuario lo comprueba midiendo la bobina caliente (§13.7).

Carga abierta real en ON: I_L < I_L(OL) = 4–25 mA ⇒ I_IS < I_IS(OL) (Tabla 8, p. 24; §7.3.3.1 y Fig. 24, p. 27). P_7.5.2 (p. 30) da como condición «I_IS(OL) = 8 mA»; se lee **8 µA**: 8 mA superaría I_IS(FAULT) mín. (6 mA), y 4–25 mA / k_ILIS (1600) = 2,5–16 µA encierra 8 µA. Lectura máxima: 8 µA × 828 Ω (R_IS + 1 %) + 10 mV = **16,6 mV**; con el cable cortado (I_L ≈ 0), I_IS ≤ 2 µA (Fig. 44, p. 43): ≤ 11,7 mV.

**Umbral de carga abierta en ON: 18 mV** (§12): carga abierta ≤ 16,6 mV (margen 1,4 mV) y carga de uso (≥ 80 mA) ≥ 18,4 mV (el margen frente a la carga mínima lo fija el límite de uso). Con la calibración por canal (§12) el error de k desaparece: la carga mínima baja y el margen sube.

- **Linealidad:** V_IS = I_IS × 10,93 kΩ (máx.) ≤ V_S − 3,5 V. Con el bus a 17,5 V, I_IS ≤ 1,28 mA → **I_L ≥ 1,73 A** lineal garantizado (k − 9,5 %). Por encima, IS satura y la lectura se confunde con un fallo (§3.4).
- **Atenuación: 6 dB (ATTEN2, 0–1600 mV, ± 10 mV).** 12 dB daría ± 50 mV: 0,1 A de error a 0,25 A. A 6 dB, el fallo con el bus por encima de ≈ 21 V satura el ADC (lectura 4095): es la indicación de fallo.
- Error total a 0,25 A: k ± 30 % más ± 10 mV/137 mV = ± 7 %. La medida sirve para «hay o no hay carga», «carga baja» (orientativa sin calibración, §12) y sobrecarga.
- C_IS = 100 nF (condición de la tabla 5-6 de S): τ = 820 Ω × 100 nF = 82 µs; lectura válida a ≥ 1 ms de subir DEN (t_sIS(ON_DEN) ≤ 10 µs, P_7.5.19, p. 31).

### 3.3 Carga abierta en OFF: R_OL (§7.3.3.2, pp. 27-28)

Umbral: el BTT da I_IS(FAULT) en OFF (DEN alto, IN bajo) cuando V_S − V_OUT < V_S − V_OL(OFF), con **V_S − V_OL(OFF) = 4–6 V** (P_7.5.1, p. 30; Tabla 8, p. 24). Con D = V_S − V_OUT: se detecta seguro si D < 4 V y no se detecta nunca si D > 6 V.

**R_OL = 47 kΩ 1 %, 0805** (C17713), de BUS_24V a OUT_n, en cada canal.

| Comprobación | Cálculo | Resultado |
|---|---|---|
| **Fuga por la carga ≤ 1 mA** | V_S/(R_OL mín. + R_L), con R_L = 30 Ω (resistencia mínima de uso, §0) | 0,52 mA a 24 V; **0,64 mA a 30 V**; 0,72 mA a 33,6 V; 0,79 mA a 36,7 V ✔ |
| **Sin activar la carga** | V_L = V_S·R_L/(R_OL + R_L), con R_L ≤ 218 Ω (máximo de uso, §0) | **≤ 0,14 V** a 30 V (0,5 % del bus) ✔ (criterio de 1 mA de REL-10). Una carga de alta impedancia ve más: queda fuera de los límites de uso |
| Carga presente → sin aviso | D > 6 V ⇔ R_L < R_OL·(V_S − 6)/6 | R_L < 89 kΩ a 17,5 V (R_OL − 1 %): × 400 por encima del máximo de uso (218 Ω) ✔. La resistencia del cable y la tolerancia de la carga no influyen |
| Carga ausente o cable cortado → aviso | D = I_fuga × R_OL < 4 V ⇔ I_fuga < 4 V/47,47 kΩ = 84,3 µA | Sin diodo, detecta con fugas externas (humedad del cable) equivalentes a R_fuga ≥ 160 kΩ (17,5 V), 237 kΩ (24 V) y 309 kΩ (30 V). **Con D12–D17** (fuga ≤ 50 µA, §5.4): ≥ 394 / 584 / 759 kΩ; con la fuga típica (≤ 1,5 µA a 100 °C), 163 / 242 / 314 kΩ. La fuga del BTT (I_L(OFF) ≤ 0,5 µA a ≤ 85 °C, Tabla 6, p. 15) sale por OUT y ayuda |
| Disipación | V_S²/R_OL | 12 mW a 24 V; 29 mW a 36,7 V. En la desmagnetización, con la rueda libre, ve V_S + V_F ≤ 38 V (75 V, V_DS(AZ) máx., solo si faltara el diodo). 0805: 125 mW, 150 V ✔ |
| Consumo de los 6 R_OL | Solo con el bus habilitado y el canal apagado (encendido, R_OL queda en corto) | ≤ 6 × 0,64 = 3,8 mA (115 mW a 30 V) |
| Asentamiento | τ = R_OL × (C_OUT + cable ≈ 5 nF) = 47 kΩ × 105 nF (C_OUT de 100 nF, SPEC-0038) | 4,9 ms → leer a ≥ 60 ms (12 τ; con 220 nF eran 10,6 ms) |

- Alternativa: 56 kΩ (0,54 mA a 30 V; detecta con R_fuga ≥ 196 kΩ a 17,5 V). Se elige 47 kΩ por la tolerancia a fugas.
- Infineon usa R_OL = 1,5 kΩ con un transistor que la conmuta (Tabla 11, p. 47; Fig. 25, p. 28). Aquí ese papel lo hace el limitador común: con LIM_EN bajo, R_OL no consume ni deja tensión en las cargas.
- **Sin R_PD en OUT** (47 kΩ en la Tabla 11): con R_OL de 47 kΩ dejaría D = 12 V con el canal abierto y enmascararía la carga abierta. El corto a VS se detecta en ON.
- **Con JP1 cerrado (DEC-0006):** el bus está siempre alimentado. R_OL consume 3,1 mA continuos (74 mW a 24 V) y cada carga ve ≤ 0,52 mA de forma permanente (≤ 1 mA ✔; ≤ 0,11 V con 218 Ω a 24 V). La comprobación funciona en cualquier momento.
- Casos que no distingue en OFF: corto a GND (parece una carga; se ve en ON) y, con dos cargas en una salida (fuera de los límites de uso), la desconexión de una. El corto a VS da lo mismo que una carga abierta.

### 3.4 Interpretación de IS (resumen; umbrales en §12)

| Estado | IN | DEN | IS (Tabla 8, p. 24) | V_ADC |
|---|---|---|---|---|
| Carga presente, OFF | L | H | Z | ≈ 0 (R_IS) |
| Carga abierta / corto a VS, OFF | L | H | I_IS(FAULT) | ≥ 1,04 V (saturado a ≥ 21 V de bus) |
| Normal, ON | H | H | I_L/k_ILIS | 0,02–0,75 V (≥ 18,4 mV con la carga mínima de uso, §3.2) |
| Carga abierta en ON (I_L < I_L(OL) 4–25 mA, P_7.5.2) | H | H | < I_IS(OL) (8 µA, §3.2) | ≤ 16,6 mV (ADC incluido) |
| Limitación, sobretemperatura, enclavamiento | H | H | I_IS(FAULT) | ≥ 1,04 V |
| DEN bajo | — | L | Z | ≈ 0 |

## 4. Corto, sobrecarga y protección (REL-05, REL-08)

### 4.1 Escenarios con el limitador común

| Escenario | Qué pasa | Qué ve el firmware | Respuesta (REL-08) |
|---|---|---|---|
| Corto franco en OUT_n con el canal encendido | Los condensadores locales (C_VS + C45/C46) dan el pico; el BTT limita a 38–56 A. U1 corta por *fast-trip* (8,4 A nom., ≤ 4,5 µs, `alimentacion.md` §3.13.2) y se enclava. El bus cae y todos los BTT se apagan por subtensión (V_S(UV) 3–4,1 V, Tabla 4, p. 8); la corriente que queda en el cable recircula por D12–D17 (§5.3). La lógica no se reinicia (`alimentacion.md` §3.13.4) | LIM_FLT bajo; IS no válida | Todos los IN a bajo → rearme (LIM_EN bajo-alto) → espera de 20 ms → encender uno a uno **los canales que estaban activos**, 50 ms cada uno, vigilando LIM_FLT. El que vuelve a disparar queda apagado y se avisa. Total < 1 s ≤ 5 s ✔ |
| Corto blando (4,57–8,4 A) | U1 regula a I_OL durante ≤ 162 ms y se enclava. El BTT del canal: 4,2 A × 0,1 Ω ≈ 1,8 W × Z_th(0,16 s) ≈ 10 K/W (Fig. 6, p. 10) = +18 °C: no llega al apagado térmico | LIM_FLT bajo; IS saturada o alta | Igual que el anterior |
| Sobrecarga de 1 A a ≈ 1,7 A | Sin corte por hardware (DEC-0004) | IS lineal > 450 mV | Aviso en Home Assistant (REL-10), sin cortar |
| Sobrecarga de ≈ 1,7 A a 3,86 A (p. ej. 3,4 A de §6) | Sin corte; IS saturada | V_ADC ≥ 0,9 V con IN alto; LIM_IMON coherente con la carga | Aviso de sobrecarga, sin cortar |
| Enclavamiento térmico (§6) | El canal se apaga y queda enclavado hasta que IN conmuta (§6.5.2, p. 21) | V_ADC ≥ 0,9 V con IN alto; LIM_IMON baja en la corriente del canal | Aviso «canal enclavado»; IN a bajo y sin reintento en el mismo riego |

- Distinguir sobrecarga fuerte de enclavamiento: con IS saturada, si LIM_IMON (± 7 %, `alimentacion.md` §3.13.7) menos la suma de los demás canales es < 0,3 A, el canal está enclavado.
- El aviso de 1 A usa la IS (§12) y no necesita LIM_IMON.

### 4.2 Pista, borne y retorno para 4,9 A (REL-05, FAB-03)

IPC-2221, capa externa, 1 oz (35 µm): I = 0,048·ΔT^0,44·A^0,725 (A en mil²).

| Corriente | Pista de 1,2 mm (65 mil²) | Requisito |
|---|---|---|
| 4,9 A (máx. de la banda del limitador) | ΔT = 38 °C | ≤ 40 °C ✔ (REL-05) |
| 3,4 A (prueba de §6, 1 h) | ΔT = 16,5 °C | ≤ 20 °C ✔ (§6) |
| 1 A (carga máxima) | ΔT ≈ 1 °C | ≤ 10 °C ✔ (REL-05; IPC-2152 da menos en placa con plano) |

- Ancho mínimo para 4,9 A con ΔT ≤ 40 °C: 1,16 mm → **1,2 mm**.
- Borne WJ500V: 15 A (UL) / 18 A (IEC), contacto ≤ 20 mΩ (WJ): a 4,9 A, 0,48 W por contacto, dentro de su corriente nominal ✔. Cable AWG 30–14.
- El BTT a 4,9 A llega al apagado térmico (§6): lo que protege a la pista y al borne hasta que actúa el limitador es su propio dimensionamiento (escalonado coherente con DEC-0004).

### 4.3 Cable largo (≥ 10 m) y ESD

- El BTT especifica la robustez al corto con un cable de 0 o 5 m (V_BAT(SC) 36 V, R 16 mΩ/m, L 1 µH/m; P_4.1.3, p. 6). Con ≥ 10 m se sale de esa condición, pero la corriente de la fuente la corta U1 (≤ 8,4 A): el BTT no llega a su limitación desde la fuente, solo desde los condensadores locales.
- Energía del cable al disparar U1: ½·L·I² = ½ × 50 µH (50 m) × 8,4² = 1,8 mJ. Si el BTT sigue encendido, recircula por D3 (SS310 en la salida de U1, `alimentacion.md` §3.13.6); si se apaga, por D12–D17 (§5.3).
- **C_OUT = 100 nF 100 V X7R 0805** (Samsung CL21B104KCFNNNE, C28233, Basic; DEC-0018 P3, SPEC-0038) en cada OUT, junto al borne: protección frente a ESD y BCI (Tabla 11, p. 48, propone 10 nF). Hasta SPEC-0037 era 220 nF (C513710). Con 100 nF, el valor se acerca al de Infineon. OUT va de −V_F (≈ −1 V, con la rueda libre) a +36,7 V; −57 V (V_S − V_DS(AZ) máx. con V_S = 18 V) solo si faltara el diodo: 100 V ✔. Efectos del valor (mayor que los 10 nF de Infineon): pico de carga al encender 0,8 V/µs × 0,1 µF = 0,08 A (0,18 A con 220 nF); τ de la carga abierta 4,9 ms (§3.3).
- El OUT del BTT aguanta ± 4 kV HBM (Tabla 3, p. 7). No se pone TVS en OUT: la rueda libre fija el negativo en −V_F, y el positivo es el del bus, ya protegido por la TVS de entrada.

### 4.4 VS, GND del chip y sobretensión

- **C_VS = 100 nF 100 V X7R 0805** (C28233, Basic; DEC-0018 P3, SPEC-0038) entre VS y GND de cada BTT (Infineon: 100 nF, Tabla 11, p. 48). El valor nominal es el de Infineon. Efectivo: 80 / 73 nF a 24 / 30 V y 60 °C (72 / 66 nF con −10 %; SimSurfing CL21B104KCFNNN: −19,9 % / −27,1 % por tensión, +0,1 % a 60 °C; `bloque-alimentacion.md` §3). DEC-0018 aceptó «≈ 85–90 nF», y la cifra real es menor. Hasta SPEC-0037 era 220 nF C513710 (0,15–0,17 µF efectivos). 100 V ≥ 53,3 V con JP1 cerrado ✔.
- **C45, C46 = 4,7 µF 100 V X7R 1210** (C381466), uno por borde, a la entrada de BUS_24V de cada grupo de 3 canales: desacoplo al final de 50–70 mm de pista `Power_In`. Efectivo ≈ 3,9 µF a 24 V. Suma en el bus: C6 4,7 + 2 × 4,7 + 6 × 0,1 = **14,7 µF nominales** (15,4 µF con 220 nF), los ≈ 15 µF supuestos en el arranque suave de U1 (`alimentacion.md` §3.13.6): I_INRUSH baja de 33 a 32 mA ✔.
- **GND del BTT directo al plano, sin R_GND ni diodo** (Infineon: 27 Ω + BAS21 y zéner de 58 V en VS, Tabla 11, p. 48). Motivos:
  - la polaridad inversa la bloquea Q1 (ALI-03), así que no hay −V_S(REV);
  - V_S ≤ 53,3 V (Vc de la TVS), por debajo de V_S(AZ) = 65 V mín. (Tabla 7, p. 22): el zéner interno no conduce y no hace falta limitar su corriente;
  - I_GND = 4,8 / 9 mA (P_4.2.5, p. 8) ≤ 20 mA ✔ (P_4.1.27, p. 7);
  - una R_GND desplaza la masa lógica del BTT (9 mA × 27 Ω = 0,24 V) y resta margen a V_IN(H).
- V_S > 48 V (máximo absoluto, P_4.1.1) solo con JP1 cerrado y durante el impulso de la TVS: cubierto por V_S(LD) = 65 V (ALI-04).

## 5. Carga inductiva: rueda libre D12–D17 (REL-03)

**D12–D17 = MDD M7 (C95872, Basic), montados en las seis salidas** (DEC-0014, que sustituye el punto 2 de DEC-0008): ánodo a GND, cátodo a OUT_n, junto al borne. Datos del M7 (M7, p. 1 y p. 2; ficha `M7.md`): V_RRM 1000 V; I_F(AV) 1 A, sin *derating* hasta T_case = 125 °C (Fig. 1); I_FSM 30 A (semionda de 8,3 ms); V_F ≤ 1,1 V a 1 A (≈ 0,8–0,95 V típ. a 0,5 A entre 100 y 25 °C, Fig. 3); I_R ≤ 5 µA a 25 °C y ≤ 50 µA a 125 °C, ambas a 1000 V; típica ≈ 0,2 µA a 75 °C y ≈ 1–1,5 µA a 100 °C, a ≤ 40 V (Fig. 2); Z_th ≈ 11–12 K/W a 50 ms (Fig. 6); R_θJA 75 K/W, con pads de cobre de 2 × 2″ (nota 2 de la p. 1), no con los del SMA.

La carga es un parámetro (DEC-0014): el cálculo usa I_L ≤ 1 A (REL-05) y τ = L/R (bobina + cable) sin valor fijo. Se sustituye el cálculo de E_AS con el *clamp* integrado y la inductancia estimada de una válvula concreta (SPEC-0023/0025), que limitaba L por válvula.

### 5.1 Energía en el BTT

Al apagar, la bobina mantiene la corriente y OUT baja hasta que conduce el diodo: V_OUT = −V_F. Entonces V_DS = V_S + V_F ≤ 31,1 V (37,8 V con JP1 cerrado), por debajo de V_DS(AZ) mín. = 66 V (Tabla 6, p. 15): **el *clamp* del BTT no conduce** y la energía de la bobina (½·L·I²) se disipa en su propia resistencia, en el cable y en el diodo.

En el BTT queda la conmutación: la corriente sigue entera mientras OUT baja a −dV/dt_OFF ≥ 0,3 V/µs (Tabla 6, p. 15), t_f ≤ 30 V / 0,3 V/µs = 100 µs, y E ≤ ½·V_S·I_L·t_f = ½ × 30 V × 1 A × 100 µs = **1,5 mJ**, el 1 % de los ≈ 155 mJ de la fig. 12 (p. 13). **Sin límite de inductancia de la carga** (REL-03).

### 5.2 Diodo en el apagado normal

| Comprobación | Cálculo | Resultado |
|---|---|---|
| Tensión inversa | Con la salida encendida, V_R = V_OUT ≤ V_S | 30 V (ALI-01), 36,7 V (V_BR mín. de la TVS, JP1 cerrado) y 53,3 V (Vc, impulso) frente a 1000 V: × 33 / × 27 / × 19 ✔ |
| Corriente de pico | i(0) = I_L | ≤ 1 A (REL-05; R_carga ≥ 30 Ω a 30 V, §0) |
| Corriente media | La corriente baja desde I_L: su media es ≤ I_L aunque se repitiera sin pausa | ≤ 1 A = I_F(AV) ✔ (Fig. 1: sin *derating* hasta T_case 125 °C) |
| Calentamiento por apagado | E ≤ V_F·I_L·τ; ΔT_J ≤ V_F·I_L·Z_th(τ) | τ = 50 ms: 55 mJ, ΔT_J ≤ 1,1 W × 12 K/W ≈ 13 K → T_J ≈ 73 °C ✔. La conducción continua (τ → ∞) solo se daría con PWM, que está fuera de los límites de uso; no se calcula (R_θJA de 75 K/W exige pads de 2 × 2″) |
| Conmutación | Rectificador estándar (t_rr sin especificar) | Solo encendido y apagado, **sin PWM** (límite de uso de §0) |

### 5.3 Diodo en un corto del cable (I_FSM)

Mientras el BTT conduce, también limitando, OUT ≥ 0 y el diodo está en inverso: la duración del corto no le afecta. Lo que recibe es la corriente del cable en el instante en que el BTT corta (apagado térmico, subtensión del bus tras el disparo de U1 o IN bajo), que se descarga por el lazo cable–corto–diodo con τ_c = L_c/R_c.

- **Pico:** ≤ I_L5(SC) máx. = **56 A** (38–56 A a V_DS = 5 V; 22 A típ. a 28 V, I_L28(SC); Tabla 7, p. 22). Con U1 (JP1 abierto) la energía que puede llegar al cable está acotada además por la de los condensadores del bus (14,7 µF a 30 V: 6,6 mJ, §4.4) más lo que deja pasar U1 hasta su *fast-trip* (≤ 9,1 A × 30 V × 4,5 µs = 1,2 mJ; `alimentacion.md` §3.13.2): ½·L_c·I² ≤ 7,8 mJ → con 10 m de cable (10 µH), ≤ 40 A; con 50 m, ≤ 18 A.
- **Duración:** τ_c = (1 µH/m) / (2·ρ/S) no depende de la longitud y crece con la sección. Con el cable del ensayo de cortocircuito del BTT (16 mΩ/m, 1 µH/m; P_4.1.3, p. 6), **62,5 µs**; con la sección máxima del borne (2,08 mm², 16,8 mΩ/m), 59 µs. V_F acorta la descarga.
- **I²t del impulso:** I_pk²·τ_c/2 = 56² × 62,5 µs / 2 = **0,098 A²s** (0,051 A²s con 10 m y U1). Capacidad del M7 a partir de la I_FSM: I_FSM²·t/2 = 30² × 8,33 ms / 2 = **3,75 A²s** (p. 1; Fig. 5). **Margen × 38** (× 74). El pico supera I_FSM (56 frente a 30 A), pero dura 1/130 de la semionda; con I²t constante, la capacidad a 62,5 µs sería ≈ 350 A (extrapolación: el fabricante no da I²t) ✔.
- **Con JP1 cerrado** (sin U1, DEC-0006), el BTT limita hasta su apagado térmico y **queda enclavado**: no reintenta solo, solo lo rearma una nueva subida de IN (§6.5.2, p. 21; §7.3.5, p. 29; Fig. 19 de la Tabla 7, p. 22; igual que §4.1 y §6). Cada subida de IN con el corto presente da, por tanto, un impulso como el anterior (≤ 56 A, ≤ 62,5 µs, ≤ 0,098 A²s, ≤ 3,5 mC). La subtensión sí se rearma sola (§6.2, p. 17): si la fuente hunde el bus por debajo de V_S(UV) = 3–4,1 V (Tabla 4, p. 8), cada recuperación por encima de V_S(OP) vuelve a encender el canal y añade un impulso. El firmware deja IN bajo al leer la IS saturada (≤ 1 s, §12) y no lo reintenta en el mismo riego (REL-08), así que el número de impulsos es pequeño; el que dé la fuente al hundirse no está calculado: punto de prueba (§13.9).
- Corto franco en el borne: el diodo queda en paralelo con el corto y solo ve la inductancia de la pista entre ambos (nH).

### 5.4 Fuga en caliente frente al presupuesto de R_OL

La carga abierta en reposo se detecta mientras la fuga total de OUT_n a GND es < 4 V / R_OL máx. (47,47 kΩ) = **84,3 µA** (§3.3).

- Cota del M7: **50 µA** (125 °C y 1000 V, p. 1). Aquí ve ≤ 36,7 V y en reposo no disipa: su temperatura es la de la placa junto al BTT (60–80 °C). La típica a esa tensión es ≈ 0,2 µA a 75 °C y ≈ 1–1,5 µA a 100 °C (Fig. 2). La cota es conservadora.
- Con la cota cabe (50 < 84,3 µA ✔) y deja 34,3 µA para la fuga del cable: aislamiento ≥ 394 kΩ a 17,5 V (584 kΩ a 24 V). Con la típica (≤ 1,5 µA a 100 °C), ≥ 163 kΩ (sin diodo eran 160 kΩ). El límite de uso de §0 toma 400 kΩ.
- Con la salida encendida, la fuga (≤ 50 µA) es el 0,06 % de la carga mínima de uso (80 mA) y queda por debajo de I_L(OL) (4–25 mA): con la carga desconectada, la salida sigue leyéndose como abierta.

### 5.5 Tiempo de desmagnetización (cierre)

Con la rueda libre, L·di/dt = −(R·i + V_F): t(x) = τ·ln[(1 + a)/(x + a)], con τ = L/R (bobina + cable), x la fracción de la corriente inicial y a = V_F/(I_L·R) = V_F/V_S.

| V_S (V_F ≈ 0,8 V) | Hasta el 5 % | Hasta cero | Con el *clamp* del BTT (sin diodo), hasta cero: τ·ln(1 + V_S/(V_DS(AZ) − V_S)) |
|---|---|---|---|
| 24 V | 2,5·τ | 3,4·τ | 0,45·τ |
| 30 V | 2,6·τ | 3,7·τ | 0,61·τ |

- Ejemplos: τ = 10 / 20 / 50 ms → 25 / 50 / 126 ms hasta el 5 % a 24 V. La válvula suelta antes, cuando la corriente baja de la de retención, y el cierre hidráulico tarda segundos: el retraso no importa en riego (DEC-0014). La placa no limita τ.
- El firmware espera la desmagnetización antes de la comprobación en reposo de un canal recién apagado (§12); mientras dura, el canal se lee como «carga presente».

## 6. Térmica del BTT

Modelo: R_DS(on) máx. = 100 mΩ a 150 °C (P_5.5.1, p. 15) escalado con la curva típica (50 → 95 mΩ entre 25 y 150 °C, Fig. 8, p. 11): 53 mΩ a 25 °C, 72 mΩ a 77 °C. P = I²·R_DS(on)(T_J) + V_S·I_GND, con I_GND = 9 mA máx. (P_4.2.5, p. 8; típ. 4,7 mA, Fig. 31, p. 36). R_thJA = **50 K/W** con ≥ 300 mm² de cobre en VS (1s0p: 47 K/W, Fig. 7, p. 10; la placa de 2 capas con vías mejora). Solo con la huella: 92 K/W.

| Caso | T_A | P | T_J | Límite (T_J(SC) ≥ 150 °C, Tabla 7, p. 22) |
|---|---|---|---|---|
| 1 A continuo, 30 V | 60 °C | 0,34 W | **77 °C** (92 °C solo con la huella) | ✔ margen 73 K |
| Ensayo térmico de §6: 1 + 1 + 4 × 0,375 A | 60 °C | 0,34 / 0,28 W | 77 / 74 °C | ✔ |
| 3,4 A, 1 h (§6, a 24 V) | 25 °C | 1,06 W | 78 °C | ✔ sin enclavamiento |
| 3,4 A | 60 °C | 1,25 W | 123 °C | ✔ |
| 4,57 A (máx. del limitador) | 60 °C | — | > 150 °C | Apagado térmico y enclavamiento (REL-08) |
| 4,9 A | 25 °C | — | > 150 °C | Ídem (DEC-0004) |

- Corriente continua máxima sin enclavamiento: **≈ 4,0 A a 60 °C** y ≈ 4,8 A a 25 °C (R_thJA 50 K/W).
- Por encima, el BTT se apaga y se enclava sin dañarse (§6.5.2, p. 21).
- La lógica del BTT (V_S·I_GND = 0,27 W a 30 V) pesa más que la conducción a 1 A (0,07 W).

## 7. LED por canal (REL-07)

| Opción | Corriente | Efecto en la carga abierta en OFF | Coste | Resultado |
|---|---|---|---|---|
| LED + R en OUT_n a GND (24 V) | 2 mA, ≈ 70 mW a 30 V | Con R_OL: 0,38 mA por el LED, V_OUT ≈ 6 V → D = 18 V > 6 V: **enmascara la carga abierta**, y el LED luce tenue en OFF. Además ve −57 V en el apagado (necesita diodo) | LED + R + diodo | ✘ |
| Transistor desde 3,3 V mandado por OUT (divisor) | 1,5 mA de 3,3 V | El divisor carga OUT (≥ 1 MΩ para no enmascarar) y el LED se enciende con la carga abierta en OFF | LED + transistor + 3 R | ✘ por coste y ambigüedad |
| **LED + 1 kΩ desde el GPIO IN_n (lado del GPIO de R_IN)** | **1,5 mA** de cada GPIO (6 × 1,5 = 9 mA de +3V3, dentro de los ≈ 45 mA de `alimentacion.md` §4) | **Ninguno** (lado lógico) | LED C2286 + R C21190 (Basic, líneas existentes): ≈ 0,06 $/placa | **✔ Elegida** |
| Sin LED | — | — | 0 | Posible (REL-07 es S; el estado está en Home Assistant) |

- Indica la orden del firmware, no la salida real: si el BTT se enclava, el LED sigue encendido y el aviso llega por Home Assistant.
- I = (3,3 − 1,8 V)/1 kΩ = 1,5 mA (KT-0603R, V_F 1,8–2,4 V a 20 mA; ≈ 20 mcd a 1,5 mA). Es el mismo criterio que el LED de estado (`mcu.md` §7).
- REL-04: con el GPIO en Z, el LED y su resistencia solo refuerzan el *pull-down*. Margen de V_IN: §2.2.
- Rojo (KT-0603R, Basic, línea de D4). Si se prefiere distinguirlo del LED de alimentación: KT-0603YG (C2289, Extended, línea de D5).

## 8. Bornes (REL-05, REL-06, REL-09, FAB-07, FAB-09)

- **J4–J9: WJ500V-5.08-2P** (C8465), 2 polos por canal. **Pin 1 = OUT_n, pin 2 = GND** en los seis (REL-06).
- **J4, J5, J6 = canales 1, 2, 3 en el borde superior; J7, J8, J9 = canales 4, 5, 6 en el inferior** (REL-09). 6 polos por borde = 30,5 mm (FAB-07).
- Los seis con la entrada del cable hacia fuera de la placa y con el pin 1 en el mismo lado visto desde la entrada del cable (los del borde inferior van girados 180° respecto a los del superior). Lo fija el layout y lo comprueba con la serigrafía.
- Corriente: 4,9 A frente a 15 A (UL) ✔ (§4.2).
- **Serigrafía** (FAB-09, REL-02, REL-11; se coloca en la fase 4): «OUTn» y «GND» (o «+» / «−») en cada borne y, junto a cada grupo de tres bornes (las dos copias iguales), los límites esenciales en tres líneas:

  ```
  SALIDA = ENTRADA 18-30 V DC
  SOLO DC, NUNCA 230 V AC
  MAX. 1 A/SALIDA, TOTAL 3,5 A
  ```

  - Altura de letra ≥ 1,0 mm y trazo de 0,15 mm: 28 caracteres ≈ 22–27 mm, dentro de los 30,5 mm del grupo. Solo ASCII (sin «≤», «·» ni tildes) para no depender de la fuente.
  - El resto de los límites (resistencia mínima, carga mínima del diagnóstico, una carga por salida, fuga, cable) va en el manual, con la tabla de §0.
- Ficha existente con símbolo `Connector:Screw_Terminal_01x02` y huella `esp-riego:TerminalBlock_Kangnex_WJ500V-5.08-2P_1x02_P5.08mm_Horizontal`. La ficha `WJ500V-5.08-2P.md` (corregida en SPEC-0024) da el uso: J1 en `alimentacion.kicad_sch` y J4–J9 en `salidas.kicad_sch`.

## 9. Lista de piezas

Referencias provisionales: siguen a las de `mcu.md` §11 (U6, R25, C26, D5, J3, SW2) y `alimentacion.md` §7 sin chocar. «n» = canal 1…6, en orden (R26 = canal 1 … R31 = canal 6).

| Ref. | Valor / función | Encapsulado | MPN principal | LCSC · tipo · stock JLCPCB (2026-11-12) | Alternativa (LCSC) | Símbolo / huella |
|---|---|---|---|---|---|---|
| U7–U12 | *High-side* 24 V, canales 1–6 | PG-TDSO-14 | Infineon BTT6050-1ERA | C534868 · Extended · 1 628 | BTT6030-2ERA (C534865 · 10 556; otro *routing*, §10) | `esp-riego:BTT6050-1ERA` / `esp-riego:Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm` |
| J4–J9 | Borne 2P 5,08 mm, salidas 1–6 | THT | Kangnex WJ500V-5.08-2P | C8465 · Extended (THT) · 293 197 | — | `Connector:Screw_Terminal_01x02` / `esp-riego:TerminalBlock_Kangnex_WJ500V-5.08-2P_1x02_P5.08mm_Horizontal` |
| R26–R31 | R_IN, 10 kΩ 1 % | 0603 | UNI-ROYAL 0603WAF1002T5E | C25804 · Basic · 42,9 M | Yageo RC0603FR-0710KL (C98220) | `Device:R` / `Resistor_SMD:R_0603_1608Metric` |
| R32–R37 | R_PD de IN1–6, 100 kΩ 1 % | 0603 | 0603WAF1003T5E | C25803 · Basic · 15,2 M | Yageo RC0603FR-07100KL (C14675) | `R_0603` |
| R38–R43 | R_DEN, 10 kΩ 1 % | 0603 | 0603WAF1002T5E | C25804 | C98220 | `R_0603` |
| R44 | R_PD de OUT_DEN, 100 kΩ 1 % | 0603 | 0603WAF1003T5E | C25803 | C14675 | `R_0603` |
| R45–R50 | R_SENSE, 10 kΩ 1 % 0,25 W 200 V | **1206** | UNI-ROYAL 1206W4F1002T5E | C17902 · Basic · 1,92 M | Yageo RC1206FR-0710KL (C132649) | `Device:R` / `Resistor_SMD:R_1206_3216Metric` |
| R51–R56 | R_IS, 820 Ω 1 % | 0603 | 0603WAF8200T5E | C23253 · Basic · 816 705 | Yageo RC0603FR-07820RL (C114638) | `R_0603` |
| R57–R62 | R_OL, 47 kΩ 1 % 0,125 W 150 V | **0805** | 0805W8F4702T5E | C17713 · Basic · 1,10 M | Yageo RC0805FR-0747KL (C126351 · Extended · 245 933) | `Device:R` / `Resistor_SMD:R_0805_2012Metric` |
| R63–R68 | R_LED, 1 kΩ 1 % | 0603 | 0603WAF1001T5E | C21190 · Basic · 28,8 M | Yageo RC0603FR-071KL (C22548) | `R_0603` |
| C27–C32 | C_VS, 100 nF 100 V X7R (SPEC-0038) | 0805 | Samsung CL21B104KCFNNNE | C28233 · Basic · 2 545 844 (2026-11-23) | — | `Device:C` / `Capacitor_SMD:C_0805_2012Metric` |
| C33–C38 | C_OUT, 100 nF 100 V X7R (SPEC-0038) | 0805 | CL21B104KCFNNNE | C28233 | — | `C_0805` |
| C39–C44 | C_IS, 100 nF 50 V X7R | 0603 | Yageo CC0603KRX7R9BB104 | C14663 · Basic · 36,5 M | Samsung CL10B104KB8NNNC (C1591) | `Device:C` / `Capacitor_SMD:C_0603_1608Metric` |
| C45, C46 | BUS_24V a granel (C45 borde superior, C46 inferior), 4,7 µF 100 V X7R | 1210 | PSA FS32X475K101EGG | C381466 · Extended · 37 932 (línea de C2/C6/C7/C22) | Walsin 1210B475K101CT (C7471274) | `Device:C` / `Capacitor_SMD:C_1210_3225Metric` |
| D6–D11 | LED de canal, rojo | 0603 | Hubei KENTO KT-0603R | C2286 · Basic · 5,99 M (línea de D4) | KT-0603YG (C2289 · Extended) | `Device:LED` / `LED_SMD:LED_0603_1608Metric` |
| D12–D17 | Rueda libre, 1 kV 1 A, **montado** (DEC-0014) | SMA | MDD M7 | C95872 · Basic · 6,49 M | — | `Device:D` / `Diode_SMD:D_SMA` (en BOM y CPL desde SPEC-0034: `dnp no`, `in_bom yes`, `in_pos_files yes`) |

- **Stock de las alternativas (2026-11-12):** C98220 11,8 M; C14675 10,8 M; C132649 3,33 M; C114638 147 774; C126351 245 933; C22548 13,5 M; C307542 29 234; C1591 2,34 M; C7471274 1 959; C2289 34 078; C534865 10 556.
- **Totales:** 6 U, 6 J, 43 R, 20 C, 6 LED, 6 diodos.
- **Líneas nuevas en el BOM:** C534868 (Extended), C17902, C17713, C23253 y C95872 (Basic). El resto, líneas existentes. C23253 (820 Ω, Basic) sustituye a 910 Ω (C23264, Extended) del primer cálculo: cumple igual REL-10 (§3.2) y ahorra una línea Extended (DEC-0007).
- **Stock para 10 placas (2026-11-12):** BTT6050 60 de 1 628 ✔ (margen limitado; segunda fuente en §10). C28233 (SPEC-0038): 12 por placa, 120 de 2 545 844 el 2026-11-23 ✔; C513710 queda para C3 y C8 (alimentación). C381466: 6 por placa (con alimentación), 60 de 37 932 ✔. C8465: 7 por placa, 70 de 293 197 ✔.
- **Piezas nuevas:** ningún símbolo ni huella nuevos; la huella `esp-riego:Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm` pasa a llevar 10 vías de 0,3 / 0,6 mm en el EP (SPEC-0024, FAB-02). Fichas en Anexo A.
- **Coste orientativo** (tramo de la cantidad real; sin cargos de piezas Extended): BTT 6 × 1,0952 $ = 6,57 $ (30 y 60 uds, tramo 30–99); bornes 0,81 $ (5 placas, tramo 1–49 con J1) / 0,65 $ (10, tramo 50–149); C45/C46 0,43 / 0,34 $; C_VS y C_OUT 12 × 0,0159 $ = 0,19 $ (C28233, SPEC-0038; con C513710 eran 0,27 $); resto (resistencias, C_IS, LED) 0,24 $; D12–D17 6 × 0,0103 $ = 0,06 $ (`M7.md`, 2026-11-17). **≈ 8,4 $ por placa con 5 placas y ≈ 8,1 $ con 10** (el estudio daba 8,33 / 7,86 $).

## 10. Segunda fuente: BTT6030-2ERA (sin diseñarla)

| Aspecto | Cambio |
|---|---|
| Pinout | 1 GND, 2 IN0, 3 DEN, 4 IS, 5 DSEL, 6 IN1, 8-10 OUT1, 12-14 OUT0, *tab* VS (ficha, Tabla 2, p. 4). **Misma huella, distinto pinout: no es intercambiable sin rehacer el *routing*.** |
| Reparto en bordes (REL-09) | 3 canales por borde con chips de 2: un chip tendría un canal en cada borde (pistas de 4,9 A cruzando la placa), o hacen falta 4 chips (2 por borde, un canal libre en cada uno) |
| DSEL e IS | IS compartido por chip, elegido con DSEL. Con un **DSEL común** a los 3 chips basta 1 GPIO, y quedan 3 ADC1 libres (lee los canales pares y los impares en dos pasos). `mcu.md` §9.2 suponía 3 DSEL |
| k_ILIS | 2240 (2360 ± 25 % a 0,5 A; 2450 ± 50 % a 50 mA; BTT30 p. 31): constante del firmware. Con R_IS = 820 Ω, 366 mV a 1 A. **No subir R_IS por encima de ≈ 1 kΩ**: el divisor de fallo pasaría de 3,1 V a 30 V |
| Fallo y carga abierta | I_IS(FAULT) 6/15/40 mA y V_S − V_OL(OFF) 4–6 V iguales: R_SENSE y R_OL no cambian |
| Corriente y térmica | I_L(NOM) 6 A con un canal y 4 A con los dos (P_5.5.3, p. 16); R_DS(on) ≤ 62 mΩ; I_GND_2 ≤ 12 mA. Dos canales comparten el encapsulado: rehacer §6 |
| E_AS | 85 mJ a 4 A (P_4.1.23, BTT30 p. 7). Con la rueda libre montada no interviene (§5.1); solo cambia la energía de conmutación |
| Coste | 3 × 2,2052 $ = 6,62 $ (igual que 6 BTT6050); con 4 chips, 8,82 $ |

## 11. Restricciones de layout

| Red | Corriente | Ancho mín. | Separación | Ubicación / keepout | Notas |
|---|---|---|---|---|---|
| BUS_24V (tronco desde U1 hasta cada grupo de 3 BTT) | 4,57 A (4,9 A como dato de REL-05) | 2,0 mm o polígono (`Power_In`) | ≥ 0,6 mm (hasta 53 V con JP1 cerrado; IPC-2221 B2) | C45 (arriba) y C46 (abajo) a la entrada de cada grupo | Clase `Power_In` (FAB-03, `alimentacion.md` §8) |
| BUS_24V en cada BTT (*tab* VS, pad 15) | 4,9 A por un solo canal | Polígono que une los 3 *tabs* del grupo | ≥ 0,6 mm | **≥ 300 mm² de cobre en VS por BTT** (cara superior + inferior), de él depende R_thJA = 50 K/W (Fig. 7, p. 10). Vías térmicas en el EP de **0,3 / 0,6 mm** (FAB-02), **ya en la huella** (10 por *tab*, pad 15, con pad en B.Cu y conexión sólida), a un polígono BUS_24V en la cara inferior que pone el layout | El *tab* es VS, **no GND**: las vías no van al plano de GND. Mantener el plano GND continuo bajo las señales analógicas (FAB-04); la franja del borde es zona de potencia. Pasta del EP al 65 % (14 ventanas a 0,10 mm del taladro; vías en la huella; ver `BTT6050-1ERA.md`). |
| OUT_n (pines 10-12 del BTT → C_OUT → J pin 1) | 1 A; 4,9 A sin daño | **1,2 mm** (ΔT 38 °C a 4,9 A; 16,5 °C a 3,4 A; ≈ 1 °C a 1 A) | **≥ 1 mm** (clase `Salidas`) en pistas, polígonos y pads fuera de las huellas de la excepción; **≥ 0,6 mm dentro de las huellas U7–U12, R57–R62 y C33–C38 y en sus pads** (nota 1) | BTT a ≤ 15 mm de su borne; los tres pines OUT unidos en la placa (nota 1 de la Tabla 2, p. 4); la pista sale de la huella del BTT por el lado de los pads OUT, sin pasar entre pads | Clase `Salidas` (FAB-03). OUT va de −V_F (≈ −1 V, rueda libre) a +37 V; −57 V solo si faltara el diodo |
| Retorno GND del borne (J pin 2 → plano) | 4,9 A | 1,2 mm o conexión directa al polígono | — | Pad THT unido a GND en las dos caras; con alivio térmico, radios con suma ≥ 1,2 mm (p. ej. 4 × 0,5 mm) o conexión sólida; ≥ 3 vías de 0,3 / 0,6 mm junto al pad | FAB-03 |
| GND del BTT (pin 3), C_VS | 9 mA | 0,25 mm | 0,2 mm | C_VS (C27–C32) a ≤ 3 mm entre el polígono VS y el pin 3; vía a GND junto al pin 3 | — |
| C_OUT (C33–C38) | Transitorios | 0,6 mm a OUT, GND corto | ≥ 1 mm de OUT_n a otras redes fuera de la huella; ≥ 0,6 mm entre los pads de C33–C38 (0805: 0,90 mm, nota 1) | Junto al pin 1 del borne, con su vía de GND al lado | ESD y BCI (Tabla 11, p. 48) |
| D12–D17 (rueda libre, montados) | ≤ 1 A al apagar; impulso ≤ 56 A durante ≈ 60 µs en un corto del cable (§5.3) | Cátodo en la pista OUT_n (1,2 mm); ánodo directo al plano GND | ≥ 1 mm de OUT_n a otras redes fuera de la huella (hueco del SMA entre pads: 1,5 mm) | **Junto al borne**, entre su pin 1 (OUT_n) y el retorno GND del pin 2, para que el lazo de la rueda libre sea diodo–borne–cable–bobina y no pase por la pista del BTT; ≥ 2 vías de 0,3 / 0,6 mm a GND junto al ánodo | Cátodo (banda) = pad 1 (`M7.md`); comprobar el giro en el CPL |
| R_OL (R57–R62) | ≤ 0,8 mA | 0,25 mm | ≥ 0,6 mm entre sus pads (0805: 0,80 mm; hasta 75 V en la desmagnetización, nota 1); ≥ 1 mm de la pista OUT_n fuera de la huella | Entre el polígono VS y OUT_n, junto al BTT | — |
| IS_HS (pin 6 del BTT → R_SENSE) | ≤ 4,8 mA | 0,25 mm | ≥ 0,6 mm (hasta 36,7 V) | **R_SENSE (R45–R50) a ≤ 5 mm del pin 6**; tramo lo más corto posible | — |
| IS1–IS6 (R_SENSE → GPIO4–9) | ≤ 3,3 mA | 0,25 mm | 0,2 mm | **R_IS (R51–R56) y C_IS (C39–C44) junto al pin del módulo**, con su GND al plano junto al módulo | ≤ 2,8 V en régimen. La señal viaja en corriente: la longitud no afecta. Lejos de SW y L1 del *buck* (`mcu.md` §12) |
| IN1–IN6, OUT_DEN | µA (1,5 mA con el LED) | 0,25 mm | 0,2 mm | **R_PD (R32–R37, R44) junto al GPIO**; **R_IN y R_DEN (R26–R31, R38–R43) junto al BTT** (§6.4, p. 19) | `mcu.md` §12 |
| LED (D6–D11, R63–R68) | 1,5 mA | 0,25 mm | 0,2 mm | Junto a su borne, visibles desde la cara superior, en la red IN_n (lado del GPIO de R_IN) | Serigrafía con el número de canal |
| Bornes J4–J9 | 4,9 A | — | — | J4–J6 (canales 1–3) en el borde superior y J7–J9 (4–6) en el inferior, de izquierda a derecha; entrada del cable hacia fuera; pin 1 = OUT_n | REL-06, REL-09, FAB-07, FAB-09 |
| Todo el bloque | — | — | — | Fuera de la zona de la antena y a ≥ 15 mm de ella (`mcu.md` §12) | MCU-02 |

**Nota 1. Excepción de separación de `Salidas` (VAL-0023-01-01).** FAB-03 pide ≥ 1 mm en `Salidas`, pero las huellas conectadas a OUT_n tienen huecos menores:

| Huella | Hueco de un pad OUT_n a la red vecina | Red vecina | Tensión máxima |
|---|---|---|---|
| BTT (U7–U12), `esp-riego:Infineon_PG-TDSO-14…` | 0,735 mm (pads 10-12 al EP) | BUS_24V (VS) | V_DS(AZ) ≤ 75 V en la desmagnetización (Tabla 6, p. 15) |
| BTT (U7–U12) | 0,62 mm (pads 10 y 12 a los NC 9 y 13) | Sin red (NC) | — (flotantes) |
| R_OL (R57–R62), `R_0805_2012Metric` | 0,80 mm | BUS_24V | ≤ 75 V |
| C_OUT (C33–C38), `C_0805_2012Metric` | 0,90 mm | GND | ≤ 57 V (OUT a −57 V en la desmagnetización) |

- **Regla para el layout:** separación de `Salidas` ≥ 1 mm en general y una regla propia de **0,6 mm** cuando uno de los dos objetos es un pad de U7–U12, R57–R62 o C33–C38 o está dentro de su patio. La escribe el ingeniero de layout en las reglas de diseño; el DRC no debe tener excepciones manuales.
- **Justificación eléctrica:** la tensión entre OUT_n y cualquier red vecina es ≤ 75 V (V_DS(AZ) máx.; cota sin la rueda libre, que con D12–D17 montados baja a ≤ 55 V: 53,3 V de Vc + V_F); IPC-2221 B2 (capa externa sin recubrir) pide 0,6 mm hasta 100 V. Los cuatro huecos cumplen (0,62–0,90 mm). Los 1 mm de FAB-03 se mantienen en pistas y polígonos, donde sí caben.
- **Alternativa R_OL y C_OUT en 1206 (1,8 mm entre pads): descartada.** No elimina la excepción, porque la impone el BTT (encapsulado fijado por DEC-0003). En C_OUT, además, cambiaría la línea existente C513710 (compartida con C3, C8 y C_VS) por una nueva, lo que empeora el coste (DEC-0007). R_OL queda en 0805 (C17713) por coherencia con la regla.
- La excepción la fija **DEC-0008** (punto 3), con la condición de cumplir los parámetros de fabricación de la clase de trabajo; `docs/02` v0.5 la recoge en FAB-03.

## 12. Notas para el firmware (FW-01…FW-04)

- **ADC de IS1–IS6:** GPIO4–9, `attenuation: 6dB`, media de ≥ 16 muestras. I_L = V_ADC / 820 Ω × 1500 (k_ILIS; 1600 por debajo de 0,1 A). Calibración opcional por canal: con un solo canal encendido, k = (LIM_IMON − 10 mA)/I_IS.
- **DEN (OUT_DEN, GPIO38):** subirlo solo para leer (≥ 1 ms de espera y lectura), por ejemplo cada 1 s. El hardware aguanta DEN alto de forma continua (§3.2), pero así se reduce la disipación de los canales sin carga.
- **Umbrales** (válidos con VIN_SENSE ≥ 16,5 V; por debajo, sin diagnóstico). Los de la carga y la suma salen de los límites de uso de §0:

| Condición | IN | Umbral | Equivalente | Acción |
|---|---|---|---|---|
| Carga abierta en ON | H | V_ADC < 18 mV durante ≥ 1 s (a ≥ 100 ms del encendido) | < ≈ 35 mA nominal. Carga abierta ≤ 16,6 mV; carga de uso (≥ 80 mA) ≥ 18,4 mV (§3.2) | Aviso «carga desconectada o cable cortado» |
| **Carga baja** (REL-11) | H | 18 mV ≤ V_ADC < 41,5 mV durante ≥ 1 s (corriente estimada < 80 mA) | Orientativo sin calibración: salta siempre por debajo de 30 mA y nunca por encima de 137 mA (k ± 45 %, ADC ± 10 mV). Con la calibración por canal, ≈ 80 mA | Aviso «carga por debajo del mínimo de uso (80 mA): la detección de carga abierta no está garantizada en esta salida», sin cortar |
| Sobrecarga de la salida (REL-05, REL-10) | H | V_ADC > 450 mV durante ≥ 2 s | > 0,82 A nominal: avisa siempre con ≥ 1 A (≥ 473 mV) y nunca por debajo de 0,63 A (nota) | Aviso «salida por encima de 1 A», sin cortar |
| **Suma de las salidas** (ALI-12, REL-10) | — | LIM_IMON > 3,3 A (0,92 V) durante ≥ 2 s | Medida ± 7 % y ADC ± 36 mA (`alimentacion.md` §3.13.7): avisa siempre con ≥ 3,6 A (prueba de `docs/02` §6) y nunca por debajo de 3,05 A (≈ 3,0 A con I_GND y R_OL, que adelantan la lectura) | Aviso «suma de las salidas cerca o por encima de 3,5 A», sin cortar; opcional: no encender más salidas mientras dure, y calibrar la ganancia de IMON por placa con una carga conocida, que estrecha la banda |
| IS saturada | H | V_ADC ≥ 0,9 V | Fallo, enclavamiento o > ≈ 1,7 A | Aviso; si LIM_IMON indica que el canal no conduce, «enclavado»: IN a bajo y sin reintento en el mismo riego (REL-08) |
| Carga abierta en OFF | L | V_ADC ≥ 0,9 V | — | Aviso «carga abierta» (o corto a VS) |
| Carga presente en OFF | L | V_ADC < 0,1 V | — | — |

- **Nota sobre la sobrecarga:** con una carga por salida (DEC-0014), el umbral de 450 mV solo tiene que avisar siempre con ≥ 1 A: a 1 A, la lectura mínima es 1 A / 1680 (k + 12 %) × 812 Ω − 10 mV = 473 mV. No avisa por debajo de 0,63 A: I / k_mín × 828 Ω + 10 mV < 450 mV con k − 21 % (interpolado entre 0,5 y 1 A, p. 30). Entre 0,63 y 1 A puede avisar o no; la calibración por canal estrecha la banda. Sustituye a la nota de VAL-0023-01-05 (dos válvulas por canal).
- **Nota sobre la suma:** el umbral va sobre LIM_IMON y no sobre la suma de las IS (± 12–45 % por canal). La lectura incluye I_GND de los BTT (≤ 54 mA) y las R_OL de los canales apagados (≤ 3,8 mA), que adelantan el aviso. Con JP1 cerrado no hay LIM_IMON: la suma de las IS da solo una estimación (± 25 %).
- **Secuencia de carga abierta en OFF** (al empezar cada riego y, con LIM_EN alto, en los canales apagados):
  1. todos los IN a bajo; LIM_EN alto;
  2. esperar ≥ 60 ms (arranque de U1, ≈ 15 ms, más 5τ de R_OL × C_OUT); en un canal recién apagado, además, ≥ 4·L/R de su carga (desmagnetización por la rueda libre, §5.5; ≥ 200 ms si no se conoce) y t_sIS(FAULT_OL_ON_OFF) (P_7.5.23, p. 31). Mientras la carga se desmagnetiza, el canal se lee como «carga presente», no como fallo;
  3. OUT_DEN alto, esperar ≥ 1 ms y leer IS1–6;
  4. OUT_DEN y, si no riega ningún canal, LIM_EN a bajo.
- **Corto (LIM_FLT bajo):** todos los IN a bajo → LIM_EN bajo y alto (rearme) → 20 ms → encender uno a uno, 50 ms cada uno, solo los canales que estaban activos, vigilando LIM_FLT. El que dispara queda apagado (aviso). ≤ 5 s (REL-08).
- **Opción «sin limitador» (JP1 cerrado):** sin LIM_FLT ni LIM_IMON; el corto se identifica por la IS saturada del canal tras el reinicio (`alimentacion.md` Anexo B). Ante una IS saturada con IN alto, apagar IN en la misma lectura (§5.3).
- **Sin PWM** en IN1–6: solo encendido y apagado (§5.2).
- **REL-04:** IN1–6 y OUT_DEN con `restore_mode: ALWAYS_OFF` (`mcu.md` Anexo B). Los LED siguen a IN.

## 13. Riesgos y puntos abiertos

1. **Rueda libre (REL-03):** cerrado por DEC-0014. D12–D17 montados: sin límite de inductancia ni medida de la válvula (§5). **Prototipo:** orientación de los diodos en la placa montada (cátodo = banda = pad 1, `M7.md`) y cierre de la válvula al apagar.
2. **Impulso de la TVS con JP1 cerrado:** V_ADC ≤ 4,11 V durante el impulso con V_IS = V_S (inyección ≤ 0,8 mA, filtrada). Fuera de ALI-01 y solo sin U1. Aceptado como residual.
3. **k_ILIS con V_IS alta:** aquí V_IS llega a 8–12 V en funcionamiento normal (con 1,2 kΩ serían < 1,5 V). El datasheet especifica la fuente de corriente hasta V_S − 3,5 V (P_7.5.6), pero mide k_ILIS sin fijar R_IS. **Prototipo:** comparar la lectura a 1 A con el bus a 18 V y a 30 V (diferencia ≤ 3 %).
4. **Fugas del cable mojado:** la carga abierta en OFF falla con un aislamiento por debajo de 160–400 kΩ (§3.3, §5.4); se vería como «carga presente». La carga abierta en ON lo cubre al regar.
5. **Stock del BTT6050:** 1 628 (2026-11-12); 10 placas consumen 60. Si baja, la segunda fuente obliga a rehacer *routing* y reparto (§10).
6. **V_OH del GPIO con el LED:** S garantiza 2,64 V sin carga y lo da típico con 40 mA. Con 1,5 mA el margen de V_IN es ≥ 0,3 V; se comprueba en el prototipo (V_IN ≥ 2,2 V con el LED encendido).
7. **Umbral de carga abierta en ON (18 mV):** margen de 1,4 mV frente a la carga abierta; la carga mínima de uso (80 mA) se eligió para leer ≥ 18,4 mV en el peor caso. **Prototipo:** (a) V_ADC con 218 Ω en el borne y el bus a 17,5 V (≥ 18,4 mV); (b) con el borne abierto (≤ 17 mV); (c) con la válvula del usuario, R de la bobina tras ≥ 1 h energizada en su arqueta, para comprobar que cumple los límites de §0 (no condiciona el diseño, DEC-0014). Si no hay margen: calibración por canal (§12).
8. **Excepción de separación de `Salidas` (FAB-03):** 0,6 mm dentro de U7–U12, R57–R62 y C33–C38 (§11, nota 1). Fijada por DEC-0008: la regla se escribe en las reglas de diseño del layout.
9. **Corto del cable con JP1 cerrado:** el BTT se enclava tras su apagado térmico; cada subida de IN, y cada rearranque por subtensión si la fuente hunde el bus por debajo de V_S(UV) = 3–4,1 V, da un impulso en D12–D17 (≤ 56 A, ≤ 62,5 µs, ≤ 0,098 A²s; §5.3). **Prototipo:** corto al final de 10 m de cable con JP1 cerrado y la fuente de 5 A: contar los impulsos en el diodo (sonda de corriente) desde que sube IN hasta que el firmware lo apaga, comprobar si el bus baja de V_S(UV) y medir la temperatura del diodo.
10. **Bobina AC alimentada en continua (válvula instalada, DEC-0011):** disipa V²/R_DC, varias veces lo que en alterna. Es un dato de la válvula, fuera de la placa (fila «Tipo de carga» de §0).

## 14. Trazabilidad

| Requisito | Pieza o cálculo | Sección |
|---|---|---|
| REL-01 | 6 canales U7–U12 BTT6050-1ERA + J4–J9 | §2, §9 |
| REL-02 | Salida = BUS_24V (≤ 30 V DC); serigrafía «SALIDA = ENTRADA 18-30 V DC» y «SOLO DC, NUNCA 230 V AC» | §8 |
| REL-03 | Entrada activa alta, V_IN ≥ 2,39 V ≥ 2,0 V (Tabla 10, p. 34). Rueda libre D12–D17 (M7) montada: E en el BTT ≤ 1,5 mJ, sin límite de L; V_RRM 1000 V; I_F(AV) 1 A; corto 0,098 A²s frente a 3,75 A²s (I_FSM); fuga ≤ 50 µA < 84 µA; cierre 2,5–3,7·L/R | §2.2, §5 |
| REL-04 | R_PD 100 kΩ en IN1–6 y OUT_DEN: ≤ 5 mV | §2.2 |
| REL-05 | 1 carga y ≤ 1 A por salida (≥ 30 Ω a 30 V); pista `Salidas` 1,2 mm: ΔT 38 °C a 4,9 A, ≈ 1 °C a 1 A; borne 15 A; retorno GND 1,2 mm | §0, §4.2, §11 |
| REL-06 | Pin 1 = OUT_n, pin 2 = GND en J4–J9 | §8 |
| REL-07 | D6–D11 + R63–R68 desde IN_n, 1,5 mA, sin efecto en la carga abierta | §7 |
| REL-08 | Limitación y apagado térmico del BTT (38 A, ≥ 150 °C, *latch*, p. 21-22) + U1; secuencia de identificación ≤ 5 s; T_J y enclavamiento a 4,57–4,9 A | §4.1, §6, §12 |
| REL-09 | J4–J6 arriba (canales 1–3), J7–J9 abajo (4–6) | §8, §11 |
| REL-10 | IS → R_SENSE 10 kΩ → ADC1 6 dB; V_ADC ≤ 2,32 V a 30 V (≤ 2,83 V a 36,7 V) con V_IS = V_S, sin corriente en el pin; R_OL 47 kΩ: 0,64 mA ≤ 1 mA; carga abierta en ON < 18 mV con carga de uso ≥ 80 mA; en OFF, hasta 89 kΩ; avisos de 1 A por salida y de 3,5 A en la suma | §3, §12 |
| REL-11 | Tabla de límites de uso: tensión, tipo de carga, 1 carga, 1 A, 3,5 A, ≥ 30 Ω, ≥ 80 mA (≤ 218 Ω), ≤ 89 kΩ, fuga ≤ 0,65 mA, cable | §0, §8 |
| ALI-12, ALI-13 | Suma ≤ 3,5 A como límite de uso; U1 (3,86–4,57 A) no actúa a 3,5 A; aviso por LIM_IMON a > 3,3 A | §0, §12 |
| FAB-03 | `Power_In` 2,0 mm; `Salidas` 1,2 mm, ≥ 1 mm salvo 0,6 mm dentro de U7–U12, R57–R62 y C33–C38 (DEC-0008); retornos 4,9 A | §11 |
| FAB-07 | 3 bornes de 2 polos por borde (30,5 mm) | §8 |
| FAB-09 | Serigrafía de bornes, tensión, carga máxima por salida y suma | §8 |

## Anexo A. Datos para las fichas (`hardware/componentes/`, fuera de la zona de ing-esquematicos)

| Ficha | Cambio o dato | LCSC | Datasheet | Pinout | Símbolo / huella |
|---|---|---|---|---|---|
| BTT6050-1ERA (actualizar) | «Uso»: U7–U12 en `salidas.kicad_sch`. Añadir: sin R_GND ni zéner en VS (§4.4); vías del EP a BUS_24V (no a GND); BTT6030 con la misma huella pero **distinto pinout**. Ficha revisada en SPEC-0024 (errata de P_7.5.2, vías del EP, stock del 2026-11-10). | C534868 | Rev. 1.00 (local) | Tabla 2, p. 4 | Existentes |
| WJ500V-5.08-2P (actualizar) | «Uso»: J1 (alimentación) y J4–J9 en `salidas.kicad_sch` (no en `conectores.kicad_sch`); 7 por placa. Ficha corregida en SPEC-0024. | C8465 | Local | Pin 1 = OUT_n / pin 2 = GND | Existentes |
| KT-0603R | D4, D5 y D6–D11. Ficha propia `KT-0603R.md` (SPEC-0024). Polaridad: ② del datasheet = cátodo = pad 1 (K) de `LED_0603_1608Metric` | C2286 | `datasheets/KT-0603R.pdf` (PDF de LCSC, C2286) | Cátodo = pad 1 (K), ánodo = pad 2 (A) | `Device:LED` / `LED_0603_1608Metric` |
| M7 (actualizar) | D12–D17, **montados** por DEC-0014 (§5). Ficha `M7.md` (SPEC-0024): «función» y «Uso» pasan de DNP a montado (jr-conformidad, SPEC-0034) | C95872 | `datasheets/M7.pdf` (MDD, Rev. 2025A5) | K (banda) = pad 1, A = pad 2 | `Device:D` / `Diode_SMD:D_SMA` |
| Resistencias y condensadores genéricos | C17902, C17713, C23253 (nuevas líneas Basic); el resto, existentes | — | — | — | Oficiales |

## Anexo B. Etiquetas jerárquicas de la hoja de salidas (para SPEC-0025)

| Etiqueta | Dirección (vista desde la hoja de salidas) | Hoja de origen o destino |
|---|---|---|
| BUS_24V | Entrada (alimentación) | Alimentación (salida de U1) |
| IN1…IN6 | Entrada | MCU (GPIO11, 12, 13, 15, 16, 17) |
| OUT_DEN | Entrada | MCU (GPIO38) |
| IS1…IS6 | Salida | MCU (GPIO4–9, ADC1_CH3–CH8) |
| GND | Símbolo de alimentación (global) | — |

- La hoja no usa +3V3: los LED se alimentan desde los GPIO.
- **Redes internas** (n = 1…6): `OUTn` (OUT del BTT, R_OL, C_OUT, cátodo de la rueda libre, J pin 1), `INn_HS` (R_IN → pin 4), `DENn_HS` (R_DEN → pin 5), `ISn_HS` (pin 6 → R_SENSE), `LEDn_A` (R_LED → ánodo del LED).
- **Conexiones por canal n** (U = U6+n, J = J3+n): IN_n → R(25+n) → `INn_HS` → U pin 4; IN_n → R(31+n) → GND; IN_n → R(62+n) → `LEDn_A` → D(5+n) → GND; OUT_DEN → R(37+n) → `DENn_HS` → U pin 5; U pin 6 → `ISn_HS` → R(44+n) → IS_n; IS_n → R(50+n) → GND y C(38+n) → GND; BUS_24V → U pin 15 (VS), C(26+n) → GND, R(56+n) → `OUTn`; U pines 10, 11, 12 → `OUTn` → C(32+n) → GND, D(11+n) (montado; cátodo en `OUTn`, ánodo en GND) y J pin 1; J pin 2 → GND; U pin 3 → GND. Pines NC (1, 2, 7, 8, 9, 13, 14) con marca de no conexión. OUT_DEN → R44 → GND. C45 y C46 entre BUS_24V y GND.
