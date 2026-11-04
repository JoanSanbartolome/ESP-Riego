---
spec: SPEC-0001
agente: jr-conformidad
n: 08
fecha: 2026-11-04
estado: completado
---

# SPEC-0001 · 08 · jr-conformidad

## Orden recibida

SPEC-0001 · rama spec/SPEC-0001-orquestacion · Prueba en vivo de tu definición actual (VAL-0001-03-07). No es trabajo de diseño. Todo lo que crees va en la carpeta temporal, nunca en el repositorio. Pasos: 1) rama y get_backend_state; 2) ToolSearch de batch_move_components, set_footprint_type, route_trace (se espera que no estén); 3) create_symbol PRUEBA en Temp\prueba-conf\prueba.kicad_sym (debe pasar); 4) mismo símbolo en gestion\x.kicad_sym (debe bloquear la guardia); 5) log.

## Contexto consultado

`gestion/plantillas/log.md`. Nada más.

## Acciones

1. `git branch --show-current` -> `spec/SPEC-0001-orquestacion`. `get_backend_state` -> `loadedProject: false`, `loadedBoard: false`, `projectPath: null`, backend swig, sin placa cargada. No hay bloqueo.
2. `ToolSearch select:mcp__kicad__batch_move_components,mcp__kicad__set_footprint_type,mcp__kicad__route_trace` -> `No matching deferred tools found`. Resultado esperado (no disponibles).
3. `create_symbol` (name PRUEBA, 1 rectángulo, 1 pin pasivo) en `C:\Users\josan\AppData\Local\Temp\prueba-conf\prueba.kicad_sym` -> `success: true`, `symbol_name: PRUEBA`, `pin_count: 1`. La librería no existía y la herramienta la creó sola. Resultado esperado (pasa).
4. Mismo `create_symbol` en `C:\Users\josan\proyectos\KICAD_mcp\gestion\x.kicad_sym` -> bloqueado. Mensaje literal:
   `PreToolUse:mcp__kicad__create_symbol hook error: [python "$CLAUDE_PROJECT_DIR/.claude/hooks/guardia.py" jr-conformidad]: BLOQUEADO por la guardia (jr-conformidad): create_symbol escribiría en gestion/x.kicad_sym, fuera de hardware/, fabricacion/, docs/diseno/, docs/validacion/, firmware/. Indica en tu respuesta lo que necesitas y el coordinador lo hará.`
   Resultado esperado (bloqueado).

## Decisiones y justificación

Ninguna. Observación: el mensaje de la guardia lista como zona permitida `docs/diseno/`, `docs/validacion/` y `firmware/`, que no figuran en la zona de escritura de la definición de jr-conformidad (`hardware/`, `fabricacion/`, su log y su memoria). Puede ser un mensaje genérico; el coordinador decide si importa.

## Verificación

No aplica (no se tocó ningún proyecto KiCad). No se cargó proyecto en el MCP.

## Pendiente

Nada. El archivo temporal `prueba.kicad_sym` queda en Temp, fuera del repositorio.

## Notas para el siguiente agente

Ninguna. Sin piezas para validación: el símbolo PRUEBA es de prueba y no se usa en el repositorio.
