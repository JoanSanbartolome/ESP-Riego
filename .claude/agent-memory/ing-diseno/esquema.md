---
name: esquema
description: Comportamiento de KiCad 10 y de hoja.py/esquema.cruces en esquemas: etiquetas, campos girados, raíz, uniones, estilo y pruebas
metadata:
  type: reference
---

- Una etiqueta local y una jerárquica con el mismo nombre en la misma hoja se unen. Por qué: cambia la red sin que el ERC avise (comprobado con la netlist). Fuente: SPEC-0019.
- Pin de hoja sin destino: `pin_not_connected`; con una etiqueta local, `label_dangling`; con una marca de no conexión, ERC 0. Por qué: son errores, no avisos. Fuente: SPEC-0019.
- Campos de un símbolo girado: el ángulo es relativo al símbolo, (360 − giro) % 360 para leerse horizontal; con `pos` de `hoja.py`, giro 90/270 → ángulo 270/90, y giro 180 → ángulo 0 con el `justify` invertido. Por qué: si no, el campo sale vertical o al otro lado. Fuente: SPEC-0019, SPEC-0022, SPEC-0035.
- Pines de hoja en la raíz: ángulo 0 (borde derecho) con `justify right` y 180 con `justify left`. Por qué: al revés el nombre sale fuera de la caja (330 de 480 casos en las demos de KiCad). Fuente: SPEC-0022.
- Pasar una etiqueta a cable o unir hojas con etiquetas en la raíz cambia el nombre de la red (`/Alimentacion/VBUS` ↔ `/VBUS`): una etiqueta local por red sobre su cable lo conserva, y se comprueba con `hoja.py netlist` sin `--grupos`. Por qué: la paridad da `net_conflict`. Fuente: SPEC-0022, SPEC-0032, SPEC-0035.
- En la raíz se conserva el orden de los `(sheet` (lo sigue `hoja.py paginas`), y `Hoja.test_raiz` depende de las coordenadas de sus pines: si se mueven, se parchea la prueba. Por qué: fallan `test_paginas_en_orden_del_arbol` y `test_raiz`. Fuente: SPEC-0032.
- Al mover piezas en una hoja con cables se mueven también sus `uniones` del JSON de `extraer`. Por qué: si no, quedan puntos de unión sueltos en mitad del cable, sin error ni aviso. Fuente: VAL-0035-01.
- Cifras junto a una pieza: texto con `"justify": "left"` a 2,54 mm bajo el `Value`, como un campo más. Por qué: con `left bottom` el superíndice («I²C») tocaba el `Value`. Fuente: SPEC-0035.
- USBLC6 (pines 1-6 y 3-4 en la misma red) y pines de una red que encierran otra (TPS2116 VIN1/MODE con PR1 en medio): sin cruces solo con un lazo por fuera y la red encerrada dentro, en su propio recuadro. Por qué: es la única forma que no cruza cables. Fuente: SPEC-0035.
- Símbolo propio con pines abajo: ≥ 10 mm entre los nombres de los laterales y los de abajo. Por qué: ILIM tapaba FAULT. Fuente: SPEC-0031.
- En `hardware/libraries/ESP-Riego.kicad_wks`, `${COMMENT1}` va a 3,5 mm en negrita en una casilla de ≈ 145 mm: unos 50 caracteres, menos en mayúsculas. Por qué: más largo se sale de la casilla. Fuente: SPEC-0014.
- Las referencias «libres» que da una spec pueden estar en uso: se comprueba el máximo real en las hojas. Por qué: C46 estaba en uso. Fuente: SPEC-0029.
- Quitar un DNP: `sincronizar.py` quita `dnp` y `exclude_from_bom`, pero conserva el `exclude_from_pos_files` de la huella (avisa): se quita a mano y se comprueba con `kicad-cli pcb export pos --exclude-dnp`. Por qué: la pieza no saldría en el CPL. Fuente: SPEC-0034; `sincronizar.py` l. 124.
- Pruebas de `comprobar.py librerias.fichas`: se muta un código que solo esté en una ficha. Por qué: si el código aparece también en una ficha de bloque, la prueba se rompe. Fuente: SPEC-0029.
- En una prueba de SVG, dos textos iguales se mezclan: se usan textos distintos. Por qué: la prueba los confunde al medir. Fuente: SPEC-0035.
