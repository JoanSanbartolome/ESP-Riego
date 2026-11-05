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
- Incluye también VAL-0007-01-03 (y las partes de texto de VAL-0005-01-01, 05 y 07):
  - §11.4 y §11.5 recomiendan aún 470 µF y ≈ 60 ms de autonomía, vigilar los 4 A con la suma de IS y un corte general con BTT6030; §0.2 y §6 dicen «se protege solo»; §8 pone `+24V_SAL` en la clase `Salidas`.
  - Cada una lleva un aviso que remite a DEC-0003 (limitador común ALI-13, REL-08 y REL-10), y el aviso de cabecera remite a §11 **y** a DEC-0003, no solo a §11.
- Incluye también VAL-0011-01-08: el estudio cita aún un total de 4 A (N2, §1.3) y pistas OUT_n de 1,0 mm (§8). Se remite a DEC-0004: carga instalada máxima de 3,5 A, banda del limitador de 3,5–4,9 A y pistas de salida de ≈ 1,2 mm.
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
- [ ] Ninguna recomendación que DEC-0003 sustituye (*hold-up*, suma de IS para los 4 A, corte con BTT6030) queda sin aviso.
- [ ] Las cifras de coste corregidas cuadran con los tramos de LCSC que se citan.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-04 | coordinador | Crea la spec (propuesta) | |
| 2026-11-05 | coordinador | Añade VAL-0007-01-03 | VAL-0007-01 |
| 2026-11-05 | coordinador | Añade VAL-0011-01-08 | VAL-0011-01 |
