# Estado

Actualizado el 2026-11-18, al cerrar SPEC-0035. Lo reescribe el coordinador en cada cierre. El histórico está en git, en el registro de cada spec y, hasta el 2026-11-11, en `logs/coordinador/`.

## Siguiente

Una spec cada vez (comparten carpeta). El esquema tiene sus cinco hojas y la subhoja «Canal» con el estilo de DEC-0015, validadas y sin incidencias conocidas.

1. **SPEC-0032 · Integración y revisión global**, que lleva a la etiqueta `v2.0-sch`. La raíz, con el estilo de DEC-0015 (`esquema.md` v17). Lleva además las 5 B de VAL-0028-01. Ya no depende de medir la válvula (DEC-0014).
2. Después, el desglose de la fase 4 con la tabla única de restricciones (`docs/diseno/restricciones.csv`) y la prueba de herramientas de layout (DEC-0009, M10).

**Modelo de los agentes (DEC-0010):** Opus o inferior, nunca Fable 5.2; validación ligera con `model: sonnet`.

## Esquema legible (SPEC-0035)

- KIC-06 (docs/02 v0.8, DEC-0015): recuadros por bloque, cables dentro, etiquetas solo hacia fuera, cifras junto a la pieza. Salidas con `canal.kicad_sch` ×6 y las referencias de siempre; netlist idéntica a la anterior salvo 30 redes internas renombradas (`/Salidas/CanalN/…`).
- Herramientas: `hoja.py` dibuja cables, recuadros y subhojas con instancias; `dibujo.py`; `comprobar.py` con `esquema.cruces`, `sueltas`, `recuadros`, `etiquetas` y `pcb_main` (sección «Huellas que cambian frente a `main`:» del parte); `hoja.py paginas`. 54 pruebas en `herramientas/pruebas/test_kicad.py`.
- Checklist `esquema.md` v17. VAL-0035-01 APROBADO_CON_OBSERVACIONES (2 M, 4 B) → VAL-0035-02 APROBADO_CON_OBSERVACIONES: solo queda -02 (la guarda no ve escrituras de `python` en línea), que el usuario decidió no corregir (DEC-0009, `gestion/README.md`).
- Desviaciones aceptadas: GND laterales de PGTH y PLIM de U1; recuadro ESD propio para U6/U16/U17.

## Límites de uso de las salidas (SPEC-0034)

- `salidas.md` §0: tabla REL-11 (1 A por salida, 3,5 A de suma, carga mínima 80 mA / ≤ 218 Ω, solo bobinas DC, sin PWM ni biestables, aislamiento ≥ 400 kΩ); serigrafía en §8 y avisos de firmware en §12 (suma sobre LIM_IMON > 3,3 A, puede avisar desde ≈ 3,0 A).
- D12–D17 (M7, C95872, Basic, 0,062 USD por placa) montados en esquema, BOM, CPL y `campos-salidas.csv`.
- Prueba de prototipo nueva (§13.9): impulsos en el diodo con JP1 cerrado (BTT enclavado; uno por subida de IN y por rearme de subtensión).
- Checklist `esquema.md` v12. VAL-0034-01 APROBADO_CON_OBSERVACIONES (1 M, 5 B) → VAL-0034-02 APROBADO.

## Requisitos v0.7 (SPEC-0033)

- DEC-0014: salidas con límites de uso propios de la placa (REL-11), sin válvula de referencia. Una carga por salida, 1 A por salida y 3,5 A de suma como límites (la suma la vigila el firmware; el limitador corta en 3,5–4,9 A), y rueda libre D12–D17 montada (sustituye el punto 2 de DEC-0008).
- EXP-05: el módulo de expansión con 24 V y limitador propios; D9 cerrada (DEC-0012).
- Prueba nueva en §6: aviso a 3,6 A sin que actúe el limitador. Checklists `esquema.md` v11 y `requisitos.md` v6.
- VAL-0033-01 RECHAZADO (4 M, 2 B) → VAL-0033-02 APROBADO.

## Pendiente del usuario

- Nada bloqueante. En el prototipo, comprobar que las válvulas instaladas (Bermad S-390-3-D, 24 V AC alimentadas en continua) caben en los límites de uso de REL-11; ya no condicionan el diseño (DEC-0014). En continua disipan 14–16 W a 24 V: que lo admitan es dato de la válvula (`salidas.md` §13.10).

## Para el layout (fase 4)

- Restricciones de AMB-02 en `sensores.md`, de EXP-02 y de los pulsadores en `conectores.md` §5, y longitud de bordes en `conectores.md` §4 (inferior: 71 de 84 mm útiles), listas para `restricciones.csv`.
- Fila SW3–SW8 en el centro (EXP-03, FAB-07), con U18 al lado; solo se alcanza con la caja abierta y comparte zona con el bus de 24 V y los planos (bus por la cara inferior).
- 115 huellas de salidas y conectores sin colocar; D12–D17 se montan (DEC-0014), junto al borne de su canal.
- Polígono BUS_24V de ≥ 300 mm² bajo cada BTT6050; el pad 15 de B.Cu y las vías ya cuelgan de VS.
- Vías y pasta del EPAD de U5 (VAL-0021-01-03), serigrafía «STATUS» junto a D5 y antena en el borde.
- Serigrafía de los límites de uso de las salidas (REL-11; texto en `salidas.md` §8).
- Separación de 0,6 mm dentro de las huellas de salida (DEC-0008).
- `restricciones.py` compara la PCB con la tabla, no calcula anchos: que la tabla salga de la corriente y del ΔT, y los retornos por zonas, son `[juicio]` (VAL-0027-01-01).

## Para la fabricación (fase 5)

- Stock del 2026-11-16: F1 0451010.MRL (C44479) 22 932, alternativa 0453010.MR (C178995) 1 437 (TA10 no vale: sin valor en continua); U13 SHT40-AD1B-R2 13 899. Del 2026-11-15: TCA9554PWR 5 455, TPS2553 48 313, TPS26632 1 240; BTT6050 1 628 el 2026-11-12. Recomprobar antes de pedir, con `jlc.py`.
- Comprobar en los Gerber el estado real de las vías del EP (F.Mask y B.Mask). Las vías rellenas y tapadas de JLCPCB encarecen la placa: consulta al usuario.
- Los ocho `[auto: pendiente]` de `checklists/fabricacion.md` van con el paquete de fabricación.

## Mantenimiento

- `verificar.py hardware/v2`: ERC 0, DRC 0 con 448 sin conectar, paridad 0 y ningún `[auto]` en FALLA; `campos.py revisar`: sin diferencias.
- Posible, sin spec: campo de tipo *Basic*/*Extended* en los símbolos de todas las hojas (SPEC-0028).
- La guarda no se endurece (DEC-0009): las dos líneas de VAL-0026-02 y el caso de VAL-0035-01-02 siguen en «Límites conocidos» de `gestion/README.md`.
- Posible, sin spec: `hoja.py paginas` como `[auto: comprobar.py esquema.paginas]` (propuesta de VAL-0035-02); hoy es `[juicio]`.
- FW-02 (YAML coherente con el pinout): cuando exista `firmware/`, en la fase 6; incluye los avisos de REL-10 por la suma de 3,5 A. El calentador del SHT4x no se usa: con él, +5V pasaría de ALI-12 (`mcu.md` §8.2).
