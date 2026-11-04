# Trazabilidad de requisitos

<!-- Generado por herramientas/gestion.py: no editar a mano. -->

Requisitos de `docs/02-especificaciones-v2.md`: 54.

| Prioridad | sin cubrir | planificado | en curso | cubierto |
|---|---|---|---|---|
| M | 21 | 0 | 17 | 0 |
| S | 8 | 0 | 5 | 0 |
| C | 1 | 0 | 2 | 0 |

| Requisito | P | Descripción | Specs | Commits | Validación | Estado |
|---|---|---|---|---|---|---|
| ALI-01 | M | Entrada principal de 24 V AC nominales desde el transformador de ri… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| ALI-02 | M | Borne atornillado de 2 polos (5,08 mm) para la entrada. | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| ALI-03 | M | Puente rectificador de onda completa, que además hace la entrada in… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| ALI-04 | M | Protección de entrada: fusible (PTC o SMD) y TVS dimensionada para… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| ALI-05 | M | Buck de 5 V ≥ 1,5 A con VIN máximo ≥ 60 V, para soportar con margen… | — | — | — | sin cubrir |
| ALI-06 | M | UVLO del buck ajustable por divisor y con histéresis, por debajo de… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| ALI-07 | M | Raíl de 3,3 V propio (LDO ≥ 800 mA desde 5 V, o buck) para el ESP32… | — | — | — | sin cubrir |
| ALI-08 | M | El USB-C alimenta la lógica para programar sin fuente externa. Se u… | — | — | — | sin cubrir |
| ALI-09 | S | Medida de la tensión rectificada con divisor en un canal ADC1, para… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| ALI-10 | S | LED de alimentación. | — | — | — | sin cubrir |
| ALI-11 | S | Test points en la tensión rectificada, 5 V, 3,3 V y GND. | — | — | — | sin cubrir |
| MCU-01 | M | ESP32-S3-WROOM-1 (N8 o superior, antena PCB) soldado en la placa. | — | — | — | sin cubrir |
| MCU-02 | M | Antena en el borde de la placa, con zona libre de cobre en todas la… | — | — | — | sin cubrir |
| MCU-03 | M | USB-C nativo (GPIO19/20, USB-Serial/JTAG) con protección ESD (p. ej… | — | — | — | sin cubrir |
| MCU-04 | M | Pulsadores BOOT (GPIO0) y RESET (EN) con red RC en EN. | — | — | — | sin cubrir |
| MCU-05 | M | Asignación de pines: entradas analógicas solo en ADC1 (GPIO1–GPIO10… | — | — | — | sin cubrir |
| MCU-06 | S | Conector UART (TX/RX/GND/3V3) como alternativa de programación y de… | — | — | — | sin cubrir |
| MCU-07 | S | LED de estado controlado por firmware. | — | — | — | sin cubrir |
| REL-01 | M | 6 salidas. La tecnología de conmutación (relé electromecánico, SSR,… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md), [SPEC-0005](specs/SPEC-0005-estudio-salidas.md) | 1: `eb860b5` | — | en curso |
| REL-02 | M | Solo baja tensión en las salidas: ≤ 30 V AC / 36 V DC, nada de 230… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| REL-03 | M | Accionamiento directo desde GPIO (o desde un expansor), con la prot… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md), [SPEC-0005](specs/SPEC-0005-estudio-salidas.md) | 1: `eb860b5` | — | en curso |
| REL-04 | M | Estado seguro: salidas desactivadas durante el arranque, el reset y… | — | — | — | sin cubrir |
| REL-05 | M | Al menos 1 A continuo por canal (dos electroválvulas de 24 V AC en… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md), [SPEC-0005](specs/SPEC-0005-estudio-salidas.md) | 1: `eb860b5` | — | en curso |
| REL-06 | M | Mismo orden de pines en los 6 bornes, coherente entre esquema, PCB… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| REL-07 | S | LED indicador por canal. | — | — | — | sin cubrir |
| REL-08 | S | Opción de alimentar las válvulas desde la entrada de 24 V AC (salid… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| REL-09 | M | Salidas repartidas en dos bordes opuestos: canales 1–3 en el borde… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| AMB-01 | M | Sensor de temperatura y humedad I²C en la placa (SHT4x o similar),… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| AMB-02 | M | Aislamiento térmico del sensor: en un borde de la placa, lejos del… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| AMB-03 | C | Sonda externa opcional por el conector I²C de expansión (EXP-02), p… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| EXP-01 | S | 1 entrada digital o de pulsos, protegida, para un caudalímetro o un… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| EXP-02 | M | Conector de expansión con ESD: I²C, alimentación, al menos 2 GPIO (… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| EXP-03 | C | Pulsadores de accionamiento manual por canal (retoma la hoja `Panel… | — | — | — | sin cubrir |
| EXP-04 | S | Ampliación de canales con un módulo de expansión. Antes de fijar EX… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| FAB-01 | M | 2 capas, FR-4 de 1,6 mm, cobre de 1 oz (2 oz a evaluar según REL-05… | — | — | — | sin cubrir |
| FAB-02 | M | Reglas compatibles con JLCPCB estándar y con margen: pista y separa… | — | — | — | sin cubrir |
| FAB-03 | M | Clases de red `Default` (0,25 mm), `Power` (≥ 0,6 mm), `AC_In` (ent… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| FAB-04 | M | Plano de GND continuo en ambas caras con cosido de vías; sin cortes… | — | — | — | sin cubrir |
| FAB-05 | M | SMD mínimo 0603 (sin 0402). Cada componente con campo `LCSC Part#`… | — | — | — | sin cubrir |
| FAB-06 | M | Componentes THT (relés si los hay, bornes) en la cara superior, sol… | — | — | — | sin cubrir |
| FAB-07 | M | Conectores de campo en los bordes superior e inferior: salidas segú… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| FAB-08 | M | Ancho ≤ 100 mm; el alto se fija al cerrar D8 (≈ 65–95 mm según la t… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| FAB-09 | M | Serigrafía con la función de cada borne, polaridades, tensión máxim… | — | — | — | sin cubrir |
| FAB-10 | C | Barniz conformado si el recinto es húmedo, con los conectores y el… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| FAB-11 | M | Modelo 3D de todos los componentes, para comprobar el encaje en la… | — | — | — | sin cubrir |
| KIC-01 | M | KiCad 10. Librerías propias dentro del repositorio con rutas `${KIP… | — | — | — | sin cubrir |
| KIC-02 | M | Esquema jerárquico por bloques: alimentación, MCU, salidas, sensore… | — | — | — | sin cubrir |
| KIC-03 | M | Antes de fabricar: ERC sin errores, y DRC sin errores ni incidencia… | — | — | — | sin cubrir |
| KIC-04 | S | Reglas en `.kicad_dru` (clases de red, zona de antena, separación d… | — | — | — | sin cubrir |
| KIC-05 | S | Salidas de fabricación generadas con `kicad-cli`, para que sean rep… | — | — | — | sin cubrir |
| FW-01 | M | Configuración ESPHome en `firmware/`, con las credenciales en `secr… | — | — | — | sin cubrir |
| FW-02 | M | Pinout del YAML derivado del esquema v2 y comprobado durante la val… | — | — | — | sin cubrir |
| FW-03 | S | Supervisión de la alimentación (fallo del transformador), de la tem… | [SPEC-0004](specs/SPEC-0004-requisitos-v02.md) | — | — | en curso |
| FW-04 | S | Tiempo máximo de riego por canal en el firmware (protección ante fa… | — | — | — | sin cubrir |
