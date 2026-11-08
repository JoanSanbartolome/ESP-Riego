---
id: DEC-0008
titulo: LED de estado rojo, rueda libre sin montar y separación de 0,6 mm en las huellas de salida
fecha: 2026-11-08
estado: aceptada
decide: usuario
specs: [SPEC-0022, SPEC-0024, SPEC-0025]
requisitos: [MCU-07, REL-03, FAB-02, FAB-03]
---

# DEC-0008 · LED de estado rojo, rueda libre sin montar y separación de 0,6 mm en las huellas de salida

## Contexto

Tres puntos que SPEC-0022 y SPEC-0023 dejaron al usuario:

1. **D5 (LED de estado, MCU-07).** Por DEC-0007 pasó del KT-0603YG verde-amarillo (C2289, Extended) al KT-0603R rojo (C2286, Basic). Deja de distinguirse por color del LED de alimentación D4, también rojo (VAL-0021-01, VAL-0022-01-04).
2. **D12–D17 (rueda libre, REL-03).** El *clamp* del BTT6050 cumple E_AS con L ≤ 2,69 H por válvula (Bermad) o ≤ 1,10 H (genérica); la inductancia aún no está medida (`salidas.md` §5, §13.1).
3. **Separación de `Salidas` (FAB-03).** FAB-03 pide ≥ 1 mm, pero los huecos entre pads de U7–U12 (BTT6050), R57–R62 (R_OL) y C33–C38 (C_OUT) son de 0,62–0,90 mm (`salidas.md` §11, nota 1; VAL-0023-01-01).

## Opciones consideradas

1. D5: rojo (Basic, serigrafía «STATUS») o verde-amarillo (Extended, distinto color).
2. D12–D17: sin montar con huella, o montados por defecto (cambia «con el *clamp* integrado» de REL-03).
3. Separación: excepción de 0,6 mm dentro de esas huellas, o buscar huellas con 1 mm (no hay en el BTT6050, cuyo paso es fijo).

## Decisión

1. **D5 rojo** (KT-0603R, C2286), identificado con la serigrafía «STATUS» junto a D5.
2. **D12–D17 sin montar (DNP)**, con su huella (M7, C95872) en la placa por si la inductancia medida no cumple. REL-03 no cambia: la carga inductiva la absorbe el *clamp* integrado.
3. **Excepción de 0,6 mm** en la clase `Salidas` cuando uno de los dos objetos es un pad de U7–U12, R57–R62 o C33–C38 o está dentro de su patio; 1 mm en el resto (pistas y polígonos). Condición del usuario: que cumpla los parámetros de fabricación de la clase de trabajo. Cumple: FAB-02 (JLCPCB estándar con margen) pide separación ≥ 0,2 mm, y 0,6 mm es la que exige IPC-2221 B2 (capa externa sin recubrir) hasta 100 V, por encima de los ≤ 75 V que ve OUT_n.

## Consecuencias

- `docs/02` pasa a v0.5: FAB-03 recoge la excepción.
- VAL-0022-01-04 queda resuelto.
- SPEC-0024: D12–D17 con campo DNP, fuera de BOM y CPL.
- SPEC-0025 y el layout de salidas: la regla de 0,6 mm se escribe en las reglas de diseño (sin excepciones manuales en el DRC), y los «requiere DEC» de `salidas.md` (§0, §5, §11 nota 1, §13 y trazabilidad) pasan a citar esta DEC.
- Si la inductancia medida no cumple, montar D12–D17 sí cambia REL-03 y se consulta de nuevo.
