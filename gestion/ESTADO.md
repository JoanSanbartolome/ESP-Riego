# Estado

Actualizado el 2026-11-26, al cerrar SPEC-0039. Lo reescribe el coordinador en cada cierre. El histórico está en git, en el registro de cada spec y, hasta el 2026-11-11, en `logs/coordinador/`.

## Siguiente

Una spec cada vez, porque comparten carpeta.

**No abrir ninguna spec hasta que el usuario lo pida** (DEC-0019).

1. Desglose de la fase 4, aprobado (DEC-0019):
   - aplicar b4 a la PCB, con la imagen aprobada antes por el usuario; reescribe FAB-08 y la fila «Tamaño» de `docs/02` §1 a 100 × 100 mm;
   - clases de red y `.kicad_dru`;
   - rutado, en una o dos specs;
   - cierre.
2. SPEC-0036 (propuesta): observaciones de VAL-0032-01. El usuario quiere una pieza de respaldo para U1; el estudio propone TPS26632RGET.
3. D5 (caja): se diseña con la PCB terminada. D6: 1 oz, provisional hasta el diseño térmico.

**Reglas vigentes:** `decisiones/VIGENTES.md` (SPEC-0039); se comprueba con `gestion.py comprobar`. **Modelo de los agentes (DEC-0010):** Opus o inferior, nunca Fable 5.2. La validación ligera se lanza con `model: sonnet`.

## Diseño tras SPEC-0038

- U4 Diodes AP2114H-3.3TRG1; J10 BH254R-10P horizontal al ras; D1–D3 de hongjiacheng; C27–C38 de 100 nF (C28233); C3 y C8 en 220 nF; THT «a mano» en `fabricacion/v2.0-prueba/`.
- Coste: **41,96 $ por placa con 5 uds y 23,95 $ con 50** (`estudio-coste.md` §9).
- `colocacion-b4.csv` sobre `hardware/v2`: 0 obligatorias, 57 objetivos y PUNTOS 6151. b, b2 y b3 están en sus commits (`experimento-colocacion.md`).
- Placa de 100 × 100 mm, que no crece. El cobre de disipación lleva un +10 % de margen (+5 % en U2): justo, se comprueba al rutar.

## Pendiente del usuario

- Guarda: si también se analiza el código en línea (`-c`, heredoc), opción 3 de DEC-0020. Hoy no (M9).
- Rieles: para J2 y U5, al ras, se confirma en la revisión DFM antes del pedido (DEC-0019).
- En el prototipo: que las válvulas instaladas caben en REL-11 (`salidas.md` §13.10); T_J de U4 (60 °C/W con cobre es una suposición); arranque con *fold-back* de U4.

## Para el layout (fase 4)

- Zona prohibida de U5: hoy 15 mm a cada lado; la HDG (Fig. 26, p. 31) pide ≤ 2 mm por el lado de la alimentación y recortar la placa; depende de D5.
- Referencia de J10 en la posición por defecto de su huella; se coloca con b4.
- Fuera del texto: rutado y cara inferior; isla y ranuras del SHT40 en `Edge.Cuts`; legibilidad con zoom; C46 (`estudio-coste.md` §8.2).
- Polígono BUS_24V bajo cada BTT6050; vías y pasta del EPAD de U5 (VAL-0021-01-03); serigrafía de REL-11 y separación de 0,6 mm en las huellas de salida (DEC-0008).
- `restricciones.py` compara la PCB con la tabla, no calcula anchos (VAL-0027-01-01).

## Para la fabricación (fase 5)

- Recomprobar el stock con `jlc.py` antes de pedir (U4: 2 300 y U1: 131, el 2026-11-23).
- Comprobar en los Gerber las vías del EP (F.Mask y B.Mask); las vías rellenas se consultan al usuario.

## Mantenimiento

- `verificar.py hardware/v2`: ERC 0, DRC 0 con 448 sin conectar y paridad 0 (VAL-0039-02).
- Herramientas propuestas en SPEC-0039: 2 de `jr-conformidad` (banco de *render* de huellas; BOM con coste) y 7 de `ing-validacion` (partes 03 y 04).
- `herramientas/kicad/README.md` dice que `hoja.py extraer` + `generar` reproduce la hoja, pero se pierde el *justify* de los textos (`hoja.py` l. 241).
- `conectores.md` l. 6 cita `stock-conectores.csv` del 2026-11-15; la fila de J10 es del 2026-11-24.
- La guarda no deja a los agentes escribir sus CSV en `gestion/logs/SPEC-NNNN/`: los copia el coordinador.
- Posibles, sin spec: un campo *Basic*/*Extended* en los símbolos; `hoja.py paginas` como `[auto]`.
- FW-02, cuando exista `firmware/` (fase 6).
