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
3. [Plan de diseño](docs/03-plan-de-diseno.md): fases, hitos y flujo de trabajo.

## Estructura

```
.
├── docs/            Análisis, especificaciones y plan
├── hardware/
│   ├── libraries/   Símbolos, huellas y modelos 3D propios (rutas ${KIPRJMOD})
│   ├── v1-tfg/      Proyecto del TFG migrado a KiCad 10
│   └── v2/          Nuevo diseño
├── firmware/        Configuración ESPHome
└── fabricacion/     Salidas de fabricación por versión
```

Las carpetas se crean a medida que avanzan las fases.

## Requisitos

- [KiCad 10](https://www.kicad.org/)
- [ESPHome](https://esphome.io/) para el firmware
