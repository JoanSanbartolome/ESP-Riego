# Informe de modelos 3D — ESP-Riego (SolidCraft)

Generador: `gen.py` produce `sht4x.json`, `pgtdso14.json` y `borne.json`. Regenerar con
`solidcraft-cli run <x>.json --out <nombre>.step`. Mediciones: `*.eval.json`. Capturas: `*_iso/top/front/bottom.png`.
Comprobacion en KiCad 10: hecha con una placa de prueba (`kicad_test/`, capturas `kicad_prueba_*.png`) que NO esta versionada; solo queda el resultado descrito al final.
Convencion: mm, Z=0 cara superior de placa, modelo (x, y) = huella (x, -y), offset 0 / rotacion 0 / escala 1. Colores (cuerpo, metal) conservados en el STEP (visibles en el render de KiCad).

## 1. SHT4x — `Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad.step`

Cotas (SHT4x.pdf, Fig. 15, p. 15 de la V7.3):
- Cuerpo 1,5 x 1,5 (fig.), altura 0,54 (fig.), pitch 0,8 (fig.), pads de 0,3 en Y (fig.), altura de pad 0,2 (cota "0,2" del alzado lateral, interpretada como grosor del pad: supuesto).
- Pads: 0,3 mm de longitud los del lado izquierdo y 0,4 mm los del derecho (cotas 0,3 y 0,4 de la vista inferior, lectura literal); pads a ras del borde del cuerpo.
- Apertura del sensor: diametro 0,6 (fig.), profundidad 0,15 (supuesto), centrada.
- Posiciones: pads en x=-0,7 / +0,7 e y=+-0,4 (huella oficial KiCad). Pin 1 = (-0,7, +0,4) modelo = (-0,7, -0,4) huella.

Bounding box medido: x -0,75..0,75; y -0,75..0,75; z 0..0,54 (= 1,5 x 1,5 x 0,54). OK.

| Pin | Pad huella (x,y) | Modelo esperado | Modelo medido (x, y) | |
|---|---|---|---|---|
| 1 | (-0,7, -0,4) | (-0,7, +0,4) | x -0,75..-0,45, y +0,25..+0,55 | OK |
| 2 | (-0,7, +0,4) | (-0,7, -0,4) | x -0,75..-0,45, y -0,55..-0,25 | OK |
| 3 | (+0,7, +0,4) | (+0,7, -0,4) | x +0,35..+0,75, y -0,55..-0,25 | OK |
| 4 | (+0,7, -0,4) | (+0,7, +0,4) | x +0,35..+0,75, y +0,25..+0,55 | OK |

Marca de pin 1 (rev. 2): hendidura circular de diametro 0,2 y 0,05 de profundidad en la cara superior, centro modelo (-0,5, +0,55) (= huella (-0,5, -0,55), esquina del pad 1), fondo en gris para que se vea. Fig. 15 muestra un circulo en esa esquina; su diametro es supuesto. Los pads no sobresalen del contorno del cuerpo (x +-0,75, y +-0,75): los pads se ven como las muescas a ras de la Fig. 15. Altura total 0,54 (medida).

Limitaciones: sin rotulado; sin pad central (die pad) ni su muesca (la huella es NoCentralPad y la figura no se lee con certeza); la cota "1 +-0,1" no se uso. Pads de 0,3/0,4 no coinciden exactamente con los de 0,5 de la huella (la huella tiene holgura de soldadura).

## 2. PG-TDSO-14 — `Infineon_PG-TDSO-14.step`

Cotas (BTT6050-1ERA.pdf, Fig. 53, p. 49; no se contrasto numericamente con BTT6030-2ERA):
- Cuerpo 8,65 (+-0,1) x 3,9 (+-0,1) (fig.). En la huella el eje largo va en Y (pads de la huella a x=+-2,73; el pie de las patillas del modelo, x +-1,95..3,00, cae dentro de ellos).
- Altura total 1,15 max (fig.); standoff 0,05 (fig.): cuerpo de z=0,05 a 1,15 (cota "(0,95)" entre parentesis, de referencia, NO usada: se tomo el maximo de 1,15; supuesto conservador para interferencias).
- Pad expuesto 6,4 x 2,65 (fig.), z 0..0,05 (supuesto: grosor = standoff).
- Patillas: ancho 0,4 (fig.), paso 1,27 (fig.), span de puntas 6,0 +-0,2 (fig.: x=+-3,0), pie plano 0,67 de largo (fig.; modelado de |x|=2,3 a 3,0), grosor 0,2 (cota "(0,2)" de la fig.), hombro a z 0,45..0,65 y tramo vertical |x|=2,3..2,5 (supuestos de forma). El angulo de 0..8 grados del flanco del cuerpo no se modelo (cuerpo prismatico).

Bounding box medido: x -3,0..3,0 (6,0 = span de puntas); y -4,325..4,325 (8,65); z 0..1,15. Cuerpo: 3,9 x 8,65 x 1,10. OK.

| Pin | Pad huella (x,y) | Modelo esperado | Modelo medido | |
|---|---|---|---|---|
| 1 | (-2.73, -3.81) | (-2.73, +3.81) | pie x -3.00..-1.95, y centro +3.81 | OK |
| 2 | (-2.73, -2.54) | (-2.73, +2.54) | pie x -3.00..-1.95, y centro +2.54 | OK |
| 3 | (-2.73, -1.27) | (-2.73, +1.27) | pie x -3.00..-1.95, y centro +1.27 | OK |
| 4 | (-2.73, +0.00) | (-2.73, -0.00) | pie x -3.00..-1.95, y centro +0.00 | OK |
| 5 | (-2.73, +1.27) | (-2.73, -1.27) | pie x -3.00..-1.95, y centro -1.27 | OK |
| 6 | (-2.73, +2.54) | (-2.73, -2.54) | pie x -3.00..-1.95, y centro -2.54 | OK |
| 7 | (-2.73, +3.81) | (-2.73, -3.81) | pie x -3.00..-1.95, y centro -3.81 | OK |
| 8 | (+2.73, +3.81) | (+2.73, -3.81) | pie x +1.95..+3.00, y centro -3.81 | OK |
| 9 | (+2.73, +2.54) | (+2.73, -2.54) | pie x +1.95..+3.00, y centro -2.54 | OK |
| 10 | (+2.73, +1.27) | (+2.73, -1.27) | pie x +1.95..+3.00, y centro -1.27 | OK |
| 11 | (+2.73, +0.00) | (+2.73, -0.00) | pie x +1.95..+3.00, y centro +0.00 | OK |
| 12 | (+2.73, -1.27) | (+2.73, +1.27) | pie x +1.95..+3.00, y centro +1.27 | OK |
| 13 | (+2.73, -2.54) | (+2.73, +2.54) | pie x +1.95..+3.00, y centro +2.54 | OK |
| 14 | (+2.73, -3.81) | (+2.73, +3.81) | pie x +1.95..+3.00, y centro +3.81 | OK || 15 (EP) | (0, 0) 2,65 x 6,4 | centro (0,0) | slug x +-1,325, y +-3,2 | OK |

Marca de pin 1 (rev. 2): hendidura circular de diametro 0,8 y 0,1 de profundidad en la cara superior, centro modelo (-1,2, +3,4) (= huella (-1,2, -3,4)), junto al pad 1 (-2,6, -3,81) y lejos de los pads 7/8 (fondo en gris). La Fig. 53 solo indica 'INDEX MARKING' en esa esquina sin cotas: diametro y profundidad supuestos.

Limitaciones: patillas rectas de seccion constante; sin radios de doblado; los pads "" de pasta de la huella no aplican.

## 3. Borne Kangnex WJ500V-5.08-2P — `TerminalBlock_Kangnex_WJ500V-5.08-2P.step`

Cotas (WJ500V-5.08-2P.pdf, dibujo unico; es de 3 polos en el dibujo, se modelaron 2):
- Altura total 14,00 +-0,2 (corte A-A). Profundidad 10,00 +-0,2 (corte A-A). Largo N x 5,08 (vista superior) = 10,16, de x=-2,54 a 7,62.
- Pines: 4,50 +-0,2 por debajo del cuerpo (corte A-A); rev. 3: pines RECTANGULARES 0,9 x 0,8 del datasheet (diagonal 1,2 mm; el taladro de 1,3 mm cumple diagonal + 0,1); sin punta chaflanada. Posicion: eje del pin a 4,50 de la cara trasera (cota 4,50 +-0,2 del corte) y 5,5 de la frontal.
- Perfil lateral (YZ) tomado a escala del corte A-A: frontal vertical hasta z=7,1 (coincide con la linea a z~7,2 de la vista frontal), inclinado hasta z=14 en y=+3,86, cara superior plana de y=+3,86 a -2,26, bajada inclinada hasta z=9,8 en y=-3,46, escalon trasero a z=9,8 (cota 9,80) hasta y=-4,5. (Valores medidos sobre el dibujo: supuestos de +-0,2.)
- Abertura de cable: 2,6 ancho x 3,1 alto (vista frontal), z 2,2..5,3 (medido en el dibujo), profundidad 6,0 (supuesto), en la cara frontal (+Y).
- Aberturas de tornillo: diametro 3,9 (medido en la vista superior), a 4,9 de la cara frontal (y=+0,6), cajeado de 2,1 mm (supuesto); cabeza de tornillo metalica diametro 3,5 de z=12,0 a 13,2 (supuesto).
- Color: verde (opcion de codigo 4 del datasheet; supuesto, el dibujo no fija color).

Orientacion (supuesto): la entrada de cable queda hacia +Y del modelo (-Y de la huella, arriba en pantalla). La huella ya marca el lado de entrada del cable (-Y de la huella, hacia +Y del modelo), asi que no hace falta rotar el modelo. El cuerpo es 10 mm de profundidad pero asimetrico respecto a los pines (y -4,5..+5,6), de modo que sobresale 0,6 mm del rectangulo +-5,0 de la huella por el lado de entrada (dentro del courtyard, 5,75).

Bounding box medido: cuerpo x -2,54..7,62 (10,16), y -4,5..5,6 (el extremo +5,6 es el marco de la ventana del cable, CARTESIAN_POINT y=5,6; el resto del cuerpo llega a 5,5), z 0..14,0; con pines z -4,5..14,0. OK.

| Pin | Pad huella (x,y) | Modelo medido | |
|---|---|---|---|
| 1 | (0, 0) | x -0,4..0,4, y -0,4..0,4 (rectangular 0,9 x 0,8), z -4,5..0 | OK |
| 2 | (5,08, 0) | x 4,68..5,48, y -0,4..0,4 (rectangular 0,9 x 0,8), z -4,5..0 | OK |

Marca de pin 1 (rev. 2): rebaje de 0,4 x 0,4 mm en la arista superior del extremo x=-2,54 (lado del pin 1, x=0), a lo largo de la cara superior. Confirmado por volumen (1150,4 -> 1149,5 mm3); en el render top apenas se aprecia.

Limitaciones: sin elementos internos (abrazadera, rosca), sin chaflanes del marco de la abertura, sin marcas ni rotulos.

## Comprobacion en KiCad 10
Placa de prueba (`kicad_test/prueba.kicad_pcb`, no versionada) con los tres footprints reales (copia, con `(model ...)` a los STEP nuevos, offset 0, rot 0, escala 1). `kicad-cli pcb render` (top e iso) y `pcb export step` terminan sin errores: los modelos cargan con color, el pin 1 (SHT4x y TDSO) cae arriba a la izquierda sobre el pad 1 y las patillas caen sobre sus pads. Rev. 2: render top ampliado (recortes en kicad_test/c_*.png): la marca del TDSO queda junto al pad 1 (arriba izquierda, junto al triangulo de pin 1 de la huella), no junto a 7/8; la del SHT4x queda en la esquina del pad 1. Export STEP sin errores. No se comparo contra los modelos oficiales de KiCad.
