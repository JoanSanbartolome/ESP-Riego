---
spec: SPEC-0006
agente: ing-diseno
n: 03
fecha: 2026-11-15
estado: completado
---

# SPEC-0006 · 03 · ing-diseno

Correcciones de VAL-0006-01 (01, 02, 03, 05, 06 y 07(1)). No se tocan el 04 ni el 07(2), que van al coordinador.

## Hecho

- `docs/diseno/viabilidad-expansion.md`:
  - **01** (§10.2 y §10.6): EN de U_A y U_B unido a su IN. Los FAULT van a EXP_INT en el lado del MCU de la de 470 Ω, junto al *pull-up*. Para `mcu.md`, SPEC-0031 añade EXP_EN a §10.1 (estado seguro), a §10.2 (R_PD de 100 kΩ, 5 mV en Z) y al Anexo B (`on_boot`, `ota: on_begin` y `on_shutdown`; ceros en el expansor antes de un OTA y antes de subir EXP_EN).
  - **02:** lista de piezas por arquitectura y variante; tabla de §8 recalculada (cambios de céntimos por R_LED 1,5 kΩ).
  - **03:** peor caso con USB a 5,25 V. R_ILIM_B pasa de 200 a 220 kΩ (C22961, Basic): 104–146 mA y T_J del TLV1117LV de 122,9 °C (119,2 °C con el buck). Recalculado el corto del cable: 5,65 W y 4,81 A.
  - **05:** OE de la arquitectura 3 por un inversor (N-MOS con *pull-up*). Corregidos el estado seguro y ESPHome (`sn74hc595` sin `oe_pin`).
  - **06:** margen de I²C en los dos sentidos: 0,47 V cuando transmite el ESP32 y 0,40 V cuando responde el módulo. El 4.º módulo (ADDR = SDA, SBAS444E p. 20) queda condicionado a comprobarlo en el prototipo: el máximo seguro es 3 × 8.
  - **07(1):** Waveshare a 31,49 $; con 5 uds, el módulo cuesta casi lo mismo.
- `hardware/componentes/bom-expansion.csv` (nuevo): 292 filas (arquitectura, canales, código, MPN, tipo, cantidad por módulo, uniones, SMT/THT, función, precio de los tramos de 5 y 10 uds).
- `hardware/componentes/stock-expansion.csv`: regenerado con la columna `Uso`, 169 filas. Ya están todos los códigos del informe, incluidas las 5 que faltaban.

## Decisiones y desviaciones

- **06:** el cálculo del informe da 0,40 V, no los 0,25 V del hallazgo. Los *pull-ups* van en el lado del conector y por la de 100 Ω no circula corriente cuando el ESP32 recibe. El informe da también los 0,25 V que saldrían con los *pull-ups* en el lado del MCU, y pide a SPEC-0031 que los ponga en el lado del conector.
- **03:** se elige 220 kΩ, no los 232 kΩ propuestos: 232 kΩ es Extended (C22913, +3,07 $ por pedido) y solo gana 0,8 K.

## Verificación

- Los 20 totales de §8 salen de `bom-expansion.csv` con un script independiente: coinciden al céntimo.
- Códigos LCSC del informe frente a `stock-expansion.csv`: ninguno falta.
- No se ha tocado ningún proyecto KiCad: `verificar.py` no aplica.

## Para validación

- §10.3, T_J de 122,9 °C (2,1 K de margen, solo en fallo): se propone una prueba en el prototipo con +3V3_EXP en corto y alimentación por USB.
- El inversor de la arquitectura 3 (≈ 0,02 $) no está en la tabla de §8.

## Pendiente

- Lo de VAL-0006-01-04 (F1) y VAL-0006-01-07(2) (prueba de `jlc.py --buscar`), para el coordinador.
- Siguen abiertos los puntos 1, 2 y 5 del parte 01: D9 con el requisito de la fuente propia del módulo, la corriente de las válvulas y el traspaso a SPEC-0031.
