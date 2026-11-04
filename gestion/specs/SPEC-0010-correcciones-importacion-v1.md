---
id: SPEC-0010
titulo: Correcciones de la importación de la v1
fase: 1
estado: propuesta
responsable: jr-conformidad
revisor: ing-validacion
rama: spec/SPEC-0010-correcciones-importacion-v1
requisitos: [KIC-01]
depende_de: [SPEC-0009]
creada: 2026-11-04
cerrada:
validacion:
---

# SPEC-0010 · Correcciones de la importación de la v1

> Propuesta: hallazgos 01–04 de VAL-0009-01. **Necesita una decisión del usuario sobre el Wemos (hallazgo 01)** antes de abrirse. La etiqueta `v1.1-tfg` se pone al cerrar esta spec.

## Objetivo

Las librerías de la v1 en `hardware/libraries/` son fieles a las del TFG (o la desviación queda aceptada y documentada), y el README y el log de la importación no contienen justificaciones falsas.

## Alcance

- Incluye:
  - **01 (M), Wemos:** según la decisión del usuario,
    - (a) sustituir el símbolo y la huella de `Wemos s2 mini` por la conversión del JSON de EasyEDA con `kicad-cli sym|fp upgrade -o`, fiel al TFG; el DRC vuelve a 40;
    - (b) mantener la copia embebida, fiel a la placa fabricada, y documentarla como desviación aceptada.
  - **02 (M):** añadir a `DC-Jack.pretty` la huella convertida del JSON con `kicad-cli fp upgrade -o`, tal cual, y anotar el artefacto del pad 3.
  - **03 y 04 (B):** corregir `hardware/v1-tfg/README.md` y añadir una corrección al log:
    - `${KICAD9_3DMODEL_DIR}` sí resuelve en KiCad 10; el cambio a `KICAD10` se mantiene porque es inocuo;
    - los modelos no se ven porque KiCad 10.0.6 no instala los `.wrl`.
  - `docs/01-analisis-v1.md` §1: 36 vías, no 38. Lo corrige el coordinador, porque `docs/01` está fuera de la zona del agente.
- Excluye: cualquier cambio de diseño de la v1, y las mejoras para la v2 (`.step`, courtyard, modelos SamacSys, tipos de pin del Wemos), que van a la copia de trabajo de la v2.

## Entradas

- `gestion/informes/VAL-0009-01.md` (hallazgos 01–04, con las órdenes de conversión).
- `gestion/logs/SPEC-0009/01-jr-conformidad.md` y `02-ing-validacion.md`.
- `hardware/v1-tfg/README.md` y `hardware/libraries/`.
- Origen de solo lectura: las carpetas `Wemos` y `DC Jack` de `C:/Users/josan/proyectos/TFG/Llibreries_Kicad/`.

## Entregables

- Las librerías y el README corregidos, y el log `gestion/logs/SPEC-0010/01-jr-conformidad.md`.

## Criterios de aceptación

- [ ] Cada hallazgo 01–04 está corregido o justificado con la orden que lo reproduce.
- [ ] `verificar.py hardware/v1-tfg` da ERC 1, paridad 77 y DRC 40 (opción a) o 39 (opción b), sin otras diferencias.
- [ ] El TFG sigue intacto (`integridad_tfg.py verificar`).

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-04 | coordinador | Crea la spec (propuesta) | |
