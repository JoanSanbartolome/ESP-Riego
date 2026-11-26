---
name: copias-y-comparaciones
description: Trampas al comparar netlists, PCB, colocaciones y migraciones sobre copias, y límites de herramientas/kicad que no dice su README
metadata:
  type: reference
---

- Cada colocación de prueba se evalúa con `colocacion.py`, `colocar.py`, `_comun.py` y `colocacion-reglas.csv` de su commit (`git show <commit>:…` en una carpeta aparte). Por qué: con las reglas nuevas, las antiguas incumplen reglas que no existían. Fuente: VAL-0037-01; `herramientas/pruebas/test_kicad.py` (`de_commit`).
- `colocacion.py extraer` redondea el patio a 0,1 mm (un 0603 sale 1,5 y mide 1,45): un hueco al límite se mide con `GetCourtyard().BBox()` de `pcbnew`, y una regla `≥` con el valor exacto no salta (F01). Por qué: si no, se da por fallo lo que cumple. Fuente: VAL-0037-01; `colocacion.py` l. 570.
- En el `.kicad_pcb`, pads y textos de una huella van en sus coordenadas locales y el ángulo del pad es absoluto: a ejes de placa se gira con el giro de la huella, y frente a la librería se le resta. Por qué: la tabla de `colocar.py` está en ejes de la placa. Fuente: VAL-0009-01, VAL-0037-01.
- `hoja.py netlist` (`_comun.comparar_netlists`) compara piezas, huella, valor y nodos, no las propiedades (`dnp`, `exclude_from_*`): para eso, la netlist kicadxml. Por qué: un DNP cambiado pasa. Fuente: VAL-0027-01; `_comun.py` l. 444.
- En la netlist kicadxml de KiCad 10, `pinfunction` lleva sufijo (`K_1`, `OUT_10-12_10`: se compara el prefijo antes de `_`) y `dnp` y `exclude_from_bom` van como `<property name>` sin `value`. Por qué: si no, todos los pines salen distintos. Fuente: VAL-0025-01.
- «Sin conectar» esperados tras una hoja: Σ(islas de pads − 1) de las redes nuevas + pads nuevos en las redes compartidas; frente al DRC se comparan los deltas base → ahora, porque el desfase es constante. Por qué: dio el +180 exacto. Fuente: VAL-0025-01, VAL-0031-01.
- «Piezas sin colocar» en la paridad son huellas sincronizadas sin posición, no ausentes. Por qué: no es un fallo de paridad. Fuente: VAL-0019-01; `sincronizar.py`.
- Los cientos de `(thickness 0.15)` añadidos a los campos ocultos son normalización de `pcbnew`; el diff de un `.kicad_pcb` se mira con `git diff --patience --numstat`. Por qué: no son un cambio de diseño. Fuente: VAL-0022-01, VAL-0029-01.
- PCB editada por script: `kicad-cli pcb upgrade --force` sobre una copia; si sale idéntica byte a byte, es lo que guardaría `pcbnew`. Un esquema reguardado solo cambia el orden de los textos (se comparan líneas ordenadas). Por qué: separa formato de cambio real. Fuente: VAL-0014-01.
- Los `.kicad_mod` propios y `docs/` están en CRLF: las mutaciones por texto llevan `\r\n` y se hacen con Python en binario (`sed -i` reescribe el archivo); en una hoja, la primera aparición de un texto suele estar en `lib_symbols`, así que se ancla a la instancia (`Reference "R16"`). Por qué: si no, la mutación no cae donde se quiere. Fuente: VAL-0027-01, VAL-0035-02.
- Para probar `restricciones.py` con el formato real, se añaden `PCB_TRACK`, `PCB_ARC` y `PCB_VIA` con `pcbnew` a una copia; en KiCad 10 las pistas llevan `(net "nombre")`. Por qué: un texto escrito a mano no tiene el formato de KiCad. Fuente: VAL-0027-01.
- `comprobar.py` sobre una copia fuera del repositorio da N/A en `librerias.gitattributes` y, sin `componentes/`, en `librerias.fichas`: se pasa también sobre `hardware/v2`, que solo lee. Por qué: N/A no es OK. Fuente: VAL-0027-01; `comprobar.py` l. 521 y 576.
- Falsos positivos de una heurística nueva: se pasa sobre una muestra de la librería oficial de KiCad (`huella.analizar`: 0 de 867). Por qué: la batería solo trae casos del proyecto. Fuente: VAL-0027-02.
- En las mutaciones sobreviven los casos con datos fijos que ya cumplen la regla (lista ya ordenada, «ya existe» sin el archivo), y «la mutación X falla» del parte suele invertir la regla, no quitarla: se rehace. Por qué: la prueba puede no detectar el defecto. Fuente: VAL-0028-01.
- `hoja.py extraer` no lee el `justify` de los textos (la ida y vuelta de la raíz cambió 3) y avisa de los cables que no representa (`P:<red>` en el pin los evita). Por qué: `extraer` + `generar` no reproduce esos textos. Fuente: VAL-0031-01, VAL-0032-01; `hoja.py` l. 241.
- `hoja.py paginas` ordena las hermanas por su página actual: intercambiar dos hermanas no falla. Por qué: una prueba de orden con hermanas no detecta nada. Fuente: VAL-0035-02.
- `seccion_huellas` de `esquema.pcb_main` se prueba leyendo la spec y los partes a mano, porque `textos_de_la_spec` pide un `Proyecto`. Por qué: no tiene orden propia. Fuente: VAL-0035-02; `comprobar.py` l. 207.
- PDF entregado frente al propio: por página, los tokens ordenados de `get_text()` de PyMuPDF. BOM: se expanden los rangos de `Refs` y se cruzan Value, LCSC y MPN con la netlist; el precio, con `jlc.py --cantidad <Cantidad × 5>`. Por qué: son las comprobaciones más rápidas de esos entregables. Fuente: VAL-0032-01.
- `kicad-cli fp upgrade -o <dir>` exige que `<dir>` no exista (código 4); `sym upgrade -o <archivo>`, no. Por qué: el error no lo dice. Fuente: VAL-0009-01.
- DRC frente a DRC: multiconjunto (`Counter`) de violaciones, no un `set`. Por qué: un `set` esconde las repetidas. Fuente: VAL-0009-01.
- Que `F.Fab` o `B.Fab` no estén en `(layers …)` no impide trazarlas (`kicad-cli --layers F.Fab`). Por qué: no es un hallazgo. Fuente: VAL-0014-01.
- `verificar.py <copia> --salida <carpeta nueva>` en cada verificación propia. Por qué: no se mezclan informes de ejecuciones distintas. Fuente: VAL-0001-02.
