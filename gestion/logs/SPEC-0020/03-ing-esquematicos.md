---
spec: SPEC-0020
agente: ing-esquematicos
n: 03
fecha: 2026-11-06
estado: completado
---

# SPEC-0020 · 03 · ing-esquematicos

## Orden recibida

Corregir `docs/diseno/mcu.md` según VAL-0020-01 (01–07) y DEC-0007; unificar VBUS en `alimentacion.md` §8. Solo texto, sin KiCad.

## Contexto consultado

- `gestion/informes/VAL-0020-01.md`, `gestion/decisiones/DEC-0007-*.md`, `docs/diseno/alimentacion.md`, `gestion/logs/SPEC-0020/01-*.md`.
- `hardware/v2/*.kicad_sch`: sin refs de piezas (solo H1–H4); la referencia es `alimentacion.md`.

## Acciones

- **01 Renumeración:** mayores refs de `alimentacion.md`: C22, R15, D4, J1, U4, JP1, TP5, L1, Q1, F1. R16–R25, D5, J2–J3, U5–U6 y SW1–SW2 no chocan. Condensadores del MCU: EN C22→**C23**, 22 µF C23→**C24**, 100 nF C24→**C25**, VBUS C25→**C26**. Aplicado en `mcu.md` (cabecera, §4, §5, §8, §11, §12, §13, §14) y en el log 01 (notas).
- **02:** V_CL del USBLC6 = 12 V a 1 A y 17 V a 5 A (§4).
- **03:** §8.1: 22 × 0,677 × 0,965 × 0,8 = 11,5 µF (SimSurfing, ±20 %). §5.1: τ mín. = 10 k × 0,99 × 1 µF × 0,90 × 0,85 × 0,97 = 7,35 ms. Tabla de EN recalculada (modelo del log 01, reproduce el original): buck de 6 ms, 0,155; buck de 3 ms, 0,081; rampa lineal, 0,294 (cota no física); fila del TPS2116 escalada por 1/τ (≈ 0,10). Resumen y trazabilidad: ≤ 0,16·VDD.
- **04:** 15 mm a buck, *high-side*, USB, UART y SHT4x pasa a objetivo del autor (la HDG lo da solo dentro de la caja); el *floorplan* puede justificar menos (§3, §12, §13).
- **05:** DEN común fijado por DEC-0007 (§0, §9.2, §9.3 descartada, §14.1). §14.7 cerrado. C25 (100 nF) → Yageo CC0603KRX7R9BB104 C14663 (Basic; alternativa C1591). Log 01 a `completado`.
- **06:** VBUS 0,75 A / 0,6 mm en `alimentacion.md` §8 (ya estaba así en `mcu.md` §12); referencia cruzada en ambas.
- **07:** «decisión D5 (caja)» frente a D5 (LED) en §3, §12, §14.5 y nota en §11.

## Decisiones y justificación

- Fila del TPS2116 en la tabla de EN: sin modelo de su rampa, se escala por 1/τ y se marca como estimación; el caso del buck domina.
- LCSC de C14663: 0 en stock hoy (VAL); Basic en JLCPCB según SPEC-0018. Lo confirma jr-conformidad.

## Verificación

- Grep: sin refs C22/C23/C24/C25 antiguas del MCU en `mcu.md` ni en el log 01 (cada una usada solo con el nuevo significado); `docs/`, `gestion/specs` y `hardware/componentes` no citan las refs del MCU.
- `verificar.py`, ERC/DRC/paridad: no aplican (sin cambios en KiCad).
- Checklist `esquema.md` v5 («Cálculos», «Entregables para layout»): cumple; sin choques de refs entre `mcu.md` y `alimentacion.md`; VBUS igual en las dos tablas.

## Pendiente

- jr-conformidad (SPEC-0021): Basic y stock en JLCPCB de C14663 (C25 del MCU).
- SPEC-0019/0021/0022: usar C23–C26 del MCU. `estudio-salidas.md` usa U5/U6/D6/D8/Q2: revisar choques con el MCU (U5/U6) al anotar.

## Notas para el siguiente agente

- Refs del MCU: U5, U6, J2, J3, SW1, SW2, D5 (LED), R16–R25, C23 (EN 1 µF), C24 (22 µF), C25 (100 nF), C26 (VBUS).
