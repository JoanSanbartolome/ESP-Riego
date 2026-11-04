---
id: SPEC-0003
titulo: Auditoría encadenada, falsos positivos y detalles de commit-msg
fase: 0
estado: descartada
responsable: coordinador
revisor: ing-validacion
rama: spec/SPEC-0003-auditoria-detalles
requisitos: []
depende_de: [SPEC-0001]
creada: 2026-11-04
cerrada:
validacion:
---

# SPEC-0003 · Auditoría encadenada, falsos positivos y detalles de commit-msg

> Nace de las observaciones B de [VAL-0001-03](../informes/VAL-0001-03.md). No bloquea el trabajo de diseño.

## Objetivo

Que la auditoría no se pueda alterar sin que se note, aunque las líneas aún no estén versionadas, y que la guarda deje de bloquear operaciones legítimas de empaquetado y copia.

## Alcance

- Incluye:
  - VAL-0001-03-03: falsos positivos (`tar`/`7z` al crear un archivo desde la raíz del repositorio, `export_symbol` desde la librería oficial, `robocopy … /MIR` hacia fuera del TFG, `ForEach-Object FullName`, `tar -c -C TFG | tar -x`).
  - VAL-0001-03-04: cada línea de la auditoría lleva el hash de la anterior, y `revisar_zonas.py` comprueba la cadena.
  - VAL-0001-03-08: `Log:` no acepta carpetas ni `.`; docstring de `commit_msg.py` al día.
- Excluye: lo que está en SPEC-0002.

## Entradas

- `gestion/informes/VAL-0001-03.md` (hallazgos 03, 04 y 08).
- `.claude/hooks/auditoria.py`, `.claude/hooks/guardia.py`, `herramientas/revisar_zonas.py`, `.githooks/commit_msg.py` y las baterías de `herramientas/pruebas/`.

## Entregables

- Auditoría encadenada y su comprobación.
- Guarda y `commit_msg.py` corregidos, con sus casos en las baterías.

## Criterios de aceptación

- [ ] Quitar, cambiar o inventar una línea de la auditoría, versionada o no, se detecta.
- [ ] Los falsos positivos de VAL-0001-03-03 pasan en la batería.
- [ ] `Log:` con una carpeta o `.` se rechaza.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-04 | coordinador | Crea la spec (propuesta) a partir de VAL-0001-03 | |
| 2026-11-04 | usuario | Descartada: no complicar más la orquestación. Los límites siguen documentados en `gestion/README.md` (Guardas) | |
