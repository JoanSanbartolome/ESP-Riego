---
id: SPEC-0005
titulo: Estudio de la tecnología de las salidas
fase: 2
estado: abierta
responsable: ing-esquematicos
revisor: ing-validacion
rama: spec/SPEC-0005-estudio-salidas
requisitos: [REL-01, REL-03, REL-05]
depende_de: [SPEC-0004]
creada: 2026-11-04
cerrada:
validacion:
---

# SPEC-0005 · Estudio de la tecnología de las salidas

> Rama apilada sobre `spec/SPEC-0004-requisitos-v02`: el estudio parte de los requisitos v0.2. Se integra en `main` después de SPEC-0004.

## Objetivo

Un estudio comparativo de las tecnologías posibles para las 6 salidas de riego, con pros, contras y limitaciones de cada una, que permita al usuario decidir (decisión D8). El usuario no quiere una solución que solo sirva para un tipo de válvula: el estudio tiene que decir qué cargas cubre cada opción y cuáles no.

## Alcance

- Incluye, como mínimo, estas opciones:
  1. Relé electromecánico: estándar tipo SRD-05 y subminiatura (p. ej. HF46F, Omron G5NB/G6), con contacto libre de potencial.
  2. SSR integrado de salida MOSFET (PhotoMOS u optoMOS, p. ej. AQY/AQV o G3VM), apto para AC y DC.
  3. Triac con optotriac (p. ej. MOC3063 o MOC3023 y un triac de nivel lógico), la solución clásica de los programadores de riego de 24 V AC.
  4. MOSFET discreto: *low-side*, *high-side* y bidireccional (*back-to-back*) para AC y DC.
  5. *High-side switch* inteligente con protección y diagnóstico (p. ej. familias BTS o VN/VNQ).
- Para cada opción, el estudio responde:
  - **Cargas que cubre:**
    - válvula de 24 V AC (la instalada);
    - válvula de 12/24 V DC;
    - válvula *latch* de 9–12 V DC (necesita inversión de polaridad);
    - bomba pequeña;
    - carga resistiva y LED.
  - **Corriente:**
    - de mantenimiento y de arranque (*inrush*) de una electroválvula de 24 V AC típica, con 1 y 2 válvulas por canal;
    - máximo por canal y total.
  - **Comportamiento eléctrico:** caída de tensión y disipación, corriente de fuga en reposo (¿puede mantener abierta una válvula?), protección de la carga inductiva (diodo, *snubber* o varistor).
  - **Seguridad:**
    - aislamiento;
    - estado seguro en el arranque, el reset y el flasheo (REL-04);
    - **modo de fallo** (abierto o cortocircuito). Si una salida falla en corto, la válvula se queda abierta y el riego no para; el estudio propone una mitigación, como una válvula maestra o un corte general.
  - **Salida alimentada o contacto libre (D2):**
    - si la opción permite alimentar las válvulas desde la propia entrada de 24 V AC, con un borne común como los programadores comerciales;
    - si permite dar un contacto libre de potencial;
    - cuántos polos de borne necesita por canal en cada caso.
  - **Placa:**
    - superficie y altura por canal;
    - impacto en el tamaño con 3 canales arriba y 3 abajo (FAB-07, FAB-08);
    - THT a mano o SMT en JLCPCB.
  - **Disponibilidad y coste:**
    - piezas en LCSC (*Basic* o *Extended*, stock y precio);
    - coste por canal y para los 6 canales, en cantidades de 5 y 10 placas, incluido el montaje en JLCPCB y el borne;
    - vida útil.
  - **Compatibilidad con el módulo de expansión** (SPEC-0006): si la misma etapa de salida se puede repetir en una placa de expansión.
- Excluye:
  - Dibujar esquemas en KiCad o abrir proyectos con el MCP. Las búsquedas de piezas (`search_jlcpcb_parts`, `get_jlcpcb_part` y el registro de piezas) no cargan ningún proyecto y se pueden usar.
  - Diseñar el módulo de expansión.

## Entradas

- `docs/02-especificaciones-v2.md` v0.2: §1, §2, REL-01 … REL-10, ALI-01 … ALI-04, FAB-07, FAB-08 y §7 (D2, D8).
- `gestion/decisiones/DEC-0002-objetivo-v2-revisado.md`.
- `docs/01-analisis-v1.md`, hallazgo H5 (etapa de relés de la v1).
- Datasheets de las piezas candidatas (WebSearch y WebFetch) y la base de piezas de JLCPCB del MCP.

## Entregables

- `docs/diseno/estudio-salidas.md`, con:
  - resumen para decidir (una tabla);
  - una sección por opción: funcionamiento, esquema de principio en texto, pros, contras, limitaciones y piezas candidatas con LCSC y precio;
  - matriz de cargas × opciones;
  - estimación de tamaño de placa por opción;
  - recomendación, con una alternativa y lo que habría que cambiar en REL-03, REL-05, REL-08, FAB-07 y FAB-08 según la opción;
  - fuentes (datasheets y notas de aplicación) con enlace.
- Log `gestion/logs/SPEC-0005/01-ing-esquematicos.md`.

## Criterios de aceptación

- [ ] Las 5 opciones del alcance están analizadas con los mismos criterios.
- [ ] La matriz de cargas × opciones cubre las 5 cargas de la lista, y cada celda dice sí, no o sí con condición, con la condición explicada.
- [ ] Cada pieza candidata tiene MPN, código LCSC, tipo (*Basic*/*Extended*), precio y fecha de consulta, y un enlace a su datasheet.
- [ ] Las corrientes de la electroválvula de 24 V AC y la fuga en reposo de cada opción están justificadas con una fuente o un cálculo.
- [ ] El modo de fallo de cada opción y la mitigación propuesta están explícitos.
- [ ] La recomendación no se da por decidida: queda como propuesta para la DEC del usuario (D8).

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-04 | coordinador | Crea la spec (abierta) | |
