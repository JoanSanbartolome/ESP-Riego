---
name: revision-herramientas
description: Cómo validar herramientas/kicad y los puntos [auto: comprobar.py …] de las checklists (VAL-0027-01): mutaciones por punto, comparadores independientes de PCB y netlist, trampas de formato
metadata:
  type: feedback
---

Un punto de checklist que pasa a `[auto]` se valida haciéndolo fallar, no viéndolo dar OK sobre `hardware/v2`.

**Por qué:** en VAL-0027-01 (2026-11-12), la batería pasaba 20/20, pero 8 de los 19 puntos de `comprobar.py` no tenían ningún caso que los hiciera fallar. Mis mutaciones sacaron tres huecos M: `smd_cara` depende de `(attr smd)`, que el BTT6050 no lleva; `zonas` no ve un relleno anticuado ni multicapa; `restricciones` no deriva el ancho de la corriente.

**Cómo aplicarlo:**
- `scratchpad\val27\mutar.py` (copia base → mutación → `comprobar.resumen(punto)`), `pcbcmp.py` (huella a huella: fpid, campos con capa y visibilidad, atributos, ruta y redes de los pads) y `netcmp.py` (netlist kicadxml con campos y propiedades, y partición de redes). Son de la sesión: se rehacen en 10 min.
- `hoja.py netlist` (`_comun.comparar_netlists`) **no compara propiedades** (dnp, exclude_from_*): uso mi netlist kicadxml.
- Los `.kicad_mod` propios tienen **CRLF**: las mutaciones por texto necesitan `\r\n`. Al sustituir texto en una hoja, la primera aparición suele estar en `lib_symbols`: hay que anclarla a la instancia (`Reference "R16"`).
- Para probar `restricciones.py` con el formato real, se añaden pistas, un arco y una vía con `pcbnew` (`PCB_TRACK`, `PCB_ARC`, `PCB_VIA`) a una copia. En KiCad 10 las pistas llevan `(net "nombre")`.
- Ojo con `comprobar.py` sobre una copia fuera del repositorio: `librerias.gitattributes` da N/A, y sin `componentes/` `librerias.fichas` también da N/A. Hay que pasarlo también sobre `hardware/v2` (solo lee).
- Contrastar las marcas de la checklist con lo que mide el script: los puntos con corriente o ΔT, «relleno al día» y «dentro de fabricacion/» suelen quedar a medias.

Relacionado: [[revision-hojas]], [[revision-piezas]], [[comprobaciones-utiles]].
