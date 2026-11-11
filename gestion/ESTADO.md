# Estado

Actualizado el 2026-11-11, con SPEC-0026 abierta. Lo reescribe el coordinador en cada cierre. El histórico está en git, en el registro de cada spec y, hasta el 2026-11-11, en `logs/coordinador/`.

## Siguiente

1. **SPEC-0026 · Orquestación v2** (abierta, rama `spec/SPEC-0026-orquestacion-v2`). Hecho: guarda, `gestion.py`, tres agentes, `CLAUDE.md`, manual, plantillas y checklists, con las tres baterías en verde. Falta, en una **sesión nueva** porque las definiciones de agente se cargan al arrancar: prueba en vivo de los tres agentes, validación ligera y cierre.
2. **SPEC-0027 · Caja de herramientas de KiCad** (propuesta): `ing-diseno`, validación completa.
3. **SPEC-0025 · Hoja de salidas** (propuesta), como piloto del ciclo nuevo. Referencia para comparar: SPEC-0022, con 5 arranques y 210 acciones para 21 piezas.
4. Bloques que faltan de la fase 3: sensores y conectores, una spec por bloque. Después, el desglose de la fase 4 con la tabla única de restricciones y la prueba de herramientas de layout (DEC-0009, M10).

## Para SPEC-0025

- Tabla de campos de las 87 referencias y atributos DNP de D12–D17: `gestion/logs/SPEC-0024/01-jr-conformidad.md`. Pasarla a `hardware/componentes/campos-salidas.csv`.
- Los 12 cambios propuestos a `salidas.md` del mismo log (el 11 dice «§3.2», pero la l. 69 está en §2.1) y los «requiere DEC», que pasan a citar DEC-0008 (§0, §5, §11 nota 1, §13 y trazabilidad).
- En la raíz: unir IN1–6, IS1–6 y OUT_DEN con la hoja MCU y quitar sus no conexiones provisionales.
- `Value` del LED: «Rojo» en D4 y «LED» en D5; la tabla propone «Rojo» para D6–D11.

## Pendiente del usuario

- Medir la inductancia de la válvula (REL-03, `salidas.md` §5). No bloquea.
- Decidir si se versiona el `.kicad_pro` que KiCad 10 reescribe al abrir el proyecto (SPEC-0028).

## Para el layout (fase 4)

- Polígono BUS_24V de ≥ 300 mm² bajo cada BTT6050; el pad 15 de B.Cu y las vías ya cuelgan de VS.
- Vías y pasta del EPAD de U5 (VAL-0021-01-03), serigrafía «STATUS» junto a D5 y antena en el borde.
- Separación de 0,6 mm dentro de las huellas de salida (DEC-0008).
- Al unir hojas en la raíz cambian los nombres de red: resincronizar antes de mirar la paridad.

## Para la fabricación (fase 5)

- Comprobar en los Gerber el estado real de las vías del EP (F.Mask y B.Mask). Las vías rellenas y tapadas de JLCPCB encarecen la placa: consulta al usuario.
- Stock del BTT6050 en descenso (1 698 → 1 658 → 1 628; 10 placas usan 60): recomprobar antes de pedir.

## Mantenimiento

- Observaciones acumuladas de las fases 2 y 3: [SPEC-0028](specs/SPEC-0028-mantenimiento-fases-2-3.md).
- FW-02 (YAML coherente con el pinout): cuando exista `firmware/`, en la fase 6.
