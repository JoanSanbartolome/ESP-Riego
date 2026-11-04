---
spec: SPEC-0005
agente: ing-esquematicos
n: 02
fecha: 2026-11-04
estado: completado
---

# SPEC-0005 · 02 · ing-esquematicos

## Orden recibida

Adenda de SPEC-0005 (rama `spec/SPEC-0005-estudio-salidas`, rebasada sobre `main`; no cambiar de rama). Datos nuevos del usuario del 2026-11-04:

- las válvulas instaladas son de 24 V DC, de ≈ 0,2 A (vía V2; spec corregida en `e10a97d`; `docs/02` v0.2 con ALI-12 y REL-08 como protección por canal);
- el usuario elige *high-side* para D8, pero el BTT6050/BTT6030 le parece caro, y propone VN5050JJTR-E, BTS428L2ATMA1, TPS281C30ERGWR y VN5012AKTR-E.

Encargo: añadir al final de `docs/diseno/estudio-salidas.md` una sección «## 11. Adenda: válvulas de 24 V DC y elección del *high-side*», sin reescribir el resto, con:

1. una tabla de conclusión (relé, *high-side* discreto e inteligente);
2. la evaluación de los 4 chips, el BTT6050-1ERA y alternativas más baratas de LCSC dimensionadas para la carga real, con criterios comunes: 18–30 V, máximo absoluto o *load dump* frente a V_C de la SMBJ33A (53,3 V), V_IH con 3,3 V, limitación y lógica viva, térmica y *clamp*, diagnóstico y pines, encapsulado, LCSC, tipo, stock, precio y coste de la etapa;
3. la recomendación de uno principal y una segunda fuente;
4. los cambios en REL-03, REL-05, REL-08, FAB-07, FAB-08 y ALI-04.

Fuentes con enlace y sin abrir KiCad. Entrega: estudio y log 02.

## Contexto consultado

- `docs/diseno/estudio-salidas.md` §0–§10 (mi entrega 01) y el log 01.
- LCSC (`wmsc.lcsc.com/ftps/wm/product/detail?productCode=…`), 2026-11-04: C534868, C534865, C112644, C112645, C534779, C75918, C17651020, C2150359, C424245, C443994, C443993, C3230071, C475505 y C59442.
- JLCPCB `partdetail` (tipo): C112644, C534779, C424245 y C75918 (Extended). C534868 y C534865 se consultaron en la entrega 01.
- Datasheets leídos con `pdftotext` / PyMuPDF a la salida estándar:
  - BTT6050-1ERA (tabla 1, §4.1);
  - ISP752R (umbrales, *clamp*, I_L(SCp));
  - BSP752R (resumen);
  - VN5050J (V_CC 41 V, *clamp*, I_limH);
  - NCV8460A (V_D 41 V, pico de 56 V, V_in,high 3,25 V, I_lim);
  - VN7140AS (40 V, 4–28 V).
- El PDF de LCSC del BTS428L2 y el del BSP762T tienen la fuente codificada y no se pudieron extraer. Sus datos (*load dump* de 60 V e I_L(SCr) de 17 A del BTS428L2; V_bb(AZ) 41 V y 5–34 V del BSP762T) vienen de copias del datasheet citadas por el buscador (chipfind).
- Búsqueda de equivalentes chinos: Novosense NSE34/35 son de 12 V; no hay ninguno de 24 V con datasheet fiable en LCSC.

## Acciones

1. Comprobada la rama (`spec/SPEC-0005-estudio-salidas`, HEAD `e10a97d`). No hay `.lck` y no se ha usado ninguna herramienta del MCP que cargue proyectos.
2. Recogidos los datos de 15 chips (los 4 del usuario, el BTT6050/BTT6030 y 9 alternativas).
3. Calculado el coste de la etapa por placa con las hipótesis de §5 (script de Python en línea, sin archivos).
4. Añadida la sección §11 al final de `docs/diseno/estudio-salidas.md` (§11.1–§11.6), sin tocar §0–§10. En la tabla de §11.3, los tipos JLCPCB no comprobados van marcados «sin verificar».

## Decisiones y justificación

Son propuestas: decide el usuario.

- **Principal: BTT6050-1ERA (C534868).** Es el chip válido más barato en LCSC (1,0889 $ a 30 unidades; etapa de 8,33 / 7,86 $ por placa).
  - Mide la corriente por canal (IS en un solo ADC1) y detecta carga abierta en ON y OFF.
  - Aguanta la SMBJ33A gracias a su V_S(LD) de 65 V y tiene entradas de 3,3 V.
  - Stock de 1 748.
- **Segunda fuente: BTT6030-2ERA (C534865)**, misma familia, 2 canales y 10 479 en stock. Reserva de otro fabricante: BSP752R (sin medida de corriente; carga abierta solo en OFF; 277 en stock).
- **Chips del usuario descartados:**
  - BTS428L2: válido pero a 2,42 $, 2,2 veces el BTT6050, y sin medida de corriente;
  - VN5050J y VN5012AK: 41 V de máximo absoluto. Haría falta una TVS SMBJ24A, que conduce dentro del rango de 18–30 V de ALI-01;
  - TPS281C30: 3 en stock y 6,34 $.
- **Alternativas «baratas» descartadas:**
  - VN7140AS, VN7050AS y TPS1HC100: de 12 V (28 V de funcionamiento, 40 V máximo);
  - BTS4140N: entrada activa baja y 0,2 A;
  - NCV8460A: V_IH de 3,25 V;
  - BSP762T: 41 V.
- **REL-08 sin fusible por canal**: lo cubren la limitación y el apagado térmico del BTT. Como la limitación mínima (38 A) supera la de la fuente, la lógica necesita autonomía (≈ 470 µF de 24 V → ≈ 60 ms con 2 W) y el firmware debe apagar el canal por IS. Hay que validarlo con un corto real.
- **FAB-07:** 2 polos por canal (OUT/GND), 6 por borde. **FAB-08:** ≈ 70 mm. **ALI-04:** mantener la SMBJ33A.

## Verificación

- `python herramientas/verificar.py hardware/v2`: no aplica (no existe `hardware/v2` y esta spec no toca KiCad). ERC, DRC y paridad: no aplicables.
- No se ha abierto ningún proyecto con el MCP.
- Costes de §11.3 recalculados con el script: BTT6050-1ERA, 1,243 $/canal a 30 unidades y 8,33 $ por placa con 5 placas.

## Pendiente

- **Usuario (vía coordinador):** aceptar el BTT6050-1ERA (o el BTT6030-2ERA) como D8. Saber que ≈ 8 $ por placa es el mínimo para un *high-side* inteligente de 24 V con stock en LCSC; la opción barata sin diagnóstico es el discreto 4b más fusibles (≈ 3,0–3,6 $).
- **Coordinador (SPEC-0007):** aplicar §11.5 (REL-03, REL-05, REL-08, FAB-07, FAB-08, ALI-04) y la nota de pines para MCU-05.
- **jr-conformidad:** confirmar los LCSC y los tipos marcados «sin verificar». Confirmar en los datasheets:
  - el umbral de entrada del BTS428L2 y del VN5050J;
  - el V_IN(T+) del BSP752R (aquí se ha tomado el del ISP752R).
- **Prototipo:** corto en campo con la fuente de 5 A (ALI-12, autonomía de la lógica) y lectura de IS con válvula, cable abierto y corto.

## Notas para el siguiente agente

- Los PDF de LCSC de las PROFET clásicas (BTS428L2, BSP7xx) tienen la fuente codificada: `pdftotext` devuelve texto desplazado y sin cifras. Hay que buscar otra copia del datasheet.
- Precios y stock del 2026-11-04.
