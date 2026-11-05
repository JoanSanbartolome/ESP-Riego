---
spec: SPEC-0017
agente: ing-esquematicos
n: 04
fecha: 2026-11-05
estado: completado
---

# SPEC-0017 · 04 · ing-esquematicos

## Orden recibida

SPEC-0017 · rama spec/SPEC-0017-calculos-alimentacion · Lee: gestion/informes/VAL-0017-01.md · Haz: en docs/diseno/alimentacion.md corregir 01 (M: hueco de JP1 de 0,6 mm, huella `esp-riego:SolderJumper-2_P1.8mm_Open_Pad1.2x3.0mm`), 02, 03 (C5 = 100 nF) y 04 según la recomendación de cada uno. 05 pasa a SPEC-0018, no lo toques · Entrega: alimentacion.md + log 04-ing-esquematicos.md. Brevedad: la respuesta final, solo el contrato de salida.

## Contexto consultado

- `gestion/informes/VAL-0017-01.md`.
- TPS2663 SLVSE94G:
  - p. 7, I_OL en 3, 4,02, 9 y 30 kΩ;
  - §6.6, p. 9: t_FASTTRIP de 1 µs (corto franco, sin máximo) y de 2,2 / 3,2 / 4,5 µs (corto blando).

## Acciones

`docs/diseno/alimentacion.md`:

- **01 (M):** JP1 con hueco de 0,6 mm y paso de 1,8 mm, huella `esp-riego:SolderJumper-2_P1.8mm_Open_Pad1.2x3.0mm`.
  - Separación justificada con Vc = 53,3 V y el bus a 0 V (IPC-2221 B2, 51–100 V), el mismo criterio que `Power_In`.
  - Estaño: 0,13 mΩ y 3,2 mW a 4,9 A.
  - Actualizado en §3.13.9, §7 (lista de piezas y piezas nuevas), §8 y Anexo A.
- **02:** tabla de los cuatro puntos de I_OL. Constante 18,09 (4,02 kΩ) y tolerancia interpolada ± 7,1 %.
  - Banda de **3,86–4,57 A**; con la lógica, 4,77 A < 5,14 A (margen 0,37 A).
  - Cifras propagadas a §0, §3.7, §3.13.4, §3.13.7, §3.13.8, §3.13.9, §4, §5, §8 y §9.
- **03:** C5 = 100 nF (C1591), τ ≈ 2 ms. Error de IMON redactado como ± 7 % + ± 10 mV.
- **04:** §3.13.4 con las cotas en µs de la p. 9 (franco: 1 µs típ., sin máximo; blando: ≤ 4,5 µs).
  - Cota pesimista: ΔV ≤ 25 V solo con cerámicos.
  - La conclusión no depende de esa cota: el +5V cae 0,12 V en 4,5 µs y el EN no cruza el umbral.
  - Se añade la medida de TP1 y TP2 con el osciloscopio en la prueba de corto de §6.
- 05: no se toca (pasa a SPEC-0018).

## Decisiones y justificación

- Ninguna nueva: se aplican las recomendaciones de VAL-0017-01.

## Verificación

- Sin cambios en KiCad.
- Comprobado con Grep que no quedan las cifras antiguas: 3,84, 4,54, 4,74, P1.6mm, hueco de 0,4 mm y C5 de 1 nF.

## Pendiente

- SPEC-0018: huella de JP1 con el nuevo nombre y las cotas; derating de los cerámicos (VAL-0017-01-05); fichas (log 01).
- Prototipo: medir la caída de `VIN_PROT` en el corto (§3.13.4).

## Notas para el siguiente agente

- La nominal de I_OL es ahora 4,21 A (con la ec. 5 era 4,19 A). R_ILIM sigue en 4,30 kΩ.
