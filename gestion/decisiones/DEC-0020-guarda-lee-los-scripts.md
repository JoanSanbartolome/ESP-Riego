---
id: DEC-0020
titulo: La guarda lee los scripts de python y node antes de ejecutarlos
fecha: 2026-11-24
estado: aceptada
modificada_por: []
decide: usuario
specs: [SPEC-0039]
requisitos: []
---

# DEC-0020 · La guarda lee los scripts de python y node antes de ejecutarlos

## Contexto

DEC-0009 (M9) congeló la guarda: el código en línea y los scripts no se analizan, y el 2026-11-18 el usuario mantuvo esa regla tras VAL-0035-01-02. En SPEC-0038, `jr-conformidad` escribió en `docs/diseno/` con un script de la carpeta temporal (`python -I estudio.py`, con `Path(r'C:/…/docs/diseno/estudio-coste.md').write_text(…)`) que la guarda no vio (VAL-0038-01-04). SPEC-0039 pide cerrar ese caso, y el usuario la manda ejecutar el 2026-11-24.

## Opciones consideradas

1. Mantener M9 y fiarlo todo a la detección (`revisar`, `revisar_zonas.py`).
2. Leer el script que se ejecuta y bloquearlo si escribe en una ruta literal fuera de la zona. El código en línea sigue sin analizarse.
3. Analizar también el código en línea (`-c`, heredoc).

## Decisión

El usuario elige la 2 al ejecutar SPEC-0039 (2026-11-24). `guardia.py` lee el script de `python` o `node` (`.py`, `.js`) y lo bloquea si abre en escritura, borra, mueve o copia hacia una ruta hecha de literales (`str`, `Path(…)`, `/`, `os.path.join`) fuera de la zona del agente. Lo que el script calcule no se ve. El resto de M9 sigue igual: el código en línea no se analiza, salvo que toque el TFG.

## Consecuencias

- Prueba Z01–Z04 en `herramientas/pruebas/test_gestion.py`; `test_guardia.py` sigue pasando.
- `gestion/README.md` («Guardas» y «Límites conocidos») recoge el cambio.
- Si hace falta cerrar también el código en línea (opción 3), es otro DEC.
