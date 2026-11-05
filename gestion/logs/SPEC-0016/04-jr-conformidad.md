---
spec: SPEC-0016
agente: jr-conformidad
n: 04
fecha: 2026-11-05
estado: completado
---

# SPEC-0016 · 04 · jr-conformidad

## Orden recibida

Corregir VAL-0016-01-01 (M), -02 y -03 (B).

## Acciones

| Hallazgo | Estado | Dónde |
|---|---|---|
| 01 (M) nombres OUT solapan | Corregida: nombres acortados a «OUT 10-12», «OUT0 12-14», «OUT1 8-10» y cuerpo ensanchado 5,08 mm (rectángulo a x = 12,7; pines de la derecha a x = 15,24, en ambos símbolos; BSP752R sin tocar). Números, tipos y filas sin cambio. Comprobado con `sym export svg` + captura de Edge de cada símbolo: ningún nombre pisa a otro | `hardware/libraries/esp-riego.kicad_sym` |
| 02 (B) pad 1 en la marca de pin 1 | Corregida: -2,73 | `INFORME.md` l. 57 |
| 03 (B) filas 14 y 15 pegadas | Corregida: fila 15 (EP) separada | `INFORME.md` §2 |

## Requiere verificación de validación

| Pieza | Qué es | Datasheet y página |
|---|---|---|
| Símbolos `BTT6050-1ERA`, `BTT6030-2ERA` | Nombres de los pines OUT y ancho del cuerpo (los pines de la derecha pasan a x = 15,24) | BTT6050-1ERA Rev 1.00 y BTT6030-2ERA, §3.2 Tabla 2, p. 4 |

## Verificación

- `verificar.py hardware/v2`: ERC 0 · DRC 0 · paridad 0 · LIMPIO.
- Checklist `librerias.md` (propuesta de VAL-0016-01: renderizar tras cambiar nombres de pin): hecho. Resto no aplica.
