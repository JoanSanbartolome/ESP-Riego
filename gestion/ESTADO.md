# Estado

Actualizado el 2026-11-14, al cerrar SPEC-0030. Lo reescribe el coordinador en cada cierre. El histórico está en git, en el registro de cada spec y, hasta el 2026-11-11, en `logs/coordinador/`.

## Siguiente

Una spec cada vez (comparten carpeta).

1. **SPEC-0029 · Bloque de sensores** (AMB-01, AMB-02): no depende de nada.
2. **SPEC-0006 · Viabilidad de la expansión**: informe y definición del conector EXP-02 (pines, tensiones, tipo y ESD, ya en su alcance); termina en la decisión D9 del usuario. Validación completa.
3. **SPEC-0031 · Conectores, expansión y pulsadores**, con la lista de restos de EXP-01 y `PULSE_IN` que dejó SPEC-0030; después SPEC-0028 y **SPEC-0032 · Integración y revisión global**, que lleva a la etiqueta `v2.0-sch`.
4. Después, el desglose de la fase 4 con la tabla única de restricciones (`docs/diseno/restricciones.csv`) y la prueba de herramientas de layout (DEC-0009, M10).

**Modelo de los agentes (DEC-0010):** Opus o inferior, nunca Fable 5.2; validación ligera con `model: sonnet`.

## Requisitos v0.6 (SPEC-0030, DEC-0011)

- EXP-01 retirado (sin entrada de pulsos ni de lluvia); D3 y D4 cerradas. EXP-03: 6 pulsadores en la placa, uno por salida, leídos por el firmware, prioridad S (aceptada por el usuario).
- `gestion.py trazabilidad` y el hook `commit-msg` aceptan IDs retirados de §9.
- Si una instancia se corta por el límite de uso, `integrar` cuenta la pausa en los minutos: se corrigen a mano en el registro.

## Pendiente del usuario

- **Válvulas instaladas (bloquea la etiqueta `v2.0-sch`):** la foto del usuario del 2026-11-13 es una Bermad S-390-3-D de 24 V AC, NC, 0,2 A y 3,5 W, con cables naranja y azul; la fila que coincide de la ficha S-390-T-3W da 42 Ω a 20 °C. No es la de 24 V DC y 156 Ω de DEC-0002 y `salidas.md`. Hoy funcionan las seis a la vez con la fuente de 24 V, sin problemas (DEC-0011). Falta medir la corriente de una válvula a 24 V DC, o la resistencia de la bobina en los dos sentidos; con el dato, `ing-diseno` revisa `salidas.md` (REL-03, REL-05, ALI-12) en SPEC-0032.
- D9, arquitectura de la expansión: con el informe de SPEC-0006.
- Medir en el prototipo la resistencia de la bobina caliente y el margen del umbral de carga abierta de 18 mV (REL-10, `salidas.md` §13.7). No bloquea.

## Para el layout (fase 4)

- Fila de 6 pulsadores en el centro de la placa (EXP-03, FAB-07): solo se alcanzan con la caja abierta y ocupan la zona del bus de 24 V y los planos (VAL-0030-02-05).
- 87 huellas de salidas sin colocar (U7–U12, J4–J9 y pasivos); D12–D17 DNP con huella en la placa (DEC-0008).
- Polígono BUS_24V de ≥ 300 mm² bajo cada BTT6050; el pad 15 de B.Cu y las vías ya cuelgan de VS.
- Vías y pasta del EPAD de U5 (VAL-0021-01-03), serigrafía «STATUS» junto a D5 y antena en el borde.
- Separación de 0,6 mm dentro de las huellas de salida (DEC-0008).
- `restricciones.py` compara la PCB con la tabla, no calcula anchos: que la tabla salga de la corriente y del ΔT, y los retornos por zonas, son `[juicio]` (VAL-0027-01-01).

## Para la fabricación (fase 5)

- Comprobar en los Gerber el estado real de las vías del EP (F.Mask y B.Mask). Las vías rellenas y tapadas de JLCPCB encarecen la placa: consulta al usuario.
- Stock del BTT6050: 1 628 el 2026-11-12 (10 placas usan 60); recomprobar antes de pedir, con `jlc.py`.
- Los ocho `[auto: pendiente]` de `checklists/fabricacion.md` van con el paquete de fabricación.

## Mantenimiento

- `verificar.py hardware/v2`: ERC 0, DRC 0 con 352 sin conectar y paridad 0; dos `[auto]` en FALLA (`librerias.fichas` y `librerias.gitattributes`), los dos en SPEC-0028. La batería `test_kicad.test_librerias_fichas` falla por lo mismo.
- Observaciones de las fases 2 y 3 y herramientas que faltan: [SPEC-0028](specs/SPEC-0028-mantenimiento-fases-2-3.md).
- La guarda no se endurece más (DEC-0009): sus límites están en `README.md`, «Límites conocidos».
- FW-02 (YAML coherente con el pinout): cuando exista `firmware/`, en la fase 6.
