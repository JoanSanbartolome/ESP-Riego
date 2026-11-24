# Decisiones vigentes

Una regla por fila, sacada del texto de un DEC o de sus secciones «Tras …», sin otra posterior que la contradiga (SPEC-0039). Los agentes leen esta tabla y no los DEC sueltos, salvo que la spec los cite. Los DEC no se reescriben: su frontmatter dice `aceptada`, `modificada` (con `modificada_por`) o `sustituida`. La comprueba `python herramientas/gestion.py comprobar`.

| tema | regla vigente | DEC | requisitos |
|---|---|---|---|
| orquestación | Un coordinador y agentes en estrella: los agentes no se comunican entre sí y toda orden y entrega pasa por el coordinador y por archivos del repositorio. | DEC-0001 | — |
| orquestación | Una rama por spec (`spec/SPEC-NNNN-<slug>`), integrada en `main` con `merge --no-ff` solo con `APROBADO` o `APROBADO_CON_OBSERVACIONES`. | DEC-0001 | — |
| orquestación | El usuario aprueba el desglose de cada fase, las etiquetas de hito y los push a GitHub (nota 1). | DEC-0001 | — |
| orquestación | Los commits llevan los trailers del proyecto (`Spec`, `Agente`, `Requisitos`, `Log`, `Validacion`), que valida el hook `commit-msg`. | DEC-0001 | — |
| orquestación | Revisión independiente: quien diseña no valida, y validación revisa los artefactos con checklists versionadas. | DEC-0001, DEC-0009 | — |
| orquestación | Una spec por bloque o por hito de layout, con pasos internos, comprobaciones automáticas entre pasos y una sola validación al final. | DEC-0009 | — |
| orquestación | Validación por niveles: `ligero` para texto, documentación, proceso y correcciones; `completo` para piezas, esquema, layout y fabricación; ante la duda, completo. | DEC-0005 | — |
| orquestación | El coordinador repasa la spec con su checklist antes de encargarla, y el autor repasa la de su trabajo antes de entregar. | DEC-0005 | — |
| orquestación | Las M que afectan a la spec siguiente se corrigen antes del merge; las B y las M que no bloquean van a la spec de mantenimiento de la fase. | DEC-0005 | — |
| orquestación | Las ediciones del coordinador en su zona se hacen sin agente ni validación propia, salvo que cambien `docs/02`, que pasa por una spec con validación ligera. | DEC-0005 | — |
| orquestación | Las correcciones y revalidaciones continúan la misma instancia del agente (`SendMessage`); un paso nuevo arranca otra. | DEC-0009 | — |
| orquestación | Cada hecho se registra en el parte (40 líneas como máximo), el informe y el commit; `ESTADO.md` sustituye al diario y validación no escribe parte. | DEC-0009 | — |
| orquestación | El trámite del coordinador va por `gestion.py` (`abrir`, `revisar`, `integrar`, `cerrar`), con tokens, acciones y minutos de cada arranque en el registro de la spec. | DEC-0009 | — |
| orquestación | Los agentes responden solo con el contrato de salida; el coordinador responde de forma concisa y, al cerrar cada spec, recuerda abrir sesión nueva o compactar. | DEC-0005 | — |
| orquestación | Las herramientas de diseño están versionadas en `herramientas/kicad/` y las usan igual autores y validación. | DEC-0009 | — |
| orquestación | Un solo agente carga un proyecto en el MCP a la vez; las escrituras por script sobre archivos y `kicad-cli` sobre copias no cuentan. | DEC-0009 | — |
| orquestación | La guarda no se endurece más: TFG de solo lectura, git solo para el coordinador y escrituras fuera de zona bloqueadas; la carpeta temporal siempre se puede escribir y el código en línea que no toca el TFG pasa. | DEC-0009 | — |
| orquestación | La guarda lee los scripts de `python` y `node` que se ejecutan y bloquea los que escriben en una ruta literal fuera de la zona del agente. | DEC-0020 | — |
| orquestación | El `.kicad_pro` se versiona cuando cambia. | DEC-0011 | KIC-01 |
| agentes | Tres agentes: `ing-diseno` (esquema, layout y piezas), `jr-conformidad` (tipo y stock, fichas, campos, BOM, CPL y paquete de fabricación) e `ing-validacion`. | DEC-0009 | — |
| agentes | `ing-diseno` e `ing-validacion` llevan `model: opus`, y `jr-conformidad` y la validación ligera, Sonnet; ningún agente se lanza con Fable 5.2 ni se continúa una instancia que arrancó con él. | DEC-0010 | — |
| requisitos | Al menos 6 salidas en la placa, ampliables con un módulo de expansión. | DEC-0002 | REL-01, EXP-04 |
| requisitos | Salidas repartidas en dos bordes: 3 canales en el borde superior y 3 en el inferior. | DEC-0002 | REL-09, FAB-07 |
| requisitos | Sensor de temperatura y humedad en la placa, que mide el aire de la caseta, con corrección calibrada en el firmware. | DEC-0002 | AMB-01, AMB-02, AMB-03 |
| requisitos | Sin sensor de nivel. | DEC-0002 | — |
| requisitos | Instalación en interior, en una caja ventilada colgada en la pared. | DEC-0002 | FAB-10 |
| requisitos | Las 6 salidas pueden estar activas a la vez. | DEC-0002 | ALI-12, REL-05 |
| requisitos | Ante un corte de la fuente basta con que Home Assistant vea la placa «no disponible»: sin reserva de energía. | DEC-0002 | ALI-09, FW-03 |
| requisitos | Sin entrada de pulsos ni de lluvia. | DEC-0011 | — |
| requisitos | 6 pulsadores manuales en la placa, uno por salida, en fila en el centro, que lee el firmware con antirrebote sin actuar directamente sobre la salida. | DEC-0011 | EXP-03 |
| requisitos | El diseño no se hace a medida de una válvula: la placa publica sus límites de uso en una tabla, como un manual. | DEC-0014 | REL-11 |
| requisitos | El módulo de expansión lleva su propia entrada de 24 V y su propio limitador, y EXP-02 no lleva 24 V. | DEC-0012, DEC-0014 | EXP-05 |
| requisitos | Esquema legible: subhoja «Canal» repetida 6 veces, un recuadro por bloque con nombre, referencias y requisitos, cables dentro del bloque, etiquetas solo para lo que sale y rejilla de 1,27 mm. | DEC-0015 | KIC-02, KIC-06 |
| alimentación | Fuente LED de 24 V DC y 5 A de tensión constante, en su ajuste de fábrica de 24 V; la placa funciona entre 18 y 30 V. | DEC-0004 | ALI-01 |
| alimentación | La polaridad inversa se rechaza con Q1, D1 y R1 (el N-MOSFET externo de U1). | DEC-0018 | ALI-03 |
| alimentación | TVS SMBJ33A, con su ruptura mínima (36,7 V) por encima de la OVP máxima supuesta (33,6 V); limitador y nodo de entrada de ≥ 60 V. | DEC-0004 | ALI-04, ALI-05 |
| alimentación | Limitador común TPS26632RGER entre las protecciones de entrada y los *high-side*; el buck se alimenta antes del limitador. | DEC-0003, DEC-0006 | ALI-13, REL-08 |
| alimentación | Banda del limitador de 3,5–4,9 A: no actúa con la carga instalada máxima y, con la lógica, queda por debajo de los 5,14 A de la fuente. | DEC-0004 | ALI-12, ALI-13 |
| alimentación | Puente de soldadura de `VIN_PROT` a `BUS_24V` para 4,9 A, abierto por defecto con U1 montado. | DEC-0006 | ALI-13 |
| alimentación | UVLO con divisor de 100 kΩ / 10 kΩ: arranque a 13,5 V nominales (12,50–14,56 V). | DEC-0006 | ALI-06 |
| alimentación | Consumo de la lógica ≤ 4,8 W en la entrada (≤ 0,2 A a 24 V), con el 5 V de la expansión incluido. | DEC-0004 | ALI-12 |
| alimentación | Fusible y `Power_In` para 5,1 A continuos a 50 °C sin actuar. | DEC-0004 | ALI-12, FAB-03 |
| alimentación | Avisos de VIN a 17 V y 31 V con la medida a ± 3 %; R15 sigue en 4,87 kΩ al 0,1 %. | DEC-0004, DEC-0018 | ALI-09 |
| alimentación | U4 es Diodes AP2114H-3.3TRG1 (C150716), con el patillaje de SOT-223. | DEC-0018 | ALI-07, ALI-08 |
| alimentación | C3 y C8 se quedan en 220 nF 100 V X7R (C513710). | DEC-0018 | ALI-05 |
| salidas | *High-side* Infineon BTT6050-1ERA (C534868) en cada canal, con su protección y su diagnóstico; segunda fuente BTT6030-2ERA y reserva BSP752R. | DEC-0003 | REL-01, REL-03, REL-10 |
| salidas | Solo salida alimentada, sin contacto libre de potencial. | DEC-0003 | REL-02, REL-08 |
| salidas | Una válvula (una carga) por salida, con 1 A continuo por salida como límite de uso en la serigrafía. | DEC-0014 | REL-05, FAB-09 |
| salidas | La suma de las salidas activas a la vez es ≤ 3,5 A, la carga instalada máxima. | DEC-0014 | ALI-12, ALI-13 |
| salidas | Sin protección por canal: la pista, el borne y el retorno de cada salida soportan 4,9 A con ΔT ≤ 40 °C (≈ 1,2 mm con 1 oz). | DEC-0004 | REL-05, FAB-03 |
| salidas | Ante un corto, el firmware identifica el canal (IS, DEN y fallo del limitador), lo deja apagado y rearma los demás en ≤ 5 s. | DEC-0003 | REL-08 |
| salidas | El bus de las salidas se habilita mientras riega algún canal y durante la comprobación de carga abierta. | DEC-0004 | REL-10, ALI-13 |
| salidas | Rueda libre D12–D17 (M7, C95872) montada en las seis salidas. | DEC-0014 | REL-03 |
| salidas | DEN común (OUT_DEN, GPIO38) a los 6 BTT6050, con R_DEN de 10 kΩ por canal y R_PD de 100 kΩ; cada IS en su canal de ADC1. | DEC-0007 | REL-10, MCU-05 |
| salidas | Separación de 0,6 mm en la clase `Salidas` cuando un objeto es un pad de U7–U12, R57–R62 o C33–C38 o está en su patio, y 1 mm en el resto, escrita en las reglas de diseño. | DEC-0008 | FAB-03 |
| salidas | C27–C38 son de 100 nF 100 V Basic (C28233). | DEC-0018 | REL-10 |
| MCU | LED de estado D5 rojo (KT-0603R, C2286), con la serigrafía «STATUS». | DEC-0008 | MCU-07 |
| MCU | GPIO39 es `BTN_INT`, y GPIO10, 18 y 37 quedan libres. | DEC-0013 | MCU-05 |
| sensores | El SHT40 (0x44) y el TCA9554 (0x20) comparten el bus I²C de la placa a 100 kHz, con el riesgo de bloqueo aceptado. | DEC-0013 | AMB-01 |
| conectores | Bornes de salida de 2 polos (OUT_n y GND). | DEC-0003 | FAB-07 |
| conectores | Expansión por I²C con TCA9535 y ADS1115 en el módulo, cuyo diseño queda fuera de la v2. | DEC-0012 | EXP-02, EXP-04 |
| conectores | J10 es una cabecera IDC 2 × 5 de 2,54 mm polarizada BH254R-10P (C492448), horizontal y al ras del borde inferior, con el pinout de `viabilidad-expansion.md` §10. | DEC-0012, DEC-0017 | EXP-02, FAB-07 |
| conectores | En EXP-02, 5 V y 3,3 V por sendos TPS2553, ESD con dos USBLC6-2SC6 y *pull-ups* de 2,2 kΩ en el lado del conector. | DEC-0012 | EXP-02 |
| conectores | Pulsadores leídos por un TCA9554PWR (C477924) en 0x20, a GND con sus *pull-ups* internos de 100 kΩ e INT en GPIO39 con 10 kΩ a +3V3; respaldo PCA9554PWR (C2873588). | DEC-0013 | EXP-03, FW-04 |
| colocación | Criterios por orden: fabricación de la clase más barata de JLCPCB, serigrafía legible, diseño térmico en la distribución y tamaño como variable. | DEC-0016 | FAB-02, FAB-05, FAB-09, AMB-02, MCU-02 |
| colocación | Placa de 100 × 100 mm, que no crece; la caja (D5) se diseña cuando la PCB esté terminada. | DEC-0016, DEC-0019 | FAB-08 |
| colocación | Cuerpo de cada pieza a ≥ 2,5 mm del borde, salvo J2, el extremo de la antena de U5 y J10, al ras. | DEC-0016, DEC-0017 | FAB-07 |
| colocación | La antena de U5 va completamente dentro de la placa, en el borde lateral, con su zona libre de cobre. | DEC-0016 | MCU-02 |
| colocación | Cobre de disipación con +10 % de margen (U1, U4, Q1 y BTT6050) y +5 % en U2. | DEC-0016 | AMB-02 |
| colocación | El TCA9554 va junto a la fila de pulsadores, en el centro de la placa. | DEC-0013 | EXP-03 |
| colocación | Resto de la fase 4, por orden: aplicar b4 a la PCB con la imagen aprobada; clases de red y `.kicad_dru`; rutado (potencia y salidas, analógica, señales y planos); cierre con DRC 0, paridad 0 y 3D. | DEC-0019 | FAB-02, FAB-03, FAB-08, KIC-04 |
| coste | Cambios de pieza sin consulta si hacen la placa más fácil o más barata de fabricar sin empeorar ninguna especificación; se anotan en el documento del bloque. | DEC-0007 | — |
| coste | Se aplican P1 (D1–D3 de hongjiacheng), P2 (THT a mano), P3 (C27–C38 a 100 nF) y P4 (U4 AP2114H); P5 se retira. | DEC-0018 | ALI-03, ALI-04, ALI-07, FAB-06 |
| coste | Coste aceptado del bloque del limitador: ≈ 8,9 $ por placa en tandas de 5. | DEC-0006 | ALI-13 |
| fabricación | Reglas de la clase estándar de 2 capas de JLCPCB, con su página y fecha; si FAB-02 es más estricto, manda FAB-02. | DEC-0016 | FAB-02 |
| fabricación | Cobre de 1 oz, provisional: el rutado hace el diseño térmico y propone 2 oz, con su coste, si no basta. | DEC-0019 | FAB-01 |
| fabricación | Los THT (J1, J3, J4–J9 y J10) quedan fuera del montaje de JLCPCB: los compra y los suelda el usuario. | DEC-0018 | FAB-06 |
| fabricación | Sin rieles; para J2 y U5, al ras del borde, se confirma en la revisión DFM antes del pedido. | DEC-0019 | FAB-02 |

**Nota 1.** El push de `main` tras cada merge está autorizado por el manual (`gestion/README.md`, paso 8, desde SPEC-0026) sin un DEC que lo recoja.
