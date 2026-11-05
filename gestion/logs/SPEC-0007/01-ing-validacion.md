---
spec: SPEC-0007
agente: ing-validacion
n: 01
fecha: 2026-11-05
estado: completado
---

# SPEC-0007 · 01 · ing-validacion

## Orden recibida

SPEC-0007 · rama spec/SPEC-0007-requisitos-v03 (activa; no cambies de rama ni uses git para escribir) · commit revisado 95f0b40 · Lee: gestion/specs/SPEC-0007-requisitos-v03.md (alcance y criterios), gestion/decisiones/DEC-0003-salidas-high-side-y-limitador.md, docs/02-especificaciones-v2.md (v0.3; compárala con la v0.2 con `git diff 9f8f402~1 95f0b40 -- docs/02-especificaciones-v2.md` o leyendo la versión anterior con `git show`), gestion/informes/VAL-0004-02.md y VAL-0005-01.md (las observaciones que esta spec debe resolver), docs/diseno/estudio-salidas.md (§11), gestion/checklists/requisitos.md (v2, en esta rama) y los cambios de esquema.md v3 y layout.md v3; los logs del coordinador solo al final. No hay cambios en KiCad: no uses el MCP. · Haz: valida criterio a criterio. En particular: que cada observación 01, 02 y 04–10 de VAL-0004-02 y 01 y 03–07 de VAL-0005-01 esté resuelta o justificada una a una; que los requisitos nuevos o redefinidos (ALI-04, ALI-09, ALI-12, ALI-13, REL-01…05, REL-08, REL-10, AMB-02, FAB-03, FAB-06…08) sean coherentes entre sí, con DEC-0003 (D2 sin contacto libre, BTT6050, limitador común) y con los datos de los datasheets citados (BTT6050 48 V máx., V_S(LD) 65 V, límite ≥ 38 A, kILIS 1500 ± 25 %); que cada requisito M tenga criterio verificable en §6 y que §7, §9 y §10 estén al día; y que no queden restos del contacto libre ni de 24 V AC como carga instalada en docs/, checklists, specs abiertas o propuestas y .claude/agents/. Aplica la checklist de requisitos v2. · Entrega: gestion/informes/VAL-0007-01.md con veredicto + log gestion/logs/SPEC-0007/01-ing-validacion.md (si ya hay logs en esa carpeta, usa el siguiente número). Responde con VEREDICTO, hallazgos por severidad, PROPUESTAS y LOG.

## Contexto consultado

- `gestion/specs/SPEC-0007-requisitos-v03.md`, DEC-0003, DEC-0002 (errata) y `docs/02` v0.3. La v0.2 la leo con `git diff 9f8f402~1 95f0b40` y comparo las tablas con un script.
- VAL-0004-02 y VAL-0005-01 (observaciones y propuestas de checklist).
- `docs/diseno/estudio-salidas.md`: §0.2, §6, §8 y §11.
- Checklists de requisitos v2, esquema v3 y layout v3, y su diff.
- SPEC-0006 y SPEC-0008 de esta rama; SPEC-0009 y SPEC-0010 de `main`, exportadas a `scratchpad/val0701`.
- `.claude/agents/*.md`, `CLAUDE.md`, `docs/03` y `.claude/agent-memory/`.
- Datasheets, ya descargados para VAL-0005-01 y extraídos con `pdftotext`:
  - BTT6050-1ERA rev. 1.00: P_4.1.1–P_4.1.3, P_4.1.12, tabla 7 (I_L5(SC)) y P_7.5.x (k_ILIS);
  - MEAN WELL LRS-150 (2025-04-07): OVP de la LRS-150-24 y protección de sobrecarga.
- Al final, para contrastar: los mensajes de los commits de la rama, el registro de la spec y el diario del coordinador del 2026-11-04 (versión de `main`).

## Acciones

1. He comprobado la rama (`spec/SPEC-0007-requisitos-v03`) y el commit (`95f0b40`). No he usado ni el MCP ni `kicad-cli`.
2. He revisado el diff completo de la rama (10 archivos).
3. He escrito `scratchpad/val0701/traza.py`, que:
   - ejecuta `gestion.trazabilidad()` en memoria, sustituyendo `escribir`: 0 avisos y 57 requisitos;
   - compara las tablas v0.2 → v0.3: 2 nuevos, 14 cambiados y REL-08 de S a M;
   - cruza el resultado con los campos `requisitos` de SPEC-0007 (coinciden exactamente) y de DEC-0003 (faltan AMB-02 y FAB-06);
   - busca IDs inexistentes o retirados en 22 archivos: no hay ninguno.
4. He buscado con Grep los términos obsoletos en todo el repositorio, salvo los informes y los logs, y en las specs de `main`.
5. He recalculado:
   - la cadena de tensiones con el datasheet del BTT6050;
   - la ventana del umbral del limitador con 5,0 / 5,25 / 5,5 A de protección de la fuente: ± 6 / 8,7 / 11 %;
   - el calentamiento IPC-2221 de una pista de 1 A (0,30 mm) con 1,5–5 A: de 25 a 388 °C.
6. He revisado una por una las 16 observaciones, los 16 requisitos que cambian y la checklist de requisitos v2.
7. He escrito `gestion/informes/VAL-0007-01.md` y este log.

## Decisiones y justificación

- **Checklist:** la de requisitos v2. Las de esquema y layout se revisan como entregables.
- **«Cada requisito M con criterio verificable en §6»:** lo interpreto para los M nuevos o redefinidos, porque los de fabricación y KiCad (FAB, KIC) se verifican por inspección o DRC, no con pruebas de §6. Todos tienen prueba o inspección. Los defectos que he encontrado están en los puntos de prueba (hallazgos 01 y 05) y en lo que no se prueba (hallazgo 02, y el limitador en el reset, hallazgo 06).
- **Severidad del 02 (M, no A):** la medida IS para cortar por firmware ya existe (REL-10) y el arreglo es una línea de docs/02, antes de que haya esquema. Pido corregirlo antes del merge, porque ninguna checklist posterior lo detectaría.
- **Severidad del 03 (M):** docs/02 manda, pero el aviso previsto en SPEC-0008 («la conclusión vigente es §11») remitiría a la recomendación que DEC-0003 sustituye. Además, el estudio es una entrada del esquema de las salidas.
- **El 10 (memoria de ing-esquematicos):** está fuera del ámbito literal de la checklist (`.claude/agents/`), pero ese agente lee su memoria al empezar. Lo dejo en B y propongo ampliar el ámbito de la búsqueda.
- **Veredicto: APROBADO_CON_OBSERVACIONES** (C 0 · A 0 · M 3 · B 7). Los tres criterios de aceptación se cumplen.

## Verificación

- No hay cambios en KiCad: `verificar.py` no aplica.
- Trazabilidad en memoria: 0 avisos y 57 requisitos (M 42, S 12, C 3). El `TRAZABILIDAD.md` versionado está sin regenerar; lo regenera el merge.
- Tablas: los cambiados o nuevos coinciden con el campo `requisitos` de SPEC-0007 (16 de 16).
- BTT6050: 48 V (P_4.1.1), 65 V (P_4.1.12), I_L5(SC) 38 / 47 / 56 A y k_ILIS 1500 ± 25 % a 0,5 A. Coinciden con docs/02 y DEC-0003.

## Pendiente

- **Coordinador:**
  - antes del merge, corregir en docs/02 los hallazgos 01 y 02, que son de redacción, y la errata de DEC-0003 (hallazgo 04);
  - el resto, como specs propuestas o como ampliación de SPEC-0008 (03) y SPEC-0006 (07);
  - pedir a ing-esquematicos que actualice su memoria (10).
- **Usuario:** el modelo de la fuente (corriente nominal, protección de sobrecarga y OVP). Cierra la ventana del limitador (01) y la elección entre la SMBJ33A y la SMBJ36A (09 b).
- **Merge:** `main` tiene SPEC-0009 y SPEC-0010. Hay que regenerar `TABLERO.md` y `TRAZABILIDAD.md`.

## Notas para el siguiente agente

- En la guardia, una redirección a `"$D/x"` se bloquea porque no expande variables: usa rutas literales en la carpeta temporal.
- `scratchpad/val0701/traza.py` sirve para cualquier spec de requisitos: cambia el commit base de la comparación de tablas.
