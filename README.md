# ESP-Riego

Controlador inalámbrico de riego por goteo basado en ESP32 e integrado en Home Assistant mediante ESPHome.

Este repositorio contiene el rediseño (v2) de la PCB desarrollada en el Trabajo Fin de Grado de Joan San Bartolomé Ferri. El proyecto original del TFG no se modifica: se importa como referencia y la v2 se diseña desde cero a partir de su análisis.

La v2 tiene 6 salidas de 24 V DC con *high-side* inteligente y limitador común, sensor de temperatura y humedad en placa, pulsadores y un conector de expansión por I²C.

## Estado

| Fase | Estado | Etiqueta |
|---|---|---|
| 0. Análisis, especificaciones y plan | ✅ | — |
| 1. Importación de la v1 a KiCad 10 | ✅ | `v1.1-tfg` |
| 2. Arquitectura y componentes | ✅ (falta la alternativa de U1) | — |
| 3. Esquema v2 | ✅ | `v2.0-sch` |
| 4. Layout v2 | ⏳ (prueba de colocación, SPEC-0037) | — |
| 5. Fabricación | — | — |
| 6. Firmware y validación | — | — |

El esquema tiene ERC limpio, 12 páginas y 187 piezas, y cuesta 27,46 USD por placa en un pedido de 5. Lo que toca ahora está en [`gestion/ESTADO.md`](gestion/ESTADO.md).

## Documentación

1. [Análisis de la PCB v1](docs/01-analisis-v1.md): estado de la placa del TFG y hallazgos.
2. [Especificaciones de la PCB v2](docs/02-especificaciones-v2.md): requisitos y criterios de aceptación.
3. [Plan de diseño](docs/03-plan-de-diseno.md): fases e hitos.
4. [Arquitectura](docs/diseno/arquitectura.md): bloques, presupuesto de potencia y GPIO. Cada bloque tiene su documento de cálculos y restricciones de layout en [`docs/diseno/`](docs/diseno/): alimentación, MCU, salidas, sensores y conectores.
5. [Decisiones](gestion/decisiones/): `DEC-0001` … `DEC-0016`.
6. [Sistema de gestión](gestion/README.md): roles, ciclo de vida de las specs, commits y auditoría. Estado de cada spec en el [tablero](gestion/TABLERO.md) y de cada requisito en la [trazabilidad](gestion/TRAZABILIDAD.md).
7. Salidas del esquema: [BOM preliminar](fabricacion/v2.0-sch/bom.csv) y [PDF](fabricacion/v2.0-sch/esquema.pdf).

## Organización del trabajo

El diseño lo hacen agentes de Claude Code coordinados por la sesión principal ([DEC-0001](gestion/decisiones/DEC-0001-orquestacion-de-agentes.md), [DEC-0009](gestion/decisiones/DEC-0009-orquestacion-v2.md) y [DEC-0010](gestion/decisiones/DEC-0010-agentes-en-opus.md)):

| Agente | Responsable de |
|---|---|
| Coordinador | Specs, órdenes, git, tablero y comunicación |
| `ing-diseno` | Cada bloque de principio a fin: cálculos, piezas, esquema y PCB, y las herramientas de KiCad |
| `jr-conformidad` | Tipo y stock, fichas, campos, BOM, CPL y paquetes de fabricación |
| `ing-validacion` | Revisión contra especificaciones e informes con veredicto |

Cada unidad de trabajo es una spec, con un bloque o un hito de layout. Tiene su propia rama, que se valida antes de integrarse en `main` con `herramientas/gestion.py` (`abrir`, `revisar`, `integrar`, `cerrar`).

## Estructura

```
.
├── docs/            Análisis, especificaciones, plan y diseño por bloque (docs/diseno/)
├── hardware/
│   ├── libraries/   Símbolos, huellas y modelos 3D propios (rutas ${KIPRJMOD})
│   ├── componentes/ Fichas de componentes y tablas de campos
│   ├── v1-tfg/      Proyecto del TFG migrado a KiCad 10
│   └── v2/          Nuevo diseño (proyecto esp-riego)
├── fabricacion/     Salidas de fabricación por versión
├── gestion/         Estado, specs, partes, informes, decisiones, checklists y plantillas
├── herramientas/    gestion.py, verificar.py y kicad/ (herramientas de diseño)
├── .claude/         Agentes, hooks de guarda y de auditoría, y memoria de los agentes
└── .githooks/       Validación de los mensajes de commit
```

`firmware/` (configuración ESPHome) se crea en la fase 6.

## Herramientas

- `python herramientas/verificar.py hardware/v2`: ERC, DRC, paridad esquema↔PCB y los puntos `[auto]` de las checklists, sin modificar el proyecto.
- `herramientas/kicad/`: hojas de esquema desde una descripción (`hoja.py`, `dibujo.py`), campos y stock (`campos.py`, `jlc.py`), sincronización con la PCB, restricciones y colocación. Su [README](herramientas/kicad/README.md) dice qué hace cada una.
- `python herramientas/gestion.py`: ciclo de las specs, tablero y trazabilidad.

## Requisitos

- [KiCad 10](https://www.kicad.org/), con su Python para las herramientas que usan `pcbnew`. Se buscan solas en `C:\Program Files\KiCad\10.0\bin`; para otra instalación, `KICAD_DIR`, `KICAD_CLI` y `KICAD_PYTHON`.
- Python 3 (scripts de `herramientas/` y hooks; solo biblioteca estándar).
- [ESPHome](https://esphome.io/) para el firmware.

Al clonar el repositorio, activa la validación de commits:

```bash
git config core.hooksPath .githooks
```
