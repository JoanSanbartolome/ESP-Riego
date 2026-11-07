---
spec: SPEC-0021
agente: ing-validacion
n: 02
fecha: 2026-11-07
estado: completado
---

# SPEC-0021 · 02 · ing-validacion

## Orden recibida

SPEC-0021 · rama spec/SPEC-0021-piezas-mcu (activa; commit revisado 73af0ee) · Nivel: completo · Lee: gestion/specs/SPEC-0021-piezas-mcu.md + gestion/logs/SPEC-0021/01-jr-conformidad.md (sección «Requiere verificación») + docs/diseno/mcu.md §11/Anexo A + checklists librerias.md (v3) y esquema.md (v6, punto FAB-02) + DEC-0007 · Haz: validar los criterios de la spec contra los entregables y los datasheets: 3D del TS-1187A (alineación y pin 1, supuestos de altura), huella esp-riego:ESP32-S3-WROOM-1 (solo cambian las 12 vías a 0,3/0,6, keepout de antena en todas las capas, 3D), copias de huella del pulsador y del HRO, taladro de J3 (1,0 mm frente a diagonal 0,93 mm), fichas nuevas y actualizadas, tipo Basic/Extended y stock con fecha por muestreo, tabla de campos para SPEC-0022. Valora también las tres propuestas DEC-0007 del log (C23→C15849, USBLC6 UMW, D5 rojo Basic) como observaciones · Entrega: gestion/informes/VAL-0021-01.md + log gestion/logs/SPEC-0021/02-ing-validacion.md.

Se reanudó el 2026-11-07, tras un corte por límite de uso.

## Contexto consultado

- Spec, DEC-0007, `mcu.md` §2–§7, §11, §12 y Anexo A, `alimentacion.md` §3.11, `docs/02` (MCU-01–07, FAB-02, FAB-11, KIC-01).
- Datasheets locales: TS-1187A (hoja única), KT-0603YG (pp. 2-3, rotulado XL-0603QYGC), B-2100S04P-A110 (hoja única), WROOM-1 v1.8 (pp. 11, 41 y 45), USBLC6-2SC6 (p. 1), TYPE-C-31-M-12 (hoja única).
- API de JLCPCB y SimSurfing (CL10A105KB8NNN), consultadas el 2026-11-07.

## Acciones

1. Rama y HEAD comprobados (73af0ee, sin commits nuevos durante la revisión).
2. `diff` de las 3 huellas frente a las oficiales de KiCad 10.0.6.
3. Placas de prueba en `scratchpad\v21\hw*` con el `.kicad_pro` de v2:
   - DRC (copia del WROOM: 0 errores de taladro; la oficial, 12);
   - Gerber de máscara y pasta;
   - render superior y frontal.
4. Caja y niveles z del STEP del TS-1187A; alzado del PDF renderizado.
5. Pines↔pads por script y frente al datasheet: WROOM, USBLC6, HRO, TS-1187A y LED.
6. `verificar.py hardware/v2`: ERC 0, DRC 0 (108 sin conectar), paridad 0; `.kicad_prl` intacto.
7. API de JLCPCB: 15 códigos por muestreo; tipo igual en todos y stock dentro de ±9 %.
8. Log 01 leído al final para contrastarlo con los artefactos.

## Decisiones y justificación

- 2 M:
  - -01: polaridad del LED ambigua en la ficha;
  - -02: tabla de campos con marcadores en `Datasheet`.
- 6 B: pasta del EPAD frente a las vías de 0,3, escalón del 3D, taladro de J3, URL de los datasheets, pines↔pads citados solo para el WROOM y fecha de la ficha del USB-C.
- Propuestas DEC-0007:
  - C15849: se puede aplicar (τ 7,16 ms; EN/VDD 0,159);
  - UMW: hace falta comparar su datasheet;
  - D5 rojo: es un cambio de diseño, lo decide el usuario.

## Verificación

Informe `gestion/informes/VAL-0021-01.md`: APROBADO_CON_OBSERVACIONES. MCP no usado.

## Pendiente

- Coordinador: corregir -02 antes del merge (lo usa SPEC-0022); -01 conviene corregirlo ya. El resto, a la spec de mantenimiento.
- Decisiones de DEC-0007: C23 (recalcular §5.1 en `mcu.md`), U6 y D5.

## Notas para el siguiente agente

- Las huellas con EP llevan la pasta en pads `""` solo de F.Paste: al cambiar los taladros, medir la distancia a esas aperturas.
