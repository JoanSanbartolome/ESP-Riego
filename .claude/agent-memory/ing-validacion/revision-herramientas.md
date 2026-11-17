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

- **Revalidación (VAL-0027-02):** `mutar2.py` reutiliza los helpers de `mutar.py` (exec hasta `CASOS = [`) y comprueba el detalle con «contiene», porque en `hardware/v2` `fichas` y `attr` ya fallan. Para medir falsos positivos de una heurística nueva, se pasa `huella.analizar` sobre una muestra de la librería oficial (0 de 867). La USB-C con patas `pad_prop_mechanical` es `smd` para KiCad: no es mixta. `--refill-zones` se demuestra con una zona real sin rellenar, creada con `pcbnew` (salen `isolated_copper`, md5 intacto).

- **Batería de casos nuevos (VAL-0028-01, ~2 h toda la spec):** para mutar las herramientas, uso un repositorio falso en la carpeta temporal con `CLAUDE.md`, `herramientas/` y `hardware/{v2,libraries,componentes}`. `test_kicad.py` localiza la raíz por `CLAUDE.md`. En `v28\mutar.py`, cada mutación es (archivo, texto, sustituto, casos): se aplica, se corre el caso y se restaura. Sobreviven los casos con datos fijos que ya cumplen la regla, como una lista ya ordenada o un «ya existe» sin el archivo homónimo. No hay que fiarse de «la mutación X falla» del parte: el autor suele invertir, no quitar.
- `git archive` lo bloquea la guarda: para sacar `main` a la carpeta temporal, `for f in $(git ls-tree --name-only main hardware/v2/); do git show main:$f > …; done`. Un `mkdir` en la misma orden que un heredoc de Python con `sys.argv` también se bloquea: el script, con Write.

Relacionado: [[revision-hojas]], [[revision-piezas]], [[comprobaciones-utiles]].
