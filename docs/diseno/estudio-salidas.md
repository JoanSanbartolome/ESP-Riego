# Estudio de la tecnología de las salidas (SPEC-0005 · D8, D2)

**Estado:** propuesta para que el usuario decida D8 y D2. No modifica `docs/02-especificaciones-v2.md`.
**Autor:** ing-esquematicos · **Fecha:** 2026-11-04 · **Precios, stock y tipo JLCPCB consultados el 2026-11-04** (LCSC y `jlcpcb.com/partdetail`).
**Requisitos:** REL-01, REL-03, REL-05 (y REL-02, REL-04, REL-08, REL-09, ALI-01…ALI-04, FAB-07, FAB-08).

> La base de piezas local del MCP (`search_jlcpcb_parts`) está vacía (0 piezas), así que los datos de LCSC y JLCPCB se han tomado de sus fichas web. `jr-conformidad` debe confirmar los códigos LCSC antes de usarlos en el esquema.

### Datos de entrada añadidos durante el estudio

Transmitidos por el coordinador el 2026-11-04. Los mensajes llegaron en dos tandas, y la segunda (**sin entrada de AC**) sustituye a la primera en todo lo que toca a la alimentación de la placa.

| # | Dato | Origen | Dónde se usa |
|---|---|---|---|
| N1 | **Única entrada: fuente de 24 V DC de hasta 5 A.** Rango de diseño de **18–30 V DC**, con protección de polaridad y una **TVS de clase SMBJ33A**. Desaparecen la entrada de 24 V AC y el puente rectificador. | Usuario, 2026-11-04 (sustituye la entrada de 24/32 V AC) | Todo el estudio |
| N2 | **Las 6 salidas pueden estar activas a la vez**, con **≈ 4 A en total** en las salidas alimentadas. | Usuario, 2026-11-04 | §1.3, §5, §7.3, §8 |
| N3 | **«Salida alimentada» (D2)** = entregar **24 V DC** a la carga desde la entrada. | Coordinador, 2026-11-04 | §1.7, §1.8 |
| N4 | Las válvulas instaladas siguen siendo de **24 V AC**, pero **ya no se pueden alimentar desde la placa**. Hay que analizar qué haría falta para seguir usándolas: **contacto libre con su propio transformador de 24 V AC (≤ 32 V AC en vacío, ≈ 45 V de pico)**, o **cambiar a válvulas de 24 V DC o de impulso (*latch*)**. | Usuario y coordinador, 2026-11-04 (VAL-0004-01, hallazgo 02) | §1.4, §3.2 |
| N5 | El **triac** solo vale para cargas AC alimentadas desde fuera; con salida alimentada en DC no funciona. | Coordinador, 2026-11-04 (VAL-0004-01, nota 6) | §2.3, §3.3 |
| N6 | Añadir las corrientes de las **electroválvulas de 24 V DC** típicas. | Coordinador, 2026-11-04 | §1.2 |
| U5 | La corriente del LED de control (SSR, optotriac, driver fotovoltaico) se justifica con margen sobre la I_FT máxima en todo el rango de V_F y de 3,3 V: es la causa de H5. | VAL-0004-01, hallazgo 08 | §1.6 |
| U6 | En `docs/02` los REL van de REL-01 a REL-09; **REL-10 no existe** (la spec lo citaba por error). Los requisitos nuevos que se proponen aquí no llevan número: lo asigna el coordinador. | VAL-0004-01, hallazgo 15 | §7.3 |

---

## 0. Resumen para decidir

### 0.1 Las cuatro formas de usar las válvulas

| Vía | Qué es | Qué necesita de la salida |
|---|---|---|
| **V1** | Mantener las válvulas de 24 V AC con **su propio transformador** (≤ 32 V AC en vacío) | **Contacto libre**, flotante y bidireccional, que bloquee ≥ 45,3 V de pico |
| **V2** | Cambiar a válvulas de **24 V DC** | **Salida alimentada** de 24 V DC (o contacto libre con fuente propia) |
| **V3** | Cambiar a válvulas ***latch*** (impulso de 6–9 V DC, con inversión de polaridad) | Etapa común de polaridad y fuente de impulso, y un interruptor bidireccional por canal |
| **V4** | Mantener las válvulas de 24 V AC **alimentadas en 24 V DC con PWM** (impulso + mantenimiento, como OpenSprinkler DC), sin transformador | Salida alimentada con **PWM** por canal; uso no estándar, ajustado a cada válvula |

### 0.2 Tabla comparativa

Valores: ✔ sí · ◐ sí con condición · ✘ no (detalle en §3). Cargas: **B** = bomba pequeña DC; **R** = carga resistiva o LED.

| Opción | V1: AC con su transformador | V2: válvula 24 V DC | V3: *latch* | V4: AC con PWM | B | R | Corto en campo (fuente de 5 A) | Fuga en reposo | Pérdidas a 1 A | Alto de placa | Coste etapa 6 canales (5 / 10 placas)¹ | Montaje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1a Relé estándar (SRD-05) | ✔ | ✔ | ◐ | ✘ | ✔ | ◐ | Aguanta; la fuente limita | ≈ 1 µA | 0,1 W + 0,36 W de bobina | ≈ 86–96 mm | 4,31 $ / 3,74 $ | THT a mano |
| **1b Relé subminiatura (G5NB / HF46F)** | ✔ | ✔ | ◐ | ✘ | ✔ | ◐ | Aguanta; la fuente limita | ≈ 1 µA | 0,1 W + 0,2 W de bobina | **≈ 75–80 mm** | **4,64 $ / 4,07 $** | THT a mano + SMT |
| 2 SSR PhotoMOS de 60 V (AQV252G) | ◐ Solo con ≤ 28 V AC en vacío medidos | ✔ | ◐ | ✘ | ◐ | ✔ | Fusible rápido por canal | ≤ 2 µA | 0,12 W | ≈ 70–75 mm | 19,94 $ / 19,07 $ | Todo SMT |
| 3 Triac + optotriac | ✔ | **✘** | ✘ | ✘ | ✘ | ◐ (AC) | Fusible rápido por canal | ≈ 0,35–1 mA | ≈ 1,0 W | ≈ 75–80 mm | 8,27 $ / 6,17 $ | Todo SMT |
| 4a MOSFET *low-side* | ✘ | ✔ | ✘ | ◐ | ✔ | ✔ | Fusible rápido; **un corto del cable a tierra abre la válvula** | ≤ 1 µA | ≈ 0,15 W | ≈ 66–70 mm | 3,13 $ / 2,42 $ | Todo SMT |
| 4b MOSFET *high-side* discreto | ✘ | ✔ | ✘ | ◐ | ✔ | ✔ | Fusible rápido por canal | ≤ 1 µA | ≈ 0,2 W | ≈ 66–70 mm | 2,74 $ / 2,08 $ | Todo SMT |
| 4c MOSFET bidireccional de 100 V + driver fotovoltaico («SSR discreto») | ✔ | ✔ | ◐ | ✘ | ✔ | ✔ | Fusible rápido por canal | ≤ 3 µA | ≈ 0,5 W | ≈ 70–75 mm | 14,96 $ / 13,78 $ | Todo SMT |
| **5 *High-side switch* inteligente de 24 V (BTT6050-1ERA)** | ✘ | ✔ | ✘ | ◐ | ✔ | ✔ | **Se protege solo y lo diagnostica** | ≤ 0,5 µA | ≈ 0,05–0,1 W | ≈ 70 mm | 8,39 $ / 7,93 $ | Todo SMT |

¹ Etapa de salida solamente (interruptor, protección, excitación del LED, LED indicador, resistencias y borne de 2 polos por canal), por placa, con las tarifas de JLCPCB *Economic PCBA* y los THT soldados a mano. No incluye el fusible rápido por canal, el corte general ni la etapa *latch*. Desglose en §5.

### 0.3 Propuesta (§7)

- **Propuesta: relé subminiatura 1b** (Omron G5NB-1A-E o Hongfa HF46F/5-HS1). Es la opción barata que cubre a la vez **V1**, para seguir con las válvulas instaladas y su transformador, y **V2**, para pasar a válvulas de 24 V DC. Salida alimentada y contacto libre seleccionables por canal (D2 = ambas), con un **corte general** del bus de 24 V.
- **Alternativa: 4c, el «SSR discreto»** de 100 V (2× IRLML0100 + VOM1271T), si se quiere todo SMT y sin desgaste, con las mismas vías V1 y V2.
- **Si el usuario decide abandonar la AC** (solo V2 y, opcionalmente, V4), la mejor opción técnica es la **5 (BTT6050-1ERA)**: protección de cortocircuito, medida de corriente por canal y diagnóstico de carga abierta, a ≈ 8 $ por placa.

---

## 1. Datos de partida

### 1.1 Requisitos y condiciones

- REL-01: 6 salidas. REL-02: ≤ 30 V AC / 36 V DC. REL-04: salidas apagadas en el arranque, el reset y el flasheo. REL-05: ≥ 1 A continuo por canal. REL-08: salida alimentada y/o contacto libre (D2). REL-09: canales 1–3 arriba y 4–6 abajo.
- ALI (pendiente de reescribir por el coordinador con N1): 18–30 V DC, protección de polaridad y TVS SMBJ33A.
- §5: ambiente de −10 a +50 °C; componentes de −20 a +85 °C como mínimo.
- H5 (v1): LED del optoacoplador en serie con un LED rojo desde 3,3 V, sin margen. Ninguna opción lo repite (§1.6).

### 1.2 Las cargas

**a) Electroválvula de 24 V AC (la instalada; con N1 solo se puede usar por V1 o V4)**

| Solenoide | Frecuencia | Arranque (*inrush*) | Mantenimiento | Resistencia de bobina | Fuente |
|---|---|---|---|---|---|
| Rain Bird G3/DV (LFV, HV, ASVF, DV) | 50/60 Hz | 0,30 A (7,2 VA) | 0,19 A (4,6 VA) | 38 Ω | Rain Bird D42606, p. 1 |
| Rain Bird G4 (PGA, PE…) | 50/60 Hz | 0,41 A (9,9 VA) | 0,14 A (3,43 VA) | 30–39 Ω | Rain Bird D42606, p. 1 |
| Hunter PGV | 60 Hz | 0,35 A | 0,19 A | — | Hunter, ficha PGV 1½"/2" |
| Hunter PGV | **50 Hz** | **0,37 A** | **0,21 A** | — | Hunter, ficha PGV 1½"/2" |
| Rain Bird 100DV (tienda) | — | 0,30 A | 0,23 A | 38 Ω | ficha de producto Rain Bird |
| Bermad S-390-T-2W-24VAC-R | AC | 0,25 A | 0,125 A (1,7 W) | 36 Ω | Bermad, ficha S-390-T-2W |

- Valores de diseño por válvula: mantenimiento **0,23 A**, *inrush* **0,41 A**.
- Tensión mínima de funcionamiento: 19 V AC (solenoide de recambio de Hunter).
- Modelo eléctrico (cálculo propio): |Z| = 24 / 0,21 = 114 Ω; R = 38 Ω; L ≈ 0,34 H; cos φ ≈ 0,33. Energía en el pico: ≈ **15 mJ por válvula**.

**b) Electroválvula de 24 V DC (vía V2) — nueva (N6)**

| Solenoide | Arranque | Mantenimiento | Potencia | Resistencia | Fuente |
|---|---|---|---|---|---|
| Bermad S-390-T-2W-24VDC (NC, 2 hilos) | 0,18 A | 0,18 A | 4,2 W | 156 Ω | Bermad, ficha S-390-T-2W («Electrical Data») |
| Bobina RPE 24 V DC (E9820000-24DC) | — | 0,24 A | ≈ 5,8 W (calculado) | ≈ 100 Ω (calculado) | Tienda dvs-beregnung.de (dato del buscador; la página devolvía 404 al consultarla) |

- En una bobina DC el **arranque es igual al mantenimiento**: no hay reactancia que limite la corriente en régimen. La corriente sube con la constante L/R hasta V/R, sin pico.
- Bobina fría: la resistencia del cobre a −10 °C es ≈ 12 % menor que a 20 °C, así que la corriente sube un ≈ 14 %.
- **Valores de diseño por válvula de 24 V DC:** **0,25 A** a 20 °C (redondeo al alza del peor dato) y **0,28 A** en frío; **2 válvulas: 0,56 A**.
- Energía al abrir: con L ≈ 1 H (supuesto, no hay dato del fabricante), ½·L·I² ≈ 31 mJ. Se toma ≤ 50 mJ para dimensionar la protección.

**c) Electroválvula *latch* (vía V3)**

| Solenoide | Tensión de impulso | Resistencia | Corriente de impulso (V/R) | Fuente |
|---|---|---|---|---|
| Rain Bird TBOS (K80920) | 9 V DC (mínimo 6,5 V a 165 psi) | 4,5 Ω ± 0,5 | 2,0 A a 9 V (Rain Bird da «400 mA de *inrush*») | Rain Bird D42606, p. 1 |
| Hunter 458200 | 6 V DC mínimo, 9 V DC máximo recomendado | 4,8 Ω | 1,9 A a 9 V; impulso de ≈ 250 ms (dato de tienda, sin verificar) | Ficha de Hunter (copia), cheapsprinklers.com |
| Bermad S-392-T-2W | 9 V DC (*latch*, 2 hilos) | — | — | Bermad, ficha S-392T (título) |

- Necesita impulsos de **6–9 V y ≈ 2 A durante decenas o cientos de ms**, con **inversión de polaridad** para cerrar.
- Con N1 hace falta una fuente de impulso de 9 V (*buck* de 9 V ≥ 2 A, o condensador cargado a 9 V) y un puente H.

**d) Válvula de 24 V AC alimentada con 24 V DC (vía V4)**

- A 24 V DC continuos: 24 / 38 = 0,63 A y 15 W, frente a ≈ 1,7 W de pérdidas en el cobre con AC. **Se quema.**
- Con **PWM**: impulso a 24 V (0,63 A) durante ≈ 0,2–0,5 s para abrir y mantenimiento a ≈ 9 V equivalentes (ciclo de trabajo ≈ 37 %), ≈ 0,24 A medios y ≈ 2,1 W en la bobina. Es lo que hace OpenSprinkler DC: impulso por *boost* y mantenimiento a 9 V.
- Con τ = L/R ≈ 9 ms, un PWM de 200 Hz o más da una corriente casi continua. Necesita un diodo de libre circulación rápido y un PWM por canal (el ESP32-S3 tiene 8 canales LEDC).
- **Uso no estándar:** hay que ajustarlo para cada modelo de válvula y queda fuera de la garantía del fabricante.

**Criterio de fuga en reposo.**
- Con 1 mA de fuga, la tensión sobre la bobina es de 0,11 V en una válvula de AC (114 Ω) y de 0,16 V en una de DC (156 Ω). Las dos están muy por debajo de su tensión de apertura.
- Cualquier fuga de ≤ 1 mA **no puede abrir ni mantener una válvula**. Sí puede dar una tensión «fantasma» en un polímetro de alta impedancia.

### 1.3 Corriente total y cortocircuito con una fuente de 5 A (N1, N2)

| Caso | Corriente en el bus de 24 V de las salidas | ¿Cabe en 4 A? |
|---|---|---|
| V2: 6 canales × 2 válvulas DC en frío | 6 × 0,56 = **3,4 A** | Sí |
| V4: 6 canales × 2 válvulas AC con PWM, mantenimiento | 6 × 0,48 = 2,9 A | Sí |
| V4: los 6 impulsos de apertura a la vez | 6 × 1,26 = 7,6 A | **No:** el firmware escalona la apertura (≥ 0,5 s entre canales) |
| V3: impulso *latch* | ≈ 2 A, de canal en canal | Sí |
| 6 canales × 1 A (REL-05 a la vez) | 6 A | **No:** por encima de N2 |
| V1 (contacto libre) | La da el transformador del usuario, no el bus | — |

- Lógica: ≈ 2–3 W, ≈ 0,1 A a 24 V, incluidas las bobinas de relé si las hay. Con 4 A de salidas queda ≈ 1 A de margen en la fuente.
- **Cortocircuito en el cable con la salida alimentada:**
  - Una fuente conmutada de 24 V y 5 A limita la corriente a ≈ 105–150 % (5,3–7,5 A; valor típico, no hay modelo) y entra en *hiccup*. Antes descarga sus condensadores de salida y el *bulk* de la placa en un pico de decenas de A durante µs.
  - Un fusible de 4 A T en el bus **no salta a tiempo** con 1,3–1,9·I_n: la fuente se queda limitando y **toda la placa (lógica incluida) cae o se reinicia**.
  - Hace falta **protección por canal**: fusible rápido (≈ 1,5 A F, que con 5 A abre en ms), PTC (más lenta), o un interruptor que limite la corriente (opción 5). Conviene además que la lógica tenga autonomía (diodo y condensador antes del *buck*) para aguantar el tiempo de disparo.
- **Cortocircuito en contacto libre (V1):** lo alimenta el transformador del usuario (30–60 VA típicos en riego doméstico, sin dato): ≈ 5–15 A hasta que actúe su protección. El relé lo aguanta; los semiconductores necesitan un fusible rápido por canal.
- La prueba térmica de §6 («1 h con las 6 salidas activas a la corriente de REL-05») son 6 A, por encima de N2. Se propone hacerla con **4 A en total** (§7.3).

### 1.4 Topología con entrada de 24 V DC

- Sin puente rectificador, **la GND es el negativo de la fuente**, suponiendo la protección de polaridad en el lado positivo (diodo ideal o P-MOS). Los interruptores referidos a GND (*low-side*, *high-side*, *smart switch*) ya pueden alimentar cargas DC directamente.
- **V1 (AC con su transformador):** el circuito de AC del usuario es independiente de la placa. Solo sirve un interruptor **flotante y bidireccional** que bloquee ≥ 45,3 V de pico: contacto de relé, SSR, triac con optotriac o MOSFET *back-to-back* con driver aislado. Hace falta aislamiento entre ese circuito y la lógica (ambos son MBTS) y ≥ 1 mm de separación en el cobre.
- **Interruptor *high-side* o *low-side* en la salida alimentada:**
  - Con *low-side* (4a), el cable de campo queda a +24 V en reposo, así que **un corto del cable a tierra (terreno húmedo) equivale a cerrar el interruptor: la válvula se abre**, y una fuga a tierra provoca corrosión electrolítica.
  - Con *high-side* (relé o SSR desde +24 V, 4b y 5), el cable queda a 0 V en reposo, y un corto a tierra es un cortocircuito que la protección corta.
  - **Se recomienda *high-side*** (COM = GND en el borne).

### 1.5 Tensiones de bloqueo

**Salida alimentada (bus de 24 V):**
- Régimen de 18–30 V.
- En un impulso de entrada, el bus sube hasta el recorte de la **SMBJ33A**: V_BR de 36,7 a 40,6 V y **V_C = 53,3 V con I_PP = 11,3 A** (valores estándar de la serie SMBJ; confirmar con el fabricante elegido). Las piezas conectadas al bus necesitan ≥ 60 V.

**Contacto libre (V1):**
- Pico de 32 × √2 = **45,3 V** del transformador del usuario.
- La TVS del contacto tiene que tener V_RWM ≥ 45,3 V: **SMAJ48CA** (V_RWM 48 V, V_BR ≤ 58,9 V, V_C 77,4 V con 5,2 A).

| Elemento | Salida alimentada (≤ 53 V) | Contacto libre (45,3 V de pico; recorte de la TVS ≤ 59 V con la corriente de la válvula, 77 V con I_PP) | Resultado |
|---|---|---|---|
| Contacto de relé (G5NB, HF46F, SRD) | 30 V DC de conmutación nominal (3 A G5NB, 5 A HF46F) | 250–277 V AC | ✔ |
| PhotoMOS AQV252G (60 V; 48 V de pico recomendados) | ✔ con SMAJ33CA o un diodo de libre circulación en la placa | Con SMAJ48CA el recorte a ≈ 0,3–0,6 A queda en ≈ 54–59 V: **0–6 V de margen** sobre 60 V | Solo V2; V1 únicamente si se miden ≤ 28 V AC (SMAJ40CA) |
| Triac BT136S + MOC3023 | No aplicable (no se apaga en DC) | 600 V / 400 V | ✔ en V1 |
| MOSFET N de 60 V (IRLML0060), 4a | 60 V frente a 53,3 V: 6,7 V de margen | — | ✔ (mejor con 100 V) |
| MOSFET P de 60 V (FDN5618P), 4b | 6,7 V de margen | — | ✔ |
| MOSFET N de 100 V (IRLML0100), 4c | ✔ | V_C de la SMAJ48CA = 77,4 V < 100 V | ✔ |
| BTT6050-1ERA | V_S máx. 48 V; V_S(LD) 65 V (impulso con R_I = 2 Ω) | — | ✔ (el impulso de la SMBJ33A queda dentro de V_S(LD)) |
| ISP752R | V_bb máx. 52 V < 53,3 V; V_bb(AZ) 62 V con R_GND | — | ◐ |

### 1.6 Excitación del LED de control: margen sobre I_FT (U5, H5)

Opciones afectadas: 2 (SSR), 3 (optotriac) y 4c (VOM1271T).

**Excitación directa desde el GPIO: no se recomienda.** El ESP32-S3 solo especifica V_OH ≥ 0,8·VDD **con carga de alta impedancia**. I_OH = 40 mA con V_OH ≥ 2,64 V y PAD_DRIVER = 3 es un valor **típico**, no garantizado (datasheet ESP32-S3 v2.2, tabla 5-4). No se puede acotar la corriente mínima del LED, que es lo que falló en H5.

**Esquema propuesto:** el LED se alimenta desde el raíl de **3,3 V** con una resistencia fija al 1 % y un **AO3400A** (*Basic*) como interruptor *low-side*. La puerta va al GPIO con un *pull-down* de 100 kΩ (REL-04). El LED indicador va en una rama propia en paralelo, nunca en serie con el LED IR.

**Hipótesis de cálculo:**
- 3,3 V ± 3 % (3,20–3,40 V);
- V_DS del AO3400A ≤ 0,01 V;
- V_F mínima de 1,0 V (supuesto conservador; los datasheets no la dan).

Fórmulas: I_F,mín = (3,20 − V_F,máx − 0,01) / (1,01·R) e I_F,máx = (3,40 − 1,0) / (0,99·R).

| LED de control | I_FT máx. (25 °C) | Requisito de I_F mínima | V_F máx. (fuente) | R | I_F mín. | I_F máx. | Límite | Margen sobre I_FT |
|---|---|---|---|---|---|---|---|---|
| AQV252G (opción 2) | 3 mA | ≥ 5 mA (mínimo recomendado) y ≥ 2·I_FT → **≥ 10 mA** | 1,5 V a 5 mA (ASCTB144E p. 2) | 150 Ω | **11,2 mA** | 16,2 mA | 30 mA recomendados | ×3,7 |
| GAQV252G3EH (opción 2 alt.) | 7 mA (LCSC) | ≥ 2·I_FT → **≥ 14 mA** | 1,5 V (supuesto) | 110 Ω | **15,2 mA** | 22,0 mA | 50 mA | ×2,2 |
| MOC3023 (opción 3) | 5 mA | ×1,3 a −20 °C (curva normalizada, a confirmar en la figura) ×1,25 de envejecimiento = 8,1 mA → **≥ 10 mA** | 1,5 V a 10 mA (MOC302xM p. 4) | 150 Ω | **11,2 mA** | 16,2 mA | 60 mA máx. abs. | ×2,2 |
| VOM1271T (opción 4c) | — (I_F = 10 mA da V_OC ≥ 7,8 V) | **≥ 10 mA** | 1,6 V a 10 mA (Vishay) | 150 Ω | **10,5 mA** | 16,2 mA | 50 mA | — |

- 6 canales: ≈ 100 mA del raíl de 3,3 V (ALI-07: ≥ 800 mA).
- Con un expansor I²C (SPEC-0006), el expansor solo excita la puerta del AO3400A.
- Las opciones 1, 4a, 4b y 5 no tienen LED de control. La bobina del relé (5 V, cierra con ≈ 75 % de la nominal; dato típico, a confirmar) y las entradas CMOS (BTT6050: compatible con 3,3 V) no tienen el problema de H5.

### 1.7 Salida alimentada en DC (N3, N5)

- Con N1, toda salida alimentada entrega **24 V DC con polaridad fija**: + en OUT_n y − en COM con un interruptor *high-side*.
- Ya no depende de cómo se cablee la entrada, porque hay protección de polaridad.
- Por opción:
  - relé, SSR, 4b, 4c y 5: funcionan con cargas DC;
  - 4a: funciona, pero con el cable a +24 V en reposo (§1.4);
  - **triac: no funciona.** Una vez disparado no se apaga en DC y la válvula se quedaría abierta. Solo sirve en V1.
- Una válvula de 24 V AC conectada a la salida alimentada sin PWM se quema (§1.2 d). La serigrafía y el manual deben decir «salida alimentada: 24 V DC; no conectar válvulas de AC».

### 1.8 Formas de conectar (D2) y polos de borne

| Forma | Esquema | Polos por canal | Polos por borde (3 canales) | Ancho a 5,08 mm |
|---|---|---|---|---|
| A. Alimentada 24 V DC, *high-side* | +24 V (fusible + corte general) → interruptor → **OUT_n** → válvula → **COM** (GND) | 1 + COM compartido | 4 | 20,3 mm |
| A'. Alimentada 24 V DC, *low-side* (4a) | **COM** (+24 V) → válvula → OUT_n → interruptor → GND | 1 + COM | 4 | 20,3 mm |
| C. Contacto libre (V1: transformador del usuario) | **OUT_n** — interruptor — **RET_n** | 2 | 6 | 30,5 mm |
| A + C seleccionable (puente de soldadura por canal) | Puente cerrado: RET_n → +24 V del bus. Puente abierto: contacto libre | 2 + COM | 7 | 35,6 mm |
| V3 *latch* (ampliación) | Puente H común (±9 V) entre la barra LATCH y COM_L; el interruptor del canal selecciona la válvula | 2 + COM_L | 7 | 35,6 mm |

Todas caben en 100 mm de ancho. En el borde inferior hay que añadir la entrada (2 polos) y el conector de expansión (≈ 15 mm). Con A + C quedan ≈ 61 mm más los huecos. El COM y la entrada llevan hasta 4–5 A; el WJ500V está especificado para 18 A.

---

## 2. Opciones

Criterios comunes a todas las opciones:

- *Pull-down* de 100 kΩ en la puerta o en la entrada, lógica activa a nivel alto y nada en los pines de arranque (REL-04, MCU-05).
- Vida útil con 6 maniobras al día: ≈ 2200 al año.
- TVS de salida **SMAJ48CA** cuando la salida puede trabajar como contacto libre (V1).

### 2.1 Opción 1 — Relé electromecánico

**Funcionamiento y esquema de principio.**

```
GPIO ──R 100Ω──┬── G  AO3400A           +5V ──┬────────┐
             100k│      D ── bobina ───────────┘  1N4148W (cátodo a +5V)
               GND     S ── GND
Contacto:  RET_n ──[ NO ]── OUT_n      SMAJ48CA entre RET_n y OUT_n
Puente JPn (por canal): RET_n ↔ +24V_SAL (bus con fusible y corte general)  → salida alimentada
                        abierto → contacto libre (V1)
LED de canal: rama propia (R + LED de +5 V al drenaje)
```

**Variantes.**
- 1a, **SRD-05VDC-SL-C**: 19,2 × 15,6 × 15,8 mm, 70 Ω (71 mA, 360 mW), 1 C, 10 A a 28 V DC (según LCSC).
- 1b, **Omron G5NB-1A-E** o **Hongfa HF46F/5-HS1**: 20,5 × 7 × 15,3 mm, 125 Ω (40 mA, 200 mW), 1 A (NO). G5NB-1A-E: 5 A a 250 V AC y 3 A a 30 V DC. HF46F/5-HS1: 5 A a 30 V DC (LCSC).

**Vías.**
- V1: ✔ (contacto libre de 250 V AC).
- V2: ✔ (24 V DC; 0,56 A frente a 3 A a 30 V DC).
- V3: ◐ (con la etapa común de polaridad).
- V4: ✘ (no admite PWM).

**Cargas.** Bomba DC de ≤ 3 A: ✔. Resistiva y LED: ◐, carga mínima de 10 mA a 5 V DC (G5NB, valor de referencia de Omron).

**Corriente y disipación.**
- Contacto ≤ 100 mΩ: 0,1 W a 1 A; 6 × 0,67 A → 0,27 W.
- Bobinas: 7 × 0,2 W = **1,4 W** con todo activo y el corte general. Son 280 mA de 5 V, a tener en cuenta en AMB-02.

**Fuga en reposo.** ≈ 1 µA (aislamiento + SMAJ48CA, I_R ≤ 1 µA según LCSC).

**Carga inductiva.**
- La SMAJ48CA en el contacto absorbe ≤ 50 mJ en los dos modos.
- En la salida alimentada, al abrir, OUT_n baja hasta ≈ 24 − 59 ≈ −35 V respecto a GND hasta que se descarga la bobina: lo que se conecte a OUT_n, como una medida de tensión, tiene que tolerarlo.
- El arco en DC a 24 V y 0,5 A está muy por debajo de 3 A a 30 V DC.

**Seguridad.**
- Aislamiento de kV entre bobina y contacto: el circuito AC del usuario (V1) queda aislado de la lógica.
- Estado seguro: relé abierto sin tensión.
- **Corto en campo:** el contacto aguanta el impulso. En la salida alimentada la fuente limita y la placa cae si no hay fusible por canal (§1.3).
- **Modo de fallo:** contacto soldado o MOSFET de bobina en corto, con la válvula abierta. Es raro.

**D2.** Alimentada 24 V DC (*high-side*, COM = GND) y contacto libre, seleccionables por canal. 2 polos + COM por borde.

**Placa.** 1b en paralelo al borde: franja de ≈ 21–25 mm; 1a: ≈ 28 mm. THT a mano (FAB-06).

**Vida útil.** G5NB: ≥ 100 000 maniobras a 5 A 250 V AC y ≥ 200 000 a 3 A 30 V DC, más de 45 años de uso.

**Expansión.** Se repite con un expansor que ataca el AO3400A. Las salidas del expansor arrancan en alta impedancia y el *pull-down* mantiene el relé abierto. El módulo necesita su parte del bus de 24 V para la salida alimentada.

**Pros.**
- **Cubre V1 y V2 a la vez y por canal:** se pueden seguir usando las válvulas de AC mientras se migra a DC.
- Aislamiento real. Fuga y caída despreciables. Robusto ante cortos.
- Barato.

**Contras.**
- THT a mano y clic.
- 1,4 W de bobinas.
- Sin PWM (no admite V4).
- Ocupa más.

**Piezas candidatas**

| Función | MPN | Fabricante | LCSC | Tipo JLCPCB | Precio (USD) | Stock | Datasheet |
|---|---|---|---|---|---|---|---|
| Relé subminiatura (principal) | G5NB-1A-E-DC5V | Omron | C48746 | Extended (THT) | 0,3551 (≥ 30) | 119 277 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/5933ba504d6295ffcb9660ee63922fa6.pdf?productCode=C48746) |
| Relé subminiatura (alternativa) | HF46F/5-HS1 | Hongfa | C5274168 | Extended (THT) | 0,8174 (≥ 30) | 21 887 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/76598c474c9acd8357505ce76bf406d9.pdf?productCode=C5274168) |
| Relé estándar (1a; candidato al corte general) | SRD-05VDC-SL-C | Songle | C35449 | Extended (THT) | 0,2990 (≥ 30) | 116 872 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/9ddfe54b7529126320ff1ddcabf6bab7.pdf?productCode=C35449) |
| Driver de bobina / de LED | AO3400A | AOS | C20917 | **Basic** | 0,0899 (≥ 5) / 0,0725 (≥ 50) | 355 435 | [Ficha](https://www.lcsc.com/product-detail/C20917.html) |
| Diodo de bobina | 1N4148W | ST (Semtech) | C81598 | **Basic** | 0,0125 (≥ 50) | 2 360 800 | [Ficha](https://www.lcsc.com/product-detail/C81598.html) |
| TVS de contacto | SMAJ48CA | MDD | C173501 | Extended | 0,0403 (≥ 20) | 12 620 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/57d80c866df506764ddd60be335ccdff.pdf?productCode=C173501) |
| LED de canal | KT-0603R | Hubei KENTO | C2286 | **Basic** | 0,0077 (≥ 100) | 4 238 300 | [Ficha](https://www.lcsc.com/product-detail/C2286.html) |
| Borne 2 polos, 5,08 mm | WJ500V-5.08-2P | Kangnex | C8465 | Extended (THT) | 0,136 (≥ 5) / 0,1096 (≥ 50) | 275 380 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/5a3d038c44f6e3872ef57456c5bdf975.pdf?productCode=C8465) |

### 2.2 Opción 2 — SSR de salida MOSFET (PhotoMOS)

**Funcionamiento y esquema de principio.**

```
+3V3 ──R 150Ω 1%── LED AQV252G (1-2) ── D AO3400A S ── GND;  G ← GPIO (100k a GND)   (§1.6)
Salida:  RET_n ──[ 4-6 AQV252G ]── OUT_n    TVS en paralelo (SMAJ33CA solo para V2; SMAJ40CA para V1 con ≤ 28 V AC)
```

**Pieza principal.** Panasonic **AQV252G** (AQV252GAX en SMD):
- 60 V de máximo absoluto y 48 V de pico recomendados;
- 2,5 A continuos y 5 A de pico (100 ms, un impulso);
- R_on ≤ 0,12 Ω;
- I_FT ≤ 3 mA;
- fuga ≤ 1 µA;
- t_on 1,1–5 ms;
- 1500 V eficaces de aislamiento.

Alternativa: SUPSiC **GAQV252G3EH**.

**Vías.**
- V1: ◐. Con 32 V AC (45,3 V de pico) **no hay TVS que deje margen** frente a los 60 V (§1.5). Solo vale si el usuario mide ≤ 28 V AC en vacío y se usa la SMAJ40CA (V_BR 44,4–49,1 V, ≈ 10 V de margen). La versión de 100 V (Letex LT925, C2890348) tiene **3 unidades** en LCSC.
- V2: ✔ con SMAJ33CA, o con un diodo de libre circulación si el canal es solo de salida alimentada.
- V3: ◐ con la etapa común.
- V4: ✘ (t_on de hasta 5 ms; no apto para PWM).

**Cargas.** Bomba DC: ◐ (arranque ≤ 5 A / 100 ms). Resistiva y LED: ✔, sin mínimo.

**Disipación.** 0,12 W a 1 A; 0,32 W con 6 × 0,67 A: la más fría.

**Fuga en reposo.** ≤ 2 µA.

**Seguridad.**
- Aislamiento de 1,5 kV.
- **Corto en campo:** con la fuente de 5 A (5,3–7,5 A más el pico de los condensadores) supera los 5 A / 100 ms. Necesita un fusible rápido por canal.
- **Modo de fallo:** cortocircuito, con la válvula abierta.

**D2.** Las dos formas, con la limitación de tensión en V1. 2 polos + COM.

**Placa.** Franja de ≈ 20–22 mm. Todo SMT.

**Pros.**
- Silenciosa, sin desgaste, la más fría y baja.

**Contras.**
- Sin margen para V1 con 32 V AC.
- Cara (2,8 $ por canal).
- Frágil ante cortos.
- La TVS depende del uso del canal.

**Piezas candidatas**

| Función | MPN | Fabricante | LCSC | Tipo JLCPCB | Precio (USD) | Stock | Datasheet |
|---|---|---|---|---|---|---|---|
| SSR de 60 V (principal) | AQV252GAX | Panasonic | C425149 | Extended | 2,8039 (≥ 30) | 5 650 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/eaef62e8d8c62312c369a4537573fadb.pdf?productCode=C425149) |
| SSR de 60 V (alternativa) | GAQV252G3EH | SUPSiC | C7435170 | Extended | 1,9013 (≥ 30) | 1 000 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/fc5528091e245e3b9340a0a364076b20.pdf?productCode=C7435170) |
| SSR de 100 V (sin stock útil) | LT925 | Letex | C2890348 | — | 1,9135 (≥ 50) | **3** | [PDF](https://datasheet.lcsc.com/datasheet/pdf/667c2bb9d044131a1ea76f426ad82ffa.pdf?productCode=C2890348) |
| TVS para V1 con ≤ 28 V AC | SMAJ40CA | MDD | C113970 | Extended | 0,0435 (≥ 20) | 47 760 | [Ficha](https://www.lcsc.com/product-detail/C113970.html) |
| Driver, LED, borne | ver §2.1 | | C20917, C2286, C8465 | | | | |

La SMAJ33CA para V2 está pendiente de código LCSC. Descartadas: AQV252G2SX (C719719, 50 V en LCSC) y G3VM-61HR (C20468424, sin stock).

### 2.3 Opción 3 — Triac con optotriac

**Funcionamiento y esquema de principio.**

```
+3V3 ──R 150Ω 1%── LED MOC3023 (1-2) ── D AO3400A S ── GND;  G ← GPIO (100k a GND)   (§1.6)
RET_n ── MT2 ─[BT136S]─ MT1 ── OUT_n      (transformador del usuario en serie con la válvula)
         MT2 ── R 180Ω ── MOC3023 (6-4) ── puerta;  snubber RC (47 nF 100 V + 100 Ω) y SMAJ48CA MT2–MT1
```

Optotriac **de fase aleatoria** (MOC3023): con carga inductiva el triac se apaga en el cero de corriente, cuando la tensión ya vale ≈ 32–43 V, por encima de la V_INH ≤ 20 V del MOC306x de paso por cero (datasheet de onsemi). *Razonamiento propio, a validar en prototipo.*

**Vías.**
- V1: ✔. Es la solución clásica para 24 V AC, aquí con el transformador del usuario.
- V2: **✘**. No se apaga en DC (N5).
- V3: ✘.
- V4: ✘.

**Cargas.** Bomba: solo la bobina de AC de un relé de arranque alimentado desde fuera. Resistiva y LED: solo AC y con I > I_H (≤ 20 mA).

**Disipación.** ≈ 1,0 W a 1 A (≤ 1,5 W): V_T0 ≈ 1,0 V estimado y r_d ≈ 0,14 Ω, con V_TM ≤ 1,7 V a 5 A (JSCJ). Con 0,46 A, ≈ 0,44 W. La corriente de V1 la da el transformador del usuario y no cuenta en el bus de 4 A, pero el calor queda dentro de la caja: hasta ≈ 2,6 W con 6 canales a 0,46 A.

**Fuga en reposo.** Snubber: 24 V × 2π·50·47 nF = **0,35 mA** (1,0 mA con 100 nF y 32 V AC). Más I_DRM ≤ 10 µA. No mantiene la válvula.

**Seguridad.**
- Aislamiento del optotriac de 4170 V eficaces.
- Corto en V1: I²t del BT136S ≈ 3 A²s; necesita un fusible rápido por canal.
- **Modo de fallo:** triac en corto, disparo espurio por dV/dt.

**D2.** **Solo contacto libre para circuitos AC externos.** No puede dar salida alimentada (N3, N5). 2 polos por canal.

**Placa.** Franja de ≈ 22–25 mm: sin carga de 1 A continuo desde la placa, basta el cobre de 0,5 A. Todo SMT.

**Pros.**
- La solución estándar de 24 V AC, barata y SMT, con 600 V de bloqueo.

**Contras.**
- **Solo V1:** queda atada a válvulas de AC con transformador propio, justo lo que el usuario no quiere (DEC-0002 §6).
- Caída de 1–1,5 V. Fuga del snubber. 4 piezas Extended.

**Piezas candidatas**

| Función | MPN | Fabricante | LCSC | Tipo JLCPCB | Precio (USD) | Stock | Datasheet |
|---|---|---|---|---|---|---|---|
| Triac 6 A, DPAK | BT136S | JSCJ | C23427 | Extended | 0,1939 (≥ 5) / 0,1574 (≥ 50) | 12 645 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/84a3b6754cab4564ad83e72f4eb013b9.pdf?productCode=C23427) |
| Triac 1 A, SOT-223 (alternativa) | Z0109MN 5AA4 | ST | C2971682 | Extended | 0,3772 (≥ 30) | **57** | [PDF](https://datasheet.lcsc.com/datasheet/pdf/1ccbee8169df5234e3d3d72fee58989d.pdf?productCode=C2971682) |
| Optotriac SMD | MOC3023SM | onsemi | C899792 | Extended | 0,4312 (≥ 10) / 0,3668 (≥ 50) | 1 008 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/e7cf114dd4ff3540a2567a41793d8554.pdf?productCode=C899792) |
| Optotriac DIP (alternativa) | MOC3023M | onsemi | C5240 | Extended (THT) | 0,4016 (≥ 5) / 0,2882 (≥ 50) | 42 810 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/764d290c828d44119733e2a09d64463f.pdf?productCode=C5240) |
| TVS, driver, LED, borne | ver §2.1 | | C173501, C20917, C2286, C8465 | | | | |

### 2.4 Opción 4 — MOSFET discreto

**4a, *low-side*.**

```
+24V (COM del borne) ── válvula ── OUT_n ── D IRLML0060 S ── GND;  M7/Schottky de OUT_n a +24V
Puerta a 5 V: GPIO → MMBT3904 → traslación no inversora (o MOSFET de 60 V especificado a 2,5 V)
```

**4b, *high-side*.**

```
+24V ── S FDN5618P D ── OUT_n ── válvula ── COM (GND);  M7 de GND (ánodo) a OUT_n (cátodo)
G ── divisor 10k/22k (V_GS ≈ 0,31·V_bus = 5,6–9,3 V) ── colector MMBT3904;  GPIO → base (100k a GND)
```

**4c, bidireccional (el «SSR discreto»).**

```
+3V3 ──R 150Ω 1%── LED VOM1271T ── D AO3400A S ── GND;  G ← GPIO (100k a GND)   (§1.6)
VOM1271T (V_OC ≥ 7,8 V con I_F = 10 mA) → puertas y fuentes comunes de 2× IRLML0100 (100 V)
RET_n ── D1 [Q1] S ═ S [Q2] D2 ── OUT_n;   SMAJ48CA entre RET_n y OUT_n (V_C 77,4 V < 100 V)
```

**Vías.**
- 4a/4b:
  - V1: ✘ (referidos a GND).
  - V2: ✔.
  - V3: ✘ (el diodo interno no bloquea la polaridad inversa).
  - V4: ◐ (PWM a ≥ 200 Hz con diodo Schottky de ≥ 60 V; ajuste por válvula).
- 4c:
  - V1: ✔ (100 V).
  - V2: ✔.
  - V3: ◐ con la etapa común.
  - V4: ✘ (el driver fotovoltaico conmuta en cientos de µs a ms; no apto para PWM).

**Disipación.**
- 4a: IRLML0060, ≤ 116 mΩ con 4,5 V → ≈ 0,12–0,15 W a 1 A.
- 4b: FDN5618P, ≈ 0,17–0,19 Ω → ≈ 0,2 W.
- 4c: 2 × ≈ 0,25 Ω (IRLML0100 con 7,8 V; 220 mΩ a 10 V) → ≈ **0,5 W a 1 A**; con 6 × 0,67 A, 1,35 W.

**Fuga en reposo.** ≤ 1 µA (≤ 3 µA en 4c).

**Seguridad.**
- 4a: **un corto del cable a tierra abre la válvula**, y el cable queda a +24 V en reposo (§1.4). No recomendable en campo.
- 4a/4b/4c: sin protección propia. Corto en campo → fusible rápido por canal.
- 4c: aislamiento de 4,5 kV.
- **Modo de fallo:** MOSFET en corto, con la válvula abierta.

**D2.**
- 4a/4b: solo salida alimentada, 1 polo + COM.
- 4c: las dos formas, 2 + COM.

**Placa.** 4a/4b: ≈ 16–18 mm. 4c: ≈ 20–22 mm. Todo SMT.

**Pros.**
- 4b: la más barata para V2 y V4, con el cable a 0 V en reposo.
- 4c: cubre V1 y V2 en SMT con 100 V de bloqueo.

**Contras.**
- Sin protección.
- 4c cuesta como un SSR y disipa 0,5 W por canal a 1 A.

**Piezas candidatas**

| Función | MPN | Fabricante | LCSC | Tipo JLCPCB | Precio (USD) | Stock | Datasheet |
|---|---|---|---|---|---|---|---|
| MOSFET N de 60 V (4a) | IRLML0060TRPBF | Infineon | C67274 | Extended | 0,2197 (≥ 5) / 0,1793 (≥ 50) | 35 925 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/40ec76b953bd4b6b83cd3e2058a79dba.pdf?productCode=C67274) |
| MOSFET N de 100 V (4c; alternativa de 4a) | IRLML0100TRPBF | Infineon | C53658 | Extended | 0,3607 (≥ 5) / 0,3124 (≥ 50) | 9 460 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/749828b75c4e4bb491f31b3834aa41e4.pdf?productCode=C53658) |
| MOSFET P de 60 V (4b) | FDN5618P | onsemi | C400792 | Extended | 0,1522 (≥ 5) / 0,1196 (≥ 50) | 24 750 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/629cfb3c8437406c7fc1aeb2ac929054.pdf?productCode=C400792) |
| NPN de traslación (4a/4b) | MMBT3904 | JSCJ | C20526 | **Basic** | 0,0118 (≥ 50) | 2 369 500 | [Ficha](https://www.lcsc.com/product-detail/C20526.html) |
| Driver fotovoltaico (4c) | VOM1271T | Vishay | C146286 | Extended | 1,2370 (≥ 30) | 6 238 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/5bb285b0c6eb43ddaec41c184c50e9b2.pdf?productCode=C146286) |
| Diodo de libre circulación sin PWM | M7 | MDD | C95872 | Basic (por confirmar) | 0,0104 (≥ 100) | 5 869 500 | [Ficha](https://www.lcsc.com/product-detail/C95872.html) |

Descartados para el bus: el SS14 (C2480, 40 V < 53 V) y el AO3400A (30 V). El Schottky de ≥ 60 V para PWM está pendiente.

### 2.5 Opción 5 — *High-side switch* inteligente de 24 V

**Funcionamiento.** MOSFET N con bomba de carga, entradas compatibles con 3,3 V, limitación de corriente, protección térmica y de sobretensión, *clamp* inductivo interno y **medida proporcional de corriente** (pin IS, k_ILIS ≈ 1500). Diagnostica la carga abierta con la salida encendida y apagada, el cortocircuito a GND y a V_S, y la sobretemperatura. Esquema de principio:

```
+24V ── VS BTT6050-1ERA OUT ── OUT_n ── válvula ── COM (GND);  M7/Schottky GND→OUT_n solo si hay PWM (V4)
GPIO ── R_IN ── IN (100k a GND);   GPIO ── R_DEN ── DEN
IS ── R_IS a GND ── ADC1 (los IS de los 6 canales se pueden unir en una sola entrada ADC1 y elegir el canal con DEN)
GND del IC ── R_GND ── GND
```

**Pieza principal.** Infineon **BTT6050-1ERA** (PROFET+ 24 V):
- V_S de funcionamiento de 5–36 V (48 V máximo absoluto) y **V_S(LD) = 65 V**;
- R_DS(on) ≤ 100 mΩ a 150 °C (50 mΩ nominales);
- I_L(NOM) 4,5 A;
- limitación de corriente mínima de 38 A;
- fuga en reposo ≤ 0,5 µA a 25 °C;
- E_AS 60 mJ (4,5 A, 28 V);
- PG-TDSO-14.

Alternativa: **BTT6030-2ERA**, de 2 canales (32 mΩ, 6 A por canal, 10 479 en stock). Tres circuitos cubren los 6 canales.

**Vías.**
- V1: ✘.
- V2: ✔.
- V3: ✘.
- V4: ◐ (PWM con diodo de libre circulación; comprobar la frecuencia máxima en el datasheet).

**Cargas.** Bomba DC: ✔ (4,5 A). Resistiva y LED: ✔.

**Disipación.** 0,05 W a 1 A con 50 mΩ, 0,1 W en caliente. La más baja.

**Fuga en reposo.** ≤ 0,5 µA.

**Tensión.** Bus de 18–30 V dentro de 5–36 V. El impulso de la SMBJ33A (≤ 53,3 V) queda dentro de V_S(LD) = 65 V.

**Seguridad.**
- **Corto en campo:** se limita y se apaga por temperatura sin destruirse, y el MCU lo ve en IS. La limitación mínima (38 A) es más alta que la de la fuente, así que **el primer ms lo limita la fuente**. El MCU tiene que apagar el canal en cuanto IS indique sobrecorriente, y la lógica necesita autonomía (§1.3). Es la única opción que lo **diagnostica**, y la medida de IS detecta también una **válvula desconectada o un cable cortado** (carga abierta).
- **Modo de fallo:** cortocircuito residual por sobretensión o ESD; detectable porque IS indica corriente con IN en bajo.

**D2.** Solo salida alimentada (*high-side*, COM = GND), 1 polo + COM.

**Placa.** TDSO-14 con su *pad* expuesto; franja de ≈ 18–20 mm; todo SMT.

**Pros.**
- Protección, medida de corriente por canal y diagnóstico.
- La que menos disipa.
- Cable a 0 V en reposo.
- Stock suficiente para 10 placas (1748 / 10 479).

**Contras.**
- No admite V1: obliga a cambiar las válvulas instaladas (V2) o a moverlas por PWM (V4).
- Un ADC1 y 1–2 GPIO más (DEN).

**Piezas candidatas**

| Función | MPN | Fabricante | LCSC | Tipo JLCPCB | Precio (USD) | Stock | Datasheet |
|---|---|---|---|---|---|---|---|
| *High-side* 24 V, 1 canal (principal) | BTT6050-1ERA | Infineon | C534868 | Extended | 1,0889 (≥ 30) | 1 748 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/f332d8427495765ea0546e562dd08e67.pdf?productCode=C534868) |
| *High-side* 24 V, 2 canales (alternativa) | BTT6030-2ERA | Infineon | C534865 | Extended | 2,2173 (≥ 30) | 10 479 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/c717e93e2471b98176c6383deb6f8e7a.pdf?productCode=C534865) |
| *High-side* industrial (descartado: 89 en stock) | ISP752RFUMA1 | Infineon | C454923 | Extended | 1,6245 (≥ 30) | 89 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/9e1390bc93a03b74461d08548900aa42.pdf?productCode=C454923) |
| *High-side* industrial (descartado: 1 en stock) | IPS160HFTR | ST | C1511766 | Extended | 3,0182 (≥ 30) | 1 | [PDF](https://datasheet.lcsc.com/datasheet/pdf/875e4620871df33cd76235e86fea9966.pdf?productCode=C1511766) |

---

## 3. Matrices

### 3.1 Cargas × opciones

| Carga | 1 Relé | 2 SSR PhotoMOS de 60 V | 3 Triac | 4a/4b MOSFET | 4c MOSFET bidireccional de 100 V | 5 *High-side* inteligente |
|---|---|---|---|---|---|---|
| **Válvula 24 V AC** (instalada) | ✔ V1: contacto libre con su transformador | ◐ V1 solo con ≤ 28 V AC medidos | ✔ V1 | ◐ V4: PWM desde 24 V DC, ajustado a la válvula | ✔ V1 | ◐ V4 |
| **Válvula 24 V DC** | ✔ V2 alimentada o con su fuente | ✔ | ✘ No se apaga en DC | ✔ | ✔ | ✔ Con diagnóstico de carga abierta |
| **Válvula *latch* 6–9 V DC** | ◐ Etapa común (puente H + fuente de 9 V ≥ 2 A) y el relé selecciona el canal | ◐ Igual | ✘ | ✘ No bloquea la polaridad inversa | ◐ Igual que el relé | ✘ Solo *high-side* |
| **Bomba pequeña DC** (≤ 2 A) | ✔ ≤ 3 A a 30 V DC | ◐ Arranque ≤ 5 A / 100 ms | ✘ (solo la bobina de AC de un relé de arranque, desde fuera) | ✔ Con diodo | ✔ ≤ 1,6 A | ✔ ≤ 4,5 A |
| **Carga resistiva / LED** | ◐ ≥ 10 mA | ✔ | ◐ Solo AC con I > I_H | ✔ | ✔ | ✔ |

La etapa *latch* común (puente H de 9 V con su fuente de impulso, más la barra LATCH y el COM_L) es una ampliación válida para las opciones 1, 2 y 4c. Se valoraría en una spec propia si el usuario se inclina por V3.

### 3.2 Qué haría falta para seguir usando las válvulas de 24 V AC (N4)

| Opción | V1: transformador propio (≤ 32 V AC) + contacto libre | V2/V3: cambiar las válvulas | V4: PWM desde 24 V DC |
|---|---|---|---|
| 1 Relé | Un transformador de riego (los de 0,65–1 A habituales) cableado a RET_n. Sin cambios en la placa: el puente JPn del canal abierto | Cambiar el solenoide o la válvula; puente JPn cerrado (V2) o etapa *latch* (V3) | No es posible |
| 2 SSR | Transformador **y medir ≤ 28 V AC en vacío**; si no, no hay margen | Como el relé | No |
| 3 Triac | Transformador | **No sirve** (habría que cambiar de tecnología) | No |
| 4a/4b | No es posible | Cambiar las válvulas (V2) | Firmware de impulso y mantenimiento con PWM, Schottky rápido y ajuste por modelo |
| 4c | Transformador | Como el relé | No |
| 5 | No es posible | Cambiar las válvulas (V2) | Como 4a/4b, con medida de corriente para ajustar el mantenimiento |

Cambiar a válvulas de 24 V DC solo exige cambiar el **solenoide**: Bermad, Hunter y Rain Bird venden solenoides separados de la válvula (S-390-T, 458200, TBOS). Comprobar la compatibilidad de rosca con el modelo instalado.

### 3.3 Salida alimentada (24 V DC) por opción (N3, N5; VAL-0004-01, nota 6)

| Opción | ¿Funciona? | Condición |
|---|---|---|
| 1 Relé | ✔ | Cargas DC; *high-side* |
| 2 SSR | ✔ | TVS SMAJ33CA o diodo de libre circulación |
| 3 Triac | **✘** | No se apaga en DC: la válvula quedaría abierta |
| 4a | ✔ | *Low-side*: cable a +24 V en reposo; un corto a tierra abre la válvula |
| 4b | ✔ | — |
| 4c | ✔ | — |
| 5 | ✔ | Con protección y diagnóstico |

---

## 4. Tamaño de placa

Hipótesis (estimación de ±5 mm; se fija en el layout):

- Ancho ≤ 100 mm.
- Borne de 5,08 mm con ≈ 8 mm de fondo.
- Núcleo central de ≈ 30 mm con el ESP32-S3-WROOM-1 en horizontal, la antena a un lateral y el USB-C en el lateral (FAB-07).
- Sin puente ni *bulk* de 100 Hz, la entrada (protección de polaridad, SMBJ33A, *buck*) es más pequeña que con AC.
- Sensor de T/HR en una esquina lateral (AMB-02).

| Opción | Disposición de la franja | Ancho de 3 canales | Alto de la franja | Alto estimado de la placa | Altura máx. del componente |
|---|---|---|---|---|---|
| 1a SRD-05 | Relé paralelo al borde | ≈ 62 mm | ≈ 28 mm | ≈ 86 mm | 15,8 mm |
| 1b G5NB / HF46F | Relé paralelo al borde | ≈ 66 mm | ≈ 21–25 mm | **≈ 75–80 mm** | 15,3 mm |
| 2 SSR | Un canal por cada 10,16 mm | ≈ 35 mm | ≈ 20–22 mm | ≈ 70–75 mm | Borne (14,1 mm) |
| 3 Triac | DPAK o SOT-223 + SOP-6 + RC | ≈ 40 mm | ≈ 22–25 mm | ≈ 75–80 mm | Borne |
| 4a/4b MOSFET | SOT-23 + SMA | ≈ 35 mm | ≈ 16–18 mm | ≈ 66–70 mm | Borne |
| 4c MOSFET bidireccional | 2 SOT-23 + SOP-4 + SOT-23 + TVS | ≈ 35 mm | ≈ 20–22 mm | ≈ 70–75 mm | Borne |
| 5 *High-side* | TDSO-14 + cobre | ≈ 35 mm | ≈ 18–20 mm | ≈ 70 mm | Borne |

En la opción 1b, la franja inferior (66 mm de relés, entrada, expansión, fusible y corte general) obliga a poner uno o dos relés en segunda fila: la placa queda cerca de **80 mm**.

---

## 5. Coste

**Hipótesis.**
- Precios de LCSC del 2026-11-04 en el tramo de 30 unidades (5 placas) y de 60 (10 placas).
- JLCPCB *Economic PCBA* (artículo actualizado el 2026-10-22): **3,07 $ por pieza Extended** y pedido, 0,0016 $ por junta SMT, y THT manual a 0,0164 $ por junta más 3,58 $ por pedido.
- THT soldados a mano por el usuario (FAB-06), salvo en la última columna.
- Incluye la SMAJ48CA y, en las opciones 2, 3 y 4c, el AO3400A del LED.
- No incluye el fusible rápido por canal (pieza por elegir, del orden de 0,1–0,2 $), el corte general, la etapa *latch*, el resto de la placa ni el envío.
- Resistencias 0603 *Basic* estimadas a 0,002 $.

| Opción | Pieza principal | Coste por canal: 5 / 10 placas (USD) | 6 canales: 5 / 10 placas (USD) | Extended SMT distintas | Total del pedido: 5 / 10 placas | **Por placa: 5 / 10** | Por placa con THT montado por JLCPCB: 5 / 10 |
|---|---|---|---|---|---|---|---|
| 1a | SRD-05VDC-SL-C | 0,591 / 0,548 | 3,55 / 3,29 | 1 | 21,53 / 37,37 | **4,31 / 3,74** | 5,71 / 4,78 |
| 1b | G5NB-1A-E-DC5V | 0,648 / 0,604 | 3,89 / 3,62 | 1 | 23,22 / 40,73 | **4,64 / 4,07** | 5,95 / 5,02 |
| 1b | HF46F/5-HS1 | 1,110 / 1,066 | 6,66 / 6,40 | 1 | 37,08 / 68,47 | **7,42 / 6,85** | 8,72 / 7,80 |
| 2 | AQV252GAX | 3,086 / 3,042 | 18,51 / 18,25 | 2 | 99,72 / 190,68 | **19,94 / 19,07** | 20,86 / 19,62 |
| 2 | GAQV252G3EH | 2,183 / 2,139 | 13,10 / 12,84 | 2 | 72,64 / 136,52 | **14,53 / 13,65** | 15,44 / 14,21 |
| 3 | BT136S + MOC3023SM | 0,921 / 0,776 | 5,53 / 4,66 | 4 | 41,35 / 61,74 | **8,27 / 6,17** | 9,18 / 6,73 |
| 4a | IRLML0060 + MMBT3904 | 0,394 / 0,327 | 2,36 / 1,96 | 1 | 15,65 / 24,21 | **3,13 / 2,42** | 4,04 / 2,98 |
| 4b | FDN5618P + MMBT3904 | 0,326 / 0,267 | 1,96 / 1,60 | 1 | 13,72 / 20,82 | **2,74 / 2,08** | 3,66 / 2,64 |
| 4c | 2× IRLML0100 + VOM1271T | 2,144 / 2,100 | 12,86 / 12,60 | 3 | 74,82 / 137,80 | **14,96 / 13,78** | 15,88 / 14,33 |
| 5 | BTT6050-1ERA | 1,253 / 1,227 | 7,52 / 7,36 | 1 | 41,96 / 79,26 | **8,39 / 7,93** | 9,30 / 8,48 |
| 5 | BTT6030-2ERA (½ por canal) | 1,271 / 1,244 | 7,62 / 7,47 | 1 | 42,06 / 79,46 | **8,41 / 7,95** | 9,32 / 8,50 |

**Corte general (§6), común a todas las opciones:**
- con un relé de ≥ 5 A a 30 V DC (SRD-05VDC-SL-C, 10 A a 28 V DC según LCSC, ≈ 0,40 $ con su driver);
- o con un BTT6030-2ERA (2,22 $), un canal por borde, que además mide la corriente de cada grupo.

---

## 6. Modo de fallo y mitigación

| Opción | Fallo dominante | Efecto | Corto en campo (salida alimentada, fuente de 5 A) | Detección en la placa |
|---|---|---|---|---|
| 1 Relé | Contacto soldado o MOSFET de bobina en corto | Válvula abierta | Aguanta; la fuente limita y la lógica cae si no hay fusible por canal | No |
| 2 SSR | Salida en corto (sobretensión, > 5 A) | Válvula abierta | Se destruye sin fusible rápido | No |
| 3 Triac | Triac en corto; disparo por dV/dt | Válvula abierta | (Solo V1) fusible rápido | No |
| 4a | MOSFET en corto; **corto del cable a tierra = válvula abierta** | Válvula abierta | Se destruye sin fusible rápido | No |
| 4b/4c | MOSFET en corto | Válvula abierta | Se destruye sin fusible rápido | No |
| 5 | Corto residual (sobretensión, ESD) | Válvula abierta | **Se protege** | **Sí** (IS: corriente con IN en bajo, carga abierta, corto) |

**Mitigación propuesta, común a todas las opciones:**

1. **Corte general del bus de 24 V de las salidas alimentadas.** Un relé de ≥ 5 A a 30 V DC o un *high-side* inteligente (BTT6030-2ERA, un canal por borde) en serie con el bus, controlado por un GPIO propio con *pull-down*. El firmware solo lo activa mientras algún canal riega. Para que la válvula se quede abierta tienen que fallar dos elementos.
2. **Válvula maestra en campo** (NC): un canal configurable como maestra en ESPHome. Cubre también V1 (contacto libre) y una rotura de tubería.
3. **Protección de cortocircuito por canal** en la salida alimentada (fusible rápido de ≈ 1,5 A F o PTC; innecesario con la opción 5), **fusible de 4 A T en el bus**, y **autonomía de la lógica** (diodo y condensador antes del *buck*) para que un corto en campo no reinicie el ESP32 mientras actúa la protección.
4. **Detección (S):** medida de la corriente del bus (shunt y ADC1, o el IS del BTT del corte general) para avisar de una salida atascada y limitar el total a 4 A.
5. **Firmware:**
   - apertura escalonada (V4: ≥ 0,5 s);
   - bloqueo de la salida alimentada en los canales de triac;
   - FW-04 y *watchdog*.

---

## 7. Recomendación (propuesta para D8 y D2; decide el usuario)

### 7.1 Propuesta: opción 1b, relé subminiatura

**Omron G5NB-1A-E-DC5V** (C48746), con **Hongfa HF46F/5-HS1** (C5274168) como segunda fuente. Driver AO3400A + 1N4148W (*Basic*) y SMAJ48CA en el contacto.

- **Es la opción barata que no ata la placa a un tipo de válvula** (DEC-0002 §6): por canal, contacto libre para las válvulas de 24 V AC con su transformador (V1) o salida alimentada de 24 V DC (V2). El usuario puede migrar de AC a DC canal a canal sin cambiar la placa. Con la etapa común, también *latch* (V3).
- Bloqueo sobrado en los dos modos (250 V AC; 3–5 A a 30 V DC). Aislamiento galvánico entre el transformador del usuario y la lógica.
- Aguanta un cortocircuito del cable sin destruirse.
- ≈ 4,1–4,6 $ por placa la etapa de 6 canales. Más de 45 años de vida a 6 maniobras al día.
- Sin LED de control, así que sin riesgo de H5.
- Precio de la elección:
  - THT a mano;
  - ≈ 80 mm de alto;
  - el clic;
  - 1,4 W de bobinas;
  - no admite PWM (V4).

**D2 propuesta: ambas**, seleccionables por canal:

- Borne de **2 polos por canal (OUT_n, RET_n) + COM (GND) por borde**: 7 polos por borde, 35,6 mm.
- **Puente de soldadura por canal**: cerrado, RET_n se une al bus +24V_SAL (fusible de 4 A T, corte general y fusible rápido del canal); abierto, contacto libre.
- Serigrafía: «alimentada: 24 V DC – no conectar válvulas de AC» y «libre: ≤ 32 V AC / 30 V DC».

### 7.2 Alternativa: opción 4c, «SSR discreto» de 100 V

2× IRLML0100 (C53658) + VOM1271T (C146286), con el LED según §1.6 y la SMAJ48CA.

- Cubre lo mismo que el relé (V1 y V2; V3 con la etapa común), en SMT, sin desgaste y ≈ 5 mm más baja.
- Costes: +9 a +10 $ por placa, 0,5 W por canal a 1 A y un fusible rápido por canal imprescindible.

**Si el usuario prefiere abandonar la AC** (V2 y, opcionalmente, V4): la **opción 5, BTT6050-1ERA** (C534868) o BTT6030-2ERA (C534865). Tiene protección de cortocircuito, medida de corriente y diagnóstico de carga abierta por canal, cable a 0 V en reposo, ≈ 8 $ por placa y todo SMT. Es la mejor técnicamente para DC, pero obliga a cambiar los solenoides instalados o a moverlos con PWM.

**Opciones no recomendadas como base:**
- Triac: solo V1 y no da salida alimentada en DC.
- SSR PhotoMOS de 60 V: sin margen para V1 con 32 V AC.
- 4a: un corto del cable a tierra abre la válvula.
- 4b: sin protección; la opción 5 la mejora por ≈ 6 $ más por placa.

### 7.3 Cambios que habría que hacer en los requisitos (propuestas; las decide el coordinador con el usuario)

Los requisitos nuevos van sin número: hoy REL llega a REL-09 (U6).

| Requisito | Con la opción 1b (relé) | Con la opción 4c | Con la opción 5 |
|---|---|---|---|
| **REL-02** | «Salida alimentada: 24 V DC (18–30 V). Contacto libre: ≤ 32 V AC / 30 V DC.» | Igual | «Solo salida alimentada de 24 V DC.» |
| **REL-03** | «Bobina excitada desde GPIO con MOSFET N (*Basic*) y diodo de libre circulación; TVS bidireccional con V_RWM ≥ 45,3 V (SMAJ48CA) en cada contacto. Sin optoacoplador.» | «LED del driver aislado alimentado desde 3,3 V con una R fija y un MOSFET N, con I_F,mín ≥ 2·I_FT en todo el rango de V_F y de 3,3 V ± 3 % (§1.6), nunca en serie con el LED indicador (H5, VAL-0004-01-08); MOSFET ≥ 100 V; TVS con V_C < V_DS.» | «*High-side* inteligente de 24 V con limitación de corriente y medida de corriente en ADC1.» |
| **REL-05** | Mantener 1 A continuo por canal. Añadir: «≤ 4 A en total en el bus de las salidas alimentadas (N2), con fusible de 4 A T, protección de cortocircuito por canal y autonomía de la lógica». Cambiar la prueba térmica de §6 a «1 h con las 6 salidas activas y 4 A en total». | Igual | Igual, sin fusible por canal |
| **REL-08** | Fijar la forma: «2 polos por canal (OUT/RET) + COM por borde; puente de soldadura por canal para la salida alimentada de 24 V DC; bus con fusible y corte general». | Igual | «1 polo por canal + COM (GND).» |
| **Nuevo (M), corte general** | «Corte general del bus de 24 V de las salidas, controlado por un GPIO propio con *pull-down*, activo solo mientras algún canal riega; contacto o interruptor de ≥ 5 A.» Y como S: «canal configurable como válvula maestra». | Igual | Igual |
| **Nuevo (S), medida del bus** | «Medida de la corriente del bus en ADC1 para detectar una salida atascada y limitar el total a 4 A.» | Igual | Incluida en IS |
| **FAB-07** | 7 polos por borde (3 × 2 + COM), más la entrada (2) y la expansión en el borde inferior; 5,08 mm. | Igual | 4 polos por borde |
| **FAB-08** | Alto ≈ **80 mm**. | ≈ 75 mm | ≈ 70 mm |
| **D6 (cobre)** | 1 oz con el bus a ≥ 2,5 mm o en polígono (§8). | Igual | Igual |

---

## 8. Restricciones de layout preliminares

Se cerrarán en la spec del bloque de salidas. Anchos según IPC-2221 para una capa externa de 1 oz con ΔT = 10 °C:

- 1 A → 0,30 mm;
- 2 A → 0,78 mm;
- 4 A → 2,03 mm;
- 5 A → 2,77 mm.

| Red | Corriente | Ancho mín. | Separación | Ubicación / keepout | Notas |
|---|---|---|---|---|---|
| `OUT_n`, `RET_n` (canal) | 1 A continuo; impulsos *latch* de 2 A | 1,0 mm | ≥ 1 mm a otras redes; ≥ 2 mm entre el circuito AC del usuario (V1) y la lógica | Entre el interruptor y el borne, lo más corta posible; franja de borde (REL-09) | Clase `Salidas`; OUT_n puede bajar a ≈ −35 V al abrir (§2.1) |
| `+24V_SAL` (bus tras el fusible de 4 A y el corte general) | 4 A (N2) | 2,5 mm o polígono | ≥ 1 mm | De la entrada (borde inferior) a los dos bornes; lejos de la antena (MCU-02) y del sensor de T/HR (AMB-02) | Clase `Salidas`; si se reparte en dos grupos, 2 A por rama (1,0 mm) |
| `COM` (GND de las salidas) | 4 A | 2,5 mm o polígono | — | Retorno al plano de GND junto a la entrada, no por debajo de la lógica | Clase `Salidas` |
| Entrada de +24 V (borne → protección → bus y *buck*) | ≈ 5 A | 3,0 mm o polígono | ≥ 0,5 mm | Borde inferior | Clase `Power` |
| Bobinas de relé (+5 V → bobina → drenaje) | 40 mA por canal, 280 mA en total | 0,25 mm (0,6 mm en el tronco de +5 V) | 0,2 mm | Diodo junto a la bobina | `Default` / `Power` |
| TVS del contacto | Impulsos de mJ | 0,6 mm | — | En los pads del interruptor o del borne | — |

---

## 9. Pendientes y validación en el prototipo

- **jr-conformidad:** confirmar los LCSC y los tipos (M7 como *Basic* sin confirmar). Faltan por elegir:
  - el relé o *high-side* del corte general;
  - el fusible de 4 A T del bus;
  - el fusible rápido por canal;
  - la SMAJ33CA (opción 2 en V2);
  - un Schottky de ≥ 60 V para PWM;
  - un MOSFET de 60 V especificado a 2,5 V para 4a.
- **Usuario:**
  - decidir entre V1 (mantener las válvulas de AC con su transformador), V2 (pasar a solenoides de 24 V DC), V3 (*latch*) o una mezcla;
  - si V1: modelo, VA y tensión en vacío del transformador;
  - marca y modelo de las válvulas instaladas.
- **Prototipo:**
  - relé: apertura de una válvula de 24 V DC a 30 V DC y recorte de la TVS;
  - 4c: temperatura con 4 A en total;
  - opción 5: diagnóstico de IS con válvula, carga abierta y corto;
  - V4 (si se usa): corriente de mantenimiento con PWM y temperatura de la bobina.
- **Bloque de alimentación (ALI):** autonomía de la lógica ante el límite de la fuente; recorte real de la SMBJ33A.
- **SPEC-0006:** el conector EXP-02 tiene que llevar su parte del bus de 24 V y el COM, o el módulo una entrada propia.

---

## 10. Fuentes

Datos del usuario y de validación:

- Datos del usuario del 2026-11-04, transmitidos por el coordinador en dos mensajes: el primero (transformador de 5 A, 32 V AC) quedó sustituido por el segundo (entrada única de 24 V DC 5 A, 18–30 V, SMBJ33A; 6 salidas a la vez y 4 A en total; válvulas de AC solo por V1 o cambio a DC/*latch*).
- `gestion/informes/VAL-0004-01.md`: hallazgos 02, 05, 08 y 15, y nota 6.

Válvulas y programadores:

- Rain Bird, *Irrigation Valve Solenoids – Technical Specifications* (D42606, 07/26), p. 1: <https://www.rainbird.com/sites/default/files/media/documents/2026-07/d42606_-_irrigation_valve_solenoids.pdf>
- Hunter, ficha de la PGV 1½" y 2": <https://cdn.shopify.com/s/files/1/1845/4805/files/CA-Cutsheet-PGV-EM.pdf>
- Hunter, especificación escrita de la PGV: <https://hunterirrigation.com/sites/default/files/hi-045-written_specs-112_and_2_pgv_valve.docx>
- Solenoide Hunter 60-6800 (19 V AC mínimos): <https://cheapsprinklers.com/products/hunter-60-6800-replacement-solenoid-for-hunter-valves>
- Solenoide *latch* Hunter 458200 (6–9 V DC, 4,8 Ω): <https://cheapsprinklers.com/products/hunter-458200-dc-latching-solenoid> y <https://hunterindustries.com/irrigation-product/accessories/solenoids>
- Rain Bird 100DV, ficha de tienda: <https://store.rainbird.com/valves/100dv-1-in-dv-series-inline-plastic-residential-irrigation-valve-npt-threads.html>
- Bermad, solenoide S-390-T-2W, «Electrical Data» (24 V AC-R, 24 V AC-D y 24 V DC: 4,2 W, 0,18 A, 156 Ω): <https://catalog.bermad.com/BERMAD-Assets/Irrigation/Solenoids/IR-SOLENOID-S-390T-2W/S-390-T-2W-Product-Page-Metric-English.pdf>
- Bermad, solenoide *latch* S-392-T-2W (9 V DC): <https://www.bermad.com/app/uploads/IR_Accessories-Solenoid-S-392T-2W_Product-Page_English_5-2018.pdf>
- Bobina RPE de 24 V DC (0,24 A): <https://dvs-beregnung.de/magnetic-coil-rpe-24-vdc-e9820000-24dc-irrigation.md> (dato del buscador; devolvía 404 el 2026-11-04)
- Hunter X-Core, folleto: <https://hunterirrigation.com/sites/default/files/BR_XCORE_EM.pdf>
- OpenSprinkler, foros (triac directo; versión DC con impulso y mantenimiento): <https://opensprinkler.com/forums/topic/3-0-ac-board-always-on/>, <https://opensprinkler.com/?p=72067> y <https://opensprinkler.com/forums/topic/powering-opensprinkler-dc/>
- Hackaday, «Converting AC irrigation valves to DC operation» (2026-02-09): <https://hackaday.com/2026/02/09/converting-ac-irrigation-valves-to-dc-operation>

Datasheets:

- Espressif, ESP32-S3 Series Datasheet v2.2, tabla 5-4: <https://documentation.espressif.com/esp32-s3_datasheet_en.pdf>
- Infineon, BTT6050-1ERA, rev. 1.00 (2019-03-09), tablas 1 y 4.1: enlace en §2.5.
- Panasonic, AQV252G (ASCTB144E): enlace en §2.2.
- onsemi, MOC302xM: enlace en §2.3.
- onsemi, MOC306xM (V_INH): <https://www.onsemi.com/pdf/datasheet/moc3163m-d.pdf>
- Vishay, VOM1271: enlace en §2.4.
- JSCJ, BT136S: enlace en §2.3.
- Infineon, ISP752R, rev. 1.2: enlace en §2.5.
- Omron G5NB: <https://www.digikey.hk/htmldatasheets/production/58275/0/0/1/g5nb-1a-e-dc18.html>
- Hongfa HF46F: <https://hubtronics.in/docs/HF46F.pdf>
- Resto: enlaces en las tablas de §2.

Tarifas:

- JLCPCB, «PCB Assembly Price» (actualizado el 2026-10-22): <https://jlcpcb.com/help/article/pcb-assembly-price>
- LCSC (precio y stock): `https://www.lcsc.com/product-detail/<LCSC>.html`, consultado el 2026-11-04.
- JLCPCB (tipo Basic/Extended): `https://jlcpcb.com/partdetail/<LCSC>`, consultado el 2026-11-04.
