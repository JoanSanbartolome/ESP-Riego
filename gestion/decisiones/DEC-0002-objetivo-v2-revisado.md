---
id: DEC-0002
titulo: Objetivo de la v2 revisado: interior, 24 V DC, 6 salidas, T/HR en placa y sin nivel
fecha: 2026-11-04
estado: aceptada
decide: usuario
specs: [SPEC-0004, SPEC-0005, SPEC-0006]
requisitos: [ALI-01, ALI-02, ALI-04, ALI-05, ALI-06, ALI-09, ALI-12, REL-01, REL-02, REL-03, REL-05, REL-06, REL-08, REL-09, AMB-01, AMB-02, AMB-03, EXP-01, EXP-02, EXP-04, FAB-03, FAB-07, FAB-08, FAB-10, FW-03]
---

# DEC-0002 · Objetivo de la v2 revisado

## Contexto

Las especificaciones v0.1 (SPEC-0000) conservaban el objetivo del TFG:

- 4 canales;
- sensor de nivel 4–20 mA;
- sonda externa de temperatura y humedad;
- caja IP65 en exterior;
- alimentación de 9–30 V DC (batería o panel solar).

El 2026-11-04 el usuario redefine el objetivo de la placa, que ya no coincide con el del TFG.

## Lo que decide el usuario

| # | Decisión | Requisitos afectados |
|---|---|---|
| 1 | Al menos **6 salidas**, ampliables con un **módulo de expansión**. Del módulo quiere más adelante un informe de viabilidad con componentes y costes. | REL-01, EXP-02, EXP-04 · D1 cerrada · D9 (SPEC-0006) |
| 2 | Bornes de las salidas repartidos: **3 canales en el borde superior y 3 en el inferior**. | REL-09, FAB-07, FAB-08 |
| 3 | **Sensor de temperatura y humedad integrado en la placa**, que mide el aire de la caseta, con corrección calibrada en el firmware. | AMB-01 … AMB-03, §6 |
| 4 | **Se elimina el sensor de nivel:** no es el objetivo de esta placa. | NIV-01 … NIV-08 retirados · D7 sin objeto |
| 5 | **Instalación en interior** (casa o caseta), en una caja ventilada colgada en la pared. Ya no es una caja hermética en exterior. | §1, §5, FAB-10 · D5 |
| 6 | Las válvulas instaladas son **electroválvulas de riego de 24 V DC, de ≈ 0,2 A cada una** (lo aclara tras el estudio de SPEC-0005; hasta entonces se había supuesto 24 V AC), pero no quiere una solución que solo sirva para un tipo de carga. Pide un estudio con pros, contras y limitaciones de relés, relés de estado sólido y transistores. | REL-03, REL-05, REL-08 · D2, D8 (SPEC-0005) |
| 7 | **Alimentación única desde una fuente de 24 V DC de hasta 5 A.** Primero propuso el transformador de riego de 24 V AC; tras la primera validación quita la entrada de AC. | ALI-01 … ALI-06, ALI-12 |
| 8 | **Las 6 salidas pueden estar activas a la vez.** | ALI-12, REL-05 |
| 9 | **Corte total de la fuente:** basta con que Home Assistant vea la placa «no disponible». Sin reserva de energía. | ALI-09, FW-03, §6 |

## Interpretación del coordinador

El usuario revisó la v0.2 y le dio el visto bueno el 2026-11-04, antes de la primera validación. Las decisiones 7 a 9 llegaron después, al resolver VAL-0004-01.

- **Rango de entrada:** 18–30 V DC alrededor de los 24 V nominales, para cubrir el ajuste de la fuente y la caída en el cable. Se recupera la protección de polaridad de la v0.1, con TVS de clase SMBJ33A, y el buck ≥ 60 V queda justificado por su Vc.
- **Válvulas instaladas de 24 V DC:** la placa puede alimentarlas directamente desde la entrada (salida alimentada). El contacto libre queda como opción para cargas con su propia fuente, como válvulas de 24 V AC con su transformador; por eso REL-02 admite hasta 32 V AC en esos contactos.
- **Presupuesto (ALI-12):** con la fuente de 5 A, las salidas alimentadas se limitan a 4 A en total, para dejar margen a la lógica.
- **Sin batería ni panel solar:** dejan de ser objetivo.
- **Sonda exterior opcional (AMB-03):** sigue siendo posible por el conector I²C de expansión.
- **Supervisión (ALI-09):** avisa de subtensión y sobretensión de la entrada en lugar de medir la batería.
- **Barniz (FAB-10):** baja a C, porque la placa queda en interior.
- **Prioridades:** REL-08 sube de C a S, EXP-02 sube de S a M, EXP-04 entra en M y AMB-03 baja de S a C.
- **Bordes:** además de las salidas 3 + 3, al borde inferior van la entrada de alimentación, la de pulsos y el conector de expansión. Los laterales quedan para la antena, el USB-C y el sensor (FAB-07).
- **Valores numéricos:**
  - REL-02: ≤ 32 V AC / 36 V DC;
  - REL-05: ≥ 1 A por canal;
  - §5: de −10 a +50 °C y 10–90 % HR sin condensación;
  - §6: ±0,5 °C / ±3 % HR.
- **Número de salidas:** «al menos 6» se lee como 6 en la placa, y las demás con el módulo de expansión (REL-01, EXP-04).

## Alternativas consideradas

- **Bornes de 3 polos (NO/COM/NC) en un solo borde:** necesitan 18 × 5,08 = 91 mm más la entrada, y no caben en 100 mm. El usuario elige repartirlos en dos bordes.
- **Bornes de 2 polos (solo NO/COM):** se aplaza. El número de polos por canal depende de la tecnología de salida y de si la salida es alimentada (SPEC-0005).
- **Alimentación desde el transformador de riego de 24 V AC:** se recogió en el primer borrador de la v0.2, con puente rectificador y entrada de 20–32 V AC. El usuario la descarta y se queda con una fuente de 24 V DC.

## Consecuencias

- `docs/02-especificaciones-v2.md` pasa a la v0.2 (SPEC-0004). Los IDs retirados no se reutilizan.
- Desaparecen:
  - el boost de 24 V del lazo;
  - la clase de red `Loop_4_20mA`;
  - la prueba del lazo;
  - la decisión D7.
- Nuevas decisiones abiertas, que resuelve el usuario:
  - **D8, tecnología de las salidas:** a partir de SPEC-0005, con las válvulas instaladas de 24 V DC y ≈ 0,2 A.
  - **D9, arquitectura del módulo de expansión:** a partir de SPEC-0006.
- El tamaño objetivo (FAB-08) se fija al cerrar D8, porque depende de la altura de cada franja de salidas.
- El usuario irá añadiendo *features*. Cada ronda se registrará en una DEC y una spec de requisitos nuevas.
