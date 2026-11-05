---
spec: SPEC-0011
agente: ing-validacion
n: 01
fecha: 2026-11-05
estado: completado
---

# SPEC-0011 · 01 · ing-validacion

## Orden recibida

SPEC-0011 · rama spec/SPEC-0011-requisitos-v04 (activa; no cambies de rama ni uses git para escribir; git de lectura sí) · commits revisados 6f2888e y 81b848f (base: d4cf007) · Lee: la spec, DEC-0004, docs/02 v0.4 (diff con d4cf007), docs/03, VAL-0007-01 (hallazgos 01, 02, 05, 06 y 09) y DEC-0003; las checklists requisitos v3, esquema v4 y layout v4 (aplica la de requisitos v3). No hay cambios en KiCad: no uses el MCP. · Haz: valida criterio a criterio, con siete comprobaciones:

1. la fuente LED supuesta frente a datasheets reales;
2. la banda de 3,5–4,9 A frente a la fuente y la lógica, con 1–2 eFuses o *hot-swap* de ≥ 60 V;
3. 1,2 mm con 1 oz para 4,9 A con ΔT ≤ 40 °C, y el BTT6050 y el borne con esa sobrecarga;
4. el total de 3,5 A frente a REL-05 y la carga instalada;
5. la SMBJ33A frente a la OVP;
6. los hallazgos 01, 02, 05, 06 y 09 uno a uno, y las decisiones del usuario sin complejidad añadida;
7. las cifras de la DEC frente a las de docs/02, y los restos de «4 A», «16 V» y «32 V».

Entrega: gestion/informes/VAL-0011-01.md y este log.

## Contexto consultado

- SPEC-0011, DEC-0004, DEC-0003 (campo `requisitos` y «Consecuencias»), docs/02 v0.4 y el diff `d4cf007..81b848f` de los 8 archivos.
- VAL-0007-01 (hallazgos y propuestas) y las checklists de requisitos v3, esquema v4 y layout v4.
- `docs/diseno/estudio-salidas.md`: §0, §1.2–§1.3 y §8, con los valores de diseño de las válvulas.
- SPEC-0006 y SPEC-0008, y la memoria de ing-esquematicos.
- Datasheets (texto en `scratchpad/val1101/`):
  - LRS-150 (2025-04-07, ya extraído);
  - LRS-100-24 y LRS-120, copias de distribuidor obtenidas con WebFetch;
  - BTT6050-1ERA rev. 1.00 (ya extraído);
  - LM5069 SNVS452G;
  - página de producto del TPS2663;
  - SMBJ33A y HLG-120H-24, solo por los resultados de búsqueda.
- Al final, para contrastar: los mensajes de `6f2888e` y `81b848f` y el diario del coordinador del 2026-11-05.

## Acciones

1. He comprobado la rama (`spec/SPEC-0011-requisitos-v04`) y el commit (`81b848f`). No he usado ni el MCP ni `kicad-cli`.
2. He adaptado `scratchpad/val1101/traza.py`, a partir del de `val0701`, con la base `d4cf007`. Resultados:
   - 0 avisos y 57 requisitos;
   - 10 IDs cambiados, que coinciden con los de la spec y la DEC;
   - ningún ID inexistente en 25 archivos.
3. He escrito `scratchpad/val1101/calc.py`, con:
   - IPC-2221: 1,16 mm para 4,9 A con ΔT = 40 °C;
   - la banda: ± 16,7 %;
   - la protección de la fuente en % de la potencia frente a la tensión de ajuste;
   - el TPS2663 (3,86–4,54 A) y el LM5069 (3,67–4,74 A);
   - las 12 válvulas frente a la tensión;
   - T_J del BTT6050 con 4,9 A;
   - los márgenes de ALI-09.
4. He descargado o leído las hojas de las fuentes y de los limitadores. La LRS-120 oficial da 404 en meanwell.com. Un segundo intento con `curl` y otra cabecera lo bloqueó el clasificador, y no lo he repetido: he usado WebFetch y WebSearch.
5. He buscado con Grep los términos obsoletos en docs/, las checklists, las specs abiertas o propuestas, los agentes, las memorias, `CLAUDE.md`, `gestion/README.md` y las plantillas.
6. He escrito el informe y este log.

## Decisiones y justificación

- **Hallazgo 01 (M) y veredicto RECHAZADO:**
  - el criterio 2 pide una banda «compatible con la fuente», y la propia DEC atribuye a la fuente un ajuste de 21,6–28,8 V, que ALI-01 admite;
  - la hoja de la LRS da la sobrecarga en % de la potencia: ya a 25 V la protección mínima (5,04 A) queda por debajo de 4,9 + 0,25 A;
  - a 28,8 V, las 12 válvulas de diseño (3,60 A a 20 °C y 4,03 A en frío) pasan de la cota inferior de la banda, y no existe ninguna banda posible;
  - el criterio se cumple solo a 24 V, así que lo doy por parcial. El arreglo es de redacción (fijar el ajuste en 24 V) y no añade complejidad.
- **Retorno GND (02) en B y no en M:** un retorno de 3,5 A con ΔT ≤ 10 °C lleva 4,9 A con ΔT ≈ 22 °C, así que no se daña. Es una incoherencia del texto, no un riesgo. Por eso el criterio 3 se cumple.
- **BTT6050 (03):** con 4,9 A no se daña, porque o queda por debajo de T_J(SC) o se enclava. Lo dejo en B porque la DEC describe mal el comportamiento («rearme») y ningún requisito dice qué hace el firmware ante el enclavamiento.
- **HLG-120H-24:** el 95–108 % sale de copias de la hoja que citan los buscadores. Lo uso solo como ejemplo de por qué hay que mirar la etiqueta real, y lo marco como no comprobado en el PDF oficial.
- **Lo que no propongo:** ningún componente ni protección por canal, por la decisión 2 del usuario.

## Verificación

- No hay cambios en KiCad: `verificar.py` no aplica.
- Trazabilidad en memoria: 0 avisos. El `TRAZABILIDAD.md` versionado difiere en 12 filas; lo regenera el merge.
- Cifras de la DEC frente a docs/02: todas coinciden. El «±10 %» de la DEC es erróneo y no está en docs/02.
- IPC-2221: 1,16 mm (4,9 A, 40 °C) y 0,30 mm (1 A, 10 °C), que coinciden con la DEC y con VAL-0007-01.

## Pendiente

- **Coordinador:** para pasar a APROBADO, el hallazgo 01:
  - ALI-12 y la DEC: «fuente en su ajuste nominal de 24 V (± 2 %)»;
  - ALI-01: quitar «el ajuste de la fuente»;
  - §6: las pruebas de sobrecarga, a 24 V;
  - docs/03: mirar la etiqueta de la fuente antes de elegir el limitador;
  - la errata «±10 %».
- **Hallazgos B:** se resuelven ahora o pasan a una spec propuesta. El 06 va a SPEC-0006, el 08 a SPEC-0008, y la memoria de ing-esquematicos se actualiza en su próxima orden.
- **Usuario:** el modelo o la etiqueta de la fuente real cerrarían el supuesto. También cabe confirmar que la deja en 24 V.

## Notas para el siguiente agente

- Las hojas de MEAN WELL de la familia LRS dan la sobrecarga en «% rated output power». Para pasarla a corriente, hay que dividir por la tensión de ajuste real.
- En meanwell.com, la URL `LRS-120-SPEC.PDF` da 404. WebFetch guarda los PDF binarios en `tool-results/`, desde donde se pueden copiar a la carpeta temporal y pasar por `pdftotext`.
