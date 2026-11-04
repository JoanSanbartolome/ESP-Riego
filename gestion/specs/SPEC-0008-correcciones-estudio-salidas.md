---
id: SPEC-0008
titulo: Correcciones menores del estudio de salidas
fase: 2
estado: propuesta
responsable: ing-esquematicos
revisor: ing-validacion
rama: spec/SPEC-0008-correcciones-estudio-salidas
requisitos: [REL-03, REL-05]
depende_de: [SPEC-0005]
creada: 2026-11-04
cerrada:
validacion:
---

# SPEC-0008 · Correcciones menores del estudio de salidas

> Propuesta: observaciones B de VAL-0005-01 que solo afectan al texto del estudio. No bloquean SPEC-0007, que toma los datos corregidos directamente del informe. Prioridad baja: se abre cuando haya hueco o antes de cerrar la fase 2.

## Objetivo

`docs/diseno/estudio-salidas.md` queda coherente con las válvulas instaladas de 24 V DC y con D8, sin los datos inexactos que señaló VAL-0005-01.

## Alcance

- Incluye los hallazgos de `gestion/informes/VAL-0005-01.md`:
  - **02:** motivo correcto del descarte del BTS428L2 (V_IN(T+) hasta 3,2 V y protección de corto solo hasta 24 V).
  - **03:** BTT6030-2ERA: 6 A con un canal y 4 A con los dos, k_ILIS 2240 y coste a 5 placas con el tramo de 10 unidades.
  - **04:** rango de k_ILIS (± 25 % a 0,5 A, ± 50 % a 50 mA) en §2.5 y §11.3.
  - **06:** criterio de energía inductiva con la ec. 5.1 y la curva E_AS(I_L), con 2 válvulas por canal.
  - **08:** aviso al principio y en §0 de que la conclusión vigente es §11 (válvulas de 24 V DC, D8); unificar ISP752R/BSP752R; sumar EXP-01 al presupuesto del borde.
  - **09:** enlaces a los datasheets del fabricante en §11.6.
  - **10:** filas de vida útil y de compatibilidad con la expansión para todas las opciones, e I_DSS citada de 4a/4b/4c.
- Excluye: cambiar la recomendación o D8; los requisitos (SPEC-0007); el tipo y stock JLCPCB (jr-conformidad, al pasar las piezas al esquema).

## Entradas

- `docs/diseno/estudio-salidas.md`.
- `gestion/informes/VAL-0005-01.md` (hallazgos 02, 03, 04, 06, 08, 09 y 10, con sus fuentes y líneas).
- Registro de `gestion/specs/SPEC-0005-estudio-salidas.md` (D8).

## Entregables

- `docs/diseno/estudio-salidas.md` corregido y el log `gestion/logs/SPEC-0008/01-ing-esquematicos.md`.

## Criterios de aceptación

- [ ] Cada hallazgo del alcance está corregido o justificado uno a uno en el log.
- [ ] Ninguna sección presenta las válvulas de 24 V AC como las instaladas sin remitir a §11.
- [ ] Las cifras de coste corregidas cuadran con los tramos de LCSC que se citan.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-04 | coordinador | Crea la spec (propuesta) | |
