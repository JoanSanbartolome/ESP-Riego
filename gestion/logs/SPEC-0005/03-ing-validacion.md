---
spec: SPEC-0005
agente: ing-validacion
n: 03
fecha: 2026-11-04
estado: completado
---

# SPEC-0005 · 03 · ing-validacion

## Orden recibida

SPEC-0005 · rama spec/SPEC-0005-estudio-salidas (ya activa; no cambies de rama) · Informe VAL-0005-01.

Lee: gestion/specs/SPEC-0005-estudio-salidas.md (objetivo, alcance, criterios de aceptación y registro); docs/diseno/estudio-salidas.md completo (§0–§10 y la adenda §11); docs/02-especificaciones-v2.md v0.2 (ALI-*, REL-*, FAB-07, FAB-08); gestion/decisiones/DEC-0002-objetivo-v2-revisado.md; gestion/informes/VAL-0004-02.md (observación 03, sobre válvulas DC); gestion/checklists/proceso.md si aplica. Lee los logs del autor (gestion/logs/SPEC-0005/01 y 02-ing-esquematicos.md) solo después de revisar el entregable.

Contexto que no está en los archivos: las válvulas instaladas son de 24 V DC, ≈ 0,2 A; la alimentación es solo una fuente de 24 V DC de hasta 5 A (rango 18–30 V, TVS SMBJ33A con Vc 53,3 V). Después de entregar el estudio, el usuario decidió D8 (anotado en el registro de la spec, commit 49bea58): BTT6050-1ERA con protección completa, segunda fuente BTT6030-2ERA y reserva BSP752R. Que D8 esté decidida no incumple el último criterio: lo que se comprueba es que el estudio la presentaba como propuesta. La DEC-0003 y los cambios de requisitos de §11.5 son de SPEC-0007, no de esta spec: no los exijas aquí, pero sí señala como observación cualquier error en §11.5 que deba arrastrar SPEC-0007.

Haz: verifica criterio a criterio los 6 criterios de aceptación de la spec. Comprueba en especial:
- que las cifras de coste por placa (5/10 placas) cuadran con los precios unitarios citados;
- los datos clave del BTT6050-1ERA, BTT6030-2ERA y BSP752R contra su datasheet: VS máx./máx. absoluto frente a 53,3 V, umbral VIH frente a 3,3 V del ESP32, corriente nominal y límite, rango de kILIS;
- el razonamiento del corto (la fuente de 5 A limita antes que el chip; el apagado por firmware según IS; ≈ 470 µF antes del buck y ≈ 60 ms de autonomía);
- los descartes de §11 (VN5050J, VN5012AK a 41 V; VN7140AS, VN7050AS, TPS1HC100; BTS4140N; NCV8460A; BTS428L2; TPS281C30);
- y los códigos LCSC citados, con fecha de consulta.
No uses el MCP de KiCad: no hace falta para esta revisión.

Entrega: gestion/informes/VAL-0005-01.md con veredicto (APROBADO, APROBADO_CON_OBSERVACIONES o RECHAZADO), hallazgos con ID VAL-0005-01-NN y severidad, y la versión de checklist aplicada, más el log gestion/logs/SPEC-0005/03-ing-validacion.md. Responde con ESTADO, ARCHIVOS, VERIFICACIÓN, PENDIENTE y LOG.

## Contexto consultado

- Proyecto:
  - `gestion/specs/SPEC-0005-estudio-salidas.md`;
  - `docs/diseno/estudio-salidas.md` (967 líneas);
  - `docs/02-especificaciones-v2.md` v0.2;
  - DEC-0002 y VAL-0004-02;
  - las checklists de proceso v2, requisitos v1 y esquema v2;
  - la plantilla del informe.
- Datasheets descargados de LCSC a `scratchpad/val0501/ds_*` y leídos con `pdftotext`, o renderizados a imagen con PyMuPDF cuando la fuente está codificada:
  - BTT6050-1ERA rev. 1.00: tablas 1, 3, 4, 7 y 10; §5.3.2 (ec. 5.1 y fig. 12, p. 13); §6.4; §6.5; §7.3.3.2;
  - BTT6030-2ERA rev. 1.00: tabla 1 y tablas de potencia, protección, IS y entradas;
  - BSP752R V1.3, pp. 3–6;
  - BTS428L2 V1.1, pp. 1–3 y 6;
  - BTS4140N V1.1, pp. 1, 3 y 4;
  - VN5050J, VN5012AK, VN7140AS, VN7050AS, TPS1HC100-Q1, NCV8460A y TPS281C30 (tablas de máximos, de funcionamiento y de entradas).
- LCSC: 38 códigos consultados el 2026-11-04 a través de `wmsc.lcsc.com/ftps/wm/product/detail`.
- JLCPCB `partdetail`: C534868, C534865, C112644 y C95872.
- Logs 01 y 02 de ing-esquematicos, leídos al final para contrastar.

## Acciones

1. Rama `spec/SPEC-0005-estudio-salidas`; commit revisado `49bea58`. No he cargado nada en el MCP ni he usado `kicad-cli`.
2. He comprobado con `git diff` que `ad8e5bc` solo añade §11 (`@@ -816,0 +817,150 @@`) y que el diff de la rama no sale de las zonas de cada autor.
3. `python herramientas/verificar.py hardware/v2` → «No existe» (código 2): no aplica.
4. Script `scratchpad/val0501_scripts/lcsc.py`: 38 códigos LCSC, con MPN, fabricante, stock y tramos de precio.
5. Script `scratchpad/val0501_scripts/calc.py`:
   - reconstrucción de los costes de §5 y §11.3;
   - energía inductiva con la ec. 5.1 del BTT6050;
   - autonomía de la lógica con el UVLO y con 18 V;
   - error de IS según k_ILIS.
6. Tablas de cotas de datasheet para el BTT6050, el BTT6030, el BSP752R y los 9 descartes.
7. He escrito `gestion/informes/VAL-0005-01.md` y este log.

## Decisiones y justificación

- **Checklists:** aplico la de esquema v2 (solo «Cálculos») y la de requisitos v1 («Coherencia técnica», para §7.3 y §11.5). La de proceso no aplica.
- **Criterio 3:** entiendo por «pieza candidata» las de las tablas «Piezas candidatas» de §2 y las tres retenidas en §11.4. Los chips descartados en §11.3 son alternativas evaluadas, y sus huecos de tipo y datasheet son el hallazgo B 09.
- **Severidad del hallazgo 01 (M, no A):**
  - es un estudio de propuesta;
  - lo correcto (que la fuente limita antes que el chip) está bien;
  - el propio estudio pide validar el corto en el prototipo;
  - la redacción de requisitos es de SPEC-0007.
  Pero los 60 ms son un error numérico frente a ALI-01 y ALI-06, y «sin fusible por canal» no está demostrado. Por eso pido que SPEC-0007 no lo adopte tal cual.
- **Veredicto: APROBADO_CON_OBSERVACIONES.** 0 C, 0 A, 1 M y 9 B; los 6 criterios se cumplen.

## Verificación

- **Costes:** 24 filas reconstruidas, todas dentro de ±0,10 $ de las del estudio. La excepción es el BTT6030-2ERA con 5 placas: el tramo de 15 unidades da 9,28 $ y no 8,38 $.
- **LCSC:** los 38 códigos corresponden a su MPN y los precios coinciden. El stock ha cambiado en BTT6050 (1 698), IRLML0100 (4 655) y FDN5618P (9 750).
- **BTT6050:**
  - V_S 48 V; V_S(LD) 65 V; V_S(AZ) ≥ 65 V;
  - V_IN(H) ≥ 2 V;
  - I_L(NOM) 4,5 A; I_L5(SC) ≥ 38 A;
  - k_ILIS 1500 ± 25 % a 0,5 A;
  - E_AS 60 mJ a 4,5 A y ≈ 155 mJ a 1 A (fig. 12).
- **Autonomía:** 60 ms solo a 24 V → 8 V con 2 W. Con 18 V hasta el UVLO quedan 5–15 ms.

## Pendiente

- **Coordinador:**
  - convertir las observaciones en specs propuestas;
  - pasar a SPEC-0007 los hallazgos 01, 04, 06 y 07, que afectan a la redacción de REL-03, REL-05, REL-08 y ALI-04;
  - pasar el 05 a la spec del bloque de salidas.
- **Autor (si se corrige el estudio):** hallazgos 02, 03, 08, 09 y 10.
- **jr-conformidad:** tipo y stock de montaje JLCPCB del BTT6050, del BTT6030 y del M7.
- **Prototipo:** corto franco y con cable largo con la fuente de 5 A; medir L de la válvula.

## Notas para el siguiente agente

- Los PDF de LCSC de las PROFET clásicas (BSP752R, BTS428L2, BTS4140N) tienen la fuente codificada. Se leen bien si se renderizan a PNG con PyMuPDF (`page.get_pixmap(dpi=90)`) y se abre la imagen.
- El conteo de páginas que da la orden `file` en esos PDF es erróneo (dice 2–3 páginas); `pypdf` da el real (19–55).
