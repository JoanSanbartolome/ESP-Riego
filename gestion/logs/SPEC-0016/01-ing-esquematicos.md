---
spec: SPEC-0016
agente: ing-esquematicos
n: 01
fecha: 2026-11-05
estado: completado
---

# SPEC-0016 · 01 · ing-esquematicos

## Orden recibida

SPEC-0016 · rama spec/SPEC-0016-mantenimiento-fases-0-2 · Lee: gestion/specs/SPEC-0016-mantenimiento-fases-0-2.md, gestion/specs/SPEC-0008-correcciones-estudio-salidas.md y los informes citados · Haz: solo tu parte (alcance de SPEC-0008 para ing-esquematicos); no toques la parte de jr-conformidad · Entrega: archivos corregidos + log gestion/logs/SPEC-0016/01-ing-esquematicos.md con cada observación corregida o justificada y repaso de checklist. Brevedad: respuesta final solo contrato de salida; log telegráfico.

## Contexto consultado

- SPEC-0016, SPEC-0008; VAL-0005-01 (01–10), VAL-0007-01 (03, 10), VAL-0011-01 (08), VAL-0011-02 (08); DEC-0003, DEC-0004; `docs/02` v0.4 (ALI-04, ALI-12, ALI-13, REL-03, REL-05, REL-08, REL-10, FAB-03, FAB-07, §6).
- Datasheets (PDF de LCSC, `pdftotext`):
  - BTT6050-1ERA rev. 1.00: E_AS p. 7; ec. 5.1 y fig. 12 p. 13; R_SENSE §6.4 p. 19; R_OL §7.3.3.2 p. 27; tabla 9 (k_ILIS, I_IS(FAULT), V_IS(RANGE)) p. 30.
  - BTT6030-2ERA rev. 1.00: I_L(NOM)1/2 6/4 A p. 16; k_ILIS 2240 p. 31; E_AS 85 mJ p. 7.
  - IRLML0060 e IRLML0100: I_DSS ≤ 20 µA (25 °C) y ≤ 250 µA (125 °C), p. 2. FDN5618P rev. 3: I_DSS ≤ 1 µA con −48 V, p. 2.
- LCSC `wmsc.lcsc.com/ftps/wm/product/detail` (2026-11-05): `pdfUrl` de C2150359, C443993, C59442, C112645, C17651020, C3230071 y C475505. URL de TI comprobadas (HTTP 200).

## Acciones

Archivo: `docs/diseno/estudio-salidas.md`.

| Observación | Estado | Dónde |
|---|---|---|
| VAL-0005-01-02 BTS428L2 | Corregida: ✘ por V_IN(T+) 1,7–3,2 V (p. 6) y corto solo hasta 24 V (p. 3), además del coste | §11.3 (fila), §11.4 (tabla), §11.6 |
| VAL-0005-01-03 BTT6030 | Corregida: 6 A con un canal y 4 A con dos (p. 16); k_ILIS 2240 (p. 31); coste con 5 placas al tramo de 10: **9,28 $** en §11.3 y **9,31 $** en §5 (con M7), y nota ² con los tramos | §2.5, §5, §11.3, §11.4 |
| VAL-0005-01-04 k_ILIS | Corregida: 1500 ± 25 % a 0,5 A, 1600 ± 50 % a 50 mA, ± 12 % a 1 A (tabla 9, p. 30); 2240 en el BTT6030 | §2.5, §11.3 |
| VAL-0005-01-06 energía inductiva | Corregida: criterio de la ec. 5.1 con 2 válvulas frente a la curva de la fig. 12; tabla recalculada (57 / 115 / 139 mJ a 30 V frente a ≈ 155 mJ) | §1.2 b (remite), §2.5, §11.2 (fila y tabla), §11.3 |
| VAL-0005-01-08 avisos | Corregida: aviso de vigencia en la cabecera (S1–S7, que remiten a §11, DEC-0003, DEC-0004 y `docs/02` v0.4) y en §0; «supuesta instalada» en N4, §0.1, §1.2 a, §2.5, §3.1, §3.2 y §7. ISP752R/BSP752R unificados en ✔ por el *load dump* de 73,5 V y V_bb(AZ) ≥ 62 V (§1.5 = §11.3). EXP-01 sumada al borde (§1.8: ≈ 71 mm con A + C; vigente ≈ 66–71 mm). La nota «umbral del ISP752R» se sustituye por el dato del BSP752R (p. 6) | Cabecera, §0, §1.5, §1.8, §11.3, §11.6 |
| VAL-0005-01-09 trazabilidad | (b) Corregida: enlaces de TI (fabricante) y PDF de LCSC para ST e Infineon en §11.6; el BSP762T ya no remite a chipfind. (a) Justificada: el «sin verificar» de los descartes no cambia la conclusión (nota tras §11.3); M7, «por confirmar», no se usa con la opción 5; LT925 marcado «no consultado». (c) Nota en la cabecera: el stock de LCSC no es el de montaje en JLCPCB. El tipo y el stock de montaje de las piezas del esquema los confirma jr-conformidad | Cabecera, §2.2, §2.4, §11.3, §11.6 |
| VAL-0005-01-10 criterios | Corregida: tabla de vida útil y expansión por opción en §2; I_DSS con página en §2.4. **Cambia la cifra:** 4a y 4c ≤ 20 µA (≤ 250 µA a 125 °C), no ≤ 1–3 µA; sigue cumpliendo el criterio de 1 mA (§0.2 actualizado) | §0.2, §2, §2.4 |
| VAL-0005-01-01 (texto) | Corregida: «se protege solo» sustituido en §0.2 y §6 | §0.2, §6 |
| VAL-0005-01-05 (texto) | Corregida: R_SENSE 10 kΩ + *clamp* (V_ADC ≤ 3,1 V) y R_OL en §2.5 y como nota para el esquema en §11.5 | §2.5, §11.5 |
| VAL-0005-01-07 (texto) | Corregida: redacción de ALI-04 («máximo absoluto o, si lo especifica, *load dump*») y pines del corte general (2 IN + 1 DEN + 1 DSEL), marcada como sustituida por S3 | §11.5 |
| VAL-0007-01-03 | Corregida: avisos en §0, §1.3, §2.5, §5, §6, §7, §8, §9, §11, §11.4 (*hold-up* 470 µF/60 ms, suma de IS, corte con BTT6030) y §11.5 (REL-05, REL-08, ALI-04, pines). Remiten a DEC-0003 y a `docs/02`, no solo a §11 | Varias |
| VAL-0011-01-08 (b) | Corregida: N2 y §1.3 remiten a DEC-0004 (3,5 A; 3,5–4,9 A); §8: `OUT_n` ≈ 1,2 mm, bus en `Power_In` 5,1 A, retornos 4,9 A | N2, §1.3, §8 |
| VAL-0011-01-08 (c) / VAL-0007-01-10 | Ya resuelta en la memoria (DEC-0003/0004, 24 V DC); ahora también el motivo del BTS428L2 y los datos del BTT6030 | `.claude/agent-memory/ing-esquematicos/project_salidas_d8.md` |

## Decisiones y justificación

- No se reescriben §0–§10: se marcan con «*Sustituido: Sn*» y una lista única en la cabecera. Así se conserva el registro de D8 y no se cambia la recomendación (fuera del alcance).
- Energía: V_DS(AZ) = 66 V (mín., P_5.5.5), R × 0,88 en frío y L supuesta (igual que en VAL-0005-01). Con 2 bobinas RPE el margen es ×1,1: medir L antes de cerrar el esquema (REL-03, ya en `docs/02`).

## Verificación

- `verificar.py hardware/v2`: ERC 0 · DRC 0 · paridad 0 · LIMPIO (sin cambios en KiCad; no se ha usado el MCP).
- Recálculos (Python): energía 18/29, 35/57, 70/115 y 86/139 mJ; BTT6030 8,38 + 3 × (2,5169 − 2,2173) = 9,28 $; §5: 42,06 + 15 × 0,2996 = 46,55 $ → 9,31 $ por placa.
- Grep de términos obsoletos en el estudio («se protege», «instalad», «470 µF», «60 ms», «4 A en total», «por borde», «autonom», «fusible de 4 A»): cada aparición vigente lleva aviso o está en una sección con aviso.

**Repaso de checklists**

`requisitos.md` v3, «Estudios de diseño»:
- Coste con el tramo de la cantidad real: cumple en el BTT6030 (§5 y §11.3). Las demás filas, 6 o 12 por placa → 30/60 uds, ya cuadraban (VAL-0005-01).
- Cada descarte cita su parámetro: cumple (BTS428L2 corregido; el resto lo comprobó VAL-0005-01).
- Aviso que remite a la sección vigente: cumple (cabecera, §0, §7, §11, §11.4 y §11.5).

`requisitos.md` v3, «Términos obsoletos»: búsqueda hecha en el estudio y en mi memoria. No aplica al resto: es la parte de jr-conformidad o está fuera de mi zona.

`esquema.md` v5, «Cálculos»:
- Fórmula, datos con fuente y margen: cumple en la energía (§11.2), la fuga (§2.4) y el coste.
- Recalculado por el revisor: pendiente de validación.
- Tensiones frente a Vc: sin cambios (BSP752R unificado en ✔).
- Derating de cerámicos: no aplica.
- Energía de desmagnetización con la curva E_AS(I_L): cumple (§11.2).
- *Hold-up*: no aplica, queda sustituido (S2).
- Disipación: sin cambios.

Las demás secciones de `esquema.md` no aplican, porque no hay esquema.

## Pendiente

- jr-conformidad: tipo y stock de montaje en JLCPCB del BTT6050, del BTT6030 y del limitador cuando pasen al esquema (VAL-0005-01-09 a/c, DEC-0003).
- Prototipo / esquema: inductancia de la válvula (REL-03). Con L ≥ 2 H o bobinas de 100 Ω, el margen frente a la fig. 12 baja a ×1,1–1,4.

## Notas para el siguiente agente

- La lista S1–S7 de la cabecera del estudio es la referencia de vigencia. Si cambia una DEC, hay que actualizarla allí.
- No he podido comprobar los enlaces de st.com ni de infineon.com: para ST e Infineon se citan los PDF de LCSC.
