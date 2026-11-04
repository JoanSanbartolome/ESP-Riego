# Trazabilidad de requisitos

<!-- Generado por herramientas/gestion.py: no editar a mano. -->

Requisitos de `docs/02-especificaciones-v2.md`: 55.

| Prioridad | sin cubrir | planificado | en curso | cubierto |
|---|---|---|---|---|
| M | 14 | 0 | 0 | 26 |
| S | 6 | 0 | 0 | 6 |
| C | 1 | 0 | 0 | 2 |

| Requisito | P | Descripción | Specs | Commits | Validación | Estado |
|---|---|---|---|---|---|---|
| ALI-01 | M | Entrada única de 24 V DC nominales desde una fuente de alimentación… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 3: `377dc07`, `b9e0032`, `29ba41e` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| ALI-02 | M | Borne atornillado de 2 polos (5,08 mm) para la entrada. | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 3: `377dc07`, `b9e0032`, `29ba41e` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| ALI-03 | M | Protección contra inversión de polaridad de bajas pérdidas (P-MOSFE… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md), [SPEC-0007](specs/SPEC-0007-requisitos-v03.md) | 4: `73d619a`, `377dc07`, `9fec5cd` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| ALI-04 | M | Protección de entrada: fusible (PTC o SMD) y TVS unidireccional con… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md), [SPEC-0007](specs/SPEC-0007-requisitos-v03.md) | 4: `73d619a`, `377dc07`, `b9e0032` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| ALI-05 | M | Buck de 5 V ≥ 1,5 A. Su VIN máxima, y la tensión nominal de los con… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 2: `377dc07`, `b9e0032` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| ALI-06 | M | UVLO del buck ajustable por divisor y con histéresis, referido a la… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 3: `377dc07`, `b9e0032`, `29ba41e` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| ALI-07 | M | Raíl de 3,3 V propio (LDO ≥ 800 mA desde 5 V, o buck) para el ESP32… | — | — | — | sin cubrir |
| ALI-08 | M | El USB-C alimenta la lógica para programar sin fuente externa. Se u… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 2: `377dc07`, `b9e0032` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| ALI-09 | S | Medida de VIN con divisor en un canal ADC1, para avisar en Home Ass… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md), [SPEC-0007](specs/SPEC-0007-requisitos-v03.md) | 4: `73d619a`, `377dc07`, `b9e0032` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| ALI-10 | S | LED de alimentación. | — | — | — | sin cubrir |
| ALI-11 | S | Test points en VIN, 5 V, 3,3 V y GND. | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 2: `377dc07`, `b9e0032` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| ALI-12 | M | Presupuesto de potencia: fuente de hasta 5 A a 24 V DC (120 W). Las… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md), [SPEC-0007](specs/SPEC-0007-requisitos-v03.md) | 3: `73d619a`, `377dc07`, `b9e0032` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| MCU-01 | M | ESP32-S3-WROOM-1 (N8 o superior, antena PCB) soldado en la placa. | — | — | — | sin cubrir |
| MCU-02 | M | Antena en el borde de la placa, con zona libre de cobre en todas la… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 2: `377dc07`, `b9e0032` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| MCU-03 | M | USB-C nativo (GPIO19/20, USB-Serial/JTAG) con protección ESD (p. ej… | — | — | — | sin cubrir |
| MCU-04 | M | Pulsadores BOOT (GPIO0) y RESET (EN) con red RC en EN. | — | — | — | sin cubrir |
| MCU-05 | M | Asignación de pines: entradas analógicas solo en ADC1 (GPIO1–GPIO10… | — | — | — | sin cubrir |
| MCU-06 | S | Conector UART (TX/RX/GND/3V3) como alternativa de programación y de… | — | — | — | sin cubrir |
| MCU-07 | S | LED de estado controlado por firmware. | — | — | — | sin cubrir |
| REL-01 | M | Al menos 6 salidas en la placa (6 en esta versión), ampliables con… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md), [SPEC-0005](specs/SPEC-0005-estudio-salidas.md) | 7: `c74fd4b`, `e10a97d`, `204dc87` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES), VAL-0005-01 (APROBADO_CON_OBSERVACIONES) | cubierto |
| REL-02 | M | Solo baja tensión en las salidas: ≤ 32 V AC / 36 V DC, incluida una… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 3: `377dc07`, `b9e0032`, `29ba41e` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| REL-03 | M | Accionamiento directo desde GPIO (o desde un expansor), con la prot… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md), [SPEC-0005](specs/SPEC-0005-estudio-salidas.md), [SPEC-0007](specs/SPEC-0007-requisitos-v03.md) | 9: `c74fd4b`, `49bea58`, `ad8e5bc` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES), VAL-0005-01 (APROBADO_CON_OBSERVACIONES) | cubierto |
| REL-04 | M | Estado seguro: salidas desactivadas durante el arranque, el reset y… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 2: `377dc07`, `b9e0032` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| REL-05 | M | Al menos 1 A continuo por canal (dos electroválvulas en paralelo) y… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md), [SPEC-0005](specs/SPEC-0005-estudio-salidas.md), [SPEC-0007](specs/SPEC-0007-requisitos-v03.md) | 10: `c74fd4b`, `49bea58`, `ad8e5bc` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES), VAL-0005-01 (APROBADO_CON_OBSERVACIONES) | cubierto |
| REL-06 | M | Mismo orden de pines en los 6 bornes, coherente entre esquema, PCB… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 3: `377dc07`, `b9e0032`, `29ba41e` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| REL-07 | S | LED indicador por canal. | — | — | — | sin cubrir |
| REL-08 | S | Opción de alimentar las válvulas desde la entrada de 24 V DC (salid… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md), [SPEC-0007](specs/SPEC-0007-requisitos-v03.md) | 8: `49bea58`, `ad8e5bc`, `e10a97d` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| REL-09 | M | Salidas repartidas en dos bordes opuestos: canales 1–3 en el borde… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 3: `377dc07`, `b9e0032`, `29ba41e` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| AMB-01 | M | Sensor de temperatura y humedad I²C en la placa (SHT4x o similar),… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 3: `377dc07`, `b9e0032`, `29ba41e` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| AMB-02 | M | Aislamiento térmico del sensor: en un borde de la placa, lejos del… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md), [SPEC-0007](specs/SPEC-0007-requisitos-v03.md) | 4: `73d619a`, `377dc07`, `b9e0032` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| AMB-03 | C | Sonda externa opcional por el conector I²C de expansión (EXP-02), p… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 3: `377dc07`, `b9e0032`, `29ba41e` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| EXP-01 | S | 1 entrada digital o de pulsos, protegida, para un caudalímetro o un… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 3: `377dc07`, `b9e0032`, `29ba41e` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| EXP-02 | M | Conector de expansión con ESD: I²C, alimentación, al menos 2 GPIO (… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md), [SPEC-0006](specs/SPEC-0006-viabilidad-expansion.md) | 3: `377dc07`, `b9e0032`, `29ba41e` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| EXP-03 | C | Pulsadores de accionamiento manual por canal (retoma la hoja `Panel… | — | — | — | sin cubrir |
| EXP-04 | M | Ampliación de canales con un módulo de expansión. Antes de fijar EX… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md), [SPEC-0006](specs/SPEC-0006-viabilidad-expansion.md) | 3: `377dc07`, `b9e0032`, `29ba41e` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| FAB-01 | M | 2 capas, FR-4 de 1,6 mm, cobre de 1 oz (2 oz a evaluar según REL-05… | — | — | — | sin cubrir |
| FAB-02 | M | Reglas compatibles con JLCPCB estándar y con margen: pista y separa… | — | — | — | sin cubrir |
| FAB-03 | M | Clases de red `Default` (0,25 mm), `Power` (≥ 0,6 mm), `Power_In` (… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md), [SPEC-0007](specs/SPEC-0007-requisitos-v03.md) | 4: `73d619a`, `377dc07`, `b9e0032` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| FAB-04 | M | Plano de GND continuo en ambas caras con cosido de vías; sin cortes… | — | — | — | sin cubrir |
| FAB-05 | M | SMD mínimo 0603 (sin 0402). Cada componente con campo `LCSC Part#`… | — | — | — | sin cubrir |
| FAB-06 | M | Componentes THT (relés si los hay, bornes) en la cara superior, sol… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 2: `377dc07`, `b9e0032` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| FAB-07 | M | Conectores de campo en los bordes superior e inferior: salidas segú… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md), [SPEC-0007](specs/SPEC-0007-requisitos-v03.md) | 4: `73d619a`, `377dc07`, `b9e0032` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| FAB-08 | M | Ancho ≤ 100 mm; el alto se fija al cerrar D8 (≈ 65–95 mm según la t… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md), [SPEC-0007](specs/SPEC-0007-requisitos-v03.md) | 4: `73d619a`, `377dc07`, `b9e0032` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| FAB-09 | M | Serigrafía con la función de cada borne, polaridades, tensión máxim… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 2: `377dc07`, `b9e0032` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| FAB-10 | C | Barniz conformado si el recinto es húmedo, con los conectores y el… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 3: `377dc07`, `b9e0032`, `29ba41e` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| FAB-11 | M | Modelo 3D de todos los componentes, para comprobar el encaje en la… | — | — | — | sin cubrir |
| KIC-01 | M | KiCad 10. Librerías propias dentro del repositorio con rutas `${KIP… | — | — | — | sin cubrir |
| KIC-02 | M | Esquema jerárquico por bloques: alimentación, MCU, salidas, sensore… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 2: `377dc07`, `b9e0032` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| KIC-03 | M | Antes de fabricar: ERC sin errores, y DRC sin errores ni incidencia… | — | — | — | sin cubrir |
| KIC-04 | S | Reglas en `.kicad_dru` (clases de red, zona de antena, separación d… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 2: `377dc07`, `b9e0032` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| KIC-05 | S | Salidas de fabricación generadas con `kicad-cli`, para que sean rep… | — | — | — | sin cubrir |
| FW-01 | M | Configuración ESPHome en `firmware/`, con las credenciales en `secr… | — | — | — | sin cubrir |
| FW-02 | M | Pinout del YAML derivado del esquema v2 y comprobado durante la val… | — | — | — | sin cubrir |
| FW-03 | S | Supervisión de la alimentación (subtensión y sobretensión, ALI-09),… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | 3: `377dc07`, `b9e0032`, `29ba41e` | VAL-0004-02 (APROBADO_CON_OBSERVACIONES) | cubierto |
| FW-04 | S | Tiempo máximo de riego por canal en el firmware (protección ante fa… | — | — | — | sin cubrir |
