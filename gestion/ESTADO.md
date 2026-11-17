# Estado

Actualizado el 2026-11-17, al cerrar SPEC-0028. Lo reescribe el coordinador en cada cierre. El histórico está en git, en el registro de cada spec y, hasta el 2026-11-11, en `logs/coordinador/`.

## Siguiente

Una spec cada vez (comparten carpeta). El esquema tiene sus cinco hojas con bloque, validadas y sin incidencias conocidas.

1. **Requisitos v0.7** (entrada de 24 V y limitador propios del módulo de expansión, y lo que salga de la medida de la válvula), cuando el usuario mida la válvula; antes de SPEC-0032 (decisión del usuario del 2026-11-15). D9 = arquitectura 1, I²C (DEC-0012).
2. **SPEC-0032 · Integración y revisión global**, que lleva a la etiqueta `v2.0-sch`. Lleva además las 5 B de VAL-0028-01.
3. Después, el desglose de la fase 4 con la tabla única de restricciones (`docs/diseno/restricciones.csv`) y la prueba de herramientas de layout (DEC-0009, M10).

**Modelo de los agentes (DEC-0010):** Opus o inferior, nunca Fable 5.2; validación ligera con `model: sonnet`.

## Mantenimiento de las fases 2 y 3 (SPEC-0028)

- Campos unificados en las cinco hojas (tablas nuevas `campos-alimentacion.csv` y `campos-mcu.csv`); fichas de los pasivos del MCU en `bloque-mcu.md`; U13 = SHT40-AD1B-R2 (C2909890, −0,10 $/placa).
- Hoja `conectores` regenerada por `hoja.py` sin cables ni `--forzar`. Herramientas nuevas: `hoja.py raiz` y `hoja.py netlist --plan`; batería `test_kicad.py` 42 OK.
- `esp-riego.kicad_pro` en el formato de KiCad 10 (versión 5), versionado (DEC-0011). Checklists `librerias.md` v7 y `layout.md` v9.
- VAL-0028-01: APROBADO_CON_OBSERVACIONES; 5 B en SPEC-0032.

## Pendiente del usuario

- **Válvulas instaladas (bloquea la etiqueta `v2.0-sch`):** la foto del usuario del 2026-11-13 es una Bermad S-390-3-D de 24 V AC, NC, 0,2 A y 3,5 W, con cables naranja y azul; la fila que coincide de la ficha S-390-T-3W da 42 Ω a 20 °C. No es la de 24 V DC y 156 Ω de DEC-0002 y `salidas.md`. Hoy funcionan las seis a la vez con la fuente de 24 V, sin problemas (DEC-0011). Falta medir la corriente de una válvula a 24 V DC, o la resistencia de la bobina en los dos sentidos; con el dato, `ing-diseno` revisa `salidas.md` (REL-03, REL-05, ALI-12) en SPEC-0032. También fija R_ILIM y la fuente del módulo de expansión (`viabilidad-expansion.md` §2.3).
- Medir en el prototipo la resistencia de la bobina caliente y el margen del umbral de carga abierta de 18 mV (REL-10, `salidas.md` §13.7). No bloquea.

## Para el layout (fase 4)

- Restricciones de AMB-02 en `sensores.md`, de EXP-02 y de los pulsadores en `conectores.md` §5, y longitud de bordes en `conectores.md` §4 (inferior: 71 de 84 mm útiles), listas para `restricciones.csv`.
- Fila SW3–SW8 en el centro (EXP-03, FAB-07), con U18 al lado; solo se alcanza con la caja abierta y comparte zona con el bus de 24 V y los planos (bus por la cara inferior).
- 115 huellas de salidas y conectores sin colocar; D12–D17 DNP con huella en la placa (DEC-0008).
- Polígono BUS_24V de ≥ 300 mm² bajo cada BTT6050; el pad 15 de B.Cu y las vías ya cuelgan de VS.
- Vías y pasta del EPAD de U5 (VAL-0021-01-03), serigrafía «STATUS» junto a D5 y antena en el borde.
- Separación de 0,6 mm dentro de las huellas de salida (DEC-0008).
- `restricciones.py` compara la PCB con la tabla, no calcula anchos: que la tabla salga de la corriente y del ΔT, y los retornos por zonas, son `[juicio]` (VAL-0027-01-01).

## Para la fabricación (fase 5)

- Stock del 2026-11-16: F1 0451010.MRL (C44479) 22 932, alternativa 0453010.MR (C178995) 1 437 (TA10 no vale: sin valor en continua); U13 SHT40-AD1B-R2 13 899. Del 2026-11-15: TCA9554PWR 5 455, TPS2553 48 313, TPS26632 1 240; BTT6050 1 628 el 2026-11-12. Recomprobar antes de pedir, con `jlc.py`.
- Comprobar en los Gerber el estado real de las vías del EP (F.Mask y B.Mask). Las vías rellenas y tapadas de JLCPCB encarecen la placa: consulta al usuario.
- Los ocho `[auto: pendiente]` de `checklists/fabricacion.md` van con el paquete de fabricación.

## Mantenimiento

- `verificar.py hardware/v2`: ERC 0, DRC 0 con 448 sin conectar, paridad 0 y ningún `[auto]` en FALLA; `campos.py revisar`: sin diferencias.
- Posible, sin spec: campo de tipo *Basic*/*Extended* en los símbolos de todas las hojas (SPEC-0028).
- `hardware/v1-tfg/Control_De_Riego.kicad_pro`, reescrito por KiCad 10 al abrirlo el 2026-11-16: pierde una exclusión de DRC y el cajetín. Sin versionar, a decidir por el usuario.
- La guarda no se endurece (DEC-0009): las dos líneas de VAL-0026-02 siguen en «Límites conocidos» de `README.md`.
- FW-02 (YAML coherente con el pinout): cuando exista `firmware/`, en la fase 6. El calentador del SHT4x no se usa: con él, +5V pasaría de ALI-12 (`mcu.md` §8.2).
