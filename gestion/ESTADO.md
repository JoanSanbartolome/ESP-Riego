# Estado

Actualizado el 2026-11-23, al cerrar SPEC-0037. Lo reescribe el coordinador en cada cierre. El histórico está en git, en el registro de cada spec y, hasta el 2026-11-11, en `logs/coordinador/`.

## Siguiente

Una spec cada vez, porque comparten carpeta.

1. SPEC-0038: aplicar en `hardware/v2` los cambios de DEC-0017 y DEC-0018.
   - J10 BH254R-10P horizontal;
   - P1: D1, D2 y D3 a las piezas equivalentes, con fichas que recojan lo de VAL-0037-01-09;
   - P2: los THT, «a mano» en la BOM;
   - P3: 100 nF en C3 y C27–C38; C8 se queda en 220 nF;
   - P4: un LDO para U4 que cumpla (el de TI tiene stock 0);
   - textos de 1,0 mm en JP1.
   - Criterio: `evaluar` de `colocacion-b4.csv` sobre `hardware/v2` con 0 obligatorias (`estudio-coste.md` §8.10).
2. Después, el desglose del resto de la fase 4: aplicar b4 a la PCB con la imagen aprobada por el usuario, `restricciones.csv` con las reglas de JLCPCB de `colocacion-reglas.csv`, y el rutado.
3. SPEC-0036 (propuesta): observaciones de VAL-0032-01. La M (alternativa de U1) se resuelve antes del pedido; el estudio propone TPS26632RGET.

**Modelo de los agentes (DEC-0010):** Opus o inferior, nunca Fable 5.2. La validación ligera se lanza con `model: sonnet`.

## Colocación en texto (SPEC-0037)

- `colocacion.py` (extraer y evaluar, 117 reglas y 4 clases en `colocacion-reglas.csv`). Se itera en texto y se mira una imagen al final; comparativa en `docs/diseno/experimento-colocacion.md`.
- Criterios de DEC-0016. Placa de **100 × 100 mm** (2 $ / 5 uds), que no crece. J2, la antena de U5 y J10 van al ras (DEC-0016, DEC-0017). Cobre de disipación con +10 % de margen (+5 % en U2): justo, se comprueba al rutar.
- Colocación de partida: `docs/diseno/colocacion-b4.csv` (0 obligatorias, 58 objetivos, con J10 horizontal en una copia).
- `docs/diseno/estudio-coste.md`: 47,15 $ por placa con 5 uds y 25,02 $ con 50. Con P1 + P2 + P3, 42,02 $ y 24,00 $. Q1 se mantiene (ALI-03 sin cambios). Montaje Economic por una cara.

## Pendiente del usuario

- Antes del primer pedido, preguntar a JLCPCB si J2, U5 y J10 al ras exigen rieles (`estudio-coste.md` §7).
- En el prototipo, comprobar que las válvulas instaladas (Bermad S-390-3-D) caben en los límites de REL-11 (`salidas.md` §13.10).

## Para el layout (fase 4)

- FAB-08 se reescribe a 100 × 100 mm, con validación, cuando el usuario apruebe la colocación final sobre `hardware/v2` (DEC-0016).
- Zona prohibida de U5: hoy deja 15 mm a cada lado de la antena. La HDG (Fig. 26, p. 31) pide ≤ 2 mm por el lado de la alimentación y recortar la placa; depende de la caja (D5).
- Fuera del texto: el rutado y la cara inferior (`corte` es una estimación), la isla y las ranuras del SHT40 en `Edge.Cuts`, la legibilidad con zoom y C46 (O13, `estudio-coste.md` §8.2).
- Polígono BUS_24V bajo cada BTT6050; vías y pasta del EPAD de U5 (VAL-0021-01-03); serigrafía de REL-11 (`salidas.md` §8) y separación de 0,6 mm dentro de las huellas de salida (DEC-0008).
- `restricciones.py` compara la PCB con la tabla, no calcula anchos (VAL-0027-01-01).

## Para la fabricación (fase 5)

- Recomprobar el stock con `jlc.py` antes de pedir. U4 TLV1117LV33 de TI: 0 (2026-11-23). U1 TPS26632RGER: 131 (2026-11-23).
- Comprobar en los Gerber las vías del EP (F.Mask y B.Mask); las vías rellenas encarecen la placa y se consultan al usuario.

## Mantenimiento

- `verificar.py hardware/v2`: ERC 0, DRC 0 con 448 sin conectar y paridad 0 (SPEC-0032; `hardware/v2` no ha cambiado desde entonces).
- Posibles, sin spec: campo *Basic*/*Extended* en los símbolos; `hoja.py paginas` como `[auto]`; que `gestion.py` separe las tandas de un agente continuado (VAL-0037-01-05).
- FW-02, cuando exista `firmware/` (fase 6).
