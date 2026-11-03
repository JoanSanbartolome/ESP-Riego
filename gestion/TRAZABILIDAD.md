# Trazabilidad de requisitos

<!-- Generado por herramientas/gestion.py: no editar a mano. -->

Requisitos de `docs/02-especificaciones-v2.md`: 61.

| Prioridad | sin cubrir | planificado | en curso | cubierto |
|---|---|---|---|---|
| M | 41 | 0 | 0 | 0 |
| S | 15 | 0 | 0 | 0 |
| C | 5 | 0 | 0 | 0 |

| Requisito | P | Descripción | Specs | Commits | Validación | Estado |
|---|---|---|---|---|---|---|
| ALI-01 | M | Entrada de 9–30 V DC (nominal 12 V y 24 V: batería, panel solar con… | — | — | — | sin cubrir |
| ALI-02 | M | Borne atornillado de 2 polos (5,08 mm) para la entrada. Un jack DC… | — | — | — | sin cubrir |
| ALI-03 | M | Protección contra inversión de polaridad de bajas pérdidas (P-MOSFE… | — | — | — | sin cubrir |
| ALI-04 | M | Protección de entrada con fusible (PTC o fusible SMD) y TVS unidire… | — | — | — | sin cubrir |
| ALI-05 | M | Buck de 5 V ≥ 1,5 A con VIN máximo ≥ 60 V, para soportar con margen… | — | — | — | sin cubrir |
| ALI-06 | M | UVLO del buck ajustable por divisor; valor por defecto ≈ 8,5 V (v1:… | — | — | — | sin cubrir |
| ALI-07 | M | Raíl de 3,3 V propio (LDO ≥ 800 mA desde 5 V, o buck) para el ESP32… | — | — | — | sin cubrir |
| ALI-08 | M | El USB-C alimenta la lógica para programar sin fuente externa. Se u… | — | — | — | sin cubrir |
| ALI-09 | S | Medida de VIN con divisor en un canal ADC1, para supervisar la bate… | — | — | — | sin cubrir |
| ALI-10 | S | LED de alimentación. | — | — | — | sin cubrir |
| ALI-11 | S | Test points en VIN, 5 V, 3,3 V y GND. | — | — | — | sin cubrir |
| MCU-01 | M | ESP32-S3-WROOM-1 (N8 o superior, antena PCB) soldado en la placa. | — | — | — | sin cubrir |
| MCU-02 | M | Antena en el borde de la placa, con zona libre de cobre en todas la… | — | — | — | sin cubrir |
| MCU-03 | M | USB-C nativo (GPIO19/20, USB-Serial/JTAG) con protección ESD (p. ej… | — | — | — | sin cubrir |
| MCU-04 | M | Pulsadores BOOT (GPIO0) y RESET (EN) con red RC en EN. | — | — | — | sin cubrir |
| MCU-05 | M | Asignación de pines: entradas analógicas solo en ADC1 (GPIO1–GPIO10… | — | — | — | sin cubrir |
| MCU-06 | S | Conector UART (TX/RX/GND/3V3) como alternativa de programación y de… | — | — | — | sin cubrir |
| MCU-07 | S | LED de estado controlado por firmware. | — | — | — | sin cubrir |
| REL-01 | M | 4 canales con relé SPDT de 5 V (SRD-05VDC-SL-C o equivalente) y bor… | — | — | — | sin cubrir |
| REL-02 | M | Solo baja tensión en contactos: ≤ 30 V DC / 24 V AC, nada de 230 V… | — | — | — | sin cubrir |
| REL-03 | M | Driver con N-MOSFET de nivel lógico (o driver integrado) gobernado… | — | — | — | sin cubrir |
| REL-04 | M | Estado seguro: relés desactivados durante el arranque, el reset y e… | — | — | — | sin cubrir |
| REL-05 | M | Pistas de contacto dimensionadas para 5 A continuos con ΔT ≤ 10 °C… | — | — | — | sin cubrir |
| REL-06 | M | Mismo orden de pines en los 4 bornes, coherente entre esquema y PCB. | — | — | — | sin cubrir |
| REL-07 | S | LED indicador por canal. | — | — | — | sin cubrir |
| REL-08 | C | Puente opcional para alimentar los comunes desde VIN, con fusible,… | — | — | — | sin cubrir |
| NIV-01 | M | Fuente de lazo dedicada de 24 V (boost), para garantizar ≥ 12 V en… | — | — | — | sin cubrir |
| NIV-02 | M | Limitación de corriente del lazo (≈ 25–30 mA), para que un cortocir… | — | — | — | sin cubrir |
| NIV-03 | M | Resistencia de carga de precisión (0,1 %, ≤ 25 ppm/°C) dimensionada… | — | — | — | sin cubrir |
| NIV-04 | M | Filtro RC de impedancia moderada (p. ej. 10 kΩ + 2,2 µF, fc ≈ 7 Hz)… | — | — | — | sin cubrir |
| NIV-05 | M | Entrada en un canal ADC1 y TVS en el borne del lazo. | — | — | — | sin cubrir |
| NIV-06 | S | Detección de fallo en firmware: < 3,6 mA (lazo abierto) y > 21 mA (… | — | — | — | sin cubrir |
| NIV-07 | C | ADC externo (ADS1115, I²C) si la precisión del ADC interno no basta. | — | — | — | sin cubrir |
| NIV-08 | C | Segundo canal 4–20 mA para un segundo depósito. | — | — | — | sin cubrir |
| AMB-01 | M | Sensor I²C fuera de la caja (SHT4x o similar, en módulo con protect… | — | — | — | sin cubrir |
| AMB-02 | M | Conector de 4 polos (3V3, GND, SDA, SCL) con protección ESD y pull-… | — | — | — | sin cubrir |
| AMB-03 | S | Cable de ≤ 2 m. Para más distancia, valorar un extensor I²C o un se… | — | — | — | sin cubrir |
| AMB-04 | C | Compatibilidad con 1-Wire (DS18B20) en el mismo conector mediante p… | — | — | — | sin cubrir |
| EXP-01 | S | 1 entrada digital o de pulsos de 5–24 V, protegida, para caudalímet… | — | — | — | sin cubrir |
| EXP-02 | S | Conector de expansión con I²C, 2 GPIO, 3V3 y GND. | — | — | — | sin cubrir |
| EXP-03 | C | Pulsadores de accionamiento manual por canal (retoma la hoja `Panel… | — | — | — | sin cubrir |
| FAB-01 | M | 2 capas, FR-4 de 1,6 mm, cobre de 1 oz (2 oz a evaluar según REL-05… | — | — | — | sin cubrir |
| FAB-02 | M | Reglas compatibles con JLCPCB estándar y con margen: pista y separa… | — | — | — | sin cubrir |
| FAB-03 | M | Clases de red `Default` (0,25 mm), `Power` (≥ 0,6 mm), `Relay_Load`… | — | — | — | sin cubrir |
| FAB-04 | M | Plano de GND continuo en ambas caras con cosido de vías; sin cortes… | — | — | — | sin cubrir |
| FAB-05 | M | SMD mínimo 0603 (sin 0402). Cada componente con campo `LCSC Part#`… | — | — | — | sin cubrir |
| FAB-06 | M | Componentes THT (relés, bornes) en la cara superior, soldados a man… | — | — | — | sin cubrir |
| FAB-07 | M | Conectores de campo en un único borde, de cara a los prensaestopas. | — | — | — | sin cubrir |
| FAB-08 | M | Dimensiones objetivo ≤ 100 × 80 mm (v1: 129 × 96,5 mm) con 4 taladr… | — | — | — | sin cubrir |
| FAB-09 | M | Serigrafía con la función de cada borne, polaridades, tensión máxim… | — | — | — | sin cubrir |
| FAB-10 | S | Barniz conformado recomendado para exterior, con los conectores enm… | — | — | — | sin cubrir |
| FAB-11 | M | Modelo 3D de todos los componentes, para comprobar el encaje en la… | — | — | — | sin cubrir |
| KIC-01 | M | KiCad 10. Librerías propias dentro del repositorio con rutas `${KIP… | — | — | — | sin cubrir |
| KIC-02 | M | Esquema jerárquico por bloques: alimentación, MCU, relés, sensores… | — | — | — | sin cubrir |
| KIC-03 | M | Antes de fabricar: ERC sin errores, y DRC sin errores ni incidencia… | — | — | — | sin cubrir |
| KIC-04 | S | Reglas en `.kicad_dru` (clases de red, zona de antena, separación d… | — | — | — | sin cubrir |
| KIC-05 | S | Salidas de fabricación generadas con `kicad-cli`, para que sean rep… | — | — | — | sin cubrir |
| FW-01 | M | Configuración ESPHome en `firmware/`, con las credenciales en `secr… | — | — | — | sin cubrir |
| FW-02 | M | Pinout del YAML derivado del esquema v2 y comprobado durante la val… | — | — | — | sin cubrir |
| FW-03 | S | Supervisión de VIN, del estado del lazo 4–20 mA y de la temperatura… | — | — | — | sin cubrir |
| FW-04 | S | Tiempo máximo de riego por canal en el firmware (protección ante fa… | — | — | — | sin cubrir |
