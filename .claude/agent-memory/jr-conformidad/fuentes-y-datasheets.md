---
name: fuentes-y-datasheets
description: Dónde bajar datasheets y datos de piezas, qué sitios no responden y cómo leer los PDF problemáticos
metadata:
  type: reference
---

- La base local del MCP (`search_jlcpcb_parts`, `get_jlcpcb_part`) está vacía; el tipo y el stock salen de `jlc.py`. Por qué: `get_jlcpcb_database_stats` da 0 piezas. Fuente: MCP, consulta de SPEC-0039 paso 3.
- El stock de LCSC no vale para JLCPCB (C14663: 0 en LCSC, 34 M en JLCPCB). Por qué: LCSC y JLCPCB tienen almacenes distintos. Fuente: SPEC-0021.
- `www.lcsc.com/datasheet/*.pdf` devuelve HTML con `curl`: el PDF real sale de `dataManualFileAccessIdUrl`, firmada y caducada a los 30 min (descargar en el acto y no imprimirla). Por qué: la URL del PDF de LCSC está bloqueada. Fuente: SPEC-0015, SPEC-0031.
- `ti.com/lit/ds/symlink/<pieza>.pdf` y `espressif.com` descargan con urllib y User-Agent «Mozilla/5.0»; `st.com` (timeout), Littelfuse (403), HRO y Kangnex no responden: anotar «revisión no confirmada». Por qué: sin ello se pierde tiempo reintentando. Fuente: SPEC-0015, SPEC-0031.
- La API de EasyEDA (`easyeda.com/api/products/<C>/components`) da 403 y el clasificador bloquea cambiar el User-Agent: crear desde el datasheet. Por qué: no hay otra vía. Fuente: SPEC-0015.
- Infineon: la página `infineon.com/package/<encapsulado>` (slug exacto del buscador; un slug inventado da 404) trae la imagen del land pattern (`assets.infineon.com/is/image/infineon/infineon-<pkg>-png-footprint-en.png`) y los datasheets están en `infineon.com/assets/row/public/documents/10/49/infineon-<mpn>-datasheet-en.pdf`. Por qué: el PDF de LCSC era idéntico. Fuente: SPEC-0024.
- Sensirion: la URL de la ficha daba 404; la vigente sale de `sensirion.com/products/catalog/SHT40`. Por qué: la versión 6.2 ya no era la vigente. Fuente: `hardware/componentes/SHT4x.md`.
- Contrastar con el datasheet lo que afirme una spec o un DEC: DEC-0013 decía que el TCA9554 no tenía pull-up interno y lo tiene (p. 16 de SCPS233E). Por qué: una cita sin comprobar llegó al diseño. Fuente: SPEC-0031.
- Los PDF de LCSC pueden ser de otro modelo (KT-0603YG enlaza el de XL-0603QYGC). Por qué: la ficha cita datos de otra pieza. Fuente: `hardware/componentes/KT-0603YG.md`.
- PDF con texto codificado o con tablas desordenadas (BSP752R, curvas de derating): `pdftoppm -png -r 70` (o 110) y mirar la imagen con Read; `pdftotext -layout` para las tablas limpias. Por qué: el texto sale desplazado. Fuente: SPEC-0024, SPEC-0028.
- Samsung SimSurfing: `curl -A Mozilla/5.0 https://product.samsungsem.com/mlcc/<MPN de 14 caracteres, sin el sufijo de embalaje>.do` (CL21B104KCFNNN, no ...NNNE) da HTML con JSON embebido (`"graphType" : "DCBias"` y `"TCC"`) que se parsea balanceando llaves; 21 603 bytes es «no existe». Por qué: es la única curva de derating pública. Fuente: `hardware/componentes/bloque-alimentacion.md` §3.
- Para MLCC de otro fabricante (PSA) se usa de proxy el Samsung de la misma tensión y tamaño: 4,7 µF 100 V 1210 = `CL32B475KCJZ4N`. Por qué: PSA no publica curva. Fuente: `hardware/componentes/bloque-alimentacion.md` §3.
- Sufijo de Uniroyal `…WAF220J…`: «J» es el multiplicador (22 Ω), no la tolerancia (WAF = 1 %). Por qué: se leía como 5 %. Fuente: SPEC-0021.
