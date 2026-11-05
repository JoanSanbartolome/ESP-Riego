---
spec: SPEC-0010
agente: jr-conformidad
n: 01
fecha: 2026-11-05
estado: completado
---

# SPEC-0010 · 01 · jr-conformidad

## Orden recibida

SPEC-0010 · rama spec/SPEC-0010-correcciones-importacion-v1 · opción (a): regenerar símbolo y huella de `Wemos s2 mini` desde el JSON con `kicad-cli sym|fp upgrade -o`, añadir la huella del jack a `DC-Jack.pretty`, corregir README y log de SPEC-0009 (hallazgos 01–04 de VAL-0009-01).

## Acciones

Rama comprobada leyendo `.git/HEAD`. Los JSON se copiaron desde el TFG al scratchpad (`scratchpad/w/in` y `scratchpad/w/jin`) con `cp`; `kicad-cli` solo trabajó sobre las copias y desde fuera de la carpeta del TFG. `kicad-cli fp upgrade -o` exige un directorio de salida que no exista.

Órdenes (`K` = `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe`, ejecutadas en `scratchpad/w`):

```
K fp  upgrade -o fout in/PCBLIB_WEMOS-S2-MINI_2025-06-16.json
K sym upgrade -o out/wemos.kicad_sym "in/SCHLIB_WEMOS-S2-MINI-(ESP32-S2FN4R2)_2025-06-16.json"
K fp  upgrade -o jout jin/PCB_DC-IN-TH_XDJK-0051-025.pcbdoc_2025-06-18.json
```

Ninguna dio error (el primer intento de `fp` falló solo porque el directorio de salida ya existía). Resultado:

- **01** `hardware/libraries/Wemos s2 mini.kicad_sym`: símbolo `WEMOS-S2-MINI (ESP32-S2FN4R2)` (mismo nombre que el `lib_id` del esquema). `Wemos s2 mini.pretty/WEMOS-S2-MINI.kicad_mod`: 32 pads, mismo nombre que el `lib_id` de U1. Copiados tal cual. La huella convertida no lleva modelo 3D.
- **02** `DC-Jack.pretty/DC-IN-TH_XDJK-0051-025.kicad_mod`: 3 pads, tal cual; eliminado el `.gitkeep`. El pad 3 (`custom`, 0,000001 mm, taladro 3×1) es un artefacto de la conversión; hay que revisarlo si alguna vez se usa. La huella no se usa en la PCB.
- **03 y 04** `hardware/v1-tfg/README.md` corregido (tabla de librerías, cambios de ruta, modelos `.wrl`, verificación). Sección «Corrección (SPEC-0010)» añadida a `gestion/logs/SPEC-0009/01-jr-conformidad.md`.

No se tocó ningún otro archivo de `hardware/v1-tfg/` ni `docs/01`.

## Verificación

`python herramientas/verificar.py hardware/v1-tfg`: ERC 1 (`pin_to_pin`), DRC 40 (1 `starved_thermal` + 39 `lib_footprint_mismatch`, 0 sin conectar), paridad 77 (61 + 10 + 6). `verificar.py` borró el `.kicad_prl`. `python herramientas/integridad_tfg.py verificar`: «TFG intacto: 337 archivos coinciden con la huella».

## Requiere verificación de validación

| Pieza | Qué es | Datasheet y página |
|---|---|---|
| Símbolo y huella `Wemos s2 mini` | Conversión directa del JSON de EasyEDA | https://www.wemos.cc/en/latest/s2/s2_mini.html (pines y dibujo mecánico; páginas sin revisar) |
| Huella `DC-Jack:DC-IN-TH_XDJK-0051-025` | Conversión directa del JSON, sin retocar; pad 3 con artefacto | sin datasheet enlazado en el origen |

## Pendiente

- Coordinador: `docs/01-analisis-v1.md` (36 vías, no 38; DRC 40) y etiqueta `v1.1-tfg` con el OK del usuario.
- Para la v2: courtyard, tipos de pin del Wemos, `.wrl` a `.step`, pad 3 del jack.
