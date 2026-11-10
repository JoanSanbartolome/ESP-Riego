---
spec: SPEC-0024
agente: jr-conformidad
n: 03
fecha: 2026-11-10
estado: completado
---

# SPEC-0024 · 03 · jr-conformidad (correcciones de VAL-0024-01, hallazgos 01 a 06)

## Orden recibida

Corregir las observaciones 01 a 06 de `gestion/informes/VAL-0024-01.md` (la 07 va a mantenimiento). No se toca `hardware/v2` ni `docs/`; MCP no usado.

## Lo corregido por hallazgo

| ID | Corrección | Dónde |
|---|---|---|
| 01 | Pasta del EP: 10 ventanas sustituidas por 14 (11,03 mm² = 65 %), a 0,10 mm del taladro. Vías sin relleno. Resto de la huella sin cambios (pads 1–14, pad 15 F.Cu y B.Cu, 10 vías, patio, serigrafía, 3D). `kicad-cli fp export svg` carga la huella sin errores | `esp-riego.pretty/Infineon_PG-TDSO-14_…_EP2.65x6.4mm.kicad_mod` (pasta y `descr`); `BTT6050-1ERA.md` (Notas de los assets); log 01 (tabla de vías, verificación, «Requiere verificación») |
| 02 | Quitado «tapadas por la cara inferior». Texto nuevo: sin apertura de máscara en B.Cu; JLCPCB no garantiza el tapado de vías con apertura en F.Mask; el estado real se comprueba en los Gerber de la fase 5. 49,6 % → 65 % | `descr`, `BTT6050-1ERA.md`, log 01 (tabla de vías y cambio 10) |
| 03 | Cambio 1: «D4, D5 y D6–D11». Añadido el cambio 11 (l. 69, texto del informe). Cambio 10 con la pasta al 65 %. Grep en `docs/diseno/salidas.md` de «sin vías», «vías», «pasta», «85 %», «stencil» y «vía térmica»: la única mención en contra era la l. 69 (l. 349 es del borne; l. 347 ya es el cambio 10). No hay cambio extra | log 01 |
| 04 | Citadas las dos reglas de JLCPCB: vía a vía 0,2 mm y «Pad Hole-to-Hole Spacing» 0,45 mm (las vías son pads `thru_hole`); se cumplen con 0,9 mm | log 01 (tabla de vías), `BTT6050-1ERA.md` |
| 05 | (a) Fila de tensión: «V_NOM 8–36 V (típ. 28 V); V_S(OP) ampliado 5–48 V (Tabla 4, p. 8)»; la Tabla 1, p. 2, resume «5 V … 36 V» (comprobado en `datasheets/BTT6050-1ERA.pdf` pp. 2 y 8). (b) `M7.md`: `verificado_por: VAL-0024-01` | `BTT6050-1ERA.md`, `M7.md` |
| 06 | Cambios 1 y 2 en bloques de código. Añadido el cambio 12 (l. 5 de `salidas.md`: «… fueron confirmados por jr-conformidad el 2026-11-10 (SPEC-0024)») | log 01 |

## Cotas de la pasta nueva (F.Paste)

EP = pad 15: x ∈ ±1,325; y ∈ ±3,2 (16,96 mm²). Vías: x = ±0,95; y = 0, ±1,2, ±2,4; taladro 0,3 (radio 0,15), anillo 0,6.

| Ventana | Nº | Centro (x; y) | Tamaño | Área unit. | Área total | Rango | Rel. de área (0,12 mm) |
|---|---|---|---|---|---|---|---|
| Central | 2 | (0; ±1,625) | 1,40 × 2,95 | 4,130 | 8,260 | x ±0,70; |y| 0,15…3,10 | 3,96 |
| Lateral | 8 | (±1,0875; ±0,60 y ±1,80) | 0,375 × 0,70 | 0,2625 | 2,100 | x 0,90…1,275; |y| 0,25…0,95 y 1,45…2,15 | 1,02 |
| Extremo | 4 | (±1,0875; ±2,875) | 0,375 × 0,45 | 0,16875 | 0,675 | x 0,90…1,275; |y| 2,65…3,10 | 0,85 |
| **Total** | 14 | | | | **11,035 mm²** | | **mín. 0,85 (> 0,66)** |

Cobertura: 11,035 / 16,96 = **65,1 %** (intervalo habitual 50–80 %; antes 85 % sin vías; 49,6 % con el patrón anterior).

| Cota | Valor | Dónde |
|---|---|---|
| Distancia mínima pasta ↔ **taladro** | **0,10 mm** (central: x 0,70 frente a taladro desde 0,80; laterales y extremos: 0,10 en y frente al taladro más próximo, p. ej. y 0,25 frente a 0,15) | todas las vías |
| Distancia mínima pasta ↔ borde del EP | **0,05 mm** (laterales y extremos en x: 1,275 frente a 1,325); 0,10 mm en y (3,10 frente a 3,20); central en x: 0,625 mm | |
| Puente central ↔ lateral | 0,20 mm (x 0,70 → 0,90) | |
| Puente entre las dos centrales | 0,30 mm (y −0,15 → 0,15) | |
| Puente entre laterales/extremos de una columna | 0,50 mm (y 0,95 → 1,45; 2,15 → 2,65; −0,25 → 0,25) | |
| Puente entre columnas laterales | 1,80 mm (x −0,90 → 0,90, ocupado por las centrales) | |

El anillo de cobre (Ø 0,6) queda en parte bajo la pasta: el criterio es el taladro (0,10 mm), como pide VAL-0024-01-01.

## Verificación

- `kicad-cli fp export svg` sobre `esp-riego.pretty` (salida fuera del repositorio): carga y traza la huella sin errores.
- `verificar.py`: no aplica (ningún proyecto KiCad tocado).
- Gerber F.Paste de una placa de prueba: no regenerado en esta pasada; las cotas salen de la geometría de la huella (cálculo directo). Validación ya comprobó este patrón (VAL-0024-01-01).

## Requiere verificación de validación

| Pieza | Qué | Datasheet y página |
|---|---|---|
| `esp-riego:Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm` | Pasta de 14 ventanas (65 %) y `descr`; el resto igual que en el log 01 | BTT6050-1ERA Rev. 1.00: Fig. 53, p. 49; nota 2 de la Tabla 3 y Fig. 4, pp. 9–10; https://www.infineon.com/package/PG-TDSO-14-11 |
| `BTT6050-1ERA.md` | Fila de tensión (Tabla 4, p. 8; Tabla 1, p. 2) y texto de vías | BTT6050-1ERA, pp. 2 y 8 |

## Repaso de `gestion/checklists/librerias.md` (solo lo que cambia)

- Tabla de cotas de huella: cumple (arriba). Cobertura de pasta frente a 50–80 %: 65 %.
- Pin 1, patio, serigrafía, 3D, pads 1–14: sin cambios.
- Ficha: cumple (fechas y códigos sin cambios; fila de tensión corregida).
- Resto de la checklist: sin cambios respecto al log 01.

## Pendiente

- **Fase 5:** comprobar en los Gerber el estado real de las vías (F.Mask y B.Mask) y decidir, si hace falta, vías rellenas y tapadas de JLCPCB.
- **SPEC-0025:** aplicar ahora 12 cambios a `salidas.md` (los del log 01, con 1, 10, 11 y 12 actualizados).
- **Mantenimiento de fase 2:** VAL-0024-01-07 (datasheets y campos incoherentes entre hojas) y las dos propuestas de checklist de validación.
