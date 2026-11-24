# Bloque de conectores: expansión EXP-02, pulsadores EXP-03 y taladros (SPEC-0031)

**Autor:** ing-diseno · **Fecha:** 2026-11-15 (paso 1: §1; paso 4: el resto).
**Requisitos:** EXP-02, EXP-03, EXP-04 (conector), AMB-03, FAB-07, FAB-08, KIC-02; además REL-04, REL-08, FW-04, MCU-05 y AMB-01.
**Decisiones:** DEC-0011 (sin entrada de pulsos; pulsadores), DEC-0012 (D9: expansión I²C con TCA9535 + ADS1115; conector de `viabilidad-expansion.md` §10) y DEC-0013 (pulsadores con TCA9554).
**Hoja:** `hardware/v2/conectores.kicad_sch` (A3). **Campos y stock:** `hardware/componentes/campos-conectores.csv` y `stock-conectores.csv` (JLCPCB, 2026-11-15).

## 0. Resumen

```
+5V ─ C48 ─ U14 TPS2553 (EN=IN, R69 68 k) ─ +5V_EXP ─ C50 ─────────────── J10-1
+3V3 ─ C49 ─ U15 TPS2553 (EN=IN, R70 220 k) ─ +3V3_EXP ─ C51 ──────────── J10-3
GPIO47 I2C_EXP_SDA ─ R73 100 ─┬─ R71 2,2 k a +3V3_EXP ─ U16 I/O1 ──────── J10-5
GPIO48 I2C_EXP_SCL ─ R74 100 ─┴─ R72 2,2 k a +3V3_EXP ─ U16 I/O2 ──────── J10-7
GPIO35 EXP_INT ─┬─ R77 10 k a +3V3, FAULT de U14 y U15 ─ R75 470 ─ U17 I/O1 ─ J10-9
GPIO36 EXP_EN ──┴─ R78 100 k a GND ─────────────────── R76 470 ─ U17 I/O2 ─ J10-10
                                     J10-2, 4, 6, 8 = GND · U16 VBUS = +3V3_EXP · U17 VBUS = +5V_EXP
GPIO41/42 (bus de la placa, R24/R25) ─ U18 TCA9554 (0x20) ─ P0…P5 ─ SW3…SW8 a GND (salidas 1…6)
GPIO39 BTN_INT ─ R79 10 k a +3V3 ─ INT de U18 · C52 en VDD de U18
```

| Función | Ref. | Pieza principal (LCSC · tipo) | Alternativa | Requisito |
|---|---|---|---|---|
| Conector de expansión | J10 | XFCN BH254R-10P, cabecera IDC 2 × 5 en ángulo recto, al ras del borde inferior (C492448 · Extended, THT; DEC-0017, SPEC-0038) | ZHOURI DC3-2.54-10PAL (C5156674; `BH254R-10P.md`) | EXP-02 |
| Interruptores de 5 V y 3,3 V | U14, U15 | TI TPS2553DBVR (C55266 · Extended) | — (la -1 se enclava) | EXP-02 |
| R_ILIM | R69, R70 | 68 kΩ (C23231) y 220 kΩ (C22961), Basic | 232 kΩ C22913 (Extended) | EXP-02 |
| C_IN / C_OUT | C48, C49 / C50, C51 | 100 nF (C14663) / 4,7 µF (C19666) y 1 µF (C15849), Basic | — | EXP-02 |
| ESD | U16, U17 | ST USBLC6-2SC6 (C7519 · Extended, línea de U6) | Semtech SRV05-4 (C13612) | EXP-02 |
| Serie y *pull-ups* | R71–R78 | 2,2 kΩ, 100 Ω, 470 Ω, 10 kΩ y 100 kΩ, Basic | — | EXP-02, REL-04 |
| Expansor de los pulsadores | U18 | TI TCA9554PWR, 0x20 (C477924 · Extended) | TI PCA9554PWR (C2873588), misma huella | EXP-03 |
| *Pull-up* de INT y desacoplo | R79, C52 | 10 kΩ (C25804), 100 nF (C14663), Basic | — | EXP-03 |
| Pulsadores | SW3–SW8 | XKB TS-1187A-B-A-B (C318884 · Basic; línea de SW1/SW2) | TS-1187A-C-E-B (C318887) | EXP-03 |
| Taladros M3 | H1–H4 | `MountingHole_3.2mm_M3_Pad_Via`, fuera del BOM | — | FAB-08 |

Resultados clave:

- **EXP-02** es el conector de `viabilidad-expansion.md` §10 sin cambios de diseño, con las referencias definitivas (§2). EXP_IO2 pasa a **EXP_EN** (salida, R78 de 100 kΩ, REL-04).
- **U14:** límite de 343–440 mA (≥ 0,30 A); **U15:** 104–146 mA (≥ 50 mA), con R al 1 % (SLVS841G pp. 16–17, ec. (1)–(3)).
- **Pulsadores (DEC-0013):** TCA9554 en el bus de la placa, 0x20, sin choque con el SHT40 (0x44). Las E/S llevan *pull-up* interno de 100 kΩ (SCPS233E pp. 16 y 25): **sin *pull-ups* externos**. INT en GPIO39. Bus de la placa a 100 kHz (§3).
- **GPIO:** quedan libres GPIO10, 18 y 37 (`mcu.md` §9.2).
- **Bordes (FAB-07, §4):** con 8 mm reservados en cada esquina para los taladros, el borde superior usa 34 de 84 mm y el inferior 71 de 84 mm.
- **Coste del bloque:** ≈ 2,2 $ en piezas (tramo de 10 uds) más dos líneas Extended nuevas de SMT (TPS2553 y TCA9554, 6,14 $ por pedido): **≈ 3,6 $ por placa con 5 uds y ≈ 3,0 $ con 10**. J10 es THT soldado por el usuario (FAB-06).
- **Pieza nueva:** símbolo `esp-riego:TPS2553DBVR` (KiCad 10 no lo trae; §6). El resto, oficiales.

Restricciones de layout (filas para `docs/diseno/restricciones.csv`; justificación en §4 y §5):

| Red | Corriente | Ancho mín. | Separación | Ubicación / keepout | Notas |
|---|---|---|---|---|---|
| +5V → U14-1 (IN) y +5V_EXP (U14-6 → C50 → J10-1, U17-5) | 0,44 A (límite de U14) | 0,3 mm | 0,2 mm | U14 y C50 junto a J10; C48 entre los pines 1 y 2 de U14 | `Default` vale (FAB-03). TPS2553 p. 25 |
| +3V3 → U15-1 y +3V3_EXP (U15-6 → C51 → J10-3, R71, R72, U16-5) | 0,15 A (límite de U15) | 0,25 mm | 0,2 mm | U15 y C51 junto a J10; C49 entre los pines 1 y 2 de U15 | — |
| ILIM_5V, ILIM_3V3 | µA | 0,2 mm | 0,2 mm | R69 / R70 junto al pin 5 de su TPS2553, pista corta | Una pista larga o ruidosa desvía el límite (TPS2553 p. 25) |
| I2C_EXP_SDA / SCL (GPIO47/48 → R73/R74) y EXP_SDA_J / EXP_SCL_J (→ U16 → J10-5/7) | 3 mA | 0,2 mm | ≥ 0,5 mm a redes de 24 V | U16 a ≤ 5 mm de J10; R71–R74 entre U16 y el módulo, junto a J10; sobre plano de GND continuo | Lejos de `Salidas` y del nodo SW del buck |
| EXP_INT / EXP_EN (GPIO35/36 → R75/R76) y EXP_INT_J / EXP_EN_J (→ U17 → J10-9/10) | < 1 mA | 0,2 mm | 0,2 mm | U17 a ≤ 5 mm de J10; R77, R78 y los FAULT de U14/U15 en el lado del MCU de R75/R76 | — |
| GND de J10 (pines 2, 4, 6 y 8) | 0,35 A | — | — | Cada pin con su vía al plano | Retorno de la lógica, no de potencia |
| J10 | — | — | ≥ 2,5 mm de patio a J1 y a J7 | Borde inferior, entre J1 y J7–J9 (FAB-07); ranura de la guía hacia el borde | Que la brida del cable no tape los bornes |
| H1–H4 | — | — | Sin piezas ni cobre de otras redes en Ø 8 mm (cabeza M3 y arandela) | Centro a 4 mm de los dos bordes de su esquina; 8 mm de cada borde reservados por esquina | FAB-08; anillo sin red (§4) |
| SW3–SW8 | — | — | ≥ 6 mm de cada tecla a piezas de más de 5 mm de alto | Fila en el **centro** de la placa, de izquierda a derecha salidas 1–6, paso 12,7 mm (mínimo 10,16), serigrafía «1»…«6» | EXP-03, FAB-07; solo se alcanzan con la caja abierta |
| BTN1–BTN6 | µA | 0,2 mm | 0,2 mm | U18 a ≤ 10 mm de la fila; pistas ≤ 40 mm sobre plano de GND | Entradas con *pull-up* interno de 100 kΩ: cortas y lejos del nodo SW del buck |
| I2C_SDA / SCL (rama hasta U18) | ≤ 0,7 mA | 0,25 mm | 0,2 mm | Rama del bus de la placa (R24/R25 en MCU) hasta U18; ≤ 10 cm de pista añadida | C_bus total ≤ 70 pF a 100 kHz (§3.3) |
| +3V3 de U18 y BTN_INT | < 1 mA | 0,25 mm | 0,2 mm | C52 a ≤ 2 mm del pin 16 de U18; R79 junto a U18 | — |

Fuentes:

- **TPS:** TI TPS2552/53, SLVS841G (oct. 2026; `hardware/componentes/datasheets/TPS2553.pdf`): pinout p. 4; I_OS pp. 16–17, ec. (1)–(3) (la (1), máximo, en la p. 16; la (2), nominal, y la (3), mínimo, en la p. 17); *layout* p. 25.
- **TCA:** TI TCA9554, SCPS233E (`datasheets/TCA9554PWR.pdf`): pinout p. 4; *pull-up* interno de 100 kΩ p. 16 («*weak pull-up (100 kΩ typical)*») y p. 25 («*no need for an external pull-up*»); dirección p. 19.
- **BH:** XFCN BH254R, hoja única (`datasheets/BH254R-10P.pdf`; ficha `BH254R-10P.md`). Hasta SPEC-0037, BH254V (`datasheets/BH254V-10P.pdf`). **USBLC6:** USBLC6-2SC6 (`datasheets/USBLC6-2SC6.pdf`), tabla 2, p. 2.
- **S:** ESP32-S3 Series Datasheet v2.2. Tabla 5-6 (p. 66): error total del ADC calibrado de ± 10 mV con ATTEN2 (6 dB), en 0–1600 mV; ± 50 mV con ATTEN3 (12 dB), en 0–2900 mV.
- **PCA:** TI PCA9554, SCPS128D (mar. 2021):
  - p. 1: INT de drenador abierto, entradas al encender y POR;
  - p. 7: I_CC;
  - p. 15: cada E/S configurada como entrada lleva un *pull-up* débil de 100 kΩ típ. a V_CC;
  - p. 18, tabla 8-2: direcciones 0x20–0x27 con A2–A0.
- **ESPHome 2026.10.2:**
  - `pca9554` admite PCA9554, PCA9554A, PCA9536 y PCA9535, probados, y TCA9554 y TCA9535, que «deberían funcionar»;
  - `pcf8574`, `mcp23008` y `tca9555`;
  - todos tienen `interrupt_pin`, que pasa de leer por sondeo a leer cuando cambia una entrada.
- **TS:** `hardware/componentes/TS-1187A-B-A-B.md`: 50 mA y 12 V; contacto ≤ 100 mΩ.
- **Precios:** `jlc.py`, 2026-11-15, tramo de la cantidad real. *Economic PCBA*: 3,07 $ por pieza Extended distinta y pedido; 0,0016 $ por unión SMT (`viabilidad-expansion.md` §6). Ninguna pieza Extended de este apartado es «preferida».

## 1. Lectura de los 6 pulsadores (EXP-03): comparación del paso 1

> **Decidido (DEC-0013, 2026-11-15): opción B'', TCA9554PWR.** El esquema elegido está en §3. La comparación del paso 1 se conserva con una corrección del paso 3: el TCA9554 **sí** lleva *pull-up* interno de 100 kΩ en cada E/S (SCPS233E pp. 16 y 25); la comparación lo confundió con el TCA9534. B'' queda sin los 6 *pull-ups* externos y con el coste corregido en §1.5–1.6.

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

- V_DD de 3,17 V (3,224 V de U4 AP2114H menos ≤ 50 mV del pico de Wi-Fi, `mcu.md` §8.3) a 3,39 V (`viabilidad-expansion.md` §10);
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
| TI TCA9554PWR | C477924 · Extended · 5 455 | Mismo esquema que B: también lleva *pull-up* interno de 100 kΩ (SCPS233E pp. 16 y 25; corregido en el paso 3, que en la comparación original añadía 6 × 10 kΩ). En ESPHome, «debería funcionar». **Elegido (DEC-0013)** |
| TI TCA9534PWR | C783615 · Extended · 7 510 | Sin *pull-ups* internos: +6 × 10 kΩ. 0,93 $ |
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
| B'' · TCA9554PWR + INT (**elegida**) | C477924 (Extended, 5 455; 0,83 / 0,68 $), C25804 (INT), C14663. *Corregido:* sin los 6 *pull-ups* (internos); la comparación original daba 1,52 / 1,06 $ con 32 uniones | 20 | **1,49 $** | **1,03 $** | 10, 18, 37 |
| C · mixta | 4 × 10 kΩ C25804, 2,2 kΩ C4190, 4,7 kΩ C23162, 100 nF C14663 (Basic) | 14 | **0,05 $** | **0,05 $** | ninguno |

### 1.6 Comparación

| Criterio | A · escalera | B · PCA9554 | C · mixta |
|---|---|---|---|
| Coste por placa (5 / 10 uds) | 0,05 / 0,05 $ | 2,10 / 1,53 $ (B'': 1,49 / 1,03 $, corregido) | 0,05 / 0,05 $ |
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

**Elección del usuario (DEC-0013):** B'', TCA9554PWR con INT en GPIO39 y el bus de la placa a 100 kHz (§3).

## 2. Conector de expansión EXP-02

Es la definición de `viabilidad-expansion.md` §10 (arquitectura 1, D9, DEC-0012) con las referencias definitivas. Aquí solo se resume y se añade lo que fija la hoja; los cálculos completos siguen en aquel documento.

### 2.1 Tipo

- **J10: XFCN BH254R-10P** (C492448; DEC-0017, SPEC-0038; BH254V-10P recta, C492442, hasta SPEC-0037), cabecera IDC con guía, 2 × 5 a 2,54 mm, en ángulo recto, THT en la cara superior (FAB-06), con la boca al ras del borde inferior. Huella `Connector_IDC:IDC-Header_2x05_P2.54mm_Horizontal` (cotas frente al dibujo en la ficha). Mismo pinout. 3 A por contacto, −40…105 °C (BH p. 1).
- Cuerpo de 20,35 ± 0,25 mm de largo, 8,8 mm de fondo y 8,9 mm de alto; taladro Ø 1,02 ± 0,05 (BH p. 1). Huella oficial `Connector_IDC:IDC-Header_2x05_P2.54mm_Horizontal`: taladro de 1,0 mm, patio de 15,13 × 21,36 mm, 3D oficial; las cotas cuadran (ficha `BH254R-10P.md`, SPEC-0038).
- Símbolo `Connector_Generic:Conn_02x05_Odd_Even`: impares en una fila y pares en la otra, como la numeración IDC (pin 1 marcado con el triángulo de la guía).
- Sin enclavamiento positivo: brida a la caja (`viabilidad-expansion.md` §10.1). Cable plano de 10 hilos, ≤ 3 m.

### 2.2 Pines y conexiones de la hoja

| J10 | Señal | GPIO | En la placa, del MCU al conector | ESD |
|---|---|---|---|---|
| 1 | +5V_EXP | — | U14 TPS2553 desde +5V; EN (3) unido a IN (1); R69 68 kΩ en ILIM; C48 100 nF en IN; C50 4,7 µF en OUT | U17 VBUS (5) |
| 3 | +3V3_EXP | — | U15 TPS2553 desde +3V3; EN unido a IN; R70 220 kΩ; C49 100 nF en IN; C51 1 µF en OUT | U16 VBUS (5) |
| 5 | EXP_SDA_J | 47 (I2C_EXP_SDA) | R73 100 Ω en serie; **R71 2,2 kΩ a +3V3_EXP en el lado del conector** | U16 I/O1 (1 y 6) |
| 7 | EXP_SCL_J | 48 (I2C_EXP_SCL) | R74 100 Ω; **R72 2,2 kΩ a +3V3_EXP**, lado del conector | U16 I/O2 (3 y 4) |
| 9 | EXP_INT_J | 35 (EXP_INT) | R75 470 Ω; **R77 10 kΩ a +3V3 y FAULT (4) de U14 y U15 en el lado del MCU** de R75 | U17 I/O1 (1 y 6) |
| 10 | EXP_EN_J | 36 (EXP_EN) | R76 470 Ω; **R78 100 kΩ a GND en el lado del MCU** de R76 (REL-04) | U17 I/O2 (3 y 4) |
| 2, 4, 6, 8 | GND | — | Plano | — |

- Netlist comprobada (`kicad-cli`, 2026-11-15): `/EXP_INT` = {U5-28, R75-1, R77-2, U14-4, U15-4}; `/EXP_EN` = {U5-29, R76-1, R78-1}; `/Conectores/EXP_SDA_J` = {J10-5, R71-2, R73-2, U16-1, U16-6}; `+5V` contiene U14-1, U14-3 y C48-1. El resto, en el Anexo A.
- **Por qué cada resistencia está en su lado:** los *pull-ups* del I²C en el lado del conector dan 0,40 V de margen de ruido cuando responde el módulo (en el lado del MCU serían 0,25 V; `viabilidad-expansion.md` §10.4). El *pull-up* de EXP_INT y los FAULT van en el lado del MCU para que los FAULT no pasen por la ESD ni por el cable (§10.6). El *pull-down* de EXP_EN va en el lado del MCU para que fije el pin aunque no haya cable (REL-04, `mcu.md` §10.2).

### 2.3 Interruptores de alimentación (U14, U15)

Ecuaciones (1)–(3) de SLVS841G, pp. 16–17 (la (1), I_OS máx., en la p. 16; la (2) y la (3), nominal y mínimo, en la p. 17), R en kΩ, I en mA; los extremos incluyen R al ± 1 %:

| | R_ILIM | I_OS mín. = 25 230 / (1,01·R)^1,016 | I_OS nom. = 23 950 / R^0,977 | I_OS máx. = 22 980 / (0,99·R)^0,94 | Carga | Margen |
|---|---|---|---|---|---|---|
| U14 (+5V_EXP) | 68 (C23231) | **343** | 388 | **440** | ≤ 300 mA (EXP-02) | 1,14× |
| U15 (+3V3_EXP) | 220 (C22961) | **104** | 123 | **146** | ≤ 50 mA | 2,1× |

- R dentro de 15–232 kΩ (TPS p. 4). V_IN de 3,3 y 5 V dentro de 2,5–6,5 V. EN activo alto (TPS2553, p. 4) unido a IN: siempre habilitados, sin GPIO.
- FAULT de drenador abierto (p. 4), con filtro de 7,5 ms: puede marcar al arrancar, así que el firmware ignora EXP_INT el primer segundo (`viabilidad-expansion.md` §10.3).
- Corto en el cable: los dos raíles juntos suman 0,985 A en +5V; el limitador de la placa queda en 4,81 A < 5,14 A, y U4 llega a 122,9 °C con USB a 5,25 V (riesgo 3 de §7; la misma cifra con el AP2114H, porque se calcula con la misma R_θJA supuesta de 60 °C/W). ALI-12 no cambia: `alimentacion.md` §4 ya cuenta 50 mA y 0,30 A.

### 2.4 Bus de expansión y ESD

- R71/R72 de 2,2 kΩ, definitivas: R_P(mín) 1,0 kΩ; t_r de 171 ns con 1 módulo y 1 m, y de 520 ns con 4 módulos y 3 m (≤ 1000 ns a **100 kHz**; `viabilidad-expansion.md` §10.4).
- U16 y U17 USBLC6-2SC6: V_RM 5,25 V, ≤ 3,5 pF por línea, IEC 61000-4-2 nivel 4 (USBLC6 tabla 2, p. 2). U16 con VBUS a +3V3_EXP (SDA, SCL) y U17 con VBUS a +5V_EXP (EXP_INT, EXP_EN), según §10.5. Corriente residual hacia el ESP32 limitada por R73–R76.
- Pinout del USBLC6 en el símbolo oficial `Power_Protection:USBLC6-2SC6`: I/O1 = 1 y 6, GND = 2, I/O2 = 3 y 4, VBUS = 5 (USBLC6 p. 1); las dos patas de cada I/O llevan la misma red en la hoja.

### 2.5 Firmware (EXP-02)

`mcu.md` Anexo B: EXP_EN como salida con `restore_mode: ALWAYS_OFF`, a bajo en `on_boot`, `ota: on_begin` y `on_shutdown`; escribir 0 en los expansores de los módulos antes de bajar EXP_EN y antes de subirlo al arrancar. `bus_exp` a 100 kHz.

## 3. Pulsadores manuales (EXP-03, DEC-0013)

### 3.1 Esquema

- **U18 TI TCA9554PWR** (C477924), TSSOP-16, alimentado de +3V3 con C52 100 nF junto a VDD (16). SDA (15) y SCL (14) al bus de la placa (`I2C_SDA`/`I2C_SCL`, GPIO41/42; *pull-ups* R24/R25 de la hoja MCU, sin duplicar).
- **A2–A0 (3, 2, 1) a GND → dirección 0x20** (TCA p. 19). En el bus de la placa solo está el SHT40 (0x44): sin choque. El TCA9535 del módulo también usa 0x20–0x27, pero va en el bus de expansión.
- **P0–P5 (4, 5, 6, 7, 9 y 10) → SW3–SW8, de la E/S a GND**: SW3 = salida 1 … SW8 = salida 6 (redes BTN1–BTN6). Cada E/S configurada como entrada tiene un *pull-up* interno de 100 kΩ típ. (TCA p. 16; p. 25: «*no need for an external pull-up*»). P6 y P7 (11, 12) sin conectar: su *pull-up* interno las mantiene en un nivel definido.
- **INT (13) → BTN_INT → GPIO39**, con **R79 10 kΩ a +3V3**. INT es de drenador abierto: es una de las funciones que admite GPIO39 (`mcu.md` §9.1), y su WPU de 45 kΩ queda en paralelo con R79 sin efecto.
- Al encender, las E/S del TCA9554 son entradas (TCA p. 1). Los pulsadores no actúan sobre las salidas sin el firmware.

### 3.2 Cálculo

- Pulsador apretado: 3,39 V / 100 kΩ = 34 µA por E/S; los 6 a la vez, 0,2 mA. Contacto del TS-1187A: 50 mA, ≤ 100 mΩ (ficha).
- V_IL del TCA9554 = 0,3·V_CC ≈ 0,96 V: con el pulsador cerrado, el pin queda a ≈ 0 V; abierto, el *pull-up* lo lleva a V_CC.
- INT: 3,39 V / 10 kΩ = 0,34 mA a nivel bajo.

### 3.3 Bus de la placa

- C_bus: el SHT40 se calculó con ≤ 50 pF (`mcu.md` §11). El TCA9554 (≈ 10 pF, supuesto) y ≈ 10 cm más de pista hasta el centro (≈ 10 pF) dan ≈ 70 pF: t_r = 0,8473 × 4,7 kΩ × 70 pF = 0,28 µs. A 400 kHz (≤ 0,3 µs) cumple con un margen del 7 %; a 100 kHz (≤ 1 µs), con 3,6×. **El bus de la placa va a 100 kHz** (DEC-0013; `mcu.md` §9.2 y Anexo B).
- Riesgo aceptado en DEC-0013: un TCA9554 averiado que retenga SDA bloquearía también el SHT40 (AMB-01).

### 3.4 Firmware (EXP-03, REL-08, FW-04)

- `pca9554` en `bus_placa`, `address: 0x20`, `interrupt_pin: GPIO39` (lee el TCA9554 solo cuando cambia una entrada). El TCA9554 «debería funcionar» con ese componente (mismo juego de registros que el PCA9554 probado); si el prototipo falla, PCA9554PWR (C2873588) en la misma huella y sin cambios de esquema (DEC-0013).
- Un `binary_sensor` por pulsador (`inverted: true`, antirrebote de ≈ 30 ms) con `on_press: switch.toggle` del canal. El *switch* aplica el tiempo máximo de FW-04 y las protecciones de REL-08: el pulsador no actúa directamente sobre la salida.
- Dos pulsaciones a la vez: se leen por separado y cada una conmuta su canal (prueba «Pulsadores manuales» de `docs/02`).

## 4. Bordes y taladros M3 (FAB-07, FAB-08)

Datos: placa de 100 × 70 mm (hasta SPEC-0037; FAB-08 pasa a 100 × 100 mm con DEC-0016, y la colocación b4, `colocacion-b4.csv`, sustituye este reparto). Patios de las huellas medidos con `huella.py`.

**Esquinas:**

- H1–H4 (`MountingHole_3.2mm_M3_Pad_Via`): anillo de Ø 6,4 mm y patio de 6,9 × 6,9 mm, con el centro a 4 mm de los dos bordes. El patio llega a 4 + 3,45 = 7,45 mm de la esquina por cada borde.
- Una cabeza M3 (ISO 4762, Ø 5,5 mm) con arandela (ISO 7089, Ø 7 mm) pide un radio libre de 3,5 mm alrededor del centro: también llega a 7,5 mm.
- **Se reservan 8 mm por esquina en cada borde.** Útil: 100 − 2 × 8 = **84 mm** en los bordes largos y 70 − 2 × 8 = **54 mm** en los laterales.

| Borde | Contenido (FAB-07) | Suma | Útil | Margen |
|---|---|---|---|---|
| Superior | J4–J6 (salidas 1–3): 3 × 10,66 mm de patio (cuerpos de 10,16 mm) + 2 huecos de 1 mm | **34,0 mm** | 84 mm | 50 mm |
| Inferior | J1 (entrada, 10,66) + 2,5 + J10 (21,36; cuerpo de 20,35 ± 0,40) + 2,5 + J7–J9 (salidas 4–6, 3 × 10,66) + 2 huecos de 1 mm | **71,0 mm** | 84 mm | 13 mm |
| Lateral de la antena | U5 con la antena fuera del borde (*keepout* de 21 mm de ancho, `mcu.md` §12) + ≥ 15 mm de objetivo hasta J2 + J2 USB-C (≈ 9 mm) | ≈ 45 mm | 54 mm | ≈ 9 mm |
| Lateral opuesto | Isla del SHT40 (≈ 12 mm, `sensores.md` §6) | ≈ 12 mm | 54 mm | ≈ 42 mm |

- **Inferior:** los 2,5 mm a cada lado de J10 separan las señales del conector de los bornes de 24 V y dejan sitio a la brida. El orden J1 · J10 · J7–J9 es el de `viabilidad-expansion.md` §10.7; el *floorplan* puede cambiarlo si así acorta BUS_24V.
- **Laterales:** USB-C y antena pueden ir en laterales distintos (el USB-C cabe también junto a la isla del sensor). Lo decide el *floorplan*; los dos repartos caben.
- Esta cifra del borde inferior sustituye a la estimación de `estudio-salidas.md` §1.8.

**Centro:** la fila SW3–SW8 a 12,7 mm de paso mide 5 × 12,7 + 7,5 = 71 mm (con el mínimo de 10,16 mm, 58 mm) y cabe en los 84 mm entre las zonas de los taladros. Va en la franja central, entre las dos bandas de bornes y *high-side*, por donde también pasan el bus de 24 V y los planos (DEC-0011): los pulsadores son SMD en la cara superior y el bus puede ir por la inferior bajo ellos. U18 va junto a la fila.

## 5. Restricciones de layout: justificación

La tabla está en §0.

- **+5V_EXP y +3V3_EXP:** los anchos cubren el límite máximo de U14 y U15 (0,44 y 0,15 A) dentro de la clase `Default`; 0,3 mm en +5V_EXP por margen. C48/C49 entre IN y GND, junto al pin (TPS p. 25).
- **ILIM:** el límite depende de la corriente por R_ILIM; una pista corta evita acoplamientos (TPS p. 25).
- **I²C de expansión y ESD:** U16/U17 a ≤ 5 mm de J10 para que la descarga no recorra la placa; 0,5 mm a 24 V por la capacidad del cable y la tensión del bus (`viabilidad-expansion.md` §10.7).
- **J10:** en el borde inferior, entre la entrada y los bornes 4–6 (FAB-07), con la ranura hacia fuera para que el cable salga por el borde.
- **Taladros:** §4.
- **Pulsadores:** paso de 12,7 mm para pulsar uno sin tocar el vecino (tecla de Ø 2 mm); 6 mm hasta piezas altas (bornes de 14 mm, condensadores de granel) para el dedo. BTN1–BTN6 son entradas de alta impedancia (100 kΩ): cortas, sobre plano y lejos del nodo SW del buck.
- **Rama I²C hasta U18:** fija el C_bus de §3.3.

## 6. Símbolos, huellas y modelos 3D

| Ref. | Símbolo | Huella | 3D |
|---|---|---|---|
| U14, U15 | **`esp-riego:TPS2553DBVR` (nuevo)** | `Package_TO_SOT_SMD:SOT-23-6` | Oficial |
| U16, U17 | `Power_Protection:USBLC6-2SC6` | `Package_TO_SOT_SMD:SOT-23-6` | Oficial |
| U18 | `Interface_Expansion:TCA9554PW` | `Package_SO:TSSOP-16_4.4x5mm_P0.65mm` | Oficial |
| J10 | `Connector_Generic:Conn_02x05_Odd_Even` | `Connector_IDC:IDC-Header_2x05_P2.54mm_Horizontal` | Oficial (SPEC-0038) |
| SW3–SW8 | `Switch:SW_Push` | `esp-riego:SW_Push_1P1T_XKB_TS-1187A` | Propio (SPEC-0021) |
| R, C | `Device:R`, `Device:C` | `R_0603_1608Metric`, `C_0603_1608Metric` | Oficial |
| H1–H4 | `Mechanical:MountingHole` | `MountingHole:MountingHole_3.2mm_M3_Pad_Via` | — (fuera del BOM) |

**Símbolo nuevo `esp-riego:TPS2553DBVR`** (KiCad 10.0.6 no trae TPS2552/53; jr-conformidad, parte 02), hecho desde la tabla de pines de la p. 4 (DBV, SOT-23-6):

| Pin | Nombre | Tipo eléctrico | Lado del símbolo |
|---|---|---|---|
| 1 | IN | `power_in` | Izquierda, arriba |
| 2 | GND | `power_in` | Abajo |
| 3 | EN (activo alto en el TPS2553) | `input` | Izquierda, abajo |
| 4 | ~FAULT (drenador abierto) | `open_collector` | Derecha, abajo |
| 5 | ILIM | `passive` | Abajo |
| 6 | OUT | `power_out` | Derecha, arriba |

- Cuerpo de 15,24 × 15,24 mm; pines de 2,54 mm en rejilla de 2,54 mm. Campos: `Value`, `Footprint` (`Package_TO_SOT_SMD:SOT-23-6`), `Datasheet` (ti.com), `Description`, `LCSC Part#` (C55266) y `MPN`.
- `huella.py Package_TO_SOT_SMD:SOT-23-6 --simbolo esp-riego:TPS2553DBVR`: 6 pines, ningún pin sin pad ni pad sin pin. Pad 1 de la huella = pin 1 del encapsulado DBV (marca de la p. 4).
- Imagen: `vista.py hoja hardware/v2 --hoja Conectores --zona 30,55,100,100`.

## 7. Riesgos y puntos abiertos

1. **TCA9554 en ESPHome:** «debería funcionar»; lo comprueba el prototipo. Si falla, PCA9554PWR en la misma huella (DEC-0013).
2. **Bus de la placa compartido:** un fallo del TCA9554 bloquearía el SHT40 (AMB-01). Riesgo aceptado (DEC-0013).
3. **U4 (AP2114H desde SPEC-0038) con el cable de expansión en corto:** 122,9 °C con USB a 5,25 V, margen de 2,1 K, solo en fallo; el apagado térmico del AP2114H es de 160 °C (p. 12) (`viabilidad-expansion.md` §12, riesgo 6). Prueba en el prototipo.
4. **Capacidades supuestas** (10 pF) del pin del ESP32-S3, del ADS1115 y del TCA9554: con el doble, el caso de 4 módulos y 3 m sigue ≤ 1000 ns (riesgo 5 de aquel documento), y el bus de la placa quedaría en ≈ 90 pF y 0,36 µs, dentro de 1 µs a 100 kHz.
5. **4.º módulo:** depende del tiempo de mantenimiento de SDA con ADDR = SDA (riesgo 4 de aquel documento).
6. **J10 sin enclavamiento:** brida a la caja (§2.1).
7. **Bordes:** las cifras de §4 usan el contorno de 100 × 70 mm (hasta SPEC-0037); la colocación b4 en 100 × 100 mm (`colocacion-b4.csv`, DEC-0016) las sustituye.

## 8. Trazabilidad

| Requisito | Pieza o cálculo | Sección |
|---|---|---|
| EXP-02 | J10 BH254R-10P con I²C (GPIO47/48), EXP_INT (35), EXP_EN (36), +3V3_EXP (U15, ≤ 50 mA), +5V_EXP (U14, ≤ 0,30 A) y GND; ESD U16/U17 | §2 |
| EXP-03 | SW3–SW8 leídos por U18 TCA9554 (0x20) en el bus de la placa, INT en GPIO39 (DEC-0013); fila en el centro | §1, §3, §4 |
| EXP-04 | Conector fijado con el informe de SPEC-0006 (arquitectura 1, DEC-0012) | §2 |
| AMB-03 | Sonda externa opcional en el bus de expansión: +3V3_EXP, SDA y SCL en J10 | §2.2 |
| FAB-07 | Bornes y J10 en los bordes superior e inferior; laterales para antena, USB-C y sensor; pulsadores en el centro | §4 |
| FAB-08 | H1–H4 M3 a 4 mm de los bordes; 8 mm reservados por esquina | §4 |
| KIC-02 | Hoja `conectores.kicad_sch` unida a la raíz con 7 pines; sin no conexiones provisionales | Anexo A |
| REL-04 | R78 100 kΩ en EXP_EN, en el lado del MCU | §2.2; `mcu.md` §10.2 |
| REL-08, FW-04 | Pulsadores leídos por el firmware; el *switch* del canal aplica las protecciones y el tiempo máximo | §3.4 |
| MCU-05 | GPIO35, 36, 47 y 48 sin cambio de número; BTN_INT en GPIO39 (entrada de drenador abierto); libres 10, 18 y 37 | §3.1; `mcu.md` §9.2 |
| AMB-01 | SHT40 y TCA9554 en el mismo bus, sin choque de direcciones; riesgo de bloqueo aceptado | §3.3 |

## Anexo A. Etiquetas jerárquicas de la hoja de conectores

| Etiqueta | Forma (vista desde Conectores) | Hoja de origen | Red de la netlist |
|---|---|---|---|
| I2C_SDA | Bidireccional | MCU (GPIO41) y Sensores | `/I2C_SDA` = {U5-34, R24-2, U13-1, U18-15} |
| I2C_SCL | Entrada | MCU (GPIO42) y Sensores | `/I2C_SCL` = {U5-35, R25-2, U13-2, U18-14} |
| BTN_INT | Salida | MCU (GPIO39) | `/BTN_INT` = {U5-32, R79-2, U18-13} |
| I2C_EXP_SDA | Bidireccional | MCU (GPIO47) | `/I2C_EXP_SDA` = {U5-24, R73-1} |
| I2C_EXP_SCL | Bidireccional | MCU (GPIO48) | `/I2C_EXP_SCL` = {U5-25, R74-1} |
| EXP_INT | Salida (FAULT de drenador abierto) | MCU (GPIO35) | `/EXP_INT` = {U5-28, R75-1, R77-2, U14-4, U15-4} |
| EXP_EN | Entrada | MCU (GPIO36) | `/EXP_EN` = {U5-29, R76-1, R78-1} |
| +5V, +3V3, GND | Símbolos de alimentación globales | — | — |

- **Redes internas:** +5V_EXP {U14-6, C50-1, J10-1, U17-5}; +3V3_EXP {U15-6, C51-1, J10-3, R71-1, R72-1, U16-5}; EXP_SDA_J {J10-5, R71-2, R73-2, U16-1, U16-6}; EXP_SCL_J {J10-7, R72-2, R74-2, U16-3, U16-4}; EXP_INT_J {J10-9, R75-2, U17-1, U17-6}; EXP_EN_J {J10-10, R76-2, U17-3, U17-4}; ILIM_5V {U14-5, R69-1}; ILIM_3V3 {U15-5, R70-1}; BTN1…BTN6 {SWn-1, U18 P0…P5}. U18-11 y U18-12 sin conectar.
- **En la hoja:** las etiquetas y los símbolos de alimentación van en el extremo de los pines, sin cables (SPEC-0028): EN e IN de U14 y de U15 llevan cada uno su +5V o +3V3, y los GND 2-4-6-8 de J10 (J10 está girado 180°: pares a la izquierda) y A0-A1-A2 de U18, su GND, girados hacia fuera del pin. La hoja se regenera con `hoja.py extraer` + `generar`, y esta tabla se comprueba con `hoja.py netlist hardware/v2 --plan docs/diseno/conectores.md --seccion "Anexo A"`.
- **En la raíz:** la hoja «Conectores» tiene los 7 pines en su borde izquierdo, unidos con etiquetas locales a los de la hoja MCU y, en I2C_SDA/SCL, también a los de Sensores. En la hoja MCU, `EXP_IO2` pasa a `EXP_EN` (salida) y el pin de GPIO37 a `BTN_INT` (entrada, GPIO39); GPIO37 queda sin conectar. Se quitaron las 5 no conexiones provisionales de la hoja MCU. La PCB se ha resincronizado: `/MCU/EXP_IO2` → `/EXP_EN` y U5-32 pasa a `/BTN_INT`; U5-30 (GPIO37) queda sin red.
