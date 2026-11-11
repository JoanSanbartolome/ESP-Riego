---
id: SPEC-0028
titulo: Mantenimiento de las fases 2 y 3
fase: 3
estado: propuesta
responsable: ing-diseno
revisor: ing-validacion
rama: spec/SPEC-0028-mantenimiento-fases-2-3
requisitos: []
depende_de: []
creada: 2026-11-11
cerrada:
validacion:
---

# SPEC-0028 · Mantenimiento de las fases 2 y 3

## Objetivo

Corregir las observaciones B y M no bloqueantes acumuladas en las fases 2 y 3. Se abre al cerrar la fase 3 o cuando acumule bastante trabajo (DEC-0005). El coordinador añade aquí una línea por observación nueva.

## Alcance

- Incluye:
  - **Campos (VAL-0024-01-07):** `Datasheet` distinto para la misma pieza según la hoja, `Fabricante` ausente en `alimentacion.kicad_sch` y `Value` del LED sin unificar («Rojo» en D4, «LED» en D5). Con `campos.py` de SPEC-0027.
  - **Fichas:** `verificado_por` de `BTT6050-1ERA.md` y `WJ500V-5.08-2P.md` sigue «pendiente».
  - **Documentos:** cambios propuestos en `gestion/logs/SPEC-0023/01-ing-esquematicos.md` a `alimentacion.md` y a `estudio-salidas.md` S7; citar la página del pinout (VAL-0021-01-07).
  - **Checklists:** `librerias.md`, cobertura de pasta y tratamiento de las vías en pads expuestos, y Grep de todas las menciones del rasgo cambiado al proponer cambios a un documento (VAL-0024-01); `layout.md`, cruce pad ↔ netlist (VAL-0019-02).
  - **Proyecto:** versionar el `.kicad_pro` que reescribe KiCad 10 al abrirlo, si el usuario lo quiere.
  - **Posible:** campo de tipo *Basic*/*Extended* en los símbolos de todas las hojas.
- Excluye: lo que es del layout o de la fabricación, que está en `gestion/ESTADO.md` (vías y pasta del EPAD de U5, polígono BUS_24V, serigrafía «STATUS», estado de las vías en los Gerber).

## Entradas

- Los informes y partes citados en cada línea.

## Entregables

- Por definir al abrirla.

## Criterios de aceptación

- [ ] Por definir al abrirla: uno por línea del alcance.

## Plan de validación

Nivel **ligero**, salvo que alguna línea toque una huella o una hoja: entonces, completo para esa parte.

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-11 | coordinador | Crea la spec (propuesta) | | | | |
| 2026-11-11 | coordinador | Recoge las observaciones de los diarios del 2026-11-07 y del 2026-11-10 | DEC-0009 |  |  |  |
