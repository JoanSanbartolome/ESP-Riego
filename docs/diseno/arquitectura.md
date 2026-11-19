# Arquitectura de la placa v2: bloques, presupuesto por raíl, GPIO y revisión global (SPEC-0032)

**Estado:** propuesta para validación. **Autor:** ing-diseno · **Fecha:** 2026-11-19. Es el `docs/04-arquitectura.md` de `docs/03-plan-de-diseno.md` (fase 2), en la zona de ing-diseno.
**Requisitos:** KIC-02, KIC-03, KIC-06, ALI-11, ALI-12, ALI-13, MCU-05, REL-04, REL-11, FAB-05 y FW-02 de `docs/02` v0.8; DEC-0014 y DEC-0015.
**Fuentes:** netlist de `hardware/v2` (`kicad-cli sch export netlist`, 197 piezas, 165 redes, 2026-11-19); `docs/diseno/<bloque>.md`; datasheets de `hardware/componentes/datasheets/` (páginas del PDF).

## 0. Resumen

**Decisiones**

- Cinco hojas por bloque bajo la raíz (KIC-02): Alimentacion, MCU, Salidas (con la subhoja Canal repetida 6 veces), Conectores y Sensores; 12 páginas en el orden del árbol (`hoja.py paginas`, código 0).
- Raíz con el estilo de DEC-0015: las hojas unidas por cables dentro de un recuadro con título, una etiqueta local por red sobre su cable (conserva los nombres de red `/VBUS`, `/IN1`… de la PCB), cifras clave junto a cada hoja y 3 líneas de nota. Flujo de izquierda a derecha: entrada y campo (Alimentacion, Conectores, Sensores) → MCU → Salidas.
- Netlist idéntica a la de `main` al abrir la spec, por grupos de pines y por nombre de red (0 diferencias): la revisión global no cambia el circuito. La PCB no se resincroniza (paridad 0).
- Presupuesto (§2): la lógica consume **4,32 W ≤ 4,8 W** en la entrada con el 5 V de la expansión a 0,30 A; la entrada llega a **4,77 A ≤ 5,1 A** con el limitador en su máximo. 3,3 V: 0,42 A (diseño 0,45 A) frente a 1 A de U4; 5 V: 0,72 A (diseño 0,75 A) frente a 2 A de U2.
- GPIO (§3): 30 de 36 conectados, 25 de función más BOOT, USB y UART; las 8 analógicas en ADC1; ninguna salida en 0, 3, 45 o 46; GPIO19/20 solo al USB. La tabla sale de la netlist pin a pin y coincide con `mcu.md` §9.2.
- Revisión global (§4): pines de arranque, estado seguro (REL-04), polaridades, ESD de los conectores de campo y test points, sin defectos. Dos observaciones sin cambio de circuito (§4.6).

**Piezas principales por bloque** (lista completa en cada `docs/diseno/<bloque>.md`; BOM con coste en `fabricacion/v2.0-sch/bom.csv`, de jr-conformidad)

| Bloque | Piezas | Documento |
|---|---|---|
| Alimentacion | J1, F1 0451010.MRL, Q1 SQD50P06-15L + D1, D2 SMBJ33A, U1 TPS26632RGER + JP1, D3 SS310, U2 LMR36520FADDAR + L1, U3 TPS2116DRLR, U4 TLV1117LV33DCYR, TP1–TP5 | `alimentacion.md` §7 |
| MCU | U5 ESP32-S3-WROOM-1-N8, J2 USB-C + U6 USBLC6-2SC6, SW1/SW2, J3 UART, D5 | `mcu.md` §11 |
| Salidas (6 × Canal) | U7–U12 BTT6050-1ERA, J4–J9 WJ500V-5.08-2P, D12–D17 M7 (montados), R_OL, R_SENSE/R_IS/C_IS, R_PD, LED D6–D11 | `salidas.md` §9 |
| Conectores | J10 BH254V-10P, U14/U15 TPS2553DBVR, U16/U17 USBLC6-2SC6, U18 TCA9554PWR + SW3–SW8, H1–H4 | `conectores.md` §0 |
| Sensores | U13 SHT40-AD1B-R2 | `sensores.md` §10 |

**Restricciones de layout por raíl** (el detalle por red está en el §8 de `alimentacion.md`, el §11 de `salidas.md` y el §12 de `mcu.md`; aquí solo lo que cruza bloques)

| Red | Corriente | Ancho mín. | Separación | Ubicación / keepout | Notas |
|---|---|---|---|---|---|
| VIN_RAW, VIN_F, VIN_PROT | 5,1 A continuos | 2,0 mm o polígono | ≥ 0,6 mm | J1 → F1 → Q1 → D2 en línea en el borde inferior | `Power_In` (FAB-03) |
| BUS_24V | 4,57 A (4,9 A como dato de REL-05) | 2,0 mm o polígono | ≥ 0,6 mm | De U1 a los dos grupos de 3 BTT; C45/C46 a la entrada de cada grupo | `Power_In` |
| OUT_n | 1 A; 4,9 A sin daño | 1,2 mm | ≥ 1 mm; 0,6 mm en las huellas de U7–U12, R57–R62 y C33–C38 | BTT a ≤ 15 mm de su borne | `Salidas` (DEC-0008) |
| +5V, +5V_BUCK, VBUS | 0,75 A | 0,6 mm | 0,2 mm | — | `Power` |
| +3V3 | 0,45 A | 0,5 mm | 0,2 mm | U4 con ≥ 4 cm² de cobre en la pestaña | — |
| GND | 5,1 A de entrada; 4,9 A por retorno de borne | Plano | — | Plano continuo bajo las analógicas (FAB-04) | Retornos de J4–J9 según FAB-03 |
| Antena de U5 | — | — | Keepout en todas las capas | U5 en una esquina, antena fuera del borde lateral; ≥ 15 mm al buck, BTT y SHT40 | MCU-02 |

## 1. Diagrama de bloques

```
                         ┌──────────────────────────── Alimentacion ─────────────────────────────┐
 J1 24 V ── F1 ── Q1 ── VIN_PROT ─┬─ D2 TVS                                                       │
 (campo)       (polaridad)        ├─ U2 buck 5 V ── +5V_BUCK ─┐                                   │
                                  │                           U3 ── +5V ─┬─ U4 LDO ── +3V3 ──┐    │
 J2 USB-C ── U6 ESD ── VBUS ──────┼───────────────────────────┘          │                   │    │
                                  └─ U1 limitador (JP1) ── BUS_24V ──┐   │                   │    │
                         └───────────────────────────────────────────┼───┼───────────────────┼────┘
                                                                     │   │                   │
 Salidas: 6 × Canal ── U7–U12 BTT6050 ◄─ BUS_24V ◄───────────────────┘   │                   ├─ U5 ESP32-S3 (MCU)
          OUT_n ── C_OUT, D12–D17 ── J4–J9 (campo)                       │                   ├─ U13 SHT40 (Sensores)
                                                                         │                   ├─ U18 TCA9554 + SW3–SW8
 Conectores: J10 (campo) ── U16/U17 ESD ◄── +5V_EXP ◄─ U14 ◄─────────────┘                   │
                                        ◄── +3V3_EXP ◄─ U15 ◄────────────────────────────────┘

 Señales entre hojas (raíz):  U5 → IN1–IN6, OUT_DEN → BTT      BTT IS → IS1–IS6 → U5 (ADC1)
                              U5 → LIM_EN → U1                 U1 → LIM_FLT, LIM_IMON; VIN_SENSE → U5
                              U5 ↔ I2C_SDA/SCL ↔ U13, U18      U5 ↔ I2C_EXP_SDA/SCL, EXP_INT, EXP_EN ↔ J10
                              U18 → BTN_INT → U5               U5 → VBUS ← J2 (VBUS sube a Alimentacion)
```

La raíz dibuja lo mismo (imagen en el parte): 26 redes entre hojas y 54 pines de hoja; `+5V`, `+3V3` y `GND` no pasan por ella porque son símbolos `power` globales; el bus de 24 V sí (BUS_24V, de Alimentacion a Salidas).

## 2. Presupuesto de potencia por raíl (6 salidas activas, ALI-12)

### 2.1 Raíl de 3,3 V (U4 TLV1117LV33)

| Carga | Corriente | Fuente |
|---|---|---|
| U5, pico de TX 802.11b a 20,5 dBm, 100 % de ciclo | 355 mA | WROOM-1 tabla 6-4, p. 28 |
| U13 SHT40 midiendo (calentador sin usar, AMB-02) | 0,5 mA | SHT4x p. 9 |
| U18 TCA9554 en reposo con las E/S a GND (pulsadores apretados) | ≤ 0,6 mA | TCA9554 p. 7 (I_CC, V_I = GND, 3,6 V, máx.) |
| U15 TPS2553 (+3V3_EXP), habilitado | ≤ 0,13 mA | SLVS841G p. 6 (I_IN_on, R_ILIM = 210 kΩ, máx.) |
| D4 (alimentación) y D5 (estado) | 1,4 + 1,8 mA | `alimentacion.md` §3.11; `mcu.md` §7 |
| D6–D11, LED de canal desde los GPIO IN | 6 × 1,5 = 9 mA | `salidas.md` §7 |
| *Pull-ups* de I²C de la placa a nivel bajo (R24, R25) | 2 × 3,39 V / 4,7 kΩ = 1,44 mA | `mcu.md` §9.2 |
| R5 (LIM_EN alto), R6, R77, R79 (FLT e INT a nivel bajo) | 4 × 3,39 V / 10 kΩ = 1,36 mA | netlist |
| R_PD de IN y DEN (7 × 100 kΩ), entradas IN y DEN de los BTT (12 × 25 µA), R78 | 0,23 + 0,30 + 0,03 = 0,56 mA | `mcu.md` §10.2; BTT tabla 10, p. 34 |
| +3V3_EXP (EXP-02) | 50 mA | `viabilidad-expansion.md` §10.3 |
| **Total** | **422 mA** (diseño 0,45 A) | |

- Capacidad: 1 A nominal, I_CL ≥ 1,1 A (TLV p. 5) → **2,2×** sobre 0,45 A. Caída, térmica y pico de Wi-Fi en `mcu.md` §8.3 (T_J 109 °C a 60 °C de ambiente).
- Con el calentador del SHT40 (100 mA máx., no se usa): 0,52 A, 1,9×.
- R16 y R17 (EN y BOOT) solo consumen con SW1 o SW2 pulsados: fuera del presupuesto.

### 2.2 Raíl de 5 V (+5V: U2 → U3, o VBUS → U3)

| Carga | Corriente | Fuente |
|---|---|---|
| U4: carga de 3,3 V + I_Q | 422 + 0,1 mA | §2.1; TLV p. 5 (I_Q ≤ 100 µA) |
| +5V_EXP (EXP-02) | 300 mA | `conectores.md` §2.3 |
| U14 TPS2553 (+5V_EXP), habilitado | ≤ 0,15 mA | SLVS841G p. 6 (R_ILIM = 68 kΩ, entre 20 y 210 kΩ) |
| U3, divisores de FB (R7/R8) y de PR1 (R11/R12) | 0,06 mA | TPS2116 p. 6; netlist |
| **Total** | **0,72 A** (diseño 0,75 A) | |

- Capacidad: U2 2 A (I_OUT,máx ≥ 2,2 A, ec. 1, p. 13; ALI-05 ≥ 1,5 A) → **2,7×** sobre 0,75 A. U3: 2,5 A, 3,3×.
- Con solo USB (programación, ALI-08): la lógica sin expansión pide 0,37 A ≤ 0,5 A de un puerto USB 2.0; con +5V_EXP a 0,30 A no cabe (ya anotado en `mcu.md` §4).

### 2.3 Entrada de 24 V y bus de las salidas

| Comprobación | Cálculo | Resultado |
|---|---|---|
| Lógica en la entrada (ALI-12) | 5,016 V × 0,75 A = 3,76 W; η ≈ 88 % (90 % típ. a 1 A y 24 V, LMR p. 1) → 4,27 W; + U1, divisores y zéner 2,3 mA × 24 V = 0,055 W | **4,32 W ≤ 4,8 W** (margen 0,48 W, 10 %); 0,18 A a 24 V |
| Bus de salidas, carga instalada máxima | 3,5 A (REL-11) + I_GND 6 × 9 mA (BTT p. 8) + fuga de R_OL de los canales apagados ≤ 6 × 0,65 mA = **3,558 A** frente a I_OL mín. 3,86 A de U1 (`alimentacion.md` §3.13.2) | U1 no actúa: margen **0,30 A (7,8 %)** |
| Entrada en régimen | 3,558 + 0,18 A | **3,74 A** |
| Entrada con el limitador en su máximo | I_OL máx. 4,57 A + lógica al tope de ALI-12 (0,20 A) | **4,77 A ≤ 5,1 A** (ALI-12, margen 0,33 A) y < 5,14 A de la fuente (0,37 A, 7,2 %) |
| Corto en el cable de expansión (fallo) | 4,57 A + 0,235 A (`viabilidad-expansion.md` §10.3) | 4,81 A < 5,14 A: la fuente no actúa |
| Capacidad de la entrada | F1 7,2 A con *derating* (`alimentacion.md` §3.2); Q1 50 A; J1 15 A; pistas `Power_In` de 2,0 mm | ≥ 1,41× sobre 5,1 A |

Térmica de los reguladores a 60 °C en la caja: `alimentacion.md` §5 (sin cambios).

## 3. Tabla de GPIO frente a la netlist (MCU-05, base de FW-02)

Generada de la netlist del proyecto integrado, pin a pin del módulo U5; señal y dirección según `mcu.md` §9.2. OD = drenador abierto.

| GPIO | Pin | Señal | Bloque | Dir. | ADC1 | Red (netlist) | Otros pines de la red (netlist) | MCU-05 |
|---|---|---|---|---|---|---|---|---|
| 0 | 27 | BOOT | MCU | E | — | /MCU/BOOT | R17-2, SW2-1 | ✔ arranque (BOOT) |
| 1 | 39 | VIN_SENSE | Alimentación | A | CH0 | /VIN_SENSE | C20-1, R14-2, R15-1 | ✔ ADC1 |
| 2 | 38 | LIM_IMON | Alimentación | A | CH1 | /LIM_IMON | C5-1, R4-2 | ✔ ADC1 |
| 3 | 15 | — | — | — | — | — | — | sin conectar (arranque) |
| 4 | 4 | IS1 | Salidas | A | CH3 | /IS1 | C39-1, R45-2, R51-1 | ✔ ADC1 |
| 5 | 5 | IS2 | Salidas | A | CH4 | /IS2 | C40-1, R46-2, R52-1 | ✔ ADC1 |
| 6 | 6 | IS3 | Salidas | A | CH5 | /IS3 | C41-1, R47-2, R53-1 | ✔ ADC1 |
| 7 | 7 | IS4 | Salidas | A | CH6 | /IS4 | C42-1, R48-2, R54-1 | ✔ ADC1 |
| 8 | 12 | IS5 | Salidas | A | CH7 | /IS5 | C43-1, R49-2, R55-1 | ✔ ADC1 |
| 9 | 17 | IS6 | Salidas | A | CH8 | /IS6 | C44-1, R50-2, R56-1 | ✔ ADC1 |
| 10 | 18 | — | — | — | — | — | — | sin conectar (libre, ADC1_CH9) |
| 11 | 19 | IN1 | Salidas | S, activa alta | — | /IN1 | R26-1, R32-1, R63-1 | ✔ |
| 12 | 20 | IN2 | Salidas | S, activa alta | — | /IN2 | R27-1, R33-1, R64-1 | ✔ |
| 13 | 21 | IN3 | Salidas | S, activa alta | — | /IN3 | R28-1, R34-1, R65-1 | ✔ |
| 14 | 22 | LIM_FLT | Alimentación | E, activa baja (OD) | — | /LIM_FLT | R6-2, U1-14 | ✔ |
| 15 | 8 | IN4 | Salidas | S, activa alta | — | /IN4 | R29-1, R35-1, R66-1 | ✔ |
| 16 | 9 | IN5 | Salidas | S, activa alta | — | /IN5 | R30-1, R36-1, R67-1 | ✔ |
| 17 | 10 | IN6 | Salidas | S, activa alta | — | /IN6 | R31-1, R37-1, R68-1 | ✔ |
| 18 | 11 | — | — | — | — | — | — | sin conectar (libre, solo entrada) |
| 19 | 13 | USB_D− | MCU | E/S | — | /MCU/USB_DM | R21-2 | ✔ USB |
| 20 | 14 | USB_D+ | MCU | E/S | — | /MCU/USB_DP | R20-2 | ✔ USB |
| 21 | 23 | LIM_EN | Alimentación | S, activa alta | — | /LIM_EN | R5-1, U1-12 | ✔ |
| 35 | 28 | EXP_INT | Conectores | E, activa baja (OD) | — | /EXP_INT | R75-1, R77-2, U14-4, U15-4 | ✔ (N8 sin PSRAM octal) |
| 36 | 29 | EXP_EN | Conectores | S, activa alta | — | /EXP_EN | R76-1, R78-1 | ✔ (N8 sin PSRAM octal) |
| 37 | 30 | — | — | — | — | — | — | sin conectar (libre) |
| 38 | 31 | OUT_DEN | Salidas | S, activa alta | — | /OUT_DEN | R38-1 … R43-1, R44-1 | ✔ |
| 39 | 32 | BTN_INT | Conectores | E, activa baja (OD) | — | /BTN_INT | R79-2, U18-13 | ✔ |
| 40 | 33 | LED_STATUS | MCU | S | — | /MCU/LED_STATUS | R23-1 | ✔ |
| 41 | 34 | I2C_SDA | MCU, Sensores, Conectores | E/S (OD) | — | /I2C_SDA | R24-2, U13-1, U18-15 | ✔ |
| 42 | 35 | I2C_SCL | MCU, Sensores, Conectores | S (OD) | — | /I2C_SCL | R25-2, U13-2, U18-14 | ✔ |
| 43 | 37 | TXD0 | MCU | S | — | /MCU/TXD0 | R22-1 | ✔ |
| 44 | 36 | RXD0 | MCU | E | — | /MCU/UART_RX | J3-3 | ✔ |
| 45 | 26 | — | — | — | — | — | — | sin conectar (arranque) |
| 46 | 16 | — | — | — | — | — | — | sin conectar (arranque) |
| 47 | 24 | I2C_EXP_SDA | Conectores | E/S (OD) | — | /I2C_EXP_SDA | R73-1 | ✔ |
| 48 | 25 | I2C_EXP_SCL | Conectores | S (OD) | — | /I2C_EXP_SCL | R74-1 | ✔ |

- MCU-05: analógicas (8) solo en GPIO1–10; ninguna salida en 0, 3, 45 o 46; GPIO19/20 solo a R20/R21 → U6 → J2; GPIO35–37 se usan porque el N8 no lleva PSRAM octal (`mcu.md` §2). ✔
- Coincide señal a señal con `mcu.md` §9.2. **FW-02:** `firmware/` aún no existe; el YAML se escribirá desde esta tabla.

## 4. Revisión global (fase 3 del plan)

### 4.1 Pines de arranque (MCU-05, MCU-04)

| Punto | Evidencia | Resultado |
|---|---|---|
| GPIO0 | /MCU/BOOT = {U5-27, R17-2, SW2-1}; R17 10 kΩ a +3V3; ningún condensador | ✔ |
| GPIO3, GPIO45, GPIO46 | `unconnected-(U5-IO3-Pad15)`, `…IO45-Pad26`, `…IO46-Pad16`: sin pistas ni piezas (WPD interno de 45 y 46 → flash a 3,3 V y arranque normal) | ✔ |
| EN | /MCU/EN = {U5-3, R16-2 (10 kΩ a +3V3), C23-1 (1 µF a GND), SW1-1}; RC de `mcu.md` §5.1 | ✔ |

### 4.2 Salidas, limitador y expansión apagados en el reset y el flasheo (REL-04)

| Red | Evidencia (netlist) | Polaridad de la entrada de control | Resultado |
|---|---|---|---|
| IN1–IN6 (GPIO11–17) | R32–R37 100 kΩ de /IN_n a GND, en el lado del GPIO de R_IN | IN del BTT activa alta; 5 mV con el pin en Z ≪ V_IN(L) 0,8 V (BTT tabla 10, p. 34) | ✔ |
| OUT_DEN (GPIO38) | R44 100 kΩ de /OUT_DEN a GND | DEN activa alta; GPIO38 bajo en descarga USB-OTG (HDG tabla 12, p. 19) | ✔ |
| LIM_EN (GPIO21) | R5 10 kΩ de /LIM_EN a GND; /LIM_EN = U1-12 (~SHDN) | ~SHDN activa baja: con el pin en Z el bus está apagado (0,1 V < 0,8 V, `alimentacion.md` §3.13.5) | ✔ |
| EXP_EN (GPIO36) | R78 100 kΩ de /EXP_EN a GND, en el lado del MCU de R76 | Activa alta en el módulo | ✔ |
| Pines en el reset | GPIO11–17, 21, 36 y 38: Z sin *pull* en el reset, sin pulsos altos al arrancar (S tablas 2-1 y 2-2, pp. 16-19; `mcu.md` §10.1) | — | ✔ |

Con JP1 cerrado (sin limitador, DEC-0006) queda solo la R_PD de cada IN (`alimentacion.md` §3.13.9). OTA y `esp_restart()`, en el firmware (`mcu.md` §10.1).

### 4.3 Polaridades

| Pieza | Evidencia (netlist, pin del símbolo) | Resultado |
|---|---|---|
| J1 | 1 = VIN_RAW (+24 V), 2 = GND | ✔ (serigrafía «+» en el pin 1, layout) |
| Q1 P-MOSFET de polaridad | D = VIN_F (entrada), S = VIN_PROT (carga), G = Q1_G: el diodo interno conduce hacia la carga | ✔ |
| D1 BZT52C15 | K = VIN_PROT (fuente de Q1), A = Q1_G: limita V_GS a −15 V | ✔ |
| D2 SMBJ33A | K = VIN_PROT, A = GND, unidireccional después de Q1 | ✔ |
| D3 SS310 | K = BUS_24V, A = GND (rueda libre a la salida de U1) | ✔ |
| C1 47 µF electrolítico (`Device:C_Polarized`) | 1 (+) = VIN_PROT, 2 = GND | ✔ |
| D12–D17 M7 | K = /Salidas/CanalN/OUT, A = GND en los 6 canales; cátodo = pad 1 (`M7.md`) | ✔ |
| D4–D11 LED | K = GND, A = resistencia; cátodo = pad 1 del KT-0603R (VAL-0022-01-01) | ✔ |
| J4–J9 | 1 = OUT_n, 2 = GND en los 6 canales (REL-06) | ✔ |
| U3 TPS2116 | VIN1 = +5V_BUCK, VIN2 = VBUS, MODE = VIN1 (prioridad del buck) | ✔ |
| J2 USB-C | CC1/CC2 con R18/R19 5,1 kΩ a GND (*sink*); VBUS solo a U3 VIN2 por U6 | ✔ |
| J3 UART | 1 = +3V3, 2 = TXD0 (R22), 3 = RXD0, 4 = GND (`mcu.md` §6) | ✔ |

### 4.4 ESD en los conectores de campo

| Conector | Protección (netlist) | Resultado |
|---|---|---|
| J1 (24 V) | D2 SMBJ33A tras F1 y Q1 (V_RWM 33 V, `alimentacion.md` §3.4) | ✔ |
| J4–J9 (salidas) | C_OUT 220 nF 100 V (C33–C38) y D12–D17 en cada OUT_n; OUT del BTT ± 4 kV HBM (BTT tabla 3, p. 7). Sin TVS en OUT por diseño (`salidas.md` §4.3) | ✔ |
| J10 (expansión) | U16 en EXP_SDA_J/EXP_SCL_J (VBUS = +3V3_EXP) y U17 en EXP_INT_J/EXP_EN_J (VBUS = +5V_EXP); R73–R76 en serie; los raíles del conector, a los VBUS de U16/U17 | ✔ |
| J2 (USB-C) | U6 en D+/D− (I/O1 y I/O2) y VBUS (pin 5); SHIELD a GND | ✔ |
| J3 (UART) | Sin ESD: conector de servicio interno, no de campo (`mcu.md` §6) | No aplica |
| SW1–SW8 | Pulsadores en placa, no conectores de campo (ver §4.6) | No aplica |

### 4.5 Test points (ALI-11)

TP1 VIN_PROT, TP2 +5V, TP3 +3V3, TP4 GND (THT, para la pinza) y TP5 BUS_24V (`alimentacion.md` §3.12), fuera del BOM y del CPL. ALI-11 pide VIN, 5 V, 3,3 V y GND. ✔

### 4.6 Otras comprobaciones y observaciones

| Punto | Evidencia | Resultado |
|---|---|---|
| Salidas de SPEC-0034 (DEC-0014) | D12–D17 sin DNP (`campos.py revisar`: 0 DNP); tabla REL-11 de `salidas.md` §0 sin cambios frente a `main` | ✔ |
| Netlist frente a `main` | `hoja.py netlist hardware/v2 <copia> --grupos` y sin `--grupos`: 0 diferencias | ✔ |
| Raíz y DEC-0015 | Reglas 1–6 a la vista de la imagen; un recuadro; ningún cable cruza una hoja ni un texto; el cruce SDA/SCL de Sensores es inevitable con tres hojas en un bus de dos hilos y va sin unión | ✔ |
| Observación 1 | SW3–SW8 van al TCA9554 sin ESD (± 2 kV HBM, TCA p. 5). No son conectores de campo; si la caja los acciona desde fuera, el layout mantiene su carcasa lejos de pistas y rodeada de GND | Sin cambio de circuito |
| Observación 2 | VBUS con solo USB no da los 0,30 A de la expansión (§2.2) | Ya en `mcu.md` §4; sin cambio |
