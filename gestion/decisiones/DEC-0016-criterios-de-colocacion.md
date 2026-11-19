---
id: DEC-0016
titulo: Criterios de colocación y tamaño de la placa como variable
fecha: 2026-11-19
estado: aceptada
decide: usuario
specs: [SPEC-0037]
requisitos: [FAB-01, FAB-02, FAB-05, FAB-08, FAB-09, MCU-02, AMB-02]
---

# DEC-0016 · Criterios de colocación y tamaño de la placa como variable

## Contexto

En SPEC-0037, la primera colocación en texto (brazo B, `colocacion-b.csv`) cumple las 65 reglas de `colocacion-reglas.csv`, pero la imagen enseña lo que las reglas no miden: patios a 0,05 mm, sin sitio para pistas ni vías; serigrafía solapada e ilegible; nada de espacio para el cobre de los pads expuestos, y desacoplos lejos de su pieza. Con 197 huellas, la placa de FAB-08 (≤ 100 × ≈ 70 mm) queda justa.

## Opciones consideradas

1. Mantener las reglas y el tamaño, y corregir a mano en el layout: más barato ahora, pero el problema se traslada al rutado y a la fabricación.
2. Añadir los criterios del usuario a `colocacion.py` y dejar el tamaño como variable, con su coste a la vista.

## Decisión

El usuario elige la 2 (2026-11-19). Criterios, por orden de prioridad:

1. **Fabricación de la clase más barata de JLCPCB.** PCB estándar de 2 capas y montaje (PCBA) sin recargos por reglas: pista, separación, vía, anillo, cobre a borde, serigrafía y separación entre piezas según las capacidades publicadas por JLCPCB, con página y fecha. Si FAB-02 es más estricto, manda FAB-02.
2. **Serigrafía legible y comprobable.** Sin solapes entre textos, ni de textos con pads, con la máscara abierta, fuera del contorno o bajo otra pieza. Altura y trazo mínimos de JLCPCB con margen. Cada referencia junto a su pieza y sin ambigüedad, para la inspección (AOI y visual), el montaje a mano de los THT y la reparación.
3. **Diseño térmico en la distribución.** Espacio para el cobre de los pads expuestos y de las piezas que disipan (U1, U2, U4, U7–U12, L1, Q1, D3, F1). Fuentes de calor repartidas y no apiladas, lejos del SHT40 (AMB-02) y de la antena (MCU-02), con su disipación estimada en las reglas.
4. **Tamaño de la placa como variable de la iteración.** Hasta 100 × 100 mm no cambia el precio de la PCB en JLCPCB; dentro de ese límite, el alto de FAB-08 (≈ 70 mm) se puede subir. Por encima de 100 mm en cualquier lado, la herramienta da el sobrecoste con su fuente, y el coordinador consulta al usuario antes de adoptarlo.

## Consecuencias

- SPEC-0037 añade el paso 3 (mejorar `colocacion.py` y las reglas) y el paso 4 (repetir el brazo B con el tamaño como variable). Todo, sobre copias.
- FAB-08 se reescribe en `docs/02` (con validación, DEC-0005) cuando el usuario apruebe el tamaño final, en la spec de colocación. Hasta entonces, el tamaño de los experimentos no cambia `hardware/v2`.
- La caja (D5) sigue pendiente: el tamaño que salga es una entrada para elegirla.
- Las reglas de fabricación de JLCPCB que se usen, con su fuente, pasan después a la tabla de restricciones (M10) y a `.kicad_dru`.
