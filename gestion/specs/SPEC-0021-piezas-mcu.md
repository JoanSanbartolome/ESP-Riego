---
id: SPEC-0021
titulo: Piezas del bloque MCU
fase: 2
estado: propuesta
responsable: jr-conformidad
revisor: ing-validacion
rama: spec/SPEC-0021-piezas-mcu
requisitos: [MCU-01, MCU-02, MCU-03, MCU-04, MCU-05, MCU-06, MCU-07, KIC-01]
depende_de: [SPEC-0020, SPEC-0018]
creada: 2026-11-05
cerrada:
validacion:
---

# SPEC-0021 · Piezas del bloque MCU

## Objetivo

Todas las piezas de la lista de `docs/diseno/mcu.md` tienen símbolo, huella y 3D en las librerías del proyecto, con sus campos completos y su disponibilidad en JLCPCB confirmada.

## Alcance

- Incluye:
  - símbolos, huellas y modelos 3D que falten, reutilizando las librerías oficiales de KiCad cuando existan;
  - campos `LCSC`, `MPN`, `Fabricante`, `Datasheet`, tipo de montaje de JLCPCB (básica o extendida) y stock;
  - fichas de `hardware/componentes/` del anexo de `docs/diseno/mcu.md` y actualización de las existentes (ESP32-S3-WROOM-1 con la variante elegida);
  - huella del módulo con la zona libre de la antena (MCU-02) como *keepout*.
- Excluye: editar hojas del esquema.

## Entradas

- `docs/diseno/mcu.md` y `gestion/logs/SPEC-0020/01-ing-esquematicos.md`.
- Librerías `hardware/libraries/` y checklist `gestion/checklists/librerias.md`.

## Entregables

- Librerías y fichas actualizadas.
- Log `gestion/logs/SPEC-0021/01-jr-conformidad.md`.

## Criterios de aceptación

- [ ] Cada pieza de la lista tiene símbolo, huella y 3D, con los pines comprobados contra el datasheet.
- [ ] Campos completos y stock de JLCPCB confirmado en la fecha.
- [ ] La huella del módulo lleva la zona libre de la antena en todas las capas.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-05 | coordinador | Crea la spec (propuesta) | |
