"""Batería de regresión de herramientas/kicad.

Uso: python herramientas/pruebas/test_kicad.py [-v]

Localiza la raíz del repositorio buscando CLAUDE.md hacia arriba, copia `hardware/v2`,
`hardware/libraries` y `hardware/componentes` a una carpeta temporal y prueba cada herramienta
sobre esa copia: que su --help y su salida caben en 30 líneas, que no modifica lo que lee y que
da el resultado esperado. Cada punto de comprobar.py tiene al menos un caso que lo hace fallar
(clase Mutaciones). No usa la red (jlc.py se prueba con una respuesta guardada).
Se lanza con el Python del sistema; las herramientas que necesitan pcbnew o wx se relanzan
solas con el Python de KiCad. Necesita KiCad 10 instalado (kicad-cli y su Python).
"""
import hashlib
import json
import py_compile
import re
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
            self.assertLessEqual(len(salida.strip().splitlines()), 30, f"--help de {h}")
        for f in sorted(KICAD.glob("*.py")):
            py_compile.compile(str(f), cfile=str(TMP / (f.name + "c")), doraise=True)

    def test_no_modifican_lo_que_leen_y_salida_corta(self):
        tabla = TMP / "restr.csv"
        tabla.write_text("Red;Corriente;Ancho mín.;Separación\nGND;1 A;0,2;0,2\n", encoding="utf-8")
        v2, mod = BASE / "v2", BASE / "libraries" / "esp-riego.pretty" / f"{BTT6050}.kicad_mod"
        ordenes = [
            ("campos", "revisar", v2), ("comprobar", v2), ("comprobar", "--lista"), ("huella", mod), ("huella", mod, "--json"),
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
        self.assertEqual(r["tipo_pads"], "smd")            # la vía del pad 3 es térmica: no la hace pasante
        self.assertIsNone(r["attr_incoherente"])

    def test_textos_de_serigrafia(self):
        base = '''(footprint "t" (layer "F.Cu") (attr smd)
  (property "Reference" "REF**" (at {x} {y} {giro}) (layer "F.SilkS") {oculto}(effects (font (size 1 1) (thickness 0.15)){just}))
  (fp_text user "${{REFERENCE}}" (at 0 0 0) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))
  (pad "1" smd rect (at -2 0) (size 1 1) (layers "F.Cu" "F.Mask" "F.Paste"))
  (pad "2" smd rect (at 2 0) (size 1 1) (layers "F.Cu" "F.Mask" "F.Paste"))
)'''
        mod = TMP / "texto.kicad_mod"
        casos = [(dict(x=0, y=-3, giro=0), 0), (dict(x=-2, y=0, giro=0), 1), (dict(x=0, y=0, giro=0), 1),   # «REF**» mide ~4,2 mm
                 (dict(x=0, y=0, giro=90), 0), (dict(x=0, y=-1.2, giro=0, just=" (justify left)"), 0),
                 (dict(x=-2.6, y=-1.2, giro=0, just=" (justify left bottom)"), 0), (dict(x=-2.6, y=0, giro=0, just=" (justify left)"), 1),
                 (dict(x=-2, y=0, giro=0, oculto="(hide yes) "), 0)]
        for datos, esperado in casos:
            mod.write_text(base.format(**{"oculto": "", "just": "", **datos}), encoding="utf-8")
            r = huella.analizar(mod)
            self.assertEqual(r["serigrafia_sobre_pads"], esperado, datos)
            self.assertEqual(r["serigrafia_textos"], ["REF**"] * esperado, datos)

    def test_tipo_por_pads_y_atributo(self):
        def pads(*tipos):
            return [{"num": n, "tipo": t, "forma": "rect", "x": x, "y": 0.0, "giro": 0.0, "w": 2.0, "h": 2.0,
                     "capas": {"*.Cu"} if t != "smd" else {"F.Cu", "F.Paste"}, "props": list(props)}
                    for n, t, x, props in tipos]
        smd, tht = ("1", "smd", 0.0, ()), ("2", "thru_hole", 5.0, ())
        termica = ("1", "thru_hole", 0.5, ())                      # mismo número que el pad SMD y dentro de él
        disipador = ("3", "thru_hole", 9.0, ("pad_prop_heatsink",))
        npth = ("", "np_thru_hole", 7.0, ())
        self.assertEqual(huella.tipo_por_pads(pads(smd, termica, disipador)), "smd")
        self.assertEqual(huella.tipo_por_pads(pads(tht, npth)), "through_hole")
        self.assertEqual(huella.tipo_por_pads(pads(smd, tht)), "mixta")
        self.assertIsNone(huella.tipo_por_pads(pads(npth)))
        motivo = huella.atributo_incoherente
        self.assertIn("por sus pads, smd", motivo([], pads(smd)))
        self.assertIn("atributo through_hole; por sus pads, smd", motivo(["through_hole"], pads(smd)))
        self.assertIn("por sus pads, through_hole", motivo(["smd"], pads(tht)))
        self.assertIn("a la vez", motivo(["smd", "through_hole"], pads(smd)))
        self.assertIn("smd o through_hole", motivo([], pads(smd, tht)))
        for attr, ps in ((["smd"], pads(smd, tht)), (["through_hole"], pads(smd, tht)), (["smd"], pads(smd, termica)),
                         (["exclude_from_pos_files", "exclude_from_bom"], pads(smd)), ([], pads(npth))):
            self.assertIsNone(motivo(attr, ps), attr)


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
        self.assertEqual(len(puntos), 20)
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


def sustituir(ruta, a, b, n=1):
    texto = _comun.leer(ruta)
    assert a in texto, f"no está {a!r} en {Path(ruta).name}"
    _comun.escribir(ruta, texto.replace(a, b, n))


def bloque(texto, ref, clave="footprint"):
    """(i, j) de la huella (o del símbolo) con esa referencia."""
    i = texto.index(f'(property "Reference" "{ref}"')
    k = texto.rindex(f"({clave} ", 0, i)
    return k, _comun.fin_bloque(texto, k)


def poner_attr(texto, attr):
    """Huella (texto del bloque) con `(attr …)` sustituido o añadido tras su `(layer …)`."""
    i = texto.find("(attr ")
    if i >= 0:
        return texto[:i] + f"(attr {attr})" + texto[_comun.fin_bloque(texto, i):]
    j = texto.index(")", texto.index("(layer ")) + 1
    return texto[:j] + f" (attr {attr})" + texto[j:]


class Mutaciones(unittest.TestCase):
    """Cada punto de comprobar.py falla con al menos un defecto (mutaciones de VAL-0027-01, mutar.py)."""

    @classmethod
    def setUpClass(cls):
        cls.d = TMP / "mut"
        for sub in ("v2", "libraries", "componentes"):
            shutil.copytree(BASE / sub, cls.d / sub)
        cls.v2, cls.libs, cls.comp = cls.d / "v2", cls.d / "libraries", cls.d / "componentes"
        cls.pcb, cls.mcu = cls.v2 / "esp-riego.kicad_pcb", cls.v2 / "mcu.kicad_sch"
        cls.pretty = cls.libs / "esp-riego.pretty"

    def setUp(self):
        self.guardados = {}

    def tearDown(self):
        for ruta, texto in self.guardados.items():
            if texto is None:
                Path(ruta).unlink(missing_ok=True)
            else:
                _comun.escribir(ruta, texto)

    def guardar(self, *rutas):
        for r in rutas:
            self.guardados.setdefault(r, _comun.leer(r) if Path(r).exists() else None)

    def punto(self, clave):
        x = comprobar.resumen(self.v2, clave)["puntos"][0]
        return x["estado"], "\n".join(x["detalle"])

    def falla(self, clave, *textos):
        estado, detalle = self.punto(clave)
        self.assertEqual(estado, "FALLA", f"{clave}: {detalle}")
        for t in textos:
            self.assertIn(t, detalle, clave)
        return detalle

    def mod(self, nombre):
        return self.pretty / f"{nombre}.kicad_mod"

    def huella_pcb(self, ref, cambio):
        self.guardar(self.pcb)
        texto = _comun.leer(self.pcb)
        i, j = bloque(texto, ref)
        _comun.escribir(self.pcb, texto[:i] + cambio(texto[i:j]) + texto[j:])

    def test_esquema_vias_y_dnp(self):
        self.guardar(self.mcu)
        sustituir(self.mcu, '"Package_TO_SOT_SMD:SOT-23-6"', '"Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm_ThermalVias"', -1)
        self.falla("esquema.vias", "QFN-24-1EP", "0,2/0,5")
        texto = _comun.leer(self.mcu)
        i = texto.index('(property "Description" "', texto.index('(property "Reference" "R16"')) + len('(property "Description" "')
        texto = texto[:i] + "No montar. " + texto[i:]
        k = texto.rindex("(dnp no)", 0, texto.index('(property "Reference" "R17"'))
        _comun.escribir(self.mcu, texto[:k] + "(dnp yes)" + texto[k + len("(dnp no)"):])
        self.falla("esquema.dnp", "R16: el texto dice que no se monta", "R17: DNP sí en la hoja y no en la PCB")

    def test_layout_zonas(self):
        self.guardar(self.pcb)
        texto = _comun.leer(self.pcb).rstrip()
        zonas = ('\t(zone (net "GND") (layers "F.Cu" "B.Cu") (uuid "11111111-1111-1111-1111-111111111111")\n'
                 '\t\t(polygon (pts (xy 0 0) (xy 10 0) (xy 10 10) (xy 0 10)))\n'
                 '\t\t(filled_polygon (layer "F.Cu") (pts (xy 0 0) (xy 10 0) (xy 10 10)))\n\t)\n'
                 '\t(zone (net "+3V3") (layers "F&B.Cu") (uuid "22222222-2222-2222-2222-222222222222")\n'
                 '\t\t(polygon (pts (xy 0 0) (xy 10 0) (xy 10 10)))\n\t)\n')
        _comun.escribir(self.pcb, texto[:-1] + zonas + ")\n")
        detalle = self.falla("layout.zonas", "zona de GND en B.Cu: sin rellenar", "zona de +3V3 en F.Cu", "zona de +3V3 en B.Cu")
        self.assertNotIn("GND en F.Cu", detalle)
        rellena = zonas.split('\t(zone (net "+3V3")')[0].replace(
            "\t)\n", '\t\t(filled_polygon (layer "B.Cu") (pts (xy 0 0) (xy 1 0) (xy 1 1)))\n\t)\n')
        _comun.escribir(self.pcb, texto[:-1] + rellena + ")\n")
        self.assertEqual(self.punto("layout.zonas"), ("OK", "1 zonas rellenadas en todas sus capas"))

    def test_layout_salida(self):
        self.guardar(self.pcb)
        original = _comun.leer(self.pcb)
        self.assertIn('(outputdirectory "")', original)
        for carpeta, esperado in (("", "OK"), ("../../fabricacion/v2/", "OK"), ("../../fabricacion/", "FALLA"),
                                  ("../../gerber/", "FALLA"), ("C:/Users/otro/fabricacion/v2/", "FALLA"),
                                  ("../../../TFG/fabricacion/", "FALLA"), ("fabricacion/v2", "FALLA")):
            _comun.escribir(self.pcb, original.replace('(outputdirectory "")', f'(outputdirectory "{carpeta}")'))
            self.assertEqual(self.punto("layout.salida")[0], esperado, carpeta)

    def test_layout_smd_cara(self):
        self.guardar(self.pcb)
        original = _comun.leer(self.pcb)

        def abajo(t):
            return t.replace('(layer "F.Cu")', '(layer "B.Cu")', 1)

        def sin_attr(t):
            return t.replace("(attr smd)", "", 1)

        def pads_abajo(t):
            return t.replace('"F.Cu" "F.Mask" "F.Paste"', '"B.Cu" "B.Mask" "B.Paste"')

        for nombre, cambio in (("con attr", abajo), ("sin attr", lambda t: sin_attr(abajo(t))),
                               ("pads en B.Cu", lambda t: sin_attr(pads_abajo(t)))):
            _comun.escribir(self.pcb, original)
            self.huella_pcb("R16", cambio)
            self.falla("layout.smd_cara", "R16: pads SMD en la cara inferior")
        _comun.escribir(self.pcb, original)
        self.huella_pcb("R16", lambda t: poner_attr(abajo(t), "smd exclude_from_pos_files"))
        self.assertEqual(self.punto("layout.smd_cara")[0], "OK")     # fuera del CPL: punto de prueba, puente

    def test_layout_restricciones(self):
        tabla = self.v2 / "restricciones.csv"
        self.guardar(self.pcb, tabla)
        tabla.write_text("Red;Corriente;Ancho mín.;Separación;Vía\nGND;1 A;0,5;0,2;0,3/0,6\n", encoding="utf-8")
        self.assertEqual(self.punto("layout.restricciones")[0], "N/A")     # tabla, pero aún sin pistas
        texto = _comun.leer(self.pcb).rstrip()
        _comun.escribir(self.pcb, texto[:-1] + '\t(segment (start 0 0) (end 10 0) (width 0.3) (layer "F.Cu") (net "GND")'
                        ' (uuid "44444444-4444-4444-4444-444444444444"))\n\t(via (at 20 20) (size 0.5) (drill 0.2)'
                        ' (layers "F.Cu" "B.Cu") (net "GND") (uuid "55555555-5555-5555-5555-555555555555"))\n)\n')
        self.falla("layout.restricciones", "GND:", "vías por debajo de FAB-02")

    def test_layout_3d(self):
        def otro_modelo(t):
            i = t.index("(model ")
            return t[:i] + '(model "${KICAD10_3DMODEL_DIR}/Resistor_SMD.3dshapes/NoExiste.step"' + t[t.index("\n", i):]

        def sin_modelo(t):
            i = t.index("(model ")
            return t[:i] + t[_comun.fin_bloque(t, i):]

        self.huella_pcb("R16", otro_modelo)
        self.huella_pcb("R17", sin_modelo)
        self.falla("layout.3d", "R16: no existe", "NoExiste.step", "R17: sin modelo 3D")

    def test_librerias_formato_y_campos(self):
        tabla, sym, json_ = self.v2 / "fp-lib-table", self.libs / "esp-riego.kicad_sym", self.pretty / "vieja.json"
        self.guardar(tabla, sym, json_)
        json_.write_text("{}", encoding="utf-8")
        sustituir(tabla, '(type "KiCad")', '(type "Legacy")')
        self.falla("librerias.formato", "vieja.json: formato no nativo", "esp-riego es de tipo Legacy")
        texto = _comun.leer(sym)
        _comun.escribir(sym, re.sub(r'(\(property "MPN" )"[^"]*"', r'\1""', texto, count=1))
        self.falla("librerias.campos", "falta MPN")

    def test_librerias_patio(self):
        sw = self.mod("SW_Push_1P1T_XKB_TS-1187A")
        self.guardar(sw)
        original = _comun.leer(sw)
        _comun.escribir(sw, original.replace('(layer "F.CrtYd")', '(layer "F.Fab")'))
        self.falla("librerias.patio", "SW_Push_1P1T_XKB_TS-1187A: sin patio")
        justo = original
        for a, b in (("(start -3.75 ", "(start -3.3 "), ("(end -3.75 ", "(end -3.3 "), ("(start 3.75 ", "(start 3.3 "), ("(end 3.75 ", "(end 3.3 ")):
            justo = justo.replace(a, b)
        self.assertNotEqual(justo, original)
        _comun.escribir(sw, justo)
        self.falla("librerias.patio", "SW_Push_1P1T_XKB_TS-1187A: margen del patio")

    def test_librerias_serigrafia(self):
        btt, fusible = self.mod(BTT6050), self.mod("Fuse_Littelfuse-NANO2-451_453")
        self.guardar(btt, fusible)
        texto = _comun.leer(btt).rstrip()
        _comun.escribir(btt, texto[:-1] + '\t(fp_line (start -3.5 -3.81) (end -2 -3.81) (stroke (width 0.12) (type solid))'
                        ' (layer "F.SilkS") (uuid "33333333-3333-3333-3333-333333333333"))\n)\n')
        texto = _comun.leer(fusible)
        nuevo = re.sub(r'(\(property "Reference" "REF\*\*"\s*\(at )[-\d.]+ [-\d.]+', r"\g<1>-2.455 0", texto, count=1)
        self.assertNotEqual(nuevo, texto)
        _comun.escribir(fusible, nuevo)
        self.falla("librerias.serigrafia", f"{BTT6050}: 1 gráficos", "Fuse_Littelfuse-NANO2-451_453: 1 gráficos o textos",
                   "(textos: REF**)")

    def test_librerias_attr(self):
        sw, fusible, btt = self.mod("SW_Push_1P1T_XKB_TS-1187A"), self.mod("Fuse_Littelfuse-NANO2-451_453"), self.mod(BTT6050)
        borne = self.mod("TerminalBlock_Kangnex_WJ500V-5.08-2P_1x02_P5.08mm_Horizontal")
        self.guardar(sw, fusible, btt, borne, self.pcb)
        sustituir(sw, "(attr smd)", "")
        sustituir(fusible, "(attr smd)", "(attr through_hole)")
        self.falla("librerias.attr", "SW_Push_1P1T_XKB_TS-1187A: sin atributo smd/through_hole; por sus pads, smd",
                   "Fuse_Littelfuse-NANO2-451_453: atributo through_hole; por sus pads, smd")
        # con los atributos que pide SPEC-0025 (BTT6050 smd, WJ500V through_hole, también J1 en la PCB) queda limpio
        for ruta in (sw, fusible):
            _comun.escribir(ruta, self.guardados[ruta])
        _comun.escribir(btt, poner_attr(_comun.leer(btt), "smd"))
        _comun.escribir(borne, poner_attr(_comun.leer(borne), "through_hole"))
        self.huella_pcb("J1", lambda t: poner_attr(t, "through_hole"))
        estado, detalle = self.punto("librerias.attr")
        self.assertEqual(estado, "OK", detalle)

    def test_librerias_3d(self):
        btt, wrl = self.mod(BTT6050), self.libs / "3d" / "Infineon_PG-TDSO-14.wrl"
        self.guardar(btt, wrl)
        sustituir(btt, "Infineon_PG-TDSO-14.step", "Infineon_PG-TDSO-14.wrl")
        self.falla("librerias.3d", f"{BTT6050}: no existe")
        shutil.copyfile(self.libs / "3d" / "Infineon_PG-TDSO-14.step", wrl)
        self.falla("librerias.3d", "el modelo no es STEP (.wrl)")

    def test_librerias_gitattributes(self):
        d = TMP / "ga"
        (d / "v2").mkdir(parents=True)
        (d / "v2" / "p.kicad_pro").write_text("{}", encoding="utf-8")
        (d / "libraries" / "3d").mkdir(parents=True)
        for nombre in ("a.step", "b.STEP"):
            (d / "libraries" / "3d" / nombre).write_bytes(b"ISO-10303-21;")
        (d / ".gitattributes").write_text("*.step binary\n", encoding="utf-8")
        x = comprobar.resumen(d / "v2", "librerias.gitattributes")["puntos"][0]
        self.assertEqual(x["estado"], "FALLA", x)
        self.assertIn("*.STEP no está como binary", x["detalle"][0])
        (d / ".gitattributes").write_text("*.step binary\n*.STEP binary\n", encoding="utf-8")
        self.assertEqual(comprobar.resumen(d / "v2", "librerias.gitattributes")["puntos"][0]["estado"], "OK")

    def test_librerias_fichas(self):
        usb, led, esp, bloque_ = (self.comp / n for n in ("USBLC6-2SC6.md", "KT-0603R.md", "ESP32-S3-WROOM-1.md",
                                                          "bloque-alimentacion.md"))
        self.guardar(usb, led, esp, bloque_)
        antes = {l.split(" ")[0] for l in self.punto("librerias.fichas")[1].splitlines()}
        self.assertFalse({"C7519", "C2913198", "C25804"} & antes, antes)
        sustituir(usb, "tipo_jlcpcb: extended", "tipo_jlcpcb:")
        # C2913198 sale de su ficha y solo se cita en otra, como alternativa: no cuenta
        sustituir(esp, "lcsc: C2913198", "lcsc: C1")
        _comun.escribir(led, _comun.leer(led) + "\nAlternativa descartada: C2913198.\n")
        # C25804 (pasivo) está en la columna LCSC de la ficha de bloque; sin tipo en su fila, falla
        sustituir(bloque_, "| C25804 | Basic ·", "| C25804 | ·")
        lineas = {l.split(" ")[0]: l for l in self.falla("librerias.fichas").splitlines()}
        self.assertIn("a su ficha (USBLC6-2SC6.md) le falta tipo", lineas["C7519"])
        self.assertIn("sin ficha", lineas["C2913198"])
        self.assertIn("(bloque-alimentacion.md) le falta tipo", lineas["C25804"])
        # una alternativa entre paréntesis en el campo lcsc tampoco cuenta como ficha
        self.assertEqual(comprobar.codigos_lcsc("C44479 (alternativa TLC TA10, C2998199)"), ["C44479"])
        self.assertEqual(comprobar.codigos_lcsc("C1858395 (FADDAR) · C2879422 (ADDAR)"), ["C1858395", "C2879422"])


if __name__ == "__main__":
    unittest.main()
