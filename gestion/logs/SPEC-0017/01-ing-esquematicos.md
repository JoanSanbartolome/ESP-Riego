---
spec: SPEC-0017
agente: ing-esquematicos
n: 01
fecha: 2026-11-05
estado: parcial
---

# SPEC-0017 · 01 · ing-esquematicos

## Orden recibida

SPEC-0017 · rama spec/SPEC-0017-calculos-alimentacion · Lee: gestion/specs/SPEC-0017-calculos-alimentacion.md y sus Entradas · Haz: todo el alcance; no edites KiCad ni uses el MCP · Entrega: docs/diseno/alimentacion.md, fichas nuevas en hardware/componentes/ y log gestion/logs/SPEC-0017/01-ing-esquematicos.md con el repaso de la checklist. Brevedad: la respuesta final, solo el contrato de salida; el log, en estilo telegráfico.

## Contexto consultado

- Spec; `docs/02` v0.4 (ALI, REL-04/08, §5, §6); DEC-0003, DEC-0004; `estudio-salidas.md` (S1–S7, §11); fichas LM5069, TPS2663, SMBJ33A, TYPE-C, USBLC6, WJ500V; checklists `requisitos.md` v3 y `esquema.md` v5.
- Datasheets (texto con pdftotext; páginas citadas en el documento): TPS2663 SLVSE94G; LMR36520 SNVSBF0C; TPS54360B SNVSB93 y LMR16030 SNVSAH9B (descartados); TPS2116 SLVSFG1A; TLV1117LV SBVS160C; SQD50P06-15L 69098 rev. E; Littelfuse 451/453 (curva de la p. 3 leída como imagen); ESP32-S3 v2.2 (ADC, p. 66; pines, pp. 16 y 18); WROOM-1 v1.8 (p. 28); SMBJ33A local.
- LCSC: JSON `wmsc.lcsc.com/ftps/wm/product/detail` (stock y precio, 2026-11-05) de todas las piezas de §7.
- Librerías oficiales de KiCad 10: símbolos y huellas comprobados por nombre (Grep y listado).

## Acciones

- Creado `docs/diseno/alimentacion.md`: arquitectura, selección, cálculos, presupuesto, térmica, pines, lista de piezas, restricciones de layout, trazabilidad, riesgos y anexos.
- Fichas nuevas: **no creadas**. La guardia bloquea `hardware/componentes/`, que no está en mi zona. Sus datos están en el Anexo A del documento.
- Sin cambios en KiCad ni en `firmware/` (el pinout no está todavía en el esquema).

## Decisiones y justificación

- Limitador: TPS26632RGER. 4,30 kΩ → 3,84–4,54 A. MODE abierto (*latch*); UVLO, PLIM y PGTH a GND; SHDN con 10 kΩ a GND; IMON con 10 kΩ. LM5069 descartado: NFET, R_S y SOA, y ≈ 1 $ más.
- Buck: LMR36520FADDAR (65 V, síncrono, EN de ± 6 %).
  - TPS54360B descartado: diodo externo y EN por corriente, con margen de ALI-06 de 0,03–0,8 V.
  - FB al 0,1 %: con el 1 % daba ± 3,1 %.
- UVLO: 100 kΩ / 10 kΩ. Arranque 12,50–14,56 V (nominal 13,5 V, no ≈ 15 V). La cota de bajada de 15,5 V, sin histéresis mínima garantizada, obliga. **Propuesta al coordinador:** aceptar el nominal de 13,5 V (los criterios M se cumplen) o reescribir el «≈ 15 V» de ALI-06.
- Unión USB: multiplexor TPS2116 en lugar de Schottky. Con el Schottky, el +5V quedaba fuera de ± 3 %, o había retroalimentación de la entrada por el diodo interno del buck.
- LDO TLV1117LV. AMS1117 (caída y tántalo) y AP7361C (stock 3) descartados.
- Medida de VIN: 0,1 % y ATTEN 6 dB (± 10 mV). A 12 dB son ± 50 mV: fuera de ± 3 %.
- Polaridad: P-MOS de 60 V con zéner de 15 V. Se descarta usar el B_GATE del TPS2663: el FET se apaga con SHDN y dejaría el buck alimentado por el diodo.
- Presupuesto propuesto para SPEC-0006: 5 V de la expansión ≤ 0,30 A y 3,3 V ≤ 50 mA. Lógica total: 4,32 W.

## Verificación

- `verificar.py hardware/v2`: ERC 0, DRC 0, paridad 0, LIMPIO (sin cambios en KiCad).
- Cálculos rehechos con un script en el *scratchpad* (resultados en §0, §3 y §4 del documento).

### Repaso de checklists

`esquema.md` v5, sección «Cálculos» y «Alimentación»:

| Punto | Estado |
|---|---|
| Fórmula, datos con fuente y margen | Cumple (§3; página por dato) |
| Recalculado por el revisor | Pendiente (validación) |
| Tensiones nominales ≥ peor caso, con Vc | Cumple (§3.5) |
| Cerámicos con *derating* de DC y temperatura | Cumple en parte. Se da la capacidad efectiva aproximada de COUT y CIN (§3.6, §3.13.4); sin curva del fabricante: pendiente en SPEC-0018 |
| Energía de desmagnetización | No aplica (bloque de salidas) |
| *Hold-up* | No aplica: no hay retención (§3.13.4) |
| Disipación a 60 °C | Cumple (§5) |
| Polaridad, fusible y TVS para 5,1 A a 50 °C | Cumple (§3.2–§3.4) |
| TVS tras la polaridad; V_GS limitada; V_DS ≥ Vc | Cumple (§3.3) |
| Divisor de VIN hasta V_RWM y pin protegido ante Vc | Cumple (33 V → 1,53 V; Vc → 2,48 V < VDD) |
| Limitador: buck antes, banda, corte antes del UVLO, *pull-down* | Cumple (§3.13) |
| Bus apagado alimentado por IN o DEN | Pendiente: bloque de salidas (§10.7) |
| V_RWM ≥ 30 V y Vc ≤ nominal | Cumple |
| UVLO tras las protecciones y ajustable | Cumple (§3.7) |
| Presupuesto con 6 salidas | Cumple (§4) |
| VBUS sin retroalimentación | Cumple (TPS2116, §3.8) |
| Tabla de restricciones de layout | Cumple (§8) |
| Campos de símbolo, ERC y cajetín | No aplica (sin esquema; SPEC-0019) |

`requisitos.md` v3, «Coherencia técnica» y «Estudios de diseño», en lo que aplica:

| Punto | Estado |
|---|---|
| Cadena de tensiones | Cumple |
| Presupuesto frente a cargas simultáneas | Cumple |
| Orden de protecciones frente a la prueba de polaridad | Cumple |
| Límite global con mecanismo | Cumple (U1) |
| Banda con tolerancia | Cumple |
| Protecciones escalonadas | Cumple: F1 7,2 A > limitador 4,54 A; la fuente a 5,14 A no actúa |
| Margen de las pruebas de §6 frente a la precisión | Cumple (§3.10) |
| UVLO en los dos sentidos | Cumple |
| Coste con el tramo de la cantidad real | Cumple (§7) |
| Descartes con el parámetro que los descarta | Cumple |
| Cambio de requisitos | No aplica: ninguno, solo la propuesta de ALI-06 |

## Pendiente

- **Coordinador o jr-conformidad (SPEC-0018):**
  - crear las fichas de LMR36520, TPS2116, TLV1117LV, SQD50P06-15L, 0451010.MRL, FXL0650-100-M, SS310 y BZT52C15 con el Anexo A;
  - completar la ficha de TPS2663 con la variante elegida.
- **jr-conformidad:**
  - tipo Basic/Extended y stock de montaje;
  - símbolo LMR36520 (derivado de LMR36510ADDA);
  - pinout de SUD50P06-15 frente a SQD50P06-15L y de TLV1117-33 frente a TLV1117LV;
  - datasheet de la alternativa UMW SUD50P06-15;
  - stock de R8 (760 uds.).
- **Coordinador:**
  - nominal del UVLO de 13,5 V frente al «≈ 15 V» de ALI-06;
  - coste del limitador (3,56 $ a 5 placas, por encima de los 2–3 $ de DEC-0003);
  - comprobar la fuente real (DEC-0004, `docs/03`).
- **SPEC-0006:** presupuesto de la expansión (5 V ≤ 0,30 A; 3,3 V ≤ 50 mA).
- **Bloque MCU:** pines propuestos (GPIO1 VIN_SENSE, GPIO2 LIM_IMON, GPIO21 LIM_EN, GPIO14 LIM_FLT).
- **Bloque de salidas:** retroalimentación del bus apagado a través de IN y DEN.

## Notas para el siguiente agente

- SPEC-0019: etiquetas jerárquicas BUS_24V, +5V, +3V3, GND, VBUS (desde el USB), VIN_SENSE, LIM_EN, LIM_FLT y LIM_IMON. Pines de U1 sin conectar: MODE, PGOOD, B_GATE, DRV y NC 19–24.
- La FB de U2 se toma antes de U3. U3 en modo prioridad: MODE a VIN1.
