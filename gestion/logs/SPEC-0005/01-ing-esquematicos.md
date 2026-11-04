---
spec: SPEC-0005
agente: ing-esquematicos
n: 01
fecha: 2026-11-04
estado: completado
---

# SPEC-0005 · 01 · ing-esquematicos

## Orden recibida

SPEC-0005 · rama spec/SPEC-0005-estudio-salidas (ya activa; no cambies de rama) · Lee: gestion/specs/SPEC-0005-estudio-salidas.md (la orden completa), docs/02-especificaciones-v2.md v0.2 (§1, §2, ALI-01…ALI-04, REL-01…REL-09, FAB-07, FAB-08, §5, §7 D2 y D8), gestion/decisiones/DEC-0002-objetivo-v2-revisado.md y docs/01-analisis-v1.md (H5) · Haz: el estudio comparativo de tecnologías de salida (relé electromecánico estándar y subminiatura, SSR de salida MOSFET, triac con optotriac, MOSFET discreto low-side/high-side/bidireccional y high-side switch inteligente) con todos los criterios del alcance de la spec: matriz de cargas × opciones, corrientes de una electroválvula de 24 V AC típica (mantenimiento e inrush) justificadas con fuente, fuga en reposo, modo de fallo y mitigación, salida alimentada frente a contacto libre (D2), polos de borne por canal, tamaño de placa con 3 canales arriba y 3 abajo, piezas candidatas con MPN, LCSC, Basic/Extended, precio, fecha de consulta y datasheet, y coste por canal y para 6 canales a 5 y 10 placas. Investiga con WebSearch/WebFetch y con las búsquedas de piezas JLCPCB del MCP (search_jlcpcb_parts, get_jlcpcb_part, suggest_jlcpcb_alternatives, search_parts_registry); NO abras ni crees proyectos KiCad ni dibujes esquemas. La recomendación queda como propuesta para que el usuario decida D8; no modifiques docs/02 · Entrega: docs/diseno/estudio-salidas.md + log gestion/logs/SPEC-0005/01-ing-esquematicos.md, y responde con ESTADO, ARCHIVOS, VERIFICACIÓN, PENDIENTE y LOG.

**Mensajes del coordinador durante el trabajo** (resumen):

1. Datos nuevos del usuario y de VAL-0004-01:
   - transformador de 5 A (120 VA);
   - 6 salidas a la vez con ≈ 4 A en total;
   - 32 V AC en vacío (≈ 45 V de pico) como peor caso;
   - para cada opción, decir si funciona «entrada DC + salida alimentada»;
   - justificar la corriente del LED de control (H5);
   - REL-10 no existe.
2. **Sustituye a la parte de alimentación del mensaje 1:**
   - la única entrada es una fuente de 24 V DC de 5 A (18–30 V), con protección de polaridad y TVS SMBJ33A;
   - «salida alimentada» = 24 V DC;
   - las válvulas instaladas de 24 V AC ya no se alimentan desde la placa: hay que analizar el contacto libre con su transformador (≤ 32 V AC) o el cambio a válvulas DC o *latch*;
   - el triac solo vale para AC externa;
   - añadir las corrientes de las válvulas de 24 V DC.

## Contexto consultado

- Documentos del proyecto:
  - `gestion/specs/SPEC-0005-estudio-salidas.md`;
  - `docs/02-especificaciones-v2.md` v0.2;
  - `gestion/decisiones/DEC-0002-objetivo-v2-revisado.md`;
  - `docs/01-analisis-v1.md` (H5);
  - `gestion/informes/VAL-0004-01.md` (hallazgos 02, 05, 08 y 15; nota 6).
- Válvulas:
  - Rain Bird D42606, p. 1 (solenoides AC y *latch* TBOS);
  - Hunter: ficha de la PGV (370/210 mA a 50 Hz), especificación escrita, solenoide 60-6800 (19 V AC) y *latch* 458200 (6–9 V DC, 4,8 Ω);
  - Bermad: S-390-T-2W, «Electrical Data» (24 V DC: 4,2 W, 0,18 A, 156 Ω), y S-392T (*latch* de 9 V);
  - bobina RPE de 24 V DC (0,24 A; dato del buscador);
  - Hunter X-Core.
- Referencias de diseño: OpenSprinkler (triac directo; versión DC con impulso y mantenimiento) y Hackaday (2026-02-09).
- Datasheets (PDF descargado con WebFetch y texto extraído con `pdftotext` a la salida estándar):
  - Panasonic AQV252G, pp. 1–3;
  - onsemi MOC302xM y MOC306xM;
  - JSCJ BT136S;
  - Infineon ISP752R y **BTT6050-1ERA** (tablas 1 y 4.1);
  - Vishay VOM1271;
  - Espressif ESP32-S3 v2.2, tabla 5-4.
- LCSC (`wmsc.lcsc.com/ftps/wm/product/detail?productCode=…`) y JLCPCB (`jlcpcb.com/partdetail/…`), consultados el 2026-11-04. Tarifas de JLCPCB «PCB Assembly Price» (2026-10-22).

## Acciones

1. Comprobada la rama (`spec/SPEC-0005-estudio-salidas`). No hay archivos `.lck` y no se ha usado ninguna herramienta del MCP que cargue proyectos.
2. MCP: `get_jlcpcb_database_stats` devuelve 0 piezas y `get_jlcpcb_part C35449` no encuentra la pieza. `search_parts_registry` no da datos de compra. Los datos de las piezas se han tomado de las webs de LCSC y JLCPCB.
3. Primera versión del estudio con 24 V AC de entrada y puente rectificador.
4. Revisión con el mensaje 1 (32 V AC, 5 A, 4 A en total, LED, entrada DC). Cambios:
   - TVS a SMAJ48CA;
   - AQV252G sin margen;
   - MOSFET de 100 V;
   - §1.6 sobre la corriente del LED.
5. **Revisión completa con el mensaje 2 (entrada única de 24 V DC).** Cambios:
   - las vías V1–V4 para las válvulas;
   - las corrientes de las válvulas de 24 V DC y *latch*;
   - la topología sin puente (*high-side* frente a *low-side*);
   - los cortocircuitos limitados por la fuente y la autonomía de la lógica;
   - la opción 5 rehecha con el BTT6050-1ERA / BTT6030-2ERA (PROFET+ 24 V);
   - la nueva matriz «qué haría falta para seguir usando las válvulas de AC»;
   - los costes recalculados con un script de Python en línea, sin archivos.
6. Escrito `docs/diseno/estudio-salidas.md`, versión final con N1–N6, U5 y U6 citados.

## Decisiones y justificación

Todas son **propuestas**: D8 y D2 las decide el usuario.

- **Propuesta para D8: relé subminiatura 1b (G5NB-1A-E; alternativa HF46F/5-HS1).** Es la opción barata (≈ 4,1–4,6 $ por placa) que cubre a la vez V1 (válvulas de AC con su transformador, contacto libre) y V2 (válvulas de 24 V DC, salida alimentada), canal a canal. Es robusta ante cortos, tiene aislamiento galvánico y no tiene LED de control (sin riesgo de H5).
- **Alternativa: 4c** (2× IRLML0100 + VOM1271T, 100 V), si se quiere todo SMT.
- **Si el usuario abandona la AC:** opción 5 (BTT6050-1ERA), con protección, medida de corriente y diagnóstico por canal.
- **D2: ambas**, con 2 polos por canal + COM por borde y un puente de soldadura por canal.
- **Descartes razonados:**
  - triac (solo V1; no se apaga en DC);
  - PhotoMOS de 60 V (sin ventana para la TVS con 45,3 V de pico; la de 100 V no tiene stock);
  - *low-side* 4a (un corto del cable a tierra abre la válvula);
  - ISP752R e IPS160 (stock de 89 y 1).
- **Excitación del LED (H5):** desde 3,3 V con una R fija y un AO3400A, no directamente desde el GPIO, porque el ESP32-S3 solo especifica V_OH con carga de alta impedancia. I_F de 10,5–22 mA según la pieza, de ×2,2 a ×3,7 sobre I_FT.
- **REL-05:** la prueba de 6 × 1 A = 6 A supera N2. Se propone hacerla con 4 A en total.
- **Corte general y medida del bus:** propuestos como requisitos nuevos **sin número** (REL-10 no existe).
- **FAB-08:** ≈ 80 mm de alto con relés, ≈ 75 mm con 4c y ≈ 70 mm con la opción 5 (±5 mm).

## Verificación

- `python herramientas/verificar.py hardware/v2`: «No existe C:\Users\josan\proyectos\KICAD_mcp\hardware\v2.» (código de salida 2). No hay proyecto v2 y esta spec no toca KiCad: ERC, DRC y paridad no aplicables.
- No se ha abierto ni creado ningún proyecto con el MCP.
- Costes de §5 recalculados con un script en línea: 1b G5NB = 0,648 $/canal a 5 placas y 4,64 $ por placa. Corrientes de LED y anchos IPC-2221 calculados con el mismo script.

## Pendiente

- **Usuario (vía coordinador):**
  - decidir D8 y D2;
  - decidir la vía de las válvulas: V1 (mantener las de AC con su transformador), V2 (solenoides de 24 V DC), V3 (*latch*) o una mezcla;
  - si V1: modelo, VA y tensión en vacío del transformador;
  - marca y modelo de las válvulas instaladas.
- **Coordinador:**
  - reescribir ALI con N1;
  - actualizar REL-02, REL-03, REL-05 (y la prueba térmica de §6), REL-08, FAB-07 y FAB-08 según §7.3 del estudio;
  - asignar ID a los dos requisitos nuevos (corte general, medida del bus);
  - el bloque ALI debe dar autonomía a la lógica frente a un corto en campo (§1.3).
- **jr-conformidad:** confirmar los LCSC y los tipos (M7 como *Basic* sin confirmar). Elegir:
  - el relé o *high-side* del corte general;
  - el fusible de 4 A T;
  - el fusible rápido por canal;
  - la SMAJ33CA;
  - un Schottky de ≥ 60 V;
  - un MOSFET de 60 V especificado a 2,5 V.
- **SPEC-0006:** el conector EXP-02 tiene que llevar su parte del bus de 24 V y el COM.
- La base de JLCPCB del MCP no está descargada (`download_jlcpcb_database` no está en mi lista de herramientas).

## Notas para el siguiente agente

- Precios y stock del 2026-11-04. El stock de ISP752R (89), Z0109MN (57), IPS160HFTR (1) y LT925 (3) no sirve.
- Las dimensiones de §4 son estimaciones para decidir; la tabla de §8 es preliminar.
- Los datos de la bobina RPE de 24 V DC y el impulso de 250 ms del Hunter 458200 vienen de tiendas, sin verificar.
