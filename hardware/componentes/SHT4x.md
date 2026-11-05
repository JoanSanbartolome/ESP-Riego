---
mpn: SHT40-AD1B / SHT41-AD1B / SHT45-AD1B (familia SHT4x)
fabricante: Sensirion
funcion: sensor I²C de temperatura y humedad del aire de la caseta (AMB-01)
lcsc: C2848306 (SHT40-AD1B-R3)
tipo_jlcpcb: extended
stock_consultado: 2026-11-05
datasheet: https://sensirion.com/media/documents/33FD6951/6A7C10A0/HT_DS_Datasheet_SHT4x_V7.3.pdf
datasheet_local: datasheets/SHT4x.pdf (versión 7.3, junio de 2026, 1,0 MB; sustituye a la 6.2, que ya no era la vigente: página de producto de sensirion.com, 2026-11-05)
simbolo: Sensor_Humidity:SHT4x
huella: Sensor_Humidity:Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad
modelo_3d: ${KICAD10_3DMODEL_DIR}/Sensor_Humidity.3dshapes/Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad.step (ausente en la instalación 10.0.6 y en kicad-packages3D); respaldo creado, que el bloque enlaza en la instancia: ${KIPRJMOD}/../libraries/3d/Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad.step
origen_assets: kicad-oficial (símbolo y huella); modelo 3D de respaldo creado con SolidCraft
verificado_por: pendiente (ing-validacion), solo el modelo 3D de respaldo
---

# SHT4x · temperatura y humedad

## Datos clave

| Parámetro | Valor | Fuente (página) |
|---|---|---|
| Alimentación VDD | 1,08 / 3,3 / 3,6 V | Tabla de la p. 9 |
| Corriente en medida | 320 µA típ. / 500 µA máx. | p. 9 |
| Exactitud | SHT40 ± 1,8 %RH y ± 0,2 °C típ.; SHT41 ± 1,8 %RH y ± 0,2 °C máx. (ver curvas); SHT45 ± 1,0 %RH y ± 0,1 °C | p. 1 y p. 4-6 |
| Dirección I²C | 0x44 (variantes AD1B), 0x45 (BD1B), 0x46 (CD1B) | p. 1 y p. 21 |
| Calentador interno | 20, 110 o 200 mW, pulso de 0,1 s o 1 s | p. 2 y p. 13 |
| Encapsulado | DFN-4, 1,5 × 1,5 mm | §5, p. 15 |
| Resistencia térmica (θ_JA) | 297 K/W con el pad central sin soldar | p. 17 |

## Pinout

| Pin | Nombre | Función |
|---|---|---|
| 1 | SDA | Datos I²C |
| 2 | SCL | Reloj I²C (entrada) |
| 3 | VDD | Alimentación |
| 4 | VSS | Masa |

(§5.4, p. 17.) El pad central no está unido a ningún pin.

## Recomendaciones de layout del fabricante (§5.3, p. 16)

- No soldar el pad central: Sensirion lo desaconseja porque el sensor puede calentarse con el calentador activo. Es el motivo de la huella «NoCentralPad».
- Sin cobre bajo el sensor salvo en los pads de pin.
- El *land pattern* dado es la referencia de Sensirion: debe ajustarse al proceso de fabricación (la huella oficial de KiCad la recoge).
- Para medir el aire de la caseta y no la placa (AMB-01): separar térmicamente el sensor del resto de la placa con ranuras (esto lo concreta el bloque de sensores).

## Alternativas

| MPN | LCSC | Diferencias |
|---|---|---|
| SHT41-AD1B-R2 | C7461861 | Mejor exactitud; 2,4792 $ a 30 uds; stock 12 072 |
| SHT45-AD1B-R2 | C5221601 | Mejor exactitud; 4,4678 $ a 30 uds; stock 7 078 |
| SHT40-AD1B-R2 | C2909890 | Mismo chip, carrete R2; stock 15 973 |

## Aprovisionamiento (JLCPCB/LCSC, consulta 2026-11-05)

| Código | Variante | Tipo | Stock | Precio unitario por tramo (USD) | 5 placas | 10 placas |
|---|---|---|---|---|---|---|
| C2848306 | SHT40-AD1B-R3 | Extended | 15 537 | 1–9: 1,8529 · 10–29: 1,5732 | 9,26 $ | 15,73 $ |
| C7461861 | SHT41-AD1B-R2 | Extended | 12 072 | 1–9: 3,2576 · 10–29: 2,7785 | 16,29 $ | 27,79 $ |
| C5221601 | SHT45-AD1B-R2 | Extended | 7 078 | 1–9: 5,7139 · 10–29: 4,9388 | 28,57 $ | 49,39 $ |

## Notas de los assets

El símbolo y la huella son oficiales y no se copian. El modelo 3D que referencia la huella oficial no existe en la instalación local de KiCad 10.0.6 ni en el repositorio oficial `kicad-packages3D` (`master` y `10.0`, comprobado el 2026-11-05: `Sensor_Humidity.3dshapes` solo contiene el HDC2080); se ha creado uno de respaldo con SolidCraft (fuentes en `hardware/libraries/3d/fuentes-solidcraft/`), con el mismo nombre que el oficial en `hardware/libraries/3d/`. El bloque de sensores tiene que añadir en la instancia el `model` con `${KIPRJMOD}/../libraries/3d/Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad.step`. Origen = origen de la huella, offset 0, rotación 0, escala 1. Cotas de la Figura 15 (p. 15 de la V7.3): cuerpo 1,5 × 1,5, altura 0,54, paso 0,8, pads de 0,3 con pads a ras del cuerpo, apertura del sensor de Ø 0,6. Supuestos: grosor de pad de 0,2 (lectura de la cota del alzado); pads de 0,3 (lado del pin 1) y 0,4 (lado opuesto) de longitud, por lectura literal; profundidad de la apertura de 0,15; marca del pin 1 como hendidura de Ø 0,2 × 0,05 en la esquina del pad 1 (diámetro supuesto); sin pad central ni rotulado. Comprobado con `kicad-cli pcb render`: pads sobre los de la huella oficial y marca en el pin 1. Ver el log de SPEC-0015.

## Uso en el proyecto

AMB-01. La variante (SHT40/41/45) la fija el bloque de sensores.
