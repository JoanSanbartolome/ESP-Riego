---
id: DEC-0010
titulo: Agentes en Opus o inferior, nunca en Fable 5.2
fecha: 2026-11-12
estado: aceptada
decide: usuario
specs: [SPEC-0027]
requisitos: []
---

# DEC-0010 · Agentes en Opus o inferior, nunca en Fable 5.2

## Contexto

DEC-0009 (M8) dejó `ing-diseno` y la validación completa con el modelo de la sesión (`model: inherit`). La sesión principal corre en Fable 5.2, así que los dos agentes lo heredaban. En SPEC-0027 la primera instancia de `ing-diseno` se cortó a los 21 minutos por el límite de uso de 5 horas. Al reanudar, el usuario pidió no lanzar ningún agente con Fable 5.2 y usar Opus o inferior; al cerrar la spec confirmó que es permanente. El motivo no lo dijo: el coordinador entiende que es el consumo.

Datos de SPEC-0027, la única spec con los dos modelos: implementación en Fable 5.2, 395 172 tokens y 100 acciones; validación completa, correcciones y revalidación en Opus, 269 466, 234 711 y 61 078 tokens. No son comparables entre sí (trabajos distintos), y la cifra es el tamaño del contexto al acabar, no el consumo.

## Opciones consideradas

1. Seguir con `model: inherit` y que el coordinador ponga `model: opus` en cada encargo. Depende de que no se olvide, y una instancia continuada conserva el modelo con el que arrancó.
2. **Fijar `model: opus` en las definiciones de `ing-diseno` e `ing-validacion`.** No depende del coordinador ni del modelo de la sesión.

## Decisión

**Opción 2, decidida por el usuario el 2026-11-12.** `ing-diseno` e `ing-validacion` llevan `model: opus`; `jr-conformidad` sigue en Sonnet y la validación ligera se sigue lanzando con `model: sonnet`. Ningún agente, tampoco los genéricos (`Explore`, `general-purpose`), se lanza con Fable 5.2.

## Consecuencias

- Sustituye la medida M8 de DEC-0009. El resto de DEC-0009 sigue igual.
- Cambian las definiciones de los dos agentes, la tabla de roles y el paso 6 de `gestion/README.md`, y `CLAUDE.md`.
- No se continúa con `SendMessage` una instancia que arrancó en Fable 5.2: se arranca otra.
- El cambio no toca herramientas, `disallowedTools` ni *matchers*, que es lo que obliga a la prueba en vivo de la checklist de proceso. El primer encargo de SPEC-0025 sirve de comprobación: si el agente no arranca en Opus, se ve en su resultado.
- La calidad del diseño con Opus frente a Fable 5.2 no está medida. Si SPEC-0025 muestra más correcciones por validación que SPEC-0022, se revisa esta decisión.
