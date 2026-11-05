---
spec: SPEC-0015
agente: ing-validacion
n: 03
fecha: 2026-11-05
estado: completado
---

# SPEC-0015 · 03 · ing-validacion

## Orden recibida

Revalidación ligera (DEC-0005) del commit `daa0aa6` frente a `2e0b34a`: comprobar los 10 hallazgos de VAL-0015-01 y confirmar que `hardware/v2`, la v1 y el TFG no cambian.

## Acciones

1. Rama `spec/SPEC-0015-recopilacion-componentes`, commit `daa0aa6`. `git diff 2e0b34a HEAD --stat`: nada en `hardware/v2` ni `hardware/v1-tfg`. `integridad_tfg.py verificar`: intacto. `revisar_zonas.py jr-conformidad`: bien.
2. Leí la huella TDSO-14 y la comparé con la imagen del land pattern de Infineon (`v15\dl_infineon\footprint.png`, de VAL-0015-01).
3. Placa de prueba en `scratchpad\v15c\` con las 2 huellas propias, la oficial del SHT4x (con el 3D de respaldo) y `libraries/3d/`: `pcb render` top y `--side left`, recortes ampliados; `pcb drc` (solo `lib_footprint_issues` de la prueba); caja de los STEP con `CARTESIAN_POINT`.
4. Comparé el borne con la sección A-A de Kangnex (`v15\wjs_0.png`).
5. Muestreo: PDF del BSP752R (p. 5 y 6) y SHT4x V7.3 (p. 15 a 17) en imagen o texto; descarga de dos PDF de Infineon y MD5; `sym export svg` de los símbolos; cuentas de precio.
6. Informe `gestion/informes/VAL-0015-02.md`.

## Resultado

APROBADO_CON_OBSERVACIONES: 10 hallazgos de VAL-0015-01 cerrados (el 10, en parte) y 2 observaciones B nuevas (INFORME de SolidCraft desactualizado, con el marco del borne a 5,6 mm; numeración de los grupos apilados en los símbolos). Sin MCP.
