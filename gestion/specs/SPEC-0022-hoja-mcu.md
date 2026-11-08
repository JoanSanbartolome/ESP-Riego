---
id: SPEC-0022
titulo: Hoja del MCU en el esquema v2
fase: 3
estado: cerrada
responsable: ing-esquematicos
revisor: ing-validacion
rama: spec/SPEC-0022-hoja-mcu
requisitos: [MCU-01, MCU-02, MCU-03, MCU-04, MCU-05, MCU-06, MCU-07]
depende_de: [SPEC-0021, SPEC-0019]
creada: 2026-11-05
cerrada: 2026-11-07
validacion: VAL-0022-01
---

# SPEC-0022 · Hoja del MCU en el esquema v2

## Objetivo

La hoja `hardware/v2/mcu.kicad_sch` pasa a ser el bloque MCU de la v2, según `docs/diseno/mcu.md`, con el ERC limpio.

## Alcance

- Incluye:
  - sustituir el contenido de la hoja por el bloque de la v2, con las piezas de SPEC-0021;
  - etiquetas jerárquicas según la tabla de GPIO, conectadas con las de `alimentacion.kicad_sch`;
  - mantener la paridad esquema–PCB que exija `verificar.py` (piezas nuevas sincronizadas sin colocar; la sincronización con la PCB es de ing-layout, con la netlist de `kicad-cli`);
  - campos de cada símbolo según la «Tabla de campos por referencia» de `gestion/logs/SPEC-0021/01-jr-conformidad.md`, con las huellas `esp-riego:ESP32-S3-WROOM-1`, `esp-riego:SW_Push_1P1T_XKB_TS-1187A` y `esp-riego:USB_C_Receptacle_HRO_TYPE-C-31-M-12`;
  - actualizar `docs/diseno/mcu.md` con lo que trae SPEC-0021: §11 y Anexo A con esas huellas, stock de la N8 (2 776), TS-1187A y C14663 Basic, alternativa C318887 de 2,5 mm y 260 gf (no «misma altura»);
  - cambios de compra de DEC-0007 propuestos en SPEC-0021, con su recálculo en `mcu.md`: C23 → C15849 (Basic; EN ≈ 0,159·VDD, §5.1), D5 → KT-0603R C2286 (Basic, rojo; corriente con R23) y U6 → UMW USBLC6-2SC6 (C2687116) solo si se comprueba la equivalencia con el datasheet; si no, se queda el de ST;
  - los cambios a `mcu.md` §9.2 y Anexo B que propone el log de SPEC-0023 (IS a 6 dB, R_IS 820 Ω, sin diodo), si SPEC-0023 está cerrada.
- Excluye: colocación y rutado; otras hojas, salvo las etiquetas que conecten con esta.

## Entradas

- `docs/diseno/mcu.md` (Anexo C: etiquetas), `gestion/logs/SPEC-0021/01-jr-conformidad.md` (tabla de campos) y `gestion/informes/VAL-0021-01.md`.
- `gestion/logs/SPEC-0023/01-ing-esquematicos.md` y `03-ing-esquematicos.md` (cambios propuestos a `mcu.md`) y `docs/diseno/salidas.md`.
- `hardware/v2/alimentacion.kicad_sch` (etiquetas que conectan con esta hoja).
- Fichas de `hardware/componentes/` de las piezas del MCU y `gestion/decisiones/DEC-0007`.
- Checklist `gestion/checklists/esquema.md` (v6).

## Pasos

1. **ing-esquematicos:** hoja `mcu.kicad_sch`, etiquetas y `mcu.md` (log 01). La paridad que quede pendiente se debe solo a las piezas de esta hoja y se lista en el log.
2. **ing-layout:** sincroniza `esp-riego.kicad_pcb` con el esquema (huellas nuevas fuera del contorno, agrupadas, sin colocar ni rutar; quita las de la v1 de este bloque que ya no existan) y comprueba el cruce pad↔netlist (log 02).
3. **ing-validacion:** validación completa.

## Entregables

- `hardware/v2/mcu.kicad_sch` y `docs/diseno/mcu.md`.
- `hardware/v2/esp-riego.kicad_pcb` sincronizada (paso 2).
- Logs `gestion/logs/SPEC-0022/01-ing-esquematicos.md` (repaso de la checklist y salida de `verificar.py`) y `02-ing-layout.md`.

## Criterios de aceptación

- [ ] Cada pieza, valor y pin de la hoja coinciden con `docs/diseno/mcu.md`.
- [ ] Campos (Footprint, Datasheet, LCSC, MPN; el tipo Basic/Extended va en `mcu.md` §11, no en el símbolo) según la tabla de campos del log 01 de SPEC-0021, con las tres huellas `esp-riego:`.
- [ ] Ninguna pieza de la hoja usa una librería de la v1.
- [ ] Etiquetas jerárquicas de la hoja según el Anexo C de `mcu.md`, conectadas con las de `alimentacion.kicad_sch`.
- [ ] `mcu.md` recoge las huellas, el stock y los cambios de compra de DEC-0007 con su recálculo (EN con C15849, corriente de D5 con R23, decisión sobre U6 justificada con el datasheet) y los cambios de §9.2/Anexo B de SPEC-0023.
- [ ] Tras el paso 2, `verificar.py hardware/v2`: ERC 0, DRC sin errores (los sin conectar por no rutar se anotan) y paridad 0.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-05 | coordinador | Crea la spec (propuesta) | |
| 2026-11-07 | coordinador | Añade al alcance lo que trae SPEC-0021 (huellas, tabla de campos, `mcu.md` y cambios de compra de DEC-0007) | VAL-0021-01 |
| 2026-11-07 | coordinador | Abre la spec; añade los pasos (sincronización de la PCB por ing-layout) y criterios verificables | VAL-0019-01-01 |
| 2026-11-07 | coordinador | Cierra la spec; M-01 (ficha y polaridad del KT-0603R) y B-02/B-03 corregidas y comprobadas con Grep; B-04 (D5 rojo) queda a confirmar por el usuario | VAL-0022-01 (APROBADO_CON_OBSERVACIONES) |
