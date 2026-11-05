# SPEC-0013 · Log 01 · jr-conformidad

Rama: spec/SPEC-0013-copia-v2. Sin `.lck` al empezar. No se usó el MCP (edición de texto y `kicad-cli`).

## Cambios

- Copiados a `hardware/v2/` los 7 archivos del proyecto, `sym-lib-table` y `fp-lib-table` (sin cambios; las rutas `${KIPRJMOD}/../libraries/...` valen).
- Renombrados: `Control_De_Riego.*` a `esp-riego.*`; `allimentacion` a `alimentacion`, `wemos_s2mini` a `mcu`, `modulo_reles` a `salidas`.
- Raíz: `Sheetname`/`Sheetfile` según la tabla de la spec y `(project "esp-riego")` en todas las instancias (esquemas).
- `.kicad_pro`: `meta.filename`, `step`, `bom_export_filename` y la lista `sheets` con los nombres nuevos.
- `.kicad_pcb`: `sheetname`/`sheetfile` de las huellas y prefijo de hoja en los nombres de red (`/Modulo_reles/` a `/Salidas/`, `/ESP32_S2/` a `/MCU/`, `/Conectores y agujeros PCB/` a `/Conectores/`). Sin esto la paridad daba 93 en lugar de 77.
- Cajetín (5 esquemas y PCB): título «ESP-Riego v2», rev 2.0-dev, fecha 2026-11-05, empresa y comment 1 «Joan San Bartolomé Ferri»; quitados los comentarios y la empresa del TFG. Hoja de dibujo sin cambios.
- `hardware/v2/README.md` creado.

## Verificación

| | v1-tfg (antes) | v2 (después) |
|---|---|---|
| ERC | 1 (pin_to_pin) | 1 (pin_to_pin) |
| DRC | 40 (1 starved_thermal, 39 lib_footprint_mismatch, 0 sin conectar) | 40 (igual) |
| Paridad | 77 (61, 10, 6) | 77 (61, 10, 6) |

- Netlist `kicad-cli` v1 (copia en scratchpad con tablas absolutas) frente a v2: 61 referencias con mismos valores y huellas, 70 redes, mismas conexiones; los nombres coinciden tras mapear el prefijo de hoja.
- PCB: 61 huellas, 262 segmentos, 36 vías y 3 zonas en ambas; `diff` de la PCB v1 (con los mapeos aplicados) frente a v2 solo difiere en el cajetín.
- Búsqueda de `Control_De_Riego|allimentacion|wemos_s2mini|modulo_reles|ESP32_S2|agujeros` en `hardware/v2`: sin resultados. Sin rutas absolutas, `.lck`, `.kicad_prl` ni `-backups/`. `hardware/v1-tfg` y `hardware/libraries` sin tocar.

## Requiere verificación de validación

Ninguna pieza nueva ni modificada (símbolos, huellas, modelos 3D): no aplica.

## Pendiente

- La PCB sigue con los modelos 3D `.wrl` (README de v1-tfg): corrección prevista en la copia v2, fuera de esta spec.
- `docs/03-plan-de-diseno.md`: lo actualiza el coordinador.
