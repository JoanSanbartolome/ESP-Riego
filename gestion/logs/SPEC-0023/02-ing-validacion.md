---
spec: SPEC-0023
agente: ing-validacion
n: 02
fecha: 2026-11-07
estado: completado
---

# SPEC-0023 · 02 · ing-validacion

## Orden recibida

«SPEC-0023 · rama spec/SPEC-0023-calculos-salidas (activa; commit revisado 992812c) · Nivel: completo · Lee: gestion/specs/SPEC-0023-calculos-salidas.md + docs/diseno/salidas.md + gestion/logs/SPEC-0023/01-ing-esquematicos.md + sus entradas (docs/02 REL-01..10, ALI-01/12/13, FAB-03/07/09 y §6; estudio-salidas.md §1.2 y §11; mcu.md §9.2, §10.2 y Anexo C; alimentacion.md; DEC-0003/0004/0006/0007; hardware/componentes/datasheets/BTT6050-1ERA.pdf) + checklists requisitos.md y esquema.md (v6) · Haz: validar cada criterio recalculando de forma independiente contra el datasheet, con atención especial a (1) REL-10 IS: V_ADC ≤ 3,1 V en todos los fallos (I_IS(FAULT) máx., V_IS hasta V_S − 1 V, BUS_24V en el peor caso, tolerancias de R_IS 820 Ω / R_SENSE 10 kΩ) y la corriente hacia el pin del ESP32-S3, y que el rango de medida útil y la atenuación del ADC sean coherentes; (2) carga abierta en OFF con R_OL 47 kΩ: fuga ≤ 1 mA, la válvula no se activa, margen frente al umbral del datasheet con 1–2 válvulas y con JP1 cerrado; (3) R_PD/R_IN/R_DEN frente a mcu.md §10.2; (4) E_AS con 2 válvulas y la inductancia supuesta, y la propuesta de D12–D17 DNP; (5) T_J; (6) referencias sin choque con alimentación y MCU y la nota de U5/U6 · Entrega: gestion/informes/VAL-0023-01.md + log gestion/logs/SPEC-0023/02-ing-validacion.md. No uses el MCP de KiCad.»

## Contexto consultado

- Rama `spec/SPEC-0023-calculos-salidas`, HEAD 992812c.
- Spec, `salidas.md`, `docs/02` v0.4, `estudio-salidas.md` (l. 19-35, §1.2), `mcu.md` §1, §7-§11 y Anexo C, `alimentacion.md` §3.13, §4, §7 y §8, DEC-0007, checklists `esquema.md` v6 y `requisitos.md` v3.
- BTT6050-1ERA Rev. 1.00: pp. 4, 6-8, 10, 13, 15, 22-31, 34, 43-44 y 47-48.
- Huellas: `esp-riego:Infineon_PG-TDSO-14…`; KiCad 10 `R_0805`, `C_0805` y `R_1206`. Símbolo `esp-riego:BTT6050-1ERA`.
- LCSC JSON: C534868, C17713, C17902, C23253, C95872.

## Acciones

1. Extracción del datasheet por página (`pdftotext` + PyMuPDF) en el *scratchpad* de la sesión.
2. Recalculado: divisor y tabla de fallo de IS, rango normal con k_ILIS, R_OL (fuga, detección, JP1), E_AS = 540·L/R² a 30 V (331·L/R² a 24 V), T_J, IPC-2221 y umbrales del firmware.
3. Comprobación de los huecos entre pads frente a FAB-03, de las referencias y de los LCSC.
4. Lectura del log del autor al final: sin afirmaciones que contradigan los artefactos.
5. Escrito `gestion/informes/VAL-0023-01.md`.

## Decisiones y justificación

- No se ejecuta `verificar.py`: el commit no toca archivos de KiCad, y la orden excluye el MCP.
- «Cumple parcialmente» del autor en ESD de los conectores de campo: se acepta. C_OUT de 220 nF absorbe una descarga IEC de 8 kV / 150 pF con ΔV ≈ 5,5 V, y Infineon (p. 47-48) no pone TVS.

## Verificación

- Veredicto: APROBADO_CON_OBSERVACIONES (2 M, 4 B).
- M-01: separación de `Salidas` (1 mm) imposible en los pads del BTT (0,62-0,735 mm), R_OL 0805 (0,80 mm) y C_OUT 0805 (0,90 mm).
- M-02: carga mínima de una válvula sin calentamiento de la bobina (R = 133 Ω < 156 Ω); con la bobina caliente, el umbral de 25 mV de carga abierta en ON tiene margen ≤ 0.

## Pendiente

- Autor: M-01 (excepción de separación en §11) y M-02 (fila de carga mínima y umbral de §12) antes de la spec que los use (layout y firmware); B-03…B-06 a mantenimiento.
- Usuario: medir L antes de cerrar el esquema (REL-03).

## Notas para el siguiente agente

- Cifras propias para contrastar: divisor de fallo 0,0744–0,0772; V_ADC ≤ 2,24 V (V_S − 1) o 2,32 V (V_S) a 30 V; E_Bermad = 80,5 / 149 mJ; L máx. 2,70 H (Bermad) y 1,10 H (0,25 A).
