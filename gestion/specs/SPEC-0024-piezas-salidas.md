---
id: SPEC-0024
titulo: Piezas del bloque de salidas
fase: 2
estado: propuesta
responsable: jr-conformidad
revisor: ing-validacion
rama: spec/SPEC-0024-piezas-salidas
requisitos: [REL-01, REL-03, REL-05, REL-07, REL-10, FAB-02, FAB-11, KIC-01]
depende_de: [SPEC-0023]
creada: 2026-11-06
cerrada:
validacion:
---

# SPEC-0024 · Piezas del bloque de salidas

## Objetivo

Todas las piezas de la lista de `docs/diseno/salidas.md` tienen símbolo, huella y 3D resolubles desde `hardware/v2`, con sus campos completos, su tipo de JLCPCB (Basic/Extended) y su stock confirmados con fecha, y sus fichas en `hardware/componentes/`.

## Alcance

- Incluye:
  - símbolos, huellas y modelos 3D que falten, reutilizando las librerías oficiales de KiCad y las de `hardware/libraries/` (BTT6050-1ERA y WJ500V-5.08-2P ya existen);
  - D6–D11 usan la ficha `hardware/componentes/KT-0603R.md` (SPEC-0022, polaridad ② = cátodo = pad 1); proponer el cambio de `salidas.md` l. 434 («ficha propia si jr-conformidad la pide») y el stock desactualizado de D4 en `bloque-alimentacion.md`;
  - huellas con vías conforme a FAB-02 (0,3 / 0,6 mm) o sin vías (checklist de esquema v6);
  - campos `LCSC`, `MPN`, `Fabricante`, `Datasheet`, tipo Basic/Extended y stock de todas las piezas;
  - fichas del Anexo A de `salidas.md` y actualización de las existentes;
  - cambios de compra que abaratan o facilitan la fabricación (DEC-0007).
- Excluye: editar hojas del esquema o la PCB; cambiar valores elegidos en SPEC-0023.

## Entradas

- `docs/diseno/salidas.md` y `gestion/logs/SPEC-0023/01-ing-esquematicos.md`.
- `hardware/libraries/`, `hardware/componentes/` y checklists `librerias.md` (v3) y `esquema.md` (v6).

## Entregables

- Librerías y fichas actualizadas.
- Log `gestion/logs/SPEC-0024/01-jr-conformidad.md` con el repaso de la checklist, la tabla de stock y la de campos por referencia.

## Criterios de aceptación

- [ ] Cada pieza de la lista tiene símbolo, huella y 3D, con los pines comprobados contra el datasheet (página citada).
- [ ] Ninguna huella lleva vías fuera de FAB-02.
- [ ] Campos completos y stock de JLCPCB confirmado en la fecha.
- [ ] Checklist de librerías v3 pasada punto por punto.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-06 | coordinador | Crea la spec (propuesta) | |
