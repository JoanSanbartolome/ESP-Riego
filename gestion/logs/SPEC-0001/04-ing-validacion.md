---
spec: SPEC-0001
agente: ing-validacion
n: 04
fecha: 2026-11-03
estado: completado
---

# SPEC-0001 · 04 · ing-validacion

## Orden recibida

SPEC-0001 · rama spec/SPEC-0001-orquestacion · Segunda revisión de validación → informe VAL-0001-02.

- **Lee:** SPEC-0001 (con los criterios y entregables ampliados), DEC-0001, VAL-0001-01 y `gestion/checklists/proceso.md` v1.
- **Haz:**
  1. revalidar los criterios de aceptación;
  2. dar el estado de los hallazgos 01–19, con evidencia;
  3. buscar fallos nuevos en `c14ae4b..HEAD`;
  4. aplicar la checklist de proceso.
  Incluye pruebas en vivo de mi definición: sin `lint_*`, `close_project` sin `save: false` bloqueado y las órdenes fallidas en la auditoría.
- **Entrega:** `gestion/informes/VAL-0001-02.md` y este log.

## Contexto consultado

- **Spec y referencias:** SPEC-0001, DEC-0001, VAL-0001-01, `proceso.md` v1, mi memoria y la plantilla del informe.
- **Lo que cambió en `c14ae4b..HEAD`:**
  - completos: `guardia.py`, `auditoria.py`, `settings.json`, las cuatro definiciones de agente, `commit_msg.py`, `verificar.py`, `integridad_tfg.py`, `revisar_zonas.py`, `test_guardia.py` y `test_commit_msg.py`;
  - por diff: `gestion.py`, `CLAUDE.md`, `gestion/README.md` (Guardas), `docs/03`, la spec y `.gitignore`.
- **Código del servidor MCP** (`C:\Users\josan\proyectos\KiCAD-MCP-Server\src\tools`): 247 herramientas, y los parámetros de `import_symbol`, `add_footprint_3d_model`, `batch_move_components` y `set_footprint_type`. Además, los esquemas de `ToolSearch` de `close_project`, `validate_*`, `get_drc_violations`, `check_kicad_ui`, `get_registry_part` y `find_duplicate_symbols`.
- **Al final, para contrastar:**
  - `gestion/logs/SPEC-0001/03-jr-conformidad.md`;
  - `gestion/logs/coordinador/2026-11-03.md`;
  - las líneas de la auditoría de los demás agentes;
  - el mensaje de `4621a2a`.

## Acciones

1. Rama comprobada. Commit revisado: `4621a2a`.
2. `py_compile` de todos los scripts, `test_guardia.py` (143/143) y `test_commit_msg.py` (20/20).
3. Mi batería de 90 casos de VAL-0001-01: 90/90 (antes, 25 discrepancias).
4. Casos nuevos de la guardia en `scratchpad\val2\` (`nuevos.py`, `red.py`, `fp.py` y `fp2.py`), con `AUDITORIA_DIR` temporal: 100 casos.
   - Elusiones del TFG y de las zonas con órdenes no listadas.
   - Redirecciones tras `git` y tras los envoltorios, que no se analizan.
   - **Falsos positivos del MCP** en las llamadas legítimas de `jr-conformidad` e `ing-esquematicos`.
5. Cruce de las herramientas MCP reales con `disallowedTools`, con la lista de `ing-validacion` y con `ESCRITURA_MCP` (`herr_mcp.py` y `permitidas.py`).
6. `verificar.py`:
   - sobre `tfg_copy` y sobre una copia nueva (`tfg3`) con `md5sum`: 1/40/77, con el proyecto restaurado;
   - con el esquema corrupto y una `--salida` vieja: salida 2;
   - detección del TFG, también con el nombre 8.3.
7. Copia del repositorio en `val2\repo`:
   - `gestion.py tablero` y `trazabilidad`, idempotentes;
   - `integridad_tfg.py crear`: solo cambia `creado`;
   - `revisar_zonas.py` con archivos plantados (vía `zonas_copia.py`): detecta lo que está fuera de zona, pero no la manipulación de la auditoría.
8. `commit_msg.py`: 9 casos extra (`msg_extra.py`) sobre el repositorio temporal de la batería versionada.
9. `integridad_tfg.py verificar` en el repositorio: 337 archivos intactos. El git propio del TFG no tiene commits (lo comprobé con `git --no-optional-locks … ls-files` y `log`).
10. Pruebas en vivo:
    - `ToolSearch` sin `lint_*`, `save_project` ni `Agent`;
    - `get_backend_state`: sin proyecto cargado;
    - `close_project` sin argumentos y con `save: true`: bloqueado;
    - `close_project` con `save: false`: pasa;
    - `ls` inexistente: registrado como `ok: false` con `error`;
    - `git commit --dry-run` y Write en `docs/`: bloqueados.
11. Contraste con los logs y el diario, y redacción del informe.

No cargué ningún proyecto en el MCP. El único `close_project` que pasó lo hizo con `save: false` y sin proyecto cargado.

## Decisiones y justificación

- **Hallazgo 01 de severidad A:** el criterio 4 exige expresamente que la guardia "deja pasar las operaciones permitidas". Las llamadas bloqueadas son flujos centrales de las fases 2–5: la librería oficial es la opción 1 de `jr-conformidad`, y la URI `${KIPRJMOD}/../libraries` es el formato que exige KIC-01.
- **Hallazgo 02 de severidad A:**
  - el TFG no tiene ninguna copia (su git no tiene commits ni remoto);
  - órdenes naturales de PowerShell y de bash lo destruyen sin bloqueo;
  - la huella solo detecta el daño, no lo repara.
  Indico en el informe que, con una copia del TFG y la lista blanca, bajaría a M.
- **Hallazgos 03 y 04 de severidad M:** dentro del repositorio, la detección (`revisar_zonas.py`, el diff y git) cubre el daño. El 03 es un fallo de código concreto y fácil de corregir.
- **No repito como hallazgos la ofuscación por variables ni por concatenación:** la recojo en el 07 como límite que hay que documentar, porque exige intención.
- **Criterio 9 como "Cumple"** con la observación 10: la carga y el acceso al MCP de los agentes de diseño quedaron probados a las 18:24, y `jr-conformidad` probó en vivo el mecanismo nuevo (`disallowedTools` y la guarda MCP).

## Verificación

```
ERC         1  (errores 0, avisos 1)        pin_to_pin [warning]
DRC        40  (errores 1, avisos 39, sin conectar 0)
Paridad    77  (61 field_mismatch, 10 net_conflict, 6 footprint_symbol_mismatch)
test_guardia 143/143 · test_commit_msg 20/20 · batería VAL-0001-01 90/90
Casos nuevos: guardia 79 casos con 42 discrepancias; falsos positivos MCP 7/8; commit-msg 4 huecos
TFG intacto (337 archivos)
```

## Pendiente

- **Coordinador:** corregir VAL-0001-02-01, 02 y 03, añadir los casos a `test_guardia.py`, hacer la prueba en vivo de `ing-esquematicos` e `ing-layout` (hallazgo 10) y encargar VAL-0001-03.
- **Usuario** (a través del coordinador): decidir cómo proteger el TFG, con una copia fuera de la carpeta, un commit inicial en su git o el atributo de solo lectura (hallazgo 02).
- **Coordinador:** abrir specs propuestas para los hallazgos 04–09.
- **Coordinador:** las carpetas `%TEMP%\verificar_*` y `%TEMP%\auditoria_prueba_*` que dejan las herramientas y la batería se pueden limpiar.

## Notas para el siguiente agente

- Para probar `revisar_zonas.py` sobre una copia en la carpeta temporal, hay que anular `guardia.TEMPORAL` (ver `scratchpad\val2\zonas_copia.py`). Si no, todo sale "dentro de su zona".
- La guardia no expande las variables de la terminal: en mis órdenes uso rutas literales, porque `$S/…` se bloquea como ruta relativa.
- Los casos nuevos que hay que añadir a la batería están en `scratchpad\val2\nuevos.py`, `red.py` y `fp.py`.
