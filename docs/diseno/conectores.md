# Bloque de conectores: expansión EXP-02, pulsadores EXP-03 y taladros (SPEC-0031)

> **Estado (paso 1, 2026-11-15):** solo está la comparación de la lectura de los 6 pulsadores (§1), para que el usuario elija (DEC-0013). El resumen del bloque, EXP-02 (desde `viabilidad-expansion.md` §10), los bordes con los taladros M3, las restricciones de layout, la trazabilidad y el anexo de etiquetas llegan en el paso 4. Las referencias de las piezas de §1 son provisionales (Ra, Rp…); las definitivas las fija el paso 3.

Fuentes:

- **S:** ESP32-S3 Series Datasheet v2.2. Tabla 5-6 (p. 66): error total del ADC calibrado de ± 10 mV con ATTEN2 (6 dB), en 0–1600 mV; ± 50 mV con ATTEN3 (12 dB), en 0–2900 mV.
- **PCA:** TI PCA9554, SCPS128D (mar. 2021):
  - p. 1: INT de drenador abierto, entradas al encender y POR;
  - p. 7: I_CC;
  - p. 15: cada E/S configurada como entrada lleva un *pull-up* débil de 100 kΩ típ. a V_CC;
  - p. 18, tabla 8-2: direcciones 0x20–0x27 con A2–A0.
- **TCA:** TI TCA9554, SCPS233E (feb. 2017), p. 1 y tabla de pines: E/S *push-pull* sin *pull-up*.
- **ESPHome 2026.10.2:**
  - `pca9554` admite PCA9554, PCA9554A, PCA9536 y PCA9535, probados, y TCA9554 y TCA9535, que «deberían funcionar»;
  - `pcf8574`, `mcp23008` y `tca9555`;
  - todos tienen `interrupt_pin`, que pasa de leer por sondeo a leer cuando cambia una entrada.
- **TS:** `hardware/componentes/TS-1187A-B-A-B.md`: 50 mA y 12 V; contacto ≤ 100 mΩ.
- **Precios:** `jlc.py`, 2026-11-15, tramo de la cantidad real. *Economic PCBA*: 3,07 $ por pieza Extended distinta y pedido; 0,0016 $ por unión SMT (`viabilidad-expansion.md` §6). Ninguna pieza Extended de este apartado es «preferida».

## 1. Lectura de los 6 pulsadores (EXP-03)

### 1.1 Datos de partida

- 6 pulsadores TS-1187A-B-A-B (C318884, Basic, 852 638 en stock), en fila en el centro de la placa, uno por salida. Los lee el firmware con antirrebote; el accionamiento manual pasa por el *switch* del canal, con su tiempo máximo (REL-08, FW-04). Son iguales en todas las opciones.
- Pines libres (DEC-0011, `mcu.md` §9.1-9.2):

| GPIO | Uso posible | Restricción |
|---|---|---|
| 10 | Cualquiera; es el **último canal de ADC1** (CH9) | Pulso bajo de 60 µs al arrancar: no afecta a una entrada |
| 37 | Cualquiera; es el **único libre que vale para una salida** activa alta (REL-04) | — |
| 18 | Solo entrada | Pulso alto al arrancar |
| 39 | Entrada o drenador abierto | WPU de 45 kΩ desde el reset |

- Lo que puede necesitar un pin más adelante: un DSEL común si se monta la segunda fuente BTT6030-2ERA (salida, `mcu.md` §9.2). Lo cubre GPIO37 (o GPIO10) si queda libre.
- Bus I²C de la placa: GPIO41/42, *pull-ups* R24/R25 de 4,7 kΩ y un solo dispositivo, el SHT40 en 0x44 (`sensores.md` §3). El bus de expansión (GPIO47/48) no vale para los pulsadores: se queda sin alimentación con EXP_EN bajo (+3V3_EXP) y ya usa 0x20–0x27 (TCA9535) y 0x48–0x4B (ADS1115) del módulo.

### 1.2 Opción A: escalera de resistencias en serie en GPIO10 (ADC1_CH9)

**Esquema:**

- **Rp = 15 kΩ** de +3V3 al nudo; nudo → GPIO10, con **C = 100 nF** a GND junto al pin.
- Del nudo sale una cadena de resistencias en serie: SW1 cierra a GND en el propio nudo y SWk en la toma k. Los tramos son Ra2 1 kΩ, Ra3 1,5 kΩ, Ra4 2 kΩ, Ra5 3 kΩ y Ra6 3,9 kΩ, con lo que S_k (suma de tramos hasta la toma k) = 0; 1; 2,5; 4,5; 7,5 y 11,4 kΩ.
- Sin pulsar, la cadena no lleva corriente y el pin está a +3V3, con el ADC saturado (código 4095).

**Cálculo:** V_k = V_DD · S_k / (Rp + S_k). Para el peor caso se combinan:

- V_DD de 3,17 V (3,211 V del TLV1117LV menos 40 mV del pico de Wi-Fi, `mcu.md` §8.3) a 3,39 V (`viabilidad-expansion.md` §10);
- cada resistencia al ± 1,5 % (± 1 % de tolerancia y 100 ppm/K en 50 K), en el sentido que más aleja el valor;
- el ADC a ± 10 mV (S tabla 5-6, ATTEN2).

| Pulsado | S_k | Mín. | Nominal (3,30 V) | Máx. | Hueco hasta el nivel siguiente | Umbral (mitad del hueco) |
|---|---|---|---|---|---|---|
| SW1 | 0 | 0 mV | 0 mV | 10 mV | 173 mV | 96 mV |
| SW2 | 1,0 kΩ | 183 | 206 | 228 | 203 | 330 |
| SW3 | 2,5 kΩ | 431 | 471 | 507 | 198 | 606 |
| SW4 | 4,5 kΩ | 705 | 762 | 811 | 215 | 918 |
| SW5 | 7,5 kΩ | 1026 | 1100 | 1163 | 173 | 1249 |
| SW6 | 11,4 kΩ | 1336 | 1425 | 1499 | — | **reposo ≥ 1600 mV** |

- **Margen:** cada umbral está a ≥ 86 mV del peor caso de los dos niveles que separa, frente a ± 10 mV del ADC (8,6 veces). El nivel más alto (1,50 V) queda dentro del margen calibrado de 0–1,6 V.
- **Valores:** salen de una búsqueda entre los valores Basic de 470 Ω–4,7 kΩ con Rp = 10, 12 o 15 kΩ (`s31_escalera.py`, carpeta temporal), que maximiza el hueco mínimo. Con Rp = 10 kΩ el mejor hueco es menor.
- **Corrientes:** máximo 3,39 V / 15 kΩ = 0,23 mA con SW1 (≤ 50 mA del TS). La fuga del pin (≤ 50 nA, S tabla 5-4) da 0,75 mV con 15 kΩ: despreciable. Los 100 mΩ del contacto, frente a 1 kΩ del primer tramo, también.
- **Tiempos:** al soltar, el nudo carga a través de Rp, con τ = 15 kΩ × 100 nF = 1,5 ms. Al pulsar SW6, τ = (15 ‖ 11,4 kΩ) × 100 nF = 0,65 ms, y llega a 10 mV del nivel en 3,4 ms. Los niveles intermedios que cruza duran < 1 ms y no pasan el filtro de 3 muestras iguales cada 10 ms (§1.5).

**Dos pulsaciones a la vez:** con la cadena en serie gana el pulsador más cercano al nudo, porque cortocircuita el resto. Si se pulsan SWj y SWk con j < k, se lee V_j: siempre uno de los dos pulsados, **nunca un tercer canal**. El firmware solo acepta una pulsación nueva después de volver al reposo, así que el segundo pulsador se ignora (hay que repetirlo), y al soltar SWj no reaparece SWk. Se descarta la escalera en paralelo (una resistencia a GND por pulsador): dos pulsados dan el paralelo de los dos, que puede caer en la ventana de otro canal y accionarlo.

**ESPHome:** no tiene un componente de teclado analógico. Se usa `sensor: adc` (GPIO10, `attenuation: 6db`, `update_interval: 10ms`, `internal: true`) con un `on_value` en *lambda* que:

1. clasifica la lectura con los umbrales de la tabla;
2. pide 3 muestras iguales seguidas (30 ms);
3. arranca desarmado y se arma en reposo;
4. con el primer nivel estable tras el reposo, conmuta el *switch* del canal (un `script` con parámetro), y se desarma.

Hay que bajar el *log* de `sensor` a `INFO` para que 100 lecturas por segundo no llenen el registro. ADC1 funciona con el Wi-Fi activo (S §4.2.2.1, p. 59). Las lecturas de IS1–IS6, VIN_SENSE y LIM_IMON comparten el ADC1 sin conflicto: ESPHome las hace de una en una.

**Pines:** usa GPIO10. Quedan **GPIO18, 37 y 39**; GPIO37 sigue disponible para un DSEL. Se pierde la reserva de ADC1; con la BTT6030 se liberarían 3 canales (`mcu.md` §9.2).

**Riesgos:**

- Un tramo en corto por un defecto de montaje haría que un pulsador accione el canal del vecino. Un Rp abierto deja el nudo flotando: el arranque desarmado evita que se accione nada, pero una deriva lenta podría dar una conmutación espuria. Lo detecta la prueba «Pulsadores manuales» de `docs/02`, y FW-04 acota el efecto.
- La lectura de reposo (ADC saturado, ≥ 1,6 V) y los umbrales se comprueban en el prototipo.

### 1.3 Opción B: expansor I²C en el bus de la placa (GPIO41/42)

**Esquema:**

- **TI PCA9554PWR** (8 E/S, TSSOP-16) junto a la fila de pulsadores, con A2–A0 a GND, dirección **0x20**. No choca con el SHT40 (0x44), que es lo único que hay en ese bus.
- P0–P5: un pulsador cada una, a GND. Los *pull-ups* internos de 100 kΩ (PCA p. 15) evitan resistencias externas. P6 y P7, sin conectar: también llevan *pull-up* interno.
- 100 nF en VCC.
- **INT** (drenador abierto, PCA p. 1) a **GPIO39**, con 10 kΩ a +3V3: es una de las dos funciones que admite ese pin, y su WPU no estorba.

**Cálculo:**

- *Pull-ups*: de 3,3 V / 100 kΩ = 33 µA por pulsador apretado.
- Consumo: I_CC ≤ 175 µA a 400 kHz (PCA p. 7).
- Bus: el SHT40 se calculó con C_bus ≤ 50 pF (`mcu.md` §11). Con el PCA9554 (≈ 10 pF) y ≈ 10 cm más de pista hasta el centro (≈ 10 pF), C_bus ≈ 70 pF y t_r = 0,8473 × 4,7 kΩ × 70 pF = 0,28 µs. Cumple ≤ 0,3 µs a 400 kHz con poco margen (7 %) y ≤ 1 µs a 100 kHz con margen 3,6 veces. **El bus de la placa se configura a 100 kHz.**

**Dos pulsaciones a la vez:** cada entrada se lee por separado: se detectan las dos y cada una conmuta su canal, que es lo que pide la prueba «un cambio por pulsación».

**ESPHome:**

- Componente `pca9554` (`address: 0x20`, `interrupt_pin: GPIO39`) en el bus `i2c` de GPIO41/42, y un `binary_sensor: gpio` por pulsador (`inverted: true`, `filters: delayed_on_off: 30ms`, `on_press: switch.toggle`).
- Es el *chip* que ESPHome cita como probado. Con INT, el componente lee el PCA9554 solo cuando cambia una entrada; sin INT, lo sondea en cada vuelta del bucle (≈ 60 lecturas por segundo en el bus del SHT40).

**Pines:** con INT usa GPIO39 y quedan **GPIO10, 18 y 37**, con la reserva de ADC1 y GPIO37 para un DSEL. Sin INT quedan los 4.

**Riesgos:**

- Un PCA9554 averiado que retenga SDA bloquearía también el SHT40 (AMB-01). La separación en dos buses (`mcu.md` §9.2) era frente al cable de expansión, no frente a un *chip* de la placa.
- Si falla el bus, los pulsadores dejan de funcionar, pero no accionan nada.

**Variantes del mismo esquema:**

| MPN | LCSC · tipo · stock | Diferencia |
|---|---|---|
| NXP PCA9554PW,118 | C17230 · Extended · 18 920 | Más barato y con más stock. El datasheet de NXP no se ha podido descargar: falta confirmar el *pull-up* de 100 kΩ y el pinout TSSOP-16 |
| TI TCA9554PWR | C477924 · Extended · 5 455 | Sin *pull-ups* internos (TCA): +6 × 10 kΩ (C25804). En ESPHome, «debería funcionar» |
| TI TCA9534PWR | C783615 · Extended · 7 510 | Igual que el TCA9554, 0,93 $ |
| PCF8574 (TI C882809 · 895; HGSEMI C2987288 · 6 935) | Extended | E/S cuasibidireccionales que hacen de *pull-up*; componente `pcf8574`. El de TI tiene poco stock y el de HGSEMI es un clon sin historial |

### 1.4 Opción C: mixta, 3 GPIO directos más una escalera de 3 niveles

- SW1–SW3 en **GPIO37, 18 y 39**, con 10 kΩ a +3V3 y el pulsador a GND.
- SW4–SW6 en una escalera en serie de 3 niveles en **GPIO10**: Rp 10 kΩ (C25804) y tramos de 2,2 kΩ (C4190) y 4,7 kΩ (C23162), con 100 nF. Con el mismo peor caso de §1.2: 0–10 mV, 548–637 mV y 1261–1419 mV, con huecos de ≥ 538 mV.
- Dos pulsaciones: los directos son independientes y en la escalera tiene prioridad SW4.
- ESPHome: `binary_sensor: gpio` para los directos más la *lambda* de §1.2 para la escalera.
- **Ocupa los 4 pines libres:** no queda ninguno para un DSEL ni para otra cosa. Mezcla dos mecanismos de lectura y no mejora a la A en nada importante.

Descartadas sin coste: una matriz de 2 × 3 (5 pines > 4) y el *charlieplexing* de 3 pines (las tres líneas tienen que conducir; GPIO18 y 39 solo admiten drenador abierto, y ESPHome no lo soporta).

### 1.5 Coste por placa

Unitarios a 5 y 10 placas (tramo de la cantidad real) más los cargos de JLCPCB *Economic*: 3,07 $ por pieza Extended y pedido, repartidos entre las placas, y 0,0016 $ por unión. No incluye el mínimo de compra de los pasivos, que ajusta jr-conformidad.

- **Común a todas:** 6 × TS-1187A (0,0215 $) más 24 uniones = **0,17 $**, que no se cuentan en la tabla.
- **Línea Extended nueva:** A y C no tienen ninguna; las variantes de B, una.

| Opción | Piezas (LCSC) | Uniones | 5 placas | 10 placas | Pines libres que deja |
|---|---|---|---|---|---|
| **A · escalera de 6 en GPIO10** | Rp 15 kΩ C22809; Ra 1 kΩ C21190, 1,5 kΩ C22843, 2 kΩ C22975, 3 kΩ C4211 y 3,9 kΩ C23018; 100 nF C14663 (todas Basic) | 14 | **0,05 $** | **0,05 $** | 18, 37, 39 |
| **B · PCA9554PWR (TI) + INT** | C2873588 (Extended, 1 545; 1,44 / 1,18 $), 100 nF C14663, 10 kΩ C25804 | 20 | 1,45 + 0,61 + 0,03 = **2,10 $** | 1,20 + 0,31 + 0,03 = **1,53 $** | 10, 18, 37 |
| B' · PCA9554PW,118 (NXP) + INT | C17230 (Extended, 18 920; 1,02 / 0,83 $) y las mismas | 20 | **1,68 $** | **1,19 $** | 10, 18, 37 |
| B'' · TCA9554PWR + 6 *pull-ups* + INT | C477924 (Extended, 5 455; 0,83 / 0,68 $), 7 × C25804, C14663 | 32 | **1,52 $** | **1,06 $** | 10, 18, 37 |
| C · mixta | 4 × 10 kΩ C25804, 2,2 kΩ C4190, 4,7 kΩ C23162, 100 nF C14663 (Basic) | 14 | **0,05 $** | **0,05 $** | ninguno |

### 1.6 Comparación

| Criterio | A · escalera | B · PCA9554 | C · mixta |
|---|---|---|---|
| Coste por placa (5 / 10 uds) | 0,05 / 0,05 $ | 2,10 / 1,53 $ (B'': 1,52 / 1,06 $) | 0,05 / 0,05 $ |
| Líneas Extended | 0 | 1 | 0 |
| Dos pulsaciones | Gana la más cercana al nudo; la otra se ignora; nunca un tercer canal | Las dos, independientes | Directos independientes; prioridad en la escalera |
| Margen de lectura | Huecos de ≥ 173 mV frente a ± 10 mV del ADC | Digital | Huecos de ≥ 538 mV |
| ESPHome | *Lambda* propia (unas 20 líneas) | Componente probado (`pca9554`) | Mixto |
| Pines libres | 18, 37, 39 (sin reserva de ADC1) | 10, 18, 37 | Ninguno |
| Efecto en otros bloques | Ninguno | Un dispositivo más en el bus del SHT40; bus a 100 kHz | Ninguno |

### 1.7 Recomendación

**Opción A: escalera de 6 niveles en serie en GPIO10.**

- Cuesta 0,05 $ por placa, sin ninguna línea Extended, frente a 1,1–2,1 $ del expansor, que en buena parte son el cargo de 3,07 $ por pedido.
- No toca el bus del SHT40.
- Con dos pulsaciones a la vez nunca acciona un canal que no se ha pulsado.
- Deja libre GPIO37 para un DSEL y GPIO18 y 39 para entradas.
- El margen de lectura en el peor caso (huecos de ≥ 173 mV frente a ± 10 mV) es holgado.
- Lo que se pierde (la segunda pulsación simultánea y la reserva de ADC1) no lo pide EXP-03: los pulsadores son de uso ocasional con la caja abierta.

**Si el usuario prefiere** que dos pulsaciones a la vez funcionen las dos, o leer los pulsadores con un componente ya probado en ESPHome: opción B con el PCA9554PWR de TI (C2873588), INT en GPIO39 y el bus de la placa a 100 kHz. B'' es la variante más barata, pero ESPHome no la ha probado. B' necesita antes confirmar el datasheet de NXP.
