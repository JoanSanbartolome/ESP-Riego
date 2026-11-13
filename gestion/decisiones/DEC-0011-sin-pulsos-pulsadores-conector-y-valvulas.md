---
id: DEC-0011
titulo: Sin entrada de pulsos, pulsadores manuales, conector con SPEC-0006 y válvulas instaladas
fecha: 2026-11-13
estado: aceptada
decide: usuario
specs: [SPEC-0006, SPEC-0028, SPEC-0030, SPEC-0031, SPEC-0032]
requisitos: [EXP-01, EXP-02, EXP-03, EXP-04, REL-03, REL-05, ALI-12]
---

# DEC-0011 · Sin entrada de pulsos, pulsadores manuales, conector con SPEC-0006 y válvulas instaladas

## Contexto

Para cerrar el esquema v2 quedaban abiertas D3 (entrada de pulsos o de lluvia, EXP-01), D4 (pulsadores manuales, EXP-03) y D9 (arquitectura de la expansión, EXP-02 y EXP-04), además de la inductancia de la válvula (REL-03) y de si se versiona el `.kicad_pro` que reescribe KiCad 10. El coordinador se lo preguntó al usuario el 2026-11-13 con el desglose de lo que falta de la fase 3.

Al contestar, el usuario envió una foto de una válvula instalada. La etiqueta dice Bermad S-390-3-D, 24 VAC, NC, 200 mA y 3,5 W, con cables naranja y azul. No es el modelo de 24 V DC (S-390-T-2W, 156 Ω y 0,18 A) que usan DEC-0002 y `docs/diseno/salidas.md`. En la ficha S-390-T-3W de Bermad (edición de agosto de 2026), la fila que coincide (24VAC-D, NC, naranja y azul, 0,2 A de arranque y de mantenimiento) da 4,0 W y 42 Ω a 20 °C; otras ediciones dicen que la resistencia de las bobinas «D» no se puede medir.

## Decisión

Decididas por el usuario el 2026-11-13.

1. **D3: no hay entrada de pulsos.** «No vamos a tener entrada de lluvia» y «también desaparece la entrada de pulsos para el caudalímetro». EXP-01 se retira.
2. **D4: pulsadores manuales, uno por salida.** «Unos botones manuales que vayan por firmware con antirrebote»; «un botón por cada accionamiento», colocados «una al lado de otra en fila en el centro de la placa». Son 6 pulsadores en la placa que lee el firmware: no actúan directamente sobre la salida.
3. **D9: el conector de expansión se fija junto con SPEC-0006.** El coordinador proponía fijarlo ya con lo que reserva la hoja MCU y aplazar el informe; el usuario prefiere hacerlos juntos. Lectura del coordinador: SPEC-0006 entrega el informe de viabilidad y, con él, la definición del conector (EXP-02); D9 la decide el usuario con el informe.
4. **`.kicad_pro`: se versiona cuando cambie.**
5. **Válvulas instaladas: las de la foto, alimentadas en continua.** «Ahora las válvulas se alimentan con la fuente de 24 V sin problema las 6 a la vez, no puedo medir ahora». El diseño de las salidas no cambia por ahora.

## Consecuencias

- **Requisitos v0.6** (spec del coordinador, validación ligera):
  - EXP-01 pasa a «Requisitos retirados»; salen del diagrama de §3 la entrada de pulsos y de FAB-07 su borne; D3 y D4 quedan cerradas.
  - EXP-03 se redefine con los 6 pulsadores, su lectura por firmware y su posición. Propuesta del coordinador: prioridad de C a S; el usuario dijo «sería interesante».
  - EXP-02 y EXP-04: el conector se fija con el informe de SPEC-0006, no después.
- **GPIO:** `PULSE_IN` (GPIO37) queda libre. Con GPIO10, 18 y 39 hay 4 pines libres y 6 pulsadores no caben uno por pin: el bloque de conectores compara una escalera de resistencias en un canal de ADC1 con un expansor I²C en el bus de la placa (`docs/diseno/mcu.md` §9).
- **Pulsadores en el centro de la placa:** solo se alcanzan con la caja abierta, y ocupan la zona por la que pasan el bus de 24 V y los planos. Es una restricción del *floorplan* de la fase 4.
- **SPEC-0006** añade a su alcance la definición del conector (pines, tensiones, tipo y ESD) a partir de lo que ya reserva la hoja MCU: I²C propio (GPIO47 y 48), `EXP_INT` (GPIO35), `EXP_IO2` (GPIO36), 3,3 V ≤ 50 mA, 5 V de 0,30 A y GND.
- **Válvulas (pendiente, antes de la etiqueta `v2.0-sch`):**
  - Que funcionen hoy las seis a la vez no dice cuánta corriente toma cada una en continua. Si la bobina fuera una resistencia de 42 Ω, serían 0,57 A y 13,7 W por válvula a 24 V: seis darían 3,4 A, al borde de la carga instalada máxima de 3,5 A (ALI-12), y dos por canal pasarían de 1 A (REL-05). Si lleva un rectificador, la cifra es otra. Es una cuenta del coordinador, sin validar.
  - Falta medir la corriente de una válvula a 24 V DC, o la resistencia de la bobina en los dos sentidos. Con el dato, `ing-diseno` revisa `salidas.md` (E_AS de REL-03, corriente por canal, IS y carga instalada) y se decide si hay que montar D12–D17 (DEC-0008) o cambiar algo más.
  - El texto de DEC-0002 («electroválvulas de riego de 24 V DC») se corrige en la v0.6: son bobinas de 24 V AC alimentadas en continua.
- **`.kicad_pro`:** sale de las consultas pendientes; la línea de SPEC-0028 pasa a ser confirmar el archivo que KiCad 10 reescribe.
