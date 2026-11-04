---
spec: SPEC-0009
agente: ing-validacion
n: 02
fecha: 2026-11-04
estado: completado
---

# SPEC-0009 · 02 · ing-validacion

## Orden recibida

SPEC-0009 · rama spec/SPEC-0009-importar-v1 · commit revisado 265b5ae · Hay que validar la spec criterio a criterio con comprobaciones propias:

- `verificar.py` e `integridad_tfg.py`;
- rutas absolutas y tipos EasyEDA;
- nicknames;
- formato KiCad 10;
- netlist y recuentos de la PCB frente a una copia sin migrar.

También hay que confirmar o refutar la explicación del DRC 40 → 39 y comprobar la fidelidad de las piezas al original. Entrega: `VAL-0009-01.md` y este log.

## Contexto consultado

- La spec, `CLAUDE.md`, `docs/01-analisis-v1.md` §1–§3, `docs/03-plan-de-diseno.md` (fase 1), `docs/02` (KIC-01), `checklists/librerias.md` v1 y `proceso.md` v2.
- Los entregables de `hardware/`.
- La plantilla del informe.
- El log `01-jr-conformidad.md`, leído **después** de formar los hallazgos.

Rama `spec/SPEC-0009-importar-v1`, HEAD `265b5ae`.

## Acciones

1. Copias en `scratchpad\val9\` (solo lectura del TFG, con `Copy-Item` hacia fuera):
   - `orig/`: proyecto sin migrar.
   - `libs_tfg/`: `Llibreries_Kicad`.
   - `repo/`: entregables.
2. `verificar.py` sobre `hardware/v1-tfg`, con `md5sum` antes y después (sin cambios), y sobre `orig/`. Comparación de los JSON de DRC, ERC y paridad con un script.
3. `integridad_tfg.py verificar` al empezar y al terminar: OK, 337 archivos.
4. Netlists XML de `kicad-cli` (`orig` frente a `repo`) comparadas por componentes, campos, redes y `libparts`.
5. Migración propia `up/` con `kicad-cli sch|pcb upgrade` y `diff` con los entregables. Esquemas idénticos; en la PCB solo cambian 53 líneas `(model …)`.
6. Comparación de las geometrías de la PCB (huellas, segmentos, vías y zonas) con un script.
7. Resolución de todos los `lib_id` y campos `Footprint` contra las tablas nuevas y las globales de KiCad 10: 0 sin resolver.
8. Cajetín: SVG del esquema con el `.wks` y sin él (resuelve).
9. Librerías:
   - `kicad-cli sym upgrade` de los `.lib` y de los `.kicad_sym` del TFG;
   - `kicad-cli fp upgrade` de los `.kicad_mod`;
   - `diff` sin las UUID;
   - comparación de pads normalizada entre la librería y las instancias de la PCB;
   - comparación de pines entre la librería, `lib_symbols` y la conversión de EasyEDA.
10. Prueba de conversión de los JSON de EasyEDA con `kicad-cli fp/sym upgrade -o`: el Wemos (huella y símbolo) y el jack (3 pads) **se convierten**.
11. Resolución de `${KICAD9_3DMODEL_DIR}` con `kicad-cli pcb export step --component-filter` y `-D`: KiCad 10 la resuelve.
12. Comprobación de los `.wrl` en la instalación de KiCad 10: hay 0.
13. Revisión de la auditoría de `jr-conformidad` con un script: ninguna orden con `kicad-cli` ni llamadas al MCP sobre el TFG.

No usé el MCP ni escribí en el TFG ni en `hardware/`.

## Resultado

**APROBADO_CON_OBSERVACIONES**, con 2 hallazgos M y 3 B:

- 01 (M): el JSON del Wemos se convierte, así que el uso de las copias embebidas parte de una premisa falsa.
- 02 (M): `DC-Jack.pretty` está vacía, cuando el JSON tiene 3 pads.
- 03 (B): se cambió `KICAD9` → `KICAD10` con una justificación falsa.
- 04 (B): el diagnóstico de los `.wrl` es erróneo; 42 modelos apuntan a `.wrl` inexistentes en KiCad 10.
- 05 (B): `.gitattributes` no protege `.IGS` ni `.STEP` en mayúsculas.

Se confirma la explicación del DRC 40 → 39, que solo afecta a U1. Todos los criterios de aceptación se cumplen.

## Pendiente (para el coordinador)

- Decidir el hallazgo 01: convertir con `kicad-cli`, o aceptar la copia embebida como desviación y corregir el texto.
- Hallazgos 02–04: corregir el README y el log en una spec pequeña.
- Hallazgo 05: `.gitattributes`.
- Corregir `docs/01` §1 («38 vías» → 36) junto con el recuento de DRC.
- Propuestas para la checklist `librerias.md` en el informe.

## Notas para el siguiente agente

- En este equipo la unidad `G:` (Google Drive) está montada con `Llibreries_Kicad`: la copia «antes» resuelve las tablas originales, incluido el JSON de EasyEDA.
- `kicad-cli fp upgrade -o <dir> <archivo.json>` y `sym upgrade -o <archivo> <archivo.json>` convierten JSON de EasyEDA Std.
- Los scripts de comparación (`netcmp.py`, `pcbcmp.py`, `pads2.py`, `pins.py`, `resolve.py` y `drcdiff.py`) están en `scratchpad\val9\`.
