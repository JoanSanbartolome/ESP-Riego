---
name: entorno-y-herramientas
description: Trampas de Windows, de la shell, del clasificador del modo automático y de verificar.py al trabajar en el repositorio
metadata:
  type: reference
---

- Python de Windows no entiende `/c/...`: usar `C:/Users/...` y `PYTHONUTF8=1` para imprimir Ω y µ. Por qué: sin ello falla la ruta o sale la salida rota. Fuente: SPEC-0028 paso 1.
- Un heredoc de Bash con varias fichas largas dio «unexpected EOF» y las barras invertidas llegan sin duplicar: escribir cada archivo con Write. Por qué: la ficha salía cortada. Fuente: SPEC-0031.
- Los cambios en `hardware/` y `fabricacion/` se hacen con Edit o Write, no con un script de Python que escribe: el clasificador del modo automático lo deniega aunque la ruta sea de la zona. Por qué: pasó con un script de 48 sustituciones. Fuente: SPEC-0039 paso 3.
- `verificar.py` solo tiene `--salida` y `--json`: no admite `--detalle`. Por qué: un `--detalle` da error de uso. Fuente: `herramientas/verificar.py` l. 110-111.
- Cambiar solo un campo (`Value`) y sincronizar la PCB hace fallar `esquema.pcb_main`: declarar en el parte «Huellas que cambian frente a `main`: …» y repetir `comprobar.py --punto esquema.pcb_main`. Por qué: la comprobación lee esa línea del parte. Fuente: SPEC-0028 paso 1; `herramientas/kicad/comprobar.py` l. 605.
- `kicad-cli sch export bom` y `pcb export pos` admiten `--exclude-dnp`; se usan sobre una copia. Por qué: sin la opción entran las piezas DNP en la BOM y el CPL. Fuente: SPEC-0024, SPEC-0038.
- Una tabla de campos se genera agrupando por (Value, Footprint, LCSC, MPN, Fabricante, Datasheet, Description, DNP); Fabricante y Datasheet de cada código salen de las tablas existentes y, si no, de `dataManualUrl` de la API. Por qué: una pieza en varias referencias da una sola fila. Fuente: SPEC-0028 paso 1.
- Una `Description` de `campos-*.csv` con coma va entre comillas. Por qué: sin ellas `campos.py revisar` la corta y da diferencias falsas. Fuente: SPEC-0024.
