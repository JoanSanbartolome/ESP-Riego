---
spec: SPEC-0021
agente: jr-conformidad
n: 03
fecha: 2026-11-07
estado: completado
---

# SPEC-0021 · 03 · jr-conformidad · Corrección VAL-0021-01

## Orden recibida

Corregir VAL-0021-01-01 y -02 (M) y las B baratas -04, -05, -06 y -08. Sin KiCad.

## Acciones

| ID | Acción | Archivo |
|---|---|---|
| -01 | Polaridad reescrita: cátodo en el lado de la barra ancha de la «T» (abajo en la vista inferior, p. 2, como el símbolo del diodo); pad 1 (K) de `LED_0603_1608Metric` | `hardware/componentes/KT-0603YG.md` §Pinout |
| -02 | Columna `Datasheet` de la tabla de campos del log 01 corregida en sitio: 0 marcadores «(PDF de LCSC…)», 0 rutas relativas a la raíz. Fabricante donde hay URL (U5 Espressif, U6 ST); `dataManualUrl` de LCSC (API de JLCPCB, 2026-11-07) en el resto. C23 lleva las dos URL (C106248 y la propuesta C15849) | `01-jr-conformidad.md` §Tabla de campos |
| -02 | Campo `datasheet:` de `ESP32-S3-WROOM-1.md` y `USBLC6-2SC6.md`: ya era la URL del fabricante; sin cambios | — |
| -04 | Anotado que se omite el escalón de la tapa de 0,9 a 1,2 mm y que el cuerpo empieza en z = 0,15; altura 1,5 correcta | `TS-1187A-B-A-B.md` §Nota sobre el modelo 3D |
| -05 | Taladro de 1,0 mm anotado como excepción justificada (estándar de tiras de 2,54 mm con pin de 0,64; el de la huella oficial); opcional copia a 1,05 | `B-2100S04P-A110.md` §Recomendaciones |
| -06 | `dataManualUrl` de LCSC como espejo en el campo `datasheet:` de las tres fichas | `KT-0603YG.md`, `TS-1187A-B-A-B.md`, `B-2100S04P-A110.md` |
| -08 | `stock_consultado: 2026-11-07`; stock 321 343 (API 2026-11-07) | `TYPE-C-31-M-12.md` |

### Tabla de campos: columna Datasheet vigente (para SPEC-0022)

Todas las URL salen del `dataManualUrl` de la API (`selectSmtComponentList`, 2026-11-07), salvo U5 y U6 (fabricante).

| Ref. | Datasheet |
|---|---|
| U5 | https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf |
| U6 | https://www.st.com/resource/en/datasheet/usblc6-2.pdf |
| los demás | véase la tabla del log 01 (corregida) |

## Verificación

- `verificar.py`: no aplica (sin proyecto KiCad tocado).
- Búsqueda en el log 01: 0 marcadores restantes en la tabla de campos.

## Repaso de checklist (`librerias.md`, ficha)

- Ficha con datasheet enlazado, LCSC como espejo: cumple (las tres fichas con URL).
- Polaridad sin ambigüedad (propuesta de VAL): aplicada en el LED.
- Excepción de taladro THT: justificada en la ficha.
- Fecha y stock actualizados en TYPE-C-31-M-12: cumple. Los precios de esa ficha siguen siendo de 2026-11-05/06 (no se reconsultaron).
- Piezas nuevas o modificadas: ninguna en esta corrección.

## Pendiente

- Coordinador: -03 (vías/pasta del EPAD, para layout y fabricación), -07 (citar página del pinout en próximas specs) y las propuestas DEC-0007 (C23, U6, D5) siguen abiertas.
- El 3D del TS-1187A conserva la simplificación (bajar la tapa a z = 0 en el generador queda opcional).
- URL de LCSC del KT-0603YG apunta al PDF rotulado XL-0603QYGC (ya anotado en la ficha).
