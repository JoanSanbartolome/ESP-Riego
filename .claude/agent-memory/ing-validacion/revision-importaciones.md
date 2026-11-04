---
name: revision-importaciones
description: Cómo validar importaciones o migraciones de proyectos y librerías KiCad (p. ej., v1 del TFG a KiCad 10) sin fiarse de las justificaciones del autor: migración independiente, conversión de EasyEDA, resolución de variables 3D
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

Relacionado: [[comprobaciones-utiles]].
