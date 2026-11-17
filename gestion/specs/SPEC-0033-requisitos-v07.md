---
id: SPEC-0033
titulo: Requisitos v0.7
fase: 3
estado: abierta
responsable: coordinador
revisor: ing-validacion
rama: spec/SPEC-0033-requisitos-v07
requisitos: [REL-03, REL-05, REL-10, REL-11, ALI-12, EXP-04, EXP-05]
depende_de: [SPEC-0030]
creada: 2026-11-17
cerrada:
validacion:
---

# SPEC-0033 · Requisitos v0.7

<!-- Objetivo, restricciones y criterios: sin pasos ni números de línea. Unas 60 líneas. Una spec de bloque o de hito de layout lleva sus pasos en «Alcance». -->

## Objetivo

`docs/02-especificaciones-v2.md` pasa a la v0.7 con las salidas definidas por límites de uso propios de la placa, independientes de la válvula (DEC-0014), y con el requisito de alimentación del módulo de expansión (DEC-0012). No queda ningún requisito que dependa de medir la válvula instalada.

## Alcance

- Incluye:
  - REL-03: la carga inductiva la absorbe la rueda libre montada en cada salida (D12–D17), sin límite de inductancia; se quitan la comprobación de E_AS con el *clamp* y la medida previa a `v2.0-sch`;
  - REL-05: una carga por salida, 1 A continuo como límite de uso en la serigrafía; sin «0,2–0,56 A con una o dos electroválvulas». La pista y el borne para 4,9 A no cambian;
  - ALI-12: la carga instalada máxima de 3,5 A pasa a ser el límite de uso de la suma de las salidas activas a la vez, sin «12 válvulas de 0,25 A». No cambian la fuente, el limitador (ALI-13) ni la lógica;
  - REL-10: los umbrales de carga abierta, expresados como límites de uso (corriente mínima de la carga, resistencia máxima en reposo), cuyos valores fija SPEC-0034;
  - requisito nuevo, **REL-11 (M)**: tabla de límites de uso de las salidas, como la de un manual, con al menos tensión, tipo de carga, corriente continua por salida, suma simultánea, resistencia mínima de la carga, corriente mínima para detectar carga abierta, fuga en reposo y cable. Sus valores los calcula SPEC-0034 a partir del circuito; los esenciales van en la serigrafía;
  - EXP-04 (o un ID propio): el módulo de expansión tiene entrada de 24 V y limitador propios, y no recibe 24 V por EXP-02 (DEC-0012, VAL-0006-01 punto a); D9 cerrada en §7 con DEC-0012;
  - §1, §2 y §6: la válvula instalada es un ejemplo de carga dentro de los límites, no el dato de diseño; la prueba de salidas comprueba los límites de uso. La prueba térmica y la de sobrecarga del conjunto siguen igual;
  - cabecera, §9 (redefiniciones de la v0.7) y §10, con DEC-0014, DEC-0012 y SPEC-0033;
  - lista, con Grep, de lo que queda por cambiar fuera de `docs/02` (`docs/diseno/salidas.md`, `estudio-salidas.md`, el campo DNP de D12–D17 en el esquema), que hace SPEC-0034.
- Excluye: `docs/diseno/` y el esquema; valores numéricos nuevos de los límites de uso (los calcula SPEC-0034); cambiar la fuente, la banda del limitador o la corriente de 1 A.

## Entradas

- `gestion/decisiones/DEC-0014-salidas-con-limites-nominales.md` entera, y el punto 2 de DEC-0008.
- `gestion/decisiones/DEC-0012-expansion-i2c.md`, «Consecuencias».
- `docs/02-especificaciones-v2.md` (v0.6) entero.
- `docs/diseno/salidas.md` §0 y §5 (rueda libre), solo para citar bien el circuito.
- `gestion/specs/SPEC-0034-limites-salidas.md`.
- `gestion/checklists/requisitos.md` (v5).

## Entregables

- `docs/02-especificaciones-v2.md` v0.7.
- `gestion/checklists/esquema.md` v11: los puntos de E_AS pasan a la rueda libre y a los límites de uso.
- `gestion/specs/SPEC-0034-limites-salidas.md`: lista de lo que queda por cambiar fuera de `docs/02`.

## Criterios de aceptación

- [ ] REL-03 exige la rueda libre montada en cada salida y no depende de la inductancia ni de una medida de la válvula; cita DEC-0014.
- [ ] REL-05 dice una carga por salida y 1 A continuo como límite de uso; la pista y el borne para 4,9 A con los mismos ΔT que en la v0.6.
- [ ] ALI-12 fija 3,5 A como límite de uso de la suma de las salidas activas a la vez, sin número ni tipo de válvulas; las demás cifras de ALI-12 y ALI-13 son las de la v0.6.
- [ ] REL-11 existe con prioridad M, enumera los límites de uso y remite sus valores a SPEC-0034 y la serigrafía.
- [ ] El módulo de expansión tiene 24 V y limitador propios, sin 24 V por EXP-02; D9 cerrada en §7 con DEC-0012.
- [ ] Ningún requisito vigente ni prueba de §6 depende de medir la válvula instalada; §1 y §2 la citan solo como ejemplo de carga.
- [ ] La cabecera cita DEC-0014; §9 (redefiniciones de la v0.7) y §10 citan SPEC-0033, DEC-0014 y DEC-0012.
- [ ] SPEC-0034 lista, con ruta, cada aparición pendiente fuera de `docs/02`; `docs/diseno/` y `hardware/` sin cambios.
- [ ] `gestion.py trazabilidad` sin avisos.

## Plan de validación

Nivel **ligero** (texto de requisitos; DEC-0005), con `gestion/checklists/requisitos.md` v5.

- Reproducir de forma independiente: la búsqueda de «válvula», «Bermad», «medir», «0,25 A», «dos electroválvulas», «E_AS» y «DNP» referidos a las salidas en `docs/`, `gestion/` (specs propuestas, checklists), `CLAUDE.md` y `.claude/agent-memory/`, y comprobar que cada aparición fuera de `docs/02` está en la lista de SPEC-0034 o es histórica (specs cerradas, informes, decisiones).
- Comparar las tablas de §4 de la v0.6 y la v0.7: cada ID cuyo texto cambia está en `requisitos` y en el historial.
- Cada punto de «Decisión» y «Consecuencias» de DEC-0014, y el requisito pendiente de DEC-0012, llegan a `docs/02` o a SPEC-0034.
- Por muestreo: las cifras de ALI-12 (salvo la carga instalada), ALI-13 y la pista de REL-05, iguales a las de la v0.6.

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-17 | coordinador | Crea la spec (propuesta) | | | | |
| 2026-11-17 | coordinador | Abre la spec |  |  |  |  |
| 2026-11-17 | ing-validacion | VAL-0033-01 RECHAZADO (4 M, 2 B) | VAL-0033-01 | 117667 |  |  |
| 2026-11-17 | ing-validacion | VAL-0033-02 APROBADO | VAL-0033-02 | 9916 |  |  |
