---
id: SPEC-0034
titulo: Límites de uso de las salidas
fase: 3
estado: propuesta
responsable: ing-diseno
revisor: ing-validacion
rama: spec/SPEC-0034-limites-salidas
requisitos: [REL-03, REL-05, REL-10, REL-11, ALI-12]
depende_de: [SPEC-0033]
creada: 2026-11-17
cerrada:
validacion:
---

# SPEC-0034 · Límites de uso de las salidas

<!-- Objetivo, restricciones y criterios: sin pasos ni números de línea. Unas 60 líneas. Una spec de bloque o de hito de layout lleva sus pasos en «Alcance». -->

## Objetivo

El bloque de salidas queda dimensionado sin una válvula de referencia (DEC-0014): rueda libre montada, una carga por salida, y una tabla de límites de uso (REL-11) calculada a partir del circuito y de las reglas vigentes, lista para el manual y para la serigrafía.

## Alcance

- Incluye:
  1. **`ing-diseno`.** `docs/diseno/salidas.md` revisado:
     - §5: la rueda libre D12–D17 pasa a montada; energía en el BTT ≈ 0, con la corriente de pico del diodo, la tensión inversa, la fuga en caliente frente al presupuesto de R_OL y el tiempo de cierre en función de L/R;
     - §0, §1, §3, §4 y §6, sin datos de una válvula concreta. El cálculo se hace con la carga como parámetro: de la resistencia mínima que da 1 A a 30 V hasta la carga mínima que aún detecta el diagnóstico;
     - tabla nueva de **límites de uso** (REL-11) en §0, del estilo de un manual. Para cada límite: valor, de qué sale (requisito, cálculo o datasheet con página) y qué pasa si se supera. Como mínimo: tensión (= la de entrada, solo DC), tipo de carga (bobina DC; una AC alimentada en DC solo si su corriente en DC está dentro del límite), una carga por salida, corriente continua por salida, suma de las salidas activas a la vez, resistencia mínima de la carga, corriente mínima para detectar carga abierta con la salida encendida, resistencia máxima para detectarla en reposo, fuga en reposo, sección y longitud del cable;
     - texto de serigrafía de los límites esenciales (para el layout) y cambios en las notas de firmware de §12 (aviso por la suma de 3,5 A y por la carga mínima).
  2. **`ing-diseno`.** Esquema: D12–D17 sin DNP (`dnp no`, en la BOM y el CPL), con `verificar.py` limpio y paridad 0.
  3. **`ing-diseno`.** `estudio-salidas.md` con un aviso en la cabecera (histórico, sustituido por DEC-0014), y lo que liste SPEC-0033 fuera de `docs/02`.
  4. **`jr-conformidad`.** Tipo, stock y precio de M7 (C95872) con fecha; `campos-salidas.csv` (columna DNP de D12–D17) y su copia al esquema; coste por placa en el parte.
- Excluye: cambiar el *high-side*, el limitador común, la fuente o la corriente de 1 A; el layout (la serigrafía se coloca en la fase 4); el firmware.

## Entradas

- `gestion/decisiones/DEC-0014-salidas-con-limites-nominales.md` entera.
- `docs/02-especificaciones-v2.md` v0.7: REL-03, REL-05, REL-08, REL-10, REL-11, ALI-01, ALI-12 y ALI-13.
- `docs/diseno/salidas.md` entero y `docs/diseno/alimentacion.md` §3.13 (limitador U1).
- `hardware/componentes/M7.md`, `BTT6050-1ERA.md` y sus datasheets.
- `hardware/componentes/campos-salidas.csv`.
- `gestion/checklists/esquema.md` (v11) y `librerias.md` (v7).
- «Pendientes de SPEC-0033», más abajo.

## Pendientes de SPEC-0033 (fuera de `docs/02`)

- `docs/diseno/salidas.md`: §0, §1, §3, §4, §5, §6, §9, §12, §13 y §14 (válvula Bermad de 156 Ω, válvula genérica de 0,25 A, 1–2 válvulas por canal, E_AS con el *clamp*, D12–D17 DNP).
- `docs/diseno/estudio-salidas.md`: aviso en la cabecera (histórico).
- `docs/diseno/viabilidad-expansion.md` §0 (aviso sobre la corriente de las válvulas), §1 (tabla de datos, válvulas instaladas), §2.3 y el punto abierto «Corriente de las válvulas» del final: el dato abierto se resuelve con los límites de uso (DEC-0014, EXP-05).
- `docs/diseno/alimentacion.md` §1, fila «Carga de salidas» («instalados máx., bobinas a −10 °C»): pasa a límite de uso de la suma (ALI-12 v0.7).
- `docs/diseno/sensores.md` §0, §6 y §7: el calentamiento con «6 salidas a 0,25 A» se recalcula con la suma de 3,5 A de ALI-12 como caso de carga, o se deja como ejemplo y se añade ese caso.
- `hardware/componentes/M7.md` (función y uso: DNP → montado) y `bloque-salidas.md` (fila de D12–D17): `jr-conformidad`.
- `hardware/v2` y `campos-salidas.csv`: D12–D17 sin DNP.
- Memorias: `.claude/agent-memory/ing-diseno/project_salidas_d8.md` (válvulas, E_AS y DNP) y su línea del índice `MEMORY.md`, y `jr-conformidad/piezas-salidas-trucos.md` (D12–D17 DNP), cada agente la suya. La de `ing-validacion` la actualiza ing-validacion al validar.
- Fuera de SPEC-0034, los cambia el coordinador: `gestion/specs/SPEC-0032-integracion-esquema.md` (el punto «`salidas.md` con el dato medido de la válvula» pasa a depender de SPEC-0034, no de una medida), y `gestion/ESTADO.md` («Siguiente», «Pendiente del usuario» y «Para el layout»), al cerrar SPEC-0033.

## Entregables

- `docs/diseno/salidas.md` revisado, con la tabla de límites de uso en §0.
- `hardware/v2/` con D12–D17 montados; `hardware/componentes/campos-salidas.csv`.
- `docs/diseno/estudio-salidas.md` con aviso en la cabecera.
- Partes `NN-ing-diseno.md` y `NN-jr-conformidad.md`.

## Criterios de aceptación

- [ ] `salidas.md` no usa los datos de una válvula concreta como dato de diseño; la válvula instalada aparece, como mucho, como ejemplo dentro de los límites.
- [ ] Tabla de límites de uso con al menos los límites del alcance, cada uno con valor, origen (requisito, cálculo con su fórmula o datasheet con página) y consecuencia de superarlo.
- [ ] Los límites son coherentes con REL-05 (1 A), ALI-12 (3,5 A en total), ALI-13 (banda 3,5–4,9 A), REL-10 (fuga ≤ 1 mA) y ALI-01 (18–30 V).
- [ ] §5 con la rueda libre montada: tensión del M7 con margen; corriente media de 1 A (REL-05); I_FSM del M7 (30 A) frente al pico y la duración del corto que deja pasar el BTT6050 hasta cortar (limitación de ≈ 38 A, `salidas.md` §4); fuga en caliente dentro del presupuesto de R_OL; tiempo de cierre en función de L/R (REL-03 v0.7, VAL-0033-02).
- [ ] D12–D17 sin DNP en el esquema, en la BOM y en `campos-salidas.csv`; `verificar.py hardware/v2` con ERC 0 y paridad 0.
- [ ] Stock y precio de C95872 con fecha.
- [ ] Texto de serigrafía de los límites esenciales y notas de firmware actualizadas.

## Plan de validación

Nivel **completo** (cálculos y esquema; DEC-0005), con `esquema.md` v11 y `librerias.md` v7.

- Reproducir de forma independiente: cada valor de la tabla de límites de uso (la resistencia mínima de la carga, la corriente mínima para la carga abierta con su ADC, la fuga en reposo y la del M7 en caliente, el pico del diodo en la desmagnetización) y su coherencia con REL-05, ALI-12, ALI-13 y REL-10; `verificar.py hardware/v2`.
- Por muestreo: los campos de D12–D17 en el esquema frente a `campos-salidas.csv`, y el stock de C95872.
- Comprobar que no queda ningún dato de diseño de una válvula concreta en `salidas.md`.

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-17 | coordinador | Crea la spec (propuesta) | | | | |
