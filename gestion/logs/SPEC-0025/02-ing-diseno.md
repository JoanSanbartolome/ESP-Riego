---
spec: SPEC-0025
agente: ing-diseno
n: 02
fecha: 2026-11-13
estado: completado
---

# SPEC-0025 · 02 · ing-diseno

## Hecho

- `hardware/libraries/esp-riego.pretty/`: `(attr smd)` en `Infineon_PG-TDSO-14_…_EP2.65x6.4mm` y `(attr through_hole)` en `TerminalBlock_Kangnex_WJ500V-5.08-2P_…`; nada más cambia (VAL-0027-01-02).
- `hardware/v2/salidas.kicad_sch`: A3, 87 piezas, 6 bloques de canal + común (R44, C45, C46) y notas; `hoja.py generar --campos campos-salidas.csv`. D12–D17 con `dnp yes`, `in_bom no`, `in_pos_files no`.
- `hardware/v2/esp-riego.kicad_sch`: hoja Salidas con 14 pines (BUS_24V, IN1–6, OUT_DEN entradas; IS1–6 salidas), recolocada a (190,5; 25,4) y 31,75 × 45,72; 28 etiquetas locales; fuera las 14 no conexiones (13 de MCU, 1 de BUS_24V de Alimentación).
- `hardware/v2/esp-riego.kicad_pcb`: `sincronizar.py --actualizar J1`: 87 huellas nuevas sin colocar, J1 recargada (through_hole), 19 pads con red renombrada (`/MCU/INn` → `/INn`, `/Alimentacion/BUS_24V` → `/BUS_24V`).
- `docs/diseno/salidas.md`: los 12 cambios de SPEC-0024 (stock de §9 y «Stock para 10 placas» con `stock-salidas.csv` del 2026-11-12; alternativa de R57–R62 = C126351); «requiere DEC» de §0, §5, §11 nota 1, §13.1, §13.8 y trazabilidad → DEC-0008; DEC-0008 en la cabecera.

## Decisiones y desviaciones

- Raíz: `hoja.py` no la toca; editada con Python en línea sobre la copia (pines `at … 180` + `justify left`, etiquetas `justify right bottom`). Candidato a herramienta (`hoja.py raiz`), igual que la comparación de la netlist con un plan de conexiones.
- Añadida a §9 una línea con el stock de las alternativas del 2026-11-12 (el cambio 5 las daba sin fila propia).

## Verificación

- `verificar.py hardware/v2`: ERC 0, DRC 0 errores (sin conectar 172 → 352: +180, solo huellas nuevas), paridad 0. `librerias.attr`, `esquema.campos` y `esquema.dnp` OK. Fallan `librerias.fichas` (9; nuevas C17713, C17902, C23253) y `librerias.gitattributes` (ya en SPEC-0028).
- Netlist frente al Anexo B y `mcu.md` §9.2 (script propio): 267 pines, 0 fallos; ningún pin fuera del plan; pines NC del BTT sin red. `hoja.py netlist` frente a `main`: solo piezas nuevas y los 19 renombres.
- `campos.py revisar`: 0 diferencias con la tabla; incoherencias 13 → 20, las 7 nuevas del tipo de SPEC-0028 (Datasheet y Fabricante frente a alimentación: C25803, C381466, C513710, C8465).
- Cajetín en el PDF (p. 2: «Salidas: 6 high-side BTT6050 y bornes», 2026-11-12, A3, 2/5); hoja y raíz revisadas con `vista.py`. `[juicio]`: cálculos sin cambios de valor; los de alimentación y MCU no aplican.

## Herramientas

- `herramientas/kicad/`: 31 usos (hoja.py pines 6, extraer 1, generar 4, netlist 1; sincronizar 2; vista 7; comprobar 4; campos revisar 4; huella 2) y verificar.py 4.
- Scripts en la carpeta temporal: 2 (`gen_salidas.py`, descripción JSON; `plan_salidas.py`, netlist frente al plan) y 7 de Python en línea (raíz ×2, atributos, `salidas.md`, ajustes del JSON ×3). MCP: no usado.

## Pendiente

- Para validación: en las huellas solo cambia el atributo (`huella.py`: smd con 40 pads; through_hole con 2).

- `librerias.fichas`: C17713, C17902 y C23253 sin ficha (`jr-conformidad`, p. ej. `bloque-salidas.md`).
