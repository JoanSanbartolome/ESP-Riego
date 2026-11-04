---
id: DEC-0002
titulo: Objetivo de la v2 revisado: interior, 24 V AC, 6 salidas, T/HR en placa y sin nivel
fecha: 2026-11-04
estado: aceptada
decide: usuario
specs: [SPEC-0004, SPEC-0005, SPEC-0006]
requisitos: [ALI-01, ALI-02, ALI-03, ALI-04, ALI-06, ALI-09, REL-01, REL-02, REL-03, REL-05, REL-06, REL-08, REL-09, AMB-01, AMB-02, AMB-03, EXP-01, EXP-02, EXP-04, FAB-03, FAB-07, FAB-08, FAB-10, FW-03]
---

# DEC-0002 · Objetivo de la v2 revisado

## Contexto

Las especificaciones v0.1 (SPEC-0000) conservaban el objetivo del TFG: 4 canales, sensor de nivel 4–20 mA, sonda de temperatura y humedad externa, caja IP65 en exterior y alimentación de 9–30 V DC (batería o panel solar). El 2026-11-04 el usuario redefine el objetivo de la placa, que ya no coincide con el del TFG.

## Lo que decide el usuario

| # | Decisión | Requisitos afectados |
|---|---|---|
| 1 | Al menos **6 salidas**, ampliables con un **módulo de expansión** del que quiere más adelante un informe de viabilidad con componentes y costes. | REL-01, EXP-02, EXP-04 · D1 cerrada · D9 (SPEC-0006) |
| 2 | Bornes de las salidas repartidos: **3 canales en el borde superior y 3 en el inferior**. | REL-09, FAB-07, FAB-08 |
| 3 | **Sensor de temperatura y humedad integrado en la placa.** | AMB-01 … AMB-03 |
| 4 | **Se elimina el sensor de nivel:** no es el objetivo de esta placa. | NIV-01 … NIV-08 retirados · D7 sin objeto |
| 5 | **Instalación en interior** (casa o caseta), en una caja ventilada colgada en la pared; ya no es una caja hermética en exterior. | §1, §5, FAB-10 · D5 |
| 6 | Las válvulas instaladas son **electroválvulas de riego de 24 V AC**, pero no quiere una solución que solo sirva para un tipo de carga: pide un estudio con pros, contras y limitaciones de relés, relés de estado sólido y transistores. | REL-03, REL-05, REL-08 · D2, D8 (SPEC-0005) |
| 7 | La placa se **alimenta del transformador de riego de 24 V AC**, para simplificar la alimentación. | ALI-01 … ALI-04, ALI-06, ALI-09 |

## Interpretación del coordinador (pendiente de revisión del usuario)

- **Entrada AC y DC:** la entrada se rectifica con un puente, de modo que admite 24 V AC y también 12–36 V DC de cualquier polaridad. El puente sustituye a la protección contra inversión de polaridad de la v0.1 (ALI-03).
- **Sin batería ni panel solar:** dejan de ser objetivo, aunque la entrada DC las sigue admitiendo.
- **Sonda exterior opcional:** el sensor en placa mide el aire del recinto porque la caja está ventilada. Para medir fuera de la caseta queda la opción de una sonda por el conector I²C de expansión (AMB-03).
- **Supervisión de la alimentación (ALI-09):** pasa a detectar el fallo del transformador en lugar de medir la batería.
- **Barniz (FAB-10):** baja a C, porque la placa queda en interior.

## Alternativas consideradas

- **Bornes de 3 polos (NO/COM/NC) en un solo borde:** necesitan 18 × 5,08 = 91 mm más la entrada, así que no caben en 100 mm. El usuario elige repartirlos en dos bordes.
- **Bornes de 2 polos (solo NO/COM):** se aplaza. El número de polos por canal depende de la tecnología de salida y de si la salida es alimentada (SPEC-0005).

## Consecuencias

- `docs/02-especificaciones-v2.md` pasa a la v0.2 (SPEC-0004). Los IDs retirados no se reutilizan.
- Desaparecen el boost de 24 V del lazo, la clase de red `Loop_4_20mA`, la prueba del lazo y la decisión D7.
- Nuevas decisiones abiertas:
  - D8, tecnología de las salidas: la resuelve el usuario a partir de SPEC-0005;
  - D9, arquitectura del módulo de expansión: la resuelve el usuario a partir de SPEC-0006.
- El tamaño objetivo (FAB-08) se fija cuando se cierre D8: depende de la altura de cada franja de salidas.
- El usuario irá añadiendo *features*. Cada ronda se registra en una DEC y en una spec de requisitos nuevas.
