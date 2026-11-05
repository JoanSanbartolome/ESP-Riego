---
spec: SPEC-0016
agente: jr-conformidad
n: 02
fecha: 2026-11-05
estado: completado
---

# SPEC-0016 · 02 · jr-conformidad

## Orden recibida

SPEC-0016 · rama spec/SPEC-0016-mantenimiento-fases-0-2 · parte de jr-conformidad (alcance de SPEC-0012 salvo checklist de librerías, VAL-0015-02-01/02, observación de SPEC-0014 sobre el cajetín).

## Acciones

| Observación | Estado | Dónde |
|---|---|---|
| VAL-0010-01-01 pad 3 del jack | Corregida: pad `custom` válido (polígono 3,56 × 1,60 mm, taladro oblongo 3×1), sin «artefacto» | `hardware/v1-tfg/README.md` l. 25; SPEC-0010 log l. 30, 44, 49 (quitado de pendientes v2); SPEC-0009 log, sección Corrección |
| VAL-0010-01-02 «38» y «copia embebida» | Anuladas con viñeta en «Corrección (SPEC-0010)» de SPEC-0009: el pendiente de `docs/01` §2 (38) y los «copia embebida» de la tabla. No se reescribe el texto original (es un registro histórico con sus correcciones) | `gestion/logs/SPEC-0009/01-jr-conformidad.md` |
| VAL-0013-02-03 casillas vacías | Corregida: quitada la línea y = 37 de la columna derecha (la casilla vacía de «Plano Nº» queda fusionada con la de la fecha); Date a y = 32 y Size a y = 12 (junto a Id). Comprobado en PDF de `hardware/v2` (copia en el scratchpad, `kicad-cli sch export pdf`) | `hardware/libraries/ESP-Riego.kicad_wks` |
| Obs. SPEC-0014 «KiCad E.D.A. 10.0.6» pisa la línea | Corregida: `KICAD_VERSION` de x = 53,12 a 58; ya no toca la línea x = 32. Comprobado en PDF | ídem |
| VAL-0015-02-01 INFORME | Corregida: pads TDSO ±2,73 (tabla y texto, con nota de que el pie del modelo queda dentro del pad); Figura 15 en p. 15 de la V7.3; huella del borne ya marca el lado de entrada; `kicad_test/` marcado como no versionado; extremo del STEP del borne y = 5,6 (marco de la ventana; el cuerpo llega a 5,5; sobresale 0,6 mm, dentro del courtyard 5,75) | `hardware/libraries/3d/fuentes-solidcraft/INFORME.md` |
| VAL-0015-02-02 pines apilados | Corregida: nombres de los 3 pines apilados «OUT (10-12)» en BTT6050; «OUT0 (12-14)» y «OUT1 (8-10)» en BTT6030 (todos los de cada grupo, para no mezclar nombres en un mismo punto). Números sin cambio. No lo había hecho el primer bloque (v2 aún no usa los símbolos) | `hardware/libraries/esp-riego.kicad_sym` |
| Checklist `librerias.md` v2 y `proceso.md` | No aplica: ya hechas por el coordinador | — |

## Requiere verificación de validación

| Pieza | Qué es | Datasheet y página |
|---|---|---|
| Símbolos `BTT6050-1ERA` y `BTT6030-2ERA` | Solo nombres visibles de los pines OUT apilados | BTT6050-1ERA Rev 1.00 y BTT6030-2ERA, §3.2 Tabla 2, p. 4 |
| `ESP-Riego.kicad_wks` | Hoja de dibujo: línea quitada y 3 textos movidos | no aplica |

## Verificación

- `verificar.py hardware/v2`: ERC 0 · DRC 0 · paridad 0 · LIMPIO (tras el cambio de la `.kicad_wks`; no se usó el MCP).
- `kicad-cli sym upgrade` sobre `esp-riego.kicad_sym`: lee sin error («not updated», ya en formato actual).
- PDF previo y posterior del esquema raíz: cajetín sin solapes.

**Repaso de checklists** (`librerias.md`, `proceso.md`)
- Tablas de librerías sin rutas absolutas: sin cambios, no tocadas.
- Piezas modificadas listadas para validación: cumple.
- Campos de componentes, aprovisionamiento, fichas, fabricación: no aplica.
- Términos obsoletos («artefacto», «copia embebida», «38»): revisados en README v1 y logs 0009/0010; el texto original de SPEC-0009 (l. 25, 55, 73) se conserva y queda anulado en su sección Corrección.
- Pendiente: validación ligera de textos y del cajetín; verificar visualmente el símbolo con `sym export svg`.

## Pendiente

- Coordinador: tipo y stock de montaje JLCPCB del BTT6050, BTT6030 y limitador (VAL-0005-01-09, según el log 01) cuando pasen al esquema; no estaba en mi alcance.
