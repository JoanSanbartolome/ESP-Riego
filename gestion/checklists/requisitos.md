# Checklist de revisión de requisitos

**Versión:** v4 (2026-11-11). Para las specs que cambian `docs/02-especificaciones-v2.md`. Cada informe cita la versión usada. Cualquier cambio sube la versión y se anota en el historial.

`[auto: X]`: lo comprueba X y nadie lo repasa a mano. `[auto: pendiente]`: lo comprobará un script de `herramientas/kicad/` (SPEC-0027); hasta entonces se repasa. `[juicio]`: lo repasan el autor, antes de entregar, y validación.

## Identificadores y trazabilidad

- [ ] [auto: gestion.py trazabilidad] `gestion.py trazabilidad` sin avisos.
- [ ] [auto: pendiente] Todos los IDs citados en docs/02, docs/03, las checklists, las specs abiertas o propuestas y las definiciones de los agentes existen como vigentes o retirados.
- [ ] [juicio] Tabla de retirados con el motivo y la DEC; ningún ID retirado se reutiliza.
- [ ] [juicio] Cambios de prioridad y de sentido anotados en el historial o en la DEC.
- [ ] [juicio] Las cifras de la DEC coinciden con las de docs/02.
- [ ] [juicio] El campo `requisitos` de la spec incluye todos los IDs cuyo texto o prioridad cambia (comparación de tablas).

## Decisiones

- [ ] [juicio] Cada decisión del usuario de la DEC llega a un requisito vigente.
- [ ] [juicio] Cada interpretación del autor figura como tal en la DEC.
- [ ] [juicio] Las decisiones abiertas (§7) son coherentes con los requisitos.

## Coherencia técnica

- [ ] [juicio] Cadena de tensiones: rango de entrada (con tolerancias de la fuente) → VRWM de la TVS → Vc → tensión nominal del buck, de los condensadores y de las piezas del nodo; UVLO referido a la tensión tras las protecciones de entrada.
- [ ] [juicio] Presupuesto de potencia de la fuente frente a las cargas simultáneas.
- [ ] [juicio] Cada criterio de §6 se puede verificar con la arquitectura descrita (p. ej., no pedir a la placa que informe de la pérdida de su única fuente).
- [ ] [juicio] Las protecciones de entrada tienen un orden coherente con los criterios de §6 (polaridad invertida frente a TVS unidireccional).
- [ ] [juicio] Cada límite global (corriente total, número de salidas) tiene un mecanismo (hardware, firmware o instalación) y una prueba en §6.
- [ ] [juicio] Las pruebas de §6 con umbrales fijan el punto de prueba dentro de la ventana en la que la placa funciona (entre el UVLO y la VRWM).
- [ ] [juicio] Si la protección de un elemento depende de que actúe antes otro (fuente, limitador), el requisito dice qué ven los demás canales y la lógica durante el evento.
- [ ] [juicio] Cada umbral con tolerancia se define como una banda, y la prueba de §6 se hace fuera de ella (por encima y por debajo).
- [ ] [juicio] En las protecciones escalonadas, lo que protege cada escalón (pista, borne, pieza) aguanta hasta que actúa el siguiente.
- [ ] [juicio] Los parámetros de los equipos externos (protección y OVP de la fuente…) se fijan como requisito o como dato de entrada supuesto en una DEC.
- [ ] [juicio] Las protecciones dadas en % de potencia se pasan a corriente en todo el rango de ajuste o de tensión permitido.
- [ ] [juicio] El total de carga se calcula a la tensión máxima permitida y con las bobinas frías (temperatura mínima de §5).
- [ ] [juicio] Cada corriente de diseño tomada de un estudio cita la condición en que está dada (temperatura y tensión), para no corregirla dos veces.
- [ ] [juicio] Los umbrales de UVLO se acotan en los dos sentidos (arranque y bajada) según las pruebas de §6 que se hacen con la placa en marcha.
- [ ] [juicio] Cada límite nuevo de consumo tiene reparto, prueba en §6 y llega a las specs que lo consumen.
- [ ] [juicio] El margen de cada prueba de §6 respecto a su umbral supera la precisión fijada para la medida.

## Términos obsoletos

- [ ] [juicio] Búsqueda de los términos retirados en docs/, gestion/checklists/, las specs abiertas o propuestas, `CLAUDE.md`, `.claude/agents/` y `.claude/agent-memory/`, y en las recomendaciones de los estudios que sustituye una DEC.
- [ ] [juicio] Cuando una aclaración del usuario cambia un dato de entrada (carga, fuente…), se buscan sus apariciones en las specs abiertas y en los entregables en curso de otras ramas.

## Estudios de diseño (`docs/diseno/` sin KiCad)

- [ ] [juicio] El coste usa el tramo de precio de la cantidad real que se compra (piezas por placa × placas), no un tramo superior.
- [ ] [juicio] Cada descarte cita el parámetro del datasheet que lo descarta, y cada «cumple» se comprueba contra todos los criterios de la tabla.
- [ ] [juicio] Cuando cambia un dato de entrada, el resumen y la recomendación anteriores llevan un aviso que remite a la sección vigente.

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| v1 | 2026-11-04 | Versión inicial, a partir de las propuestas de VAL-0004-01 |
| v2 | 2026-11-04 | Propuestas de VAL-0004-02 y VAL-0005-01: orden de protecciones, mecanismo de los límites globales, puntos de prueba, dependencia entre protecciones y sección de estudios de diseño |
| v3 | 2026-11-05 | Propuestas de VAL-0007-01 y VAL-0011-01: umbrales como bandas, protecciones escalonadas, parámetros de equipos externos, cifras de la DEC frente a docs/02, búsqueda en las memorias y estudios sustituidos, protecciones en % de potencia, carga a tensión máxima y en frío, límites de consumo con reparto y prueba, margen de las pruebas, condición de las corrientes de diseño y UVLO en los dos sentidos. Se ajustó antes del merge de SPEC-0011 (VAL-0011-01 y VAL-0011-02) |
| v4 | 2026-11-11 | DEC-0009: cada punto marcado `[auto]` o `[juicio]` |
