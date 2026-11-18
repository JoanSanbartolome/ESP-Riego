---
id: SPEC-0035
titulo: Esquema legible
fase: 3
estado: abierta
responsable: ing-diseno
revisor: ing-validacion
rama: spec/SPEC-0035-esquema-legible
requisitos: [KIC-02, KIC-03, KIC-06]
depende_de: [SPEC-0034]
creada: 2026-11-17
cerrada:
validacion:
---

# SPEC-0035 · Esquema legible

<!-- Objetivo, restricciones y criterios: sin pasos ni números de línea. Unas 60 líneas. Una spec de bloque o de hito de layout lleva sus pasos en «Alcance». -->

## Objetivo

Las cinco hojas de `hardware/v2` tienen el aspecto del esquema del TFG (DEC-0015): recuadros por bloque, piezas unidas con cables, etiquetas solo entre bloques y hojas, y cifras clave junto a la pieza. Las conexiones no cambian.

## Alcance

- Incluye:
  0. **Coordinador.** `docs/02` v0.8 con KIC-06 (esquema legible según las reglas de DEC-0015) y los puntos de estilo en `gestion/checklists/esquema.md`.
  1. **`ing-diseno`, herramientas.** `hoja.py` (u otra herramienta de `herramientas/kicad/`) dibuja cables, puntos de unión, recuadros con título y subhojas con varias instancias, con sus pruebas en `test_kicad.py`. `comprobar.py` añade como `[auto]` lo que se puede contar: cables que cruzan símbolos o textos, etiquetas sueltas, textos que se solapan y piezas fuera de un recuadro; y que el diff de la PCB frente a `main` solo toque las huellas de las referencias que la spec cambia, o que el parte liste las demás (propuesta de VAL-0034-01).
  2. **`ing-diseno`, hoja piloto: Sensores.** Se entrega con su imagen y **el usuario aprueba el estilo** antes del paso 3.
  3. **`ing-diseno`, resto de hojas:** Conectores, MCU, Alimentación y Salidas. Salidas, con la subhoja «Canal» repetida 6 veces y las referencias de hoy en cada instancia; lo común (R44, C45, C46), en la hoja Salidas. Cada hoja, con su imagen.
  4. **`ing-diseno`, PCB resincronizada** con paridad 0, sin mover huellas colocadas.
- Excluye: cambiar piezas, valores, campos o conexiones; la raíz (la deja con el mismo estilo SPEC-0032); el layout.

## Entradas

- `gestion/decisiones/DEC-0015-esquema-legible.md` entera, con sus reglas de estilo.
- Imagen de referencia del usuario: el esquema del TFG, hoja de conectores. Se ve con `vista.py hoja` sobre una **copia** de `C:\Users\josan\proyectos\TFG` fuera de esa carpeta (solo lectura).
- `herramientas/kicad/README.md` (`hoja.py`, `vista.py`, `comprobar.py`) y sus límites.
- `docs/diseno/<bloque>.md`: resumen de cada bloque, para las cifras que van junto a cada pieza.
- `gestion/checklists/esquema.md` v13, sección «Estilo» (los `[auto: pendiente]` son los que el paso 1 lleva a `comprobar.py`).
- `docs/02-especificaciones-v2.md` v0.8, KIC-06.

## Entregables

- `herramientas/kicad/` ampliado, con sus pruebas.
- `hardware/v2/*.kicad_sch` (cinco hojas y la subhoja `canal.kicad_sch`) y `esp-riego.kicad_pcb` resincronizado.
- Imagen de cada hoja (en el parte, como ruta) y partes `NN-ing-diseno.md`.

## Criterios de aceptación

- [ ] Netlist idéntica por grupos de pines antes y después (`hoja.py netlist`). Solo cambian los nombres de las redes internas de Salidas, por la jerarquía.
- [ ] `verificar.py hardware/v2`: ERC 0, paridad 0 y ningún `[auto]` en FALLA, incluidos los de estilo; `campos.py revisar` sin diferencias.
- [ ] Cada hoja cumple las reglas 1–6 de DEC-0015 a la vista de su imagen: recuadros con título (nombre, referencias e IDs), cables dentro del bloque, etiquetas solo hacia fuera, cifras junto a la pieza y como mucho 2 o 3 líneas de nota por bloque.
- [ ] Salidas: una subhoja «Canal» con 6 instancias que conservan las referencias U7–U12, J4–J9 y el resto de hoy.
- [ ] El usuario aprobó la hoja piloto antes del paso 3 (anotado en el registro).
- [ ] `test_kicad.py` en verde con las pruebas nuevas.

## Plan de validación

Nivel **completo** (esquema; DEC-0005), con `esquema.md` v13.

- Reproducir de forma independiente: la comparación de netlists por grupos de pines frente a `main`; `verificar.py hardware/v2`; las referencias de cada instancia de «Canal» frente a `campos-salidas.csv` y a la PCB.
- Por muestreo: tres bloques de hojas distintas, mirando la imagen contra las reglas de DEC-0015, y las cifras junto a la pieza contra `docs/diseno/`.

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-17 | coordinador | Crea la spec (propuesta) | | | | |
| 2026-11-17 | coordinador | Abre la spec |  |  |  |  |
| 2026-11-17 | coordinador | Abre la spec y hace el paso 0 (docs/02 v0.8, esquema.md v13) |  |  |  |  |
| 2026-11-17 | ing-diseno | Pasos 1–2: herramientas de estilo y hoja piloto Sensores | 01-ing-diseno | 351199 | 135 | 58 |
| 2026-11-17 | usuario | Aprueba el estilo de la hoja piloto Sensores (imagen de `vista.py hoja`) |  |  |  |  |
| 2026-11-18 | ing-diseno | Paso 3a: Conectores, MCU y Alimentación (con un corte por el límite de uso) | 02-ing-diseno | 355860 | 57 | 29 |
| 2026-11-18 | ing-diseno | Pasos 3b–4: Salidas con «Canal» ×6, dibujo.py, LED con GND por cable, PCB resincronizada | 03-ing-diseno | 338804 | 119 | 27 |
| 2026-11-18 | ing-validacion | VAL-0035-01 APROBADO_CON_OBSERVACIONES (2 M, 4 B) | VAL-0035-01 | 209216 | 71 | 11 |
