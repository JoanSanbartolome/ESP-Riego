---
spec: SPEC-0009
agente: jr-conformidad
n: 01
fecha: 2026-11-04
estado: completado
---

# SPEC-0009 · 01 · jr-conformidad

## Orden recibida

SPEC-0009 · rama spec/SPEC-0009-importar-v1 · Lee: gestion/specs/SPEC-0009-importar-v1.md, CLAUDE.md, docs/01-analisis-v1.md §1–§3, gestion/checklists/librerias.md · Haz: la spec entera (copiar del TFG en solo lectura a hardware/v1-tfg/, librerías nativas con los mismos nicknames en hardware/libraries/ incluida la hoja de dibujo y los modelos 3D, tablas con ${KIPRJMOD}, migración a KiCad 10 sin tocar el diseño, comprobación con verificar.py e integridad_tfg.py; referencia «antes» sobre copia sin migrar en el scratchpad; diferencias inexplicables: no corregir y devolver como pendiente) · Entrega: hardware/v1-tfg/, hardware/libraries/ + este log.

## Contexto consultado

`gestion/specs/SPEC-0009-importar-v1.md`, `CLAUDE.md`, tablas de librerías y `.kicad_pro` del TFG (lectura), contenido de `Llibreries_Kicad`. Rama comprobada leyendo `.git/HEAD` (`spec/SPEC-0009-importar-v1`). Sin `.lck` en `hardware/` (no existía).

## Acciones

1. Copia (solo lectura del TFG) de los 7 archivos del proyecto, `sym-lib-table` y `fp-lib-table` a `hardware/v1-tfg/`, y `Panel_Control.kicad_sch` a `referencia/`. Misma copia sin migrar en el scratchpad (`scratchpad/antes/`) para la referencia «antes».
2. Librerías en `hardware/libraries/` con los nicknames originales:
   - Símbolos `PS2705-1-F3-A`, `BC817-25-7-F`, `1548129`, `PRT-10811`: `.lib` + `.dcm` copiados al scratchpad y convertidos con `kicad-cli sym upgrade -o`. Primero probé los `.kicad_sym` que hay junto a los `.lib` en la librería del TFG, pero el esquema se había hecho con los `.lib` y daban 8 `lib_symbol_mismatch` nuevos en el ERC; la conversión del `.lib` (con su `.dcm`, que aporta la descripción) los elimina.
   - Huellas `.kicad_mod` copiadas a `PS2705.pretty`, `BC817-25-7.pretty`, `PRT10811.pretty`, `KiCad.pretty` (la 1548129), `PhoenixTerminal.pretty` (114 archivos) y `SMMS0530-150M.pretty` (2); `kicad-cli fp upgrade` a formato 10.
   - `Wemos s2 mini` (símbolo y huella): el JSON de EasyEDA no se convierte con KiCad; se extrajo la copia embebida en `wemos_s2mini.kicad_sch` (`lib_symbols`) y en la PCB (huella: sin `at`, UUID, red, `path`/`sheetname`/`sheetfile`; referencia `REF**`), con un script en el scratchpad.
   - `DC-Jack.pretty`: el JSON de EasyEDA (`PCB_DC-IN-TH_XDJK-0051-025`) contiene solo un contorno y una referencia al paquete, sin pads. No hay nada que extraer y la huella no se usa en la PCB (el jack es `Connector_BarrelJack:BarrelJack_Kycon_KLDX-0202-xC_Horizontal`). Carpeta vacía con `.gitkeep` para que el nickname siga resolviendo.
   - Hoja de dibujo `Cajetin_Kicad.kicad_wks` y `3d/` (`TLP185.step`, `Transistor.IGS`, `PSMT3012.STEP`, `Wemos S2 Mini V1.0.0.step`).
3. `sym-lib-table` y `fp-lib-table` reescritas con `${KIPRJMOD}/../libraries/...` y tipo `KiCad`.
4. Cambios de ruta (todos mecánicos con `sed`):
   - `.kicad_pro`: líneas 694 y 875 `page_layout_descr_file` a `${KIPRJMOD}/../libraries/Cajetin_Kicad.kicad_wks`; línea 691 `"svg"` (ruta `C:/Users/josan/Desktop/…`, último directorio de exportación) a `""`. Es el único otro cambio del `.kicad_pro` (`diff` con el original).
   - `.kicad_pcb`, 10 `(model …)` con `G:/…` a `${KIPRJMOD}/../libraries/3d/…`: TLP185.step (líneas 515, 4060, 9407, 14442), Transistor.IGS (838, 10128, 10849, 15185), Wemos S2 Mini V1.0.0.step (5573), PSMT3012.STEP (6564).
   - `.kicad_pcb`, 43 `${KICAD9_3DMODEL_DIR}` a `${KICAD10_3DMODEL_DIR}`: `kicad-cli pcb export step` en KiCad 10 daba «File not found» con el nombre antiguo y deja de darlo con el nuevo.
   - Footprints de `PhoenixTerminal.pretty`: `${KISYS3DMOD}` a `${KICAD10_3DMODEL_DIR}` (no se usan en la PCB, que usa la librería oficial `TerminalBlock_Phoenix`).
   - Los esquemas no tenían rutas absolutas.
5. Migración a formato 10 con `kicad-cli sch upgrade --force` (5 hojas + `Panel_Control`) y `kicad-cli pcb upgrade --force` (no se usó el MCP, no hizo falta). Versiones: esquema `20260306`, PCB `20260206`. Borrados los `.kicad_prl` que crea kicad-cli en `hardware/v1-tfg/`.
6. Ni el MCP ni `kicad-cli` abrieron nada del TFG: todo lo que se leyó con kicad-cli estaba en `hardware/` o en el scratchpad.

## Decisiones y justificación

- Mantener nicknames originales aunque dos no encajen en el esquema habitual (`KiCad` para la 1548129): lo pide la spec y los `lib_id` ya resuelven.
- Un `.kicad_sym` por nickname (no un único `esp-riego.kicad_sym`), porque la spec exige conservar los nicknames. Cuando se cree la librería de la v2 (SPEC posterior) se decidirá si se unifica.
- Convertir desde `.lib`+`.dcm` en lugar de usar los `.kicad_sym` ya presentes: reproduce exactamente lo que el esquema tenía embebido (ERC 1 = 1).
- DC-Jack vacía: no hay origen recuperable; inventar la pieza sería crear una huella sin datasheet y no se usa.

## Verificación

`python herramientas/verificar.py` (antes = copia sin migrar en scratchpad con las tablas originales `G:/…`; después = `hardware/v1-tfg`):

| | Antes | Después |
|---|---|---|
| ERC | 1 (`pin_to_pin`) | 1 (`pin_to_pin`) |
| DRC | 40 (1 error `starved_thermal`, 39 `lib_footprint_mismatch`, 0 sin conectar) | 39 (1 error `starved_thermal`, 38 `lib_footprint_mismatch`, 0 sin conectar) |
| Paridad | 77 (61 `footprint_symbol_field_mismatch`, 10 `net_conflict`, 6 `footprint_symbol_mismatch`) | 77 (igual) |

**Diferencia explicada (DRC 39 → 38):** desaparece el aviso `lib_footprint_mismatch` de U1 («Footprint 'WEMOS-S2-MINI' does not match copy in library 'Wemos s2 mini'»). Los otros 38 son idénticos (comparados uno a uno por tipo, descripción y posición). Causa: antes la huella de la librería era el JSON de EasyEDA y no coincidía con la copia embebida; ahora la librería es esa misma copia embebida, así que coincide. No procede de ningún cambio del diseño. Si el coordinador prefiere el recuento 39 literal, habría que usar otra versión de la huella; no lo veo recomendable. El análisis de la v1 (`docs/01-analisis-v1.md` §2) deberá citar 38 tras esta importación.

**Netlist** (`kicad-cli sch export netlist --format kicadsexpr`, original vs `hardware/v1-tfg`; comparación semántica con script): 61 componentes con mismos valor, huella y campos; 70 redes con los mismos nodos (ref, pin). Idénticas.

**PCB** (comparación antes/después con script): 61 huellas con misma posición, capa, lib_id y redes por pad; 262 segmentos, 36 vías, 3 zonas y 7 elementos `gr_*` idénticos. El recuento de `(net N …)` pasa de 71 a 0 solo porque KiCad 10 ya no guarda la tabla de redes (se identifican por nombre).

**Símbolos y huellas:** no hay símbolos ni huellas no encontrados (el ERC/DRC no dan `lib_symbol_issues` ni `footprint_not_found`). `kicad-cli pcb export step` ya no da «File not found» de ningún modelo 3D resuelto con `${KIPRJMOD}` ni `${KICAD10_3DMODEL_DIR}` (el mensaje «Could not add 3D model» que sigue saliendo para los `.wrl` es una limitación del exportador de STEP, no de la ruta).

`python herramientas/integridad_tfg.py verificar`: «TFG intacto: 337 archivos coinciden con la huella».

Comprobaciones finales: sin `.lck`, `-backups/`, `.kicad_prl` ni `fp-info-cache` en `hardware/`; búsqueda de `G:/`, `C:/Users`, `EasyEDA`, `JLCEDA`, `KICAD9`, `KISYS` en `hardware/` (salvo modelos 3D binarios): 0 coincidencias. Nota: `3d/Transistor.IGS` lleva en su cabecera una ruta `C:\Users\980006740\…` del autor del modelo (dato interno del IGES, no una ruta de carga).

## Requiere verificación de validación

Piezas creadas o modificadas por mí (las valida `ing-validacion`):

| Pieza | Qué es | Datasheet y página |
|---|---|---|
| Símbolo `Wemos s2 mini:WEMOS-S2-MINI (ESP32-S2FN4R2)` | Extraído de la copia embebida en el esquema (origen: JSON de EasyEDA, contribuidor `sergiy_gurin`) | https://www.wemos.cc/en/latest/s2/s2_mini.html (esquema de pines) |
| Huella `Wemos s2 mini:WEMOS-S2-MINI` | Extraída de la PCB (sin rediseño); 32 pads | https://www.wemos.cc/en/latest/s2/s2_mini.html (dibujo mecánico) |
| Símbolos `PS2705-1-F3-A`, `BC817-25-7-F`, `1548129`, `PRT-10811` | Convertidos de `.lib` a `.kicad_sym` (SamacSys) sin editar | PS2705: https://www.renesas.com/us/en/document/dst/ps2705-1-data-sheet-0; BC817-25-7-F: https://www.diodes.com/assets/Datasheets/ds11107.pdf; 1548129 y PRT-10811: enlaces del campo `Datasheet` de cada símbolo |
| Huellas importadas (`PS2705`, `BC817-25-7`, `PRT10811`, `KiCad`, `SMMS0530-150M`, `PhoenixTerminal`) | Copiadas y actualizadas de formato, sin editar | los mismos de arriba; página del dibujo recomendado no revisada |

Son piezas de la v1 conservadas tal cual; la validación de fondo (huella vs datasheet) corresponde a la v2.

## Pendiente

- Coordinador: actualizar `docs/01-analisis-v1.md` §2 (DRC: 38 `lib_footprint_mismatch`, no 39, en el proyecto importado) y revisar si la etiqueta `v1.1-tfg` se pone con este estado.
- `DC-Jack.pretty` está vacía (sin origen recuperable); sin consecuencias en la v1.
- Los `.kicad_sym`/`.kicad_mod` del TFG (SamacSys) tienen modelos 3D por nombre relativo (`BC817-25-7-F.stp`, `1548129.stp`…) que no existen: preexistente, no corregido. Las huellas de la PCB usan rutas propias a `3d/`.
- Nada de diseño ha cambiado; H1–H12 siguen abiertos para la v2.

## Notas para el siguiente agente

- `kicad-cli` recrea `Control_De_Riego.kicad_prl` al leer el proyecto; `verificar.py` lo borra, pero si usas `kicad-cli` directamente, bórralo.
- Las librerías están planas en `hardware/libraries/` con un archivo por nickname; las tablas de `hardware/v2/` pueden apuntar a las mismas con `${KIPRJMOD}/../libraries/...`.
- Los scripts de extracción (`conv.py`, `extraer.py`) y las referencias «antes» están en el scratchpad de esta sesión, no se versionan.
