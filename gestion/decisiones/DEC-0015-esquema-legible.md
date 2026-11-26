---
id: DEC-0015
titulo: Esquema legible con el aspecto del esquema del TFG
fecha: 2026-11-17
estado: aceptada
modificada_por: []
decide: usuario
specs: [SPEC-0035, SPEC-0032]
requisitos: [KIC-02, KIC-06]
---

# DEC-0015 · Esquema legible con el aspecto del esquema del TFG

## Contexto

Las hojas de `hardware/v2` las genera `hoja.py`, que no dibuja cables: cada pin lleva su etiqueta o su símbolo de alimentación, las piezas quedan sueltas y cada bloque se cierra con un bloque de notas largo. La netlist es correcta (ERC 0, paridad 0), pero para seguir un circuito hay que buscar etiquetas por toda la hoja.

El 2026-11-17, el usuario enseña su esquema del TFG (hoja de conectores: sensor de nivel, sensor de humedad y temperatura, agujeros y puntos de prueba) y pide que todas las hojas tengan ese aspecto, porque es legible y fácil de comprobar. Lo exige de forma expresa.

## Opciones consideradas

1. **Salidas, 6 canales iguales:** una subhoja «Canal» que KiCad repite 6 veces (jerarquía con varias instancias), o los 6 canales cableados en la misma hoja.
2. **Títulos de los recuadros:** solo el nombre del bloque (como en el TFG), o el nombre más las referencias y los IDs de requisito (como ahora).
3. **Notas:** solo cifras junto a la pieza, o cifras más una nota breve por bloque.

## Decisión

Decidida por el usuario el 2026-11-17:

- **Salidas:** una subhoja «Canal» repetida 6 veces. La hoja Salidas muestra los 6 bloques y lo común (*pull-down* de OUT_DEN y condensadores a granel). Cada instancia conserva las referencias de hoy (U7–U12, J4–J9…), para no tocar las tablas de campos ni la PCB.
- **Títulos:** nombre del bloque con sus referencias principales y sus IDs de requisito, p. ej. «Buck 5 V: U2 LMR36520 (ALI-05, ALI-06)».
- **Notas:** cifras clave junto a la pieza (como «fc=5.9Hz» o «4mA:0.6V» en el TFG) y, como mucho, 2 o 3 líneas de nota por bloque. El detalle se queda en `docs/diseno/`.

Reglas de estilo, tomadas del esquema del TFG (requisito KIC-06):

1. Cada hoja se divide en recuadros, uno por bloque, con línea de trazo y punto y el título arriba a la izquierda.
2. Dentro de un recuadro, las piezas se unen con cables y puntos de unión. Las etiquetas (globales o jerárquicas, con su forma de entrada o salida) solo se usan para las señales que salen del bloque o de la hoja.
3. Alimentación con símbolos `power` unidos al pin por un cable corto: tensiones hacia arriba y GND hacia abajo.
4. El circuito se lee de izquierda a derecha (entradas a la izquierda, salidas a la derecha), con las tensiones arriba y la masa abajo.
5. Referencia y valor de cada pieza junto a ella, sin solaparse con nada. Ningún cable cruza un símbolo ni un texto, y no hay etiquetas sueltas.
6. Rejilla de 1,27 mm y tamaños de texto por defecto de KiCad.

## Consecuencias

- `docs/02` pasa a la v0.8 con el requisito KIC-06 (esquema legible según estas reglas), y `gestion/checklists/esquema.md` recibe los puntos de estilo: los que se pueden contar, como `[auto]` en `comprobar.py` (cables que cruzan símbolos, etiquetas sueltas, textos que se solapan); el resto, como `[juicio]` sobre la imagen de cada hoja.
- `hoja.py` necesita dibujar cables y subhojas con varias instancias; si no, se hace con otra herramienta de `herramientas/kicad/`. No se dibuja a mano pieza a pieza sin herramienta reutilizable.
- Las conexiones no cambian: la netlist por grupos de pines es idéntica antes y después. Solo cambian los nombres de las redes internas de un canal, por la jerarquía nueva, y la PCB se resincroniza con paridad 0.
- SPEC-0035 hace el trabajo, con una hoja piloto que el usuario aprueba sobre una imagen antes de seguir con las demás. SPEC-0032 (integración) va después y deja la raíz con el mismo estilo.
