# Checklist de revisión de requisitos

**Versión:** v1 (2026-11-04). Para las specs que cambian `docs/02-especificaciones-v2.md`. Cada informe cita la versión usada. Cualquier cambio sube la versión y se anota en el historial.

## Identificadores y trazabilidad

- [ ] `gestion.py trazabilidad` sin avisos.
- [ ] Todos los IDs citados en docs/02, docs/03, las checklists, las specs abiertas o propuestas y las definiciones de los agentes existen como vigentes o retirados.
- [ ] Tabla de retirados con el motivo y la DEC; ningún ID retirado se reutiliza.
- [ ] Cambios de prioridad y de sentido anotados en el historial o en la DEC.
- [ ] El campo `requisitos` de la spec incluye todos los IDs cuyo texto o prioridad cambia (comparación de tablas).

## Decisiones

- [ ] Cada decisión del usuario de la DEC llega a un requisito vigente.
- [ ] Cada interpretación del autor figura como tal en la DEC.
- [ ] Las decisiones abiertas (§7) son coherentes con los requisitos.

## Coherencia técnica

- [ ] Cadena de tensiones: rango de entrada (con tolerancias de la fuente) → VRWM de la TVS → Vc → tensión nominal del buck, de los condensadores y de las piezas del nodo; UVLO referido a la tensión tras las protecciones de entrada.
- [ ] Presupuesto de potencia de la fuente frente a las cargas simultáneas.
- [ ] Cada criterio de §6 se puede verificar con la arquitectura descrita (p. ej., no pedir a la placa que informe de la pérdida de su única fuente).

## Términos obsoletos

- [ ] Búsqueda de los términos retirados en docs/, gestion/checklists/, las specs abiertas o propuestas, `CLAUDE.md` y `.claude/agents/`.

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| v1 | 2026-11-04 | Versión inicial, a partir de las propuestas de VAL-0004-01 |
