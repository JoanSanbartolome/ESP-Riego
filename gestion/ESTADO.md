# Estado

Actualizado el 2026-11-24, al cerrar SPEC-0038. Lo reescribe el coordinador en cada cierre. El histórico está en git, en el registro de cada spec y, hasta el 2026-11-11, en `logs/coordinador/`.

## Siguiente

Una spec cada vez, porque comparten carpeta.

1. Desglose del resto de la fase 4, que se consulta al usuario:
   - aplicar `colocacion-b4.csv` a la PCB de `hardware/v2` cuando el usuario apruebe la imagen;
   - `restricciones.csv` con las reglas de JLCPCB de `colocacion-reglas.csv`;
   - el rutado.
2. SPEC-0036 (propuesta): observaciones de VAL-0032-01. La M (alternativa de U1) se resuelve antes del pedido; el estudio propone TPS26632RGET.

**Modelo de los agentes (DEC-0010):** Opus o inferior, nunca Fable 5.2. La validación ligera se lanza con `model: sonnet`.

## Diseño tras SPEC-0038

- DEC-0017 y DEC-0018 aplicadas en `hardware/v2`:
  - U4 es Diodes AP2114H-3.3TRG1, con el mismo patillaje; el margen en el cambio de U3 es de 0,145 V (`alimentacion.md` §3.9);
  - J10 es BH254R-10P horizontal, con el mismo pinout;
  - D1, D2 y D3 llevan las piezas de P1;
  - C27–C38 son de 100 nF (C28233); C3 y C8 se quedan en 220 nF (C513710);
  - los THT (J1, J3, J4–J10) van «a mano» en `fabricacion/v2.0-prueba/`.
- Coste: **41,96 $ por placa con 5 uds y 23,95 $ con 50** (`estudio-coste.md` §9).
- `colocacion-b4.csv` sobre `hardware/v2`: 0 obligatorias, 57 objetivos y PUNTOS 6151.
- Placa de 100 × 100 mm, que no crece. J2, la antena de U5 y J10 van al ras (DEC-0016, DEC-0017). El cobre de disipación lleva un +10 % de margen (+5 % en U2): justo, se comprueba al rutar.

## Pendiente del usuario

- Antes del primer pedido, preguntar a JLCPCB si J2, U5 y J10 al ras exigen rieles (`estudio-coste.md` §7).
- En el prototipo:
  - comprobar que las válvulas instaladas (Bermad S-390-3-D) caben en los límites de REL-11 (`salidas.md` §13.10);
  - medir T_J de U4: los 60 °C/W con cobre son una suposición, porque el datasheet solo da 128 °C/W sin disipador;
  - probar el arranque con *fold-back* de U4.

## Para el layout (fase 4)

- FAB-08 se reescribe a 100 × 100 mm, con validación, cuando el usuario apruebe la colocación final sobre `hardware/v2` (DEC-0016).
- Zona prohibida de U5: hoy deja 15 mm a cada lado de la antena. La HDG (Fig. 26, p. 31) pide ≤ 2 mm por el lado de la alimentación y recortar la placa; depende de la caja (D5).
- La referencia de J10 está en la posición por defecto de su huella; se coloca con b4.
- Fuera del texto:
  - el rutado y la cara inferior (`corte` es una estimación);
  - la isla y las ranuras del SHT40 en `Edge.Cuts`;
  - la legibilidad con zoom;
  - C46 (O13, `estudio-coste.md` §8.2).
- Polígono BUS_24V bajo cada BTT6050; vías y pasta del EPAD de U5 (VAL-0021-01-03); serigrafía de REL-11 (`salidas.md` §8) y separación de 0,6 mm dentro de las huellas de salida (DEC-0008).
- `restricciones.py` compara la PCB con la tabla, no calcula anchos (VAL-0027-01-01).

## Para la fabricación (fase 5)

- Recomprobar el stock con `jlc.py` antes de pedir. U4 AP2114H: 2 300 (2026-11-23). U1 TPS26632RGER: 131 (2026-11-23).
- Comprobar en los Gerber las vías del EP (F.Mask y B.Mask); las vías rellenas encarecen la placa y se consultan al usuario.

## Mantenimiento

- `verificar.py hardware/v2`: ERC 0, DRC 0 con 448 sin conectar y paridad 0 (SPEC-0038).
- **Guarda de zonas (VAL-0038-01-04):** `jr-conformidad` escribió en `docs/` con un script que la guarda no vio. Lo deshizo y `revisar` lo detectó, pero hay que cerrar el hueco en la guarda.
- Posibles, sin spec:
  - un campo *Basic*/*Extended* en los símbolos;
  - `hoja.py paginas` como `[auto]`;
  - que `gestion.py` separe las tandas de un agente continuado al sumar acciones y minutos (VAL-0037-01-05; en SPEC-0038 se corrigió a mano otra vez).
- FW-02, cuando exista `firmware/` (fase 6).
