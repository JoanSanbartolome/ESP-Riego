---
id: SPEC-0017
titulo: Selección y cálculos del bloque de alimentación
fase: 2
estado: cerrada
responsable: ing-esquematicos
revisor: ing-validacion
rama: spec/SPEC-0017-calculos-alimentacion
requisitos: [ALI-01, ALI-02, ALI-03, ALI-04, ALI-05, ALI-06, ALI-07, ALI-08, ALI-09, ALI-10, ALI-11, ALI-12, ALI-13]
depende_de: []
creada: 2026-11-05
cerrada: 2026-11-05
validacion: VAL-0017-02
---

# SPEC-0017 · Selección y cálculos del bloque de alimentación

## Objetivo

`docs/diseno/alimentacion.md` fija cada pieza del bloque de entrada y limitador con su valor y su cálculo, de modo que SPEC-0018 pueda crear las piezas y SPEC-0019 dibujar la hoja sin decidir nada.

## Alcance

- Incluye:
  - selección justificada (datasheet con página, LCSC y stock) y cálculos de: borne de entrada (ALI-02), TVS (ALI-04), protección de polaridad (ALI-03), buck de 5 V con UVLO e histéresis (ALI-05, ALI-06), raíl de 3,3 V (ALI-07), unión del USB-C al raíl de 5 V (ALI-08), divisor de VIN al ADC1 (ALI-09), LED (ALI-10), test points (ALI-11) y limitador común del bus de salidas con su banda, habilitación por GPIO con *pull-down* e IMON (ALI-12, ALI-13, REL-04, DEC-0003, DEC-0004);
  - presupuesto de potencia por raíl (24 V, 5 V, 3,3 V) con las 6 salidas activas;
  - lista de piezas del bloque (referencia, valor, encapsulado, LCSC) e indicación de cuáles necesitan símbolo o huella nuevos;
  - pines del MCU que pide el bloque (ADC1 de VIN, habilitación e IMON del limitador), como propuesta para el bloque MCU.
- Excluye:
  - crear símbolos, huellas o editar KiCad;
  - cambiar requisitos: una cifra que no cuadre con `docs/02` se propone al coordinador.

## Entradas

- `docs/02-especificaciones-v2.md` (ALI-01…ALI-13, REL-04, REL-08, §6).
- `gestion/decisiones/DEC-0003-salidas-high-side-y-limitador.md` y `DEC-0004-fuente-led-y-carga-maxima.md`.
- `docs/diseno/estudio-salidas.md` (S2–S4: limitador).
- Fichas `hardware/componentes/` (LM5069, TPS2663, SMBJ33A, TYPE-C-31-M-12, USBLC6-2SC6, WJ500V-5.08-2P) y `datasheets/`.
- `hardware/v2/alimentacion.kicad_sch` (v1, solo lectura, como referencia).
- Checklists `gestion/checklists/requisitos.md` y `esquema.md` (sección «Cálculos»).

## Entregables

- `docs/diseno/alimentacion.md`.
- Datos de las fichas nuevas en un anexo de `docs/diseno/alimentacion.md` (las fichas las crea jr-conformidad en SPEC-0018).
- Log `gestion/logs/SPEC-0017/01-ing-esquematicos.md` con el repaso de checklist.

## Criterios de aceptación

- [x] Cada requisito ALI-01…ALI-13 tiene en el documento la pieza o el cálculo que lo cumple, con la condición de partida de cada cifra (tensión, temperatura, tolerancia).
- [x] UVLO: arranque en frío desde 17 V y funcionamiento hasta 15,5 V con las tolerancias del divisor y de la referencia (ALI-06).
- [x] Tensión nominal de cada pieza del nodo de entrada ≥ Vc máx de la TVS + 10 % (ALI-05).
- [x] Banda del limitador dentro de 3,5–4,9 A con sus tolerancias; buck alimentado antes del limitador (DEC-0004, S2/S4).
- [x] Medida de VIN ≤ ± 3 % en todo el rango (ALI-09).
- [x] Presupuesto de potencia por raíl con margen frente a la corriente nominal de cada regulador.
- [x] Lista de piezas con LCSC y stock, y marca de las que necesitan pieza nueva.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-05 | coordinador | Crea la spec (propuesta) | |
| 2026-11-05 | coordinador | Abre la spec (aprobada por el usuario) | |
| 2026-11-05 | coordinador | Fichas pasan a SPEC-0018 (zona de jr-conformidad) | |
| 2026-11-05 | coordinador | Cierra la spec; M de VAL-0017-02 corregida y comprobada con Grep | VAL-0017-02 (APROBADO_CON_OBSERVACIONES) |
