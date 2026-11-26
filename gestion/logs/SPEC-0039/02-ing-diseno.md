---
spec: SPEC-0039
agente: ing-diseno
n: 02
fecha: 2026-11-24
estado: completado
---

# SPEC-0039 · 02 · ing-diseno

## Hecho

- Barrido de los 23 `antiguo` de `superados.csv` (literal y variantes: «220 nF 100 V», «100×70», «+ 20 %», «TLV1117LV33…») en `docs/diseno/`, `herramientas/kicad/` y `firmware/` (no existe): 124 coincidencias, todas en `docs/diseno/` → 7 `actualizar`, 86 `histórica`, 0 `otra placa`, 31 fuera del `alcance`. Lista con archivo, línea, término, clase y acción: `gestion/logs/SPEC-0039/barrido-ing-diseno.csv`.
- `actualizar`: `conectores.md` l. 242 y 353 (huella y patio de J10 horizontal), `sensores.md` l. 57 y `mcu.md` l. 75 (100 × 100 mm), `salidas.md` l. 428 (C_OUT junto a C28233), `estudio-coste.md` l. 48 (C513710 ya no se comparte con salidas) y l. 187 (C_VS de 100 nF; no es literal de la lista, mismo dato).
- `histórica`: rótulo «hasta SPEC-0037» junto al término (en `conectores.md` l. 66, `salidas.md` l. 240 y `alimentacion.md` l. 8 y 249 ya estaba). Los candidatos de U4 que no se eligieron llevan «descartado en SPEC-0038» (`alimentacion.md` l. 245; `estudio-coste.md` l. 63).
- Fuera de alcance: C3/C8 (C513710, 220n 100V, CC0805KKX7R0BB224), C23162 en R24/R25 y la escalera, «+20 %» de la deriva del LDO y de la serigrafía T02, y un falso positivo en `colocacion-b.csv`.
- Borrados `docs/diseno/colocacion-b`, `-b2` y `-b3` (`.csv` y `.png`). Citas por commit: `experimento-colocacion.md` (b `abbcc5e`, b2 `80a7b8f`, b3 `36b804c`), `estudio-coste.md` l. 22 y 188 y `herramientas/kicad/README.md` («Pruebas»).
- `herramientas/kicad/README.md`: sección «Recetas» nueva (cambiar campos o huella sin mover; pasar la batería en un repositorio falso).
- Memoria: 8 archivos y 192 afirmaciones → 5 archivos por tema, 96 líneas (78 VIGENTE, 72 DUPLICADA, 25 OBSOLETA, 10 ESTADO, 7 RECETA). Clasificación: `gestion/logs/SPEC-0039/memoria-ing-diseno.csv`.
- `herramientas/kicad/test_kicad.py`: copia de la batería. `ColocacionPaso5` y `ColocacionPaso6` sacan b2 y b3 de su commit (`de_commit`) y evalúan sobre `hardware/v2` de `d0705a7` (último antes de SPEC-0038, J10 vertical), copiado a la carpeta temporal con las librerías de la batería (`v2_j10_vertical`). Lo que afirman las pruebas no cambia.

## Decisiones y desviaciones

- `conectores.md` §4 (reparto de bordes con 100 × 70) y `sensores.md` §5.1 (calentamiento con A = 0,014 m²) quedan como históricos y no se recalculan: §4 lo sustituye b4, y con 100 × 100 mm (0,020 m², 5,0 K/W frente a 7,1) las cifras de §5 son una cota alta.

## Verificación

- Grep tras el barrido: cada línea con un `antiguo` lleva «hasta SPEC-00NN» o «descartado en SPEC-0038», o es una de las 31 fuera de alcance.
- `gestion.py comprobar`: 0 incidencias en la memoria de ing-diseno (las de jr-conformidad e ing-validacion, de los pasos 3 y 4). `test_kicad.py Generales`: OK.
- Batería entera de la copia (`python herramientas/kicad/test_kicad.py`): 70 pruebas, OK (189 s). Los 3 fallos de `ColocacionPaso5/6` venían de SPEC-0038 (J10 horizontal en `hardware/v2`; b3 daba 16 obligatorias) y se resuelven con la PCB de `d0705a7`.
- Sin cambios en `hardware/v2`: `verificar.py` no aplica.

## Pendiente

- Coordinador: llevar `herramientas/kicad/test_kicad.py` a `herramientas/pruebas/`.
- Fuera de mi zona citan b, b2 o b3 por nombre: DEC-0016 y DEC-0017 (cuerpo), VAL-0037-01 y SPEC-0037 (registros) y la memoria de ing-validacion (paso 4).
