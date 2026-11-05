---
id: SPEC-0015
titulo: Recopilación de componentes de la v2
fase: 2
estado: abierta
responsable: jr-conformidad
revisor: ing-validacion
rama: spec/SPEC-0015-recopilacion-componentes
requisitos: [MCU-01, MCU-03, REL-03, ALI-04, ALI-13, AMB-01, FAB-05, FAB-07, KIC-01]
depende_de: [SPEC-0011]
creada: 2026-11-05
cerrada:
validacion:
---

# SPEC-0015 · Recopilación de componentes de la v2

> Petición del usuario (2026-11-05): recopilar los datasheets, modelos, símbolos y huellas de los componentes que se van a usar. Va **en paralelo con SPEC-0014** (limpieza de `hardware/v2`).
>
> Reglas del paralelo:
>
> - esta spec no toca `hardware/v2/`;
> - en el MCP solo se usan herramientas de consulta (`search_*`, `get_*`) y descargas que no carguen un proyecto;
> - **nunca `open_project`**, porque SPEC-0014 tiene el proyecto cargado.

## Objetivo

Cada componente ya elegido o candidato nombrado en los requisitos y decisiones de la v2 tiene:

- ficha en `hardware/componentes/`;
- datasheet del fabricante;
- símbolo, huella y modelo 3D listos para usar en KiCad 10;
- disponibilidad en JLCPCB/LCSC confirmada.

## Alcance

- Incluye estos componentes. La variante exacta de cada uno la fija después su bloque; aquí se recopila la familia:

  | Bloque | Componente | Origen |
  |---|---|---|
  | MCU | ESP32-S3-WROOM-1 (N8 o superior, la misma huella) | MCU-01 |
  | MCU | USBLC6-2SC6 (ESD del USB) | MCU-03 |
  | MCU | Conector USB-C 2.0 de 16 pines con montaje en JLCPCB | MCU-03 |
  | Salidas | BTT6050-1ERA (C534868), BTT6030-2ERA (C534865) y BSP752R (C112644) | DEC-0003 |
  | Entrada | SMBJ33A | ALI-04, DEC-0004 |
  | Entrada | Candidatos del limitador común: TPS2663 y LM5069 | ALI-13, DEC-0004 |
  | Sensores | SHT4x (SHT40/SHT41/SHT45) | AMB-01 |
  | Conectores | Borne de 2 polos de 5,08 mm WJ500V-5.08-2P (C8465) | FAB-07, estudio de salidas |

- Para cada uno:
  - **Ficha** `hardware/componentes/<MPN>.md` con la plantilla `gestion/plantillas/componente.md`:
    - datos clave para el diseño;
    - pinout;
    - recomendaciones de layout del fabricante;
    - código LCSC, tipo (*Basic*/*Extended*), stock y precio a la cantidad real (5 y 10 placas), con fecha;
    - enlaces al datasheet.
  - **Datasheet:** PDF oficial del fabricante, o de LCSC si el fabricante no lo publica, en `hardware/componentes/datasheets/`. Solo si ocupa ≤ 5 MB; si ocupa más, solo el enlace.
  - **Símbolo, huella y modelo 3D**, en el orden de preferencia de la checklist de librerías:
    1. librería oficial de KiCad 10: no se copia, la ficha cita `librería:nombre`;
    2. PartReel;
    3. JLCPCB/LCSC, convertido a formato nativo;
    4. creación desde el datasheet.
    
    Lo que no venga de la librería oficial va a la librería propia de la v2: `hardware/libraries/esp-riego.kicad_sym`, `esp-riego.pretty` y `3d/`. Los modelos 3D van en `.step`.
- Excluye:
  - Elegir piezas que aún no estén decididas (buck, LDO, LED, pasivos…), que llegan con su bloque.
  - Tocar `hardware/v2/`, incluidas sus tablas de librerías: las piezas se inscriben en la primera spec de bloque que las use.
  - Cambiar las librerías de la v1.

## Entradas

- Esta spec y `CLAUDE.md`.
- `docs/02-especificaciones-v2.md` v0.4, `DEC-0003` y `DEC-0004`.
- `docs/diseno/estudio-salidas.md` (§11 y la tabla de costes, con los códigos LCSC).
- `gestion/checklists/librerias.md` v2 y `gestion/plantillas/componente.md`.
- Las memorias de jr-conformidad sobre conversiones con `kicad-cli`.

## Entregables

- `hardware/componentes/<MPN>.md`, una por componente o familia, y `hardware/componentes/datasheets/`.
- `hardware/libraries/esp-riego.kicad_sym`, `esp-riego.pretty/` y `3d/`, solo con lo que no esté en la librería oficial.
- Log `gestion/logs/SPEC-0015/01-jr-conformidad.md`:
  - una tabla de componente, origen de cada pieza, LCSC, tipo y stock;
  - la sección «Requiere verificación de validación» con cada pieza creada o convertida.

## Criterios de aceptación

- [ ] Cada componente de la tabla tiene su ficha completa según la checklist de librerías v2, con datasheet y LCSC con fecha.
- [ ] Cada símbolo, huella y modelo 3D se puede resolver: de la librería oficial de KiCad 10 o de `hardware/libraries/esp-riego.*`, en formato nativo y sin rutas absolutas.
- [ ] Cada pieza que no viene de la librería oficial está en la sección «Requiere verificación de validación», con la página del datasheet de su dibujo recomendado.
- [ ] `hardware/v2/`, las librerías de la v1 y el TFG no cambian. El MCP no ha cargado ningún proyecto.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-05 | coordinador | Crea la spec (abierta) | |
