---
id: DEC-0006
titulo: UVLO a 13,5 V y limitador TPS26632 con puente de soldadura
fecha: 2026-11-05
estado: aceptada
decide: usuario
specs: [SPEC-0017, SPEC-0018, SPEC-0019]
requisitos: [ALI-06, ALI-12, ALI-13, REL-04, REL-08]
---

# DEC-0006 · UVLO a 13,5 V y limitador TPS26632 con puente de soldadura

## Contexto

SPEC-0017 (`docs/diseno/alimentacion.md` §3.7 y §3.13) deja dos puntos al usuario:

- **UVLO:** el arranque queda a 13,5 V nominales, no en los ≈ 15 V orientativos de ALI-06. Con ≈ 15 V no se cumpliría la bajada ≤ 15,5 V, que es M.
- **Coste:** el TPS26632 cuesta 3,56 $ por placa en tandas de 5, por encima de los 2–3 $ de DEC-0003. No hay alternativa más barata con las mismas funciones: el LM5069 con NFET sale por ≈ 4,5 $ y el TPS26633 por 6,9 $, con un stock de 11.

## Decisión

1. **UVLO:** divisor de 100 kΩ / 10 kΩ, con el arranque a 13,5 V nominales (12,50–14,56 V). El ≈ 15 V de ALI-06 era orientativo; la cifra se corrige en la spec de mantenimiento de la fase.
2. **Limitador:** TPS26632RGER, con un **puente de soldadura de IN a OUT** (de `VIN_PROT` a `BUS_24V`). Se cierra con una gota de estaño si U1 no se monta o falla.

## Consecuencias

- El puente aguanta la corriente máxima del bus, 4,9 A (ALI-13), con el estaño. Su huella y su anchura las fija SPEC-0017 y las crea SPEC-0018.
- Por defecto el puente va **abierto**, con U1 montado. Cerrado, se pierden:
  - la protección común ante cortos (ALI-13, REL-08), que pasa a depender de la fuente y de cada BTT;
  - el corte general y la IMON.
  REL-04 se sigue cumpliendo en cada salida gracias al *pull-down* de su IN. Todo esto se indica en la serigrafía y en el README.
- Coste aceptado: el bloque sale por ≈ 8,9 $ por placa en tandas de 5.
