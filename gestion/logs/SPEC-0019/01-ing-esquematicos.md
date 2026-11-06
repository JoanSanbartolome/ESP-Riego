---
spec: SPEC-0019
agente: ing-esquematicos
n: 01
fecha: 2026-11-06
estado: completado
---

# SPEC-0019 · 01 · ing-esquematicos

## Orden recibida

SPEC-0019 · rama spec/SPEC-0019-hoja-alimentacion (activa en C:\Users\josan\proyectos\KICAD_mcp) · Lee: gestion/specs/SPEC-0019-hoja-alimentacion.md + sus entradas + gestion/decisiones/DEC-0006 y DEC-0007 · Haz: todo el alcance. Piezas: D2 = esp-riego:SMBJ33A, U2 = huella esp-riego:Texas_DDA0008B_…, F1 = esp-riego:Fuse_Littelfuse-NANO2-451_453, JP1 = esp-riego:SolderJumper-2_P1.8mm_Open_Pad1.2x3.0mm; C22 (2.º CIN de U2), C3 y C10 en 0805 con sus LCSC; no uses las referencias reservadas al MCU. Eres el único usuario de KiCad; save_project y close_project al terminar. · Entrega: hardware/v2 (hoja y tablas), docs/diseno/alimentacion.md §7/§8, hardware/v2/README.md + log gestion/logs/SPEC-0019/01-ing-esquematicos.md con la salida de verificar.py. Brevedad: solo contrato de salida; log telegráfico.

## Contexto consultado

- SPEC-0019, DEC-0006, DEC-0007; `docs/diseno/alimentacion.md` (completo); `docs/diseno/mcu.md` §9.2, §11 y Anexo C.
- Logs SPEC-0018 01, 04, 05, 07; `gestion/informes/VAL-0014-01.md` (01, 02), `VAL-0018-02.md` (04), `VAL-0018-01.md` (06).
- `hardware/componentes/bloque-alimentacion.md`; checklist `esquema.md` v5.
- API JLCPCB `selectSmtComponentList` (2026-11-06): C14663 Basic 34 750 639; C1591 Extended 3 136 376; C136967 Extended 14 042.
- Librería KiCad 10 `Jumper.kicad_sym` (pines de `SolderJumper_2_Open` a ± 5,08 mm).

## Acciones

- `hardware/v2/alimentacion.kicad_sch`: hoja vaciada y redibujada en A3 (fecha 2026-11-06). 55 piezas (J1, F1, Q1, R1–R15, C1–C22, D1–D4, U1–U4, L1, JP1, TP1–TP5), 59 símbolos de alimentación (#PWR001–055, #FLG01–04), conexiones por etiquetas locales (un cable: R13–D4), 6 etiquetas jerárquicas, 6 marcas de no conexión y textos por bloque (cálculos clave y nota de JP1).
  - Piezas colocadas con el MCP (`batch_add_and_connect`, `batch_add_components`); etiquetas, campos y retoques con scripts propios del *scratchpad* (`s19_*.py`), porque las llamadas del MCP pasaban de 30 s y se cortaban a medias.
  - `lib_symbols` sustituidos por los de KiCad 10 (el MCP embebe copias antiguas: 53 `lib_symbol_mismatch`) y archivo normalizado con `kicad-cli sch upgrade --force` sobre una copia, comprobado y copiado.
  - Campos `MPN`, `LCSC Part#`, `Datasheet` y `Description` en las 55 piezas (de `bloque-alimentacion.md` y fichas). JP1 y TP1–TP5: sin LCSC, `in_bom no` e `in_pos_files no`.
- `hardware/v2/esp-riego.kicad_sch`: 6 pines en la hoja `Alimentacion` (`BUS_24V`, `VIN_SENSE`, `LIM_IMON`, `LIM_FLT` salida; `LIM_EN`, `VBUS` entrada) con marca de no conexión provisional.
- `hardware/v2/sym-lib-table`, `fp-lib-table`: solo `esp-riego` (VAL-0014-01-02).
- `hardware/v2/conectores.kicad_sch`: texto corregido (VAL-0014-01-01 a). La (b) desaparece con el texto antiguo de alimentación.
- `docs/diseno/alimentacion.md`: cabecera, §0, §7 (símbolos y huellas reales, R8 y 100 nF de DEC-0007, viñetas de cambios, fichas, librerías propias e interfaz de la hoja), §8 (JP1: conexión sólida y soldador; VAL-0018-02-04) y §10.5.
- `hardware/v2/README.md`: fila de la hoja, pines provisionales, sección JP1 (lo que se pierde cerrado), tablas y estado de verificación.

## Decisiones y justificación

- **+5V, +3V3 y GND con símbolos de alimentación**, no con etiquetas jerárquicas: son globales y así los usa `mcu.md` Anexo C. Las 6 señales restantes sí van como jerárquicas.
- **Pines de hoja con no conexión en la raíz:** sin hojas destino, cada pin daba un `pin_not_connected` (error); con una etiqueta local daba `label_dangling` (error). La marca deja el ERC a 0. SPEC-0022 y la de salidas la quitan al conectar.
- **PWR_FLAG** en GND, VIN_PROT, +5V_BUCK y VBUS (sin fuente `power_out` en la hoja). El de VBUS sobra cuando la hoja MCU tenga el suyo.
- **C14663 aplicado** (DEC-0007 lo condicionaba al stock de JLCPCB: Basic, 34,75 M el 2026-11-06). Mismo X7R 50 V 0603: no empeora ninguna especificación.
- MODE de U1 sin conectar = *latch-off* (§3.13.3), con marca de no conexión.
- Referencias del bloque MCU (C23–C26, R16–R25, D5, J2–J3, U5–U6, SW1–SW2) sin usar.

## Verificación

- `python herramientas/verificar.py hardware/v2`: ERC 0 (0 errores, 0 avisos) · DRC 0 (0 sin conectar) · paridad 55 (`missing_footprint` × 55) → «CON INCIDENCIAS». Las 55 son las piezas nuevas de la hoja, aún sin pasar a la PCB, que no es de mi zona. Sin otras diferencias.
- Netlist (`kicad-cli sch export netlist`, sobre una copia) comparada con el plan, pin a pin: 24/24 redes iguales. Las etiquetas jerárquicas se unen con las locales del mismo nombre.
- PDF de la copia (con `../libraries`): cajetín «Alimentación: protecciones, limitador, buck y 3,3 V», hoja Alimentacion, rev. 2.0-dev, 2026-11-06, A3, 4/5. Revisado a la vista: sin textos superpuestos relevantes.
- MCP: no se cargó ningún proyecto (las herramientas de esquema escriben directamente en el archivo); `close_project` → «nothing to close». Sin `.lck`.

### Repaso de `checklists/esquema.md` v5

| Punto | Estado |
|---|---|
| Hojas por bloque, sin huérfanas | Cumple (pines de hoja con NC provisional) |
| Cajetín en el PDF | Cumple (ver arriba) |
| ERC sin errores; avisos justificados | Cumple: 0 / 0 |
| Referencias anotadas, sin duplicados | Cumple (sin las reservadas al MCU) |
| `Value`, `Footprint`, `LCSC Part#`, `MPN`, `Datasheet`, `Description` | Cumple; JP1 y TP sin LCSC (sin pieza; fuera de BOM y de posiciones) |
| Huella existente (KIC-01) | Cumple: oficiales de KiCad 10 o `esp-riego` (tabla del proyecto) |
| DNP | No aplica: no hay piezas sin montar (JP1 y TP no son piezas) |
| Cálculos con fórmula, fuente y margen | Cumple (SPEC-0017/0018; DEC-0007 no cambia valores) |
| Recalculado por el revisor | Validación |
| Tensiones nominales ≥ nodo | Cumple (§3.5, sin cambios) |
| *Derating* de cerámicos | Cumple; C14663 justificado en §7 |
| E_AS, *hold-up* | No aplica |
| Disipación | Cumple (§5, sin cambios) |
| Polaridad, fusible y TVS para 5,1 A | Cumple: Q1, F1 y D2 en la hoja según §3.2–§3.4 |
| TVS tras la polaridad; zéner de V_GS | Cumple: D2 tras Q1; D1 K en S, A en G |
| Divisor de VIN | Cumple: R14/R15/C20 → `VIN_SENSE` |
| Limitador: buck antes; banda; habilitación con *pull-down* | Cumple: U2 desde `VIN_PROT`, U1 → `BUS_24V`, R2 4,30 kΩ, R5 a GND |
| IN/DEN con el bus apagado | No aplica (bloque de salidas) |
| VRWM y Vc | Cumple (§3.4–§3.5) |
| UVLO tras protecciones y ajustable | Cumple: R9/R10 desde `VIN_PROT` |
| Presupuesto (ALI-12) | Cumple (§4) |
| VBUS sin retroalimentación (ALI-08) | Cumple: U3 TPS2116, MODE = VIN1, PR1 con R11/R12 |
| Microcontrolador | No aplica (pines propuestos en §6; los asigna el bloque MCU) |
| Salidas e interfaces de campo | No aplica |
| Tabla de restricciones de layout | Cumple (§8, JP1 actualizado) |

## Pendiente

- **ing-layout:** sincronizar la PCB con el esquema (55 huellas, sin colocarlas) para dejar la paridad a 0. Serigrafía de JP1 (§8).
- **jr-conformidad:** `bloque-alimentacion.md` con R8 → C136967 y los 100 nF → C14663 (Basic, 2026-11-06); recuento de líneas Extended (sale C1591). Confirmar los `LCSC Part#` de la hoja, que van rellenos con los códigos de §7.
- **SPEC-0022 (MCU) y la spec de salidas:** quitar las marcas de no conexión de los pines de `Alimentacion` en la raíz al cablearlos. Quitar el PWR_FLAG de VBUS de esta hoja si la MCU pone otro.
- Firmware: no aplica (no hay `firmware/` y el pinout aún no está en el esquema).

## Notas para el siguiente agente

- Los scripts que generan la hoja están en el *scratchpad* (`s19_plan.py` = posiciones y redes); no se versionan. Para cambios pequeños, editar con KiCad o con el MCP.
- `alimentacion.kicad_sch` está en A3. Coordenadas de bloques: entrada y = 63,5; limitador x 220–350; buck y 178/216; U3 x 244; U4 y VIN_SENSE x 330–394.
