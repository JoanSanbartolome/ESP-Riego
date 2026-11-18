---
spec: SPEC-0035
agente: ing-diseno
n: 04
fecha: 2026-11-18
estado: completado
---

# SPEC-0035 · 04 · ing-diseno

Corrección de VAL-0035-01: hallazgos 01, 03, 04 y 06. La PCB no cambia.

## Hecho

- **01 · `_estilo.py`:** los textos se miden por su tinta real, con la fuente newstroke medida en el SVG de `kicad-cli`. Medí avance, tinta y alto de los 119 caracteres de las hojas, la línea base según la justificación, la interlínea (1,61) y el trazo (0,1524 mm). Holgura de 0,05 mm.
  - Coincide con el SVG a ±0,003 mm: «TLV1117LV33DCYR» mide 17,29 mm, frente a los 15,24 de antes.
  - La vertical también fallaba: las mayúsculas quedaban 0,3-0,5 mm por encima de la caja.
- **Casos reales corregidos en las hojas:**
  - Alimentación: el valor de C16 tocaba C17. C16 pasa a x 101,6.
  - Alimentación: C7, C22 y C8 estaban a 0,5 mm. Pasan a 26,67, 44,45 y 62,23 (VIN_PROT a 24,13) y quedan a 1,8-3 mm.
  - MCU: la etiqueta LED_STATUS se solapaba con BTN_INT. Su cable llega ahora a x 193,04.
- **03 · `hoja.py paginas`** (nuevo): numera las páginas en el orden del árbol; sin `-o` solo comprueba. `generar` avisa cuando da páginas nuevas.
  - Orden: Salidas 2, Canal1–6 3–8, MCU 9, Alimentación 10, Conectores 11 y Sensores 12.
  - En el PDF, el «Id» de las 12 hojas coincide con su página.
- **04 · README de `herramientas/kicad/`:** líneas 69–73 de `esquema.md` v16, con las 25 filas comprobadas. Añadidos la fila de `paginas` y los límites nuevos.
- **06 · `esquema.pcb_main`:** solo cuenta lo que va tras la marca de sección descrita en el README (`comprobar.seccion_huellas`), en la SPEC o en los partes. El parte 03 la cumple: 84 huellas, todas declaradas.

## Verificación

- `verificar.py hardware/v2`: ERC 0, DRC 0 (448 sin conectar: placa sin rutar), paridad 0. [auto]: 25, con 23 OK, 0 FALLA y 2 N/A. `campos.py revisar`: 0 diferencias. Netlist por grupos frente a `main`: 0 diferencias.
- Batería nueva, pasada en el repositorio falso del scratchpad (`…\v35b\repo`): `C:\Users\josan\AppData\Local\Temp\claude\2c54f79e79dd3002\c980b02f-1588-4782-8921-adea897769ca\scratchpad\v35b\repo\herramientas\pruebas\test_kicad.py`.
- Pruebas nuevas:
  - `Mutaciones.test_esquema_cruces_texto_largo`: un cable a 0,5 mm del final de la «R» falla, y otro a 0,24 mm pasada la tinta no.
  - `Hoja.test_tinta_frente_al_svg` (9 textos, ±0,03 mm), `Hoja.test_paginas_en_orden_del_arbol` y `Generales.test_lineas_de_checklist_del_readme`.
  - `test_esquema_pcb_main`: una referencia citada fuera de la sección ya no cuenta.
- Imágenes: `…\scratchpad\v35b\alim_fix.png` y `…\v35b\mcu_fix.png`. PDF: `…\v35b\esquema.pdf`.

## Pendiente

- **Coordinador:** sustituir `herramientas/pruebas/test_kicad.py` por la batería del scratchpad. Propuesta para la checklist: un punto `[auto]` con las páginas en el orden del árbol (ya lo comprueba `hoja.py paginas`, código 1).
