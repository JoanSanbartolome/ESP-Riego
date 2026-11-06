---
spec: SPEC-0019
agente: jr-conformidad
n: 02
fecha: 2026-11-06
estado: completado
---

# SPEC-0019 · 02 · jr-conformidad

## Orden
Poner al día `bloque-alimentacion.md` (DEC-0007) y comprobar los `LCSC Part#` de `alimentacion.kicad_sch` frente a `alimentacion.md` §7. Sin MCP ni kicad-cli; esquema solo leído (Grep).

## Acciones
- `hardware/componentes/bloque-alimentacion.md`: R8 → Yageo RT0603BRD0724K9L C136967 (Extended, 14 042); C5, C9, C13, C14, C20, C21 → Yageo CC0603KRX7R9BB104 C14663 (Basic, 34 750 639; JLCPCB 2026-11-06, datos del log 01); propuestas convertidas en «aplicados».
- Recuento: Extended 19 → 18 (sale C1591; C4156365 → C136967 no cambia la cuenta); Basic 10 → 11 (entra C14663). Total 29 líneas. Contado a mano con la lista de la ficha.

## Comprobación de campos LCSC (hoja vs §7)
- 55 piezas leídas. Coinciden todas: J1 C8465, F1 C44479, Q1 C3281500, D1 C173427, D2 C224019, D3 C15874, D4 C2286, U1 C1850278, U2 C1858395, U3 C3235557, U4 C15578, L1 C475521; R1/R9/R12 C25803, R2 C23159, R3–R6/R10 C25804, R7/R14 C122538, R8 C136967, R11 C23137, R13 C21190, R15 C855888; C1 C165628, C2/C6/C7/C22 C381466, C3/C8 C513710, C4 C21122, C5/C9/C13/C14/C20/C21 C14663, C10 C28323, C11/C12/C16/C17 C12891, C15 C15849, C18/C19 C19702.
- JP1 y TP1–TP5: LCSC vacío (correcto, sin pieza).
- **Discrepancias: ninguna.** No se comprobaron MPN, Datasheet ni Description (fuera de la orden).

## Checklist `librerias.md`
No aplica: no se crean ni modifican símbolos, huellas ni modelos. Sin piezas para «Requiere verificación de validación».

## Verificación
No aplica (no se tocó ningún proyecto KiCad).

## Pendiente
- Stock de C14663 y C136967 es de JLCPCB (LCSC 0 en C14663): confirmar al pedir.
