---
name: revision-hojas
description: Cómo validar una hoja de esquema de la v2 (SPEC-0019 alimentación): netlist XML de una copia, placa de prueba para DRC de las huellas, paridad frente a zonas de agentes, vías ThermalVias frente a FAB-02
metadata:
  type: feedback
---

SPEC-0019 (VAL-0019-01, 2026-11-06): la hoja estaba bien red a red. Los fallos estaban en la PCB que no se sincronizó y en una huella oficial que nadie había pasado por el DRC.

**Por qué:** la spec encargaba la sincronización a ing-esquematicos, pero `.kicad_pcb` está en sus `AJENOS` (`guardia.py`) y `sync_schematic_to_board` en sus `disallowedTools`. Sin las huellas en la PCB, `verificar.py` no ve sus errores de DRC.

**Cómo aplicarlo:**
- Copiar `hardware/v2` y `hardware/libraries` al *scratchpad* (rutas literales: la guardia no expande `$S`). Correr `verificar.py <copia> --salida <carpeta nueva>`. Exportar la netlist con `kicad-cli sch export netlist --format kicadxml` y volcarla con un script (`ElementTree`: refs, campos y nodos con `pinfunction`).
- Si las huellas no están en la PCB: hacer una **placa de prueba**. Se copia el `.kicad_pcb` y el `.kicad_pro` de v2 y se insertan los `.kicad_mod` con `(at x y)` antes del último `)`. Luego `kicad-cli pcb drc --format json`. Así salen los `drill_out_of_range`.
- Las huellas oficiales `*_ThermalVias` de TI QFN (p. ej. RGE0024H) traen vías de 0,2 / 0,5 mm: incumplen FAB-02 (0,3 / 0,6). Ya van dos veces (U2 en VAL-0018-02-01, U1 en VAL-0019-01-02).
- **Paridad:** «piezas sin colocar» = sincronizadas sin posición, no ausentes. Comprobar siempre que cada entregable cae en la zona del agente responsable.
- Para comprobar el cajetín, `Read` del PDF con `pages` basta. Los scripts con `python -I` necesitan `sys.stdout.reconfigure(encoding='utf-8')`.
- Los símbolos `power:` globales para +5V, +3V3 y GND son aceptables aunque la spec pida etiquetas jerárquicas (`mcu.md` Anexo C).

Relacionado: [[revision-piezas]], [[revision-alimentacion]], [[comprobaciones-utiles]].
