---
spec: SPEC-0014
agente: ing-layout
n: 02
fecha: 2026-11-05
estado: completado
---

# SPEC-0014 · 02 · ing-layout

## Orden recibida

> SPEC-0014 · rama spec/SPEC-0014-limpieza-v2 (activa; no cambies de rama ni uses git para escribir) · Lee: gestion/specs/SPEC-0014-limpieza-v2.md (tú haces la parte de la PCB), CLAUDE.md, el log gestion/logs/SPEC-0014/01-ing-esquematicos.md (sección PENDIENTE para ti), gestion/informes/VAL-0013-02.md (observaciones 01 y 02), docs/02 (FAB-02, FAB-08), gestion/checklists/layout.md v5 · Haz: limpia hardware/v2/esp-riego.kicad_pcb: actualiza desde el esquema (quedan solo H1–H4), borra todas las huellas, pistas, vías, zonas y textos de la v1; contorno preliminar de 100 × 70 mm en Edge.Cuts con H1–H4 en las esquinas (margen razonable para M3) y un texto en User.Comments que lo marque como preliminar; reglas de FAB-02 en el proyecto (pista y separación ≥ 0,2 mm, vía 0,3/0,6 mm, cobre a borde ≥ 0,5 mm); pcbplotparams/outputdirectory vacío; quita de embedded_files la copia del Cajetin_Kicad.kicad_wks del TFG; comment 1 de la PCB = «Placa de control de riego». Además, en esp-riego.kicad_pro, borra los netclass_patterns y netclass_assignments heredados de la v1 (REL1–4, ECHO, TRIG, /ESP32_EN…), dejando solo la clase Default; las clases de la v2 (FAB-03) llegan con el layout. No toques los esquemas, hardware/v1-tfg ni hardware/libraries. En paralelo trabaja jr-conformidad en otra spec sobre hardware/componentes y hardware/libraries/esp-riego.* (no los toques; ese agente no carga proyectos en el MCP, así que el MCP es tuyo). Si usas el MCP: guarda y close_project; sin .lck. Verifica con verificar.py hardware/v2 (objetivo: ERC 0 errores, DRC 0 errores y 0 sin conectar, paridad 0) y el cajetín de la PCB en un PDF exportado sobre una copia (copia también hardware/libraries junto a ella para que encuentre ESP-Riego.kicad_wks). · Entrega: hardware/v2/esp-riego.kicad_pcb, esp-riego.kicad_pro (y README.md si hace falta) + log gestion/logs/SPEC-0014/02-ing-layout.md. Responde con ESTADO, ARCHIVOS, VERIFICACIÓN, PENDIENTE y LOG.

## Contexto consultado

- `gestion/specs/SPEC-0014-limpieza-v2.md` (alcance de la PCB y criterios de aceptación).
- `gestion/logs/SPEC-0014/01-ing-esquematicos.md` (pendiente para ing-layout: borrar las 57 huellas de la v1 y conservar H1–H4, que necesitan el campo `LCSC Part#`).
- `gestion/informes/VAL-0013-02.md`, observaciones 01 (`outputdirectory "../../"`) y 02 (`embedded_files` con `Cajetin_Kicad.kicad_wks`).
- `docs/02-especificaciones-v2.md`: FAB-02, FAB-03, FAB-08, KIC-04 y MCU-02.
- `gestion/checklists/layout.md` v5, en lo que aplica a una placa vacía (reglas y verificación; dimensiones y 4 taladros M3).
- `hardware/v2/esp-riego.kicad_pcb`, `esp-riego.kicad_pro`, `conectores.kicad_sch` (campos de H1–H4) y `README.md`; `herramientas/verificar.py`.

## Acciones

1. Comprobaciones iniciales: rama `spec/SPEC-0014-limpieza-v2`; `check_kicad_ui`, KiCad no está abierto; `get_backend_state`, sin proyecto cargado; sin `.lck` en `hardware/v2`. MD5 de `hardware/v2/*`, `hardware/v1-tfg/*.kicad_*` y `hardware/libraries/*.kicad_wks` antes de empezar.
2. Inventario de la PCB por elementos de nivel 1: 61 huellas, 262 segmentos, 36 vías, 3 zonas, 2 `gr_rect`, 5 `gr_text`, 1 `embedded_files`. No hay declaraciones `(net …)` de nivel 1 (formato de KiCad 10), grupos, cotas ni otras gráficas. Los pads de H1–H4 no tienen red.
3. Limpieza de la PCB con un script propio (biblioteca estándar, en el *scratchpad*, `limpiar_pcb.py`). Trabaja sobre los hijos de nivel 1 del s-expr y conserva el texto original de todo lo que se queda y los CRLF:
   - **Quita** 57 huellas (todas menos H1–H4), 262 segmentos, 36 vías, 3 zonas, los 2 `gr_rect` (contorno de 129,0 × 96,5 mm y el rectángulo de serigrafía de la zona del 4–20 mA), los 5 `gr_text` de serigrafía («V_Nivel», «+12V», «+3.3V», «+5V», «DHT 11») y el bloque `embedded_files` con `Cajetin_Kicad.kicad_wks` (VAL-0013-02-02).
   - **Contorno** nuevo: `gr_rect` en `Edge.Cuts` de (100, 60) a (200, 130) mm, con un ancho de 0,05 mm (`board_outline_line_width` del proyecto).
   - **Texto** en `User.Comments` en el centro de la placa (150, 95), de 1,5 mm: «CONTORNO PRELIMINAR 100 x 70 mm (FAB-08, SPEC-0014) / Se fija en el floorplan: medidas, taladros y caja (D5)».
   - **H1–H4**: posición nueva en las mismas esquinas que en la v1, a 4 mm de los dos bordes (tabla en Decisiones). La referencia (`F.SilkS`) pasa al lado interior de la placa (y = +4,2 mm en los de arriba y −4,2 mm en los de abajo) para que la serigrafía no quede fuera del contorno; el valor (`F.Fab`) va al lado contrario. Se añade el campo `LCSC Part#` vacío y oculto en `F.Fab`, como lo escribe «Actualizar PCB desde el esquema» (quita las 4 incidencias `footprint_symbol_field_mismatch`). UUID, `path`, `locked` y el resto de la huella no cambian.
   - **Cabecera**: `comment 1` = «Placa de control de riego» (`title` sigue «ESP-Riego v2»); `pcbplotparams/outputdirectory ""` (VAL-0013-02-01); `aux_axis_origin` y `grid_origin` en (100, 130), la esquina inferior izquierda del contorno.
4. Proyecto (`limpiar_pro.py`, edición de texto que no reserializa el JSON; se comprueba al final que sigue siendo JSON válido):
   - reglas de FAB-02 (tabla en Decisiones);
   - tamaño de vía predefinido 0,45/0,3 → 0,6/0,3;
   - clases de red: solo `Default` (pista 0,2, separación 0,2, vía 0,6/0,3, sin cambios); se borran `power` y `signal`;
   - `netclass_assignments` (28 redes de la v1) → `null` y `netclass_patterns` (11 patrones: 3V3, GND, 5V, /GPIO0, /ESP32_EN, REL1–REL4, ECHO, TRIG) → `[]`, que es lo que KiCad escribe en un proyecto nuevo;
   - `drc_exclusions`: se quita la exclusión heredada del `starved_thermal` de U1 de la v1, que ya no existe.
5. Prueba completa sobre copias en el *scratchpad* antes de tocar `hardware/v2`:
   - `prueba/` y `prueba2/`, con `hardware/v2` y `hardware/libraries` copiados al lado; `verificar.py` sobre `prueba2/v2`: ERC 0, DRC 0, paridad 0.
   - **«Actualizar desde el esquema» con el MCP** sobre la copia `prueba2/v2`: `open_project` → `sync_schematic_to_board` («0 footprints added, 0 nets added, 0 pads assigned»; los 36 pads de H1–H4 no tienen red en el esquema y se dejan como están) → `get_design_rules` (pcbnew lee bien las reglas nuevas: separación 0,2, pista 0,2, vía 0,6/0,3, anillo 0,15, cobre a borde 0,5) → `close_project` con guardado. **La PCB guardada por pcbnew es idéntica byte a byte (`cmp`) a la del script.** Antes, en `prueba/`, la sincronización sin el campo `LCSC Part#` confirmó que el `sync` del MCP no copia campos de símbolo a huella, por eso el campo lo pone el script.
6. Se copian a `hardware/v2` la PCB y el proyecto ya verificados en la copia. **El proyecto real no se abrió en el MCP**, a propósito: al abrir y cerrar, incluso sin guardar, el MCP reescribe el `.kicad_pro` con todos los valores por defecto de KiCad 10 (≈ 60 líneas nuevas, entre ellas `top_level_sheets` con un UUID nulo `00000000-…`, que escribe pcbnew sin conocer el esquema) y deja `.kicad_prl` y `.mcp-backups/`. Como la PCB que pcbnew guarda tras sincronizar es idéntica a la entregada, no aporta nada y solo ensucia el diff. No hay zonas que rellenar.
7. `hardware/v2/README.md`: sección «PCB» nueva (contorno, taladros, reglas y clases) y estado de la verificación.

## Decisiones y justificación

- **Posición del contorno.** De (100, 60) a (200, 130) mm: deja la placa centrada en la zona útil de la hoja A4 y lejos del cajetín. Origen auxiliar y de rejilla en la esquina inferior izquierda (100, 130) para medir el *floorplan* desde ahí.
- **Taladros M3 a 4 mm de cada borde.** El pad de `MountingHole_3.2mm_M3_Pad_Via` mide 6,4 mm de diámetro: a 4 mm, el cobre queda a 0,8 mm del borde (FAB-02 pide ≥ 0,5 mm) y el patio (r = 3,45 mm), a 0,55 mm. Deja sitio a una cabeza DIN 912 M3 (Ø 5,5 mm) o a una arandela de Ø 7 mm sin salirse de la placa. Se fijará con la caja (D5) en el *floorplan*. Esquinas (las mismas que en la v1):

  | Ref. | Posición (mm) | Esquina |
  |---|---|---|
  | H3 | (104, 64) | arriba a la izquierda |
  | H1 | (196, 64) | arriba a la derecha |
  | H4 | (104, 126) | abajo a la izquierda |
  | H2 | (196, 126) | abajo a la derecha |

- **Anillo de los taladros sin red.** Se deja como llega del esquema: el DRC no da avisos. Si se quiere a GND (para la caja o para el cosido del plano, FAB-04) o NPTH, es un cambio de esquema de `ing-esquematicos` y se decide en el *floorplan*.
- **Reglas de FAB-02** (`board.design_settings.rules` del `.kicad_pro`):

  | Regla | v1 | v2 |
  |---|---|---|
  | `min_clearance` | 0,15 | 0,2 |
  | `min_track_width` | 0,15 | 0,2 |
  | `min_connection` | 0,15 | 0,2 |
  | `min_copper_edge_clearance` | 0,25 | 0,5 |
  | `min_via_diameter` | 0,5 | 0,6 |
  | `min_through_hole_diameter` | 0,3 | 0,3 |
  | `min_via_annular_width` | 0,1 | 0,15 (= (0,6 − 0,3)/2) |

  El resto (separación a taladro 0,25, taladro a taladro 0,25, serigrafía 0,15, texto ≥ 0,8 mm) no cambia. Las micro-vías no se usan (2 capas).
- **Clase `Default` sin cambios** (pista 0,2, separación 0,2, vía 0,6/0,3), que ya cumple FAB-02. FAB-03 pide `Default` con pista de 0,25 mm: se ajusta junto con `Power`, `Power_In` y `Salidas` y el `.kicad_dru` (KIC-04) en la spec de layout, como dice la orden.
- **Exclusión de DRC de la v1** retirada: apuntaba a una huella (U1) que ya no existe y no debe heredarse.
- **Sin el MCP en el proyecto real** (ver Acciones, punto 6). La «actualización desde el esquema» se hizo con el MCP sobre una copia idéntica y el resultado es el mismo archivo.

## Verificación

`python herramientas/verificar.py hardware/v2` (estado final):

```
ERC         0  (errores 0, avisos 0)
DRC         0  (errores 0, avisos 0, sin conectar 0)
Paridad     0
Resultado: LIMPIO
```

No queda ningún aviso que justificar.

- **PDF del cajetín:** `kicad-cli pcb export pdf --include-border-title --layers Edge.Cuts,User.Comments,F.SilkS,F.Cu --mode-single` sobre la copia `scratchpad\copia_pdf\v2\`, con `copia_pdf\libraries\` al lado (MD5 de `ESP-Riego.kicad_wks` igual al de `hardware/libraries`). Revisado como imagen:
  - «Placa de control de riego» en la casilla grande de arriba (`${COMMENT1}`) y «ESP-Riego v2» una sola vez (`${TITLE}`);
  - «Rev: 2.0-dev», «Date: 2026-11-05», «Joan San Bartolomé Ferri», «File: esp-riego.kicad_pcb» y «Hoja: Edge.Cuts» (comportamiento normal de pcbnew, aceptado en VAL-0013-02);
  - contorno de 100 × 70 mm, los 4 taladros en las esquinas con su referencia dentro de la placa y el texto de contorno preliminar en el centro.
- **Restos de la v1:** Grep en `hardware/v2` de `Cajetin`, `embedded_files`, `REL1`, `ECHO`, `ESP32_EN`, `"power"` y `"signal"`: 0 coincidencias. `outputdirectory` solo aparece una vez, vacío.
- **MD5 antes y después:** solo cambian `esp-riego.kicad_pcb` y `esp-riego.kicad_pro` (y el `README.md`, editado después). Los 5 `.kicad_sch`, `fp-lib-table`, `sym-lib-table`, `hardware/v1-tfg/*.kicad_*` y `hardware/libraries/*.kicad_wks` no cambian. La PCB mantiene CRLF y el proyecto, LF, como antes.
- **MCP:** `get_backend_state` al terminar: sin proyecto ni placa cargados. Las dos sesiones sobre copias se cerraron con `close_project`. No hay `.lck`, `-backups/`, `.mcp-backups/`, `.kicad_prl` ni `fp-info-cache` en `hardware/`.

## Pendiente

- **Coordinador / layout (FAB-03, KIC-04):** clases `Power`, `Power_In` y `Salidas`, `Default` a 0,25 mm y el `.kicad_dru` (zona de antena, separación de las salidas) en la primera spec de layout.
- **Floorplan:** confirmar el contorno de 100 × 70 mm (FAB-08 admite 70 ± 5 mm), la posición de los taladros con la caja (D5) y el texto de `User.Comments`, que se borra entonces. Decidir si el anillo de H1–H4 va a GND o sin red, o si son NPTH; es un cambio de esquema (`ing-esquematicos`).
- **Observación menor, zona de librerías:** en el cajetín, «KiCad E.D.A. 10.0.6» pisa la línea vertical de la casilla de la derecha. Viene de `ESP-Riego.kicad_wks` (no es de esta spec); se puede ajustar cuando se toque la hoja de dibujo.

## Notas para el siguiente agente

- El `sync_schematic_to_board` del MCP informa solo de huellas añadidas y pads asignados; **no copia campos del símbolo a la huella** (comprobado: con H1–H4 sin `LCSC Part#`, la paridad seguía en 4 después de sincronizar). La paridad `footprint_symbol_field_mismatch` hay que resolverla aparte. No se probó si borra huellas sobrantes: aquí se quitaron antes con script.
- Abrir el proyecto en el MCP reescribe el `.kicad_pro` (valores por defecto de KiCad 10 y `top_level_sheets` con UUID nulo), aunque se cierre sin guardar, y deja `.kicad_prl` y `.mcp-backups/`. Hay que revisar el diff del `.kicad_pro` y limpiar después de cada sesión del MCP.
- Los scripts de esta spec (`limpiar_pcb.py` y `limpiar_pro.py`) están solo en el *scratchpad* de la sesión; no forman parte del repositorio.
