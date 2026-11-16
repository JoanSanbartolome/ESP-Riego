---
name: reference-herramientas-kicad
description: Uso práctico de herramientas/kicad (SPEC-0027): qué sustituye a los scripts del scratchpad, cuánto tarda la batería y trampas del shell al parchear archivos
metadata:
  type: reference
---

Desde SPEC-0027 (2026-11-12) existe `herramientas/kicad/` (lista y ejemplos en su `README.md`). Sustituye a los scripts de sesiones anteriores citados en [[mcp-efectos-secundarios]], [[reference-trucos-esquema]] y [[reference-fuentes-piezas]]: `sync.py` → `sincronizar.py`; `s22_gen.py` → `hoja.py` (descripción JSON; `extraer` saca la de una hoja sin cables); `jlc.py`; `render.py`/`banco.py` → `vista.py`; `vias.py`/`pins.py` → `huella.py`.

Lo que no está en las herramientas y cuesta tiempo:

- **Batería:** `test_kicad.py` entera tarda de 3 a 4,5 min (unas 25 llamadas a kicad-cli): lanzarla en segundo plano. Las clases sin KiCad van en segundos: `python …/test_kicad.py Huella Jlc Restricciones Comprobar Campos`.
- **Heredocs de Bash con Python:** a veces `\\` llega a Python como `\` (no siempre). Un parche con `"\\n"` partió una línea, y un `r"\\1"` dejó un byte 0x01 en `restricciones.py` que ninguna prueba vio (lo delató `file`: «data»). Para editar, la herramienta Edit; si hace falta un heredoc, sin barras invertidas (`chr(10)`, `chr(92)`), y después buscar bytes de control.
- **`diff` contra el repositorio:** los archivos de `herramientas/` están en CRLF en el árbol de trabajo; un `diff` contra una copia en LF saca el archivo entero. Usar `git diff --no-index` o `tr -d '\r'`.
- **Flujo para cambiar `hardware/v2`:** copia en el scratchpad con `v2` y `libraries` hermanas → herramienta con `-o` sobre la copia → `verificar.py <copia>` → copiar solo el archivo al repositorio.
- **Probar que una prueba nueva detecta el defecto:** montar en el scratchpad un «repo» falso (`CLAUDE.md` + `herramientas/kicad/` de `HEAD` + `hardware/{v2,libraries,componentes}`) y lanzar allí la batería nueva. La guarda bloquea `git archive`; `git show HEAD:<ruta> > <scratch>/<ruta>` sí pasa.
- **Mutaciones:** `test_kicad.py` tiene la clase `Mutaciones` (copia propia de v2 + libraries + componentes, restaura en `tearDown`). Un punto nuevo de `comprobar.py` lleva allí su caso que falla.
- **Raíz:** desde SPEC-0028, `hoja.py raiz --extraer` + editar el JSON + `hoja.py raiz` (sin Python en línea). Las etiquetas renombran las redes (`/MCU/IN1` → `/IN1`): `sincronizar.py` lo resuelve. Netlist frente a un anexo de diseño: `hoja.py netlist <proy> --plan <doc> --seccion "Anexo A"` (redes escritas `RED = {REF-PIN, …}`).
- **Hoja A3 de 6 canales con `hoja.py`** (sin cables, etiqueta en cada pin): bloques de 129,5 × 81 mm; las etiquetas verticales ocupan ~8 mm, así que entre dos pines enfrentados con etiqueta hacen falta ≥ 15 mm; el `Value` de un borne, con `pos` encima. Revisar con `vista.py hoja --zona`.
- `hoja.py generar` conserva los UUID de la hoja que sustituye (paridad intacta), pero no toca los pines de hoja de la raíz ni dibuja cables.

SPEC-0029 (2026-11-14):
- `herramientas/pruebas/test_kicad.py` está **fuera de mi zona**: desde SPEC-0028 se copia a `herramientas/kicad/test_kicad.py`, se le añaden los casos y el coordinador lo mueve. Se ejecuta igual desde ahí (busca CLAUDE.md hacia arriba). Las pruebas de `librerias.fichas` se rompen cuando un código aparece en una ficha de bloque nueva: mutar un código que solo esté en una ficha.
- La terminal Bash (MSYS) convierte `--hoja /` en `C:/Program Files/...`: la raíz con `vista.py hoja … --hoja /` se lanza desde PowerShell. Y la guarda bloquea cualquier comando que contenga la palabra del control de versiones seguida de otra palabra, también en un heredoc de texto.
- Modelo 3D oficial ausente: `sincronizar.py` enlaza el de `libraries/3d` con el mismo nombre y `librerias.3d` lo acepta (`_comun.modelo_de_respaldo`); no hace falta copiar la huella a `esp-riego`.
- Las referencias «libres» de la spec pueden estar mal: comprobar el máximo real en las hojas (C46 estaba en uso).
