---
id: SPEC-0021
titulo: Piezas del bloque MCU
fase: 2
estado: abierta
responsable: jr-conformidad
revisor: ing-validacion
rama: spec/SPEC-0021-piezas-mcu
requisitos: [MCU-01, MCU-02, MCU-03, MCU-04, MCU-05, MCU-06, MCU-07, FAB-02, FAB-11, KIC-01]
depende_de: [SPEC-0020, SPEC-0018]
creada: 2026-11-05
cerrada:
validacion:
---

# SPEC-0021 · Piezas del bloque MCU

## Objetivo

Todas las piezas de la lista de `docs/diseno/mcu.md` §11 tienen símbolo, huella y 3D resolubles desde `hardware/v2`, con sus campos completos, su tipo de JLCPCB (Basic/Extended) y su stock confirmados con fecha, y sus fichas en `hardware/componentes/`.

## Alcance

- Incluye:
  - **3D del pulsador TS-1187A** (SW1, SW2): KiCad 10.0 no trae el `.step` de `Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A` (comprobado por el coordinador el 2026-11-06). Se obtiene o se genera en `.step`, alineado con la huella (pin 1 con render, Y hacia arriba), en `hardware/libraries/3d/`, y se enlaza desde una copia de la huella en `esp-riego.pretty` si hace falta (FAB-11).
  - **Huella del módulo y FAB-02:** la oficial `RF_Module:ESP32-S3-WROOM-1` lleva 12 vías de 0,2 / 0,6 mm en el EPAD (pad 41), que no cumplen FAB-02 (0,3 / 0,6). Se crea `esp-riego:ESP32-S3-WROOM-1` a partir de la oficial con vías de 0,3 / 0,6 mm (con la máscara tal como la trae la oficial) o sin vías (las pone el layout), anotando la elección. Conserva la zona libre de la antena (*keepout*) en todas las capas (MCU-02), el modelo 3D oficial y el resto de pads sin cambios; se comprueba con `diff` frente a la oficial.
  - Cualquier otra huella de §11 con vías se revisa igual (checklist de esquema v6, punto FAB-02).
  - **Fichas nuevas** (Anexo A de `mcu.md`): `TS-1187A-B-A-B.md`, `KT-0603YG.md` (polaridad según la marca del PDF) y `B-2100S04P-A110.md`.
  - **Ficha `ESP32-S3-WROOM-1.md`:** variante **N8** (C2913198) fija, alternativa N16, la nota de la antena (§3) y que la placa no admite R8/R16V (GPIO35–37 en uso). Huella `esp-riego:ESP32-S3-WROOM-1`.
  - **Tipo Basic/Extended y stock de JLCPCB/LCSC**, con fecha, de **todas** las piezas de §11 (principales y alternativas), incluido C14663 (stock LCSC 0 el 2026-11-06: se confirma en la API de JLCPCB). Si una principal no tiene stock, se aplica DEC-0007 (cambio de compra equivalente que abarata o facilita, sin consulta) y se anota en el log para que el coordinador lo lleve a `mcu.md`.
  - Campos que llevarán los símbolos (`Value`, `Footprint`, `LCSC Part#`, `MPN`, `Fabricante`, `Datasheet`, `Description`): tabla en el log, lista para SPEC-0022.
- Excluye:
  - editar hojas del esquema o la PCB de `hardware/v2`;
  - cambiar valores o piezas elegidas en `mcu.md`, salvo cambios de compra de DEC-0007;
  - editar `docs/diseno/mcu.md` (los cambios se proponen en el log).

## Entradas

- `docs/diseno/mcu.md` (§0, §2, §3, §11, §12 y Anexo A) y `gestion/logs/SPEC-0020/01-ing-esquematicos.md`.
- `hardware/libraries/`, `hardware/componentes/` y las tablas de librerías de `hardware/v2`.
- Checklists `gestion/checklists/librerias.md` (v3) y `gestion/checklists/esquema.md` (v6, punto de FAB-02).
- DEC-0007 (cambios de compra).

## Entregables

- `hardware/libraries/esp-riego.pretty/ESP32-S3-WROOM-1.kicad_mod` (y la copia de la huella del TS-1187A si hace falta), `.step` del TS-1187A en `hardware/libraries/3d/`.
- Fichas nuevas y actualizada en `hardware/componentes/`.
- Log `gestion/logs/SPEC-0021/01-jr-conformidad.md` con: repaso de las checklists, tabla de stock y tipo con fecha, tabla de campos por referencia, renders y la lista de piezas que validación debe revisar contra su datasheet.

## Criterios de aceptación

- [ ] Cada pieza de §11 tiene símbolo, huella y 3D resolubles desde `hardware/v2`; pines y pads comprobados contra el datasheet (página citada).
- [ ] El 3D del TS-1187A existe en `.step`, alineado con la huella, con el pin 1 confirmado por render.
- [ ] Ninguna huella del bloque lleva vías fuera de FAB-02 (0,3 / 0,6 mm); la del módulo conserva el *keepout* de la antena en todas las capas.
- [ ] Tipo Basic/Extended y stock de todas las piezas de §11 con fecha; los cambios de compra, justificados con DEC-0007.
- [ ] Fichas TS-1187A-B-A-B, KT-0603YG y B-2100S04P-A110 creadas y la del ESP32-S3-WROOM-1 con la variante N8.
- [ ] Checklist de librerías v3 pasada punto por punto.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-05 | coordinador | Crea la spec (propuesta) | |
| 2026-11-06 | coordinador | Abre la spec (encargo del usuario): 3D del TS-1187A, FAB-02 en la huella del módulo, fichas y stock | |
