---
spec: SPEC-0017
agente: ing-esquematicos
n: 02
fecha: 2026-11-05
estado: completado
---

# SPEC-0017 · 02 · ing-esquematicos

## Orden recibida

SPEC-0017 · rama spec/SPEC-0017-calculos-alimentacion · Lee: gestion/decisiones/DEC-0006-uvlo-y-puente-del-limitador.md · Haz: en docs/diseno/alimentacion.md, (1) marca el UVLO y el coste como decididos por DEC-0006; (2) añade el puente de soldadura de VIN_PROT a BUS_24V en paralelo con U1: huella (oficial `Jumper:SolderJumper_2_Open` u otra), tamaño de los pads y cálculo para 4,9 A con estaño; posición por defecto abierto; qué funciones se pierden con el puente cerrado; añádelo a la lista de piezas y al Anexo A. Las fichas siguen sin crearse (las crea SPEC-0018) · Entrega: alimentacion.md + log 02-ing-esquematicos.md. Brevedad: la respuesta final, solo el contrato de salida.

## Contexto consultado

- DEC-0006.
- KiCad 10: `Jumper.pretty` (SolderJumper-2_P1.3mm_*: pads de 1,0 × 1,5 mm, hueco 0,3 mm, F.Cu y F.Mask sin pasta) y el símbolo `Jumper:SolderJumper_2_Open`.

## Acciones

- `docs/diseno/alimentacion.md`:
  - cabecera con DEC-0006;
  - §0: tabla y resultados;
  - §3.7: UVLO decidido;
  - §7: coste aceptado; JP1 en la lista y en la lista de piezas nuevas;
  - §8: fila de JP1;
  - §9: trazabilidad de ALI-13;
  - §10.1: cerrado;
  - nueva §3.13.9 (puente);
  - Anexo A: JP1;
  - Anexo B: opción «sin limitador».

## Decisiones y justificación

- Se descarta la huella oficial: pads de 1,5 mm, por debajo de los 2,0 mm de `Power_In`; el estaño equivale a ≈ 1,1 mm de pista.
- Huella nueva `esp-riego:SolderJumper-2_P1.6mm_Open_Pad1.2x3.0mm`:
  - pads de 1,2 × 3,0 mm y hueco de 0,4 mm;
  - sin pasta y con máscara común.
- 4,9 A:
  - cobre de 3,0 mm ≥ 2,84 mm (IPC-2221, ΔT 10 °C);
  - estaño de 0,6 mm² → 0,09 mΩ y 2,1 mW; equivale a 0,078 mm² de cobre, frente a 0,070 mm² de la pista de 2,0 mm.
- Con JP1 cerrado se pierden ALI-13, REL-08 (la lógica puede reiniciarse), el corte general, FLT, IMON, el *clamp* a 35 V y dVdT. REL-04 se mantiene por los IN de los *high-side*.

## Verificación

- Sin cambios en KiCad; `verificar.py` del log 01: LIMPIO.
- Repaso de la checklist de esquema (v5), puntos afectados:
  - escalones de protección: sin JP1 cambia el escalón y queda documentado;
  - tabla de layout: actualizada.

## Pendiente

- SPEC-0018: huella nueva de JP1 y las fichas del log 01.
- Spec de mantenimiento: texto de ALI-06 (DEC-0006).
- SPEC-0019: serigrafía de JP1 y README de `hardware/v2`.

## Notas para el siguiente agente

- JP1: pad 1 a VIN_PROT y pad 2 a BUS_24V, junto a U1. Sin pieza (fuera de BOM y CPL).
