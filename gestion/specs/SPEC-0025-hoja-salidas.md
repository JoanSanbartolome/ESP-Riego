---
id: SPEC-0025
titulo: Hoja de salidas en el esquema v2
fase: 3
estado: abierta
responsable: ing-diseno
revisor: ing-validacion
rama: spec/SPEC-0025-hoja-salidas
requisitos: [REL-01, REL-03, REL-04, REL-05, REL-06, REL-07, REL-08, REL-10]
depende_de: [SPEC-0024, SPEC-0022]
creada: 2026-11-06
cerrada:
validacion:
---

# SPEC-0025 · Hoja de salidas en el esquema v2

## Objetivo

`hardware/v2/salidas.kicad_sch` pasa a ser el bloque de salidas de la v2 según `docs/diseno/salidas.md`: 6 canales con las piezas de SPEC-0024, unida a la raíz y sincronizada con la PCB (sin colocar), con ERC 0 y paridad 0. Es el piloto del ciclo nuevo (DEC-0009) y de `herramientas/kicad/`: lo que se repite se hace con esas herramientas, no con scripts nuevos en la carpeta temporal.

## Alcance

- Incluye:
  - **Paso 1 (`jr-conformidad`).** La tabla de campos de las 87 referencias pasa a `hardware/componentes/campos-salidas.csv`, con el formato de `herramientas/kicad/README.md` («Formatos»): `Value` «Rojo» en D6–D11 y D12–D17 con `DNP` = sí. Recomprobar tipo y stock de los códigos de `salidas.md` §9 con `jlc.py` y dejar la tabla con fecha junto al CSV (`hardware/componentes/stock-salidas.csv`).
  - **Paso 2 (`ing-diseno`).**
    - Antes de sincronizar: `(attr smd)` en la huella del BTT6050 y `(attr through_hole)` en la del WJ500V, en la librería `esp-riego` y en J1 de la PCB (VAL-0027-01-02), para que `librerias.attr` pase.
    - La hoja de salidas con `hoja.py generar --campos hardware/componentes/campos-salidas.csv`, según `salidas.md` Anexo B (redes, etiquetas jerárquicas y numeración por canal), D12–D17 con DNP (DEC-0008).
    - En la raíz, los pines de hoja de Salidas (`BUS_24V`, IN1–6, IS1–6, OUT_DEN) unidos con los de las hojas MCU y Alimentación, y fuera las no conexiones provisionales de esos pines de la hoja MCU. `hoja.py` no toca la raíz: MCP o edición del archivo.
    - Sincronizar la PCB con `sincronizar.py` (huellas nuevas sin colocar).
    - En `salidas.md`: los 12 cambios propuestos en el log de SPEC-0024 (el 11 está en §2.1, l. 69, no en §3.2) y los «requiere DEC» de §0, §5, §11 nota 1, §13 y trazabilidad, que pasan a citar DEC-0008.
- Excluye: colocación y rutado; unificar los campos entre hojas (D5 «LED», `Fabricante` de alimentación, «100n»/«100nF»: SPEC-0028); otras hojas, salvo sus no conexiones en la raíz.

## Entradas

- `docs/diseno/salidas.md`: §2–§9 y Anexo B.
- `gestion/logs/SPEC-0024/01-jr-conformidad.md`: «Tabla de campos por referencia» y «Cambios propuestos a `docs/diseno/salidas.md`»; `03-jr-conformidad.md`, «Lo corregido por hallazgo».
- `herramientas/kicad/README.md` (herramientas, formatos y límites conocidos).
- DEC-0008. Checklists `gestion/checklists/esquema.md` (v9) y `librerias.md` (el punto del atributo).
- Punto de partida (`main` en `037f0e8`): `verificar.py hardware/v2` da ERC 0, DRC 0 con 172 sin conectar, paridad 0, y FALLA en `librerias.attr`, `librerias.fichas` y `librerias.gitattributes`.

## Entregables

- `jr-conformidad`: `hardware/componentes/campos-salidas.csv`, `hardware/componentes/stock-salidas.csv` y parte `gestion/logs/SPEC-0025/01-jr-conformidad.md`.
- `ing-diseno`: `hardware/v2/salidas.kicad_sch`, `hardware/v2/esp-riego.kicad_sch`, `hardware/v2/esp-riego.kicad_pcb`, las dos huellas en `hardware/libraries/`, `docs/diseno/salidas.md` y parte `gestion/logs/SPEC-0025/02-ing-diseno.md`, que cuenta los scripts escritos en la carpeta temporal y los usos de `herramientas/kicad/`.

## Criterios de aceptación

- [ ] Cada pieza, valor, huella y pin de la hoja coinciden con `salidas.md` §9 y Anexo B (`hoja.py netlist` o netlist exportada).
- [ ] `verificar.py hardware/v2`: ERC 0, DRC 0 errores, paridad 0; `librerias.attr`, `esquema.campos` y `esquema.dnp` pasan. Los «sin conectar» suben solo por las huellas nuevas, y el parte da la cifra.
- [ ] `campos.py revisar hardware/v2`: 0 diferencias con `campos-salidas.csv`; ninguna incoherencia nueva entre hojas salvo las de SPEC-0028.
- [ ] Mismo orden de pines en los 6 bornes: pin 1 = OUTn, pin 2 = GND (REL-06).
- [ ] D12–D17: DNP en el símbolo y en la huella, fuera de BOM y CPL (DEC-0008).
- [ ] Ninguna pieza de la hoja usa una librería de la v1.
- [ ] En la raíz, ninguna no conexión en un pin de hoja que ahora esté unido, y las redes IN1–6, IS1–6, OUT_DEN y BUS_24V llegan a los GPIO de `salidas.md` Anexo B.

## Plan de validación

Nivel **completo**. Se reproduce de forma independiente: la netlist de la hoja frente al Anexo B (un canal entero y los pines de U7–U12 frente a la Tabla 2, p. 4 del BTT6050), las uniones de la raíz con los GPIO, el DNP de D12–D17 en BOM y CPL exportados, y los atributos de las dos huellas. Por muestreo: tres filas de `campos-salidas.csv` y de `stock-salidas.csv` frente a LCSC, y tres de los 12 cambios de `salidas.md`.

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-06 | coordinador | Crea la spec (propuesta) | |
| 2026-11-11 | coordinador | Responsable: ing-diseno; se completa con el ciclo nuevo al abrirla | DEC-0009 |  |  |  |
| 2026-11-12 | coordinador | Abre la spec |  |  |  |  |
| 2026-11-12 | jr-conformidad | campos-salidas.csv (87 refs) y stock del 2026-11-12 | 01-jr-conformidad | 69447 | 13 | 2 |
