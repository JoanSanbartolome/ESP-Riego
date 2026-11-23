---
id: DEC-0017
titulo: Conector de expansión J10 horizontal, al ras del borde inferior
fecha: 2026-11-20
estado: aceptada
decide: usuario
specs: [SPEC-0037]
requisitos: [EXP-03, FAB-07]
---

# DEC-0017 · Conector de expansión J10 horizontal, al ras del borde inferior

## Contexto

En la colocación del paso 5 de SPEC-0037 (`colocacion-b3.csv`), J10 (BH254V-10P, IDC 2 × 5 de 2,54 mm, vertical) está en el borde inferior a 2,5 mm del borde (DEC-0016), y la clavija entra de arriba abajo: el cable sale perpendicular a la placa y su altura (9,05 mm) obliga a apartar pulsadores y LED (reglas P05, E08 y L01).

## Opciones consideradas

1. Mantener J10 vertical.
2. J10 en ángulo recto (horizontal), con la clavija entrando por el borde inferior de la placa y el conector al ras de ese borde.

## Decisión

El usuario elige la 2 (2026-11-20): J10 horizontal, con la conexión por el borde inferior de la placa y el conector al ras del borde, como J2. Es una excepción más a los 2,5 mm de DEC-0016. Mismo número de pines y mismo pinout; la pieza (con guía y, si la hay en JLCPCB, de tipo básica o preferente) la propone `ing-diseno` en SPEC-0037, paso 6.

## Consecuencias

- `colocacion-reglas.csv`: J10 pasa a `ras` en el borde inferior, con la boca hacia fuera; las reglas de altura (P05, E08 y L01) se recalculan con la altura de la pieza nueva.
- Si JLCPCB pide bordes auxiliares por J10 al ras, cuenta junto con J2 y U5 (regla R01).
- El cambio de símbolo, huella y BOM en `hardware/v2` va en la spec que aplique los cambios del estudio de coste.
