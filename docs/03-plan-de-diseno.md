# Plan de diseño

Hoja de ruta para pasar de la PCB del TFG (v1) a la v2 definida en [02-especificaciones-v2.md](02-especificaciones-v2.md).

## Fases e hitos

| Fase | Contenido | Entregable | Etiqueta |
|---|---|---|---|
| 0 | Repositorio, análisis de la v1, especificaciones y plan | `docs/` | — |
| 1 | Importar el proyecto del TFG y migrarlo a KiCad 10 | `hardware/v1-tfg/` abre sin librerías rotas | `v1.1-tfg` |
| 2 | Arquitectura y selección de componentes | Diagrama de bloques, presupuesto de potencia, BOM preliminar con LCSC, pinout | — |
| 3 | Esquema v2 | Esquema jerárquico con ERC limpio y revisado | `v2.0-sch` |
| 4 | Layout v2 | PCB con DRC y paridad limpios, comprobada en 3D dentro de la caja | `v2.0-layout` |
| 5 | Fabricación | Gerber, taladros, BOM/CPL para JLCPCB, revisión DFM y pedido | `v2.0` |
| 6 | Firmware y validación | YAML de ESPHome v2 e informe de pruebas | `v2.0-validada` |

## Fase 1: importación de la v1

La v1 se conserva **tal como se fabricó**: solo se arreglan las rutas de librería y el formato de archivo, sin tocar el diseño.

- [ ] Copiar del TFG, sin modificar el original, solo los fuentes: `.kicad_pro`, las 5 hojas de la jerarquía y `.kicad_pcb`. Se excluyen backups, `fp-info-cache`, `.kicad_prl` y los `.rar`.
- [ ] Guardar `Panel_Control.kicad_sch` como referencia (no está en la jerarquía). No se importa `untitled.kicad_sch`, que es un duplicado del Wemos.
- [ ] Pasar las librerías usadas a formato nativo (`.kicad_sym` / `.pretty`) en `hardware/libraries/`, incluidas las que hoy se leen de JSON de EasyEDA.
- [ ] Reescribir `sym-lib-table` y `fp-lib-table` con rutas `${KIPRJMOD}/../libraries/...`.
- [ ] Abrir y guardar en KiCad 10 para migrar el formato.
- [ ] Comprobar que ERC, DRC y paridad dan las mismas incidencias que el análisis, es decir, que la migración no ha cambiado nada.
- [ ] Commit y etiqueta `v1.1-tfg`.

## Fase 2: arquitectura y selección de componentes

- [ ] Cerrar las decisiones abiertas D2–D9; D8 (tecnología de las salidas) con el estudio de SPEC-0005 y D9 (módulo de expansión) con el informe de SPEC-0006.
- [ ] Diagrama de bloques definitivo y presupuesto de potencia por raíl (entrada rectificada, 5 V, 3,3 V).
- [ ] Seleccionar componentes con disponibilidad en JLCPCB/LCSC y una alternativa para cada pieza crítica: puente rectificador, buck, LDO, protecciones, etapa de salida, sensor de temperatura y humedad, y conectores.
- [ ] Tabla de asignación de GPIO según MCU-05.
- [ ] Cálculos: condensador de bulk y rizado, UVLO, divisor de la tensión rectificada, protección de las salidas, corriente de los LED y anchura de pistas (IPC-2152).
- [ ] Documentar todo en `docs/04-arquitectura.md`.

## Fase 3: esquema v2

- [ ] Proyecto `hardware/v2/` con las hojas `alimentacion`, `mcu`, `salidas`, `sensores` y `conectores`.
- [ ] Campos en cada símbolo: `Value`, `Footprint`, `LCSC Part#`, `MPN` y `Datasheet`.
- [ ] ERC sin errores.
- [ ] Revisión: pines de arranque, estado de las salidas en el reset, polaridades, ESD en todos los conectores de campo, test points.

## Fase 4: layout v2

- [ ] *Floorplan*: salidas 1–3 en el borde superior y 4–6 en el inferior, junto con la entrada y la expansión (REL-09, FAB-07); antena en un lateral, lejos de las salidas; buck junto a la entrada; sensor de temperatura y humedad en un borde, aislado térmicamente (AMB-02).
- [ ] Clases de red y `.kicad_dru` (FAB-02, FAB-03, KIC-04).
- [ ] Rutado: primero potencia y salidas, después analógica y por último señales. Planos de GND con cosido de vías.
- [ ] DRC sin errores y paridad esquema↔PCB limpia.
- [ ] Revisión en 3D con la caja ventilada (D5).

## Fase 5: fabricación

- [ ] Exportar con `kicad-cli` a `fabricacion/v2.0/`: Gerber, taladros, BOM, CPL y PDF de esquema y PCB.
- [ ] Revisión DFM en JLCPCB y comprobación de la rotación de los componentes en el CPL.
- [ ] Pedido y registro de coste.

## Fase 6: firmware y validación

- [ ] `firmware/control-riego.yaml` con el pinout v2 y `secrets.yaml` fuera del repositorio.
- [ ] Ejecutar los criterios de aceptación de las especificaciones (§6).
- [ ] Informe de validación en `docs/validacion/` y lista de mejoras para una v2.1.

## Organización del trabajo

Cada fase se divide en specs atómicas (`SPEC-NNNN`) que ejecutan los agentes de Claude Code bajo la dirección del coordinador. Cada spec tiene su propia rama y solo se integra en `main` con un informe de validación aprobado. Cada hito se marca con una etiqueta. Roles, ciclo de vida, formato de los commits y consultas de auditoría: [gestion/README.md](../gestion/README.md).

## Herramientas

- KiCad 10 y `kicad-cli` (`herramientas/verificar.py` para ERC, DRC y paridad).
- Servidor MCP de KiCad (edición, análisis y búsqueda de piezas JLCPCB) usado por los agentes desde Claude Code.
- `herramientas/gestion.py` para specs, tablero y trazabilidad.
- JLCPCB / LCSC para la fabricación y los componentes.
