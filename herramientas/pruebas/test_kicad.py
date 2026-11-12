"""Batería de regresión de herramientas/kicad.

Uso: python herramientas/pruebas/test_kicad.py [-v]

Localiza la raíz del repositorio buscando CLAUDE.md hacia arriba, copia `hardware/v2`,
`hardware/libraries` y `hardware/componentes` a una carpeta temporal y prueba cada herramienta
sobre esa copia: que tiene --help, que su salida cabe en 30 líneas, que no modifica lo que lee
y que da el resultado esperado. No usa la red (jlc.py se prueba con una respuesta guardada).
Se lanza con el Python del sistema; las herramientas que necesitan pcbnew o wx se relanzan
solas con el Python de KiCad. Necesita KiCad 10 instalado (kicad-cli y su Python).
"""
import hashlib
import json
import py_compile
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def _raiz():
    for carpeta in Path(__file__).resolve().parents:
        if (carpeta / "CLAUDE.md").is_file():
            return carpeta
    raise SystemExit("No se encuentra CLAUDE.md por encima de la batería.")


REPO = _raiz()
KICAD = REPO / "herramientas" / "kicad"
sys.path.insert(0, str(KICAD))
import _comun  # noqa: E402
import campos  # noqa: E402
import comprobar  # noqa: E402
import huella  # noqa: E402
import jlc  # noqa: E402
import restricciones  # noqa: E402

HERRAMIENTAS = ["jlc", "campos", "hoja", "sincronizar", "colocar", "vista", "huella", "restricciones", "comprobar"]
BTT6050 = "Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm"
TMP = BASE = None


def setUpModule():
    global TMP, BASE
    TMP = Path(tempfile.mkdtemp(prefix="test_kicad_"))
    BASE = TMP / "hardware"
    ignorar = shutil.ignore_patterns("*-backups", ".mcp-backups", "*.lck", "*.kicad_prl", "datasheets")
    for sub in ("v2", "libraries", "componentes"):
        shutil.copytree(REPO / "hardware" / sub, BASE / sub, ignore=ignorar)


def tearDownModule():
    shutil.rmtree(TMP, ignore_errors=True)


def correr(herramienta, *args):
    r = subprocess.run([sys.executable, str(KICAD / f"{herramienta}.py"), *map(str, args)], capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout, r.stderr


def verificar(carpeta):
    r = subprocess.run([sys.executable, str(REPO / "herramientas" / "verificar.py"), str(carpeta), "--json"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return json.loads(r.stdout)


def huella_md5(*carpetas):
    h = hashlib.md5()
    for carpeta in carpetas:
        for f in sorted(Path(carpeta).rglob("*")):
            if f.is_file():
                h.update(f.relative_to(carpeta).as_posix().encode())
                h.update(f.read_bytes())
    return h.hexdigest()


def copia(nombre):
    destino = BASE / nombre
    shutil.copytree(BASE / "v2", destino)
    return destino


def png(ruta):
    datos = Path(ruta).read_bytes()
    assert datos[:8] == b"\x89PNG\r\n\x1a\n", "no es un PNG"
    return struct.unpack(">II", datos[16:24])


class Generales(unittest.TestCase):
    def test_ayuda_y_compilacion(self):
        for h in HERRAMIENTAS:
            codigo, salida, _ = correr(h, "--help")
            self.assertEqual(codigo, 0, h)
            self.assertIn("Uso:", salida, h)
        for f in sorted(KICAD.glob("*.py")):
            py_compile.compile(str(f), cfile=str(TMP / (f.name + "c")), doraise=True)

    def test_no_modifican_lo_que_leen_y_salida_corta(self):
        tabla = TMP / "restr.csv"
        tabla.write_text("Red;Corriente;Ancho mín.;Separación\nGND;1 A;0,2;0,2\n", encoding="utf-8")
        v2, mod = BASE / "v2", BASE / "libraries" / "esp-riego.pretty" / f"{BTT6050}.kicad_mod"
        ordenes = [
            ("campos", "revisar", v2), ("comprobar", v2), ("huella", mod), ("huella", mod, "--json"),
            ("hoja", "pines", "RF_Module:ESP32-S3-WROOM-1"), ("hoja", "extraer", v2 / "mcu.kicad_sch", "-o", TMP / "nm.json"),
            ("hoja", "netlist", v2, v2), ("restricciones", v2, tabla), ("vista", "hoja", v2, "--hoja", "MCU", "-o", TMP / "nm1.png"),
            ("vista", "placa", v2, "--todo", "-o", TMP / "nm2.png"), ("colocar", v2 / "esp-riego.kicad_pcb", "--exportar", TMP / "nm.csv"),
            ("sincronizar", v2, "-o", TMP / "nm.kicad_pcb"),
        ]
        antes = huella_md5(BASE)
        for orden in ordenes:
            codigo, salida, error = correr(*orden)
            self.assertIn(codigo, (0, 1), f"{orden[:2]}: {error}")
            self.assertLessEqual(len(salida.strip().splitlines()), 30, orden[:2])
            self.assertGreater(len(salida.strip()), 0, orden[:2])
        self.assertEqual(antes, huella_md5(BASE), "alguna herramienta ha tocado lo que lee")

    def test_emitir_recorta(self):
        import contextlib
        import io
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            _comun.emitir([f"l{i}" for i in range(100)])
        lineas = salida.getvalue().strip().splitlines()
        self.assertEqual(len(lineas), 30)
        self.assertIn("71 líneas más", lineas[-1])


class Jlc(unittest.TestCase):
    RESPUESTA = {"data": {"componentPageInfo": {"list": [
        {"componentCode": "C25804", "componentModelEn": "0603WAF1002T5E", "componentBrandEn": "UNI-ROYAL",
         "componentLibraryType": "base", "stockCount": 42773225,
         "componentPrices": [{"startNumber": 1, "endNumber": 999, "productPrice": 0.0022},
                             {"startNumber": 1000, "endNumber": -1, "productPrice": 0.0011}]},
        {"componentCode": "C534868", "componentModelEn": "BTT6050-1ERA", "componentBrandEn": "Infineon",
         "componentLibraryType": "expand", "stockCount": 1628, "componentPrices": []}]}}}

    def test_interpretar(self):
        fila = jlc.interpretar("C25804", self.RESPUESTA, cantidad=5000)
        self.assertEqual((fila["tipo"], fila["stock"], fila["precio"]), ("Basic", 42773225, 0.0011))
        self.assertEqual(jlc.interpretar("C25804", self.RESPUESTA)["precio"], 0.0022)
        self.assertEqual(jlc.interpretar("C534868", self.RESPUESTA)["tipo"], "Extended")
        self.assertIsNone(jlc.interpretar("C1", self.RESPUESTA))
        self.assertIsNone(jlc.interpretar("C25804", {"data": None}))

    def test_codigos(self):
        self.assertEqual(jlc.codigos_de("U7 C534868 · CL21A226 y C25804, C12, C534868 (ABC123)"), ["C534868", "C25804"])


class Campos(unittest.TestCase):
    def test_rangos(self):
        self.assertEqual(campos.rangos(["R3", "R1", "R2", "C7", "R10", "R11"]), "C7, R1–R3, R10, R11")
        self.assertEqual(campos.expandir("R26–R31, C45 C46;D5"), ["R26", "R27", "R28", "R29", "R30", "R31", "C45", "C46", "D5"])

    def test_aplicar_y_revisar(self):
        origen = BASE / "v2" / "mcu.kicad_sch"
        tabla, destino = TMP / "campos.csv", TMP / "mcu_campos.kicad_sch"
        tabla.write_text('Refs;Value;Fabricante;DNP;Nota\nR16;;Otro fabricante;;con "comillas"\nC23-C24;;;sí;\nD5;Rojo;;no;\n',
                         encoding="utf-8")
        antes = origen.read_bytes()
        codigo, salida, error = correr("campos", "aplicar", tabla, origen, "-o", destino)
        self.assertEqual(codigo, 0, error)
        self.assertEqual(antes, origen.read_bytes())
        piezas = {s["ref"]: s for s in _comun.simbolos_hoja(_comun.leer(destino))}
        self.assertEqual(piezas["R16"]["props"]["Fabricante"], "Otro fabricante")
        self.assertEqual(piezas["R16"]["props"]["Nota"], 'con "comillas"')
        self.assertEqual(piezas["D5"]["props"]["Value"], "Rojo")
        self.assertTrue(piezas["C23"]["dnp"] and piezas["C24"]["dnp"] and not piezas["C25"]["dnp"])
        self.assertEqual(piezas["R17"]["props"]["Fabricante"], "UNI-ROYAL")   # lo que no está en la tabla no cambia
        codigo, salida, _ = correr("campos", "revisar", destino, "--json")
        r = json.loads(salida)
        self.assertEqual(codigo, 1)
        self.assertEqual(r["dnp"], ["C23", "C24"])
        self.assertTrue(any(d["pieza"] == "C25804" and d["campo"] == "Fabricante" for d in r["distintos"]), r["distintos"])
        # un campo vacío se detecta, y la tabla se compara con la hoja
        texto = _comun.leer(destino).replace('(property "LCSC Part#" "C7519"', '(property "LCSC Part#" ""')
        _comun.escribir(destino, texto)
        r = campos.revisar([destino], {destino.name: campos.leer_tabla(tabla)})
        self.assertIn("U6", r["faltan"][f"{destino.name}|LCSC Part#"])
        self.assertTrue(any("no está en la tabla" in t for t in r["tabla"]))
        self.assertFalse(any(t.startswith(("R16:", "C23:", "D5:")) for t in r["tabla"]), r["tabla"])


class Huella(unittest.TestCase):
    def test_btt6050(self):
        mod = BASE / "libraries" / "esp-riego.pretty" / f"{BTT6050}.kicad_mod"
        codigo, salida, error = correr("huella", mod, "--json")
        self.assertEqual(codigo, 0, error)
        r = json.loads(salida)
        self.assertEqual(len(r["vias"]), 10)
        self.assertEqual({(v["taladro"], v["corona"]) for v in r["vias"]}, {(0.3, 0.6)})
        self.assertTrue(r["vias_fab02"])
        self.assertEqual(round(r["ep"]["pasta_pct"]), 65)
        self.assertEqual(r["ep"]["pasta_sobre_taladro"], 0)
        self.assertEqual(r["paso"], 1.27)
        codigo, salida, _ = correr("huella", f"esp-riego:{BTT6050}", "--proyecto", BASE / "v2", "--simbolo", "esp-riego:BTT6050-1ERA")
        self.assertIn("10 de 0,3 / 0,6", salida)
        self.assertIn("= 65 % del pad", salida)
        self.assertIn("sin pad ninguno · pads sin pin ninguno", salida)

    def test_huella_con_defectos(self):
        mod = TMP / "mala.kicad_mod"
        mod.write_text('''(footprint "mala" (layer "F.Cu") (attr smd)
  (fp_line (start -3 0) (end 3 0) (stroke (width 0.12) (type solid)) (layer "F.SilkS"))
  (fp_line (start -3 1.2) (end 3 1.2) (stroke (width 0.12) (type solid)) (layer "F.SilkS"))
  (pad "1" smd rect (at -1 0) (size 1 1) (layers "F.Cu" "F.Mask" "F.Paste"))
  (pad "2" smd rect (at 1 0) (size 1 1) (layers "F.Cu" "F.Mask" "F.Paste"))
  (pad "3" smd rect (at 0 4) (size 4 4) (layers "F.Cu" "F.Mask"))
  (pad "3" thru_hole circle (at 0 4) (size 0.5 0.5) (drill 0.2) (layers "*.Cu"))
  (pad "" smd rect (at -1 4) (size 2 2) (layers "F.Paste"))
  (pad "" smd rect (at 0 4) (size 2 2) (layers "F.Paste"))
)''', encoding="utf-8")
        r = huella.analizar(mod)
        self.assertEqual(r["serigrafia_sobre_pads"], 1)
        self.assertEqual(r["patio"], {})
        self.assertFalse(r["vias_fab02"])
        self.assertEqual(r["ep"]["num"], "3")
        self.assertAlmostEqual(r["ep"]["pasta"], 6.0)          # dos ventanas de 2 × 2 solapadas 1 × 2
        self.assertEqual(r["ep"]["pasta_sobre_taladro"], 2)
        self.assertEqual(r["modelos"], [])
        self.assertAlmostEqual(huella.area_union([(0, 0, 2, 2), (1, 1, 3, 3)]), 7.0)


class Hoja(unittest.TestCase):
    def test_regenera_mcu_con_la_misma_netlist(self):
        proy = copia("v2_hoja")
        desc = TMP / "mcu.json"
        codigo, salida, error = correr("hoja", "extraer", BASE / "v2" / "mcu.kicad_sch", "-o", desc)
        self.assertEqual(codigo, 0, salida + error)
        codigo, salida, error = correr("hoja", "generar", desc, "--proyecto", proy, "-o", proy / "mcu.kicad_sch")
        self.assertEqual(codigo, 0, salida + error)
        self.assertIn("21 piezas (21 con su UUID)", salida)
        self.assertNotEqual((BASE / "v2" / "mcu.kicad_sch").read_bytes(), (proy / "mcu.kicad_sch").read_bytes())
        codigo, salida, error = correr("hoja", "netlist", BASE / "v2", proy)
        self.assertEqual(codigo, 0, salida + error)
        self.assertIn(": 0 diferencias", salida)
        r = verificar(proy)
        self.assertEqual(r["erc"]["total"], 0, r["erc"])
        self.assertEqual(r["paridad"]["total"], 0, r["paridad"])

    def test_no_sustituye_una_hoja_con_cables(self):
        codigo, salida, _ = correr("hoja", "extraer", BASE / "v2" / "alimentacion.kicad_sch", "-o", TMP / "ali.json")
        self.assertEqual(codigo, 1)
        self.assertIn("wire", salida)
        self.assertFalse((TMP / "ali.json").exists())
        desc = TMP / "vacia.json"
        desc.write_text('{"piezas": []}', encoding="utf-8")
        codigo, _, error = correr("hoja", "generar", desc, "--proyecto", BASE / "v2", "--como", "alimentacion.kicad_sch",
                                  "-o", TMP / "ali.kicad_sch")
        self.assertEqual(codigo, 2)
        self.assertIn("--forzar", error)

    def test_hoja_nueva_desde_cero(self):
        proy = copia("v2_nueva")
        campos_ = {"Footprint": "Resistor_SMD:R_0603_1608Metric", "MPN": "X", "Fabricante": "X", "Datasheet": "http://x",
                   "Description": "prueba", "LCSC Part#": "C25804"}
        desc = {"papel": "A4", "cajetin": {"title": "Prueba", "comment": {"1": "Hoja de prueba"}},
                "piezas": [
                    {"ref": "R901", "simbolo": "Device:R", "x": 100, "y": 100, "giro": 0, "campos": dict(campos_, Value="1k"),
                     "pines": {"1": "P:+3V3", "2": "L:NODO"}},
                    {"ref": "R902", "simbolo": "Device:R", "x": 120, "y": 100, "giro": 90, "campos": dict(campos_, Value="2k"),
                     "pines": {"1": "L:NODO", "2": "G:GLOBAL_X:input"}},
                    {"ref": "D901", "simbolo": "Device:LED", "x": 140, "y": 100, "giro": 90, "dnp": True,
                     "campos": dict(campos_, Value="Rojo", Footprint="LED_SMD:LED_0603_1608Metric"),
                     "pines": {"1": "P:GND", "2": "NC"}},
                    {"ref": "U901", "simbolo": "Power_Protection:USBLC6-2SC6", "x": 180, "y": 100,
                     "campos": dict(campos_, Footprint="Package_TO_SOT_SMD:SOT-23-6"),
                     "pines": {"1": "L:NODO", "2": "P:GND", "3": "H:SALE:output", "4": "", "5": "P:+3V3", "6": "NC"}}],
                "textos": [{"x": 50, "y": 50, "tam": 2, "negrita": True, "texto": "Dos\nlíneas"}]}
        archivo = TMP / "nueva.json"
        archivo.write_text(json.dumps(desc, ensure_ascii=False), encoding="utf-8")
        codigo, salida, error = correr("hoja", "generar", archivo, "--proyecto", proy, "-o", proy / "salidas.kicad_sch", "--forzar")
        self.assertEqual(codigo, 0, salida + error)
        red = _comun.exportar_netlist(proy, "esp-riego", TMP / "nueva.net")
        self.assertEqual(red["comps"]["R902"]["value"], "2k")
        self.assertEqual(red["comps"]["U901"]["footprint"], "Package_TO_SOT_SMD:SOT-23-6")
        self.assertIn("dnp", red["comps"]["D901"]["props"])
        nodo = next(n for n, nodos in red["redes"].items() if ("R901", "2") in nodos)
        self.assertTrue(nodo.endswith("NODO"))
        self.assertEqual(red["redes"][nodo], {("R901", "2"), ("R902", "1"), ("U901", "1")})
        self.assertIn(("R901", "1"), red["redes"]["+3V3"])
        self.assertIn(("U901", "2"), red["redes"]["GND"])
        self.assertIn(("R902", "2"), red["redes"]["GLOBAL_X"])
        # la hoja generada se puede volver a extraer y da la misma descripción de conexiones
        codigo, _, error = correr("hoja", "extraer", proy / "salidas.kicad_sch", "-o", TMP / "nueva2.json")
        self.assertEqual(codigo, 0, error)
        otra = json.loads((TMP / "nueva2.json").read_text(encoding="utf-8"))
        self.assertEqual({p["ref"]: p["pines"] for p in otra["piezas"]}, {p["ref"]: p["pines"] for p in desc["piezas"]})
        self.assertEqual(otra["textos"][0]["texto"], "Dos\nlíneas")
        # falta declarar un pin: error claro y no se escribe
        desc["piezas"][0]["pines"].pop("2")
        archivo.write_text(json.dumps(desc, ensure_ascii=False), encoding="utf-8")
        codigo, _, error = correr("hoja", "generar", archivo, "--proyecto", proy, "-o", TMP / "no.kicad_sch", "--como", "salidas.kicad_sch")
        self.assertEqual(codigo, 2)
        self.assertIn("R901: pines sin conexión declarada: 2", error)
        self.assertFalse((TMP / "no.kicad_sch").exists())


class Pcb(unittest.TestCase):
    def test_sincronizar_deja_la_paridad_a_cero(self):
        proy = copia("v2_sync")
        pcb = proy / "esp-riego.kicad_pcb"
        texto = _comun.leer(pcb)
        quitar = []
        for nombre, i, j in _comun.trozos(texto):
            if nombre == "footprint" and any(f'(property "Reference" "{r}"' in texto[i:j] for r in ("U5", "R16")):
                quitar.append((i, j))
        self.assertEqual(len(quitar), 2)
        for i, j in reversed(quitar):
            texto = texto[:i] + texto[j:]
        texto = texto.replace('(property "Value" "22uF"', '(property "Value" "cambiado"', 1)
        # R17 pasa a ser una huella sin símbolo (otra referencia y otra ruta): se borra y R17 entra de nuevo
        i = texto.index('(property "Reference" "R17"')
        j = texto.index('(path "', i)
        texto = (texto[:i] + '(property "Reference" "R999"' + texto[i + len('(property "Reference" "R17"'):j]
                 + '(path "/00000000-0000-0000-0000-00000000dead/00000000-0000-0000-0000-00000000beef"'
                 + texto[texto.index('"', j + 7) + 1:])
        _comun.escribir(pcb, texto)
        antes = verificar(proy)
        self.assertGreater(antes["paridad"]["total"], 0)
        md5 = huella_md5(proy)
        codigo, salida, error = correr("sincronizar", proy, "-o", TMP / "sync.kicad_pcb", "--actualizar", "U6")
        self.assertEqual(codigo, 0, salida + error)
        self.assertIn("nuevas 3 · borradas 1 · recargadas 1", salida)
        self.assertIn("Paridad 0", salida)
        self.assertIn("Nuevas (sin colocar): U5 R16 R17", salida)
        self.assertIn("Borradas: R999", salida)
        self.assertEqual(md5, huella_md5(proy))
        shutil.copyfile(TMP / "sync.kicad_pcb", pcb)
        despues = verificar(proy)
        self.assertEqual(despues["paridad"]["total"], 0, despues["paridad"])
        self.assertEqual(despues["drc"]["errores"], 0, despues["drc"])

    def test_colocar(self):
        origen = BASE / "v2" / "esp-riego.kicad_pcb"
        tabla, destino, vuelta = TMP / "col.csv", TMP / "col.kicad_pcb", TMP / "col2.csv"
        tabla.write_text("ref;x;y;giro;cara\nU5;50;20;90;F\nC24;40;30;;B\nR16;45.5;30;180;\nZZ9;1;1;0;F\n", encoding="utf-8")
        antes = origen.read_bytes()
        codigo, salida, error = correr("colocar", origen, tabla, "-o", destino)
        self.assertEqual(codigo, 1, salida + error)      # ZZ9 no existe
        self.assertIn("3 huellas colocadas de 4", salida)
        self.assertIn("ZZ9", salida)
        self.assertEqual(antes, origen.read_bytes())
        codigo, _, error = correr("colocar", destino, "--exportar", vuelta)
        self.assertEqual(codigo, 0, error)
        filas = {f.split(",")[0]: f.split(",") for f in vuelta.read_text(encoding="utf-8").splitlines()}
        self.assertEqual(filas["U5"][1:], ["50", "20", "90", "F"])
        self.assertEqual(filas["R16"][1:], ["45.5", "30", "180", "F"])
        self.assertEqual((filas["C24"][1], filas["C24"][2], filas["C24"][4]), ("40", "30", "B"))

    def test_vista(self):
        v2 = BASE / "v2"
        codigo, salida, error = correr("vista", "hoja", v2, "--hoja", "mcu.kicad_sch", "--zona", "150,95,280,190", "--ancho", 800, "-o", TMP / "z.png")
        self.assertEqual(codigo, 0, salida + error)
        self.assertEqual(png(TMP / "z.png"), (800, 585))
        self.assertGreater((TMP / "z.png").stat().st_size, 20000)   # con dibujo, no en blanco
        codigo, salida, error = correr("vista", "huella", f"esp-riego:{BTT6050}", "--proyecto", v2, "--ancho", 400, "-o", TMP / "h.png")
        self.assertEqual(codigo, 0, salida + error)
        self.assertEqual(png(TMP / "h.png")[0], 400)
        codigo, salida, error = correr("vista", "placa", v2, "--ancho", 600, "-o", TMP / "p.png")
        self.assertEqual(codigo, 0, salida + error)
        self.assertEqual(png(TMP / "p.png")[0], 600)
        codigo, _, error = correr("vista", "hoja", v2, "--hoja", "noexiste", "-o", TMP / "n.png")
        self.assertEqual(codigo, 2)
        self.assertIn("no hay ninguna hoja", error)


class Restricciones(unittest.TestCase):
    PCB = '''(kicad_pcb (version 20260206) (generator "pcbnew")
  (segment (start 0 0) (end 10 0) (width 1.2) (layer "F.Cu") (net "/Ali/BUS_24V") (uuid "a"))
  (segment (start 0 5) (end 10 5) (width 0.2) (layer "F.Cu") (net "/Sal/OUT1") (uuid "b"))
  (segment (start 0 5.5) (end 10 5.5) (width 0.2) (layer "F.Cu") (net "GND") (uuid "c"))
  (segment (start 0 5.2) (end 10 5.2) (width 0.2) (layer "B.Cu") (net "SIG") (uuid "d"))
  (via (at 20 20) (size 0.5) (drill 0.2) (layers "F.Cu" "B.Cu") (net "GND") (uuid "e"))
  (via (at 30 20) (size 0.6) (drill 0.3) (layers "F.Cu" "B.Cu") (net "SIG") (uuid "f"))
)'''
    PRO = {"net_settings": {"classes": [{"name": "Default", "clearance": 0.2}, {"name": "Salidas", "clearance": 0.6}],
                            "netclass_patterns": [{"netclass": "Salidas", "pattern": "/Sal/OUT*"}]}}

    def setUp(self):
        self.d = Path(tempfile.mkdtemp(dir=TMP))
        (self.d / "p.kicad_pcb").write_text(self.PCB, encoding="utf-8")
        (self.d / "p.kicad_pro").write_text(json.dumps(self.PRO), encoding="utf-8")
        (self.d / "t.md").write_text(
            "| Red | Corriente | Ancho mín. | Separación | Ubicación / keepout | Notas |\n|---|---|---|---|---|---|\n"
            "| `BUS_24V` | 5,1 A | 1,2 mm | 0,2 mm | — | bus |\n| `OUT*` | 4,9 A | ≥ 1,2 | 0,6 | | salidas |\n"
            "| SIG | | 0,2 | — | | |\n| NADA, NADA2 | | 1 | 1 | | |\n", encoding="utf-8")

    def test_tabla_y_filas(self):
        tabla = restricciones.leer_tabla(self.d / "t.md")
        self.assertEqual([(f["redes"], f["ancho"], f["separacion"]) for f in tabla],
                         [(["BUS_24V"], 1.2, 0.2), (["OUT*"], 1.2, 0.6), (["SIG"], 0.2, None), (["NADA", "NADA2"], 1.0, 1.0)])
        r = restricciones.comprobar(self.d / "p.kicad_pcb", tabla)
        self.assertEqual([f["estado"] for f in r["filas"]], ["OK", "FALLA", "OK", "SIN DATOS"])
        salidas = r["filas"][1]
        self.assertEqual(salidas["redes"], ["/Sal/OUT1"])
        self.assertEqual(salidas["separacion_regla"], 0.6)          # la clase Salidas ya pide 0,6
        self.assertAlmostEqual(salidas["separacion_medida"], 0.3)   # pero la pista de GND está a 0,3
        self.assertEqual(len(salidas["motivos"]), 2)                # ancho y separación medida
        self.assertEqual(r["vias_bajo_fab02"], 1)
        codigo, salida, error = correr("restricciones", self.d / "p.kicad_pcb", self.d / "t.md")
        self.assertEqual(codigo, 1, error)
        self.assertEqual(len(salida.strip().splitlines()), 5)
        (self.d / "n.md").write_text("| Red | Ancho mín. |\n|---|---|\n| **GND**, `OUT*` | 0,2 |\n", encoding="utf-8")
        self.assertEqual(restricciones.leer_tabla(self.d / "n.md")[0]["redes"], ["GND", "OUT*"])   # negrita y comodín

    def test_reglas_del_dru_y_csv(self):
        (self.d / "p.kicad_dru").write_text('(version 1)\n(rule "gnd"\n  (condition "A.NetName == \'GND\'")\n'
                                            '  (constraint clearance (min 0.5mm)))\n(rule "sal" (condition "A.NetClass == \'Salidas\'")'
                                            ' (constraint clearance (min 0.8mm)))\n', encoding="utf-8")
        regla = restricciones.reglas_separacion(self.d, "p")
        self.assertEqual(regla("GND")[0], 0.5)
        self.assertEqual(regla("/Sal/OUT1")[0], 0.8)
        self.assertEqual(regla("SIG"), (0.2, "clase Default"))
        (self.d / "t.csv").write_text("Red;Corriente;Ancho mín.;Separación;Vía\nGND;1 A;0,2;0,5;0,2/0,5\n", encoding="utf-8")
        r = restricciones.comprobar(self.d / "p.kicad_pcb", restricciones.leer_tabla(self.d / "t.csv"), self.d, "p")
        self.assertEqual(r["filas"][0]["estado"], "FALLA")          # regla 0,5 cumple; medida 0,3 no
        self.assertEqual(len(r["filas"][0]["motivos"]), 1)


class Comprobar(unittest.TestCase):
    def estados(self, carpeta):
        r = comprobar.resumen(carpeta)
        return {x["punto"]: x for x in r["puntos"]}, r

    def test_proyecto_actual(self):
        puntos, r = self.estados(BASE / "v2")
        self.assertEqual(len(puntos), 19)
        self.assertLessEqual(len(r["lineas"]), 30)
        for punto in ("esquema.hojas", "esquema.huellas", "esquema.vias", "layout.incrustados", "layout.salida",
                      "layout.smd_cara", "librerias.formato", "librerias.rutas", "librerias.serigrafia"):
            self.assertEqual(puntos[punto]["estado"], "OK", puntos[punto])
        self.assertNotIn("ERROR", {x["estado"] for x in puntos.values()})

    def test_detecta_lo_que_se_rompe(self):
        proy = copia("v2_rota")
        (proy / "huerfana.kicad_sch").write_text('(kicad_sch (version 20260306) (uuid "x") (paper "A4"))', encoding="utf-8")
        pcb = proy / "esp-riego.kicad_pcb"
        texto = _comun.leer(pcb).rstrip()
        self.assertTrue(texto.endswith(")"))
        texto = texto[:-1] + ('\t(embedded_files\n\t\t(file\n\t\t\t(name "viejo.kicad_wks")\n\t\t\t(type worksheet)\n\t\t)\n\t)\n'
                              '\t(zone\n\t\t(net "GND")\n\t\t(layer "F.Cu")\n\t\t(polygon (pts (xy 0 0) (xy 1 0) (xy 1 1)))\n\t)\n)\n')
        texto = texto.replace("(attr smd)", "(attr smd dnp)", 1).replace('(outputdirectory "")', '(outputdirectory "C:/tmp/gerber")')
        _comun.escribir(pcb, texto)
        tabla = proy / "fp-lib-table"
        tabla.write_text(tabla.read_text(encoding="utf-8").replace("${KIPRJMOD}/../libraries", "C:/libs"), encoding="utf-8")
        mcu = proy / "mcu.kicad_sch"
        _comun.escribir(mcu, _comun.leer(mcu).replace('(property "MPN" "USBLC6-2SC6"', '(property "MPN" ""')
                        .replace('"Package_TO_SOT_SMD:SOT-23-6"', '"Package_TO_SOT_SMD:NoExiste"'))
        (proy / "restricciones.csv").write_text("Red;Ancho mín.;Separación\nGND;0,2;0,2\n", encoding="utf-8")
        puntos, _ = self.estados(proy)
        for punto in ("esquema.hojas", "esquema.campos", "esquema.huellas", "esquema.dnp", "layout.zonas",
                      "layout.incrustados", "librerias.rutas"):
            self.assertEqual(puntos[punto]["estado"], "FALLA", puntos[punto])
        self.assertIn("huerfana.kicad_sch", puntos["esquema.hojas"]["detalle"][0])
        self.assertIn("U6", puntos["esquema.campos"]["detalle"][0])
        self.assertIn("viejo.kicad_wks", puntos["layout.incrustados"]["detalle"][0])
        self.assertEqual(puntos["layout.restricciones"]["estado"], "N/A")   # hay tabla, pero aún no hay pistas
        self.assertEqual(puntos["layout.salida"]["estado"], "FALLA" if '(outputdirectory "C:/tmp/gerber")' in texto else "OK")

    def test_no_se_cae(self):
        r = comprobar.resumen(TMP / "no-existe")
        self.assertEqual(r["fallan"], 0)
        self.assertEqual(len(r["lineas"]), 1)
        codigo, salida, _ = correr("comprobar", BASE / "v2", "--punto", "librerias.fichas")
        self.assertIn(codigo, (0, 1))
        self.assertLessEqual(len(salida.strip().splitlines()), 30)


if __name__ == "__main__":
    unittest.main()
