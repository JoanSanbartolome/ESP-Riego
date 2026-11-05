---
id: SPEC-0016
titulo: Mantenimiento de las fases 0 a 2
fase: 2
estado: cerrada
responsable: ing-esquematicos
revisor: ing-validacion
rama: spec/SPEC-0016-mantenimiento-fases-0-2
requisitos: [REL-03, REL-05, KIC-01]
depende_de: []
creada: 2026-11-05
cerrada: 2026-11-05
validacion: VAL-0016-02
---

# SPEC-0016 · Mantenimiento de las fases 0 a 2

> Spec de mantenimiento (DEC-0005): reúne las observaciones B y las correcciones de texto pendientes de las fases 0–2, que no bloquean. Sustituye a SPEC-0008 y SPEC-0012, que se descartan por haberse agrupado aquí. Se abre cuando el usuario lo indique; el trabajo es de dos agentes, uno detrás de otro, y la validación es ligera.

## Objetivo

Los documentos, fichas y fuentes heredados de las specs anteriores quedan sin afirmaciones superadas ni restos pendientes.

## Alcance

- Incluye, para **ing-esquematicos**:
  - todo el alcance de SPEC-0008 (correcciones del estudio de salidas: VAL-0005-01 02, 03, 04, 06, 08, 09 y 10; VAL-0007-01-03; VAL-0011-01-08).
- Incluye, para **jr-conformidad**:
  - todo el alcance de SPEC-0012 (VAL-0010-01-01 y 02, notas de la importación de la v1; VAL-0013-02-03, las casillas vacías de `ESP-Riego.kicad_wks`), salvo la checklist de librerías, ya hecha;
  - VAL-0015-02-01: actualizar `hardware/libraries/3d/fuentes-solidcraft/INFORME.md` (pads del TDSO en ±2,73, Figura 15 en la p. 15 de la V7.3, lado de entrada del cable del borne, `kicad_test/` no versionado, extremo del STEP del borne en y = 5,6);
  - VAL-0015-02-02: numeración visible de los grupos de pines apilados de BTT6050-1ERA y BTT6030-2ERA (p. ej. «OUT 10–12»), si el primer bloque de salidas no lo ha hecho ya;
  - observación de ing-layout en SPEC-0014: «KiCad E.D.A. 10.0.6» pisa la línea de la casilla derecha de `ESP-Riego.kicad_wks`.
- Excluye:
  - cambios de requisitos o de diseño;
  - VAL-0014-01-01 y 02 (textos de bloque y tablas de librerías de `hardware/v2`), que hace el primer bloque.

## Entradas

- `gestion/specs/SPEC-0008-correcciones-estudio-salidas.md` y `SPEC-0012-notas-importacion-v1.md` (alcances detallados).
- Los informes citados.

## Entregables

- Los archivos corregidos y los logs `gestion/logs/SPEC-0016/01-ing-esquematicos.md` y `02-jr-conformidad.md`, con el repaso de checklist.

## Criterios de aceptación

- [x] Cada observación del alcance está corregida o justificada una a una en el log de su autor.
- [x] Los criterios de aceptación de SPEC-0008 y SPEC-0012 se cumplen.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-05 | coordinador | Crea la spec (propuesta) | |
| 2026-11-05 | coordinador | Abre la spec | |
| 2026-11-05 | coordinador | Cierra la spec | VAL-0016-02 (APROBADO) |
