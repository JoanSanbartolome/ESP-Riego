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
- `hoja.py generar` conserva los UUID de la hoja que sustituye (paridad intacta), pero no toca los pines de hoja de la raíz ni dibuja cables.
