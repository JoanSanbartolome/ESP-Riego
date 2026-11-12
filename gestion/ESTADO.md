# Estado

Actualizado el 2026-11-12, al cerrar SPEC-0027. Lo reescribe el coordinador en cada cierre. El histórico está en git, en el registro de cada spec y, hasta el 2026-11-11, en `logs/coordinador/`.

## Siguiente

1. **SPEC-0025 · Hoja de salidas** (propuesta), como piloto del ciclo nuevo y de `herramientas/kicad/`. Referencia para comparar: SPEC-0022, con 5 arranques y 210 acciones para 21 piezas.
2. Bloques que faltan de la fase 3: sensores y conectores, una spec por bloque. Después, el desglose de la fase 4 con la tabla única de restricciones (`docs/diseno/restricciones.csv`, que es la que lee `restricciones.py`) y la prueba de herramientas de layout (DEC-0009, M10).

**Modelo de los agentes:** el usuario pidió el 2026-11-12 no lanzar agentes con Fable 5.2. Hasta que diga otra cosa, cada `Agent` lleva `model: opus` (o `sonnet` donde ya tocaba), y no se continúa una instancia que arrancó con Fable.

## Para SPEC-0025

- **Primer paso, antes de sincronizar U7–U12:** añadir `(attr smd)` a la huella del BTT6050 y `(attr through_hole)` a la del WJ500V, en la librería y en J1 de la PCB. Sin el atributo no salen en el CPL (VAL-0027-01-02); `librerias.attr` falla hasta entonces.
- Tabla de campos de las 87 referencias y atributos DNP de D12–D17: `gestion/logs/SPEC-0024/01-jr-conformidad.md`. Pasarla a `hardware/componentes/campos-salidas.csv`, con el formato de `herramientas/kicad/README.md`, y aplicarla con `campos.py aplicar`.
- Los 12 cambios propuestos a `salidas.md` del mismo log (el 11 dice «§3.2», pero la l. 69 está en §2.1) y los «requiere DEC», que pasan a citar DEC-0008 (§0, §5, §11 nota 1, §13 y trazabilidad).
- En la raíz: unir IN1–6, IS1–6 y OUT_DEN con la hoja MCU y quitar sus no conexiones provisionales. `hoja.py` no toca los pines de hoja de la raíz ni admite símbolos de varias unidades o espejados.
- `Value` del LED: «Rojo» en D4 y «LED» en D5; la tabla propone «Rojo» para D6–D11.

## Pendiente del usuario

- Decidir si lo de Opus es permanente: habría que cambiar `model: inherit` en `ing-diseno` e `ing-validacion` (DEC-0009, M8) y repetir la prueba en vivo.
- Medir la inductancia de la válvula (REL-03, `salidas.md` §5). No bloquea.
- Medir en el prototipo la resistencia de la bobina caliente y el margen del umbral de carga abierta de 18 mV (REL-10, `salidas.md` §13.7). No bloquea.
- Decidir si se versiona el `.kicad_pro` que KiCad 10 reescribe al abrir el proyecto (SPEC-0028).

## Para el layout (fase 4)

- Polígono BUS_24V de ≥ 300 mm² bajo cada BTT6050; el pad 15 de B.Cu y las vías ya cuelgan de VS.
- Vías y pasta del EPAD de U5 (VAL-0021-01-03), serigrafía «STATUS» junto a D5 y antena en el borde.
- Separación de 0,6 mm dentro de las huellas de salida (DEC-0008).
- Al unir hojas en la raíz cambian los nombres de red: resincronizar antes de mirar la paridad.
- `restricciones.py` compara la PCB con la tabla, no calcula anchos: que la tabla salga de la corriente y del ΔT, y los retornos por zonas, son `[juicio]` (VAL-0027-01-01).

## Para la fabricación (fase 5)

- Comprobar en los Gerber el estado real de las vías del EP (F.Mask y B.Mask). Las vías rellenas y tapadas de JLCPCB encarecen la placa: consulta al usuario.
- Stock del BTT6050 en descenso (1 698 → 1 658 → 1 628; 10 placas usan 60): recomprobar antes de pedir, con `jlc.py`.
- Los ocho `[auto: pendiente]` de `checklists/fabricacion.md` van con el paquete de fabricación.

## Mantenimiento

- `verificar.py hardware/v2` da hoy ERC 0, DRC 0 con 172 sin conectar y paridad 0, y tres puntos `[auto]` en FALLA: `librerias.attr` (SPEC-0025), `librerias.fichas` y `librerias.gitattributes` (SPEC-0028).
- Observaciones acumuladas de las fases 2 y 3, las dos B de la guarda de VAL-0026-02 y lo pendiente de SPEC-0027: [SPEC-0028](specs/SPEC-0028-mantenimiento-fases-2-3.md).
- La guarda no se endurece más (DEC-0009): sus límites están en `README.md`, «Límites conocidos», y la batería falla si falta alguno.
- FW-02 (YAML coherente con el pinout): cuando exista `firmware/`, en la fase 6.
