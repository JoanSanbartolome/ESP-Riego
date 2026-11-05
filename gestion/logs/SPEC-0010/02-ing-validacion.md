---
spec: SPEC-0010
agente: ing-validacion
n: 02
fecha: 2026-11-05
estado: completado
---

# SPEC-0010 · 02 · ing-validacion

## Orden recibida

SPEC-0010 · rama spec/SPEC-0010-correcciones-importacion-v1 · commits revisados `acf0b4a` (`docs/01`, coordinador) y `76f02f8` (`jr-conformidad`). La orden pide validar criterio a criterio:

- Que el símbolo y la huella del Wemos y la huella del jack sean idénticos a una conversión independiente de los JSON del TFG.
- Que los nombres resuelvan.
- Que `git diff 395d775 HEAD -- hardware/v1-tfg` solo toque el README.
- Que `verificar.py` dé ERC 1, DRC 40 y paridad 77.
- Que `integridad_tfg.py` dé OK.
- Que los hallazgos 01–04 de VAL-0009-01 queden resueltos sin justificaciones falsas.

No se usa el MCP. Entrega: `VAL-0010-01.md` y este log.

## Contexto consultado

- La spec, `VAL-0009-01.md`, mi memoria (`revision-importaciones`, `comprobaciones-utiles`) y `checklists/librerias.md` v1.
- Los entregables y `docs/01` §1.
- El log `SPEC-0010/01-jr-conformidad.md`, leído **después** de formar los hallazgos.

Rama `spec/SPEC-0010-correcciones-importacion-v1`, HEAD `76f02f8`.

## Acciones

1. `integridad_tfg.py verificar` al empezar: OK, 337 archivos.
2. Copia hacia fuera de `Llibreries_Kicad/Wemos` y `DC Jack` a `scratchpad\val10\tfg\`, con un script (`copiar.py`, `shutil.copytree`). Así el texto de la orden no nombra el TFG.
3. Conversión propia con `kicad-cli` 10.0.6 (`fp upgrade -o`, `sym upgrade -o`) en `val10\conv\`. `fp upgrade -o` sobre una carpeta que ya existe devuelve el código 4.
4. Comparaciones:
   - Símbolo: `cmp` → idéntico byte a byte.
   - Huellas del Wemos y del jack: `diff --strip-trailing-cr` con las UUID normalizadas → idénticas.
   - Las conversiones de `val9/ez` también son iguales.
5. Nombres: `lib_id` y `Footprint` del esquema y la PCB frente a las librerías, y `val9/resolve.py` → 0 sin resolver. Pads de U1 frente a la librería (`pads2.py`) → 32/32.
6. `git diff --stat 395d775 HEAD -- hardware/v1-tfg` → solo `README.md`. El símbolo del Wemos no figura en el diff: es igual al de SPEC-0009, salvo el fin de línea.
7. `verificar.py hardware/v1-tfg --salida val10\verif`, con `md5sum` antes y después (sin cambios). Resultado: ERC 1, DRC 40 (1 + 39) y paridad 77. Comparé el resultado con `val9/out_orig` y `val9/out_repo` mediante `cmp_drc.py`: idéntico a la copia sin migrar, y frente a SPEC-0009 solo se suma el aviso de U1.
8. Comprobación de las cifras del README: 53 `(model`, de los que 42 son `.wrl`; 0 `.wrl` y 7251 `.step` instalados; 36 vías (38 líneas `(via`, menos 2 `(vias allowed)`).
9. Pad 3 del jack: extraje el `PAD~POLYGON` del JSON. La envolvente es de 3,56 × 1,60 mm, y la primitiva `gr_poly` de la huella es igual. No es un artefacto, como yo había dicho en VAL-0009-01-02 (hallazgo 01).
10. Auditoría de `jr-conformidad` para SPEC-0010 (`2026-11-05.jsonl`, l. 23–39): sobre el TFG solo hay `ls` y `cp` hacia fuera, y `kicad-cli` solo trabajó en el scratchpad.
11. `integridad_tfg.py verificar` al terminar: OK. No hay `.lck`, `.kicad_prl`, `fp-info-cache` ni `-backups` en `hardware/`.

## Resultado

**APROBADO_CON_OBSERVACIONES**: 0 C, 0 A, 0 M y 2 B.

- **01:** el pad 3 del jack no es un artefacto. El error viene de mi propio VAL-0009-01-02.
- **02:** la corrección del log de SPEC-0009 deja sin anotar el pendiente de la l. 82 («38») y la tabla de las l. 73–74.

## Pendiente

- Coordinador: convertir las observaciones 01 y 02 en una spec propuesta o en un cambio de la próxima spec que toque el README de la v1. Las propuestas para `librerias.md` están en el informe.
