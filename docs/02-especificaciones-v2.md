# Especificaciones de la PCB v2

**Estado:** borrador v0.2 (2026-11-04). Los cambios respecto a la v0.1 están en [DEC-0002](../gestion/decisiones/DEC-0002-objetivo-v2-revisado.md) y en el [historial](#10-historial).

Decisiones de partida:

- Módulo ESP32-S3 soldado en la placa.
- Alimentación única desde una fuente de 24 V DC de hasta 5 A.
- Instalación en interior (casa o caseta), en una caja ventilada colgada en la pared.
- Solo cargas de baja tensión.
- Montaje SMT en JLCPCB y componentes THT soldados a mano.
- KiCad 10.

## 1. Objetivo

Controlador de riego de **6 salidas**, con temperatura y humedad medidas en la placa e integración en Home Assistant mediante ESPHome. Se alimenta de una fuente de 24 V DC y se monta en interior, en una caja ventilada a la pared.

- Las salidas no quedan atadas a un único tipo de válvula. Su tecnología se decide con un estudio (D8), que tiene en cuenta las electroválvulas instaladas: 24 V DC, ≈ 0,2 A cada una.
- El número de canales se puede ampliar con un módulo de expansión (D9).
- La v2 corrige los hallazgos de [01-analisis-v1.md](01-analisis-v1.md) y se monta en JLCPCB.
- No incluye sensor de nivel de depósito.

## 2. Resumen v1 → v2

| | v1 (TFG) | v2 (objetivo) |
|---|---|---|
| MCU | Wemos S2 Mini enchufable | ESP32-S3-WROOM-1 soldado, USB-C propio |
| Alimentación | 12 V DC por jack, sin protecciones | 24 V DC de una fuente de hasta 5 A, por borne, con protección de polaridad, fusible y TVS |
| Salidas | 4 relés, opto + BC817 | 6 salidas; tecnología según el estudio de SPEC-0005 (D8) |
| Nivel | 4–20 mA alimentado a 12 V | Eliminado |
| Temperatura / humedad | DHT11 en placa | Sensor I²C en placa (SHT4x o similar), aislado térmicamente, que mide el aire de la caseta |
| Expansión | — | Conector para un módulo de más canales (D9) |
| Instalación | Caja estanca | Interior, caja ventilada a la pared |
| Montaje | Todo a mano, 1210 / 0805 | SMT JLCPCB (≥ 0603) + THT a mano |
| Tamaño | 129 × 96,5 mm | ≤ 100 mm de ancho; el alto depende de D8 (≈ 65–95 mm) |
| Herramienta | KiCad 9 | KiCad 10 |

## 3. Arquitectura

```mermaid
flowchart LR
    VIN["Entrada 24 V DC"] --> PROT["Fusible + polaridad + TVS"]
    PROT --> BUCK["Buck 5 V"]
    USB["USB-C"] --> OR["OR VBUS / 5 V"]
    BUCK --> OR
    OR --> LDO["3,3 V"]
    LDO --> MCU["ESP32-S3-WROOM-1"]
    MCU --> OUT["6 salidas (tecnología D8)"]
    OR -. "control o bobinas, según D8" .-> OUT
    PROT -. "salida alimentada (D2)" .-> FOUT["Fusible de salidas"]
    FOUT -.-> OUT
    MCU <--> TH["Sensor T/HR en placa (I²C)"]
    MCU <--> EXP["Conector de expansión (I²C + GPIO)"]
    OR --> EXP
    PULSOS["Entrada de pulsos / lluvia"] --> MCU
    PROT --> VMON["Divisor VIN → ADC1"]
    VMON --> MCU
```

## 4. Requisitos

Prioridad: **M** debe · **S** debería · **C** podría.

### 4.1 Alimentación (ALI)

| ID | P | Requisito |
|---|---|---|
| ALI-01 | M | Entrada única de 24 V DC nominales desde una fuente de alimentación. Rango de funcionamiento de 18 a 30 V DC, para cubrir el ajuste de la fuente y la caída en el cable. |
| ALI-02 | M | Borne atornillado de 2 polos (5,08 mm) para la entrada. |
| ALI-03 | M | Protección contra inversión de polaridad de bajas pérdidas (P-MOSFET o controlador de diodo ideal), dimensionada para la corriente de entrada de ALI-12. |
| ALI-04 | M | Protección de entrada: fusible (PTC o SMD) y TVS unidireccional con tensión de trabajo (VRWM) ≥ 30 V (p. ej. SMBJ33A). |
| ALI-05 | M | Buck de 5 V ≥ 1,5 A. Su VIN máxima, y la tensión nominal de los condensadores y de cada pieza del nodo de entrada, son ≥ la tensión de *clamping* máxima (Vc) de la TVS elegida con un 10 % de margen (orientativo: ≥ 60 V con SMBJ33A, Vc = 53,3 V). Se admite un valor menor solo si `docs/diseno/` justifica una Vc más baja con la corriente de pulso limitada. |
| ALI-06 | M | UVLO del buck ajustable por divisor y con histéresis, referido a la tensión tras las protecciones de entrada: umbral de subida por debajo de 18 V menos la caída de las protecciones, con margen (≈ 15 V), y por encima de la VIN mínima del buck para dar 5 V a 1,5 A. |
| ALI-07 | M | Raíl de 3,3 V propio (LDO ≥ 800 mA desde 5 V, o buck) para el ESP32-S3 y los sensores. |
| ALI-08 | M | El USB-C alimenta la lógica para programar sin fuente externa. Se une al raíl de 5 V con diodo Schottky o ideal para no retroalimentar el PC ni la entrada. Con solo USB no se garantiza el accionamiento de las salidas. |
| ALI-09 | S | Medida de VIN con divisor en un canal ADC1, para avisar en Home Assistant de subtensión o sobretensión de la entrada. El corte total de la fuente se ve como la placa «no disponible»; no se añade reserva de energía (decisión del usuario). |
| ALI-10 | S | LED de alimentación. |
| ALI-11 | S | Test points en VIN, 5 V, 3,3 V y GND. |
| ALI-12 | M | Presupuesto de potencia: fuente de hasta 5 A a 24 V DC (120 W). Las 6 salidas pueden estar activas a la vez; la corriente total de las salidas alimentadas desde la entrada se limita a 4 A, para dejar margen a la lógica. Fusible, protección de polaridad y pistas de entrada (`Power_In`) dimensionados para 5 A. |

### 4.2 Microcontrolador (MCU)

| ID | P | Requisito |
|---|---|---|
| MCU-01 | M | ESP32-S3-WROOM-1 (N8 o superior, antena PCB) soldado en la placa. |
| MCU-02 | M | Antena en el borde de la placa, con zona libre de cobre en todas las capas según la guía de diseño hardware de Espressif, y alejada de las salidas y del buck. |
| MCU-03 | M | USB-C nativo (GPIO19/20, USB-Serial/JTAG) con protección ESD (p. ej. USBLC6-2SC6) y resistencias CC de 5,1 kΩ. |
| MCU-04 | M | Pulsadores BOOT (GPIO0) y RESET (EN) con red RC en EN. |
| MCU-05 | M | Asignación de pines: entradas analógicas solo en ADC1 (GPIO1–GPIO10); sin salidas en pines de arranque (GPIO0, 3, 45, 46); GPIO35–37 libres si el módulo lleva PSRAM octal; GPIO19/20 reservados al USB. |
| MCU-06 | S | Conector UART (TX/RX/GND/3V3) como alternativa de programación y depuración. |
| MCU-07 | S | LED de estado controlado por firmware. |

### 4.3 Salidas de riego (REL)

| ID | P | Requisito |
|---|---|---|
| REL-01 | M | Al menos 6 salidas en la placa (6 en esta versión), ampliables con el módulo de expansión (EXP-04). La tecnología de conmutación (relé electromecánico, SSR, triac o MOSFET) se elige con el estudio de SPEC-0005 (D8). |
| REL-02 | M | Solo baja tensión en las salidas: ≤ 32 V AC / 36 V DC, incluida una fuente externa de las válvulas conectada a un contacto libre (p. ej. un transformador de riego de 24 V AC en vacío). Nada de 230 V AC. Indicado en la serigrafía. |
| REL-03 | M | Accionamiento directo desde GPIO (o desde un expansor), con la protección de la carga inductiva que exija la tecnología elegida (diodo, *snubber* o varistor). Sin optoacoplador, salvo que forme parte de la tecnología elegida (SSR u optotriac). Si la tecnología lleva un LED de control, su corriente queda fijada con margen sobre la IFT máxima en todo el rango de Vf y de 3,3 V (causa de H5). |
| REL-04 | M | Estado seguro: salidas desactivadas durante el arranque, el reset y el flasheo (pull-down en la entrada de control, lógica activa a nivel alto). |
| REL-05 | M | Al menos 1 A continuo por canal (dos electroválvulas en paralelo) y soporte de su corriente de arranque. Las 6 salidas pueden estar activas a la vez, con el total de ALI-12. Los valores definitivos se fijan al cerrar D8. Pistas dimensionadas con ΔT ≤ 10 °C (IPC-2152). |
| REL-06 | M | Mismo orden de pines en los 6 bornes, coherente entre esquema, PCB y serigrafía. |
| REL-07 | S | LED indicador por canal. |
| REL-08 | S | Opción de alimentar las válvulas desde la entrada de 24 V DC (salida alimentada, con fusible y borne común, como los programadores comerciales), y opción de contacto libre de potencial para cargas con su propia fuente (p. ej. válvulas de 24 V AC con su transformador). Qué opciones ofrece la placa y cómo se eligen se decide con D2. Cada salida alimentada lleva protección propia contra cortocircuito, y la lógica aguanta el disparo sin reiniciarse: un corto en el cable de un canal no puede dejar sin alimentación la placa ni los demás canales. |
| REL-09 | M | Salidas repartidas en dos bordes opuestos: canales 1–3 en el borde superior y canales 4–6 en el inferior. |

### 4.4 Temperatura y humedad (AMB)

| ID | P | Requisito |
|---|---|---|
| AMB-01 | M | Sensor de temperatura y humedad I²C en la placa (SHT4x o similar), para medir el aire de la caseta o la habitación donde está la caja, no el interior de la caja. |
| AMB-02 | M | Aislamiento térmico del sensor: en un borde de la placa, lejos del buck, del LDO, del módulo ESP32-S3 y de las salidas, con ranuras fresadas a su alrededor y sin planos de cobre debajo, y orientado hacia las rejillas de la caja. El firmware admite una corrección (*offset*) calibrada contra una referencia. |
| AMB-03 | C | Sonda externa opcional por el conector I²C de expansión (EXP-02), para medir fuera del recinto. |

### 4.5 Entradas y expansión (EXP)

| ID | P | Requisito |
|---|---|---|
| EXP-01 | S | 1 entrada digital o de pulsos, protegida, para un caudalímetro o un sensor de lluvia: de 5 a 24 V o contacto seco. |
| EXP-02 | M | Conector de expansión con ESD: I²C, alimentación, al menos 2 GPIO (una de interrupción), 3V3 y GND. Los pines y tensiones salen del informe de viabilidad (EXP-04) antes de cerrar el esquema. |
| EXP-03 | C | Pulsadores de accionamiento manual por canal (retoma la hoja `Panel_Control` del TFG). |
| EXP-04 | M | Ampliación de canales con un módulo de expansión. Antes de fijar EXP-02 se hace un informe de viabilidad con arquitecturas, componentes y costes (SPEC-0006, D9). |

### 4.6 PCB y fabricación (FAB)

| ID | P | Requisito |
|---|---|---|
| FAB-01 | M | 2 capas, FR-4 de 1,6 mm, cobre de 1 oz (2 oz a evaluar según REL-05), acabado HASL sin plomo o ENIG. |
| FAB-02 | M | Reglas compatibles con JLCPCB estándar y con margen: pista y separación ≥ 0,2 mm, vía 0,3 / 0,6 mm, cobre a borde ≥ 0,5 mm. |
| FAB-03 | M | Clases de red `Default` (0,25 mm), `Power` (≥ 0,6 mm), `Power_In` (entrada y protecciones, 5 A según ALI-12) y `Salidas` (ancho según REL-05, separación ≥ 1 mm). |
| FAB-04 | M | Plano de GND continuo en ambas caras con cosido de vías; sin cortes bajo el buck ni bajo las señales analógicas. |
| FAB-05 | M | SMD mínimo 0603 (sin 0402). Cada componente con campo `LCSC Part#` (preferencia: piezas *Basic* de JLCPCB) y exportación de BOM + CPL para JLCPCB. |
| FAB-06 | M | Componentes THT (relés si los hay, bornes) en la cara superior, soldados a mano o con montaje THT. |
| FAB-07 | M | Conectores de campo en los bordes superior e inferior: salidas según REL-09; en el inferior, también la entrada de alimentación, la entrada de pulsos (EXP-01) y el conector de expansión. Los laterales quedan para la antena (MCU-02), el USB-C (accesible desde fuera) y el sensor de temperatura y humedad (AMB-02). |
| FAB-08 | M | Ancho ≤ 100 mm; el alto se fija al cerrar D8 (≈ 65–95 mm según la tecnología de salida). 4 taladros M3 para fijarla dentro de la caja. |
| FAB-09 | M | Serigrafía con la función de cada borne, polaridades, tensión máxima de las salidas, versión y fecha. |
| FAB-10 | C | Barniz conformado si el recinto es húmedo, con los conectores y el sensor de humedad enmascarados. |
| FAB-11 | M | Modelo 3D de todos los componentes, para comprobar el encaje en la caja. |

### 4.7 Proyecto KiCad (KIC)

| ID | P | Requisito |
|---|---|---|
| KIC-01 | M | KiCad 10. Librerías propias dentro del repositorio con rutas `${KIPRJMOD}`: sin rutas absolutas ni JSON de EasyEDA. |
| KIC-02 | M | Esquema jerárquico por bloques: alimentación, MCU, salidas, sensores y conectores. |
| KIC-03 | M | Antes de fabricar: ERC sin errores, y DRC sin errores ni incidencias de paridad esquema↔PCB. |
| KIC-04 | S | Reglas en `.kicad_dru` (clases de red, zona de antena, separación de las salidas). |
| KIC-05 | S | Salidas de fabricación generadas con `kicad-cli`, para que sean reproducibles. |

### 4.8 Firmware (FW)

| ID | P | Requisito |
|---|---|---|
| FW-01 | M | Configuración ESPHome en `firmware/`, con las credenciales en `secrets.yaml` (no versionado). |
| FW-02 | M | Pinout del YAML derivado del esquema v2 y comprobado durante la validación. |
| FW-03 | S | Supervisión de la alimentación (subtensión y sobretensión, ALI-09), de la temperatura y la humedad del sensor en placa (con la corrección de AMB-02) y de la temperatura interna del ESP32. |
| FW-04 | S | Tiempo máximo de riego por canal en el firmware (protección ante fallos de comunicación). |

## 5. Condiciones ambientales

- Interior (casa o caseta), en una caja ventilada colgada en la pared; no estanca.
- Temperatura de funcionamiento objetivo de −10 a +50 °C (caseta sin climatizar); humedad del 10 al 90 % HR sin condensación.
- Componentes con rango de al menos −20 a +85 °C.

## 6. Criterios de aceptación

Amplían las pruebas del pliego del TFG.

| Prueba | Criterio |
|---|---|
| Barrido de alimentación a 18, 24 y 30 V DC | 5 V y 3,3 V dentro de ±3 %; sin reinicios al conmutar las 6 salidas a la vez |
| Polaridad invertida a 30 V DC | Sin daños |
| Entrada por debajo de 18 V o por encima de 30 V DC | Aviso de subtensión o sobretensión en Home Assistant (ALI-09) |
| Corte total de la fuente | La placa aparece como no disponible en Home Assistant; al volver la tensión, arranca con las salidas desactivadas (REL-04) |
| Salidas | Los 6 canales conmutan una electroválvula real de cada tipo que admita D8 y la corriente de REL-05; quedan desactivados durante el reset y el flasheo |
| Wi-Fi / Home Assistant | Conexión, OTA e integración correctas |
| Temperatura / humedad | Tras calibrar la corrección de AMB-02, lectura coherente (±0,5 °C, ±3 % HR) con una referencia situada en la caseta, fuera de la caja, tras 1 h con las 6 salidas activas |
| Cortocircuito en una salida alimentada | Actúa la protección del canal; la lógica y los demás canales siguen funcionando (REL-08) |
| Térmica | 1 h con las 6 salidas activas y el total de ALI-12 (4 A) repartido entre ellas: ΔT de las pistas ≤ 10 °C |

## 7. Decisiones abiertas

| ID | Decisión | Estado |
|---|---|---|
| D1 | Número de canales | **Cerrada:** 6, ampliables (DEC-0002) |
| D2 | Salida alimentada desde 24 V DC, contacto libre o ambas (REL-08) | Pendiente de SPEC-0005 |
| D3 | Entrada de pulsos o de lluvia (EXP-01) | Por defecto, sí |
| D4 | Pulsadores de forzado manual (EXP-03) | Por defecto, no |
| D5 | Modelo de caja ventilada y medidas internas | Pendiente |
| D6 | Cobre de 1 oz o 2 oz | Por defecto, 1 oz; se revisa con D8 |
| D7 | ADC interno o ADS1115 para el 4–20 mA | **Sin objeto:** se elimina el sensor de nivel (DEC-0002) |
| D8 | Tecnología de las salidas: relé, SSR, triac o MOSFET (REL-01, REL-03, REL-05); las válvulas instaladas son de 24 V DC, ≈ 0,2 A | Pendiente de SPEC-0005 |
| D9 | Arquitectura del módulo de expansión (EXP-02, EXP-04) | Pendiente de SPEC-0006 |

## 8. Trazabilidad con los hallazgos v1

| Hallazgo | Requisitos |
|---|---|
| H1 Esquema y PCB desincronizados | REL-06, KIC-03 |
| H2 ADC2 con Wi-Fi | MCU-05, ALI-09 |
| H3 Lazo 4–20 mA | Sin objeto: se elimina el sensor de nivel (DEC-0002) |
| H4 Alimentación | ALI-01 … ALI-06, ALI-12 |
| H5 Optoacoplador | REL-03, REL-04 |
| H6 DHT11 | AMB-01, AMB-02, AMB-03 (se mide la caseta: DEC-0002, decisión 3) |
| H7 Wemos enchufable | MCU-01, MCU-03, FAB-07 |
| H8 Librerías absolutas | KIC-01 |
| H9 Hojas huérfanas | KIC-02, EXP-03 |
| H10 DRC | KIC-03 |
| H11 Tamaño y encapsulados | FAB-05, FAB-08 |
| H12 Firmware | FW-01, FW-02 |

## 9. Requisitos retirados

Sus IDs no se reutilizan.

| ID | Retirado en | Decisión | Motivo | Requisito en la versión anterior |
|---|---|---|---|---|
| NIV-01 | v0.2 | DEC-0002 | Se elimina el sensor de nivel (DEC-0002, decisión 4) | Fuente de lazo dedicada de 24 V (boost) |
| NIV-02 | v0.2 | DEC-0002 | Se elimina el sensor de nivel (DEC-0002, decisión 4) | Limitación de corriente del lazo |
| NIV-03 | v0.2 | DEC-0002 | Se elimina el sensor de nivel (DEC-0002, decisión 4) | Resistencia de carga de precisión |
| NIV-04 | v0.2 | DEC-0002 | Se elimina el sensor de nivel (DEC-0002, decisión 4) | Filtro RC y clamp antes del ADC |
| NIV-05 | v0.2 | DEC-0002 | Se elimina el sensor de nivel (DEC-0002, decisión 4) | Entrada en ADC1 y TVS en el borne del lazo |
| NIV-06 | v0.2 | DEC-0002 | Se elimina el sensor de nivel (DEC-0002, decisión 4) | Detección de fallo del lazo según NAMUR NE43 |
| NIV-07 | v0.2 | DEC-0002 | Se elimina el sensor de nivel (DEC-0002, decisión 4) | ADC externo ADS1115 |
| NIV-08 | v0.2 | DEC-0002 | Se elimina el sensor de nivel (DEC-0002, decisión 4) | Segundo canal 4–20 mA |
| AMB-04 | v0.2 | DEC-0002 | Ya no hay conector de sonda externa propio: el sensor va en placa (decisión 3) y la sonda opcional usa el I²C de expansión (AMB-03) | Compatibilidad 1-Wire (DS18B20) en el conector del sensor externo |

En la v0.2 se redefinen sin cambiar de ID. Cuando se redefinieron, solo SPEC-0005 citaba alguno (REL-01, REL-03 y REL-05), y ya con el sentido nuevo.

- ALI-01, ALI-02, ALI-04, ALI-05, ALI-06 y ALI-09: de 9–30 V DC con batería o panel solar a una fuente de 24 V DC (18–30 V).
- REL-01 … REL-05 y REL-08: de 4 relés a 6 salidas con tecnología por decidir.
- AMB-01 … AMB-03: de sonda externa a sensor en placa.
- EXP-02, FAB-03, FAB-07, FAB-08, FAB-10 y FW-03.

Cambios de prioridad: REL-08 C → S, EXP-02 S → M, AMB-03 S → C y FAB-10 S → C. Nuevos: REL-09 (M), EXP-04 (M) y ALI-12 (M).

## 10. Historial

| Versión | Fecha | Cambios | Spec · decisión |
|---|---|---|---|
| v0.1 | 2026-11-03 | Primera versión, a partir del análisis de la v1 | SPEC-0000 |
| v0.2 | 2026-11-04 | Interior con caja ventilada; fuente de 24 V DC de hasta 5 A; 6 salidas (3 + 3) que pueden activarse a la vez; T/HR de la caseta medida en placa; sin sensor de nivel; módulo de expansión; D8 y D9; ajustes de VAL-0004-01 | SPEC-0004 · DEC-0002 |
