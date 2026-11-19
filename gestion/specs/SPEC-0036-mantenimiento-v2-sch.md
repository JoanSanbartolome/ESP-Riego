---
id: SPEC-0036
titulo: Mantenimiento del esquema v2.0-sch
fase: 4
estado: propuesta
responsable: ing-diseno
revisor: ing-validacion
rama: spec/SPEC-0036-mantenimiento-v2-sch
requisitos: [FAB-05, KIC-06, ALI-13]
depende_de: []
creada: 2026-11-19
cerrada:
validacion:
---

# SPEC-0036 · Mantenimiento del esquema v2.0-sch

<!-- Objetivo, restricciones y criterios: sin pasos ni números de línea. Unas 60 líneas. Una spec de bloque o de hito de layout lleva sus pasos en «Alcance». -->

## Objetivo

Las observaciones de VAL-0032-01 quedan cerradas antes del pedido de fabricación.

## Alcance

- Incluye (una línea por observación):
  - VAL-0032-01-01 (M, `jr-conformidad` + usuario): U1 TPS26632RGER con 93 de stock y la alternativa TPS26633RGER con 1. Otra variante en RGE-24 con stock o reserva en JLCPCB (consulta de coste al usuario); stock y fecha en `alimentacion.md` §7; marcar de nuevo la casilla del plan cuando U1 tenga alternativa. Antes del pedido.
  - VAL-0032-01-02 (B, `ing-diseno`): cifra de BUS_24V en la raíz: «24 V tras U1, ≤ 4,57 A (ALI-13)».
  - VAL-0032-01-03 (B, `ing-diseno`): `hoja.py extraer` lee el `justify` de los textos; prueba de ida y vuelta de la raíz que compare el archivo sin UUID (la aplica el coordinador en `herramientas/pruebas/`).
- Excluye: el layout.

## Entradas

<Archivos y secciones concretas que el responsable debe leer. La spec es la orden completa: un agente sin más contexto tiene que poder ejecutarla.>

-

## Entregables

-

## Criterios de aceptación

- [ ]

## Plan de validación

<Nivel (ligero o completo). Qué reproduce validación de forma independiente (lo que tiene riesgo: cotas, mapeo de pines, cálculos con poco margen) y qué comprueba por muestreo (lo mecánico: stock, campos, enlaces).>

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-19 | coordinador | Crea la spec (propuesta) | | | | |
