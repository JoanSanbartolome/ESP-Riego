---
spec: SPEC-0022
agente: ing-layout
n: 02
fecha: 2026-11-07
estado: completado
---

# SPEC-0022 · 02 · ing-layout

## Orden recibida

SPEC-0022 · rama spec/SPEC-0022-hoja-mcu (activa en C:\Users\josan\proyectos\KICAD_mcp) · Lee: gestion/specs/SPEC-0022-hoja-mcu.md (paso 2) + gestion/logs/SPEC-0022/01-ing-esquematicos.md (Verificación y Pendiente) + gestion/logs/SPEC-0019/05-ing-layout.md (método de sincronización por script usado entonces) + gestion/informes/VAL-0019-02.md si existe (cruce pad↔netlist) · Haz: sincroniza hardware/v2/esp-riego.kicad_pcb con el esquema usando la netlist de kicad-cli: entran las 21 huellas de la hoja MCU (U5, U6, J2, J3, SW1, SW2, D5, C23–C26, R16–R25) fuera del contorno, agrupadas, sin colocar ni rutar; quita las huellas de la v1 del bloque MCU que ya no existan en el esquema; asigna a los 11 pads afectados las redes renombradas /VBUS, /VIN_SENSE, /LIM_IMON, /LIM_FLT y /LIM_EN. Comprueba el cruce pad↔netlist de todas las huellas nuevas y renombradas. Objetivo: python herramientas/verificar.py hardware/v2 con ERC 0, DRC sin errores (sin conectar por no rutar, anotados) y paridad 0. No toques el esquema ni coloques nada (la serigrafía «STATUS» de D5 es del layout posterior: solo anótala). Único usuario de KiCad: comprueba que no hay .lck, save y close_project al terminar. · Entrega: PCB + log gestion/logs/SPEC-0022/02-ing-layout.md con la salida de verificar.py y el cruce. Brevedad: en tu respuesta solo el contrato de salida; log telegráfico.

- Rama `spec/SPEC-0022-hoja-mcu` ✔. `check_kicad_ui`: KiCad no corre; sin `.lck`.

## Contexto consultado

- SPEC-0022 (paso 2); log 01 de SPEC-0022 (Verificación, Pendiente); log 05 de SPEC-0019; VAL-0019-02 (cruce netlist↔PCB).
- `hardware/v2/esp-riego.kicad_pcb` antes: 59 huellas (H1–H4 + 55 de Alimentacion), 0 pistas/vías/zonas.
- Checklist `gestion/checklists/layout.md` v5.

## Acciones

1. Copia de `hardware/v2` + `hardware/libraries` en el *scratchpad* (`…/scratchpad/l22/`, sin `esp-riego-backups/`).
2. Netlist: `kicad-cli sch export netlist --format kicadsexpr` sobre la copia (Eeschema 10.0.6).
3. Script `l22/sync.py` (el de SPEC-0019, ruta de librería adaptada y origen de las nuevas en y = 120), con `python.exe -I` de KiCad 10.0.6:
   - 21 huellas nuevas desde la librería del campo `Footprint` (3 `esp-riego:`, resto oficiales), con `path`, `sheetname/sheetfile`, campos ocultos y 3D de la librería;
   - redes de la netlist en todos los pads numerados (incluidas `unconnected-(…)`);
   - 11 pads renombrados: C5.1, R4.2 → `/LIM_IMON`; C15.1, U3.6 → `/VBUS`; C20.1, R14.2, R15.1 → `/VIN_SENSE`; R5.1, U1.12 → `/LIM_EN`; R6.2, U1.14 → `/LIM_FLT`;
   - borradas: ninguna (la PCB no tenía huellas de la v1 del bloque MCU).
4. Colocación fuera del contorno (100–200 × 60–130), bajo el bloque de Alimentacion: x 10,0–63,7, y 120,0–197,6 (*courtyard*), filas J/D · U · C · R · SW. Sin rutar, sin zonas, sin bloquear.
5. Copiado solo el `.kicad_pcb` al repo (el `.kicad_pro` no se toca).
6. MCP: no se cargó ningún proyecto; `close_project` → «nothing to close».

## Decisiones y justificación

- Script en lugar de `sync_schematic_to_board`: el MCP no da paridad 0 en jerárquicos (log 05 de SPEC-0019).
- Sin `PCB_GROUP`: agrupadas por posición, como en SPEC-0019.
- U5: *bbox* 48 × 41 mm por el dibujo de la zona de antena de la huella; queda fuera del contorno.

## Verificación

`python herramientas/verificar.py hardware/v2` (repo, tras copiar):

- ERC 0 (errores 0, avisos 0).
- DRC 0 (errores 0, avisos 0), **sin conectar 172** (108 antes + 64 de la hoja MCU): todo sin rutar.
- Paridad 0. Resultado «CON INCIDENCIAS» solo por los sin conectar.

Cruce pad↔netlist (`l22/cruce.py`, `pcbnew` frente a la netlist `kicadsexpr`), todas las huellas:

- 80/80 referencias; huella, valor, `path`, `LCSC Part#` y `MPN` iguales; red de los 310 pads numerados igual a la netlist; pines de la netlist sin pad: 0; pads sin número con red: 0 → **0 diferencias**.
- 21 nuevas: ninguna toca el contorno; sin solapes de *courtyard* entre ellas ni con las de Alimentacion; 21/21 con modelo 3D.
- `git diff --patience` del `.kicad_pcb`: +5 865 / −11; las 11 líneas quitadas son solo las `(net "/Alimentacion/…")` de los 11 pads renombrados.

### Repaso de `gestion/checklists/layout.md` v5

Reglas y verificación
- `.kicad_dru` y clases: no aplica (sin cambios de reglas).
- DRC sin errores: cumple; sin conectar 172 → pendiente del rutado (fuera de alcance).
- Paridad: cumple (0).
- Zonas rellenadas: no aplica (no hay zonas).
- Cajetín en PDF: no aplica (sin cambios de cajetín).
- `embedded_files`: cumple (no hay).
- `outputdirectory`: cumple (sin cambios, vacío).
- Cruce pad↔netlist por usar script (propuesta de VAL-0019-02, aún no en v5): cumple (0 diferencias).

Floorplan, Potencia y cargas, Masa, Fabricación y montaje: no aplica (sin colocar ni rutar; la spec excluye colocación).

3D y mecánica
- Modelo 3D en todos: parcial — nuevas 21/21; siguen sin modelo H1–H4, TP1–TP5 y JP1 (pendiente de SPEC-0019, FAB-11).
- Caja: no aplica.

## Pendiente

- **Layout (spec de colocación):** serigrafía «STATUS» junto a D5 (`mcu.md` §12); vías del EPAD de U5 (12, VAL-0021-01-03: abiertas a 0,10 mm de la pasta); resto de restricciones de `mcu.md` §12 (antena en borde, MCU-02).
- **Coordinador:** la propuesta de VAL-0019-02 (ítem de cruce pad↔netlist) sigue fuera de `layout.md` v5.
- `hardware/v2/esp-riego-backups/` y `esp-riego.kicad_prl` existían antes de esta spec (ignorados por git, del 2026-11-05/06); no los he tocado.

## Notas para el siguiente agente

- Huellas de la hoja MCU fuera del contorno en x 10–64, y 120–198; las de Alimentacion siguen en x 10–92, y 60–113.
- Scripts `sync.py` y `cruce.py` en `C:\Users\josan\AppData\Local\Temp\claude\2c54f79e79dd3002\dfbda2c0-57ad-4610-8ff3-7cd189c858eb\scratchpad\l22\` (no versionados); reutilizables para las hojas siguientes cambiando `LIBS` e `Y0`.
