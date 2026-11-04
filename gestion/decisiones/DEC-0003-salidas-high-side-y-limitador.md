---
id: DEC-0003
titulo: Salidas con high-side inteligente BTT6050 y limitador común del bus de salidas
fecha: 2026-11-04
estado: aceptada
decide: usuario
specs: [SPEC-0005, SPEC-0007]
requisitos: [ALI-04, ALI-09, ALI-12, ALI-13, REL-01, REL-02, REL-03, REL-04, REL-05, REL-08, REL-10, FAB-03, FAB-07, FAB-08]
---

# DEC-0003 · Salidas con *high-side* inteligente y limitador común

## Contexto

DEC-0002 dejó abiertas:

- **D8**, la tecnología de las salidas;
- **D2**, salida alimentada, contacto libre o ambas.

El estudio de SPEC-0005 (`docs/diseno/estudio-salidas.md`, validado en VAL-0005-01) compara relé, SSR, triac, MOSFET discreto y *high-side* inteligente. Las válvulas instaladas son de 24 V DC, de ≈ 0,2 A cada una. La placa se alimenta de una fuente de 24 V DC de hasta 5 A.

VAL-0005-01-01 señaló que, con un corto en una salida, la fuente de 5 A limita antes que el *high-side* (≥ 38 A). En ese caso:

- el bus de 24 V cae para todos los canales;
- la medida IS deja de ser fiable;
- la lógica queda con 5–15 ms de autonomía, no con los 60 ms que se habían estimado.

## Lo que decide el usuario

| # | Decisión | Requisitos afectados |
|---|---|---|
| 1 | **D8: *high-side* inteligente Infineon BTT6050-1ERA** (C534868) en cada canal, con su protección y su diagnóstico completos. La segunda fuente es el BTT6030-2ERA (C534865) y la reserva, el BSP752R (C112644). Se descartan el relé y el MOSFET discreto. Relajar las protecciones ahorraba ≈ 4,7–5,8 $ por placa, a cambio de perder la protección propia del canal y de que el fallo típico deje la válvula abierta. | REL-01, REL-03, REL-05, REL-10 |
| 2 | **Limitador común en el bus de las salidas** ante un cortocircuito (VAL-0005-01-01), en lugar de un condensador de autonomía con una reacción por hardware. | ALI-12, ALI-13, REL-08 |
| 3 | **D2: solo salida alimentada; se quita el contacto libre de potencial.** Lo confirma a propuesta del coordinador. Una carga con su propia fuente (p. ej. una válvula de 24 V AC) se movería con un relé externo o con el módulo de expansión. | REL-02, REL-08 |

## Interpretación del coordinador

- **D2: solo salida alimentada** (confirmada por el usuario, decisión 3).
  - El BTT6050 conmuta el positivo del bus y no ofrece contacto libre de potencial.
  - Se retira el contacto libre de REL-08, y REL-02 queda en ≤ 36 V DC.
  - Una carga con su propia fuente, como una válvula de 24 V AC, se puede mover con un relé externo gobernado por una salida, o con el módulo de expansión (D9).
  - Esto reduce la flexibilidad que el usuario pedía en DEC-0002 (decisión 6); el usuario lo acepta.
- **Limitador común (ALI-13):**
  - Es un eFuse o un controlador *hot-swap* de ≥ 60 V, entre las protecciones de entrada y los *high-side*. Su umbral:
    - no actúa con los 4 A de ALI-12;
    - sumado al consumo de la lógica, queda por debajo de la corriente a la que limita la fuente.
  - El buck se alimenta antes del limitador: un corto en las salidas no le quita tensión, y la lógica no necesita retención (*hold-up*). ALI-09 sigue sin reserva de energía.
  - Su habilitación desde un GPIO sustituye al corte general con un BTT6030-2ERA por borde que proponía el estudio (§11.5).
  - La medida de su corriente total (IMON), si la tiene, sustituye a la suma de las IS para vigilar los 4 A, que tiene un error de ± 25 % (VAL-0005-01-04).
- **REL-08 se relaja:**
  - ante un corto, el bus de las salidas puede cortarse un momento;
  - el firmware identifica el canal en fallo (IS, DEN y fallo del limitador), lo deja apagado y rearma los demás en ≤ 5 s.
  - Con el límite fijo del BTT6050 (≥ 38 A), mantener alimentados los demás canales durante el corto exigiría un fusible por canal, y el usuario ha elegido el limitador común.
  - REL-08 pasa de S a M, porque ahora es la protección real de las salidas.
- **Diagnóstico (REL-10, S):** IS por canal hacia un ADC1, con R_SENSE y la tensión acotada en caso de fallo, y carga abierta en OFF con un *pull-up* R_OL (VAL-0005-01-05).
- **Bornes (FAB-07):** 2 polos por canal (OUT_n y GND), así que hay 6 polos (30,5 mm) en cada borde. Con la entrada, los pulsos y la expansión, el borde inferior suma ≈ 66–71 mm de los ≈ 86 mm útiles.
- **Tamaño (FAB-08):** ≈ 100 × 70 mm (±5 mm), a confirmar en el layout.
- **Observaciones de VAL-0004-02** que se resuelven en la v0.3:
  - orden de la TVS respecto a la polaridad;
  - VRWM frente a la OVP de la fuente;
  - puntos de aviso a 16 V y 32 V;
  - prueba térmica con dos canales a 1 A;
  - corrección de T/HR en reposo y con carga;
  - clase de red del bus de las salidas;
  - presupuesto de los bordes.

## Alternativas consideradas

- **Relé subminiatura G5NB:** 5,54 / 4,97 $ por placa (pedidos de 5 / 10 placas), con fusibles. Es la única opción con contacto libre, pero no tiene diagnóstico y su montaje es THT.
- **MOSFET discreto con fusible por canal:** 3,64 / 2,98 $. No tiene protección propia ni diagnóstico, y el MOSFET puede morir en corto antes que el fusible y dejar la válvula abierta.
- **BTT6030-2ERA como principal:** 8,38 / 7,91 $, o 9,28 $ con 5 placas, al tramo de precio de 10 unidades (VAL-0005-01-03). Da 4 A por canal con los dos activos, y su kILIS es 2240 (el firmware cambia la constante). Queda como segunda fuente.
- **Chips de la lista del usuario:**
  - VN5050J y VN5012AK: 41 V de máximo absoluto, por debajo de la Vc de la TVS.
  - BTS428L2: umbral de entrada de hasta 3,2 V y protección de corto solo hasta 24 V.
  - TPS281C30: caro y con poco stock.
- **Condensador de autonomía y reacción por hardware** frente al corto: es más barato, pero exige un *hold-up* calculado al límite (5–15 ms) y un comparador. El usuario prefiere el limitador común.

## Consecuencias

- `docs/02-especificaciones-v2.md` pasa a la v0.3 (SPEC-0007). Cambios:
  - nuevos: ALI-13 y REL-10;
  - redefinidos: REL-01, REL-02, REL-03, REL-04, REL-05, REL-08, ALI-04, ALI-09, ALI-12, AMB-02, FAB-03, FAB-07 y FAB-08;
  - D2 y D8 quedan cerradas.
- **Coste:**
  - la etapa de salidas cuesta 8,33 / 7,86 $ por placa;
  - el limitador común añade ≈ 2–3 $, una estimación que hay que confirmar al elegir la pieza en el esquema;
  - se ahorra el corte general con BTT6030-2ERA (≈ 2,22 $).
- **Pines del ESP32-S3**, como nota para el esquema:
  - 6 IN y 6 DEN (o 3 DEN y 3 DSEL con BTT6030-2ERA);
  - 1 ADC1 para las IS;
  - la habilitación y el fallo del limitador;
  - 1 ADC1 para IMON, si la tiene.
  
  Si faltan GPIO, los DEN pueden ir a un expansor I²C.
- **jr-conformidad** confirma el tipo y el stock de montaje en JLCPCB del BTT6050, del BTT6030 y del limitador elegido cuando pasen al esquema.
- **SPEC-0008** (propuesta) corrige el texto del estudio con los hallazgos B de VAL-0005-01.
