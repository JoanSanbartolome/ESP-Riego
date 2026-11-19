---
id: SPEC-0037
titulo: Colocación iterada en texto (experimento M10)
fase: 4
estado: abierta
responsable: ing-diseno
revisor: ing-validacion
rama: spec/SPEC-0037-colocacion-en-texto
requisitos: [FAB-07, REL-09, AMB-02, MCU-02, EXP-03]
depende_de: []
creada: 2026-11-19
cerrada:
validacion:
---

# SPEC-0037 · Colocación iterada en texto (experimento M10)

<!-- Objetivo, restricciones y criterios: sin pasos ni números de línea. Unas 60 líneas. Una spec de bloque o de hito de layout lleva sus pasos en «Alcance». -->

## Objetivo

Con los criterios de DEC-0016, saber qué cuesta menos en tokens para iterar la colocación: KiCad con imágenes o una herramienta en texto que extrae las huellas, puntúa cada colocación y la devuelve a KiCad con `colocar.py`. Es la prueba de herramientas de M10 (DEC-0009) y da un punto de partida de colocación para el *floorplan*.

## Alcance

- Incluye:
  - paso 1 (`ing-diseno`): herramienta en `herramientas/kicad/` con `extraer` (por huella: referencia, cara, giro, patio, pads con su red y bloque, en un formato compacto) y `evaluar` (colocación CSV de `colocar.py` → informe en texto de pocas líneas: solapes de patio, piezas fuera del contorno o en una zona prohibida, reglas de colocación incumplidas, longitud de las conexiones sin rutar, total y por clase de red, y una puntuación);
  - tabla de reglas de colocación sacada de REL-09, FAB-07, MCU-02, AMB-02, EXP-03, `conectores.md` §4–§5, `sensores.md` y `arquitectura.md` §0 (columna «Ubicación / keepout»), con el contorno actual de la PCB;
  - paso 2 (brazo B, instancia nueva de `ing-diseno`): colocar sobre una copia solo con la herramienta en texto, hasta que `evaluar` no dé incumplimientos o hasta 30 iteraciones; una imagen al final con `vista.py placa`;
  - paso 3, opcional (lo decide el usuario al ver el resultado del paso 2; 2026-11-19: «probar con una herramienta en texto»): brazo A, otra instancia nueva, la misma colocación de partida y las mismas reglas, solo con KiCad (MCP o `colocar.py`) y `vista.py`, sin `evaluar` mientras itera, hasta que dé la colocación por buena o gaste el doble de tokens que el brazo B; después se le pasa `evaluar`;
  - paso 3 (`ing-diseno`, instancia nueva; DEC-0016): `colocacion.py` y las reglas con los criterios de DEC-0016, por orden: (1) fabricación de la clase más barata de JLCPCB (PCB de 2 capas y PCBA, con página y fecha de las capacidades), incluida la separación entre piezas y a borde; (2) serigrafía: posición de las referencias, sin solapes con textos, pads, máscara abierta, contorno ni otras piezas, altura y trazo mínimos, referencia junto a su pieza; (3) térmico: espacio para el cobre de las piezas que disipan, fuentes de calor repartidas, lejos del SHT40 y de la antena, con su disipación estimada; (4) tamaño de la placa como variable (contorno y taladros M3 que se mueven con él), con el sobrecoste de JLCPCB por encima de 100 × 100 mm; más las propuestas del paso 2 (desacoplos `cerca`, LED visibles y la clase de red en `--detalle`);
  - paso 4 (brazo B', instancia nueva): repetir el paso 2 con la herramienta del paso 3, iterando también el tamaño, primero dentro de 100 × 100 mm;
  - comparación (coordinador): tokens, iteraciones, minutos y resultado de `evaluar` de cada brazo, con la recomendación para la fase 4.
- Excluye: escribir en `hardware/v2` (los dos brazos trabajan sobre copias), el rutado, la tabla de restricciones por red (`restricciones.csv`, otra spec), cambiar el contorno o la caja (D5) y la aprobación del *floorplan*, que se hace en la spec de colocación con la imagen.

## Entradas

- `gestion/decisiones/DEC-0009-orquestacion-v2.md`, M10.
- `docs/02-especificaciones-v2.md` v0.8: REL-09, FAB-07, MCU-02, AMB-02 y EXP-03.
- `docs/diseno/arquitectura.md` §0 (bloques y tabla de ubicación y *keepout*), `conectores.md` §4 (longitud de bordes) y §5 (EXP-02 y pulsadores), `sensores.md` (restricciones de AMB-02) y `mcu.md` (antena).
- `herramientas/kicad/README.md`: `colocar.py`, `vista.py placa`, `restricciones.py` y `_comun.py`.
- `gestion/ESTADO.md`, «Para el layout (fase 4)».

## Entregables

- Paso 1: `herramientas/kicad/<nombre>.py` y su fila en el README; reglas en `docs/diseno/colocacion-reglas.csv`; casos de prueba como parche en la carpeta temporal (los aplica el coordinador en `herramientas/pruebas/`); parte `01-ing-diseno.md`.
- Paso 2 (y el 3, si se hace): la colocación de cada brazo (`docs/diseno/colocacion-b.csv` y, en su caso, `colocacion-a.csv`), su imagen (ruta en el parte), la salida de `evaluar` y el número de iteraciones; partes `02-` y `03-ing-diseno.md`.
- Paso 3: `colocacion.py`, reglas y README al día, casos de prueba como parche; parte `04-ing-diseno.md`.
- Paso 4: `docs/diseno/colocacion-b2.csv` con su tamaño de placa, imagen y salida de `evaluar`; parte `05-ing-diseno.md`.
- Coordinador: `docs/diseno/experimento-colocacion.md` con la tabla comparativa y la recomendación.

## Criterios de aceptación

- [ ] `extraer` cubre las 197 huellas de la PCB y su salida para toda la placa cabe en ≤ 8 k tokens.
- [ ] `evaluar` detecta, en los casos de prueba, un solape de patio, una pieza fuera del contorno, una pieza en la zona prohibida de la antena, un borne en el borde equivocado y el SHT40 lejos del borde; su informe ocupa ≤ 30 líneas.
- [ ] Cada regla de la tabla cita su origen (requisito o sección de un documento de diseño).
- [ ] La ida y vuelta `colocar.py` exportar → `evaluar` → `colocar.py` aplicar deja en la PCB las posiciones del CSV.
- [ ] Los tokens, iteraciones y minutos del brazo B salen del resultado del agente y de la auditoría; si se hace el brazo A, parte de la misma colocación y las mismas reglas, con una instancia nueva.
- [ ] `evaluar` detecta, en casos sembrados, una separación de JLCPCB incumplida, dos textos de serigrafía solapados, un texto sobre un pad, una referencia lejos de su pieza, dos fuentes de calor demasiado juntas y una placa de más de 100 mm sin aviso de coste; cada regla de JLCPCB cita página y fecha.
- [ ] La colocación del paso 4 cumple todas las reglas obligatorias, con el tamaño de placa y su precio en JLCPCB en el parte; un tamaño por encima de 100 × 100 mm no se adopta sin el OK del usuario (DEC-0016).
- [ ] `hardware/v2` sin cambios; `test_kicad.py` en verde con los casos nuevos.

## Plan de validación

Nivel **completo** (la herramienta decide la colocación de la fase 4; DEC-0005), con `checklists/layout.md` en lo que aplique.

- Reproducir de forma independiente: `evaluar` sobre las colocaciones entregadas y sobre una colocación con cinco fallos sembrados (uno de cada tipo del criterio); el recuento de huellas de `extraer` frente a la PCB; la ida y vuelta con `colocar.py`; los tokens de la tabla comparativa frente al registro y la auditoría.
- Por muestreo: cinco reglas de la tabla frente a su origen; la imagen de cada brazo frente a su informe de `evaluar`.

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-19 | coordinador | Crea la spec (propuesta) | | | | |
| 2026-11-19 | coordinador | Abre la spec |  |  |  |  |
| 2026-11-19 | ing-diseno | colocacion.py (extraer, evaluar) y reglas de colocación | 01-ing-diseno | 296093 | 86 | 26 |
| 2026-11-19 | ing-diseno | brazo B: colocación en texto, 6 iteraciones, 0 incumplimientos | 02-ing-diseno | 173296 | 25 | 18 |
