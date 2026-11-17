---
spec: SPEC-0035
agente: ing-diseno
n: 01
fecha: 2026-11-17
estado: completado
---

# SPEC-0035 · 01 · ing-diseno

Pasos 1 (herramientas) y 2 (hoja piloto Sensores). El paso 3 no se ha empezado: espera la aprobación del estilo.

## Hecho

- `herramientas/kicad/hoja.py`: `generar` dibuja cables (se parten en los extremos y pines que caen encima; uniones automáticas con ≥ 3 extremos), conexión `W` en un pin (falla si no llega cable), `etiquetas` fuera de los pines, `recuadros` (`text_box` de trazo y punto con título) y subhojas, también repetidas (`refs` por instancia; páginas nuevas). `extraer` lo lee todo y ya no se niega ante cables. `netlist --grupos` compara por grupos de pines.
- `_comun.py`: `comparar_grupos`, `por_instancia` (una pieza por referencia de instancia) e instancias en `simbolos_hoja`; `campos.py` y `comprobar.py` cuentan las piezas por instancia.
- `comprobar.py` (25 puntos): `esquema.cruces`, `esquema.sueltas`, `esquema.recuadros`, `esquema.etiquetas` (geometría en `_estilo.py`) y `esquema.pcb_main` (huellas que cambian frente a `main`, citadas en la SPEC o en sus partes).
- `herramientas/kicad/test_kicad.py`: copia de la batería con 7 pruebas nuevas o cambiadas (`Hoja`: cables, subhoja repetida, Alimentación con cables, tramos, `--grupos`, polilínea; `Mutaciones`: estilo y `pcb_main`). README de `herramientas/kicad/` al día.
- `hardware/v2/sensores.kicad_sch`: hoja piloto con las reglas 1–6 de DEC-0015. `hardware/v2/estilo-pendiente.txt` (nuevo) y una línea en `hardware/v2/README.md`.

## Decisiones y desviaciones

- **Transición:** los cuatro puntos de estilo excluyen las hojas que lista `estilo-pendiente.txt` (Alimentación, Conectores, MCU y Salidas, aún sin redibujar), para que `verificar.py` no dé FALLA mientras el piloto espera. El paso 3 borra el archivo. Sin él, `esquema.recuadros` da 197 FALLA y `esquema.cruces` 5, todos reales (p. ej. «U2» sobre el cuerpo de U2 y dos `VIN_SENSE` superpuestas en Alimentación).
- La raíz queda fuera de los puntos de estilo (excluida de la spec; SPEC-0032).
- En el piloto, las redes conservan su nombre: `I2C_SDA` e `I2C_SCL` siguen como etiquetas jerárquicas en el extremo de su cable; el resto va con cables.
- Cifras junto a la pieza: «I²C 0x44» (U13) y «≤2 mm de U13» (C47), de `sensores.md` §0. Dos líneas de nota.

## Verificación

- `verificar.py hardware/v2`: ERC 0, DRC 0 (448 sin conectar: placa sin rutar), paridad 0; puntos [auto] 25: OK 23, FALLA 0, N/A 2. `campos.py revisar`: 0 diferencias.
- Netlist por grupos frente a la de `main` guardada antes de empezar: 0 diferencias (también por nombre). La PCB no cambia (`esquema.pcb_main`: ninguna huella cambia).
- `test_kicad.py` completo (copia en `herramientas/kicad/`): 48 pruebas en verde, 148 s.

## Para validación

- `_estilo.py` mide los textos con una caja aproximada (0,8 × alto por carácter). Probado contra las imágenes: los 5 cruces de Alimentación son reales y el falso positivo de U6 (MCU) se quitó midiendo el cuerpo y los pines por separado.

## Pendiente

- **Usuario:** aprobar el estilo con `C:\Users\josan\AppData\Local\Temp\claude\2c54f79e79dd3002\c980b02f-1588-4782-8921-adea897769ca\scratchpad\entrega\sensores-piloto.png` (y `sensores-piloto-zona.png`), frente a `tfg-conectores.png` en la misma carpeta.
- **Coordinador:** mover `herramientas/kicad/test_kicad.py` a `herramientas/pruebas/`; aplicar en `gestion/checklists/esquema.md` el texto de `…\scratchpad\entrega\esquema-md-estilo.txt` (marcas `[auto: comprobar.py …]`, v14); borrar `C:\c\Users\josan\AppData\Local\Temp\…\scratchpad\ref\` (dos archivos de netlist escritos ahí por error).
