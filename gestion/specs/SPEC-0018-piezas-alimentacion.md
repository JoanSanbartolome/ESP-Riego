---
id: SPEC-0018
titulo: Piezas del bloque de alimentación
fase: 2
estado: cerrada
responsable: jr-conformidad
revisor: ing-validacion
rama: spec/SPEC-0018-piezas-alimentacion
requisitos: [ALI-01, ALI-02, ALI-03, ALI-04, ALI-05, ALI-06, ALI-07, ALI-08, ALI-09, ALI-10, ALI-11, ALI-12, ALI-13, KIC-01]
depende_de: [SPEC-0017]
creada: 2026-11-05
cerrada: 2026-11-05
validacion: VAL-0018-02
---

# SPEC-0018 · Piezas del bloque de alimentación

## Objetivo

Todas las piezas de la lista de `docs/diseno/alimentacion.md` tienen símbolo, huella y 3D en las librerías del proyecto, con sus campos completos y su disponibilidad en JLCPCB confirmada.

## Alcance

- Incluye:
  - símbolos, huellas y modelos 3D que falten, reutilizando las librerías oficiales de KiCad cuando existan;
  - campos `LCSC`, `MPN`, `Fabricante`, `Datasheet` y tipo de montaje de JLCPCB (básica o extendida) y stock;
  - fichas de `hardware/componentes/`: crear las del Anexo A de `docs/diseno/alimentacion.md` y añadir a la de TPS2663 la variante elegida;
  - huella de JP1 `esp-riego:SolderJumper-2_P1.8mm_Open_Pad1.2x3.0mm` (DEC-0006, hueco de 0,6 mm por VAL-0017-01-01; medidas en `alimentacion.md`);
  - VAL-0017-01-05: *derating* DC y térmico de los cerámicos con la curva del fabricante (prioridad: C11/C12 y C16/C17);
  - pendientes del log de SPEC-0017 (pines de SUD50P06-15 frente a SQD50P06-15L, de TLV1117-33 frente a TLV1117LV, símbolo de LMR36520 a partir de LMR36510ADDA, stock de R8).
- Excluye:
  - cambiar valores o piezas elegidas en SPEC-0017 (si una no está disponible, se propone una alternativa al coordinador);
  - editar los esquemas o la PCB de `hardware/v2`.

## Entradas

- `docs/diseno/alimentacion.md` (lista de piezas, SPEC-0017).
- `hardware/libraries/` y las tablas de librerías.
- Checklist `gestion/checklists/librerias.md`.

## Entregables

- Piezas nuevas en `hardware/libraries/` y fichas actualizadas.
- Log `gestion/logs/SPEC-0018/01-jr-conformidad.md` con el repaso de la checklist y la lista de piezas que validación debe revisar contra su datasheet.

## Criterios de aceptación

- [ ] Cada pieza de la lista tiene símbolo y huella resolubles desde `hardware/v2`, con su 3D.
- [ ] Pines y pads coinciden con el datasheet (página citada).
- [ ] Campos completos y stock en JLCPCB confirmados con fecha.
- [ ] La checklist de librerías está pasada punto por punto.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-05 | coordinador | Crea la spec (propuesta) | |
| 2026-11-05 | coordinador | Abre la spec (aprobada por el usuario) | |
| 2026-11-05 | coordinador | Cierra la spec; M de VAL-0018-02 corregida (vías 0,3/0,6, DRC 0 con U2 colocada) | VAL-0018-02 (APROBADO_CON_OBSERVACIONES) |
