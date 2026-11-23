---
name: revision-colocacion
description: Cómo validar colocacion.py, las colocaciones de prueba (b…b4) y los estudios de coste con piezas alternativas (VAL-0037-01): copias, sembrados, auditoría sin tokens, clones de LDO
metadata:
  type: feedback
---

Cada colocación se evalúa con la herramienta y las reglas **de su paso** (`git show <commit>:herramientas/kicad/{colocacion,colocar,_comun}.py` y `…/colocacion-reglas.csv` en una carpeta aparte). Con las de ahora, las antiguas incumplen reglas nuevas, y eso no es un fallo.

**Por qué:** en VAL-0037-01 (2026-11-23), b3 daba 2 obligatorias con las reglas actuales y 0 con las de `36b804c`. Además, b4 solo da 0 con J10 horizontal: en `hardware/v2` daba 13, porque el autor cambió la huella en una copia y no lo entregó.

**Cómo aplicarlo:**
- Para una huella que aún no está en `hardware/v2`, se cambia el campo Footprint en la hoja de la copia (con sed) y se pasa `sincronizar.py <copia>/v2 -o <copia>/v2/esp-riego.kicad_pcb`.
- Sembrados: `scratchpad\v37\sembrar.py` (cambios por referencia sobre b4, un CSV por caso y lectura del `--detalle`). Para F01, el hueco se mide con el patio real (`pcbnew` `GetCourtyard().BBox()`). `extraer` redondea el patio a 0,1 mm: un 0603 sale 1,5 mm y mide 1,45. Con 0,10 exactos F01 no salta, y es correcto (≥).
- Ida y vuelta: compararla con un lector propio del texto de la PCB. La referencia está en coordenadas de la huella, así que hay que girarla con el giro de la huella para pasarla a ejes de placa.
- La auditoría no guarda tokens: solo acciones y marcas de tiempo por `agent_id`. Hay que buscar huecos de más de 10 min, que indican un agente continuado en dos tandas.
- Las alternativas «misma pieza» de JSMSEMI o TECH PUBLIC para TLV1117LV pueden ser un 1117 clásico (caída de 1,2 V y tántalo). Se renderiza el PDF (`pdftoppm`) cuando `pdftotext` sale vacío (fuentes chinas).
- Cuando un estudio cita una tabla de «valores típicos», hay que buscar en el texto del datasheet un «must». En el LMR36520, p. 20, el de 220 nF a la entrada es obligatorio.
- Al recalcular el error de una medida, se comprueban los términos que el documento de diseño ya suma (en ALI-09, la caída de F1 + Q1).

Relacionado: [[revision-herramientas]], [[revision-alimentacion]], [[revision-piezas]].
