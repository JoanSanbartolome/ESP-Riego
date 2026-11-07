---
spec: SPEC-0023
agente: ing-esquematicos
n: 01
fecha: 2026-11-07
estado: completado
---

# SPEC-0023 · 01 · ing-esquematicos

## Orden recibida

«SPEC-0023 · rama spec/SPEC-0023-calculos-salidas (se creará al terminar; ahora la carpeta está en spec/SPEC-0021-piezas-mcu, que no es tuya) · Lee: gestion/specs/SPEC-0023-calculos-salidas.md y todas sus entradas (docs/02 REL-01..10, ALI-01/12/13, FAB-03/07/09 y §6; docs/diseno/estudio-salidas.md §1.2 y §11; docs/diseno/mcu.md §9.2, §10.2 y Anexo C; docs/diseno/alimentacion.md; DEC-0003/0004/0006/0007; fichas BTT6050-1ERA, BTT6030-2ERA, WJ500V-5.08-2P y datasheets/BTT6050-1ERA.pdf; checklists requisitos.md y esquema.md v6) · Haz: el documento de selección y cálculos del bloque de salidas según el alcance de la spec, con especial cuidado en V_ADC ≤ 3,1 V en fallo de IS (REL-10) y la carga abierta en OFF con R_OL (fuga ≤ 1 mA); referencias desde U7/R26/C27/D6/J4 y nota sobre U5/U6 de estudio-salidas.md (son IDs de observaciones) · Entrega: docs/diseno/salidas.md + log gestion/logs/SPEC-0023/01-ing-esquematicos.md. Restricciones: solo texto. No uses KiCad (ni MCP ni kicad-cli) […]. Solo creas esos dos archivos nuevos; no modifiques ningún archivo existente (propón en el log los cambios a otros documentos) ni tu memoria fuera de .claude/agent-memory/ing-esquematicos/.»

Reanudación (coordinador, 2026-11-07): mismas restricciones; el corte por límite de uso llegó antes de escribir ningún archivo.

- Rama: `spec/SPEC-0021-piezas-mcu` (autorizado por el coordinador: la de SPEC-0023 se crea al terminar). Sin KiCad: no aplica la comprobación de `.lck`.

## Contexto consultado

- `gestion/specs/SPEC-0023-calculos-salidas.md`; `docs/02-especificaciones-v2.md` §4.1, §4.3, §4.6, §5, §6.
- `docs/diseno/estudio-salidas.md` §1.2, §2.5, §11; `mcu.md` §1, §9, §10, §11, §12, Anexos B y C; `alimentacion.md` §1–§2, §3.13, §4–§10, Anexo B.
- DEC-0003, 0004, 0006, 0007. Checklists `esquema.md` v6 y `requisitos.md` v3.
- Fichas BTT6050-1ERA, BTT6030-2ERA, WJ500V-5.08-2P (y KT-0603YG, bloque-alimentacion).
- BTT6050-1ERA Rev. 1.00 (local): pp. 4, 6-8, 10, 13, 15, 17, 19, 21-24, 27-28, 30-31, 33-34, 36, 43-44, 47-48 (páginas 6, 8, 10, 13, 30, 36, 43, 44 y 46 renderizadas con PyMuPDF).
- BTT6030-2ERA Rev. 1.00 (local): k_ILIS, I_IS(FAULT), V_OL(OFF), I_GND_2, E_AS.
- ESP32-S3 Series Datasheet v2.2 (espressif.com, descargado al *scratchpad*): tabla 5-4 (p. 65), tabla 5-6 (p. 66).
- API de JLCPCB `selectSmtComponentList` (2026-11-06): C534868, C534865, C8465, C25804, C25803, C21190, C14663, C513710, C381466, C2289, C2286, C95872, C17902, C25819, C17713, C23253, C23264, C57112, C107059, C98220, C14675, C22548, C132649, C114638.

## Acciones

1. Lectura de entradas y extracción del datasheet (`pdftotext` + render de tablas y curvas).
2. Cálculos en el *scratchpad* (`s23_calc.py`, scripts en línea): E_AS (ec. 5.1), térmica iterada con R_DS(on)(T), divisor de IS en fallo, R_OL, umbrales del firmware, IPC-2221.
3. Consulta de stock y tipo en JLCPCB (`s23_jlc.py`).
4. Creado `docs/diseno/salidas.md` (§0–§14, Anexos A y B).

## Decisiones y justificación

- **IS sin diodo de *clamp*:** R_SENSE 10 kΩ (1206) en serie y R_IS 820 Ω + C_IS 100 nF en el nodo del ADC. Toda I_IS pasa por la serie: transimpedancia de 820 Ω, y el divisor acota el fallo a ≤ 2,24 V a 30 V (≤ 2,76 V a 36,7 V) < VDD mín.: no entra corriente en el pin. Un Schottky a +3V3 recorta a 3,84 V (> 3,1 V). La R_IS de 1,2 kΩ en el pin (Infineon, p. 48) disiparía 0,7 W en fallo continuo (canal sin válvula con DEN común alto).
- **820 Ω (C23253, Basic) en lugar de 910 Ω (C23264, Extended):** cumple igual (§3.2); DEC-0007.
- **R_OL 47 kΩ 0805:** 0,64 mA a 30 V; 0805 por los 75 V de V_DS(AZ) en la desmagnetización (0603 = 75 V justos).
- **C_OUT 220 nF 100 V (C513710) en lugar de 10 nF:** línea existente; OUT llega a −57 V (no vale 50 V; no hay 10 nF 100 V Basic). Sin efecto en la detección (τ 10,6 ms).
- **Sin R_GND ni zéner en VS:** Q1 bloquea la polaridad inversa y V_S ≤ 53,3 V < V_S(AZ) 65 V.
- **Sin R_PD en OUT:** enmascararía la carga abierta con R_OL de 47 kΩ.
- **LED desde el GPIO IN_n** (1,5 mA, KT-0603R Basic): el LED en OUT enmascara la carga abierta (D = 18 V). Cambia mi nota anterior de memoria (transistor desde 3,3 V): con 1,5 mA, el margen de V_IN sigue siendo ≥ 0,3 V.
- **E_AS:** L estimada por τ de los solenoides AC del mismo tamaño (9–16,7 ms). Instalada (Bermad DC): 81–150 mJ a 30 V < 155 mJ. Genérica de 0,25 A: cumple solo con L ≤ 1,10 H. **D12–D17 (M7) como huella DNP**: montarlas requiere DEC (REL-03 dice «con el *clamp* integrado»).
- **C45/C46 4,7 µF** por borde: total del bus 15,4 µF = el supuesto de `alimentacion.md` §3.13.6.

## Verificación

- `python herramientas/verificar.py hardware/v2`: **no ejecutado** (la orden prohíbe KiCad y `kicad-cli`; no hay cambios en `hardware/`). ERC/DRC/paridad: sin objeto en esta spec.
- Repaso de la checklist `esquema.md` v6 (secciones que aplican a un documento de cálculos):
  - Cada valor calculado con fórmula, fuente y margen: **cumple** (§2–§6).
  - Recalculado por el revisor: **pendiente** (validación).
  - Tensión nominal ≥ peor caso del nodo con la Vc de la TVS: **cumple** (C 100 V; R_SENSE 200 V; R_OL 150 V; BTT por V_S(LD) 65 V).
  - Cerámicos con *derating*: **cumple** (C_VS/C_OUT 0,15–0,17 µF; C45/C46 ≈ 3,9 µF; C_IS a ≤ 3 V).
  - E_AS con 2 cargas y la curva E_AS(I_L): **cumple con condición** (L sin dato del fabricante; pendiente de medir, §5).
  - *Hold-up*: no aplica.
  - Disipación a 60 °C: **cumple** (BTT 77 °C a 1 A; R_SENSE ≤ 44 %; R_OL ≤ 29 mW).
  - Retroalimentación del bus apagado por IN/DEN: **cumple** (§2.3), prueba en prototipo.
  - Salidas apagadas en reset/flasheo: **cumple** (R_PD, §2.2).
  - Protección inductiva REL-03: **cumple con condición** (ver E_AS).
  - Corriente por canal/total, pistas, bornes y retornos para 4,9 A: **cumple** (§4.2, §11).
  - Térmica a 4,9 A y enclavamiento: **cumple** (§6: TSD y *latch*; firmware §12).
  - LED sin enmascarar la carga abierta: **cumple** (§7).
  - IS acotada y R_OL ≤ 1 mA: **cumple** (§3).
  - Corto en una salida (qué ven los demás y la lógica): **cumple** (§4.1).
  - Orden de pines de los bornes: **cumple** (§8); la serigrafía la comprueba el layout.
  - ESD/TVS en conectores de campo: **cumple parcialmente**: C_OUT 220 nF (recomendación del datasheet) y ESD de OUT ± 4 kV; sin TVS en OUT por la desmagnetización (§4.3). Lo valora validación.
  - Tabla de restricciones de layout: **cumple** (§11).
  - Estructura, campos de símbolos, huellas, DNP: no aplica (sin esquema); D12–D17 marcadas DNP en §9 para SPEC-0025.
- `requisitos.md` v3, «Estudios de diseño»: coste con el tramo de la cantidad real **cumple** (§9); descartes con parámetro **cumple** (§3.1, §4.4, §7); avisos de vigencia: no aplica.
- Criterios de aceptación de la spec: los 8 cubiertos (E_AS con la condición de L).

## Pendiente

- **Usuario (REL-03):** medir la inductancia de la válvula instalada antes de cerrar el esquema (método en `salidas.md` §5). Límites: ≤ 2,69 H por válvula (Bermad 156 Ω), ≤ 1,10 H (válvula de 0,25 A).
- **Coordinador, propuesta de DEC:** montar D12–D17 (M7, C95872, Basic, ≈ 0,06 $/placa) por defecto como rueda libre, para no depender de L. Cambia «con el *clamp* integrado» de REL-03. Si no, quedan DNP.
- **jr-conformidad (SPEC-0024):** confirmar C534868, C17902, C17713, C23253 y las alternativas; stock del BTT6050 (1 658).
- **Cambios propuestos a otros documentos (no los he tocado):**
  - `mcu.md` §9.2 (columna «Elemento externo» de IS1–6): «R_SENSE 10 kΩ (salidas) + R_IS 820 Ω y C_IS 100 nF junto al pin; sin diodo»; Anexo B: IS a 6 dB, I = V/820 Ω × 1500. §9.2, nota del BTT6030: basta un DSEL común (1 GPIO).
  - `alimentacion.md` §4: añadir I_GND de los BTT (≤ 6 × 9 mA = 54 mA) a la carga del bus: 3,554 A < 3,86 A ✔. §10.7 (retroalimentación del bus apagado): cerrado en `salidas.md` §2.3.
  - Ficha `WJ500V-5.08-2P.md`: «Uso» → J1 y J4–J9 en `salidas.kicad_sch`. Ficha `BTT6050-1ERA.md`: BTT6030 con la misma huella pero distinto pinout; vías del EP a BUS_24V; sin R_GND (Anexo A).
  - `estudio-salidas.md` S7: remitir a `salidas.md` §3.
  - Firmware (`firmware/`): umbrales y secuencias de `salidas.md` §12 cuando se dibuje la hoja (SPEC-0025).
- **Validación:** recalcular §3.2, §3.3, §5 y §6; pruebas de prototipo de §13 (k_ILIS con V_IS alta, V_IN con LED, bus apagado).

## Notas para el siguiente agente

- SPEC-0025: el Anexo B de `salidas.md` da etiquetas, redes internas y conexiones por canal con las referencias. R_IS/C_IS van en la hoja de salidas, pero el layout los coloca junto al módulo (§11).
- El *tab* VS del BTT es BUS_24V: sus vías térmicas no van al plano GND.
- Los umbrales del firmware dependen de R_IS = 820 Ω y R_SENSE = 10 kΩ: si cambian, rehacer §3.2 y §12.
