# Bloque de salidas: 6 canales *high-side* BTT6050-1ERA y bornes (SPEC-0023)

**Estado:** propuesta para validación. **Autor:** ing-esquematicos · **Fecha:** 2026-11-07.
**Requisitos:** REL-01, REL-03…REL-10; además ALI-01, ALI-12, ALI-13, FAB-03, FAB-07, FAB-09 y §6 de `docs/02` v0.4; DEC-0003, DEC-0004, DEC-0006, DEC-0007.
**Precios y stock:** API de JLCPCB (`selectSmtComponentList`), consulta del 2026-11-06. El tipo Basic/Extended y los códigos LCSC definitivos los confirma jr-conformidad (SPEC-0024).

> Datasheets (páginas del PDF):
> - **BTT:** Infineon BTT6050-1ERA Rev. 1.00, 2019-03-09 (`hardware/componentes/datasheets/BTT6050-1ERA.pdf`). En pp. 23-32 el pie dice «*Target Data Sheet 30*»: se cita la página del PDF.
> - **BTT30:** BTT6030-2ERA Rev. 1.00 (`datasheets/BTT6030-2ERA.pdf`).
> - **S:** ESP32-S3 Series Datasheet v2.2 (espressif.com): tabla 5-4, p. 65; tabla 5-6, p. 66.
> - **WJ:** WJ500V-5.08-2P (ficha y `datasheets/WJ500V-5.08-2P.pdf`).
> - `alimentacion.md` (BUS_24V, U1 TPS26632, JP1) y `mcu.md` (§9.2, §10.2, Anexo C).

## 0. Resumen

```
BUS_24V ─┬─ C_VS ─ GND            (por canal; C45/C46 a granel, uno por borde)
         ├─ VS(tab) U(n) BTT6050 OUT ─┬─ OUT_n ─ C_OUT ─ GND ─ J(n) pin 1   ── válvula(s) ── J(n) pin 2 = GND
         └─ R_OL 47 kΩ ───────────────┘          (D DNP M7: GND → OUT_n)
GPIO IN_n ─┬─ R_PD 100 kΩ ─ GND ;  ├─ R_LED 1 kΩ ─ LED ─ GND ;  └─ R_IN 10 kΩ ─ IN
OUT_DEN (GPIO38) ─ R_PD 100 kΩ ─ GND ;  ─ 6 × R_DEN 10 kΩ ─ DEN de cada BTT
IS (pin) ─ R_SENSE 10 kΩ 1206 ─┬─ IS_n → ADC1 (6 dB)
                               ├─ R_IS 820 Ω ─ GND
                               └─ C_IS 100 nF ─ GND
BTT GND (pin 3) ─ GND directo (sin R_GND ni diodo, §4.4)
```

| Función | Pieza principal | Alternativa | Requisito |
|---|---|---|---|
| *High-side* (×6) | Infineon BTT6050-1ERA, C534868 (Extended, 1 658) | BTT6030-2ERA, C534865 (otro *routing*, §10) | REL-01, REL-03, REL-08 |
| Borne (×6) | Kangnex WJ500V-5.08-2P, C8465 | — (ficha existente; misma línea que J1) | REL-05, REL-06, REL-09, FAB-07 |
| Medida IS | R_SENSE 10 kΩ 1206 + R_IS 820 Ω + C_IS 100 nF; **el divisor acota V_ADC sin diodo** | — | REL-10 |
| Carga abierta en OFF | R_OL 47 kΩ 0805 de BUS_24V a OUT_n | 56 kΩ (§3.3) | REL-10 |
| Entradas | R_IN = R_DEN = 10 kΩ; R_PD 100 kΩ en cada IN y una en OUT_DEN | — | REL-03, REL-04 |
| LED de canal | KT-0603R (C2286, Basic) + 1 kΩ desde el GPIO IN_n | KT-0603YG (C2289) | REL-07 |
| Desacoplo | C_VS y C_OUT 220 nF 100 V 0805 (C513710, línea existente); 2 × 4,7 µF 100 V 1210 (C381466, línea existente) | — | — |
| Rueda libre (opcional) | M7, C95872 (Basic), **DNP** | — | REL-03 (§5) |

Resultados clave:

- **IS (REL-10):** V_ADC ≤ **2,24 V a 30 V** en fallo (≤ 2,76 V hasta 36,7 V, la V_BR mínima de la TVS), siempre por debajo de VDD mín. (3,211 V): **no entra corriente al pin** del ESP32-S3. Lectura lineal hasta ≥ 1,7 A con el bus a 17,5 V; 547 mV a 1 A.
- **Carga abierta en OFF:** fuga por la válvula **0,64 mA a 30 V** (0,78 mA a 36,7 V) ≤ 1 mA; 0,08 V sobre la bobina. Detección con la válvula presente hasta R_L < 90 kΩ y válvula ausente con fugas externas ≥ 159 kΩ (a 17,5 V).
- **E_AS (REL-03):** con 2 válvulas del tipo instalado (Bermad 24 V DC, 156 Ω), 81–150 mJ a 30 V frente a ≈ 155 mJ de la curva (fig. 12): **cumple con L ≤ 2,69 H por válvula**. Con la válvula genérica de diseño (0,25 A) solo cumple con L ≤ 1,10 H. **La inductancia hay que medirla antes de cerrar el esquema** (REL-03); D12–D17 quedan como huella DNP por si no cumple (§5).
- **Térmica:** T_J = 77 °C a 1 A y 60 °C (R_thJA 50 K/W, con 300 mm² de cobre en VS). Sin enclavamiento hasta ≈ 4,0 A a 60 °C; a 4,57–4,9 A el BTT llega al apagado térmico y se enclava (previsto en DEC-0004 y REL-08).
- **Piezas nuevas:** ningún símbolo ni huella; las del BTT6050 y el WJ500V existen (`esp-riego`). Líneas de BOM nuevas: C534868 (Extended) y tres resistencias Basic (C17902, C17713, C23253).

## 1. Datos de partida

| Dato | Valor | Origen |
|---|---|---|
| Bus de salidas | `BUS_24V` (salida de U1): 18–30 V en el borne (ALI-01) → ≈ 17,5–30 V en el bus; *clamp* de U1 a 32–35 V durante ≤ 162 ms; con JP1 cerrado, hasta la OVP de la fuente (33,6 V supuestos) y la V_BR de la TVS (36,7 V mín.); pico de 53,3 V (Vc) solo durante un impulso | `alimentacion.md` §1, §3.13.1, §3.13.9 |
| Limitador común | U1: I_OL = 3,86–4,57 A, *fast-trip* 2 × I_OL, *latch-off*; habilitación LIM_EN, fallo LIM_FLT, medida LIM_IMON | `alimentacion.md` §3.13 |
| Carga por canal | 1–2 válvulas de 24 V DC: 0,18 A (Bermad S-390-T, 156 Ω) a 0,25 A (diseño, 20 °C); 0,28 A en frío a 24,5 V; **0,56 A con 2** | `estudio-salidas.md` §1.2 b, REL-05 |
| Parámetro de la placa | 1 A continuo por canal; pista, borne y retorno para 4,9 A | REL-05, DEC-0004 |
| Cable de campo | ≥ 10 m (prueba de corto de §6) | `docs/02` §6 |
| Pines | IN1–6: GPIO11, 12, 13, 15, 16, 17; OUT_DEN: GPIO38; IS1–6: GPIO4–9 (ADC1_CH3–CH8) | `mcu.md` §9.2 |
| GPIO | V_OH ≥ 0,8·VDD = 2,64 V; fuga ≤ 50 nA; máximo VDD + 0,3 V; VDD = 3,211–3,389 V | S tabla 5-4, p. 65; `mcu.md` §1 |
| ADC1 | ATTEN2 (6 dB): 0–1600 mV, ± 10 mV; ATTEN3 (12 dB): 0–2900 mV, ± 50 mV (con 100 nF en el pin) | S tabla 5-6, p. 66 |
| Ambiente | 50 °C + 10 °C en la caja = **60 °C** | §5, checklist de esquema |

**Nota sobre «U5» y «U6» de `estudio-salidas.md`:** en la tabla de datos de entrada de ese estudio (línea 31), U5 y U6 son identificadores de observaciones de VAL-0004-01, no referencias de piezas. Este documento no los usa como designadores: U5 y U6 son el ESP32-S3 y el USBLC6 (`mcu.md` §11), y los *high-side* son U7–U12.

## 2. *High-side* y entradas (REL-03, REL-04)

### 2.1 Pieza

BTT6050-1ERA (DEC-0003): V_S(OP) 5–48 V, V_S(LD) 65 V (Tabla 3, p. 6), R_DS(on) ≤ 100 mΩ a 150 °C (P_5.5.1, p. 15), I_L(NOM) 4,5 A, I_L5(SC) 38–56 A (Tabla 7, p. 22), entradas para 3,3 V (p. 2). Pinout: 3 GND, 4 IN, 5 DEN, 6 IS, 10-12 OUT, *tab* VS; NC 1, 2, 7, 8, 9, 13, 14 (Tabla 2, p. 4). Símbolo `esp-riego:BTT6050-1ERA` y huella `esp-riego:Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm` (sin vías: las pone el layout, §11).

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

Datos del BTT (Tabla 9, p. 30): k_ILIS = 1600 ± 50 % (50 mA), 1500 ± 25 % (0,5 A), ± 12 % (1 A), ± 9 % (2 A), ± 8 % (4 A); I_IS(FAULT) = 6 / 15 / 40 mA; V_S − V_IS(RANGE) = 1–3,5 V (saturación: el pin IS es una fuente de corriente hasta V_S − 3,5 V y nunca pasa de V_S − 1 V); fuga con DEN bajo ≤ 1 µA; I_IS sin carga ≤ 2 µA (Fig. 44, p. 43). Máximo del pin IS: −0,3 V…V_S, −25…50 mA (Tabla 3, p. 6).

Elección: **IS → R_SENSE (10 kΩ, 1206) → nodo del ADC, con R_IS = 820 Ω y C_IS = 100 nF a GND en ese nodo.** Toda I_IS circula por la serie R_SENSE + R_IS, así que:

- en funcionamiento normal, V_ADC = I_IS · R_IS (transimpedancia de 820 Ω) y V_IS = I_IS · 10,82 kΩ;
- en fallo, el pin IS satura a V_S − V_IS(RANGE) y R_SENSE/R_IS es un divisor que acota V_ADC. **No hace falta diodo de *clamp*:** un Schottky a +3V3 recortaría a 3,39 + 0,45 = 3,84 V, por encima de 3,1 V, y además inyectaría corriente en +3V3.
- La señal viaja en corriente: R_SENSE va junto al BTT y R_IS + C_IS junto al módulo, de modo que la caída en la masa entre ambos no entra en la lectura (§11).

Descartado: R_IS de 1,2 kΩ en el pin IS (Tabla 11, p. 48). En fallo (I_IS(FAULT) hasta 40 mA, pin saturado a V_S − 1) disipa (29 V)²/1,2 kΩ = 0,7 W de forma continua: con el DEN común, un canal sin válvula da I_IS(FAULT) siempre que DEN está alto y el bus habilitado (Tabla 8, p. 24). La serie de 10,82 kΩ limita esa potencia a 72 mW.

### 3.2 Cálculos de IS

**Fallo** (I_IS(FAULT) ≥ 6 mA × 10,82 kΩ = 65 V > V_S: siempre satura). Divisor con tolerancia del 1 %: 0,0744–0,0772 (nominal 0,0758). V_ADC = (V_S − V_IS(RANGE)) × divisor.

| V_S | Caso | V_ADC en fallo | Corriente | P en R_SENSE | Comprobación |
|---|---|---|---|---|---|
| 17,5 V | ALI-01 mín. menos las caídas | 1,04–1,27 V | 1,6 mA | 25 mW | Por encima del umbral de fallo de 0,9 V (§12) |
| 24 V | Nominal | 1,53–1,78 V | 2,1 mA | 45 mW | — |
| **30 V** | **ALI-01 máx. (peor caso de la spec)** | 1,97–**2,24 V** | 2,7 mA | 72 mW | **≤ 3,1 V ✔** (margen 0,86 V) |
| 33,6 V | OVP de la fuente con JP1 cerrado | ≤ 2,52 V | 3,0 mA | 91 mW | ✔ |
| 35 V | *Clamp* de U1 (≤ 162 ms) | ≤ 2,62 V | 3,1 mA | 99 mW | ✔ |
| 36,7 V | V_BR mín. de la TVS (techo en régimen con JP1 cerrado) | ≤ 2,76 V | 3,3 mA | 109 mW | ✔ |
| 53,3 V | Impulso con JP1 cerrado (µs–ms) | ≤ 4,04 V | 4,8 mA | 230 mW (impulso) | ✘ durante el impulso: inyección ≤ (4,04 − 3,51)/758 Ω = 0,7 mA, filtrada por C_IS (τ = 76 µs). Fuera de ALI-01; residual (§13) |

- **Corriente en el pin del ESP32-S3:** en régimen, V_ADC ≤ 2,76 V < VDD mín. 3,211 V: el diodo de protección del pin no conduce y la corriente es la de fuga (≤ 50 nA, S tabla 5-4). Margen frente a VDD + 0,3 V (3,51 V): ≥ 0,75 V ✔.
- **R_SENSE:** 72 mW a 30 V y 109 mW a 36,7 V en fallo continuo → **1206 de 0,25 W** (29–44 %). Tensión de trabajo 200 V ≥ 53 V ✔. R_IS: ≤ 9 mW (0603).
- **BTT:** el fallo cuesta (V_S − V_IS)·I_IS ≤ 3,5 V × 4,8 mA = 17 mW.

**Funcionamiento normal** (V_ADC = I_IS × 820 Ω; rango con k_ILIS y R al 1 %):

| I_L | I_IS (k nominal) | V_ADC nominal | Rango | Uso |
|---|---|---|---|---|
| 0,05 A | 31 µA | 26 mV | 17–52 mV | Umbral de carga abierta en ON |
| 0,135 A | 87 µA | 71 mV | ≥ 51 mV | 1 válvula Bermad caliente con el bus a 18 V (k ± 39 % interpolado) |
| 0,25 A | 0,167 mA | 137 mV | 104–197 mV | 1 válvula |
| 0,56 A | 0,373 mA | 306 mV | 230–412 mV | 2 válvulas en frío |
| 1 A | 0,667 mA | 547 mV | 483–627 mV | REL-05 |
| 1,2 A | 0,800 mA | 656 mV | ≤ 744 mV | — |
| 1,5 A | 1,000 mA | 820 mV | ≤ 920 mV | — |

- **Linealidad:** V_IS = I_IS × 10,93 kΩ (máx.) ≤ V_S − 3,5 V. Con el bus a 17,5 V, I_IS ≤ 1,28 mA → **I_L ≥ 1,73 A** lineal garantizado (k − 9,5 %). Por encima, IS satura y la lectura se confunde con un fallo (§3.4).
- **Atenuación: 6 dB (ATTEN2, 0–1600 mV, ± 10 mV).** 12 dB daría ± 50 mV: 0,1 A de error a 0,25 A. A 6 dB, el fallo con el bus por encima de ≈ 21 V satura el ADC (lectura 4095): es la indicación de fallo.
- Error total a 0,25 A: k ± 30 % más ± 10 mV/137 mV = ± 7 %. La medida sirve para «hay o no hay carga», «una o dos válvulas» (solo con calibración por canal) y sobrecarga.
- C_IS = 100 nF (condición de la tabla 5-6 de S): τ = 820 Ω × 100 nF = 82 µs; lectura válida a ≥ 1 ms de subir DEN (t_sIS(ON_DEN) ≤ 10 µs, P_7.5.19, p. 31).

### 3.3 Carga abierta en OFF: R_OL (§7.3.3.2, pp. 27-28)

Umbral: el BTT da I_IS(FAULT) en OFF (DEN alto, IN bajo) cuando V_S − V_OUT < V_S − V_OL(OFF), con **V_S − V_OL(OFF) = 4–6 V** (P_7.5.1, p. 30; Tabla 8, p. 24). Con D = V_S − V_OUT: se detecta seguro si D < 4 V y no se detecta nunca si D > 6 V.

**R_OL = 47 kΩ 1 %, 0805** (C17713), de BUS_24V a OUT_n, en cada canal.

| Comprobación | Cálculo | Resultado |
|---|---|---|
| **Fuga por la válvula ≤ 1 mA** | V_S/(R_OL + R_L) | 0,51 mA a 24 V; **0,64 mA a 30 V**; 0,71 mA a 33,6 V; 0,78 mA a 36,7 V ✔ |
| **Sin activar la válvula** | 0,64 mA × 156 Ω (con 2 válvulas, la mitad) | **0,10 V** en la bobina; abre a > 15 V ✔ (`estudio-salidas.md` §1.2) |
| Válvula presente → sin aviso | D > 6 V ⇔ R_L < R_OL·(V_S − 6)/6 | R_L < 90 kΩ a 17,5 V. Las válvulas (44–160 Ω con el cable) quedan × 560 por debajo ✔. La tolerancia de la válvula (0,2–0,56 A, 1–2 por canal) y la resistencia del cable no influyen |
| Válvula ausente o cable cortado → aviso | D = I_fuga × R_OL < 4 V ⇔ I_fuga < 4 V/47,5 kΩ = 84 µA | Detecta con fugas externas (humedad del cable) equivalentes a R_fuga ≥ 159 kΩ (17,5 V), 235 kΩ (24 V) y 306 kΩ (30 V). La fuga del BTT (I_L(OFF) ≤ 0,5 µA a ≤ 85 °C, Tabla 6, p. 15) sale por OUT y ayuda |
| Disipación | V_S²/R_OL | 12 mW a 24 V; 29 mW a 36,7 V. En la desmagnetización ve V_DS(AZ) ≤ 75 V (Tabla 6, p. 15) durante ≤ 14 ms: 0,12 W de impulso. 0805: 125 mW, 150 V ✔ (0603 quedaría justo en sus 75 V) |
| Consumo de los 6 R_OL | Solo con el bus habilitado y el canal apagado (encendido, R_OL queda en corto) | ≤ 6 × 0,64 = 3,8 mA (115 mW a 30 V) |
| Asentamiento | τ = R_OL × (C_OUT + cable ≈ 5 nF) = 47 kΩ × 225 nF | 10,6 ms → leer a ≥ 60 ms |

- Alternativa: 56 kΩ (0,54 mA a 30 V; detecta con R_fuga ≥ 196 kΩ a 17,5 V). Se elige 47 kΩ por la tolerancia a fugas.
- Infineon usa R_OL = 1,5 kΩ con un transistor que la conmuta (Tabla 11, p. 47; Fig. 25, p. 28). Aquí ese papel lo hace el limitador común: con LIM_EN bajo, R_OL no consume ni deja tensión en las válvulas.
- **Sin R_PD en OUT** (47 kΩ en la Tabla 11): con R_OL de 47 kΩ dejaría D = 12 V con el canal abierto y enmascararía la carga abierta. El corto a VS se detecta en ON.
- **Con JP1 cerrado (DEC-0006):** el bus está siempre alimentado. R_OL consume 3,1 mA continuos (74 mW a 24 V) y cada válvula ve 0,51 mA de forma permanente (≤ 1 mA ✔, 0,08 V). La comprobación funciona en cualquier momento.
- Casos que no distingue en OFF: corto a GND (parece una válvula; se ve en ON) y una de dos válvulas desconectada (se ve en ON con calibración por canal). El corto a VS da lo mismo que una carga abierta.

### 3.4 Interpretación de IS (resumen; umbrales en §12)

| Estado | IN | DEN | IS (Tabla 8, p. 24) | V_ADC |
|---|---|---|---|---|
| Carga presente, OFF | L | H | Z | ≈ 0 (R_IS) |
| Carga abierta / corto a VS, OFF | L | H | I_IS(FAULT) | ≥ 1,04 V (saturado a ≥ 21 V de bus) |
| Normal, ON | H | H | I_L/k_ILIS | 0,05–0,75 V |
| Carga abierta en ON (I_L < I_L(OL) 4–25 mA, P_7.5.2) | H | H | < I_IS(OL) | < 26 mV |
| Limitación, sobretemperatura, enclavamiento | H | H | I_IS(FAULT) | ≥ 1,04 V |
| DEN bajo | — | L | Z | ≈ 0 |

## 4. Corto, sobrecarga y protección (REL-05, REL-08)

### 4.1 Escenarios con el limitador común

| Escenario | Qué pasa | Qué ve el firmware | Respuesta (REL-08) |
|---|---|---|---|
| Corto franco en OUT_n con el canal encendido | Los condensadores locales (C_VS + C45/C46) dan el pico; el BTT limita a 38–56 A. U1 corta por *fast-trip* (8,4 A nom., ≤ 4,5 µs, `alimentacion.md` §3.13.2) y se enclava. El bus cae y todos los BTT se apagan por subtensión (V_S(UV) 3–4,1 V, Tabla 4, p. 8). La lógica no se reinicia (`alimentacion.md` §3.13.4) | LIM_FLT bajo; IS no válida | Todos los IN a bajo → rearme (LIM_EN bajo-alto) → espera de 20 ms → encender uno a uno **los canales que estaban activos**, 50 ms cada uno, vigilando LIM_FLT. El que vuelve a disparar queda apagado y se avisa. Total < 1 s ≤ 5 s ✔ |
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
- Energía del cable al disparar U1: ½·L·I² = ½ × 50 µH (50 m) × 8,4² = 1,8 mJ. Si el BTT sigue encendido, recircula por D3 (SS310 en la salida de U1, `alimentacion.md` §3.13.6); si se apaga, por su *clamp* (muy por debajo de la curva de §5) o por D12–D17 si se montan.
- **C_OUT = 220 nF 100 V X7R** en cada OUT, junto al borne: protección frente a ESD y BCI (Tabla 11, p. 48, propone 10 nF). Se usa la línea C513710 (220 nF 100 V), ya presente en el BOM (DEC-0007: una línea menos; ningún dato empeora). OUT oscila entre −57 V (V_S − V_DS(AZ) máx. con V_S = 18 V) y +36,7 V: 100 V ✔. Efectos del valor mayor: pico de carga al encender 0,8 V/µs × 0,22 µF = 0,18 A; τ de la carga abierta 10,6 ms (§3.3).
- El OUT del BTT aguanta ± 4 kV HBM (Tabla 3, p. 7). No se pone TVS en OUT: tendría que dejar pasar los −57 V de la desmagnetización y se quedaría con la energía del *clamp*.

### 4.4 VS, GND del chip y sobretensión

- **C_VS = 220 nF 100 V X7R 0805** (C513710) entre VS y GND de cada BTT (Infineon: 100 nF, Tabla 11, p. 48). Efectivo 0,15–0,17 µF a 24–30 V y 60 °C (`alimentacion.md` §3.13.6) ✔. 100 V ≥ 53,3 V con JP1 cerrado ✔.
- **C45, C46 = 4,7 µF 100 V X7R 1210** (C381466), uno por borde, a la entrada de BUS_24V de cada grupo de 3 canales: desacoplo al final de 50–70 mm de pista `Power_In`. Efectivo ≈ 3,9 µF a 24 V. Suma en el bus: C6 4,7 + 2 × 4,7 + 6 × 0,22 = **15,4 µF nominales**, los ≈ 15 µF supuestos en el arranque suave de U1 (`alimentacion.md` §3.13.6) ✔.
- **GND del BTT directo al plano, sin R_GND ni diodo** (Infineon: 27 Ω + BAS21 y zéner de 58 V en VS, Tabla 11, p. 48). Motivos:
  - la polaridad inversa la bloquea Q1 (ALI-03), así que no hay −V_S(REV);
  - V_S ≤ 53,3 V (Vc de la TVS), por debajo de V_S(AZ) = 65 V mín. (Tabla 7, p. 22): el zéner interno no conduce y no hace falta limitar su corriente;
  - I_GND = 4,8 / 9 mA (P_4.2.5, p. 8) ≤ 20 mA ✔ (P_4.1.27, p. 7);
  - una R_GND desplaza la masa lógica del BTT (9 mA × 27 Ω = 0,24 V) y resta margen a V_IN(H).
- V_S > 48 V (máximo absoluto, P_4.1.1) solo con JP1 cerrado y durante el impulso de la TVS: cubierto por V_S(LD) = 65 V (ALI-04).

## 5. Carga inductiva (REL-03)

Ecuación 5.1 (p. 13): E = V_DS(AZ)·(L/R_L)·[(V_S − V_DS(AZ))/R_L · ln(1 − R_L·I_L/(V_S − V_DS(AZ))) + I_L], con:

- V_DS(AZ) = 66 V mín. (Tabla 6, p. 15; el mínimo da la mayor energía);
- I_L = V_S/R_L; 2 válvulas en paralelo (R_L/2, L/2); bobina fría (R × 0,88, `estudio-salidas.md` §1.2 b); V_S = 30 V (ALI-01).
- Capacidad: fig. 12 (p. 13), T_J,start = 150 °C, V_S = 28 V. La curva empieza en 1 A con ≈ 155 mJ y baja con la corriente; con 0,44–0,69 A se toma 155 mJ, que es conservador. Mínimo absoluto de la curva: ≈ 53 mJ (8–10 A).

**Inductancia (sin dato del fabricante).** El cociente τ = L/R depende de la geometría y del llenado de cobre, no del número de espiras. Se estima con los solenoides de 24 V AC del mismo tamaño, con el émbolo dentro (la condición del apagado):

- Rain Bird: |Z| = 24/0,21 = 114 Ω, R = 38 Ω → L = 0,34 H a 50 Hz, **τ = 9,0 ms** (`estudio-salidas.md` §1.2 a);
- Bermad S-390-T 24 VAC (mismo cuerpo que la de 24 V DC): |Z| = 24/0,125 = 192 Ω, R = 36 Ω → L = 0,60 H (50 Hz) / 0,50 H (60 Hz), **τ = 14–17 ms**.
- Con R_ac > R_dc por las pérdidas en el núcleo, estos valores son cotas superiores. **Rango de diseño: τ = 9–16,7 ms.**

| 2 válvulas por canal | R_L (fría, /2) | L por válvula (τ 9 / 16,7 ms) | I_L a 30 V | E a 24 V | **E a 30 V** | Frente a 155 mJ | L máx. por válvula |
|---|---|---|---|---|---|---|---|
| Bermad 24 V DC, 156 Ω (tipo instalado) | 68,5 Ω | 1,40 / 2,61 H | 0,44 A | 50 / 92 mJ | **81 / 150 mJ** | ✔ (× 1,9 / × 1,03) | **2,69 H** |
| Válvula de diseño, 0,25 A (96 Ω) | 43,8 Ω | 0,86 / 1,60 H | 0,69 A | 75 / 139 mJ | **122 / 226 mJ** | ✔ / ✘ | **1,10 H** |

- **Cumple con la válvula instalada en todo el rango estimado**, con poco margen en la cota alta. Con la válvula genérica de 0,25 A solo cumple si L ≤ 1,10 H. Margen no cuantificado a favor: la curva es con T_J,start = 150 °C y aquí T_J ≤ 77 °C al apagar (§6).
- A 35 V (*clamp* de U1, fuera de ALI-01) la energía sube × 1,4.
- **REL-03 pide medir L antes de cerrar el esquema** (pendiente del usuario). Método: válvula a 24 V con el émbolo dentro; al cortar, recircular por un diodo y una resistencia conocida R_x en serie, y medir el tiempo al 37 % de la corriente: L = τ·(R_bobina + R_x).
- **Contingencia: D12–D17, M7 (C95872, Basic) DNP**, de GND (ánodo) a OUT_n (cátodo). Si se monta, la desmagnetización se hace en la bobina (E en el BTT ≈ 0) y la válvula cierra en ≈ 3τ (30–50 ms, irrelevante para riego). Fuga a 30 V: ≤ 5 µA a 25 °C (1 kV, C95872), decenas de µA en caliente, < 84 µA del presupuesto de R_OL (§3.3) ✔. **Montarlas cambia el «con el *clamp* integrado» de REL-03: requiere DEC** (§13).
- Tiempo de desmagnetización con el *clamp* (L = 1,6 H, 30 V): 14 ms.

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
- Serigrafía (FAB-09, REL-02): «OUTn» y «GND» (o «+» / «−») en cada borne; junto a cada grupo, «24 V DC · máx. 30 V · 1 A/canal».
- Ficha existente con símbolo `Connector:Screw_Terminal_01x02` y huella `esp-riego:TerminalBlock_Kangnex_WJ500V-5.08-2P_1x02_P5.08mm_Horizontal`. **La ficha dice «Uso: `conectores.kicad_sch`»: los bornes de salida van en `salidas.kicad_sch`** (propuesta de cambio en el log).

## 9. Lista de piezas

Referencias provisionales: siguen a las de `mcu.md` §11 (U6, R25, C26, D5, J3, SW2) y `alimentacion.md` §7 sin chocar. «n» = canal 1…6, en orden (R26 = canal 1 … R31 = canal 6).

| Ref. | Valor / función | Encapsulado | MPN principal | LCSC · tipo · stock JLCPCB | Alternativa (LCSC) | Símbolo / huella |
|---|---|---|---|---|---|---|
| U7–U12 | *High-side* 24 V, canales 1–6 | PG-TDSO-14 | Infineon BTT6050-1ERA | C534868 · Extended · 1 658 | BTT6030-2ERA (C534865 · 10 617; otro *routing*, §10) | `esp-riego:BTT6050-1ERA` / `esp-riego:Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm` |
| J4–J9 | Borne 2P 5,08 mm, salidas 1–6 | THT | Kangnex WJ500V-5.08-2P | C8465 · Extended (THT) · 279 844 | — | `Connector:Screw_Terminal_01x02` / `esp-riego:TerminalBlock_Kangnex_WJ500V-5.08-2P_1x02_P5.08mm_Horizontal` |
| R26–R31 | R_IN, 10 kΩ 1 % | 0603 | UNI-ROYAL 0603WAF1002T5E | C25804 · Basic · 42,7 M | Yageo RC0603FR-0710KL (C98220) | `Device:R` / `Resistor_SMD:R_0603_1608Metric` |
| R32–R37 | R_PD de IN1–6, 100 kΩ 1 % | 0603 | 0603WAF1003T5E | C25803 · Basic · 16,3 M | Yageo RC0603FR-07100KL (C14675) | `R_0603` |
| R38–R43 | R_DEN, 10 kΩ 1 % | 0603 | 0603WAF1002T5E | C25804 | C98220 | `R_0603` |
| R44 | R_PD de OUT_DEN, 100 kΩ 1 % | 0603 | 0603WAF1003T5E | C25803 | C14675 | `R_0603` |
| R45–R50 | R_SENSE, 10 kΩ 1 % 0,25 W 200 V | **1206** | UNI-ROYAL 1206W4F1002T5E | C17902 · Basic · 2,09 M | Yageo RC1206FR-0710KL (C132649) | `Device:R` / `Resistor_SMD:R_1206_3216Metric` |
| R51–R56 | R_IS, 820 Ω 1 % | 0603 | 0603WAF8200T5E | C23253 · Basic · 755 673 | Yageo RC0603FR-07820RL (C114638) | `R_0603` |
| R57–R62 | R_OL, 47 kΩ 1 % 0,125 W 150 V | **0805** | 0805W8F4702T5E | C17713 · Basic · 1,21 M | Yageo RC0805FR-0747KL (jr-conformidad) | `Device:R` / `Resistor_SMD:R_0805_2012Metric` |
| R63–R68 | R_LED, 1 kΩ 1 % | 0603 | 0603WAF1001T5E | C21190 · Basic · 27,5 M | Yageo RC0603FR-071KL (C22548) | `R_0603` |
| C27–C32 | C_VS, 220 nF 100 V X7R | 0805 | Yageo CC0805KKX7R0BB224 | C513710 · Extended · 34 575 (línea de C3/C8) | Samsung CL21B224KCFSFNE (C307542) | `Device:C` / `Capacitor_SMD:C_0805_2012Metric` |
| C33–C38 | C_OUT, 220 nF 100 V X7R | 0805 | CC0805KKX7R0BB224 | C513710 | C307542 | `C_0805` |
| C39–C44 | C_IS, 100 nF 50 V X7R | 0603 | Yageo CC0603KRX7R9BB104 | C14663 · Basic · 34,7 M | Samsung CL10B104KB8NNNC (C1591) | `Device:C` / `Capacitor_SMD:C_0603_1608Metric` |
| C45, C46 | BUS_24V a granel (C45 borde superior, C46 inferior), 4,7 µF 100 V X7R | 1210 | PSA FS32X475K101EGG | C381466 · Extended · 52 897 (línea de C2/C6/C7/C22) | Walsin 1210B475K101CT (C7471274) | `Device:C` / `Capacitor_SMD:C_1210_3225Metric` |
| D6–D11 | LED de canal, rojo | 0603 | Hubei KENTO KT-0603R | C2286 · Basic · 6,66 M (línea de D4) | KT-0603YG (C2289 · Extended) | `Device:LED` / `LED_SMD:LED_0603_1608Metric` |
| D12–D17 | Rueda libre, 1 kV 1 A — **DNP** | SMA | MDD M7 | C95872 · Basic · 5,63 M | — | `Device:D` / `Diode_SMD:D_SMA` (campo DNP; fuera de BOM y CPL mientras no haya DEC) |

- **Totales:** 6 U, 6 J, 43 R, 20 C, 6 LED (+ 6 diodos DNP).
- **Líneas nuevas en el BOM:** C534868 (Extended), C17902, C17713 y C23253 (Basic). El resto, líneas existentes. C23253 (820 Ω, Basic) sustituye a 910 Ω (C23264, Extended) del primer cálculo: cumple igual REL-10 (§3.2) y ahorra una línea Extended (DEC-0007).
- **Stock para 10 placas:** BTT6050 60 de 1 658 ✔ (margen limitado; segunda fuente en §10). C513710: 14 por placa (con C3 y C8), 140 de 34 575 ✔.
- **Piezas nuevas:** ningún símbolo ni huella. Fichas en Anexo A.
- **Coste orientativo** (tramo de la cantidad real; sin cargos de piezas Extended): BTT 6 × 1,0952 $ = 6,57 $ (30 y 60 uds, tramo 30–99); bornes 0,81 $ (5 placas, tramo 1–49 con J1) / 0,65 $ (10, tramo 50–149); C45/C46 0,43 / 0,34 $; C513710 0,27 $; resto (resistencias, C_IS, LED) 0,24 $. **≈ 8,3 $ por placa con 5 placas y ≈ 8,1 $ con 10** (el estudio daba 8,33 / 7,86 $).

## 10. Segunda fuente: BTT6030-2ERA (sin diseñarla)

| Aspecto | Cambio |
|---|---|
| Pinout | 1 GND, 2 IN0, 3 DEN, 4 IS, 5 DSEL, 6 IN1, 8-10 OUT1, 12-14 OUT0, *tab* VS (ficha, Tabla 2, p. 4). **Misma huella, distinto pinout: no es intercambiable sin rehacer el *routing*.** |
| Reparto en bordes (REL-09) | 3 canales por borde con chips de 2: un chip tendría un canal en cada borde (pistas de 4,9 A cruzando la placa), o hacen falta 4 chips (2 por borde, un canal libre en cada uno) |
| DSEL e IS | IS compartido por chip, elegido con DSEL. Con un **DSEL común** a los 3 chips basta 1 GPIO, y quedan 3 ADC1 libres (lee los canales pares y los impares en dos pasos). `mcu.md` §9.2 suponía 3 DSEL |
| k_ILIS | 2240 (2360 ± 25 % a 0,5 A; 2450 ± 50 % a 50 mA; BTT30 p. 31): constante del firmware. Con R_IS = 820 Ω, 366 mV a 1 A. **No subir R_IS por encima de ≈ 1 kΩ**: el divisor de fallo pasaría de 3,1 V a 30 V |
| Fallo y carga abierta | I_IS(FAULT) 6/15/40 mA y V_S − V_OL(OFF) 4–6 V iguales: R_SENSE y R_OL no cambian |
| Corriente y térmica | I_L(NOM) 6 A con un canal y 4 A con los dos (P_5.5.3, p. 16); R_DS(on) ≤ 62 mΩ; I_GND_2 ≤ 12 mA. Dos canales comparten el encapsulado: rehacer §6 |
| E_AS | 85 mJ a 4 A (P_4.1.23, BTT30 p. 7): rehacer §5 con su fig. 12 |
| Coste | 3 × 2,2052 $ = 6,62 $ (igual que 6 BTT6050); con 4 chips, 8,82 $ |

## 11. Restricciones de layout

| Red | Corriente | Ancho mín. | Separación | Ubicación / keepout | Notas |
|---|---|---|---|---|---|
| BUS_24V (tronco desde U1 hasta cada grupo de 3 BTT) | 4,57 A (4,9 A como dato de REL-05) | 2,0 mm o polígono (`Power_In`) | ≥ 0,6 mm (hasta 53 V con JP1 cerrado; IPC-2221 B2) | C45 (arriba) y C46 (abajo) a la entrada de cada grupo | Clase `Power_In` (FAB-03, `alimentacion.md` §8) |
| BUS_24V en cada BTT (*tab* VS, pad 15) | 4,9 A por un solo canal | Polígono que une los 3 *tabs* del grupo | ≥ 0,6 mm | **≥ 300 mm² de cobre en VS por BTT** (cara superior + inferior), de él depende R_thJA = 50 K/W (Fig. 7, p. 10). Vías térmicas en el EP de **0,3 / 0,6 mm** (FAB-02) a un polígono BUS_24V en la cara inferior (≥ 8 por *tab*) | El *tab* es VS, **no GND**: las vías no van al plano de GND. Mantener el plano GND continuo bajo las señales analógicas (FAB-04); la franja del borde es zona de potencia |
| OUT_n (pines 10-12 del BTT → C_OUT → J pin 1) | 1 A; 4,9 A sin daño | **1,2 mm** (ΔT 38 °C a 4,9 A; 16,5 °C a 3,4 A; ≈ 1 °C a 1 A) | **≥ 1 mm** (clase `Salidas`) | BTT a ≤ 15 mm de su borne; los tres pines OUT unidos en la placa (nota 1 de la Tabla 2, p. 4) | Clase `Salidas` (FAB-03). OUT oscila de −57 V a +37 V |
| Retorno GND del borne (J pin 2 → plano) | 4,9 A | 1,2 mm o conexión directa al polígono | — | Pad THT unido a GND en las dos caras; con alivio térmico, radios con suma ≥ 1,2 mm (p. ej. 4 × 0,5 mm) o conexión sólida; ≥ 3 vías de 0,3 / 0,6 mm junto al pad | FAB-03 |
| GND del BTT (pin 3), C_VS | 9 mA | 0,25 mm | 0,2 mm | C_VS (C27–C32) a ≤ 3 mm entre el polígono VS y el pin 3; vía a GND junto al pin 3 | — |
| C_OUT (C33–C38), D12–D17 (DNP) | Transitorios | 0,6 mm a OUT, GND corto | ≥ 1 mm a otras redes | Junto al pin 1 del borne, con su vía de GND al lado | ESD y BCI (Tabla 11, p. 48) |
| R_OL (R57–R62) | ≤ 0,8 mA | 0,25 mm | ≥ 0,6 mm entre sus pads (hasta 75 V en la desmagnetización) | Entre el polígono VS y OUT_n, junto al BTT | — |
| IS_HS (pin 6 del BTT → R_SENSE) | ≤ 4,8 mA | 0,25 mm | ≥ 0,6 mm (hasta 36,7 V) | **R_SENSE (R45–R50) a ≤ 5 mm del pin 6**; tramo lo más corto posible | — |
| IS1–IS6 (R_SENSE → GPIO4–9) | ≤ 3,3 mA | 0,25 mm | 0,2 mm | **R_IS (R51–R56) y C_IS (C39–C44) junto al pin del módulo**, con su GND al plano junto al módulo | ≤ 2,8 V en régimen. La señal viaja en corriente: la longitud no afecta. Lejos de SW y L1 del *buck* (`mcu.md` §12) |
| IN1–IN6, OUT_DEN | µA (1,5 mA con el LED) | 0,25 mm | 0,2 mm | **R_PD (R32–R37, R44) junto al GPIO**; **R_IN y R_DEN (R26–R31, R38–R43) junto al BTT** (§6.4, p. 19) | `mcu.md` §12 |
| LED (D6–D11, R63–R68) | 1,5 mA | 0,25 mm | 0,2 mm | Junto a su borne, visibles desde la cara superior, en la red IN_n (lado del GPIO de R_IN) | Serigrafía con el número de canal |
| Bornes J4–J9 | 4,9 A | — | — | J4–J6 (canales 1–3) en el borde superior y J7–J9 (4–6) en el inferior, de izquierda a derecha; entrada del cable hacia fuera; pin 1 = OUT_n | REL-06, REL-09, FAB-07, FAB-09 |
| Todo el bloque | — | — | — | Fuera de la zona de la antena y a ≥ 15 mm de ella (`mcu.md` §12) | MCU-02 |

## 12. Notas para el firmware (FW-01…FW-04)

- **ADC de IS1–IS6:** GPIO4–9, `attenuation: 6dB`, media de ≥ 16 muestras. I_L = V_ADC / 820 Ω × 1500 (k_ILIS; 1600 por debajo de 0,1 A). Calibración opcional por canal: con un solo canal encendido, k = (LIM_IMON − 10 mA)/I_IS.
- **DEN (OUT_DEN, GPIO38):** subirlo solo para leer (≥ 1 ms de espera y lectura), por ejemplo cada 1 s. El hardware aguanta DEN alto de forma continua (§3.2), pero así se reduce la disipación de los canales sin válvula.
- **Umbrales** (válidos con VIN_SENSE ≥ 16,5 V; por debajo, sin diagnóstico):

| Condición | IN | Umbral (V_ADC) | Equivalente | Acción |
|---|---|---|---|---|
| Carga abierta en ON | H | < 25 mV durante ≥ 1 s (a ≥ 100 ms del encendido) | < 0,05 A | Aviso «válvula desconectada o cable cortado» |
| Sobrecarga (REL-10) | H | > 450 mV durante ≥ 2 s | > 0,82 A nominal: avisa siempre con ≥ 1 A reales y nunca con 0,56 A | Aviso, sin cortar |
| IS saturada | H | ≥ 0,9 V | Fallo, enclavamiento o > ≈ 1,7 A | Aviso; si LIM_IMON indica que el canal no conduce, «enclavado»: IN a bajo y sin reintento en el mismo riego (REL-08) |
| Carga abierta en OFF | L | ≥ 0,9 V | — | Aviso «carga abierta» (o corto a VS) |
| Carga presente en OFF | L | < 0,1 V | — | — |

- **Secuencia de carga abierta en OFF** (al empezar cada riego y, con LIM_EN alto, en los canales apagados):
  1. todos los IN a bajo; LIM_EN alto;
  2. esperar ≥ 60 ms (arranque de U1, ≈ 15 ms, más 5τ de R_OL × C_OUT); en un canal recién apagado, ≥ 100 ms (desmagnetización y t_sIS(FAULT_OL_ON_OFF), P_7.5.23, p. 31);
  3. OUT_DEN alto, esperar ≥ 1 ms y leer IS1–6;
  4. OUT_DEN y, si no riega ningún canal, LIM_EN a bajo.
- **Corto (LIM_FLT bajo):** todos los IN a bajo → LIM_EN bajo y alto (rearme) → 20 ms → encender uno a uno, 50 ms cada uno, solo los canales que estaban activos, vigilando LIM_FLT. El que dispara queda apagado (aviso). ≤ 5 s (REL-08).
- **Opción «sin limitador» (JP1 cerrado):** sin LIM_FLT ni LIM_IMON; el corto se identifica por la IS saturada del canal tras el reinicio (`alimentacion.md` Anexo B).
- **REL-04:** IN1–6 y OUT_DEN con `restore_mode: ALWAYS_OFF` (`mcu.md` Anexo B). Los LED siguen a IN.

## 13. Riesgos y puntos abiertos

1. **Inductancia de la válvula (REL-03):** sin dato del fabricante; estimada en 1,4–2,6 H (Bermad DC). Cumple con L ≤ 2,69 H (instalada) o ≤ 1,10 H (genérica de 0,25 A). **El usuario la mide antes de cerrar el esquema** (§5). Si no cumple: montar D12–D17 (requiere DEC) o limitar a 1 válvula por canal ese modelo.
2. **Impulso de la TVS con JP1 cerrado:** V_ADC ≤ 4,04 V durante el impulso (inyección ≤ 0,7 mA, filtrada). Fuera de ALI-01 y solo sin U1. Aceptado como residual.
3. **k_ILIS con V_IS alta:** aquí V_IS llega a 8–12 V en funcionamiento normal (con 1,2 kΩ serían < 1,5 V). El datasheet especifica la fuente de corriente hasta V_S − 3,5 V (P_7.5.6), pero mide k_ILIS sin fijar R_IS. **Prototipo:** comparar la lectura a 1 A con el bus a 18 V y a 30 V (diferencia ≤ 3 %).
4. **Fugas del cable mojado:** la carga abierta en OFF falla con fugas por debajo de 159–306 kΩ (§3.3); se vería como «carga presente». La carga abierta en ON lo cubre al regar.
5. **Stock del BTT6050:** 1 658; 10 placas consumen 60. Si baja, la segunda fuente obliga a rehacer *routing* y reparto (§10).
6. **V_OH del GPIO con el LED:** S garantiza 2,64 V sin carga y lo da típico con 40 mA. Con 1,5 mA el margen de V_IN es ≥ 0,3 V; se comprueba en el prototipo (V_IN ≥ 2,2 V con el LED encendido).

## 14. Trazabilidad

| Requisito | Pieza o cálculo | Sección |
|---|---|---|
| REL-01 | 6 canales U7–U12 BTT6050-1ERA + J4–J9 | §2, §9 |
| REL-02 | Salida = BUS_24V (≤ 30 V DC); serigrafía «24 V DC · máx. 30 V» | §8 |
| REL-03 | Entrada activa alta, V_IN ≥ 2,39 V ≥ 2,0 V (Tabla 10, p. 34); *clamp* integrado: E = 81–150 mJ (instalada) a 30 V < 155 mJ (fig. 12, p. 13), L pendiente de medir; D12–D17 DNP | §2.2, §5 |
| REL-04 | R_PD 100 kΩ en IN1–6 y OUT_DEN: ≤ 5 mV | §2.2 |
| REL-05 | Pista `Salidas` 1,2 mm: ΔT 38 °C a 4,9 A, ≈ 1 °C a 1 A; borne 15 A; retorno GND 1,2 mm | §4.2, §11 |
| REL-06 | Pin 1 = OUT_n, pin 2 = GND en J4–J9 | §8 |
| REL-07 | D6–D11 + R63–R68 desde IN_n, 1,5 mA, sin efecto en la carga abierta | §7 |
| REL-08 | Limitación y apagado térmico del BTT (38 A, ≥ 150 °C, *latch*, p. 21-22) + U1; secuencia de identificación ≤ 5 s; T_J y enclavamiento a 4,57–4,9 A | §4.1, §6, §12 |
| REL-09 | J4–J6 arriba (canales 1–3), J7–J9 abajo (4–6) | §8, §11 |
| REL-10 | IS → R_SENSE 10 kΩ → ADC1 6 dB; V_ADC ≤ 2,24 V a 30 V (≤ 2,76 V a 36,7 V) sin corriente en el pin; R_OL 47 kΩ: 0,64 mA ≤ 1 mA; aviso a > 0,82 A | §3, §12 |
| FAB-03 | `Power_In` 2,0 mm; `Salidas` 1,2 mm, ≥ 1 mm; retornos 4,9 A | §11 |
| FAB-07 | 3 bornes de 2 polos por borde (30,5 mm) | §8 |
| FAB-09 | Serigrafía de bornes, tensión y carga máximas | §8 |

## Anexo A. Datos para las fichas (`hardware/componentes/`, fuera de la zona de ing-esquematicos)

| Ficha | Cambio o dato | LCSC | Datasheet | Pinout | Símbolo / huella |
|---|---|---|---|---|---|
| BTT6050-1ERA (actualizar) | «Uso»: U7–U12 en `salidas.kicad_sch`. Añadir: sin R_GND ni zéner en VS (§4.4); vías del EP a BUS_24V (no a GND); BTT6030 con la misma huella pero **distinto pinout** | C534868 | Rev. 1.00 (local) | Tabla 2, p. 4 | Existentes |
| WJ500V-5.08-2P (actualizar) | «Uso»: J1 (alimentación) y J4–J9 en `salidas.kicad_sch` (no en `conectores.kicad_sch`); 7 por placa | C8465 | Local | Pin 1 = OUT_n / pin 2 = GND | Existentes |
| KT-0603R | D6–D11 (y D4). Ya en `bloque-alimentacion.md`; ficha propia si jr-conformidad la pide | C2286 | PDF de LCSC (C2286) | Ánodo / cátodo según el PDF | `Device:LED` / `LED_0603_1608Metric` |
| M7 (DNP) | D12–D17, solo si se aprueba montarlas (§5) | C95872 | PDF de LCSC (C95872) | K / A (banda = cátodo) | `Device:D` / `Diode_SMD:D_SMA` |
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
- **Redes internas** (n = 1…6): `OUTn` (OUT del BTT, R_OL, C_OUT, D DNP, J pin 1), `INn_HS` (R_IN → pin 4), `DENn_HS` (R_DEN → pin 5), `ISn_HS` (pin 6 → R_SENSE), `LEDn_A` (R_LED → ánodo del LED).
- **Conexiones por canal n** (U = U6+n, J = J3+n): IN_n → R(25+n) → `INn_HS` → U pin 4; IN_n → R(31+n) → GND; IN_n → R(62+n) → `LEDn_A` → D(5+n) → GND; OUT_DEN → R(37+n) → `DENn_HS` → U pin 5; U pin 6 → `ISn_HS` → R(44+n) → IS_n; IS_n → R(50+n) → GND y C(38+n) → GND; BUS_24V → U pin 15 (VS), C(26+n) → GND, R(56+n) → `OUTn`; U pines 10, 11, 12 → `OUTn` → C(32+n) → GND, D(11+n) (DNP; cátodo en `OUTn`, ánodo en GND) y J pin 1; J pin 2 → GND; U pin 3 → GND. Pines NC (1, 2, 7, 8, 9, 13, 14) con marca de no conexión. OUT_DEN → R44 → GND. C45 y C46 entre BUS_24V y GND.
