---
id: SPEC-0022
titulo: Hoja del MCU en el esquema v2
fase: 3
estado: propuesta
responsable: ing-esquematicos
revisor: ing-validacion
rama: spec/SPEC-0022-hoja-mcu
requisitos: [MCU-01, MCU-02, MCU-03, MCU-04, MCU-05, MCU-06, MCU-07]
depende_de: [SPEC-0021, SPEC-0019]
creada: 2026-11-05
cerrada:
validacion:
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

- `docs/diseno/mcu.md`, `gestion/logs/SPEC-0021/01-jr-conformidad.md`.
- Checklist `gestion/checklists/esquema.md`.

## Entregables

- `hardware/v2/mcu.kicad_sch`.
- Log `gestion/logs/SPEC-0022/01-ing-esquematicos.md` con el repaso de la checklist y la salida de `verificar.py`.

## Criterios de aceptación

- [ ] Cada pieza, valor y pin de la hoja coinciden con `docs/diseno/mcu.md`.
- [ ] `verificar.py hardware/v2`: ERC 0, sin errores de paridad nuevos.
- [ ] Ninguna pieza de la hoja usa una librería de la v1.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-05 | coordinador | Crea la spec (propuesta) | |
| 2026-11-07 | coordinador | Añade al alcance lo que trae SPEC-0021 (huellas, tabla de campos, `mcu.md` y cambios de compra de DEC-0007) | VAL-0021-01 |
