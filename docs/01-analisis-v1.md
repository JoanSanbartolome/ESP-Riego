# Análisis de la PCB v1 (TFG)

Revisión de la placa *Control_De_Riego* diseñada en el TFG, punto de partida de la v2.

- **Fuente analizada:** carpeta `KiCad_PCB/Control_De_Riego` del TFG (idéntica a `PCB_FINAL.rar`). El original no se ha modificado: el análisis se hizo sobre una copia.
- **Herramientas:** KiCad 10.0.6 (`kicad-cli`: ERC, DRC y paridad esquema↔PCB), lectura directa de los archivos y de la memoria (LaTeX).
- **Fecha:** 2026-11-03.

## 1. Resumen de la placa

| Parámetro | Valor |
|---|---|
| Formato de archivos | KiCad 9 (esquema `20250114`, PCB `20241229`) |
| Dimensiones | 129,0 × 96,5 mm |
| Capas | 2 (F.Cu / B.Cu), FR-4 1,6 mm |
| Componentes | 61 referencias |
| Microcontrolador | Wemos S2 Mini (ESP32-S2FN4R2), enchufable en tiras hembra |
| Alimentación | Jack DC 12 V → TPS54202 (buck 5 V, 2 A) → 3,3 V del LDO del propio Wemos |
| Salidas | 4 relés SRD-05VDC-SL-C (SPDT); optoacoplador PS2705 + BC817 por canal |
| Entradas | Transmisor de nivel 4–20 mA (R15 = 150 Ω, filtro RC 270 kΩ / 100 nF) y DHT11 |
| Pistas | 0,3 mm señal (51), 0,5 mm alimentación (169), 0,7 mm (21), 3 mm cargas (21); 38 vías |
| Jerarquía | Raíz + `Modulo_reles`, `ESP32_S2`, `Alimentacion`, `Conectores y agujeros PCB` |

Pinout del ESP32-S2 según la PCB:

| Señal | Pad Wemos | GPIO |
|---|---|---|
| REL1 … REL4 | 3, 5, 7, 9 | GPIO3, 5, 7, 9 (activas a nivel bajo) |
| TH_Data (DHT11) | 13 | GPIO12 |
| V_Level (4–20 mA) | 24 | GPIO18 (ADC2) |

### Versiones del TFG

`PCB_1_1_0(fabricada).rar`, `PCB_FINAL.rar` y la carpeta de trabajo contienen **el mismo `.kicad_pcb`** (SHA-1 idéntico). Solo cambian los esquemas, que se editaron después de fabricar. Ninguna de las versiones del esquema coincide con la PCB fabricada (ver H1).

## 2. Verificaciones automáticas (KiCad 10.0.6)

| Comprobación | Resultado |
|---|---|
| ERC | 1 aviso: `pin_to_pin`, el pin VBUS de U1 (bidireccional) está unido a un `PWR_FLAG` |
| DRC | 1 error `starved_thermal`: el pad 20 (GND) de U1 conecta con una isla aislada en B.Cu |
| DRC | 39 avisos `lib_footprint_mismatch` (huellas distintas a las de la librería actual) |
| DRC | 0 elementos sin conectar |
| Paridad esquema↔PCB | 77 incidencias: 61 campos `LCSC Part#` ausentes en huellas, 10 conflictos de red, 6 huellas distintas |

Las mismas 77 incidencias de paridad aparecen al analizar la versión fabricada 1.1.0.

## 3. Hallazgos

Severidad: **C** crítico · **A** alto · **M** medio · **B** bajo.

| ID | Sev. | Hallazgo | Impacto |
|---|---|---|---|
| H1 | C | **Esquema y PCB desincronizados.** `V_Level` va a IO10 (pad 12) en el esquema y a IO18 (pad 24) en la PCB. En los bornes J1–J4, los pines 1 y 2 (NO / común) están intercambiados. Las huellas de los bornes (MaiXu en el esquema, Phoenix en la PCB) y de L1 son distintas. | El esquema no documenta la placa real; cualquier cambio desde el esquema rompe la PCB. |
| H2 | A | `V_Level` está en **GPIO18, un canal ADC2** del ESP32-S2. Espressif documenta que ADC2 comparte recursos con el Wi-Fi. | Lecturas de nivel que fallan o pierden precisión con Wi-Fi activo. |
| H3 | A | **Lazo 4–20 mA sin margen de tensión.** El lazo se alimenta a 12 V y R15 (150 Ω) cae 3 V a 20 mA, así que al transmisor le quedan 9 V (mínimo de fábrica: 12 V). Sin TVS ni limitación de corriente. | La parte alta del rango puede saturar. Un cortocircuito en el cable pone 12 V sobre R15: 80 mA y ≈ 1 W en una 1210. |
| H4 | A | **Alimentación limitada a 12 V por jack DC de 2,1 mm.** El EN del TPS54202 corta a 11,7 V; su VIN máximo es 28 V. Sin protección contra inversión de polaridad, sobretensión ni fusible. | Incumple el requisito del TFG de admitir batería y solar: una batería de plomo de 12 V cae por debajo de 11,7 V con carga o parcialmente descargada. Tampoco sirve para 24 V con margen. |
| H5 | M | **Excitación del optoacoplador desde 3,3 V.** R1 (50 Ω), el LED rojo y el LED IR del PS2705 van en serie, con muy poco margen de tensión; la corriente depende de la tolerancia de Vf. La salida del opto se alimenta del mismo 5 V / GND. | Corriente de LED poco controlada. El opto no aporta aislamiento galvánico real y añade 4 componentes por canal. |
| H6 | M | **DHT11** de precisión limitada (±2 °C, ±5 %HR) y montado dentro de la caja IP65. | Mide el clima del interior de la caja, no el de la parcela. |
| H7 | M | **Wemos enchufable en tiras hembra.** | Contactos sensibles a vibración, humedad y oxidación en exterior. El USB solo es accesible abriendo la caja. |
| H8 | M | **Librerías con rutas absolutas** (`G:/Otros ordenadores/Mi PC/...`) en `sym-lib-table` y `fp-lib-table`; el Wemos y el jack se leen de JSON de EasyEDA. | El proyecto no abre correctamente en otro equipo ni desde un repositorio. |
| H9 | B | **Hojas huérfanas:** `Panel_Control.kicad_sch` (formato KiCad 8: 4 LED, 1 pulsador, conectores 1×4 y 1×9) y `untitled.kicad_sch` (copia del Wemos) no están en la jerarquía. | Confusión. La interfaz física del panel nunca llegó a la placa. |
| H10 | B | Error de DRC por conexión térmica incompleta en U1 y 39 huellas que difieren de la librería. | Riesgo menor de soldadura; huellas no actualizables. |
| H11 | B | **Placa grande** (129 × 96,5 mm), resistencias 1210 en señales de baja potencia y huellas *HandSolder*. | Más coste y área de la necesaria; no está preparada para montaje SMT automático. |
| H12 | M | **Firmware (`control-riego.yaml`, anexo de la memoria).** DHT en GPIO11 (PCB: GPIO12) y ADC en GPIO10 (PCB: GPIO18). El sensor `template` usa `id(voltaje_sensor_nivel)`, que no existe (el id es `voltaje_sensor_nivel_esp32`). Clave API, contraseña OTA y del AP en claro. | El YAML no corresponde a la PCB y no compila tal cual. Las credenciales no deben versionarse. |

## 4. Qué se conserva en la v2

- Arquitectura ESP32 + ESPHome + Home Assistant, validada en el TFG.
- Medida de nivel con transmisor presostático 4–20 mA y filtrado paso bajo (se corrige el dimensionado).
- Relés SPDT con diodo de rueda libre, LED por canal y bornes atornillados de 5 mm.
- Test points en las señales clave.
- Montaje en caja IP65 sobre carril DIN con anclajes impresos en 3D.
- Pistas anchas en los contactos de los relés.
