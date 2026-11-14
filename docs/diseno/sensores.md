# Bloque de sensores: temperatura y humedad del aire de la caseta (SPEC-0029)

**Autor:** ing-diseno · **Fecha:** 2026-11-14.
**Requisitos:** AMB-01, AMB-02, KIC-02; además FAB-02, FAB-03, FAB-07, FW-03 y MCU-05.
**Stock:** `hardware/componentes/stock-sensores.csv` (JLCPCB, 2026-11-14, paso 1 de SPEC-0029).

> Datasheets (páginas del PDF):
> - **SHT:** Sensirion SHT4x, versión 7.3, junio de 2026 (`hardware/componentes/datasheets/SHT4x.pdf`).
> - **LMR:** TI LMR36520 (`datasheets/LMR36520.pdf`); **TPS:** TI TPS2116 (`datasheets/TPS2116.pdf`).
> - `mcu.md` §1, §8.2, §9.2, §11 y §12; `alimentacion.md` §3.9 y §10; `salidas.md` §6.

## 0. Resumen

```
+3V3 ─┬──────────── U13 VDD (3)          GPIO41 ─ R24 4,7 k ─ +3V3 (hoja MCU)
      └─ C47 100 nF ─ GND                  │
GND ─────────────── U13 VSS (4)           I2C_SDA ── U13 SDA (1)
                                          GPIO42 ─ R25 4,7 k ─ +3V3 (hoja MCU)
                                            │
                                          I2C_SCL ── U13 SCL (2)
```

| Función | Pieza principal | Alternativa | Requisito |
|---|---|---|---|
| Sensor T/HR | U13 Sensirion **SHT40-AD1B-R3**, C2848306 (Extended, 13 207) · I²C **0x44** | SHT40-AD1B-R2, C2909890 (mismo chip, bobina de 2 500); SHT41-AD1B-R2, C7461861 (más exacto, §2) | AMB-01 |
| Desacoplo | C47 100 nF 50 V X7R 0603, Yageo CC0603KRX7R9BB104, C14663 (Basic; línea de C25) | Samsung CL10B104KB8NNNC (C1591, Extended) | AMB-01 |
| *Pull-ups* | R24 y R25 (4,7 kΩ) de la hoja MCU: **no se duplican** | — | AMB-01 |

Resultados clave:

- **Variante:** SHT40 (la del paso 1). La exactitud que pide §6 de `docs/02` (± 0,5 °C, ± 3 % HR tras calibrar) la decide la corrección del firmware, no la variante (§2).
- **Dirección:** 0x44, sola en el bus de la placa (GPIO41/42); la expansión va en otro bus (GPIO47/48): sin choque (§3).
- **Consumo:** 0,5 mA máx. midiendo y 2,2 µA de media a 1 medida/s; cuadra con los 0,5 mA de `mcu.md` §8.2. Calentador **sin usar** (§4).
- **Autocalentamiento:** 2 mK a 1 medida/s; 0,49 K si se midiera sin parar: el firmware mide cada ≥ 10 s (§4.3).
- **Aislamiento (AMB-02):** isla en el borde lateral, rodeada de ranuras con un solo puente y sin planos. Estimación: la isla sigue al **≈ 30 %** del calentamiento de la placa (frente al ≈ 100 % sin ranuras): **≈ 1,3 K en reposo y ≈ 3 K con las 6 salidas a 0,25 A**. La diferencia (≈ 1,7 K) supera ± 0,5 °C: lo previsible es que haga falta la corrección **según las salidas activas** de AMB-02/FW-03, y **hay que recalcular la HR** con la temperatura corregida (§5, §8).
- **Huella sin pad central** (oficial `…_NoCentralPad`); la instancia de la PCB enlaza el modelo 3D de respaldo (`sincronizar.py`, §7).
- **Referencias:** U13 y **C47**. El paso 1 propuso C46, pero C46 ya existe en la hoja de salidas (4,7 µF a granel): se corrige `campos-sensores.csv`.

Restricciones de layout (filas listas para `docs/diseno/restricciones.csv`; justificación en §6):

| Red | Corriente | Ancho mín. | Separación | Ubicación / keepout | Notas |
|---|---|---|---|---|---|
| Isla de U13 y C47 (ranuras) | — | — | Ranura ≥ 1,0 mm de ancho (fresado no metalizado); cobre a borde de ranura ≥ 0,5 mm (FAB-02) | **Borde lateral** (FAB-07), de preferencia el opuesto a la antena. Isla de ≈ 10 × 12 mm (mín. 6 × 8) en `Edge.Cuts`, rodeada de ranuras con **un solo puente** de 3 mm de ancho y ≥ 5 mm de largo | AMB-02. Un 2.º puente sin cobre solo si hace falta rigidez (sube la conducción < 0,3 mW/K) |
| Isla y puente (sin planos) | — | — | — | Área de regla en **F.Cu y B.Cu** sobre la isla y el puente: sin relleno de cobre ni vías; pistas permitidas. Se suma el *keepout* F.Cu de la huella bajo el sensor | AMB-02; SHT §5.3, p. 16 («no copper under the sensor other than at the pin pads») |
| I2C_SDA, I2C_SCL (tramo hasta U13) | ≤ 0,7 mA | 0,25 mm (`Default`) | 0,2 mm | Por el puente; **≥ 20 mm de pista** entre el borde del plano y los pads de U13; sin vías en la isla | No ensanchar: el cobre es el 70 % de la fuga térmica (§5.2). Refina la fila I2C de `mcu.md` §12 |
| +3V3, GND (tramo hasta U13) | ≤ 0,5 mA | 0,25 mm (`Default`) | 0,2 mm | Una pista de cada por el puente, **sin plano**; C47 a ≤ 2 mm entre los pads 3 (VDD) y 4 (VSS), en la isla | Mismo criterio de longitud que el I²C |
| Distancias de la isla | — | — | — | Borde de la isla a **≥ 20 mm** de L1/U2 (buck), U4 (LDO), U1/Q1/F1 (limitador y entrada) y U7–U12 (*high-side*); a **≥ 15 mm** de U5 y de su zona de antena (`mcu.md` §12) | Objetivo del autor, no requisito: el *floorplan* puede justificar menos (§6.3) |
| U13 (orientación) | — | — | — | Cara superior, apertura hacia arriba y frente a las rejillas de la caja; sin serigrafía, barniz, etiquetas ni adhesivos sobre la isla | AMB-02; SHT §2.3, p. 7 (contaminación). La rejilla la fija la caja (decisión D5) |

## 1. Datos de partida

| Dato | Valor | Origen |
|---|---|---|
| Raíl +3V3 | 3,211–3,389 V (TLV1117LV ± 2,7 %) | `mcu.md` §1; `alimentacion.md` §3.9 |
| Bus I²C de la placa | GPIO41 (SDA, pin 34 de U5) y GPIO42 (SCL, pin 35); R24/R25 = 4,7 kΩ a +3V3; 400 kHz | `mcu.md` §9.2, §11 |
| Bus de expansión | GPIO47/48, otro bus (SPEC-0031) | `mcu.md` §9.2 |
| Placa | 100 × 70 mm (preliminar), 2 capas, 1,6 mm, 1 oz; planos de GND en las dos caras (FAB-04) | FAB-01, FAB-04, FAB-08 |
| Ambiente de diseño | +50 °C en la caseta + ≥ 10 °C dentro de la caja | `docs/02` §5; checklist de esquema |
| Verificación | ± 0,5 °C y ± 3 % HR frente a una referencia en la caseta, en reposo y tras 1 h con las 6 salidas, con la corrección de AMB-02 | `docs/02` §6 |

## 2. Variante (AMB-01)

| Variante | T máx. (0–65 °C) | HR máx. (10–90 %, 25 °C) | Precio 1–9 (USD) | Stock |
|---|---|---|---|---|
| SHT40-AD1B | ± 0,4 °C (Fig. 10, p. 7) | ± 3,5 % HR (Fig. 2, p. 5) | 1,8538 | 13 207 |
| SHT41-AD1B | ± 0,4 °C (Fig. 11, p. 7) | ± 2,5 % HR (Fig. 3, p. 5) | 3,2592 | 11 244 |
| SHT45-AD1B | ± 0,3 °C (Fig. 13, p. 7) | ± 2,0 % HR (Fig. 5, p. 5) | 5,7167 | 6 530 |

- Ninguna variante cumple § 6 sin calibrar: la isla se calienta 1–3 K (§5) y el error de temperatura arrastra la HR: dHR/dT = HR · 17,62 · 243,12 / (243,12 + T)² = **2,98 % HR por K** a 25 °C y 50 % HR (Magnus, §8).
- Con la corrección calibrada contra la referencia (T y, después, HR por Magnus más un *offset* de HR medido en la misma calibración), el error estático del sensor se absorbe: la variante no decide el cumplimiento.
- Sin *offset* de HR, ni el SHT41 garantiza ± 3 %: 2,5 % HR + 0,5 K × 2,98 = 4,0 % HR.
- **Se fija SHT40-AD1B-R3** (C2848306), la del paso 1. Si el prototipo no alcanza ± 3 % HR, la mejora directa es el SHT41-AD1B-R2 (C7461861): misma huella, misma dirección y +1,41 $ por placa.

## 3. Dirección I²C

- La letra 7 del código fija la dirección: A = 0x44, B = 0x45, C = 0x46 (Tabla 11, p. 21). SHT40-**A**D1B → **0x44**.
- En el bus de la placa solo está U13. Una sonda externa (AMB-03) va por el bus de expansión (GPIO47/48), así que puede ser otro SHT4x o un SHT3x en 0x44 sin choque.
- El *general call reset* (0x00, comando 0x06, p. 13) solo reinicia el bus de la placa.

## 4. Eléctrico

### 4.1 Alimentación y consumo

| Comprobación | Cálculo | Resultado |
|---|---|---|
| Rango de VDD | 3,211–3,389 V dentro de 1,08–3,6 V (p. 9) | ✔ margen 0,21 V |
| Tensión en SDA/SCL | *Pull-ups* al mismo +3V3; máx. VDD + 0,3 V (Tabla 6, p. 10) | ✔ |
| Pendiente de VDD ≤ 20 V/ms (p. 9) | Con 24 V: el buck arranca en t_SS ≥ 3 ms (LMR p. 7) → ≤ 5 V/3 ms = 1,7 V/ms. Con USB: t_SS del TPS2116 1,7 ms típ. a 5 V (TPS p. 7) → ≈ 2,9 V/ms. El LDO sigue a su entrada | ✔ (≥ 6×) |
| Corriente midiendo | 320 µA típ. / **500 µA máx.** (p. 9) | = 0,5 mA de `mcu.md` §8.2 ✔ |
| Corriente media | 2,2 µA a 1 medida/s, alta repetibilidad (p. 9); reposo 0,08 µA típ., 1,0 µA máx. a 25 °C | Despreciable |
| Calentador | 60 mA típ., **100 mA máx.** a «200 mW» (p. 9), ≤ 1 s, ciclo ≤ 10 % (p. 13) | **Sin usar** (§4.3). Si se usara: 0,45 + 0,10 = 0,55 A ≤ 1 A del TLV1117LV. `mcu.md` §8.2 da 61 mA (típico): el máximo es 100 mA |

### 4.2 Bus I²C (pull-ups de la hoja MCU)

| Comprobación | Cálculo | Resultado |
|---|---|---|
| R_p mínima | 4,7 kΩ ≥ 390 Ω (VDD ≥ 1,62 V, p. 9) | ✔ |
| V_OL del sensor | ≤ 0,4 V con R_p > 390 Ω (p. 9) ≤ V_IL del ESP32 (0,25 · 3,211 = 0,80 V, S tabla 5-4) | ✔ margen 0,4 V |
| Corriente a nivel bajo | 3,389 V / 4,7 kΩ = 0,72 mA por línea (`mcu.md` §8.2 cuenta 0,7 mA) | ✔ |
| Niveles de entrada del sensor | V_IL ≤ 0,3 · VDD = 0,96 V; V_IH ≥ 0,7 · VDD = 2,37 V (p. 9) | ✔ (salidas en drenador abierto) |
| C_bus máxima a 400 kHz | C_b < t_r / (0,8473 · R_p) = 300 ns / (0,8473 · 4,7 kΩ) = **75 pF** (p. 9) | — |
| C_bus estimada | Pista de ≤ 100 mm, 0,25 mm sobre 1,5 mm de FR-4: ≈ 0,45 pF/cm → 4,5 pF; + ≤ 10 pF por pin en U5 y U13 (supuesto) → **≤ 25 pF** | ✔ margen 3×; dentro de los 50 pF de `mcu.md` §11 |
| Sin *clock stretching* (p. 11) | El controlador del ESP32 no lo necesita | ✔ |

### 4.3 Desacoplo y autocalentamiento

- **C47:** 100 nF entre VDD y VSS, como el circuito típico (Fig. 1, p. 3). Peor caso: 100 nF × 0,90 (± 10 %) × 0,85 (X7R, ± 15 %) × 0,95 (polarización de 3,3 V en una pieza de 50 V; supuesto) = **73 nF**. Basta para los escalones de 0,5 mA del sensor; el raíl tiene ≈ 25 µF en U5 (`mcu.md` §8.1).
- **Autocalentamiento:** ΔT = P · R_θJA, con R_θJA = 297 K/W (calentador apagado, pad central sin soldar; Tabla 10, p. 17).
  - 1 medida/s: 3,3 V × 2,2 µA = 7,3 µW → **2 mK**.
  - Midiendo sin parar: 3,3 V × 0,5 mA = 1,65 mW → **0,49 K**. Por eso el firmware mide cada ≥ 10 s (ESPHome: 60 s por defecto).
  - Calentador de 200 mW: 0,2 × 357 K/W = 71 K en régimen; aunque va por pulsos, falsea la medida durante minutos: **apagado** (`heater_max_duty: 0.0`, §8).

## 5. Aislamiento térmico (AMB-02)

### 5.1 Fuentes de calor de la placa

| Estado | Piezas | Potencia | Fuente |
|---|---|---|---|
| Reposo | U5 Wi-Fi conectado (≈ 100 mA × 3,3 V, supuesto) 0,33 W; U4 (5,1 − 3,3) × 0,1 A = 0,18 W; U2 ≈ 0,12 W (0,5 W de salida con η ≈ 80 % a carga baja, supuesto) | **≈ 0,63 W** | `alimentacion.md` §10 |
| 6 salidas a 0,25 A (1,5 A) | Reposo + 6 × (24 V × 4,7 mA + 0,25² × 0,06 Ω) = 0,69 W en los BTT + U1 ≈ 0,10 W + Q1 1,5² × 0,026 = 0,06 W | **≈ 1,5 W** | `salidas.md` §6; `alimentacion.md` §10 |
| Ensayo de §6 (1 + 1 + 4 × 0,375 A, 3,5 A) | Reposo + BTT 1,8 W + U1 0,55 W + Q1 0,32 W + F1 0,09 W | ≈ 3,4 W (cota alta) | `salidas.md` §6 |

Calentamiento medio de la placa sobre el aire de la caja: ΔT_placa = P / (h · A), con A = 2 × 100 × 70 mm² = 0,014 m² y h = 10 W/m²K (convección natural y radiación; supuesto, rango 7–15) → 7,1 K/W:

- reposo: **≈ 4,5 K**; 6 salidas a 0,25 A: **≈ 10,5 K**; ensayo de §6: ≈ 24 K.
- Con planos en las dos caras, el cobre reparte el calor: k·t = 0,3 × 1,6 mm + 2 × 385 × 35 µm = 0,027 W/K y la longitud de reparto es √(k·t / 2h) = √(0,027 / 20) ≈ **37 mm**. En 100 × 70 mm la placa es casi isoterma: **la distancia sola no aísla; lo hacen las ranuras**.

### 5.2 Isla y puente

Fracción del calentamiento de la placa que llega a la isla: f = G_puente / (G_puente + G_isla).

- **Pistas por el puente** (4: SDA, SCL, +3V3, GND; 0,25 mm × 35 µm, L = 20 mm): G = 4 × 385 × 0,25 mm × 35 µm / 20 mm = **0,67 mW/K**.
- **FR-4 del puente** (3 × 1,6 mm, 5 mm de largo): G = 0,3 × 4,8 mm² / 5 mm = **0,29 mW/K**.
- **Isla al aire** (10 × 12 mm, dos caras, h = 10): G = 10 × 2,4 cm² = **2,4 mW/K**.
- f = 0,96 / (0,96 + 2,4) = **0,29**.
  - Con pistas de 5 mm (plano hasta el puente): G_pistas = 2,7 mW/K → f = 0,56.
  - Sin ranuras, el sensor sigue a la placa: f ≈ 1.
  - Isla de 6 × 8 mm: G_isla = 0,96 mW/K → f = 0,50. Por eso se pide ≈ 10 × 12 mm.

Calentamiento previsto de la isla (± 50 %, por h y por el reparto real): **≈ 1,3 K en reposo** y **≈ 3,0 K con 6 salidas a 0,25 A** (≈ 7 K en el ensayo de §6). Error de HR sin recalcular: a 25 °C y 50 % HR, 3 K → 41,9 % HR (§8).

### 5.3 Conclusiones para el diseño

- Las cuatro pistas son el 70 % de la fuga: anchura `Default` (0,25 mm), ≥ 20 mm de largo desde el borde del plano y ningún plano en la isla ni en el puente.
- Un solo puente, de 3 mm (cuatro pistas de 0,25 mm con 0,2 mm entre ellas = 1,6 mm, más 0,5 mm a cada borde de ranura por FAB-02 = 2,6 mm).
- Ranura ≥ 1,0 mm: el aire de la ranura conduce ≈ 0,026 W/mK, 10 veces menos que el FR-4. Más ancha apenas mejora y quita placa.
- La diferencia reposo/carga prevista (≈ 1,7 K) supera ± 0,5 °C: la corrección fija probablemente no basta. AMB-02 ya lo admite (según las salidas activas o la temperatura interna del ESP32). Se confirma en el prototipo (§9).

## 6. Restricciones de layout: justificación

### 6.1 Borde y orientación (FAB-07)

FAB-07 deja los laterales para la antena (MCU-02), el USB-C y el sensor. La antena va en una esquina de un lateral (`mcu.md` §3); el sensor, de preferencia en el lateral opuesto, para quedar lejos de U5 y de su zona libre. La isla mira a la rejilla de la caja (AMB-02) y el sensor va en la cara superior (FAB-06 y `layout.smd_cara`), con la apertura hacia arriba.

### 6.2 Sin cobre debajo

- La huella oficial ya trae un *keepout* en F.Cu bajo el cuerpo (pistas, vías y relleno prohibidos; pads permitidos). Coincide con §5.3 del datasheet (p. 16).
- AMB-02 pide más: **ningún plano en la isla en ninguna capa**. Se resuelve con un área de regla en F.Cu y B.Cu sobre la isla y el puente: relleno y vías prohibidos, pistas permitidas.

### 6.3 Distancias

- Con la isla, la distancia pesa menos que en una placa sin ranuras (§5.1), pero la zona de la placa junto al puente es la que fija la temperatura de partida.
- **Objetivo: ≥ 20 mm** del borde de la isla a buck, LDO, limitador y *high-side* (las fuentes de §5.1), y **≥ 15 mm** a U5 y a su antena (`mcu.md` §12).
- Con un lateral de 70 mm y los BTT a ≤ 15 mm de sus bornes en los bordes superior e inferior (`salidas.md` §11), la mitad del lateral queda a ≈ 20 mm de cada fila de BTT.
- El *floorplan* puede justificar menos con el cálculo de §5.

### 6.4 Lo que no cambia

- I2C_SDA/SCL y +3V3/GND siguen en `Default` (FAB-03). No hace falta ninguna clase ni regla de anchura nueva; las reglas nuevas son el área de la isla (KIC-04) y las ranuras en `Edge.Cuts`.
- Las ranuras y la isla se dibujan en la fase 4. Este bloque no coloca ni ruta nada.

## 7. Símbolo, huella y modelo 3D

| Elemento | Pieza | Comprobación |
|---|---|---|
| Símbolo | `Sensor_Humidity:SHT4x` (oficial) | 1 SDA (bidireccional), 2 SCL (entrada), 3 VDD, 4 VSS = Tabla de §5.4, p. 17 ✔ |
| Huella | `Sensor_Humidity:Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad` (oficial) | `huella.py`: 4 pads SMD de 0,5 × 0,3 mm, columnas a x = ± 0,7, filas a y = ± 0,4 (paso 0,8; separación de columnas 1,4) = Fig. 17, p. 16 ✔. Pads 1 (−0,7, −0,4), 2 (−0,7, 0,4), 3 (0,7, 0,4) y 4 (0,7, −0,4), vista superior = Fig. 18, p. 17 ✔. **Sin pad central** ✔. Patio 2,4 × 2,0 mm (margen 0,25). Sin vías |
| Modelo 3D | El oficial no existe en KiCad 10.0.6 (ficha `SHT4x.md`) | La instancia de U13 en la PCB enlaza `${KIPRJMOD}/../libraries/3d/Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad.step` (offset 0, giro 0, escala 1) |

- **Herramientas (SPEC-0029):** `sincronizar.py` sustituye, al cargar una huella, un modelo de la librería que no existe por el de `../libraries/3d` con el mismo nombre. `comprobar.py librerias.3d` acepta ese caso como respaldo y lo nombra en su línea. La función común es `_comun.modelo_de_respaldo`.
- Ninguna librería de la v1: símbolo y huella son oficiales de KiCad 10.

## 8. Notas para el firmware (FW-03)

- `i2c` `bus_placa` (SDA 41, SCL 42, 400 kHz; `mcu.md` Anexo B) y `sensor: sht4x` con `address: 0x44`, `precision: High`, `heater_max_duty: 0.0` y `update_interval` ≥ 10 s (60 s recomendado; §4.3).
- **Corrección de AMB-02**, en este orden:
  1. T_aire = T_sensor − ΔT, con ΔT fijo o ΔT(n) según el número n de salidas activas (o según la temperatura interna del ESP32), calibrado contra la referencia en reposo y tras 1 h con las 6 salidas.
  2. HR_aire = HR_sensor · e_s(T_sensor) / e_s(T_aire), con e_s(T) = 6,112 · exp(17,62 · T / (243,12 + T)) hPa (Magnus, constantes de Sonntag 1990 sobre agua, −45…60 °C). Conserva la humedad absoluta.
  3. *Offset* de HR medido en la misma calibración, si hace falta para ± 3 %.
- Tras cambiar el número de salidas, la isla tarda en asentarse: τ ≈ C_isla / G ≈ (1,6 mm × 1,2 cm² × 1,9 J/cm³K ≈ 0,37 J/K) / 3,4 mW/K ≈ **110 s**. El firmware aplica ΔT(n) con ese filtro de primer orden o deja de publicar ~5 τ (≈ 10 min); el valor se ajusta en el prototipo.

## 9. Riesgos y puntos abiertos

1. **Estimación térmica (§5):** h, el reparto real y la potencia del módulo son supuestos (± 50 %). Se mide en el prototipo con la prueba de `docs/02` §6. Si el calentamiento de la isla con carga pasa de ≈ 5 K, se alargan las pistas del puente o se agranda la isla.
2. **Ranura mínima:** ≥ 1,0 mm de fresado no metalizado es lo habitual en JLCPCB estándar. Se confirma con las reglas de fabricación de la fase 5.
3. **Isla en voladizo:** una isla de 10 × 12 mm sobre un puente de 3 × 1,6 mm de FR-4 aguanta el montaje y el uso normal, pero no golpes. Si la caja o el montaje lo piden, un 2.º puente sin cobre (+0,29 mW/K, f = 0,34).
4. **Rejilla de la caja:** la posición de la isla depende de la caja (decisión D5).

## 10. Lista de piezas

| Ref. | Valor / función | Encapsulado | MPN principal | LCSC · tipo · stock (2026-11-14) | Alternativa (LCSC) | Símbolo / huella |
|---|---|---|---|---|---|---|
| U13 | Sensor T/HR, I²C 0x44 | DFN-4 1,5 × 1,5 | Sensirion SHT40-AD1B-R3 | C2848306 · Extended · 13 207 | SHT40-AD1B-R2 (C2909890 · 14 052); SHT41-AD1B-R2 (C7461861 · 11 244) | `Sensor_Humidity:SHT4x` / `Sensor_Humidity:Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad` |
| C47 | 100 nF 50 V X7R, desacoplo de VDD | 0603 | Yageo CC0603KRX7R9BB104 | C14663 · Basic · 34 639 344 | Samsung CL10B104KB8NNNC (C1591 · Extended) | `Device:C` / `Capacitor_SMD:C_0603_1608Metric` |

- Campos: `hardware/componentes/campos-sensores.csv` (`campos.py revisar`: 0 diferencias).
- Coste: 1,8538 + 0,0104 = **1,86 $ por placa** (tramo 1–9) y una línea Extended más en el montaje.

## 11. Trazabilidad

| Requisito | Pieza o cálculo | Sección |
|---|---|---|
| AMB-01 | U13 SHT40-AD1B en la placa, I²C 0x44 en GPIO41/42, C47; *pull-ups* R24/R25 de la hoja MCU | §2–§4, §10 |
| AMB-02 | Isla en el borde lateral con ranuras, un puente y sin planos; distancias; corrección en reposo y con salidas | §5, §6, §8 |
| KIC-02 | Hoja `sensores.kicad_sch` («Sensores») en la raíz: cinco hojas | Anexo B |
| FAB-07 | Sensor en un lateral | §6.1 |
| FW-03 | Corrección de T y de HR, calentador apagado, intervalo de medida | §8 |
| MCU-05 | Sin cambios de pines: GPIO41/42 (`mcu.md` §9.2) | §1 |

## Anexo A. Datos para las fichas

- `SHT4x.md`: la variante queda fijada (SHT40-AD1B-R3) y la instancia enlaza el modelo de respaldo (§7). La ficha no se ha tocado en este paso.
- C14663 ya tiene la línea de C25 (`mcu.md` §11) y de C39–C44 (`campos-salidas.csv`).

## Anexo B. Etiquetas jerárquicas de la hoja de sensores

| Etiqueta | Forma (vista desde la hoja de sensores) | Hoja de origen o destino |
|---|---|---|
| I2C_SDA | Bidireccional | MCU (GPIO41, pin 34 de U5; R24) |
| I2C_SCL | Entrada (SCL del sensor es solo entrada, p. 17) | MCU (GPIO42, pin 35 de U5; R25) |
| +3V3, GND | Símbolos de alimentación (globales) | — |

- **En la hoja:** etiqueta jerárquica en el extremo de los pines 1 y 2 de U13; +3V3 en U13-3 y C47-1; GND en U13-4 y C47-2. No hay redes internas.
- **En la raíz:** hoja «Sensores» (página 6) con los pines `I2C_SDA` (bidireccional) e `I2C_SCL` (entrada) en su borde derecho, unidos a los de la hoja MCU con etiquetas locales del mismo nombre. Se quitaron las dos no conexiones provisionales de esos pines de MCU. Las redes pasan de `/MCU/I2C_SDA` y `/MCU/I2C_SCL` a `/I2C_SDA` y `/I2C_SCL` (la PCB se ha resincronizado).
- **Netlist:** `/I2C_SDA` = {U5-34, R24-2, U13-1}; `/I2C_SCL` = {U5-35, R25-2, U13-2}; U13-3 y C47-1 en +3V3; U13-4 y C47-2 en GND.
