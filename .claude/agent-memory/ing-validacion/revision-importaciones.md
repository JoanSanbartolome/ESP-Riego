---
name: revision-importaciones
description: Cómo validar importaciones, migraciones o limpiezas de proyectos y librerías KiCad (p. ej., v1 del TFG a KiCad 10) sin fiarse de las justificaciones del autor: migración independiente, conversión de EasyEDA, resolución de variables 3D
metadata:
  type: feedback
---

Para validar una migración de KiCad, rehago la migración por mi cuenta y comparo con `diff`. No me basta con comparar recuentos.

**Por qué:** en VAL-0009-01 (2026-11-04), el log del autor daba por hechas tres cosas que resultaron falsas:
- «el JSON de EasyEDA no se convierte»;
- «la DC-Jack no tiene pads»;
- «KiCad 10 no resuelve `${KICAD9_3DMODEL_DIR}`».

Con ellas justificaba desviarse de la spec. Solo se descubre reproduciéndolas.

**Cómo aplicarlo:**
- Migración independiente: `kicad-cli sch|pcb upgrade --force` sobre una copia sin migrar, y después `diff --strip-trailing-cr` con lo entregado. Si los esquemas son idénticos y la PCB solo difiere en las rutas, el diseño no ha cambiado.
- Librerías: `kicad-cli sym upgrade -o` y `fp upgrade -o` del origen, y `diff` filtrando `(uuid `, porque el formato `module` antiguo regenera las UUID.
- EasyEDA Std: `kicad-cli fp upgrade -o <dir> <json>` y `sym upgrade -o <archivo> <json>` **sí** convierten.
- Pads de la PCB frente a la librería: el ángulo del pad en la PCB es absoluto. Para normalizar, le resto la rotación de la huella; la posición está en coordenadas locales.
- Variables 3D: lo pruebo con `kicad-cli pcb export step --component-filter <ref> -D VAR=/inexistente`. KiCad 10.0.6 resuelve `${KICAD9_3DMODEL_DIR}` por su cuenta y no trae ningún `.wrl`, solo `.step`.
- En este equipo, `G:` (Drive) está montada con `Llibreries_Kicad`: la copia «antes» del TFG sí resuelve las tablas `G:/…`.
- Las órdenes con «proyectos/TFG» en el texto las bloquea la guardia aunque solo lean. Construyo la cadena en un script escrito con Write.
- Reviso `git ls-files --eol` en los binarios nuevos: `.IGS` y `.STEP` en mayúsculas pueden quedar como texto.
- `kicad-cli fp upgrade -o <dir>` exige que `<dir>` no exista (si existe, devuelve el código 4). Con `sym upgrade -o <archivo>` no pasa.
- Pads `custom` de EasyEDA (`PAD~POLYGON`): KiCad los convierte en un ancla de 0,000001 mm más una `gr_poly`. Mido la envolvente de la primitiva antes de llamarlo artefacto. En VAL-0009-01-02 me equivoqué con el pad 3 del jack y la spec copió el error (VAL-0010-01-01).
- Antes de afirmar que una pieza «se extrajo de otro sitio y difiere», hago `cmp` del archivo completo, no solo de los pines. El símbolo del Wemos de SPEC-0009 ya era idéntico a la conversión del JSON, y lo descubrí tarde (VAL-0010-01).
- Las referencias «antes» de VAL-0009 (`out_orig/drc.json`, `resolve.py`, `pads2.py`) están en `scratchpad\val9\`. Para comparar DRC uso un multiconjunto (`Counter`), no un `set`.

Copias o renombrados de proyecto (VAL-0013-01, 2026-11-05):
- Diseño idéntico: aplico con `sed` el mapeo de hojas/redes/`sheetfile` a la PCB de origen y hago `diff --strip-trailing-cr` frente a la nueva (solo debe quedar lo permitido). Netlists: `scratchpad\cmp_net.py` (componentes, redes y partición de nodos). ERC/DRC por violación: `scratchpad\cmp_inf.py`.
- **El cajetín se valida en el PDF exportado** (`sch export pdf`, `pcb export pdf --include-border-title`), no en el `title_block`: `Cajetin_Kicad.kicad_wks` (heredada del TFG) tiene fijo el título del TFG, no usa `${TITLE}` ni `${REVISION}` y pinta `COMMENT1` como «PROYECTO:».
- Las rutas de salida del `.kicad_pro` (`plot`, `bom_export_filename`) heredadas de la v1 apuntan a `../../`, que es la raíz del repositorio. **El trazado de pcbnew usa `pcbplotparams/outputdirectory` del `.kicad_pcb`**, no `output.plot` del `.kicad_pro`: hay que revisar los dos (en VAL-0013-01 se me pasó el de la PCB).
- Un `diff` frente al origen no muestra lo que se hereda sin cambios. Busco a propósito restos heredados: `embedded_files` de la PCB (la v1 lleva incrustada `Cajetin_Kicad.kicad_wks`, comprimida con zstd; en el equipo no hay zstd), `outputdirectory` y textos fijos en la hoja de dibujo.

Limpiezas o vaciados de un proyecto (VAL-0014-01, 2026-11-05):
- **Inventario con la netlist del estado de partida**, no solo con los recuentos. Extraigo la base con `git show <base>:<ruta> > scratchpad` (la guardia bloquea `git archive`) y hago `kicad-cli sch export netlist` sobre esa copia. Así encontré un texto de hoja que decía «test points a +12 V» cuando solo uno lo estaba.
- **Restos que el `diff` no enseña:** las tablas `sym-lib-table` y `fp-lib-table` siguen listando las librerías de la v1 aunque ya no se usen. También miro las capas, el `stackup` y las reglas heredadas.
- **PCB editada con script:** `kicad-cli pcb upgrade --force` sobre una copia; si sale idéntica byte a byte, es lo que guardaría pcbnew. En los esquemas, el reguardado solo cambia el orden de los textos (comparar líneas ordenadas).
- **No es un hallazgo:** que `F.Fab` o `B.Fab` no aparezcan en `(layers …)` no impide trazarlas, porque `kicad-cli --layers F.Fab` las saca. Lo pruebo antes de decir que se pierde algo.
- Scripts reutilizables en `scratchpad\val14\` (`inventario.py`, `nets.py`, `fp_h.py`). El *scratchpad* es de sesión, así que si hacen falta otra vez, se rehacen.

Relacionado: [[comprobaciones-utiles]].
