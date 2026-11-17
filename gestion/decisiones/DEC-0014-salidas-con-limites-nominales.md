---
id: DEC-0014
titulo: Salidas con límites de uso propios, una válvula por salida y rueda libre montada
fecha: 2026-11-17
estado: aceptada
decide: usuario
specs: [SPEC-0033, SPEC-0034, SPEC-0032]
requisitos: [REL-03, REL-05, REL-10, ALI-12]
---

# DEC-0014 · Salidas con límites de uso propios, una válvula por salida y rueda libre montada

## Contexto

REL-03, REL-05 y ALI-12 dependen de la válvula: «1–2 válvulas por canal», la carga instalada de 3,5 A sale de «12 válvulas de 0,25 A», y la energía de desmagnetización se comprueba con la inductancia de la válvula. Desde DEC-0011, las válvulas instaladas (Bermad S-390-3-D, de 24 V AC, alimentadas en continua) están pendientes de medir, y esa medida bloquea la etiqueta `v2.0-sch` (`ESTADO.md`). Con el *clamp* integrado del BTT6050, la energía solo cumple hasta una inductancia máxima por válvula (`salidas.md` §5; DEC-0008, punto 2).

El 2026-11-17, el usuario pide que el diseño no se haga a medida de una válvula. Las salidas se diseñan a partir de las reglas vigentes, con una válvula por salida, y la placa publica sus límites de uso como lo haría un manual (por ejemplo, «no conectar más de X A»). La cifra de 4 A que puso de ejemplo no es una referencia.

## Opciones consideradas

1. **Medir la válvula instalada** y dimensionar con ella. Es lo que pedía DEC-0011: bloquea el esquema hasta tener la medida y deja la placa atada a esa válvula.
2. **Límites de uso propios de la placa**, independientes de la válvula. Con dos variantes para la carga inductiva:
   - a. mantener el *clamp* integrado y publicar una inductancia máxima en función de la corriente (curva E_AS). Sin coste, pero algunas válvulas quedan fuera;
   - b. montar la rueda libre D12–D17 (M7, C95872, *Basic*; la huella ya está en la placa). La energía se disipa en la bobina (E en el BTT ≈ 0) y no hay límite de inductancia. La válvula cierra en ≈ 3τ (30–50 ms con las bobinas típicas), lo que no importa en riego. Coste: 6 diodos *Basic*.
3. **Corriente nominal por salida:** 1 A (la de REL-05 hoy) o 0,5 A.

## Decisión

Decidida por el usuario el 2026-11-17: **opción 2b, con 1 A por salida**.

- **Una válvula (una carga) por salida.** Sustituye a «1–2 válvulas por canal».
- **1 A continuo por salida**, como límite de uso indicado en la serigrafía (REL-05).
- **Rueda libre D12–D17 montada** en las seis salidas. Sustituye el punto 2 de DEC-0008 (DNP). REL-03 deja de depender de la inductancia y de la medida de la válvula.
- **Suma de las salidas activas a la vez ≤ 3,5 A**, la carga instalada máxima que ya fijan ALI-12 y ALI-13, ahora como límite de uso y no como «12 válvulas de 0,25 A». No cambian la fuente, el limitador común ni su banda (3,5–4,9 A; DEC-0004).
- **Tabla de límites de uso** de las salidas, como la de un manual. La calcula `ing-diseno` a partir del circuito y de las reglas vigentes: tensión, tipo de carga (solo DC, a la tensión de entrada), corriente continua por salida, suma simultánea, resistencia mínima de la carga, corriente mínima para detectar una carga abierta (REL-10), fuga en reposo y cable.

## Consecuencias

- `docs/02` pasa a la v0.7 (SPEC-0033): se reescriben REL-03, REL-05, REL-10 y ALI-12, y §1, §2 y §6 cuando hablan de la válvula; hay un requisito nuevo con los límites de uso. En la misma versión entran el requisito del módulo de expansión pendiente de DEC-0012 (24 V y limitador propios, sin pasar 24 V por EXP-02) y el cierre de D9.
- SPEC-0034 (`ing-diseno`): `salidas.md` rehecho con la tabla de límites de uso; D12–D17 montados (sin DNP, en la BOM y el CPL); serigrafía de los límites.
- SPEC-0032 (integración) va después de SPEC-0034. La etiqueta `v2.0-sch` ya no depende de medir la válvula.
- Pasan a ser históricos en el diseño: el valor de 156 Ω de DEC-0002, la ficha de la Bermad que se usó como referencia en `estudio-salidas.md`, y la medida pendiente de DEC-0011 y de `ESTADO.md`. Lo que se mida en el prototipo (bobina caliente, margen del umbral de carga abierta) comprueba que la válvula del usuario está dentro de los límites; no condiciona el diseño.
- Coste: +6 diodos *Basic* por placa. `jr-conformidad` confirma el precio y el stock en SPEC-0034.
