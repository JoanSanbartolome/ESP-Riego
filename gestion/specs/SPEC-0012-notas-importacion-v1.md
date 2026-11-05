---
id: SPEC-0012
titulo: Notas de la importación de la v1 y checklist de librerías v2
fase: 1
estado: descartada
responsable: jr-conformidad
revisor: ing-validacion
rama: spec/SPEC-0012-notas-importacion-v1
requisitos: [KIC-01]
depende_de: [SPEC-0010]
creada: 2026-11-05
cerrada:
validacion:
---

# SPEC-0012 · Notas de la importación de la v1 y checklist de librerías v2

> Propuesta: observaciones B de VAL-0010-01 y propuestas de checklist de VAL-0009-01 y VAL-0010-01. Solo documentación: no cambia ninguna librería ni el proyecto de la v1. Prioridad baja; conviene hacerla antes de la primera spec que importe o cree piezas para la v2.

## Objetivo

La documentación de la importación de la v1 no contiene afirmaciones superadas, y la checklist de librerías recoge lo aprendido en SPEC-0009 y SPEC-0010.

## Alcance

- Incluye:
  - **VAL-0010-01-01:** el pad 3 de `DC-Jack.pretty` no es un artefacto. Es un pad `custom` con polígono (3,56 × 1,60 mm, taladro oblongo de 3 × 1 mm), equivalente a los pads 1 y 2 girados 90°. Hay que corregirlo en:
    - `hardware/v1-tfg/README.md` l. 25;
    - `gestion/logs/SPEC-0010/01-jr-conformidad.md` l. 30, 44 y 49;
    - `gestion/logs/SPEC-0009/01-jr-conformidad.md` l. 98;
    - y quitar «pad 3 del jack» de los pendientes para la v2.
  - **VAL-0010-01-02:** en la sección «Corrección (SPEC-0010)» del log de SPEC-0009, anular dos afirmaciones:
    - el pendiente de la l. 82 (38 en `docs/01` §2; lo correcto es 39, que es lo que ya dice);
    - la tabla de las l. 73–74, que llama «copia embebida» a las piezas del Wemos (el símbolo siempre fue la conversión; ahora la huella también).
  - ~~**Checklist `gestion/checklists/librerias.md` v2**~~: hecha por el coordinador al abrir SPEC-0015 (la necesitaba la recopilación de componentes). Sus puntos eran:
    - antes de dar un JSON de EasyEDA por no convertible, probar `kicad-cli fp|sym upgrade -o` y anotar la orden;
    - en las importaciones, comprobar la fidelidad con una conversión independiente y un `diff` sin las UUID, además de la comparación normalizada de los pads;
    - comprobar que los modelos `${KICADn_3DMODEL_DIR}` existen en KiCad 10, que no instala ningún `.wrl`;
    - comprobar que las extensiones de los modelos 3D, en mayúsculas y en minúsculas, están como `binary` en `.gitattributes`;
    - antes de llamar artefacto a un pad `custom`, medir la envolvente de sus primitivas;
    - al sustituir una pieza, comprobar con `git diff` que el archivo cambia, y anotarlo si sale idéntico.
  - **Checklist `proceso.md`:** cuando un log justifica una desviación con «no se convierte» o «no resuelve», validación la reproduce con una orden concreta.
- Incluye también VAL-0013-02-03 (parte de la hoja de dibujo): en `hardware/libraries/ESP-Riego.kicad_wks`, quitar o aprovechar las dos casillas que quedaron vacías (antes «Plano Nº» y «Escala»).
- Excluye: cambios de librerías o del proyecto de la v1, y las mejoras para la v2 (courtyard, `.step`, modelos SamacSys, tipos de pin del Wemos).

## Entradas

- `gestion/informes/VAL-0009-01.md` y `VAL-0010-01.md`.
- Los archivos y líneas citados arriba.
- `gestion/checklists/librerias.md` y `proceso.md`.

## Entregables

- README y logs corregidos, más el log `gestion/logs/SPEC-0012/01-jr-conformidad.md`.
- Checklists de librerías v2 y de proceso actualizadas, por el coordinador.

## Criterios de aceptación

- [ ] Ninguna parte de la documentación de la importación llama artefacto al pad 3 ni copia embebida a las piezas del Wemos.
- [ ] Ningún pendiente pide cambiar `docs/01` §2.
- [ ] Cada propuesta de checklist está incorporada o descartada con su motivo.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-05 | coordinador | Crea la spec (propuesta) | |
| 2026-11-05 | coordinador | La checklist de librerías v2 se adelanta a la apertura de SPEC-0015 | SPEC-0015 |
| 2026-11-05 | coordinador | Se descarta: su alcance se agrupa en SPEC-0016 (mantenimiento, DEC-0005) | SPEC-0016 |
