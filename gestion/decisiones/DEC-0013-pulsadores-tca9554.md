---
id: DEC-0013
titulo: Lectura de los 6 pulsadores con un TCA9554 en el bus I²C de la placa
fecha: 2026-11-15
estado: aceptada
decide: usuario
specs: [SPEC-0031]
requisitos: [EXP-03, AMB-01, MCU-05, FW-04]
---

# DEC-0013 · Lectura de los 6 pulsadores con un TCA9554 en el bus I²C de la placa

## Contexto

EXP-03 (v0.6, DEC-0011) pide 6 pulsadores en la placa, uno por salida, leídos por el firmware con antirrebote. Quedan cuatro pines libres (GPIO10, ADC1; GPIO18, solo entrada y con pulso alto al arrancar; GPIO37; GPIO39, con WPU), así que no caben uno por pin. `docs/diseno/conectores.md` §1 (SPEC-0031, paso 1) compara las opciones con precios y stock de `jlc.py` del 2026-11-15.

## Opciones consideradas

Coste por placa con 5 / 10 uds, sin los 0,17 $ de los 6 pulsadores TS-1187A, comunes a todas (`conectores.md` §1.5):

1. **A · escalera de 6 niveles en GPIO10** (recomendada por `ing-diseno`): 0,05 / 0,05 $, todo Basic. Con dos pulsaciones a la vez gana la más cercana y nunca acciona un tercer canal; *lambda* propia en ESPHome. Quedan libres GPIO18, 37 y 39.
2. **B · PCA9554PWR de TI en 0x20, INT en GPIO39:** 2,10 / 1,53 $, una línea Extended. Detecta las dos pulsaciones; componente `pca9554` probado en ESPHome. Quedan libres GPIO10, 18 y 37.
3. **B' · PCA9554PW,118 de NXP:** 1,68 / 1,19 $; falta su datasheet.
4. **B'' · TCA9554PWR de TI con 6 *pull-ups* externos de 10 kΩ, INT en GPIO39:** 1,52 / 1,06 $, una línea Extended (C477924, 5 455 en JLCPCB). Como B; en ESPHome «debería funcionar».
5. **C · mixta** (3 pines directos y escalera de 3): 0,05 / 0,05 $; ocupa los 4 pines libres.

## Decisión

Decidida por el usuario el 2026-11-15: **B'', TCA9554PWR (C477924) en el bus I²C de la placa (GPIO41/42), dirección 0x20, con un *pull-up* de 10 kΩ (C25804) por pulsador, INT en GPIO39 con 10 kΩ a +3V3 y 100 nF (C14663) en VCC**. Las dos pulsaciones simultáneas se detectan por separado, sin tocar GPIO10 (reserva de ADC1) ni GPIO37.

## Consecuencias

- **Coste:** +1,52 $ por placa con 5 uds y +1,06 $ con 10, sobre todo por la línea Extended (3,07 $ por pedido).
- **Pines:** GPIO39 pasa a `BTN_INT` (entrada, drenador abierto con *pull-up*); quedan libres GPIO10, 18 y 37. SPEC-0031 lo lleva a `mcu.md` §9.2 y a la hoja MCU.
- **Bus de la placa:** un segundo dispositivo junto al SHT40 (0x44, sin choque); R24 y R25 siguen siendo los *pull-ups* del bus, que se configura a **100 kHz** (`conectores.md` §1.3: t_r ≈ 0,28 µs con ≈ 70 pF). Un TCA9554 averiado que retenga SDA bloquearía también el SHT40 (AMB-01): riesgo aceptado.
- **Firmware (fase 6):** componente `pca9554` con `address: 0x20` e `interrupt_pin: GPIO39`, un `binary_sensor` por pulsador con antirrebote; el prototipo comprueba que el TCA9554 funciona con él. Si falla, el PCA9554PWR (C2873588) va en la misma huella TSSOP-16 sin los *pull-ups* externos.
- **Layout (fase 4):** el TCA9554 junto a la fila de pulsadores, en el centro de la placa (FAB-07).
