# Estado

Actualizado el 2026-11-13, al cerrar SPEC-0025. Lo reescribe el coordinador en cada cierre. El histórico está en git, en el registro de cada spec y, hasta el 2026-11-11, en `logs/coordinador/`.

## Siguiente

Una spec cada vez (comparten carpeta), con el ciclo de SPEC-0025: paso de campos, paso de diseño y una validación.

1. **Requisitos v0.6** (DEC-0011, sin crear): retira EXP-01, redefine EXP-03 con 6 pulsadores y cierra D3 y D4. Coordinador, validación ligera.
2. **SPEC-0029 · Bloque de sensores** (sin crear; AMB-01, AMB-02): no depende de nada, puede ir antes.
3. **SPEC-0006 · Viabilidad de la expansión**, que además fija el conector EXP-02 (DEC-0011) y termina en la decisión D9 del usuario.
4. Bloque de conectores, expansión y pulsadores; después SPEC-0028 y la integración y revisión global del esquema, que lleva a la etiqueta `v2.0-sch`.
5. Después, el desglose de la fase 4 con la tabla única de restricciones (`docs/diseno/restricciones.csv`, que es la que lee `restricciones.py`) y la prueba de herramientas de layout (DEC-0009, M10).

**Modelo de los agentes (DEC-0010):** Opus o inferior, nunca Fable 5.2. Comprobado en SPEC-0025: `ing-diseno` e `ing-validacion` arrancan en Opus por su definición.

## Piloto del ciclo nuevo (SPEC-0025)

- 4 arranques (`jr-conformidad` ×2 en una instancia, `ing-diseno` ×1 reanudado tras el límite de uso, `ing-validacion` ×1), 126 acciones, 489 349 tokens y unos 30 min para 87 piezas. Referencia, SPEC-0022: 5 arranques y 210 acciones para 21 piezas.
- Sin correcciones: VAL-0025-01 con una sola B.
- Scripts en la carpeta temporal: 2 de `ing-diseno` más 7 de Python en línea (sobre todo la raíz) y 1 de validación; `herramientas/kicad/`: 36 usos. Lo que falta está en SPEC-0028 (`hoja.py raiz`, `hoja.py netlist --plan`).
- `integrar` toma los minutos de toda la instancia: si un agente se corta o se continúa, se corrigen a mano en el registro con las horas de la auditoría.

## Pendiente del usuario

- **Válvulas instaladas (bloquea la etiqueta `v2.0-sch`):** la foto del usuario del 2026-11-13 es una Bermad S-390-3-D de 24 V AC, NC, 0,2 A y 3,5 W, con cables naranja y azul; la fila que coincide de la ficha S-390-T-3W da 42 Ω a 20 °C. No es la de 24 V DC y 156 Ω de DEC-0002 y `salidas.md`. Hoy funcionan las seis a la vez con la fuente de 24 V, sin problemas (DEC-0011). Falta medir la corriente de una válvula a 24 V DC, o la resistencia de la bobina en los dos sentidos; con el dato, `ing-diseno` revisa `salidas.md` (REL-03, REL-05, ALI-12).
- D9, arquitectura de la expansión: con el informe de SPEC-0006.
- Medir en el prototipo la resistencia de la bobina caliente y el margen del umbral de carga abierta de 18 mV (REL-10, `salidas.md` §13.7). No bloquea.

## Para el layout (fase 4)

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

- `verificar.py hardware/v2` da hoy ERC 0, DRC 0 con 352 sin conectar y paridad 0, y dos puntos `[auto]` en FALLA: `librerias.fichas` (6 pasivos del MCU) y `librerias.gitattributes`, los dos en SPEC-0028. `librerias.attr` ya pasa.
- Observaciones acumuladas de las fases 2 y 3, VAL-0025-01-01 y las herramientas que faltan: [SPEC-0028](specs/SPEC-0028-mantenimiento-fases-2-3.md).
- La guarda no se endurece más (DEC-0009): sus límites están en `README.md`, «Límites conocidos», y la batería falla si falta alguno.
- FW-02 (YAML coherente con el pinout): cuando exista `firmware/`, en la fase 6.
