---
id: SPEC-0038
titulo: Cambios del estudio de coste en hardware/v2
fase: 4
estado: abierta
responsable: ing-diseno
revisor: ing-validacion
rama: spec/SPEC-0038-cambios-del-estudio-de-coste-en
requisitos: [ALI-03, ALI-04, ALI-05, ALI-07, ALI-08, FAB-06, EXP-02, EXP-03]
depende_de: [SPEC-0037]
creada: 2026-11-23
cerrada:
validacion:
---

# SPEC-0038 · Cambios del estudio de coste en hardware/v2

## Objetivo

Aplicar en `hardware/v2` lo que decidió el usuario en DEC-0017 y DEC-0018, después de VAL-0037-01, de modo que:
- el esquema, la PCB, las fichas y la BOM reflejen las piezas nuevas;
- la colocación de partida `colocacion-b4.csv` siga en 0 obligatorias sobre la PCB real.

## Alcance

- Incluye:
  - paso 1 (`ing-diseno`):
    - **U4**: elegir un LDO de 3,3 V con stock en JLCPCB que cumpla ALI-07 y ALI-08, es decir, caída con los 3,9 V del cambio de U3 (`alimentacion.md` §3.8), estable con los cerámicos de la placa y θJA con la disipación de §4. Patillaje de SOT-223 si puede ser. Candidatos: AP2114H-3.3TRG1 (C150716) y TPTLV1117LV33DCYR (C52146079). Recalcular `alimentacion.md`, y su símbolo y huella si cambian.
    - **P3**: C3 y C27–C38 pasan a 100 nF 100 V X7R Basic (C28233), y C8 se queda en 220 nF (LMR36520 p. 20). Ajustar `salidas.md` §5 y `alimentacion.md`.
    - **J10**: pasa a BH254R-10P horizontal, con símbolo y huella; el mismo pinout (DEC-0017).
    - **JP1**: textos de su huella a 1,0 mm de alto y 0,15 mm de trazo, o quitados.
    - Sincronizar la PCB. Aplicar `colocacion-b4.csv` sobre una copia y pasarle `evaluar`.
  - paso 2 (`jr-conformidad`):
    - **P1**: D1, D2 y D3 pasan a las piezas equivalentes (C19077412, C19077586 y C7420364). Las fichas recogen las diferencias de VAL-0037-01-09.
    - Ficha de U4 y tabla de campos copiada al esquema.
    - **P2**: J1, J3, J4–J9 y J10, marcados en la BOM y el CPL como «a mano», fuera del montaje de JLCPCB.
    - BOM y coste por placa recalculados frente a `estudio-coste.md` §0.
- Excluye:
  - mover piezas en la PCB de `hardware/v2`: la colocación se aplica en la spec siguiente, cuando el usuario apruebe la imagen;
  - el rutado;
  - cambiar Q1 o R15 (DEC-0018);
  - la zona de U5 (D5);
  - FAB-08.

## Entradas

- `gestion/decisiones/DEC-0017-*.md` y `DEC-0018-*.md` (todo).
- `gestion/informes/VAL-0037-01.md` (hallazgos 01, 02, 04 y 09) y `VAL-0037-02.md`.
- `docs/diseno/estudio-coste.md`: §0, §2 (P3, P4), §6 (P2), §8.5, §8.10 y §9.
- `docs/diseno/alimentacion.md` §3.8, §4 y §7; `salidas.md` §5; `conectores.md` §0.
- `hardware/componentes/BH254R-10P.md`.
- `herramientas/kicad/README.md`: `sincronizar.py`, `campos.py`, `colocar.py` y `colocacion.py`.

## Entregables

- Paso 1:
  - esquema y PCB de `hardware/v2`;
  - librería con J10 y JP1;
  - `alimentacion.md` y `salidas.md` al día;
  - ficha de la pieza nueva de U4 con su datasheet;
  - salida de `evaluar` en el parte;
  - parte `01-ing-diseno.md`.
- Paso 2:
  - fichas de D1, D2 y D3 y tablas de campos;
  - campos copiados al esquema;
  - BOM y CPL de prueba con los THT «a mano»;
  - parte `02-jr-conformidad.md`.

## Criterios de aceptación

- [ ] U4 cumple ALI-07 y ALI-08 con el cálculo de `alimentacion.md`, que cita páginas del datasheet. Tiene stock en JLCPCB (cifra y fecha).
- [ ] C8 sigue en 220 nF 100 V X7R; C3 y C27–C38 están en C28233.
- [ ] J10 es BH254R-10P, con la red de cada pin igual que antes (netlist comparada pin a pin).
- [ ] Los textos de JP1 cumplen 1,0 mm de alto y 0,15 mm de trazo, o se han quitado.
- [ ] D1, D2 y D3 llevan las piezas de P1. Sus fichas tienen las cifras de VAL-0037-01-09.
- [ ] La BOM marca los THT «a mano», y el coste por placa cuadra con el estudio o explica la diferencia.
- [ ] `evaluar` de `colocacion-b4.csv` sobre una copia de `hardware/v2` da 0 obligatorias (`estudio-coste.md` §8.10).
- [ ] `verificar.py hardware/v2`: ERC 0, DRC 0 (sin conectar, aparte) y paridad 0; `campos.py revisar` sin diferencias.

## Plan de validación

Nivel **completo** (piezas y esquema; DEC-0005).

- Se reproduce de forma independiente:
  - la caída y la estabilidad del LDO nuevo frente a su datasheet;
  - la netlist de J10 pin a pin frente a la de `main`;
  - `evaluar` de b4 sobre `hardware/v2`;
  - la huella de J10 frente al dibujo de XFCN.
- Por muestreo: stock y precio de las piezas nuevas, campos de la BOM y fichas de P1.

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-23 | coordinador | Crea la spec (propuesta) | | | | |
| 2026-11-23 | coordinador | Abre la spec |  |  |  |  |
