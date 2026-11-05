---
spec: SPEC-0014
agente: ing-esquematicos
n: 01
fecha: 2026-11-05
estado: completado
---

# SPEC-0014 · 01 · ing-esquematicos

## Orden recibida

> SPEC-0014 · rama spec/SPEC-0014-limpieza-v2 (activa; no cambies de rama ni uses git para escribir) · Lee: gestion/specs/SPEC-0014-limpieza-v2.md (la orden completa; tú haces la parte del ESQUEMA), CLAUDE.md, docs/02-especificaciones-v2.md v0.4, DEC-0002/0003/0004 en gestion/decisiones/, docs/01-analisis-v1.md §1, hardware/v2/README.md, gestion/informes/VAL-0013-02.md, gestion/checklists/esquema.md v5 · Haz: limpia el esquema de hardware/v2 según la spec: retira los circuitos de la v1 que no encajan en v0.4 (Wemos, relés, optos, BC817, diodos de bobina, TPS54202, jack, 4–20 mA, DHT11, bornes que no cumplan FAB-07…) con sus cables, etiquetas y pines jerárquicos; conserva solo lo que cumpla v0.4 tal cual, justificándolo; deja en cada hoja un texto con el bloque pendiente y sus requisitos; comment 1 del cajetín por hoja según la spec (raíz: «Placa de control de riego»). NO toques la PCB (la limpia ing-layout después) ni hardware/v1-tfg ni hardware/libraries. En paralelo trabaja jr-conformidad en otra spec (hardware/componentes y hardware/libraries/esp-riego.*): no toques esos archivos y no te extrañe verlos aparecer. Eres el único que usa el MCP con un proyecto cargado: guarda y haz close_project al terminar; no dejes .lck. Verifica con verificar.py hardware/v2 (el ERC del esquema limpio: 0 errores; la paridad y el DRC fallarán hasta que ing-layout sincronice la PCB, anótalo) y revisa el cajetín en un PDF exportado sobre una copia. Actualiza tu memoria de agente: la nota de D8 con válvulas de 24 V AC y ≈ 4 A está superada (DEC-0003: 24 V DC, BTT6050; DEC-0004: carga instalada 3,5 A, banda del limitador 3,5–4,9 A). · Entrega: hardware/v2/*.kicad_sch (y README.md) + log gestion/logs/SPEC-0014/01-ing-esquematicos.md con el inventario de lo retirado. Responde con ESTADO, ARCHIVOS, VERIFICACIÓN, PENDIENTE (lo que ing-layout debe saber) y LOG.

## Contexto consultado

- `gestion/specs/SPEC-0014-limpieza-v2.md` (alcance, criterios de aceptación).
- `docs/02-especificaciones-v2.md` v0.4: ALI-01…ALI-13, MCU-01…MCU-07, REL-01…REL-10, AMB-01…AMB-03, EXP-01…EXP-04, FAB-05, FAB-07, FAB-08, KIC-02.
- `gestion/decisiones/` DEC-0002 (sin sensor de nivel, sensor T/HR en placa), DEC-0003 (salidas *high-side* BTT6050 y limitador común), DEC-0004 (fuente LED de 5 A, carga instalada 3,5 A, banda 3,5–4,9 A).
- `docs/01-analisis-v1.md` §1 y §3 (bloques de la v1; H4, H5, H6, H7, H11).
- `hardware/v2/README.md`, `gestion/informes/VAL-0013-02.md` (observación 03, `comment 1`), `gestion/checklists/esquema.md` v5 (estructura y cajetín).
- `hardware/libraries/ESP-Riego.kicad_wks` (solo lectura, copiada al *scratchpad* para el PDF): `${COMMENT1}` está en la casilla grande de arriba, a 3,5 mm en negrita, en un hueco de ≈ 145 mm.
- `hardware/v2/esp-riego.kicad_pcb` (solo lectura, con Grep): red de los pads de TP1–TP4 para el inventario.

## Acciones

1. Comprobaciones iniciales: rama `spec/SPEC-0014-limpieza-v2`; KiCad no está abierto (`check_kicad_ui`) y no hay `.lck` en `hardware/v2`. Huella MD5 de `hardware/v2/*` y `hardware/v1-tfg/*` antes de empezar.
2. Inventario de las 5 hojas con un analizador de *s-expressions* (script de solo biblioteca estándar en el *scratchpad*).
3. Limpieza con un script propio (en el *scratchpad*), probado antes sobre una copia: quita de cada hoja los símbolos que no se conservan, los cables, uniones, *no-connect*, etiquetas locales y globales, *netclass flags*, textos y cuadros de texto de la v1, y las definiciones de `lib_symbols` que quedan sin uso. Conserva el texto original de todo lo que se queda (cabecera, cajetín, hojas, `sheet_instances`, H1–H4) y los finales de línea CRLF. El MCP no tiene herramientas para borrar uniones, *no-connect*, *netclass flags* ni cuadros de texto, por eso se hizo con script.
4. Texto del bloque pendiente en cada hoja con `mcp__kicad__add_schematic_text` (encabezado de 2,54 mm en negrita y cuerpo de 1,524 mm), y un texto en la raíz con el mapa de hojas y requisitos y la hoja `Sensores` por llegar.
5. `comment 1` del cajetín en cada hoja. Las primeras propuestas (≈ 60–70 caracteres) se salían de la casilla en el PDF: se acortaron hasta que todas caben (ver Verificación).
6. Coherencia: `instances (project "")` de H1, heredado de la v1, pasa a `"esp-riego"` como H2–H4.
7. `hardware/v2/README.md` actualizado (estado de esqueleto, tabla de hojas con bloque, requisitos y contenido).
8. MCP: no se cargó ningún proyecto (las herramientas de texto trabajan sobre el archivo). `get_backend_state` confirma que no hay proyecto ni placa cargados; `close_project` (sin guardar) responde «No project was loaded». No hay `.lck` ni `-backups/`.

## Inventario de lo retirado

### Alimentacion (`alimentacion.kicad_sch`)

| Ref. | Valor | Huella v1 | Función en la v1 | Motivo |
|---|---|---|---|---|
| J5 | DC Jack | BarrelJack_Kycon_KLDX-0202-xC_Horizontal | Entrada de 12 V | ALI-02: entrada por borne de 2 polos de 5,08 mm (H4) |
| U2 | TPS54202DDC | SOT-23-6 | Buck 12 V → 5 V | ALI-05: VIN máx. 28 V < 60 V; ALI-01: 18–30 V (H4) |
| L1 | 22uH | SMMS0530-150M | Bobina del buck | Red del TPS54202 (ALI-05) |
| C1 | 10uF | C_0805 HandSolder | Entrada del buck | Red del TPS54202; tensión no válida para ALI-05 |
| C2 | 100nF | C_0805 HandSolder | Entrada del buck | Ídem |
| C3 | 100nF | C_0805 HandSolder | *Bootstrap* | Ídem |
| C4, C5 | 22uF | C_0805 HandSolder | Salida de 5 V | Ídem |
| C6 | 68pF | C_0805 HandSolder | *Feed-forward* | Ídem |
| R9 | 270k | R_1210 HandSolder | Divisor de EN (UVLO 11,7 V) | ALI-06: UVLO ≈ 15 V tras las protecciones (H4) |
| R10 | 33k | R_1210 HandSolder | Divisor de EN | Ídem |
| R11 | 100k | R_1210 HandSolder | Divisor de FB | Red del TPS54202 (ALI-05) |
| R12 | 13k | R_1210 HandSolder | Divisor de FB | Ídem |
| R13 | 180 | R_1210 HandSolder | Resistencia del LED de alimentación | ALI-10 pide LED, pero este va en el 5 V del buck retirado, sin MPN ni LCSC (FAB-05) y con huella *HandSolder* (H11). Se rehace con el bloque (en caso de duda, se retira) |
| D9 | Green | LED_0805 HandSolder | LED de alimentación | Ídem |
| #PWR016–#PWR026 (11) | GND, +12V, +5V | — | Símbolos de alimentación | Sin piezas a las que conectar; +12V no existe en la v2 |
| #FLG01–#FLG03 (3) | PWR_FLAG | — | Banderas de alimentación | Sin red que marcar: un PWR_FLAG suelto da error de ERC |
| — | 49 cables, 15 uniones, 1 texto («ON: 11.7 V / OFF: 11 V»), 1 cuadro de texto | | | Restos del circuito retirado |

### MCU (`mcu.kicad_sch`)

| Ref. | Valor | Huella v1 | Función en la v1 | Motivo |
|---|---|---|---|---|
| U1 | WEMOS-S2-MINI (ESP32-S2FN4R2) | Wemos s2 mini:WEMOS-S2-MINI | MCU enchufable | MCU-01: ESP32-S3-WROOM-1 soldado (H7) |
| #PWR013–#PWR015 (3) | +3.3V, +5V, GND | — | Símbolos de alimentación | Sin piezas |
| #FLG04 | PWR_FLAG | — | Bandera en VBUS (origen del aviso `pin_to_pin` de la v1) | Sin piezas |
| — | 15 cables, 2 uniones, 22 *no-connect*, 6 etiquetas globales (REL1–REL4, TH_Data, V_Level), 1 cuadro de texto | | | Señales de la v1 que ya no existen |

### Salidas (`salidas.kicad_sch`)

| Ref. | Valor | Huella v1 | Función en la v1 | Motivo |
|---|---|---|---|---|
| K1–K4 | SANYOU_SRD_Form_C | Relay_SPDT_SANYOU_SRD | Relés de salida | REL-01/REL-03: *high-side* BTT6050, sin relé (DEC-0003) |
| Q1, Q2, Q5, Q6 | PS2705-1-F3-A | SOP254P700X230-4N | Optoacopladores | REL-03: sin optoacoplador (H5) |
| Q3, Q4, Q7, Q8 | BC817-25-7-F | SOT96P240X110-3N | Transistores de bobina | REL-03 (DEC-0003) |
| D3, D4, D7, D8 | 1N4007 | D_DO-41 THT | Diodos de bobina | REL-03: desmagnetización con el *clamp* del *high-side* |
| D1, D2, D5, D6 | Red | LED_0805 HandSolder | LED en serie con el del opto | H5; REL-07 pide LED por canal, pero con otro circuito y sin enmascarar la carga abierta (REL-10) |
| R1, R2, R5, R6 | 50 | R_1210 HandSolder | Corriente del LED del opto | REL-03 (H5) |
| R3, R4, R7, R8 | 1k | R_1210 HandSolder | Base de los BC817 | REL-03 |
| J1–J4 | Conector Rele 1…4 (Conn_01x03) | TerminalBlock_MaiXu_MX126-5.0-03P (5,00 mm) | Bornes NO/COM/NC | FAB-07: 2 polos por canal (OUT_n, GND) a 5,08 mm; REL-01: 6 canales; H1 (orden de pines) |
| #PWR01–#PWR012 (12) | +3.3V, +5V, GND | — | Símbolos de alimentación | Sin piezas |
| — | 108 cables, 12 uniones, 24 etiquetas locales (IN/NO/NC_REL1–4), 4 globales (REL1–REL4), 20 *netclass flags*, 2 cuadros de texto | | | Restos del circuito retirado |

### Conectores (`conectores.kicad_sch`)

| Ref. | Valor | Huella v1 | Función en la v1 | Motivo |
|---|---|---|---|---|
| J6 | Conn_01x02 | TerminalBlock_MaiXu_MX126-5.0-02P (5,00 mm) | Borne del lazo 4–20 mA | DEC-0002: sin sensor de nivel (NIV-01…08 retirados); paso 5,00 ≠ 5,08 mm (FAB-07) |
| R15 | 150 | R_1210 HandSolder | Resistencia de carga del lazo | DEC-0002 (H3) |
| R14 | 270k | R_1210 HandSolder | Filtro RC del lazo | DEC-0002 |
| C7 | 100nF | C_0805 HandSolder | Filtro RC del lazo | DEC-0002 |
| J7 | Conn_01x03 | PinHeader_1x03_P2.54mm | Conector del DHT11 | AMB-01: sensor I²C en placa (H6) |
| TP1 | TestPoint | TestPoint_Pad_1.0x1.0mm | Punto de prueba en V_Level | DEC-0002: la red no existe |
| TP2 | TestPoint | TestPoint_Pad_1.0x1.0mm | Punto de prueba en +12V | ALI-01: no hay 12 V |
| TP3 | TestPoint | TestPoint_Pad_1.0x1.0mm | Punto de prueba en +5V | ALI-11 pide test points en VIN, 5 V, 3,3 V y GND: los rehace el bloque de alimentación con sus redes y sus piezas (sin LCSC, FAB-05). En caso de duda, se retira |
| TP4 | TestPoint | TestPoint_Pad_1.0x1.0mm | Punto de prueba en +3.3V | Ídem |
| #PWR027–#PWR034 (8) | GND, +12V, +5V, +3.3V | — | Símbolos de alimentación | Sin piezas |
| — | 19 cables, 2 uniones, 3 etiquetas globales (V_Level ×2, TH_Data), 2 textos («4mA:0.6V / 20mA:3V», «fc=5.9Hz»), 3 cuadros de texto | | | Restos del circuito retirado |

**Total:** 57 componentes con huella (15 + 1 + 32 + 9), 34 símbolos de alimentación y 4 PWR_FLAG, 191 cables, 31 uniones, 22 *no-connect*, 24 etiquetas locales, 13 globales, 20 *netclass flags*, 3 textos y 7 cuadros de texto. No había etiquetas ni pines jerárquicos (la v1 unía las hojas con etiquetas globales): la raíz queda con las 4 hojas y sin pines. Las definiciones de `lib_symbols` sin uso también se han quitado (34 en total).

### Conservado

| Ref. | Valor | Huella | Requisito | Justificación |
|---|---|---|---|---|
| H1–H4 | MountingHole (`Mechanical:MountingHole`) | `MountingHole:MountingHole_3.2mm_M3_Pad_Via` (librería oficial de KiCad 10) | FAB-08 | La placa lleva 4 taladros M3. El símbolo no tiene pines, está fuera de la BOM (`in_bom no`) y la huella existe en las librerías oficiales (KIC-01). Que el anillo quede sin red o vaya a GND, o que se cambie a NPTH, es una decisión del layout |

## Decisiones y justificación

- **Todo lo demás se retira**, incluso lo que tiene un requisito parecido en la v2 (LED de alimentación ALI-10, test points ALI-11, LED por canal REL-07): en la v1 cuelgan de redes que desaparecen (+12V, 5 V del TPS54202, cadena del opto), no tienen MPN ni LCSC (FAB-05) y usan huellas *HandSolder* 1210/0805 (H11). La spec dice «en caso de duda, se retira».
- **PWR_FLAG:** ninguno se conserva. Sin redes, un PWR_FLAG suelto daría `pin_not_connected`; cada bloque pondrá los suyos.
- **`comment 1`** (VAL-0013-02-03). La casilla admite ≈ 145 mm a 3,5 mm en negrita, unos 50 caracteres. El texto de ejemplo de la spec («Bloque de alimentación: entrada, protecciones, limitador y buck», 63 caracteres) se salía de la casilla y pisaba la de la fecha, así que se acortó:
  - raíz: «Placa de control de riego»;
  - Alimentacion: «Alimentación: protecciones, limitador, buck y 3,3 V»;
  - MCU: «Microcontrolador: ESP32-S3, USB-C y UART»;
  - Salidas: «Salidas: 6 high-side con diagnóstico y bornes»;
  - Conectores: «Conectores: pulsos, expansión y taladros M3».
- **Reparto de bloques entre hojas** (propuesta, en los textos y en el README): bornes de salida en `Salidas` (REL-06, REL-09); borne de entrada en `Alimentacion` (ALI-02); entrada de pulsos, expansión y taladros en `Conectores` (EXP-01…04, FAB-07, FAB-08); hoja `Sensores` nueva para AMB-01…03 (KIC-02). Lo fijará cada spec de bloque.
- No se ha tocado `esp-riego.kicad_pro`: sus `netclass_patterns` y `netclass_assignments` aún tienen restos de la v1 (REL1–4, ECHO, TRIG, /ESP32_EN, 3V3, 5V, GND), pero las clases de red son del layout (FAB-03; la spec las excluye).

## Verificación

`python herramientas/verificar.py hardware/v2` (después de todos los cambios):

```
ERC         0  (errores 0, avisos 0)
DRC        40  (errores 1, avisos 39, sin conectar 0)
    39  lib_footprint_mismatch [warning]
     1  starved_thermal [error]
Paridad    61
    57  extra_footprint
     4  footprint_symbol_field_mismatch
Resultado: CON INCIDENCIAS
```

- **ERC 0:** cumple el criterio de la spec para el esquema. No queda ningún aviso.
- **DRC 40 y paridad 61:** son esperables. La PCB sigue siendo la de la v1 hasta que `ing-layout` la sincronice:
  - los 57 `extra_footprint` son exactamente los 57 componentes retirados;
  - los 4 `footprint_symbol_field_mismatch` son H1–H4: el símbolo tiene el campo `LCSC Part#` (vacío) y la huella de la PCB no. Se resuelven al actualizar la PCB desde el esquema;
  - el DRC (39 `lib_footprint_mismatch` y 1 `starved_thermal` en U1) desaparece cuando se borran las huellas de la v1.
- **PDF del cajetín:** `kicad-cli sch export pdf` sobre una copia en el *scratchpad* (`copia_pdf/`, con `libraries/` al lado para que resuelva `${KIPRJMOD}/../libraries/ESP-Riego.kicad_wks`). Revisé las 5 páginas como imagen:
  - «ESP-Riego v2» sale una sola vez por página, en `${TITLE}`;
  - `${COMMENT1}` muestra la descripción de cada hoja dentro de la casilla, sin pisar la fecha;
  - se ven «Hoja: esp-riego / Salidas / MCU / Alimentacion / Conectores», «Rev: 2.0-dev», la fecha y el autor;
  - los textos de bloque pendiente se leen bien y no se solapan con nada.

  Nota: con una copia sin `../libraries/`, KiCad usa sin avisar la hoja por defecto. Para comprobar el cajetín hay que copiar también la hoja de dibujo.
- **MD5:** después de verificar, `esp-riego.kicad_pcb`, `esp-riego.kicad_pro`, `sym-lib-table`, `fp-lib-table` y `hardware/v1-tfg/*` no cambian. Solo cambian los 5 `.kicad_sch` y el `README.md`. Los esquemas mantienen CRLF.
- No hay `.lck`, `-backups/` ni `.kicad_prl` en `hardware/v2`. El MCP no tiene proyecto cargado.

## Pendiente

- **ing-layout (SPEC-0014, parte de PCB):**
  - actualizar la PCB desde el esquema: borrar las 57 huellas de la v1, con sus pistas, vías, zonas y textos, y conservar H1–H4, que recibirán el campo `LCSC Part#` y quitarán las 4 incidencias de paridad;
  - recolocar H1–H4 en las esquinas del contorno de 100 × 70 mm. La huella es `MountingHole_3.2mm_M3_Pad_Via`, con anillo de cobre sin red: si se prefiere NPTH o conectarla a GND, que se proponga, porque el cambio se hace en el esquema;
  - después de sincronizar, el objetivo es DRC 0 y paridad 0.
- **Coordinador:** los `netclass_patterns` y `netclass_assignments` de la v1 en `esp-riego.kicad_pro` quedan para quien defina las clases de red (FAB-03).
- **Coordinador:** el ejemplo de `comment 1` de la spec no cabe en la casilla de la hoja de dibujo. Si se quieren descripciones más largas, hay que reducir la letra de `${COMMENT1}` (3,5 mm) en `ESP-Riego.kicad_wks`, que es zona de librerías.

## Notas para el siguiente agente

- Las hojas no tienen pines jerárquicos ni etiquetas. Cada bloque crea los suyos. Mejor usar etiquetas jerárquicas en lugar de las globales de la v1.
- El texto de cada hoja (encabezado a la altura de y = 33 mm y cuerpo debajo) se puede borrar cuando llegue el bloque. Los textos de varias líneas del MCP se justifican abajo: el punto `at` es la base de la última línea y el bloque crece hacia arriba.
- `comment 1` cabe hasta unos 50 caracteres.
