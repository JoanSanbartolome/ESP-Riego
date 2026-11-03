---
id: SPEC-0000
titulo: Análisis de la v1, especificaciones y plan de la v2
fase: 0
estado: cerrada
responsable: coordinador
revisor: usuario
rama: main
requisitos: []
depende_de: []
creada: 2026-11-03
cerrada: 2026-11-03
validacion: n/a
---

# SPEC-0000 · Análisis de la v1, especificaciones y plan de la v2

> Registro retroactivo: este trabajo se hizo antes de existir el sistema de orquestación. Se integró directamente en `main` con el commit `abd45a7` y sin informe de validación.

## Objetivo

Dejar documentado el punto de partida del rediseño: estado de la PCB del TFG, requisitos de la v2 y plan por fases.

## Entregables

- `docs/01-analisis-v1.md`: análisis de la v1 (ERC, DRC, paridad y hallazgos H1–H12).
- `docs/02-especificaciones-v2.md`: requisitos de la v2 (ALI, MCU, REL, NIV, AMB, EXP, FAB, KIC, FW), criterios de aceptación y decisiones abiertas D1–D7.
- `docs/03-plan-de-diseno.md`: fases 0–6 e hitos.
- `README.md`, `.gitignore` y `.gitattributes`.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-03 | coordinador | Análisis de la v1 sobre una copia del proyecto del TFG | `docs/01-analisis-v1.md` |
| 2026-11-03 | usuario | Decisiones de partida: ESP32-S3 soldado, 9–30 V, solo baja tensión, SMT en JLCPCB, KiCad 10 | `docs/02-especificaciones-v2.md` |
| 2026-11-03 | coordinador | Primer commit del repositorio | `abd45a7` |
