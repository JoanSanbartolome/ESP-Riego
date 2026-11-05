---
spec: SPEC-0018
agente: jr-conformidad
n: 05
fecha: 2026-11-05
estado: completado
---

# SPEC-0018 · 05 · jr-conformidad

## Orden
Alinear `hardware/componentes/bloque-alimentacion.md` con `docs/diseno/alimentacion.md` (§3.5, §3.6, §7). Solo texto.

## Acciones
- §2 (pasivos; la orden lo llama §1): + C22 en la línea C381466; C3 a la fila de C8 (220 nF 0805 C513710); C10 → C28323 (Basic, 3 504 368; LCSC 0); C15 queda en C15849.
- Recuento: Extended 20 → 19 (sale C15725), Basic 9 → 10.
- §3 tabla de derating: C3 (100 nF) eliminada y unida a C8; C10 con fila propia (CL21B105KBFNNN, SimSurfing según alimentacion.md §3.6); C22 en la fila de C2/C6/C7; C15 sola.
- §3 puntos 3–5 reescritos como resueltos.
- Cifras copiadas de alimentacion.md; no consultadas de nuevo.

## Verificación
- Sin KiCad: verificar.py no aplica.
- Checklist librerías: sin piezas ni librerías nuevas; no aplica.

## Pendiente
- Campos de C22, C3 y C10 en el esquema: SPEC-0019.
- alimentacion.md §7 conserva C8 en 72 260 y C3 en 72 240 (stock LCSC); no se tocó.
- Sin ficha para C28323 (pasivo; consistente con el resto).

## Requiere verificación de validación
Ninguna pieza creada ni modificada.
