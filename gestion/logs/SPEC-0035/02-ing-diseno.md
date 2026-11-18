---
spec: SPEC-0035
agente: ing-diseno
n: 02
fecha: 2026-11-18
estado: completado
---

# SPEC-0035 · 02 · ing-diseno

Paso 3, primera parte: Conectores, MCU y Alimentación redibujadas con las reglas 1–6 de DEC-0015, con `hoja.py generar` y el piloto Sensores como patrón. Salidas, «Canal» y la PCB no se han tocado.

## Hecho

- `hardware/v2/conectores.kicad_sch` (8 recuadros), `mcu.kicad_sch` (7) y `alimentacion.kicad_sch` (7): cables y uniones dentro de cada bloque, etiquetas solo entre bloques y hojas, alimentación con cable corto (tensiones arriba, GND abajo), cifras junto a la pieza (ILIM, τ, VOUT, I_OL en nota, ÷21,53, ≈1,4 mA…) y ≤ 2 líneas de nota por bloque. Mismos campos, UUID y valores.
- `hardware/v2/estilo-pendiente.txt`: solo queda `salidas.kicad_sch`.
- Imágenes: `C:\Users\josan\AppData\Local\Temp\claude\2c54f79e79dd3002\c980b02f-1588-4782-8921-adea897769ca\scratchpad\entrega\paso3-Conectores.png`, `…\entrega\paso3-MCU.png` y `…\entrega\paso3-Alimentacion.png`.

## Decisiones y desviaciones

- **Nombres de red conservados:** las redes internas de un bloque que antes se nombraban con etiquetas (ILIM_5V, BTN1–BTN6, CC1, CC2, UART_TX, LED_A, Q1_G, U1_ILIM, U2_FB…) llevan una etiqueta local sobre su cable, una vez por recuadro. Sin ella cambiarían los nombres de red y la paridad con la PCB.
- **ESD en recuadro propio** (U16/U17 en Conectores, U6 en MCU): los pines 1-6 y 3-4 del USBLC6 son la misma red, y unirlos por fuera encierra VBUS o las I/O. Dibujarlo sin cruces solo es posible con su etiqueta de VBUS dentro del lazo, y eso pide un recuadro propio para no repetir etiqueta. Ningún cruce cable-cable.
- **LED (D4, D5):** GND puesto directamente en el cátodo, sin cable. `_estilo.py` mide el símbolo por su caja, y las flechas de Device:LED sobresalen 0,76 mm detrás del cátodo: cualquier cable que salga de ese pin da un falso «cruza D5». Salidas (6 LED) lo encontrará igual.
- Etiqueta local y jerárquica del mismo nombre en una hoja (LIM_EN, VBUS, VIN_SENSE, LIM_IMON, I2C_SDA…) se fusionan en una sola etiqueta jerárquica por recuadro. Las banderas de ERC de Alimentación van en un recuadro propio.
- Campos de símbolos girados: 90° y 270° con el ángulo relativo (270 o 90) para que se lean en horizontal, y 180° con `right` para que salgan a la izquierda.

## Verificación

- `verificar.py hardware/v2`: ERC 0, DRC 0 (448 sin conectar, placa sin rutar), paridad 0; [auto] 25: OK 23, FALLA 0, N/A 2 (los 4 de estilo, en OK con 4 hojas). `campos.py revisar`: 0 diferencias. `esquema.pcb_main`: ninguna huella cambia.
- `hoja.py netlist` frente a la copia de `main` de `scratchpad\ref\main_v2` y frente a HEAD: 0 diferencias, por grupos y por nombre.
- Herramientas sin cambios: no hace falta pasar `test_kicad.py`.

## Para validación

- Bloques para el muestreo: Alimentación «Unión USB / 5 V» (lazo de MODE alrededor de PR1), Conectores «ESD» y MCU «USB-C».

## Pendiente

- **Coordinador:** la siguiente parte (Salidas + «Canal» + PCB). Los JSON se generaron con un ayudante de scratchpad (`…\scratchpad\p3\dib.py`: coordenadas de pin, cables pin a pin y comprobación de conectividad frente a la hoja original). Propuesta: pasarlo a `herramientas/kicad/` con su prueba, y que `_estilo.py` mida el cuerpo por primitivas para quitar el falso positivo del LED.
