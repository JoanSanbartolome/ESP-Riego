---
id: SPEC-0029
titulo: Bloque de sensores
fase: 3
estado: propuesta
responsable: ing-diseno
revisor: ing-validacion
rama: spec/SPEC-0029-bloque-sensores
requisitos: [AMB-01, AMB-02, KIC-02]
depende_de: []
creada: 2026-11-13
cerrada:
validacion:
---

# SPEC-0029 · Bloque de sensores

<!-- Objetivo, restricciones y criterios: sin pasos ni números de línea. Unas 60 líneas. Una spec de bloque o de hito de layout lleva sus pasos en «Alcance». -->

## Objetivo

> Propuesta: entradas, entregables, criterios y plan de validación se completan al abrirla.

El bloque de sensores de la v2 queda completo: `docs/diseno/sensores.md`, la pieza del SHT4x y la hoja `hardware/v2/sensores.kicad_sch` unida a la raíz, con ERC 0 y paridad 0.

## Alcance

- Incluye:
  - selección y cálculos: variante del SHT4x a partir de `hardware/componentes/SHT4x.md`, dirección I²C, desacoplo y consumo a 3,3 V;
  - restricciones de layout de AMB-02 (borde lateral según FAB-07, ranuras, sin cobre debajo, puente térmico), listas para `docs/diseno/restricciones.csv`;
  - símbolo, huella y modelo 3D, si no valen los oficiales;
  - hoja nueva y su hoja en la raíz, unida a `I2C_SDA` e `I2C_SCL` de la hoja MCU (GPIO41 y 42; R24 y R25 ya están en la hoja MCU);
  - campos (`hardware/componentes/campos-sensores.csv`), stock y fichas; PCB sincronizada con las huellas sin colocar.
- Excluye: colocación, ranuras y rutado (fase 4); el I²C de expansión (SPEC-0031).

## Entradas

<Archivos y secciones concretas que el responsable debe leer. La spec es la orden completa: un agente sin más contexto tiene que poder ejecutarla.>

-

## Entregables

-

## Criterios de aceptación

- [ ]

## Plan de validación

<Nivel (ligero o completo). Qué reproduce validación de forma independiente (lo que tiene riesgo: cotas, mapeo de pines, cálculos con poco margen) y qué comprueba por muestreo (lo mecánico: stock, campos, enlaces).>

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-13 | coordinador | Crea la spec (propuesta) | | | | |
