---
spec: SPEC-0028
agente: ing-diseno
n: 02
fecha: 2026-11-16
estado: completado
---

# SPEC-0028 · 02 · ing-diseno

## Hecho

- `hardware/v2/conectores.kicad_sch`: sin cables. EN/IN de U14/U15 con `P:+5V:90` / `P:+3V3:90`, GND 2-4-6-8 de J10 y A0–A2 de U18 con `P:GND:270`; C48/C49 7,62 mm a la izquierda; nota «SLVS841G pp. 16–17»; fecha 2026-11-16. Descripción: `C:\Users\josan\AppData\Local\Temp\claude\2c54f79e79dd3002\3d01005c-f65e-42f6-96f0-c658602557c4\scratchpad\con2.json` (= `hoja.py extraer` de la hoja). Primera regeneración con `--forzar` (quitaba los 7 cables); la segunda, sin él.
- `hardware/v2/esp-riego.kicad_pcb`: `sincronizar.py` lleva los campos del paso 1 y el Value de U13, C23, C25 y D5 (96 campos; 0 huellas ni redes cambiadas).
- `herramientas/kicad/hoja.py`: `P:RED:giro` (símbolo de alimentación girado, `extraer` lo reproduce); `raiz` (pines de hoja y etiquetas/NC de la raíz, `--extraer`); `netlist --plan DOC [--seccion]`. `--help` en 30 líneas. `README.md`: tabla, formatos (descripción de la raíz, plan de conexiones) y límites.
- `herramientas/kicad/test_kicad.py` (copia de `herramientas/pruebas/` + casos): `Comun.test_modelo_de_respaldo`, `Verificar` (comprobar.py roto ×3 variantes; zona sin rellenar), `Jlc.test_resultados_y_buscar`, `Hoja.test_raiz`, `Hoja.test_netlist_plan`, giro `P:GND:270`, U13 en `Pcb.test_sincronizar…` y `Mutaciones.test_librerias_3d_respaldo`.
- Docs: `alimentacion.md` (cabecera, §0 y §7 alternativa de F1 = 0453010.MR, §3.2 TA10 descartado, §4 I_GND, §10.7 cerrado); `salidas.md` l. 4 → `docs/02` v0.5 (solo eso); `estudio-salidas.md` S7 → `salidas.md` §3; `mcu.md` §8.2 calentador 100 mA máx. (p. 9) → 0,55 A; `sensores.md` U13 = SHT40-AD1B-R2 (R3 pieza anterior; coste 1,76 $, SHT41 +1,51 $); `viabilidad-expansion.md` §5 inversor SN74LVC1G04DBVR (C7827; V_IH 2,0 V, SCES214AF p. 5); `conectores.md` Anexo A «En la hoja».

## Decisiones y desviaciones

- H1–H4: la hoja ya tenía `in_bom no` / `in_pos_files no` (regenerada en SPEC-0031) y la huella `exclude_from_pos_files exclude_from_bom`. Las 4 `footprint_symbol_mismatch` de la paridad de partida eran el Value de C23, C25, D5 y U13, no H1–H4.
- §4: I_GND (≤ 6 × 9 mA, P_4.2.5 p. 8) pasa por U1. Normal 3,554 A frente a 3,86 A mín. de la banda (margen 0,31 A, 7,9 %); borne 3,74 A; peor caso sin cambio, 4,77 A < 5,14 A.
- `test_librerias_fichas` ya fallaba antes de esta spec (C7519 y C25804 están ahora en otras fichas de bloque): muta también `bloque-conectores.md` y usa C23137 (solo en `bloque-alimentacion.md`).
- Calentador del SHT4x: en +5V daría 0,85 A durante el pulso, por encima de 0,835 A (ALI-12); se anota, sin cambio (no se usa, AMB-02).

## Verificación

- `verificar.py hardware/v2`: ERC 0; DRC 0 errores (448 sin conectar, sin rutar); paridad 0; [auto] OK 18, fallan 0, N/A 2. `campos.py revisar`: 0 / 0 / 0.
- `hoja.py netlist` frente a `main`, hoja Conectores: 0 diferencias (proyecto: 96, solo campos del paso 1, 0 de red). `netlist --plan conectores.md --seccion "Anexo A"`: 15 redes, 55 pines, 0 diferencias.
- `hoja.py raiz --extraer` + `raiz` sobre una copia: misma netlist, mismos UUID, ERC 0; render revisado.
- Batería (`herramientas/kicad/test_kicad.py`): 42 pruebas OK en 200 s. Mutaciones (repo falso): respaldo → None, sin `--refill-zones`, orden de `resultados`, etiquetas de `raiz` y «pines de más» del plan: los casos nuevos fallan.
- MCP no cargado: `esp-riego.kicad_pro` sin cambios.

## Pendiente

- Coordinador: mover `herramientas/kicad/test_kicad.py` a `herramientas/pruebas/`.
- `viabilidad-expansion.md` l. 166 cita TA10 como alternativa de F1 (dato fechado de SPEC-0006); fuera del alcance, sin tocar.
