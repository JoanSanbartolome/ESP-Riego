---
spec: SPEC-0032
agente: ing-diseno
n: 01
fecha: 2026-11-19
estado: completado
---

# SPEC-0032 · 01 · ing-diseno

## Hecho

- `hardware/v2/esp-riego.kicad_sch`: raíz con el estilo de DEC-0015 (hojas cableadas, un recuadro con título, nombre de cada red sobre su cable, cifras junto a las hojas y nota de 3 líneas). Mismo orden de hojas y páginas (Id 1–12). Imagen: `C:\Users\josan\AppData\Local\Temp\claude\2c54f79e79dd3002\ad4da10c-a29b-4ee4-bc81-7ee404e64af6\scratchpad\entrega\s32-raiz.png` (zona derecha: `…\entrega\s32-raiz-derecha.png`).
- `herramientas/kicad/hoja.py`: `generar` escribe también la raíz (instancia «/» y `sheet_instances` con la página 1); `README.md` al día.
- `docs/diseno/arquitectura.md`: diagrama de bloques, presupuesto por raíl, tabla de GPIO sacada de la netlist y revisión global con su evidencia.
- `docs/diseno/alimentacion.md` §3.2: I²t del TA10 igual que en la ficha (VAL-0028-01-05).
- VAL-0028-01-01 y -02: parche `…\scratchpad\entrega\s32-test_kicad.patch` (archivo entero: `…\entrega\s32-test_kicad.py`).

## Decisiones y desviaciones

- Etiqueta local sobre cada cable de la raíz: sin ella, KiCad renombra las 26 redes entre hojas (`/VBUS` → `/Alimentacion/VBUS`, 126 pines) y la PCB cambiaría. Con ella la netlist es idéntica también por nombre (la checklist v16 lo admite).
- El cable de SDA a Sensores cruza el de SCL sin unión. Con tres hojas en un bus de dos hilos y los pines en un solo lado, un cruce es inevitable.
- Las hojas siguen en el orden de `main`: así no se renumeran las páginas ni se rompe `test_paginas_en_orden_del_arbol`.
- La revisión global no cambia el circuito: netlist igual y PCB sin tocar. Huellas que cambian frente a `main`: ninguna.

## Verificación

- `verificar.py hardware/v2`: ERC 0, DRC 0 (448 sin conectar, placa sin rutar), paridad 0; puntos `[auto]`: 23 OK, 0 fallan, 2 N/A. `campos.py revisar`: 0/0/0, sin DNP. `hoja.py paginas`: código 0. Netlist frente a `main`, por grupos y por nombre: 0 diferencias.
- Batería completa en un repositorio falso, con el parche, el `hoja.py` nuevo y la raíz nueva: 54 OK. Mutaciones: sin el `sorted` de `jlc.resultados`, falla `Jlc.test_resultados_y_buscar`; sin `Path(real).is_file()` en `modelo_de_respaldo`, falla `Comun.test_modelo_de_respaldo`.
- Checklist `[juicio]`: «Pinout coherente con el YAML» no aplica, porque no existe `firmware/`; la tabla de GPIO de `arquitectura.md` §3 es su base.

## Para validación

- Presupuesto de 3,3 V, cargas que antes no estaban: TCA9554 ≤ 0,6 mA (p. 7, V_I = GND) y TPS2553 ≤ 0,13/0,15 mA (SLVS841G p. 6).
- η del buck del 88 % a 0,75 A: es una estimación a partir del 90 % típico a 1 A (LMR p. 1), la misma que en `alimentacion.md` §4.
- Observación sin cambio de circuito: SW3–SW8 no llevan ESD (TCA ± 2 kV HBM); en el layout, lejos de las pistas (`arquitectura.md` §4.6).

## Pendiente

- Coordinador: aplicar el parche a `herramientas/pruebas/test_kicad.py`. Además de -01 y -02, reescribe `Hoja.test_raiz`: la raíz ya no tiene etiquetas en los pines, así que la prueba la regenera sin cables con `hoja.py generar` y prueba `raiz` sobre ella. Sin el parche, `test_raiz` falla con la raíz nueva.
- jr-conformidad (paso 2): BOM, PDF y VAL-0028-01-03 y -04.
