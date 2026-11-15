# Viabilidad del módulo de expansión de canales y conector EXP-02 (SPEC-0006)

**Estado:** propuesta para la decisión D9 del usuario. **Autor:** ing-diseno · **Fecha:** 2026-11-15. **Rev. VAL-0006-01** (2026-11-15): barreras de REL-04 y conexiones de los TPS2553 para SPEC-0031 (§10.6), lista de piezas por variante, R_ILIM_B = 220 kΩ por el caso del USB (§10.3), OE de la arquitectura 3, márgenes de I²C en los dos sentidos y 4.º módulo (§10.4), precio del Waveshare.
**Requisitos:** EXP-02, EXP-04; además ALI-12, ALI-13, REL-03…REL-05, REL-10, FAB-07 de `docs/02` v0.6; DEC-0003, DEC-0004, DEC-0011.
**Precios y stock:** API de JLCPCB (`herramientas/kicad/jlc.py`, también `--buscar`), consulta del **2026-11-15**, en el tramo de la cantidad real del pedido. Todos los precios usados y todos los códigos citados, con cantidad y tramo: `hardware/componentes/stock-expansion.csv`. Lista de piezas de cada arquitectura y variante (código × cantidad por módulo, tipo, uniones y precio de los dos tramos), de la que salen los totales de §8: `hardware/componentes/bom-expansion.csv`. Tarifas de montaje: JLCPCB *Economic PCBA*, artículo actualizado el 2026-10-22 (fuentes, §10).

> Datasheets (páginas del PDF, descargados el 2026-11-15 de ti.com o de la copia de LCSC):
> - **TCA9535:** SCPS201F (sep. 2026). **TCA9555:** SCPS200E (abr. 2019). **ADS1115:** SBAS444E (dic. 2024). **TPS2553:** SLVS841G (oct. 2026). **P82B715:** SCPS145B (feb. 2016). **PCF8574:** SCPS068K (sep. 2024). **TPIC6B595:** SLIS032D (abr. 2025). **MCP23017:** DS20001952D (LCSC C47023).
> - **USBLC6:** ST USBLC6-2 Rev 5 (`hardware/componentes/datasheets/USBLC6-2SC6.pdf`). **BH254V:** XFCN BH254V-xxP, rev. A1, 2024-07-19 (LCSC C492442, 1 página). **Cable:** 3M 3365, TS-0080-15 (dic. 2006).
> - **BTT:** BTT6050-1ERA Rev. 1.00 (`hardware/componentes/datasheets/`). **TPS2663:** SLVSE94G. `mcu.md` §8–§10 y `alimentacion.md` §3.13 y §4.

## 0. Resumen para decidir (D9)

**Lo que vale para todas las arquitecturas:**

- **El módulo necesita su propia entrada de 24 V y su propio limitador** (TPS26632, como la placa). Con la fuente de 5 A de la placa no cabe: el limitador de la placa ya llega a 4,57 A y, con la lógica, a 4,77 A frente a los 5,14 A a los que actúa la fuente (ALI-12, ALI-13). Un segundo limitador en la misma fuente pasa de 5,14 A. Por EXP-02 **no pasan 24 V** (§2.2). Es una consecuencia de D9 que hay que escribir en los requisitos (PENDIENTE 1).
- **La etapa de salida se repite:** BTT6050-1ERA por canal (DEC-0003), las mismas resistencias y la misma medida IS. Esta etapa, la entrada de 24 V y los cargos fijos de JLCPCB son ≈ 90 % del coste del módulo (§8).
- **La corriente de las válvulas instaladas sigue sin medir (DEC-0011).** Fija cuántas válvulas puede tener encendidas a la vez el módulo con una fuente de 5 A: 12 si toman 0,29 A (válvula de 24 V DC) y solo 5 si son 42 Ω resistivos (0,66 A en frío). No cambia la arquitectura ni el conector; cambia R_ILIM del módulo, la fuente y, quizá, una regla de firmware (§2.3).

| | 1 · I²C (expansor) | 2 · RS-485 / Modbus | 3 · Registros 74HC595 | 4 · Nodo ESP32 propio | 5 · CAN |
|---|---|---|---|---|---|
| Distancia | ≤ 3 m (≤ 50 m con P82B715) | ≤ 1200 m | ≤ 1 m | Cobertura Wi-Fi | ≤ 500 m a 125 kb/s |
| Módulos × canales | 3 × 8 seguros; 4 × 8 con ADDR = SDA, a comprobar (§10.4) | 247 × 8 | sin límite lógico | sin límite (HA) | > 100 × 8 |
| Diagnóstico REL-10 | Sí (ADS1115) | Sí (ADC del MCU) | **No** | Sí | Sí |
| Estado seguro si se corta | Hardware: EXP_EN + *pull-downs* | Firmware del esclavo (tiempo sin Modbus) | Hardware: EXP_EN + OE (con inversor) | Firmware del nodo | Firmware del esclavo |
| ESPHome | `pca9554` (16 pines) + `ads1115` | `modbus_controller`; esclavo **sin ESPHome** | `sn74hc595` | YAML propio (otro nodo) | `canbus` + *lambdas*; esclavo sin ESPHome |
| Firmware y puesta en marcha | Baja | Alta | Baja | Baja (dos nodos) | Alta |
| **8 canales, por módulo: 5 / 10 uds** | **30,9 / 24,9 $** | 31,3 / 25,4 $ + adaptador | 27,2 / 22,1 $ | 37,5 / 29,9 $ | 32,6 / 26,0 $ + adaptador |
| 6 canales: 5 / 10 uds | 28,2 / 22,2 $ | 28,8 / 22,7 $ | 24,5 / 19,4 $ | 34,8 / 27,2 $ | 30,1 / 23,2 $ |

**Recomendación (§9):** arquitectura **1, I²C con TCA9535 + ADS1115**, en la misma caja o en una contigua (≤ 3 m de cable plano), con entrada de 24 V y limitador propios. Es la más barata de las que mantienen el diagnóstico, va entera en el YAML de la placa principal y su estado seguro no depende del firmware. **Alternativa:** arquitectura **4, un nodo ESP32-S3 independiente** (en la práctica, otra placa ESP-Riego con 6 u 8 canales), cuando el módulo esté lejos o no se quiera tender cable. La alternativa no usa EXP-02.

**Conector EXP-02 (§10):** cabecera IDC 2 × 5 a 2,54 mm con guía de polarización (XFCN BH254V-10P, C492442, 28 794 en JLCPCB el 2026-11-15; alternativa Würth 61201021621, C4355000). Pines: 5 V, 3,3 V, I2C_EXP_SDA (GPIO47), I2C_EXP_SCL (GPIO48), EXP_INT (GPIO35), EXP_EN (GPIO36) y cuatro GND intercalados. **No pide GPIO nuevos:** quedan libres GPIO10, 18, 37 y 39 para los pulsadores de EXP-03. **3,3 V ≤ 50 mA y 5 V ≤ 0,30 A, como `alimentacion.md` §4: ALI-12 no cambia.** Cada alimentación sale por un TPS2553 con límite de corriente, para que un corto en el cable no tumbe la lógica de la placa. ESD con dos USBLC6-2SC6 (línea de U6). *Pull-ups* definitivos de 2,2 kΩ a 100 kHz. Sin extensor de bus en la placa. Piezas del lado de la placa: §10.6 (≈ 2 $ por placa); restricciones de layout: §10.7.

## 1. Datos de partida

| Dato | Valor | Origen |
|---|---|---|
| Pines reservados | I2C_EXP_SDA GPIO47 y SCL GPIO48 (bus propio, separado del SHT4x), EXP_INT GPIO35 (entrada), EXP_IO2 GPIO36 (E/S). Los cuatro en alta impedancia, sin *pull*, durante el reset y el flasheo | `mcu.md` §9.2 |
| Pines libres | GPIO10 (ADC1_CH9, cualquier uso), GPIO18 (solo entrada), GPIO37 (libre desde DEC-0011), GPIO39 (entrada o drenador abierto) | `mcu.md` §9.1-9.2, DEC-0011 |
| Pulsadores EXP-03 | 6, leídos por el firmware: escalera de resistencias en un ADC1 (GPIO10) o expansor en el bus de la placa (SPEC-0031) | DEC-0011 |
| Alimentación para la expansión | +3V3 ≤ 50 mA (dentro de los 0,45 A del TLV1117LV) y +5V ≤ 0,30 A (dentro de los 0,75 A del buck); lógica 4,32 W ≤ 4,8 W | `alimentacion.md` §4, `mcu.md` §8.2 |
| Fuente y limitador de la placa | 24 V, 5 A, sobrecarga desde 5,14 A; limitador 3,86–4,57 A; instalada ≤ 3,5 A | ALI-12, ALI-13, `alimentacion.md` §3.13.2 |
| Etapa de salida | BTT6050-1ERA por canal, IN activa alta, IS a ADC con R_SENSE 10 kΩ / R_IS 820 Ω | DEC-0003, `salidas.md` §0 |
| Válvulas instaladas | Bermad S-390-3-D, 24 V AC alimentada en continua; corriente sin medir. 42 Ω a 20 °C según la fila de la ficha (cuenta del coordinador, sin validar) | DEC-0011 |
| Ambiente | 60 °C dentro de la caja; −10 °C mínimo | §5 de `docs/02` |

## 2. Lo común a las cinco arquitecturas

### 2.1 Etapa de salida del módulo

Se repite la de la placa (`salidas.md`): BTT6050-1ERA, R_IN y R_PD en IN, R_OL, C_VS, C_OUT, LED de canal, borne WJ500V. Dos formas de medir IS:

- **IS por canal a un ADC** (arquitecturas 2, 4 y 5, con un MCU en el módulo): igual que la placa, DEN común.
- **IS compartido** (arquitecturas 1 y 3): las salidas IS de los 8 BTT se unen en un nodo con una R_SENSE, R_IS y C_IS, y cada canal se selecciona con su DEN. Con DEN bajo, IS queda en alta impedancia (BTT p. 23). El datasheet solo desaconseja compartir IS entre chips con distinta alimentación (p. 23); aquí todos cuelgan del mismo bus del módulo. Fuga de cada IS deshabilitado ≤ 1 µA (I_IS(DIS), p. 30): 7 µA × 820 Ω = 5,7 mV en el nodo, que el diseño del módulo resta del umbral de carga abierta (18 mV en `salidas.md` §3.2, calculado con el error del ADC del ESP32; con el ADS1115 el error es mucho menor).

Con IS compartido, cada canal necesita IN y DEN: 16 líneas para 8 canales, justo las de un expansor de 16 bits.

### 2.2 Alimentación de las salidas y de la lógica del módulo

| Opción | Valoración |
|---|---|
| 24 V por EXP-02 desde `BUS_24V` | **No.** ALI-13 lo prohíbe: el bus limitado ya tiene su carga instalada (3,5 A) |
| 24 V por EXP-02 desde `VIN_PROT` (antes del limitador) | **No.** F1, Q1 y las pistas `Power_In` están dimensionados para 5,1 A (ALI-12); más corriente obliga a cambiar ALI-12, el fusible y la fuente. Además, la cabecera IDC no lleva amperios |
| **Entrada de 24 V propia en el módulo** (borne + fusible + polaridad + TVS + TPS26632) | **Sí.** Repite el nodo de entrada de `alimentacion.md` §2 sin el buck. Coste ≈ 5,3 $ en piezas por módulo con 10 uds (§8) |

- **Fuente del módulo:** una segunda fuente de 24 V (por ejemplo, otra igual a la de la placa). Con la misma fuente de 5 A, el limitador de la placa (máx. 4,57 A) más el del módulo (mín. 3,86 A) superan los 5,14 A: habría que cambiar ALI-12, ALI-13 y DEC-0004 (fuente mayor). Se propone en PENDIENTE 1.
- **Masas:** si la fuente del módulo es otra (salida aislada, lo normal en las fuentes LED), el GND de EXP-02 es la única unión y por él solo circula la corriente de la lógica. Si las dos fuentes comparten el negativo, parte del retorno de las válvulas del módulo vuelve por los GND del cable: con 1 m de cable plano (4 × 28 AWG, 0,053 Ω) frente a ≈ 12 mΩ del cable de alimentación, ≈ 16 % de 3,5 A = 0,55 A y 29 mV de desplazamiento, aceptable frente a los 0,5 V de margen de ruido del I²C (§10.4). Recomendación: no unir el negativo del módulo a tierra ni a la otra fuente.
- **Lógica del módulo por EXP-02:** en las arquitecturas 1 y 3 basta el 3,3 V del conector (§10.3: ≤ 9,5 mA por módulo). Las arquitecturas 2, 4 y 5 hacen su 3,3 V con un buck de 65 V desde su entrada (como la placa, ALI-05) y no toman nada del conector.

### 2.3 Efecto de la corriente de las válvulas (dato abierto, DEC-0011)

| Caso | I por válvula a 24,5 V y −10 °C | 8 válvulas (1 por canal) | 16 válvulas (2 por canal) | Válvulas a la vez con instalada ≤ 3,5 A y la banda de la placa |
|---|---|---|---|---|
| A · 24 V DC, 0,25 A a 20 °C (diseño) | 3,47 A / 12 = **0,29 A** (ALI-12) | 2,3 A ✔ | 4,6 A ✗ | 12 |
| B · 42 Ω resistivos (DEC-0011, sin validar) | 42 Ω × (1 − 0,00393 × 30) = 37,0 Ω → 24,5 / 37,0 = **0,66 A** | 5,3 A ✗ | 10,6 A ✗ | **5** |
| C · bobina AC con rectificador u otra | se mide | — | — | — |

- Con el caso A, un módulo de 8 canales con una válvula por canal cabe en una fuente de 5 A con el limitador de la placa (R_ILIM 4,30 kΩ, 3,86–4,57 A).
- Con el caso B, para 8 válvulas a la vez el TPS26632 tendría que subir a su máximo (R_ILIM 3,0 kΩ: 6 A ± 7 %, 5,58–6,42 A; TPS2663 p. 7), con una fuente de ≥ 7 A (24 V, 10 A) y el fusible y las pistas de entrada del módulo para esa corriente. La otra salida es una regla de firmware (≤ 5 válvulas a la vez en el módulo), que sería un requisito nuevo.
- En el caso B, dos válvulas por canal (1,32 A) superan el 1 A de REL-05 en el módulo y en la placa. Es la revisión que SPEC-0032 ya tiene pendiente (REL-03, REL-05, ALI-12); el módulo hereda su resultado.
- **Nada de esto cambia el conector EXP-02:** las salidas no se alimentan por él.

### 2.4 Estado seguro común

- En el módulo, cada IN y cada DEN llevan R_PD de 100 kΩ (como `salidas.md` §2.2). Sin control, el BTT está apagado.
- El limitador del módulo se habilita con **EXP_EN** (GPIO36, salida activa alta), con *pull-down* en la placa y en el módulo. Durante el reset, el flasheo y el arranque de la placa, GPIO36 está en alta impedancia (`mcu.md` §9.2) y el bus del módulo queda apagado: **REL-04 se extiende al módulo** sin firmware.
- Si se corta el cable, el *pull-down* del módulo apaga su limitador (arquitecturas 1 y 3). En las arquitecturas 2, 4 y 5, el corte lo detecta el firmware del módulo.

## 3. Arquitectura 1 · Expansor de GPIO por I²C

**Esquema:** EXP-02 → TCA9535 (16 E/S: IN1–8 y DEN1–8) + ADS1115 (canal 0: IS compartido; canal 1: IMON del limitador del módulo; canal 2: tensión de entrada) + entrada de 24 V con TPS26632 + 8 BTT6050. EXP_INT recoge el FLT (drenador abierto) del limitador del módulo. Dos cabeceras en el módulo (entrada y paso) para encadenar.

**Elección del expansor:**

| Pieza | Valoración |
|---|---|
| **TI TCA9535PWR** (C130204, 14 188, 1,22 $ a 10) | **Elegido.** Sin *pull-ups* internos en las E/S (p. 1); al encender, todas son entradas (p. 4, p. 16) y los R_PD del módulo dejan los BTT apagados. 8 direcciones (A0–A2, p. 17). V_OH ≥ 2,6 V a −8 mA con V_CC = 3 V (p. 7): V_IN del BTT ≥ 2,6 − 25 µA × 10 kΩ = 2,35 V ≥ 2,0 V. Fuente total ≤ 160 mA (p. 8, nota 3) frente a 8 × 1 mA de LED. C_io de SDA ≤ 9,5 pF (p. 8). −40…125 °C (p. 6) |
| TI PCA9535PWR (C3202154, 2 210, 1,18 $) | **Alternativa**, misma huella TSSOP-24 y mismos registros. Es el chip probado en ESPHome (`pca9554`, `pin_count: 16`); el TCA9535 figura como equivalente «que debería funcionar» |
| Microchip MCP23017 (C47023, 1 697, 1,49 $) | Válido: entradas al encender (IODIR = FFh, p. 16), pin RESET (p. 1), INT de drenador abierto (p. 11), ESPHome `mcp230xx`. GPA7 y GPB7 solo salida (p. 1), sin problema aquí. Descartado por precio y stock frente al TCA9535 |
| TCA9555 / PCA9555 | **Descartado:** incluye *pull-up* interno en las E/S (TCA9555 p. 3): al encender, IN alto en los 16 pines. Encendería las válvulas si el bus del módulo estuviera habilitado y anularía los R_PD |
| PCF8574 | **Descartado:** E/S cuasi-bidireccionales, altas al encender (p. 1) |

- **ADC:** TI ADS1115IDGSR (C37593, 12 662, 1,13 $): 16 bits, 4 direcciones (pin ADDR, p. 20), FSR ± 4,096 V con entradas hasta V_DD + 0,3 V (p. 4), 150–300 µA (p. 6). IS máximo en fallo: 2,32 V (`salidas.md` §0), dentro del rango. ESPHome `ads1115`. Alternativa: ADS1015 (C193969, 12 bits, 1,39 $).
- **Distancia y cableado:** cable plano de 10 hilos (28 AWG, 3M 3365 o equivalente) con GND entre señales, ≤ 3 m en total a 100 kHz (§10.4). Para 3–50 m, un par de P82B715 (C2649394, 6 726, 0,89 $; 400 pF en el lado del bus y 3000 pF en la línea, > 50 m con par trenzado, p. 1): uno en un adaptador enchufado en EXP-02 y otro en el módulo. El PCA9615 (diferencial) no tiene stock en JLCPCB el 2026-11-15.
- **Módulos y canales:** 3 módulos × 8 canales = 24 canales más con las direcciones del ADS1115 a GND, VDD y SCL; el 4.º (ADDR = SDA) pide una condición de tiempo que se comprueba en el prototipo (§10.4). El TCA9535 admite 8. Cada módulo, su dirección con puentes.
- **Estado seguro:** corte del cable → sin 3,3 V el TCA9535 no alimenta IN y los R_PD apagan los BTT; EXP_EN a nivel bajo apaga el limitador. Corte solo de SDA o SCL → el TCA9535 conserva sus salidas, pero el firmware ve el NACK y baja EXP_EN. Reset del TCA9535 por un bajón de 3,3 V → vuelve a entradas (POR, p. 18) → apagado. Bloqueo del firmware de la placa → los *watchdogs* del ESP32-S3 la reinician y GPIO36 vuelve a alta impedancia.
- **ESPHome:** `i2c` (`bus_exp`, 47/48, 100 kHz), `pca9554` con `pin_count: 16` y `interrupt_pin` en GPIO35, `ads1115`, `switch` de GPIO36 para EXP_EN con `restore_mode: ALWAYS_OFF`. Secuencia: escribir las salidas a 0 → subir EXP_EN → esperar ≥ 20 ms (como LIM_EN, `alimentacion.md` §3.13.5) → canal. Lectura de IS: un DEN alto cada vez, ≥ 1 ms y lectura del ADS1115.
- **Complejidad:** baja. Un solo firmware (el YAML de la placa); puesta en marcha: dirección por puentes y cable.

## 4. Arquitectura 2 · RS-485 / Modbus RTU

**Esquema:** en el módulo, MCU pequeño (WCH CH32V203C8T6, C3001172, 0,73 $; ADC de 12 bits, UART y CAN) + transceptor SP3485EN (C8963, Basic, 0,24 $) + PSM712 (C32677, ESD de RS-485) + buck de 65 V a 3,3 V (LMR36520ADDAR) + 8 BTT con IS por canal y DEN común. En la placa, el transceptor va en un adaptador enchufado en EXP-02: TX y RX por la matriz de GPIO en GPIO47/48 y DE en GPIO36; se alimenta del 5 V del conector con su propio regulador de 3,3 V (un transceptor que transmite sobre 54 Ω pasa de los 50 mA del pin de 3,3 V).

- **Distancia:** hasta 1200 m a ≤ 100 kb/s por par trenzado con terminación de 120 Ω, más GND (TIA-485).
- **Módulos:** direcciones Modbus 1–247; 32 cargas unidad por segmento con el SP3485.
- **Alimentación:** local (buck), nada por el conector salvo el adaptador.
- **Estado seguro:** lo pone el firmware del esclavo: si no recibe una trama válida en un tiempo, apaga salidas y limitador. Sin firmware que lo haga, el hardware no lo garantiza.
- **ESPHome:** en la placa, `uart` + `modbus` + `modbus_controller` (bobinas para IN, registros de entrada para IS). El esclavo no ejecuta ESPHome: firmware propio en C (Modbus RTU, mapa de registros, *watchdog*), con otra cadena de herramientas y programador (WCH-LinkE). ESPHome tiene `modbus_server`, pero solo en un ESP32, y entonces el módulo sería la arquitectura 4 con cable.
- **Comercial:** Waveshare Modbus RTU Relay 8CH (B), 7–36 V, 31,49 $ (Robotshop, 2026-11-15, según VAL-0006-01; la búsqueda del autor daba 37,95 $): relés de contacto seco, sin diagnóstico ni *high-side*.
- **Complejidad:** alta (segundo firmware, terminación, polarización del bus).

## 5. Arquitectura 3 · Registros de desplazamiento encadenados

**Esquema:** 2 × 74HC595D (C5947, Basic, 0,10 $) para IN1–8 y DEN1–8; SER, SRCLK y RCLK por GPIO47, 48 y 35 (matriz de GPIO). OE (activa a nivel bajo) con *pull-up* a 3,3 V y gobernada desde EXP_EN (GPIO36) **a través de un inversor**: un N-MOS de señal (p. ej. 2N7002) con la puerta en EXP_EN (que conserva su carga de ≥ 22 kΩ a GND) y el drenador en OE. EXP_EN bajo → N-MOS abierto → OE alto → salidas en alta impedancia. Mismo conector EXP-02; ≈ 0,02 $ más (no incluidos en §8 ni en `bom-expansion.csv`), que no cambian la comparación.

- **TPIC6B595 descartado:** salidas *low-side* de drenador abierto y 150 mA continuos (p. 1); no hace de *high-side* ni aguanta 0,66 A. Obligaría a otra topología de salida que la de DEC-0003.
- **Sin diagnóstico:** el 74HC595 solo escribe. No hay IS (REL-10) ni lectura de fallo, salvo añadir un 74HC165 y un comparador por canal, que lo acercan al coste de la arquitectura 1.
- **Distancia:** líneas CMOS sin protocolo ni comprobación: ≤ 1 m dentro de la caja. Un pulso de ruido en SRCLK desplaza todos los bits y puede encender otro canal hasta el siguiente refresco.
- **Módulos:** ESPHome admite `sr_count` hasta 256, sin direcciones.
- **Estado seguro:** en el reset de la placa, en el arranque o con el cable cortado, EXP_EN queda bajo (*pull-downs*), el inversor deja OE alto por su *pull-up* (lo pide la documentación de ESPHome) y las salidas del 74HC595 quedan en alta impedancia → R_PD → BTT apagados, sea cual sea el contenido aleatorio del registro. Además, EXP_EN bajo apaga el limitador del módulo. El firmware carga ceros en el registro antes de subir EXP_EN.
- **ESPHome:** `sn74hc595` (modo GPIO) sin `oe_pin`: OE se gobierna con el `switch` de EXP_EN (GPIO36) a través del inversor (EXP_EN alto = salidas habilitadas).
- **Comercial:** OpenSprinkler Zone Expander, 16 zonas a 24 V AC, 49–50 $ (opensprinkler.com, 2026-11-15).
- **Complejidad:** baja en firmware, pero sin diagnóstico ni detección de errores en el bus.

## 6. Arquitectura 4 · Segundo nodo ESP32 independiente

**Esquema:** una placa con ESP32-S3-WROOM-1-N8, buck de 65 V, TLV1117LV, USB-C, 8 BTT con IS por canal a ADC1 y DEN común, entrada de 24 V y limitador. Es, en la práctica, **otra placa ESP-Riego** (con 6 canales, ya diseñada) o una variante de 8 canales: ADC1 tiene 10 canales en GPIO1–10 (`mcu.md` §9.1).

- **Distancia:** la de la cobertura Wi-Fi; con ESP-NOW (`espnow`, `packet_transport`) los nodos hablan entre sí sin el router.
- **Módulos:** sin límite técnico; cada nodo es un dispositivo de Home Assistant.
- **Alimentación:** local, con su propia fuente.
- **Estado seguro:** firmware del nodo. ESPHome da `api: reboot_timeout` y `on_client_disconnected` para apagar si se pierde Home Assistant; REL-04 lo cumple su propio hardware (como la placa).
- **ESPHome:** nativo; un segundo YAML casi igual al de la placa. La coordinación entre nodos (que no rieguen a la vez si comparten fuente, secuencias) va en Home Assistant.
- **Comercial:** KinCony KC868-A8 (ESP32, 8 relés, «Made for ESPHome»), desde 55 $ (shop.kincony.com, 2026-11-15); relés, sin diagnóstico.
- **Complejidad:** baja en firmware; puesta en marcha de un segundo nodo Wi-Fi. No usa EXP-02.

## 7. Arquitectura 5 · CAN (referencia)

**Esquema:** CH32V203C8T6 (CAN integrado) + TJA1051T/3 (C38695, 0,46 $; V_IO para lógica de 3,3 V) + PESD2CAN (C75176) + buck de 3,3 V + 8 BTT. En la placa, el TWAI del ESP32-S3 por la matriz de GPIO (GPIO47/48) y el transceptor en un adaptador en EXP-02, alimentado con el 5 V del conector (≤ 70 mA en dominante).

- **Distancia y módulos:** del orden de 500 m a 125 kb/s y más de 100 nodos (cifras típicas de ISO 11898-2, no comprobadas en un datasheet porque es solo referencia).
- **Estado seguro:** firmware del esclavo (tiempo sin tramas).
- **ESPHome:** `canbus` con `esp32_can`; tramas propias en *lambdas* en la placa, y firmware propio en el esclavo.
- **Complejidad:** alta; no aporta nada frente a la arquitectura 2 para este uso.

## 8. Costes

**Hipótesis (iguales para las cinco):**

- Precios de JLCPCB del 2026-11-15, en el tramo de la cantidad real (piezas por módulo × módulos). Lista completa: `hardware/componentes/stock-expansion.csv`.
- JLCPCB *Economic PCBA*: 8,18 $ de preparación + 1,53 $ de plantilla por pedido, 3,07 $ por pieza Extended distinta (las «Extended preferidas» no pagan), 0,0016 $ por unión SMT. THT (bornes y cabeceras) soldado por el usuario (FAB-06); columna aparte con el THT de JLCPCB (3,58 $ por pedido + 0,0164 $ por unión).
- PCB de 2 capas ≤ 100 × 100 mm: 2 $ las 5 (oferta de JLCPCB) y 5 $ las 10 (**supuesto**, sin presupuesto). Sin envío, aranceles ni cupones (JLCPCB da cupones de montaje mensuales que pueden quitar los 8 $ de preparación).
- Todas llevan la misma entrada de 24 V (sin buck) y la misma etapa de salida (§2.1). Las 2, 4 y 5 llevan además el buck de 65 V; las 2 y 5 necesitan un adaptador en la placa (≈ 1–3 $ en piezas, no incluido).
- Lista de piezas de cada variante: `hardware/componentes/bom-expansion.csv` (con ella, Σ cantidad × módulos × precio del tramo da la columna «Piezas»). En el módulo, R_LED = 1,5 kΩ (C22843), por el presupuesto de §10.3.
- Sin merma de piezas. El fusible 0451010.MRL (C44479) tiene **stock 0 en JLCPCB** el 2026-11-15; su precio se usa igual (alternativa TA10, C2998199, 1 307).

| Arquitectura | Canales | Módulos | Piezas (pedido) | Extended distintas | Montaje | PCB | Total pedido | **Por módulo** | Por módulo con THT de JLCPCB |
|---|---|---|---|---|---|---|---|---|---|
| 1 · I²C | 8 | 5 / 10 | 99,76 / 187,60 | 13 | 52,80 / 55,99 | 2 / 5 | 154,56 / 248,59 | **30,91 / 24,86** | 32,25 / 25,84 |
| 1 · I²C | 6 | 5 / 10 | 86,62 / 161,84 | 13 | 52,28 / 54,93 | 2 / 5 | 140,89 / 221,77 | **28,18 / 22,18** | 29,45 / 23,09 |
| 2 · RS-485 | 8 | 5 / 10 | 100,95 / 191,86 | 13 | 53,40 / 57,17 | 2 / 5 | 156,35 / 254,03 | **31,27 / 25,40** | 32,35 / 26,12 |
| 2 · RS-485 | 6 | 5 / 10 | 89,08 / 165,76 | 13 | 52,80 / 55,99 | 2 / 5 | 143,88 / 226,75 | **28,78 / 22,67** | 29,79 / 23,33 |
| 3 · 74HC595 | 8 | 5 / 10 | 87,42 / 166,09 | 11 | 46,62 / 49,75 | 2 / 5 | 136,04 / 220,85 | **27,21 / 22,08** | 28,55 / 23,07 |
| 3 · 74HC595 | 6 | 5 / 10 | 74,28 / 140,33 | 11 | 46,09 / 48,70 | 2 / 5 | 122,36 / 194,03 | **24,47 / 19,40** | 25,75 / 20,32 |
| 4 · Nodo ESP32-S3 | 8 | 5 / 10 | 122,79 / 227,04 | 16 | 62,86 / 66,89 | 2 / 5 | 187,65 / 298,94 | **37,53 / 29,89** | 38,54 / 30,55 |
| 4 · Nodo ESP32-S3 | 6 | 5 / 10 | 109,47 / 200,94 | 16 | 62,27 / 65,71 | 2 / 5 | 173,74 / 271,65 | **34,75 / 27,17** | 35,69 / 27,75 |
| 5 · CAN | 8 | 5 / 10 | 101,21 / 191,43 | 15 | 59,52 / 63,28 | 2 / 5 | 162,73 / 259,71 | **32,55 / 25,97** | 33,62 / 26,69 |
| 5 · CAN | 6 | 5 / 10 | 89,34 / 165,33 | 15 | 58,93 / 62,10 | 2 / 5 | 150,26 / 232,42 | **30,05 / 23,24** | 31,06 / 23,90 |

Lectura:

- Los cargos de montaje (≈ 53 $ por pedido, sobre todo 13–16 piezas Extended a 3,07 $) pesan más que la diferencia entre arquitecturas. Con 10 módulos de 8 canales, frente a la arquitectura 3: +2,8 $ la 1 (TCA9535 + ADS1115), +3,3 $ la 2 y +3,9 $ la 5 (MCU, transceptor y buck, sin el adaptador) y +7,8 $ la 4 (ESP32-S3, USB y buck).
- Precios principales (tramo de 10 módulos): BTT6050 1,09 $ × 80 (stock 1 624: con 10 placas y 10 módulos se gastan 140), TPS26632 3,00 $ (stock 1 240), SQD50P06 0,98 $, TCA9535 1,22 $, ADS1115 1,13 $, ESP32-S3-WROOM-1-N8 4,25 $.
- Si el módulo se encarga en el mismo pedido que la placa, las líneas Extended comunes (BTT6050, TPS26632, bornes…) no se pagan dos veces.

**Comparación con módulos comerciales** (precios de venta al público, consulta del 2026-11-15):

| Producto | Canales | Precio | Diferencias |
|---|---|---|---|
| Hunter PCM-300 (para Pro-C) | 3, 24 V AC | 35–63 $ | Solo para su programador; triacs de 24 V AC |
| OpenSprinkler Zone Expander | 16, 24 V AC (o DC según versión) | 49–50 $ | Solo para OpenSprinkler |
| Waveshare Modbus RTU Relay 8CH (B) | 8 relés | 31,49 $ | Contacto seco: necesita cableado de 24 V aparte; sin diagnóstico |
| KinCony KC868-A8 | 8 relés, ESP32 | desde 55 $ | ESPHome; relés, sin diagnóstico ni limitador |

El módulo propio de 8 canales cuesta 24,9 $ con 10 uds, menos que cualquiera de ellos; con 5 uds (30,9 $) cuesta casi lo mismo que el Waveshare (31,49 $). Es el único con diagnóstico por canal y limitador (REL-10, ALI-13).

## 9. Recomendación

**Propuesta: arquitectura 1 (I²C, TCA9535 + ADS1115), en la misma caja o en una contigua, con ≤ 3 m de cable plano.**

1. Es la más barata de las que conservan el diagnóstico de REL-10 (24,9 $ por módulo de 8 canales con 10 uds).
2. Todo va en el YAML de la placa con componentes de ESPHome (`pca9554`, `ads1115`): no hay segundo firmware.
3. El estado seguro es de hardware: *pull-downs* en IN y DEN, POR del expansor a entradas y EXP_EN con *pull-down* en los dos lados (REL-04 se extiende al módulo).
4. Usa exactamente los pines que ya reserva la hoja MCU y deja los cuatro libres para EXP-03.

**Alternativa: arquitectura 4 (nodo ESP32-S3 propio)**, si el módulo va lejos (> 3 m) o en otra caja con su fuente: +5 $ por módulo con 10 uds (+6,6 $ con 5), sin cable de datos, ESPHome nativo; el estado seguro depende de su firmware. La versión de 6 canales es otra placa ESP-Riego v2 sin diseño nuevo.

Descartadas como propuesta: la 3 (sin diagnóstico, bus sin comprobación), la 2 y la 5 (segundo firmware fuera de ESPHome y adaptador, sin ventaja de coste). Para distancias de 3–50 m con la arquitectura 1, un par de P82B715 (§3), sin cambiar EXP-02.

## 10. Definición del conector EXP-02 (para SPEC-0031)

### 10.1 Tipo

| Campo | Valor |
|---|---|
| Familia | Cabecera IDC con guía (*box header*), recta, para cable plano de 1,27 mm |
| Paso, polos | 2,54 mm, 2 × 5 = 10 polos |
| Montaje | THT, cara superior (FAB-06), en el borde inferior junto a la entrada y los bornes 4–6 (FAB-07) |
| Polarización | Guía con ranura de 4,5 mm en el lado largo y triángulo en el pin 1 (BH254V p. 1). La ranura mira hacia el exterior de la placa, para que el cable salga por el borde |
| Bloqueo | **Sin enclavamiento positivo**: retención por fricción del conector IDC; se fija el cable con una brida a la caja. Las versiones con expulsores (*ejector*) no tienen stock en JLCPCB (Würth 61201021721: 0; BOOMELE C61102: 28). Si el usuario exige enclavamiento, la opción es Molex Micro-Fit 3.0 2 × 5 recta (43045-1012, C277725, 5 955 en JLCPCB), con otra numeración de pines y cable crimpado |
| Principal | XFCN BH254V-10P · **C492442** · Extended · **28 794** en JLCPCB (2026-11-15) · 0,12 $. 3 A por contacto, −40…105 °C, 600 V AC, PBT UL94 V-0 (BH254V p. 1). Cotas 2 × 5: A = 10,16 mm, B = 20,35 mm, ancho 8,9 mm, alto 9,05 mm, taladro Ø 1,02 mm (p. 1) |
| Alternativa | Würth 61201021621 (WR-BHD) · C4355000 · 1 243 · 0,64 $ |
| Huella y símbolo | `Connector_IDC:IDC-Header_2x05_P2.54mm_Vertical` (oficial) y `Connector_Generic:Conn_02x05_Odd_Even`; SPEC-0031 contrasta la huella con la p. 1 |
| Cable | Plano de 10 hilos, 28 AWG (3M 3365/10 o equivalente; G-S-G 47,5 pF/m, TS-0080 p. 1; −20…105 °C), con dos conectores IDC hembra de 10 polos. ≤ 3 m en total |

### 10.2 Pines

Orden pensado para el cable plano: cada línea de I²C va entre dos GND y las alimentaciones junto a un GND. Las resistencias en serie y los *pull-ups* van en la placa, con los *pull-ups* del lado del conector y la ESD pegada al conector.

| Pin | Señal | GPIO | Dir. (vista desde la placa) | Tensión | Corriente | En la placa, del MCU al conector | ESD |
|---|---|---|---|---|---|---|---|
| 1 | +5V_EXP | — | Salida | +5V tras el interruptor: 4,83–5,11 V con el buck; ≥ 4,33 V con USB | **≤ 0,30 A** (límite del interruptor 343–439 mA) | TPS2553DBVR (U_A) desde +5V, EN (activo alto, p. 4) unido a su IN: siempre habilitado; R_ILIM 68 kΩ; C_IN 100 nF, C_OUT 4,7 µF | U_EXP2 pin 5 (VBUS) |
| 2 | GND | — | — | 0 V | retorno | Plano | — |
| 3 | +3V3_EXP | — | Salida | 3,20–3,39 V | **≤ 50 mA** (límite 104–146 mA) | TPS2553DBVR (U_B) desde +3V3, EN unido a su IN; R_ILIM **220 kΩ**; C_IN 100 nF, C_OUT 1 µF | U_EXP1 pin 5 (VBUS) |
| 4 | GND | — | — | 0 V | retorno | Plano | — |
| 5 | I2C_EXP_SDA | **47** | E/S, drenador abierto | 0–3,39 V | ≤ 3 mA (1,55 mA con 2,2 kΩ) | 100 Ω en serie; 2,2 kΩ a +3V3_EXP | U_EXP1 I/O1 (1↔6) |
| 6 | GND | — | — | 0 V | — | Plano | — |
| 7 | I2C_EXP_SCL | **48** | Salida, drenador abierto | 0–3,39 V | ≤ 3 mA | 100 Ω en serie; 2,2 kΩ a +3V3_EXP | U_EXP1 I/O2 (3↔4) |
| 8 | GND | — | — | 0 V | — | Plano | — |
| 9 | EXP_INT | **35** | Entrada, activa baja; drenador abierto en los módulos (INT del expansor y FLT del limitador) y FAULT de U_A y U_B | 0–3,39 V | ≤ 0,35 mA | 470 Ω en serie; 10 kΩ a +3V3 **en el lado del MCU** de la de 470 Ω, donde se unen también los FAULT de U_A y U_B | U_EXP2 I/O1 (1↔6) |
| 10 | EXP_EN (antes EXP_IO2) | **36** | Salida, activa alta: habilita el limitador de los módulos | 0 / ≥ 2,4 V en el módulo | ≤ 0,5 mA (4 módulos) | 470 Ω en serie; **100 kΩ a GND en el lado del MCU** (REL-04) | U_EXP2 I/O2 (3↔4) |

- **GPIO:** los cuatro de `mcu.md` §9.2, sin cambios de número. EXP_IO2 pasa a llamarse **EXP_EN** y se fija como salida (GPIO36: alta impedancia en el reset y el flasheo, sin pulsos altos, `mcu.md` §9.1: apto para salidas). No se usa ningún pin libre: **GPIO10, 18, 37 y 39 quedan para los pulsadores de EXP-03** (escalera en GPIO10 o INT de un expansor de la placa).
- **Uso por arquitectura:** 1 → tal cual. 3 → SER, SRCLK y RCLK en los pines 5, 7 y 9 (GPIO47, 48 y 35 por la matriz de GPIO; con 2,2 kΩ a 3,3 V las líneas siguen en reposo alto) y EXP_EN (pin 10) a la OE de los 74HC595 a través de un inversor en el módulo (§5). 2 y 5 → adaptador en EXP-02: TX/RX en 47/48, DE en 36 (RS-485), o TWAI en 47/48 con el transceptor a 5 V. 4 → no lo usa.
- **Requisitos para el módulo** (los fija este conector): carga en EXP_EN ≥ 22 kΩ a GND por módulo (con el TPS26632: 10 µA × 22 kΩ = 0,22 V < 0,8 V, apagado; TPS2663 p. 7); sin *pull-ups* propios en SDA/SCL; ≤ 30 pF por línea de I²C; ESD propia en su conector.

### 10.3 Alimentación (EXP-02 frente a `alimentacion.md` §4 y ALI-12)

| Comprobación | Cálculo | Resultado |
|---|---|---|
| Carga de un módulo de la arquitectura 1 en +3V3_EXP | TCA9535 ≤ 40 µA (p. 7) + ADS1115 ≤ 0,3 mA (p. 6) + 8 LED de canal a 1 mA (R_LED 1,5 kΩ en el módulo) + 16 R_PD × 33 µA + 8 × 25 µA de IN = 9,1 mA por módulo; *pull-ups* de I²C 2 × 1,55 mA una vez | 1 módulo: **12,2 mA**; 4 módulos: 4 × 9,1 + 3,1 = **39,5 mA ≤ 50 mA** ✔. Requisito para el módulo: ≤ 9,5 mA en +3V3_EXP |
| +5V_EXP | Arquitectura 1: 0 mA. Adaptador CAN: ≤ 70 mA | ≤ 0,30 A ✔ |
| ALI-12 | El presupuesto de `alimentacion.md` §4 ya cuenta 50 mA y 0,30 A: 4,32 W ≤ 4,8 W | **Sin cambio** ✔ |
| Interruptor de 5 V (U_A) | I_OS mín. = 25 230 / (68 × 1,01)^1,016 = 343 mA ≥ 300 mA (+14 %); máx. = 22 980 / (68 × 0,99)^0,94 = 439 mA (ec. 2-3 y la de máximo, pp. 17 y 20; R al 1 %). Caída: 0,15 Ω × 0,3 A = 45 mV (p. 6) | ✔ |
| Interruptor de 3,3 V (U_B) | R_ILIM 220 kΩ (C22961, Basic): I_OS mín. = 25 230 / (220 × 1,01)^1,016 = 104 mA ≥ 50 mA (2,1×); máx. = 22 980 / (220 × 0,99)^0,94 = 146 mA (210 kΩ da 110–150 mA en la tabla de la p. 7). Dentro de 15–232 kΩ (p. 16). V_IN 3,3 V dentro de 2,5–6,5 V (p. 6); UVLO 2,35 V (p. 7) | ✔ |
| Corto en el cable (los dos raíles a la vez) | +3V3: 0,40 + 0,146 = 0,546 A; +5V: 0,546 + 0,439 = 0,985 A → 5 × 0,985 / 0,88 + 0,05 = 5,65 W = 0,235 A a 24 V; con el limitador de la placa en su máximo, 4,57 + 0,235 = **4,81 A < 5,14 A** (margen 0,33 A) | ✔ La fuente no actúa; la lógica no se reinicia. La lógica pasa de 4,8 W solo durante el fallo |
| TLV1117LV durante el corto, peor caso con USB a 5,25 V (como `mcu.md` §8.3) | (5,25 − 0,03 − 3,3) × 0,546 = 1,05 W × 60 °C/W → T_J = **122,9 °C** < 125 °C (con el buck: 0,99 W → 119,2 °C) | ✔, margen 2,1 K, solo en fallo: U_B entra en apagado térmico cíclico (3,3 V × 0,146 A × 182,6 °C/W = +88 °C → 135 °C, p. 16), así que la media es menor. Con los 200 kΩ de la primera versión salían 124,4 °C; 232 kΩ daría 122,1 °C, pero es Extended (C22913) y gana solo 0,8 K. **Prueba en el prototipo:** corto de +3V3_EXP con USB, temperatura de U4 |
| Sin cable | U_A y U_B con salida en vacío; EXP_INT a nivel alto por su *pull-up*; EXP_EN con 100 kΩ | ✔ |

- Los FAULT de U_A y U_B (drenador abierto, p. 4) se unen a EXP_INT: el firmware distingue el corto en el cable (FAULT con los módulos sin fallo) leyendo el FLT del módulo por I²C. FAULT tiene un filtro de 7,5 ms (p. 7) y puede marcar en el arranque: el firmware ignora EXP_INT el primer segundo.
- Las dos funciones del TPS2553 son una línea Extended nueva (TPS2553DBVR, C55266, 48 302, 0,46 $). Las R_ILIM son Basic: 68 kΩ C23231 y 220 kΩ C22961.

### 10.4 *Pull-ups*, capacidad del bus y extensor

Ecuaciones (TCA9535 §7.2.2, p. 27): R_P(mín) = (V_CC − V_OL) / I_OL; R_P(máx) = t_r / (0,8473 · C_b). t_r ≤ 1000 ns en modo estándar (100 kHz) y ≤ 300 ns en rápido (TCA9535 p. 8). C_b ≤ 400 pF.

| Elemento por línea | C | Fuente |
|---|---|---|
| ESP32-S3 + pista en la placa | 10 pF | **supuesto** (el datasheet no da la capacidad del pin) |
| USBLC6 en la placa | 3,5 pF máx. | USBLC6 tabla 2, p. 2 |
| Cable plano G-S-G | 47,5 pF/m | 3M TS-0080 p. 1 |
| Conectores | 1 pF por conector | supuesto |
| Módulo: USBLC6 + TCA9535 (SDA 9,5 pF, p. 8) + ADS1115 (10 pF, supuesto) + pista 5 pF | 28 pF | — |

| Caso | C_b | t_r con 2,2 kΩ + 1 % | Resultado |
|---|---|---|---|
| 1 módulo, 1 m | 13,5 + 47,5 + 2 + 28 = **91 pF** | 0,8473 × 2222 × 91 pF = **171 ns** | ✔ estándar y rápido |
| 4 módulos, 3 m en total | 13,5 + 142,5 + 8 + 112 = **276 pF** | **520 ns** | ✔ estándar (≤ 1000 ns); ✗ rápido |
| Cable de 100 pF/m (no plano), 1 módulo, 3 m | 343 pF | 646 ns | ✔ estándar |

- **R_P = 2,2 kΩ ± 1 % (C4190, Basic), definitiva**, a +3V3_EXP, una por línea y solo en la placa. R_P(mín) = (3,39 − 0,4) / 3 mA = 1,0 kΩ ≤ 2,18 kΩ ✔ (I_OL 3 mA a 0,4 V en SDA, TCA9535 p. 7). Corriente a nivel bajo: 1,55 mA (ya contada en `mcu.md` §8.2).
- **Velocidad: 100 kHz** (`mcu.md` Anexo B, `bus_exp`). 400 kHz solo con un módulo y ≤ 1 m.
- **Margen de ruido, en los dos sentidos** (los *pull-ups* están en el lado del conector de la de 100 Ω):
  - transmite el ESP32: su corriente de bajada atraviesa la de 100 Ω. En el módulo, V_OL ≤ 0,1 × V_DD = 0,34 V (ESP32-S3 tabla 5-4) + 1,55 mA × 100 Ω = 0,49 V frente a V_IL del TCA9535 = 0,3 × V_CC = 0,96 V con 3,20 V (p. 6): **margen 0,47 V**;
  - responde el módulo: V_OL del TCA9535 ≤ 0,4 V a 3 mA (p. 7). El pin del ESP32 es entrada y no circula corriente por la de 100 Ω, así que ve 0,4 V frente a V_IL = 0,25 × V_DD = 0,80 V (tabla 5-4): **margen 0,40 V**. Si los *pull-ups* se pusieran en el lado del MCU, la corriente pasaría por la de 100 Ω y el margen bajaría a 0,80 − 0,555 = 0,25 V: SPEC-0031 los deja en el lado del conector;
  - los 29 mV de desplazamiento de masa de §2.2 caben en los dos.
- **4.º módulo (ADS1115 con ADDR = SDA):** el ADS1115 exige entonces SDA bajo ≥ 100 ns después de la bajada de SCL (SBAS444E p. 20). Con 3 módulos (ADDR a GND, VDD y SCL) no hay condición. El 4.º se admite solo si el prototipo comprueba ese tiempo de mantenimiento con el controlador I²C del ESP32-S3; si no, el máximo es 3 × 8 canales.
- **Extensor:** no hace falta hasta 3 m. Para más distancia, un par de P82B715 (§3) en adaptadores, ninguno en la placa principal.

### 10.5 ESD

| Pieza | Líneas | Tensión de trabajo | Capacidad | Nivel IEC 61000-4-2 | Fuente |
|---|---|---|---|---|---|
| **U_EXP1: ST USBLC6-2SC6** (C7519, línea de U6, 39 134 en JLCPCB el 2026-11-15) | SDA (I/O1), SCL (I/O2); VBUS = +3V3_EXP | I_RM ≤ 150 nA a V_RM = 5,25 V ≥ 3,39 V | ≤ 3,5 pF I/O–GND (2,5 típ.) | Nivel 4: ± 8 kV contacto, ± 15 kV aire | p. 1; tabla 2, p. 2 |
| **U_EXP2: ST USBLC6-2SC6** (C7519) | EXP_INT (I/O1), EXP_EN (I/O2); VBUS = +5V_EXP | V_RM 5,25 V ≥ 5,25 V (máximo de +5V con USB; 5,107 V con el buck) | ≤ 3,5 pF | Nivel 4 | p. 1–2 |
| Alimentaciones | +3V3_EXP y +5V_EXP, por el zéner VBUS–GND de U_EXP1 y U_EXP2 (V_BR ≥ 6 V a 1 mA, p. 2) y la capacidad de salida de U_A y U_B | — | — | El TPS2553 pasa ± 8 kV de contacto en la salida de su placa de evaluación (p. 5, nota 3) | — |

- **Capacidad frente al tiempo de subida:** 3,5 pF por línea en cada extremo, incluidos en §10.4: son 7 de los 91 pF del caso de 1 m (≈ 8 % de t_r).
- *Clamping* 12 V a 1 A y 17 V a 5 A (8/20 µs, p. 2). Las resistencias en serie limitan la corriente residual hacia el ESP32: en INT y EN, (5,25 + 1,1 − 3,6) V / 470 Ω ≈ 6 mA; en SDA y SCL, 100 Ω (no se sube más: 100 Ω × 1,55 mA = 0,155 V ya entran en el margen de §10.4).
- Si U_A corta el 5 V, EXP_INT y EXP_EN quedan a ≈ 0,6 V por los diodos de U_EXP2 hacia +5V_EXP: el limitador del módulo se apaga (estado seguro), EXP_INT marca fallo y GPIO36 entrega ≤ (3,39 − 0,6) / 470 Ω = 6 mA. Lo mismo con SDA y SCL si cae +3V3_EXP: el bus de expansión se queda bajo, sin tocar el del SHT4x.
- Una sola línea Extended para la ESD (la de U6); alternativa con un solo encapsulado para las cuatro líneas: Semtech SRV05-4 (C13612, 59 734), que sería una línea nueva.

### 10.6 Lista de piezas para SPEC-0031 (lado de la placa)

Referencias provisionales: SPEC-0031 asigna las definitivas.

| Ref. | Valor / función | Encapsulado | MPN | LCSC · tipo · stock JLCPCB (2026-11-15) | Alternativa |
|---|---|---|---|---|---|
| J_EXP | Cabecera 2 × 5, 2,54 mm, recta | THT | XFCN BH254V-10P | C492442 · Extended · 28 794 | Würth 61201021621 (C4355000) |
| U_EXP1, U_EXP2 | ESD, 2 líneas + VBUS | SOT-23-6 | ST USBLC6-2SC6 | C7519 · Extended (línea de U6) · 39 134 | Semtech SRV05-4 (C13612), las 4 líneas en uno |
| U_A, U_B | Interruptor con límite de corriente, 5 V y 3,3 V | SOT-23-6 | TI TPS2553DBVR | C55266 · Extended · 48 302 | — (la variante -1 se enclava; no se quiere) |
| R_ILIM_A | 68 kΩ 1 % | 0603 | 0603WAF6802T5E | C23231 · Basic | — |
| R_ILIM_B | 220 kΩ 1 % | 0603 | 0603WAF2203T5E | C22961 · Basic | 232 kΩ C22913 (Extended) |
| C (×2) | C_IN de U_A y U_B, 100 nF | 0603 | CC0603KRX7R9BB104 | C14663 · Basic | — |
| C | C_OUT de U_A, 4,7 µF | 0603 | CL10A475KO8NNNC | C19666 · Basic (línea de C26) | — |
| C | C_OUT de U_B, 1 µF | 0603 | CL10A105KB8NNNC | C15849 · Basic | — |
| R (×2) | *Pull-ups* de SDA y SCL, 2,2 kΩ 1 % | 0603 | 0603WAF2201T5E | C4190 · Basic | — |
| R (×2) | Serie de SDA y SCL, 100 Ω 1 % | 0603 | 0603WAF1000T5E | C22775 · Basic | — |
| R (×2) | Serie de EXP_INT y EXP_EN, 470 Ω 1 % | 0603 | 0603WAF4700T5E | C23179 · Basic (línea de R22) | — |
| R | *Pull-up* de EXP_INT, 10 kΩ | 0603 | 0603WAF1002T5E | C25804 · Basic | — |
| R | *Pull-down* de EXP_EN, 100 kΩ | 0603 | 0603WAF1003T5E | C25803 · Basic | — |

- **Coste añadido a la placa:** ≈ 1,4 $ en piezas más 3,07 $ por pedido de la línea TPS2553: ≈ 2,0 $ por placa con 5 y ≈ 1,7 $ con 10.
- **Conexiones de los TPS2553 en la hoja:** EN de U_A y U_B (activo alto en el TPS2553, p. 4) unido a su IN: siempre habilitados, sin GPIO. FAULT de U_A y U_B (drenador abierto) unidos a EXP_INT en el **lado del MCU** de la de 470 Ω, en el mismo nodo que el *pull-up* de 10 kΩ; así no pasan por la ESD ni por el cable.
- **Cambios que SPEC-0031 lleva a `mcu.md`:**
  - §9.2: columna «Elemento externo» de GPIO35, 36, 47 y 48 con esta tabla; GPIO36 pasa a EXP_EN, salida activa alta;
  - §10.1: EXP_EN entra en la tabla de estado seguro junto a IN1–6, OUT_DEN y LIM_EN (Z en el reset y el flasheo; en OTA y `esp_restart()` lo cubre el firmware) y es la barrera del módulo;
  - §10.2: fila nueva «EXP_EN | R_PD = 100 kΩ 1 % (C25803) del GPIO a GND, en el lado del MCU de la de 470 Ω | Conectores | Pin en Z: 50 nA × 100 kΩ = 5 mV < 0,8 V; con el GPIO alto y 4 módulos de 22 kΩ, 2,43 V en el módulo ≥ 2,0 V (§10.2 de este informe)»;
  - Anexo B: EXP_EN como `output` con `restore_mode: ALWAYS_OFF`, a bajo en `on_boot` (prioridad alta), `ota: on_begin` y `on_shutdown`, igual que LIM_EN. Antes de un OTA o de un reinicio, escribir 0 en las salidas del TCA9535 (o del 74HC595) y después bajar EXP_EN; al arrancar, escribir 0 en el expansor antes de subir EXP_EN. Con EXP_EN alto tras un reset de CPU, el TCA9535 conservaría sus salidas y el limitador del módulo seguiría habilitado;
  - §14.2 se cierra. El presupuesto de §8.2 no cambia.

### 10.7 Restricciones de layout (para `restricciones.csv`, fase 4)

| Red | Corriente | Ancho mín. | Separación | Ubicación / keepout | Notas |
|---|---|---|---|---|---|
| +5V_EXP | 0,44 A (límite) | 0,3 mm | 0,2 mm | U_A junto a J_EXP | `Default` vale (FAB-03) |
| +3V3_EXP | 0,15 A (límite) | 0,25 mm | 0,2 mm | U_B junto a J_EXP | — |
| I2C_EXP_SDA / SCL | 3 mA | 0,2 mm | ≥ 0,5 mm a redes de 24 V | U_EXP1 a ≤ 5 mm de J_EXP; pistas cortas sobre plano de GND continuo | Lejos de `Salidas` y de los nodos conmutados del buck |
| EXP_INT / EXP_EN | < 1 mA | 0,2 mm | 0,2 mm | U_EXP2 a ≤ 5 mm de J_EXP | — |
| GND de J_EXP | 0,35 A | — | — | Cada pin GND con su vía al plano | Retorno de la lógica, no de potencia |
| J_EXP | — | — | — | Borde inferior, entre la entrada J1 y los bornes 4–6 (FAB-07); la ranura de la guía hacia el borde | Que la brida del cable no tape los bornes |

## 11. Fuentes (consulta del 2026-11-15)

- JLCPCB: API `selectSmtComponentList` (precios y stock, `hardware/componentes/stock-expansion.csv`); tarifas de montaje: <https://jlcpcb.com/help/article/pcb-assembly-price> (actualizado el 2026-10-22); oferta de PCB y cupones: <https://jlcpcb.com/blog/free-assembly-for-1-6-layer-pcbs-and-discounts-on-8-20-layer-pcba>.
- ESPHome: <https://esphome.io/components/> (lista de expansores, ADC, Modbus, CAN y ESP-NOW), <https://esphome.io/components/pca9554/>, <https://esphome.io/components/tca9555/>, <https://esphome.io/components/mcp230xx/>, <https://esphome.io/components/sn74hc595/>.
- Comerciales: Hunter PCM-300 <https://smartsprinklergenius.com/products/hunter-plug-in-expansion-module-pcm-300-for-pro-c-hpc-3-station> y <https://www.sprinklersupplystore.com/products/hunter-3-sta-module-for-pro-c-cntrl>; OpenSprinkler <https://opensprinkler.com/product/zone-expander/>; Waveshare <https://www.robotshop.com/products/waveshare-industrial-modbus-rtu-8-ch-relay-module-b-w-rs485-interface-736v-power-supply>; KinCony <https://shop.kincony.com/collections/kc868-ax>.
- Cable: 3M 3365, TS-0080-15 (<https://www.farnell.com/datasheets/190363.pdf>).

## 12. Riesgos y puntos abiertos

1. **Fuente propia del módulo:** requisito nuevo (PENDIENTE 1). Sin él, la arquitectura no cumple ALI-12 con una sola fuente de 5 A.
2. **Corriente de las válvulas** (DEC-0011): fija R_ILIM y la fuente del módulo (§2.3).
3. **TCA9535 en ESPHome:** «debería funcionar» (registros iguales que el PCA9535 probado). El primer prototipo lo comprueba; si falla, PCA9535PWR en la misma huella.
4. **4.º módulo:** depende del tiempo de mantenimiento de SDA con ADDR = SDA (§10.4).
5. **Capacidad del pin del ESP32-S3 y del ADS1115:** supuestas (10 pF). Con el doble (20 pF cada una), el caso de 4 módulos y 3 m sube a 326 pF y 614 ns, todavía ≤ 1000 ns.
6. **TLV1117LV con el cable en corto:** 122,9 °C con USB a 5,25 V (§10.3), margen de 2,1 K, solo en fallo.
7. **Stock:** fusible 0451010.MRL a 0 en JLCPCB (afecta también a F1 de la placa); TPS26632 baja de 1 631 a 1 240; BTT6050 1 624.
