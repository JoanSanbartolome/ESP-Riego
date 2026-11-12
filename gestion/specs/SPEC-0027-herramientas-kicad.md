---
id: SPEC-0027
titulo: Caja de herramientas de KiCad
fase: 3
estado: abierta
responsable: ing-diseno
revisor: ing-validacion
rama: spec/SPEC-0027-herramientas-kicad
requisitos: []
depende_de: [SPEC-0026]
creada: 2026-11-11
cerrada:
validacion:
---

# SPEC-0027 · Caja de herramientas de KiCad

## Objetivo

Las operaciones de diseño que los agentes repetían con scripts desechables (277 archivos, 874 KB en la carpeta temporal) quedan como herramientas versionadas y probadas en `herramientas/kicad/`, con salida corta, y `verificar.py` comprueba los puntos de checklist marcados `[auto: pendiente]`. Es la medida M1 de [DEC-0009](../decisiones/DEC-0009-orquestacion-v2.md), con la comprobación de restricciones de M10.

## Alcance

- Incluye, recuperando lo que ya funcionó (memoria de `ing-diseno` y scripts de `%TEMP%\claude\*\*\scratchpad`: `gen.py`, `sync.py`, `jlc.py`, `render.py`, `pins.py`, `cruce.py`, `mk_pcb.py`):
  - `jlc.py`: tipo, stock y precio de N códigos LCSC en una llamada, como tabla o CSV con fecha;
  - `campos.py`: copia `hardware/componentes/campos-<bloque>.csv` a los símbolos de una hoja y lista las incoherencias (campo que falta, misma pieza con campos distintos entre hojas, DNP);
  - `hoja.py`: genera o actualiza una hoja de esquema desde una descripción de piezas y redes;
  - `sincronizar.py`: netlist → PCB con `pcbnew` (huellas nuevas sin colocar, redes, campos y atributos), con paridad cero;
  - `colocar.py`: aplica a la PCB una tabla de colocación (referencia, x, y, giro, cara);
  - `vista.py`: imagen PNG de una hoja, de la placa, de una zona o de una huella;
  - `huella.py`: cotas de un `.kicad_mod` (pads, paso, taladros, vías y cobertura de pasta del pad expuesto);
  - `restricciones.py`: anchos, separaciones y vías por red de la PCB frente a una tabla de restricciones;
  - `comprobar.py`: los puntos `[auto: pendiente]` de las checklists de esquema, layout y librerías, que `herramientas/verificar.py` añade a su informe;
  - `herramientas/kicad/README.md` con una línea y un ejemplo por herramienta, y la batería `herramientas/pruebas/test_kicad.py`.
- Excluye:
  - el paquete de fabricación (se hará con la fase 5) y cualquier cambio en `hardware/v2`;
  - rutado automático y elección de herramienta de layout (prueba previa a la fase 4, M10).

## Entradas

- DEC-0009 (M1 y M10) y `gestion/README.md`.
- `.claude/agent-memory/ing-diseno/` (`reference_trucos_esquema.md`, `mcp-efectos-secundarios.md`, `reference_fuentes_piezas.md`) y `.claude/agent-memory/jr-conformidad/` (API de JLCPCB).
- Los puntos `[auto: pendiente]` de `gestion/checklists/` (Grep).
- `herramientas/verificar.py` y `hardware/v2` como banco de pruebas, siempre sobre una copia. Punto de partida en `e1b984f`: ERC 0, DRC 0 con 172 sin conectar, paridad 0.
- Los scripts de la carpeta temporal están en subcarpetas de cada `scratchpad` (`gen/gen.py`, `s19/sync.py`, `v18/mk_pcb.py`, `v21/`, `v22/`, `v24/`…): búsqueda recursiva.
- Estado anterior a `38090d2` (`047cabd`), ya extraído con `git archive`: `%TEMP%\esp-riego\SPEC-0027\pre-38090d2\hardware\` (`v2` y `libraries`). Se copia antes de usarlo.
- Python de KiCad, con `pcbnew`: `C:\Program Files\KiCad\10.0\bin\python.exe` (3.11). El del sistema es 3.12.

## Entregables

- De `ing-diseno`, todo en `herramientas/kicad/`, que es su zona y que crea esta spec: las herramientas, el `README.md` y la batería `test_kicad.py`, que localiza la raíz del repositorio buscando `CLAUDE.md` hacia arriba. El parte da las líneas del enganche de `comprobar.py` en `herramientas/verificar.py` y la lista de puntos de checklist cubiertos, cada uno con su script.
- Del coordinador, después de integrar (`herramientas/` y `gestion/` son su zona): el enganche en `herramientas/verificar.py`, la batería movida a `herramientas/pruebas/test_kicad.py` y las checklists con cada `[auto: pendiente]` cubierto cambiado a `[auto: <script>]`.

## Criterios de aceptación

- [ ] Cada herramienta tiene `--help`, da su resultado en 30 líneas como máximo y no modifica lo que lee: escribe solo en el destino que se le indica (`md5sum` antes y después).
- [ ] `sincronizar.py`, sobre una copia del estado anterior a `38090d2`, deja la paridad a cero como la dejó SPEC-0022.
- [ ] `hoja.py` regenera `mcu.kicad_sch` con la misma netlist que la hoja actual y ERC 0.
- [ ] `huella.py` da para la huella del BTT6050 las 10 vías de 0,3 / 0,6 mm y el 65 % de pasta de VAL-0024-01.
- [ ] `jlc.py` da para los códigos de `salidas.md` §9 el mismo tipo que la tabla de SPEC-0024.
- [ ] `campos.py` encuentra las incoherencias de VAL-0024-01-07 (`Datasheet`, `Fabricante` y `Value` del LED) en las hojas actuales.
- [ ] `verificar.py hardware/v2` informa de los puntos `[auto]` nuevos sin cambiar su resultado de ERC, DRC y paridad.
- [ ] `python herramientas/pruebas/test_kicad.py` pasa con el Python del sistema y sin red (lo que necesita `pcbnew` se lanza con el Python de KiCad), y `python -m py_compile` no da errores.

## Plan de validación

Nivel **completo**. Se reproduce de forma independiente: los seis criterios con resultado conocido y que ninguna herramienta toca lo que lee. Por muestreo: el README y los `--help`.

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-11 | coordinador | Crea la spec (propuesta) | | | | |
| 2026-11-12 | coordinador | Abre la spec |  |  |  |  |
| 2026-11-12 | ing-diseno | caja de herramientas de KiCad: nueve herramientas, README y batería | 01-ing-diseno | 395172 | 100 | 59 |
