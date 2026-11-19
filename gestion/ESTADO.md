# Estado

Actualizado el 2026-11-19, al cerrar SPEC-0032. Lo reescribe el coordinador en cada cierre. El histórico está en git, en el registro de cada spec y, hasta el 2026-11-11, en `logs/coordinador/`.

## Siguiente

Una spec cada vez (comparten carpeta). El esquema v2 está cerrado para el layout (SPEC-0032); la etiqueta `v2.0-sch`, con OK del usuario.

1. El desglose de la fase 4 con la tabla única de restricciones (`docs/diseno/restricciones.csv`) y la prueba de herramientas de layout (DEC-0009, M10).
2. SPEC-0036 (propuesta): observaciones de VAL-0032-01; la M (alternativa de U1) antes del pedido.

**Modelo de los agentes (DEC-0010):** Opus o inferior, nunca Fable 5.2; validación ligera con `model: sonnet`.

## Integración del esquema (SPEC-0032)

- Raíz con el estilo de DEC-0015 (`hoja.py generar` escribe la raíz), páginas 1–12 en el orden del árbol; netlist igual a la de SPEC-0035.
- `docs/diseno/arquitectura.md`: bloques, presupuesto (lógica 4,32 W ≤ 4,8 W; entrada 4,77 A ≤ 5,1 A), GPIO contra la netlist (base de FW-02) y revisión global sin cambios de circuito.
- `fabricacion/v2.0-sch/`: BOM preliminar (53 líneas, 187 piezas, 27,46 USD por placa a 5 placas; + ≈ 78 USD por pedido de recargo de 26 Extended) y PDF.
- VAL-0032-01 APROBADO_CON_OBSERVACIONES (1 M, 2 B) → SPEC-0036. Las 5 B de VAL-0028-01, cerradas.

## Specs anteriores (resumen)

- SPEC-0035: KIC-06 (DEC-0015), Salidas con `canal.kicad_sch` ×6; herramientas `hoja.py`, `dibujo.py`, `comprobar.py` y `hoja.py paginas`; checklist `esquema.md` v17. Desviaciones aceptadas: GND laterales de PGTH y PLIM de U1; recuadro ESD propio para U6/U16/U17.
- SPEC-0034: REL-11 en `salidas.md` §0 (serigrafía §8, avisos de firmware §12), D12–D17 montados, prueba §13.9.

## Pendiente del usuario

- Nada bloqueante. En el prototipo, comprobar que las válvulas instaladas (Bermad S-390-3-D, 24 V AC alimentadas en continua) caben en los límites de uso de REL-11; ya no condicionan el diseño (DEC-0014). En continua disipan 14–16 W a 24 V: que lo admitan es dato de la válvula (`salidas.md` §13.10).

## Para el layout (fase 4)

- Restricciones de AMB-02 en `sensores.md`, de EXP-02 y de los pulsadores en `conectores.md` §5, y longitud de bordes en `conectores.md` §4 (inferior: 71 de 84 mm útiles), listas para `restricciones.csv`.
- Fila SW3–SW8 en el centro (EXP-03, FAB-07), con U18 al lado y lejos de las pistas (sin ESD, `arquitectura.md` §4.6); comparte zona con el bus de 24 V (bus por la cara inferior).
- 115 huellas de salidas y conectores sin colocar; D12–D17 se montan (DEC-0014), junto al borne de su canal.
- Polígono BUS_24V de ≥ 300 mm² bajo cada BTT6050; el pad 15 de B.Cu y las vías ya cuelgan de VS.
- Vías y pasta del EPAD de U5 (VAL-0021-01-03), serigrafía «STATUS» junto a D5 y antena en el borde.
- Serigrafía de REL-11 (`salidas.md` §8); separación de 0,6 mm dentro de las huellas de salida (DEC-0008).
- `restricciones.py` compara la PCB con la tabla, no calcula anchos: que la tabla salga de la corriente y del ΔT, y los retornos por zonas, son `[juicio]` (VAL-0027-01-01).

## Para la fabricación (fase 5)

- Stock del 2026-11-16: F1 0451010.MRL (C44479) 22 932, alternativa 0453010.MR (C178995) 1 437 (TA10 no vale: sin valor en continua); U13 SHT40-AD1B-R2 13 899. Del 2026-11-15: TCA9554PWR 5 455, TPS2553 48 313, TPS26632 1 240; BTT6050 1 628 el 2026-11-12. Recomprobar antes de pedir, con `jlc.py`. U1 TPS26632RGER: 93, y su alternativa TPS26633RGER, 1 (2026-11-19): resolver antes del pedido (VAL-0032-01-01, SPEC-0036).
- Comprobar en los Gerber el estado real de las vías del EP (F.Mask y B.Mask). Las vías rellenas y tapadas de JLCPCB encarecen la placa: consulta al usuario. Los ocho `[auto: pendiente]` de `checklists/fabricacion.md` van con el paquete.

## Mantenimiento

- `verificar.py hardware/v2`: ERC 0, DRC 0 con 448 sin conectar, paridad 0 y ningún `[auto]` en FALLA; `campos.py revisar`: sin diferencias.
- La guarda no se endurece (DEC-0009): las dos líneas de VAL-0026-02 y el caso de VAL-0035-01-02 siguen en «Límites conocidos» de `gestion/README.md`.
- Posibles, sin spec: campo *Basic*/*Extended* en los símbolos (SPEC-0028); `hoja.py paginas` como `[auto]` (VAL-0035-02).
- FW-02 (YAML coherente con el pinout): cuando exista `firmware/`, en la fase 6; incluye los avisos de REL-10 por la suma de 3,5 A. El calentador del SHT4x no se usa: con él, +5V pasaría de ALI-12 (`mcu.md` §8.2).
