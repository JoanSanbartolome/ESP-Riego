# v2 — ESP-Riego (esqueleto de trabajo)

Proyecto KiCad 10 `esp-riego`. Nació como copia de la v1 (`hardware/v1-tfg/`, etiqueta `v1.1-tfg`, SPEC-0013) y en SPEC-0014 se vació: se retiraron todos los circuitos de la v1 que no encajan en los requisitos v0.4 (`docs/02-especificaciones-v2.md`, DEC-0002, DEC-0003 y DEC-0004). El inventario de lo retirado está en `gestion/logs/SPEC-0014/01-ing-esquematicos.md`.

Cajetín: hoja de dibujo `../libraries/ESP-Riego.kicad_wks`, título «ESP-Riego v2», revisión 2.0-dev. `comment 1` lleva la descripción de cada hoja («Placa de control de riego» en la raíz).

## Hojas

| Hoja (`Sheetname` · archivo) | Bloque pendiente | Requisitos | Contenido actual |
|---|---|---|---|
| `Alimentacion` · `alimentacion.kicad_sch` (A3) | Entrada, protecciones, limitador común, buck, 3,3 V | ALI-01 … ALI-13 | **Bloque de la v2** (SPEC-0019): J1, F1, Q1, D1–D4, U1–U4, L1, JP1, TP1–TP5 y pasivos, según `docs/diseno/alimentacion.md`. Pines de hoja: `BUS_24V`, `VIN_SENSE`, `LIM_IMON`, `LIM_FLT`, `LIM_EN` y `VBUS` |
| `MCU` · `mcu.kicad_sch` (A3) | ESP32-S3-WROOM-1, USB-C, BOOT/RESET, UART | MCU-01 … MCU-07, FW-02 | **Bloque de la v2** (SPEC-0022): U5, U6, J2, J3, SW1, SW2, D5 y pasivos, según `docs/diseno/mcu.md`. 25 pines de hoja (Anexo C de `mcu.md`) |
| `Salidas` · `salidas.kicad_sch` | 6 *high-side* BTT6050 con diagnóstico y sus bornes | REL-01 … REL-10 | Texto del bloque pendiente |
| `Conectores` · `conectores.kicad_sch` | Entrada de pulsos, expansión, reparto de bornes | EXP-01 … EXP-04, FAB-07, FAB-08 | Texto del bloque pendiente y H1–H4 (taladros M3, FAB-08) |

La hoja `Sensores` (AMB-01 … AMB-03) se añade con el bloque de temperatura y humedad (KIC-02). Cada bloque crea sus pines jerárquicos. En la raíz, `VBUS`, `VIN_SENSE`, `LIM_IMON`, `LIM_FLT` y `LIM_EN` unen MCU y Alimentacion con etiquetas locales (SPEC-0022). Los pines sin hoja de destino llevan una marca de no conexión **provisional** (`BUS_24V`; IN, OUT_DEN, IS, I²C y expansión de MCU): la spec que dibuje Salidas, Sensores o Conectores la quita. +5V, +3V3 y GND son símbolos de alimentación globales.

## Puente JP1 del limitador (DEC-0006)

JP1 es un puente de soldadura de `VIN_PROT` a `BUS_24V`, en paralelo con U1 (TPS26632). **Va abierto**, con U1 montado. Solo se cierra, con una gota de estaño, si U1 no se monta o falla abierto. Con U1 sano no se cierra: la corriente se lo saltaría. Serigrafía: «JP1: abierto = limitador · cerrado = sin limitador».

Con JP1 cerrado (y sin U1) se pierde (`docs/diseno/alimentacion.md` §3.13.9):

- la limitación común a 3,86–4,57 A (ALI-13): un corto en una salida lo limitan la fuente (≥ 5,14 A) y el BTT6050 (≥ 38 A); `VIN_PROT` cae y la lógica puede reiniciarse, así que **REL-08 no se cumple**;
- el corte general del bus por `LIM_EN`: el bus queda siempre alimentado;
- `LIM_FLT` e `LIM_IMON`: FLT lee alto siempre e IMON 0 V; en el firmware hay que activar la opción «sin limitador»;
- el *clamp* del bus a ≤ 35 V: el bus ve `VIN_PROT` hasta 53,3 V, dentro de los 65 V del BTT6050;
- el arranque suave del bus (dVdT).

Se mantiene REL-04: cada IN de las salidas tiene su *pull-down*, así que las salidas siguen apagadas en el reset y el flasheo. Los pads tienen conexión sólida a la zona: para cerrarlo hace falta un soldador potente o punta ancha.

## PCB

Sincronizada con el esquema, sin colocar ni rutar (SPEC-0019 y SPEC-0022; detalle en `gestion/logs/SPEC-0022/02-ing-layout.md`). Tiene 80 huellas: H1–H4 dentro del contorno, y fuera de él, agrupadas por posición, las 55 de Alimentacion (x 10–92, y 60–113 mm) y las 21 de la hoja MCU (x 10–64, y 120–198 mm). Sin pistas, vías ni zonas.

- Contorno **preliminar** de 100 × 70 mm en `Edge.Cuts` (FAB-08), de (100, 60) a (200, 130) mm; el origen auxiliar y el de la rejilla están en la esquina inferior izquierda. Un texto en `User.Comments` lo marca como preliminar hasta el *floorplan*.
- H1–H4 (`MountingHole_3.2mm_M3_Pad_Via`, anillo sin red), a 4 mm de los dos bordes de su esquina: H3 arriba a la izquierda, H1 arriba a la derecha, H4 abajo a la izquierda y H2 abajo a la derecha.
- Reglas de FAB-02 en el `.kicad_pro`: pista y separación ≥ 0,2 mm, vía 0,6/0,3 mm, cobre a borde ≥ 0,5 mm. Solo existe la clase `Default` (0,2 mm, vía 0,6/0,3). Las clases de FAB-03 y el `.kicad_dru` (KIC-04) llegan con el layout.
- `pcbplotparams/outputdirectory` vacío y sin `embedded_files`.

## Cómo se trabaja

Cada bloque llega con su propia spec. La PCB se actualiza desde el esquema en cada bloque; el layout definitivo se hace cuando el esquema esté estable.

Las librerías están en `../libraries/` (tablas con `${KIPRJMOD}/../libraries/...`). Desde SPEC-0019 las tablas del proyecto solo tienen `esp-riego` (símbolos y huellas propios de la v2); el resto son las oficiales de KiCad 10. Las librerías de la v1 siguen en `../libraries/` para `v1-tfg`, que tiene sus propias tablas (VAL-0014-01-02).

Verificación: `python herramientas/verificar.py hardware/v2`. Estado tras el paso 2 de SPEC-0022: ERC 0 (0 avisos), DRC 0 (0 avisos; 172 sin conectar porque la PCB no está rutada) y paridad 0. Las 21 huellas de la hoja MCU están fuera del contorno hasta la spec de colocación.
