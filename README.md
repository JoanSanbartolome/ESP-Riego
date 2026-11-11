# ESP-Riego

Controlador inalámbrico de riego por goteo basado en ESP32 e integrado en Home Assistant mediante ESPHome.

Este repositorio contiene el rediseño (v2) de la PCB desarrollada en el Trabajo Fin de Grado de Joan San Bartolomé Ferri. El proyecto original del TFG no se modifica: se importa como referencia y la v2 se diseña desde cero a partir de su análisis.

## Estado

| Fase | Estado |
|---|---|
| 0. Análisis, especificaciones y plan | ✅ |
| 1. Importación de la v1 a KiCad 10 | ⏳ |
| 2. Arquitectura y componentes | — |
| 3. Esquema v2 | — |
| 4. Layout v2 | — |
| 5. Fabricación | — |
| 6. Firmware y validación | — |

## Documentación

1. [Análisis de la PCB v1](docs/01-analisis-v1.md): estado de la placa del TFG y hallazgos.
2. [Especificaciones de la PCB v2](docs/02-especificaciones-v2.md): requisitos, criterios de aceptación y decisiones abiertas.
3. [Plan de diseño](docs/03-plan-de-diseno.md): fases e hitos.
4. [Sistema de gestión](gestion/README.md): roles, ciclo de vida de las specs, commits y auditoría. Estado actual en el [tablero](gestion/TABLERO.md) y en la [trazabilidad de requisitos](gestion/TRAZABILIDAD.md).

## Organización del trabajo

El diseño lo hacen agentes de Claude Code coordinados por la sesión principal ([DEC-0001](gestion/decisiones/DEC-0001-orquestacion-de-agentes.md) y [DEC-0009](gestion/decisiones/DEC-0009-orquestacion-v2.md)):

| Agente | Responsable de |
|---|---|
| Coordinador | Specs, órdenes, git, tablero y comunicación |
| `ing-diseno` | Cada bloque de principio a fin: cálculos, piezas, esquema y PCB |
| `jr-conformidad` | Tipo y stock, fichas, campos, BOM, CPL y paquetes de fabricación |
| `ing-validacion` | Revisión contra especificaciones e informes con veredicto |

Cada unidad de trabajo es una spec (un bloque o un hito de layout) con su propia rama, validada antes de integrarse en `main`. Lo que toca ahora está en [`gestion/ESTADO.md`](gestion/ESTADO.md).

## Estructura

```
.
├── docs/            Análisis, especificaciones, plan, cálculos y planes de prueba
├── hardware/
│   ├── libraries/   Símbolos, huellas y modelos 3D propios (rutas ${KIPRJMOD})
│   ├── componentes/ Fichas de componentes
│   ├── v1-tfg/      Proyecto del TFG migrado a KiCad 10
│   └── v2/          Nuevo diseño
├── firmware/        Configuración ESPHome
├── fabricacion/     Salidas de fabricación por versión
├── gestion/         Specs, logs, informes, decisiones, checklists y plantillas
├── herramientas/    Scripts de gestión y verificación
├── .claude/         Agentes, hooks y memoria de los agentes
└── .githooks/       Validación de los mensajes de commit
```

Las carpetas de diseño se crean a medida que avanzan las fases.

## Requisitos

- [KiCad 10](https://www.kicad.org/)
- Python 3 (scripts de `herramientas/` y hooks)
- [ESPHome](https://esphome.io/) para el firmware

Al clonar el repositorio, activa la validación de commits:

```bash
git config core.hooksPath .githooks
```
