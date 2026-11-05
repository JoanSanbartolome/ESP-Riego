---
id: DEC-0005
titulo: Ahorro de tokens en el ciclo de las specs
fecha: 2026-11-05
estado: aceptada
decide: usuario
specs: []
requisitos: []
---

# DEC-0005 · Ahorro de tokens en el ciclo de las specs

## Contexto

El 2026-11-05 la sesión llegó al límite de uso de 5 horas. Lo que más consume:

- **Validaciones:** de 120 000 a 280 000 tokens cada una, unas doce en dos días.
- **Agentes de diseño:** de 65 000 a 260 000 tokens por entrega.
- **Rechazos:** cada uno cuesta una corrección y otra validación completa. Dos de ellos los causó una spec mal redactada por el coordinador (SPEC-0011 y SPEC-0013).

El usuario elige cuatro medidas de las siete propuestas.

## Lo que decide el usuario

| # | Medida |
|---|---|
| 1 | **Validación por niveles según el riesgo.** |
| 2 | **Menos rechazos:** el coordinador revisa la spec antes de encargarla y el autor pasa la checklist antes de entregar. |
| 3 | **Agrupar las correcciones pequeñas** en una spec de mantenimiento por fase, y ediciones mínimas de la zona del coordinador sin agente. |
| 6 | **Menos ruido en las herramientas:** `git config core.safecrlf false` (solo local) y salidas filtradas. |

Se descartan por ahora la 4 (bajar el modelo o el esfuerzo de los agentes, que exige reiniciar la sesión) y la 5 (lecturas más acotadas); la 7 (compactar o abrir una sesión nueva) la gestiona el usuario. El coordinador avisa cuando es buen momento: después de cada merge.

## Interpretación del coordinador

- **Niveles de validación.** La orden a `ing-validacion` dice `nivel: ligero` o `nivel: completo`.
  - **Ligero:** para specs de solo texto o documentación (requisitos, estudios, notas, checklists) y correcciones de una validación anterior. Se lanza con `model: sonnet`. Comprueba los criterios de aceptación y los puntos de checklist que cite la orden. Lo que el autor demuestra con evidencia reproducible se comprueba por muestreo, sin rehacerlo entero.
  - **Completo:** para piezas nuevas (símbolo, huella, 3D), esquema, layout y fabricación, con Opus, como hasta ahora.
  - Ante la duda, completo. Una revalidación tras un `RECHAZADO` se limita a los hallazgos y a lo que tocó la corrección.
- **Antes de encargar** (coordinador): repasa la spec con la checklist que aplique y busca contradicciones internas, sobre todo entre «Incluye», «Excluye» y los criterios, y cifras derivadas sin su condición de partida.
- **Antes de entregar** (autor): el autor repasa la checklist de su trabajo y anota en su log, punto por punto, qué cumple, qué no aplica y qué queda pendiente. Validación parte de ese repaso.
- **Observaciones de una validación:**
  - las M que afectan a la spec siguiente se corrigen antes del merge, con revalidación ligera;
  - las B y las M que no bloquean se acumulan en una spec de mantenimiento por fase (`SPEC-NNNN · Mantenimiento de la fase N`), que se abre al cerrar la fase o cuando acumula bastante trabajo.
- **Sin agente:** las ediciones del coordinador en su zona (checklists, decisiones, specs, diario, plantillas, manual) se hacen directamente y se registran en el diario y en el commit, sin validación propia. Si una de ellas cambia requisitos (`docs/02`), pasa por una spec con validación ligera.

## Consecuencias

- `gestion/README.md` y `CLAUDE.md` recogen los niveles, la revisión previa y la spec de mantenimiento.
- Las definiciones de los agentes autores añaden el repaso de la checklist al terminar, y `ing-validacion` añade los niveles. Estos cambios se cargan al reiniciar la sesión; mientras tanto, el coordinador los incluye en cada orden.
- Las specs propuestas SPEC-0008 y SPEC-0012 se pueden agrupar en la primera spec de mantenimiento.
