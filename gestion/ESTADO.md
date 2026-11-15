# Estado

Actualizado el 2026-11-15, al cerrar SPEC-0006. Lo reescribe el coordinador en cada cierre. El histórico está en git, en el registro de cada spec y, hasta el 2026-11-11, en `logs/coordinador/`.

## Siguiente

Una spec cada vez (comparten carpeta). El esquema tiene cinco hojas; faltan los conectores.

1. **D9 del usuario** con `docs/diseno/viabilidad-expansion.md` §0 (abajo); se registra en DEC-0012 y ajusta el alcance de SPEC-0031.
2. **SPEC-0031 · Conectores, expansión y pulsadores**: pasa `viabilidad-expansion.md` §10 a `conectores.md` y a la hoja, con la lista de §10.6 para `mcu.md` (§9.2 EXP_IO2 → EXP_EN, §10.1, §10.2, Anexo B y §14.2), los dos TPS2553 y la conexión de EN y FAULT; más los restos de EXP-01 y `PULSE_IN` de SPEC-0030. Después SPEC-0028 y **SPEC-0032 · Integración y revisión global**, que lleva a la etiqueta `v2.0-sch`.
3. Después, el desglose de la fase 4 con la tabla única de restricciones (`docs/diseno/restricciones.csv`) y la prueba de herramientas de layout (DEC-0009, M10).

**Modelo de los agentes (DEC-0010):** Opus o inferior, nunca Fable 5.2; validación ligera con `model: sonnet`.

## Expansión y conector EXP-02 (SPEC-0006)

- Conector: IDC 2 × 5 de 2,54 mm polarizado (BH254V-10P, C492442): 5 V, 3,3 V, I2C_EXP (GPIO47/48), EXP_INT (GPIO35), EXP_EN (GPIO36) y 4 GND; cada alimentación por un TPS2553 (≈ 2 $ por placa), ESD con dos USBLC6-2SC6, *pull-ups* de 2,2 kΩ en el lado del conector. ALI-12 no cambia; GPIO10, 18, 37 y 39 quedan para EXP-03.
- El módulo necesita su propia entrada de 24 V y su limitador: con la fuente de 5 A no cabe (4,77 A frente a 5,14 A). Requisito nuevo, a decidir con D9 (no cambia ALI-01, ALI-12 ni ALI-13).
- VAL-0006-02: APROBADO_CON_OBSERVACIONES; 1 M (F1 sin stock) y 2 B, en SPEC-0028.
- Coste: 4 arranques y 638 068 tokens (registro de la spec).

## Pendiente del usuario

- **D9, arquitectura de la expansión:** recomendada la 1, I²C con TCA9535 + ADS1115 (24,9 $ por módulo de 8 canales con 10 uds); alternativa, la 4, nodo ESP32-S3 propio (29,9 $), que no usa EXP-02.
- **Válvulas instaladas (bloquea la etiqueta `v2.0-sch`):** la foto del usuario del 2026-11-13 es una Bermad S-390-3-D de 24 V AC, NC, 0,2 A y 3,5 W, con cables naranja y azul; la fila que coincide de la ficha S-390-T-3W da 42 Ω a 20 °C. No es la de 24 V DC y 156 Ω de DEC-0002 y `salidas.md`. Hoy funcionan las seis a la vez con la fuente de 24 V, sin problemas (DEC-0011). Falta medir la corriente de una válvula a 24 V DC, o la resistencia de la bobina en los dos sentidos; con el dato, `ing-diseno` revisa `salidas.md` (REL-03, REL-05, ALI-12) en SPEC-0032. También fija R_ILIM y la fuente del módulo de expansión (`viabilidad-expansion.md` §2.3).
- Medir en el prototipo la resistencia de la bobina caliente y el margen del umbral de carga abierta de 18 mV (REL-10, `salidas.md` §13.7). No bloquea.

## Para el layout (fase 4)

- Restricciones de AMB-02 en `sensores.md` (isla en el borde lateral, ranuras con un puente, sin planos ni vías, ≥ 20 mm de pista I²C) y del conector EXP-02 en `viabilidad-expansion.md` §10.7, listas para `restricciones.csv`.
- Fila de 6 pulsadores en el centro de la placa (EXP-03, FAB-07): solo se alcanzan con la caja abierta y ocupan la zona del bus de 24 V y los planos (VAL-0030-02-05).
- 87 huellas de salidas sin colocar (U7–U12, J4–J9 y pasivos); D12–D17 DNP con huella en la placa (DEC-0008).
- Polígono BUS_24V de ≥ 300 mm² bajo cada BTT6050; el pad 15 de B.Cu y las vías ya cuelgan de VS.
- Vías y pasta del EPAD de U5 (VAL-0021-01-03), serigrafía «STATUS» junto a D5 y antena en el borde.
- Separación de 0,6 mm dentro de las huellas de salida (DEC-0008).
- `restricciones.py` compara la PCB con la tabla, no calcula anchos: que la tabla salga de la corriente y del ΔT, y los retornos por zonas, son `[juicio]` (VAL-0027-01-01).

## Para la fabricación (fase 5)

- F1 (0451010.MRL) con stock 0 el 2026-11-15: sustituto en SPEC-0028. Stock del BTT6050: 1 628 el 2026-11-12; del TPS26632, 1 240 el 2026-11-15. Recomprobar antes de pedir, con `jlc.py`.
- Comprobar en los Gerber el estado real de las vías del EP (F.Mask y B.Mask). Las vías rellenas y tapadas de JLCPCB encarecen la placa: consulta al usuario.
- Los ocho `[auto: pendiente]` de `checklists/fabricacion.md` van con el paquete de fabricación.

## Mantenimiento

- `verificar.py hardware/v2`: ERC 0, DRC 0 con 358 sin conectar y paridad 0; dos `[auto]` en FALLA (`librerias.fichas` y `librerias.gitattributes`), los dos en SPEC-0028.
- Observaciones de las fases 2 y 3 y herramientas que faltan: [SPEC-0028](specs/SPEC-0028-mantenimiento-fases-2-3.md). La guarda no se endurece más (DEC-0009).
- FW-02 (YAML coherente con el pinout): cuando exista `firmware/`, en la fase 6.
