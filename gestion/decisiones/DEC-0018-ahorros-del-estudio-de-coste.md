---
id: DEC-0018
titulo: Ahorros del estudio de coste: se mantiene Q1 y se aplican P1–P5
fecha: 2026-11-23
estado: aceptada
decide: usuario
specs: [SPEC-0037, SPEC-0038]
requisitos: [ALI-03, ALI-04, ALI-05, ALI-07, ALI-09, FAB-06]
---

# DEC-0018 · Ahorros del estudio de coste: se mantiene Q1 y se aplican P1–P5

## Contexto

El estudio de coste del paso 6 de SPEC-0037 (`docs/diseno/estudio-coste.md`) da 47,15 $ por placa con 5 uds y 25,02 $ con 50. Con 5 uds, el 34 % es la cuota de las piezas Extended. El usuario propuso quitar Q1, y el estudio lo desaconseja: U1 solo rechaza la polaridad inversa con un N-MOSFET externo (SLVSE94G §8.3.5, pp. 20-21), y sin protección la entrada invertida pone la fuente en corto (§2.1).

## Decisión

El usuario (2026-11-23):

- **Mantiene Q1, D1 y R1** (opción A de §2.1). ALI-03 no cambia.
- **Aplica las cinco propuestas de ahorro** de §9:
  - **P1**: D1, D2 y D3 pasan a sus equivalentes preferidas de hongjiacheng (C19077412, C19077586 y C7420364), una vez la validación compare las fichas;
  - **P2**: los THT (J1, J4–J9, J10 y J3) los compra y los suelda el usuario. Quedan fuera del montaje de JLCPCB (FAB-06 lo admite);
  - **P3**: los 220 nF 100 V (C3, C8 y C27–C38) pasan a 100 nF 100 V Basic (C28233). Se acepta separarse de la Tabla 8-1 del LMR36520 en C8 y una C_VS efectiva de ≈ 85–90 nF;
  - **P4**: U4 pasa a JSMSEMI TLV1117LV33DCYR (C48937499), porque la de TI no tiene stock, después de comprobar la caída y la estabilidad con 22 µF;
  - **P5**: R15 pasa de 4,87 kΩ 0,1 % a 4,7 kΩ 1 % (C23162). El error de ALI-09 queda en 2,91 % ≤ 3 %.
- Ahorro estimado de la decisión inicial: ≈ 6,75 $ por placa con 5 uds y ≈ 1,41 $ con 50 (§9). Tras VAL-0037-01 (abajo), P1 + P2 + P3 bajan el coste a 42,02 $ con 5 uds y 24,00 $ con 50; P4, por determinar.

Tras VAL-0037-01 (2026-11-23), el usuario corrige tres de las cinco:

- **P3**: C8 sigue en 220 nF 100 V X7R. TI lo exige: «must be used», LMR36520 p. 20 (VAL-0037-01-02). C3 y C27–C38 sí pasan a 100 nF Basic (C28233).
- **P4**: el JSMSEMI C48937499 es un 1117 clásico con ≈ 1,2 V de caída, así que no vale (VAL-0037-01-01). SPEC-0038 busca un LDO de 3,3 V que cumpla ALI-07 y ALI-08 (caída con los 3,9 V del cambio de U3, estable con cerámico, patillaje de SOT-223 si puede ser), con stock en JLCPCB. Candidatos: Diodes AP2114H-3.3TRG1 (C150716) y TECH PUBLIC TPTLV1117LV33DCYR (C52146079).
- **P5 se retira**: R15 sigue en 4,87 kΩ al 0,1 %. Con la caída de F1 y Q1, el 1 % deja ALI-09 en 3,68 % (VAL-0037-01-03).
- Quedan P1, P2, P3 (sin C8) y P4 (con el LDO que salga). El ahorro se recalcula en el estudio.

Tras SPEC-0038, paso 1 (2026-11-23):

- **P4**: U4 pasa a Diodes AP2114H-3.3TRG1 (C150716), con el mismo patillaje (`alimentacion.md` §3.9).
- **P3**: C3 vuelve a 220 nF 100 V X7R (C513710, como C8). Con 100 nF, su capacidad efectiva baja a 73–80 nF, frente al «0,1 µF o más» del TPS2663 (p. 27); +0,014 $/placa. C27–C38 siguen en 100 nF (C28233); su C_VS efectiva es de 73–80 nF, no de 85–90.

## Consecuencias

- La spec que aplique los cambios en `hardware/v2` (SPEC-0038) hace lo siguiente:
  - recalcula `alimentacion.md` (U4), `salidas.md` §5 y las fichas;
  - actualiza la BOM con los THT marcados «a mano»;
  - incluye J10 BH254R-10P (DEC-0017) y los textos de 1,0 mm de JP1.
- Validación completa: se comparan las fichas de P1 y del LDO de P4 con las piezas de ahora y se reproducen las cifras de P3.
