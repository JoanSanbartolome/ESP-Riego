---
id: SPEC-0014
titulo: Limpieza de la copia de trabajo de la v2
fase: 3
estado: abierta
responsable: ing-esquematicos (esquema) e ing-layout (PCB)
revisor: ing-validacion
rama: spec/SPEC-0014-limpieza-v2
requisitos: [KIC-02, KIC-03, FAB-02, FAB-08]
depende_de: [SPEC-0013]
creada: 2026-11-05
cerrada:
validacion:
---

# SPEC-0014 · Limpieza de la copia de trabajo de la v2

> Petición del usuario (2026-11-05): limpiar la copia de trabajo de la v2 para tener un inicio limpio. Va **en paralelo con SPEC-0015** (recopilación de componentes), que no toca `hardware/v2/` ni carga proyectos en el MCP. Dentro de esta spec trabajan dos agentes, uno detrás de otro: **ing-esquematicos** limpia el esquema y después **ing-layout** limpia la PCB.

## Objetivo

`hardware/v2/` queda como esqueleto limpio de la v2:

- un esquema jerárquico con las 4 hojas (Alimentacion, MCU, Salidas, Conectores), sin los circuitos de la v1 que no encajan en los requisitos v0.4;
- una PCB vacía con el contorno preliminar de FAB-08.

ERC, DRC y paridad quedan sin errores.

## Alcance

- Incluye, en el **esquema** (ing-esquematicos):
  - Retirar de cada hoja los componentes, cables, etiquetas y pines jerárquicos de la v1 que no encajan en `docs/02-especificaciones-v2.md` v0.4, DEC-0003 y DEC-0004. Como mínimo:
    - el Wemos S2 Mini y sus tiras (MCU-01: ESP32-S3-WROOM-1 soldado);
    - los relés, los optoacopladores PS2705, los BC817 y su red, y los diodos de bobina (REL-03: *high-side* BTT6050);
    - el buck TPS54202 y su red (ALI-05: VIN ≥ 60 V);
    - el jack DC (ALI-02: borne);
    - el circuito del 4–20 mA (DEC-0002: sin sensor de nivel);
    - el DHT11 (AMB-01: sensor I²C en placa);
    - los bornes que no cumplan FAB-07.
  - Se conserva una pieza solo si cumple los requisitos v0.4 tal como está (p. ej. un taladro M3 o un `PWR_FLAG`), justificándolo en el log con el requisito. En caso de duda, se retira.
  - Cada hoja queda con un texto que dice qué bloque de la v2 llegará y con qué requisitos (p. ej. Alimentacion: ALI-01…ALI-13). La hoja raíz conserva las 4 hojas, sin pines jerárquicos huérfanos.
  - Inventario en el log de todo lo retirado (referencia, valor, motivo).
  - `comment 1` del cajetín (VAL-0013-02-03): en cada hoja, la descripción del bloque (p. ej. «Bloque de alimentación: entrada, protecciones, limitador y buck»); en la raíz, «Placa de control de riego». Así el título no sale repetido.
- Incluye, en la **PCB** (ing-layout, cuando el esquema esté limpio):
  - Sincronizar con el esquema: retirar todas las huellas, pistas, vías, zonas y textos de la v1 que ya no tengan componente.
  - Sustituir el contorno de la v1 (129,0 × 96,5 mm) por uno **preliminar** de 100 × 70 mm (FAB-08), con 4 taladros M3 en las esquinas. Un texto en `User.Comments` lo marca como preliminar, hasta el *floorplan*.
  - Reglas básicas del proyecto según FAB-02: pista y separación ≥ 0,2 mm, vía de 0,3/0,6 mm y cobre a borde ≥ 0,5 mm. Las clases de red y el `.kicad_dru` quedan para el layout.
  - Restos heredados de la v1 (VAL-0013-02-01 y 02):
    - `pcbplotparams/outputdirectory` vacío;
    - quitar de `embedded_files` la copia incrustada de `Cajetin_Kicad.kicad_wks`, o sustituirla por la hoja de la v2;
    - `comment 1` de la PCB, «Placa de control de riego».
- Excluye:
  - Añadir circuitos o elegir piezas de la v2: los bloques son specs propias.
  - Las librerías y las fichas de componentes (SPEC-0015).
  - Las tablas de librerías de `hardware/v2` para las piezas nuevas.
  - `hardware/v1-tfg/` y `hardware/libraries/`.

## Entradas

- Esta spec y `CLAUDE.md`.
- `docs/02-especificaciones-v2.md` v0.4, `gestion/decisiones/DEC-0002`, `DEC-0003` y `DEC-0004`.
- `docs/01-analisis-v1.md` §1, con la lista de bloques de la v1.
- `hardware/v2/` (copia de SPEC-0013) y su `README.md`.
- Las checklists `esquema.md` v5 y `layout.md` v5, solo en lo que aplique a una placa vacía.
- `gestion/informes/VAL-0013-02.md` (observaciones 01–03).

## Entregables

- `hardware/v2/` limpio: los esquemas, la PCB y el proyecto, con el `README.md` actualizado.
- Logs `gestion/logs/SPEC-0014/01-ing-esquematicos.md` y `02-ing-layout.md`.

## Criterios de aceptación

- [ ] `python herramientas/verificar.py hardware/v2` da ERC con 0 errores, DRC con 0 errores y 0 sin conectar, y paridad 0. Cada aviso que quede se justifica en el log.
- [ ] Ninguna pieza de la v1 que contradiga v0.4 sigue en el esquema ni en la PCB. Cada pieza conservada está justificada con su requisito.
- [ ] Las 4 hojas siguen en la jerarquía, cada una con su texto de bloque pendiente.
- [ ] La PCB tiene el contorno preliminar de 100 × 70 mm, los 4 taladros M3 y las reglas de FAB-02, sin restos de la v1: ni `embedded_files` del TFG ni `outputdirectory` fuera de `fabricacion/`.
- [ ] El cajetín, comprobado en los PDF exportados sobre una copia, muestra el título una vez y la descripción del bloque en cada hoja.
- [ ] `hardware/v1-tfg/` y `hardware/libraries/` no cambian. No quedan `.lck` ni `-backups/`, y el MCP queda con `close_project`.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-05 | coordinador | Crea la spec (abierta) | |
