"""Batería de regresión de herramientas/kicad.

Uso: python herramientas/pruebas/test_kicad.py [-v]

Localiza la raíz del repositorio buscando CLAUDE.md hacia arriba, copia `hardware/v2`,
`hardware/libraries` y `hardware/componentes` a una carpeta temporal y prueba cada herramienta
sobre esa copia: que su --help y su salida caben en 30 líneas, que no modifica lo que lee y que
da el resultado esperado. Cada punto de comprobar.py tiene al menos un caso que lo hace fallar
(clase Mutaciones). No usa la red (jlc.py se prueba con una respuesta guardada).
También prueba verificar.py (comprobar.py roto, zona sin rellenar) y lo compartido de _comun.
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
import colocacion  # noqa: E402
import comprobar  # noqa: E402
import dibujo  # noqa: E402
import _estilo  # noqa: E402
import hoja  # noqa: E402
import huella  # noqa: E402
import jlc  # noqa: E402
import restricciones  # noqa: E402

HERRAMIENTAS = ["jlc", "campos", "hoja", "sincronizar", "colocar", "colocacion", "vista", "huella", "restricciones", "comprobar",
                "dibujo"]
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
        plan = TMP / "plan_nm.md"
        plan.write_text("- `/I2C_SDA` = {U5-34, R24-2, U13-1, U18-15}\n", encoding="utf-8")
        v2, mod = BASE / "v2", BASE / "libraries" / "esp-riego.pretty" / f"{BTT6050}.kicad_mod"
        ordenes = [
            ("campos", "revisar", v2), ("comprobar", v2), ("comprobar", "--lista"), ("huella", mod), ("huella", mod, "--json"),
            ("hoja", "pines", "RF_Module:ESP32-S3-WROOM-1"), ("hoja", "extraer", v2 / "mcu.kicad_sch", "-o", TMP / "nm.json"),
            ("hoja", "netlist", v2, v2), ("hoja", "netlist", v2, v2, "--grupos"), ("hoja", "netlist", v2, "--plan", plan),
            ("hoja", "raiz", "--proyecto", v2, "--extraer", "-o", TMP / "nm_raiz.json"), ("restricciones", v2, tabla), ("vista", "hoja", v2, "--hoja", "MCU", "-o", TMP / "nm1.png"),
            ("vista", "placa", v2, "--todo", "-o", TMP / "nm2.png"), ("colocar", v2 / "esp-riego.kicad_pcb", "--exportar", TMP / "nm.csv"),
            ("colocacion", "extraer", v2, "-o", TMP / "nm_col.txt"), ("colocacion", "extraer", v2, "--refs", "U5"),
            ("colocacion", "evaluar", v2, "--detalle", TMP / "nm_col_ev.txt"),
            ("colocacion", "referencias", v2, "-o", TMP / "nm_col_refs.csv"),
            ("sincronizar", v2, "-o", TMP / "nm.kicad_pcb"), ("dibujo", "comprobar", TMP / "nm.json", v2 / "mcu.kicad_sch", "--proyecto", v2),
        ]
        antes = huella_md5(BASE)
        for orden in ordenes:
            codigo, salida, error = correr(*orden)
            self.assertIn(codigo, (0, 1), f"{orden[:2]}: {error}")
            self.assertLessEqual(len(salida.strip().splitlines()), 30, orden[:2])
            self.assertGreater(len(salida.strip()), 0, orden[:2])
        self.assertEqual(antes, huella_md5(BASE), "alguna herramienta ha tocado lo que lee")

    def test_lineas_de_checklist_del_readme(self):
        """Cada fila de «Puntos de checklist» del README cita una línea que existe en la versión actual de su checklist
        y lleva la marca `[auto: comprobar.py <punto>]` de esa fila (VAL-0035-01-04)."""
        readme = (KICAD / "README.md").read_text(encoding="utf-8")
        archivos = {"esquema": "esquema.md", "layout": "layout.md", "librerías": "librerias.md"}
        filas = re.findall(r"^\| (esquema|layout|librerías) \| (\d+)[^|]*\|[^|]*\| `([a-z0-9_.]+)`", readme, re.M)
        self.assertEqual(len(filas), len(comprobar.PUNTOS))
        for lista, linea, punto in filas:
            lineas = (REPO / "gestion" / "checklists" / archivos[lista]).read_text(encoding="utf-8").splitlines()
            donde = [k + 1 for k, l in enumerate(lineas) if f"[auto: comprobar.py {punto}]" in l]
            self.assertIn(int(linea), donde, f"README: {lista} l. {linea} ({punto}); la marca está en {donde}")

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

    def test_resultados_y_buscar(self):
        """--buscar (VAL-0006-01-07): todas las piezas de la respuesta, de más a menos stock, sin red."""
        respuesta = json.loads(json.dumps(self.RESPUESTA))
        respuesta["data"]["componentPageInfo"]["list"].reverse()      # la de menos stock primero (VAL-0028-01-01)
        respuesta["data"]["componentPageInfo"]["list"].insert(0, {"componentModelEn": "sin código", "stockCount": 10 ** 9})
        filas = jlc.resultados(respuesta, cantidad=5000)
        self.assertEqual([f["codigo"] for f in filas], ["C25804", "C534868"])
        self.assertEqual((filas[0]["tipo"], filas[0]["precio"]), ("Basic", 0.0011))
        self.assertEqual((filas[1]["tipo"], filas[1]["stock"], filas[1]["precio"]), ("Extended", 1628, None))
        self.assertEqual(jlc.resultados({"data": None}), [])
        original = jlc.pedir
        try:
            jlc.pedir = lambda palabra, intentos=2: respuesta if palabra == "BTT" else (_ for _ in ()).throw(OSError("sin red"))
            lineas = jlc.buscar(["BTT", "otra"], 1, "2026-01-01")
        finally:
            jlc.pedir = original
        self.assertEqual(lineas[0], "JLCPCB · 2026-01-01 · búsqueda · precio en USD para 1 ud.")
        self.assertEqual(lineas[1], "«BTT»: 2 resultados")
        self.assertTrue(lineas[2].lstrip().startswith("C25804") and "0.0022" in lineas[2], lineas[2])
        self.assertIn("BTT6050-1ERA · Infineon", lineas[3])
        self.assertEqual(lineas[4], "«otra»: OSError: sin red")


class Comun(unittest.TestCase):
    def test_modelo_de_respaldo(self):
        """VAL-0029-01-01 (a): modelo oficial que falta → el de libraries/3d con el mismo nombre; si no, None."""
        libs3d = TMP / "respaldo3d"
        libs3d.mkdir(exist_ok=True)
        (libs3d / "Falta.step").write_text("ISO-10303-21;", encoding="utf-8")
        f = _comun.modelo_de_respaldo
        self.assertEqual(f("${KICAD10_3DMODEL_DIR}/NoHay.3dshapes/Falta.step", libs3d), "${KIPRJMOD}/../libraries/3d/Falta.step")
        self.assertEqual(f("${KICAD9_3DMODEL_DIR}/NoHay.3dshapes/Falta.step", libs3d), "${KIPRJMOD}/../libraries/3d/Falta.step")
        existe = "${KICAD10_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0603_1608Metric.step"
        self.assertTrue((_comun.MODELOS / "Resistor_SMD.3dshapes" / "R_0603_1608Metric.step").is_file())
        (libs3d / "R_0603_1608Metric.step").write_text("ISO-10303-21;", encoding="utf-8")  # VAL-0028-01-02: hay respaldo
        self.assertIsNone(f(existe, libs3d))                                              # el oficial existe y manda
        self.assertIsNone(f("${KICAD10_3DMODEL_DIR}/NoHay.3dshapes/Otro.step", libs3d))  # sin respaldo
        self.assertIsNone(f("${KICAD10_3DMODEL_DIR}/NoHay.3dshapes/Falta.step", None))
        self.assertIsNone(f("${OTRA_VARIABLE}/Falta.step", libs3d))                      # variable que no se resuelve


class Verificar(unittest.TestCase):
    """verificar.py (VAL-0027-02-02): un comprobar.py roto no lo tumba, y el DRC rellena las zonas sin tocar la PCB."""

    def test_comprobar_roto(self):
        d = TMP / "verif_roto"
        (d / "herramientas" / "kicad").mkdir(parents=True)
        (d / "p").mkdir()
        shutil.copyfile(REPO / "herramientas" / "verificar.py", d / "herramientas" / "verificar.py")
        (d / "p" / "mini.kicad_sch").write_text(
            '(kicad_sch (version 20260306) (generator "eeschema") (generator_version "10.0") '
            '(uuid "0b6e2a4e-0000-4000-8000-000000000001") (paper "A4") (lib_symbols) (sheet_instances (path "/" (page "1"))))\n',
            encoding="utf-8")
        (d / "p" / "mini.kicad_pro").write_text("{}", encoding="utf-8")
        for nombre, cuerpo, texto in (("excepción", 'def para_verificar(c):\n    raise RuntimeError("roto a propósito")\n', "roto a propósito"),
                                      ("sintaxis", "def para_verificar(c)\n    return {}\n", "comprobar.py, line 1"),
                                      ("sin la función", "X = 1\n", "para_verificar")):
            (d / "herramientas" / "kicad" / "comprobar.py").write_text(cuerpo, encoding="utf-8")
            antes = huella_md5(d / "p")
            r = subprocess.run([sys.executable, str(d / "herramientas" / "verificar.py"), str(d / "p")], capture_output=True,
                               text=True, encoding="utf-8", errors="replace")
            self.assertEqual(r.returncode, 0, f"{nombre}: {r.stdout}{r.stderr}")
            self.assertIn("Puntos [auto]: no disponibles", r.stdout, nombre)
            self.assertIn(texto, r.stdout, nombre)
            self.assertIn("Resultado: LIMPIO", r.stdout, nombre)
            self.assertEqual(antes, huella_md5(d / "p"), nombre)
            r = subprocess.run([sys.executable, str(d / "herramientas" / "verificar.py"), str(d / "p"), "--json"],
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
            resumen = json.loads(r.stdout)
            self.assertEqual((resumen["auto"]["fallan"], resumen["limpio"]), (0, True), nombre)

    def test_zona_sin_rellenar(self):
        proy = copia("v2_zona")
        pcb = proy / "esp-riego.kicad_pcb"
        texto = _comun.leer(pcb).rstrip()
        self.assertIn("(start 100 60)", texto)                  # contorno 100 × 70 mm desde (100, 60)
        zona = ('\t(zone (net "GND") (layer "F.Cu") (uuid "66666666-6666-6666-6666-666666666666")\n'
                '\t\t(connect_pads (clearance 0.2))\n\t\t(min_thickness 0.2)\n\t\t(fill (thermal_gap 0.3) (thermal_bridge_width 0.3))\n'
                '\t\t(polygon (pts (xy 100.5 60.5) (xy 199.5 60.5) (xy 199.5 129.5) (xy 100.5 129.5)))\n\t)\n')
        _comun.escribir(pcb, texto[:-1] + zona + ")\n")
        self.assertNotIn("filled_polygon", _comun.leer(pcb))
        antes = huella_md5(proy)
        r = verificar(proy)
        self.assertEqual(antes, huella_md5(proy), "verificar.py ha guardado la PCB rellenada")
        # sin --refill-zones la zona vacía no da nada; rellenada en memoria, deja islas (isolated_copper)
        self.assertGreater(r["drc"]["por_tipo"].get("isolated_copper [warning]", 0), 0, r["drc"])
        self.assertEqual(r["drc"]["errores"], 0, r["drc"])
        self.assertEqual(r["paridad"]["total"], 0, r["paridad"])


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

    def test_no_sustituye_lo_que_no_representa(self):
        """Una hoja con un elemento que hoja.py no sabe dibujar (polilínea): extraer no escribe y generar no la sustituye."""
        ali = TMP / "ali_poly.kicad_sch"
        texto = _comun.leer(BASE / "v2" / "alimentacion.kicad_sch").rstrip()
        _comun.escribir(ali, texto[:-1] + '\t(polyline (pts (xy 0 0) (xy 10 0)) (stroke (width 0) (type default)) (uuid "p1"))\n)\n')
        codigo, salida, _ = correr("hoja", "extraer", ali, "-o", TMP / "ali.json")
        self.assertEqual(codigo, 1)
        self.assertIn("polyline", salida)
        self.assertFalse((TMP / "ali.json").exists())
        desc = TMP / "vacia.json"
        desc.write_text('{"piezas": []}', encoding="utf-8")
        codigo, _, error = correr("hoja", "generar", desc, "--proyecto", BASE / "v2", "--como", "alimentacion.kicad_sch",
                                  "--base", ali, "-o", TMP / "ali.kicad_sch")
        self.assertEqual(codigo, 2)
        self.assertIn("--forzar", error)

    def test_regenera_alimentacion_con_cables(self):
        """extraer + generar reproduce una hoja con cables y etiquetas fuera de los pines (Alimentación)."""
        proy = copia("v2_ali")
        desc = TMP / "ali_cables.json"
        codigo, salida, error = correr("hoja", "extraer", BASE / "v2" / "alimentacion.kicad_sch", "-o", desc)
        self.assertEqual(codigo, 0, salida + error)
        d = json.loads(desc.read_text(encoding="utf-8"))
        self.assertEqual((len(d["cables"]), len(d["recuadros"])), (188, 7))         # redibujada en SPEC-0035
        self.assertIn({"x": 27.94, "y": 45.72, "con": "L:VIN_RAW", "lado": "R"}, d["etiquetas"])
        codigo, salida, error = correr("hoja", "generar", desc, "--proyecto", proy, "-o", proy / "alimentacion.kicad_sch")
        self.assertEqual(codigo, 0, salida + error)
        self.assertIn("55 piezas (55 con su UUID)", salida)
        codigo, salida, error = correr("hoja", "netlist", BASE / "v2", proy)
        self.assertEqual(codigo, 0, salida + error)
        self.assertIn(": 0 diferencias", salida)

    def test_tramos_y_uniones(self):
        """Los cables se parten donde llega otro extremo o un pin; unión con 3 o más extremos; un cruce no une."""
        tramos, uniones, grado = hoja.tramos_y_uniones(
            [[[0, 0], [10, 0]], [[5, 0], [5, 5]], [[0, 10], [10, 10]], [[5, 8], [5, 12]], [[20, 0], [30, 0]]],
            pines=[(10, 0), (25, 0)])
        self.assertEqual(uniones, [(5.0, 0.0), (25.0, 0.0)])          # T y pin en mitad de un cable
        self.assertIn(((0.0, 0.0), (5.0, 0.0)), tramos)
        self.assertIn(((20.0, 0.0), (25.0, 0.0)), tramos)
        self.assertEqual(grado[(10.0, 0.0)], 2)                         # cable que acaba en un pin: sin unión
        self.assertNotIn((5.0, 10.0), grado)                            # cruce sin extremos: no se une
        self.assertTrue(hoja.toca((7, 0), tramos))
        self.assertFalse(hoja.toca((7, 1), tramos))

    def test_comparar_grupos(self):
        """netlist --grupos: una red renombrada no es una diferencia; una red partida sí."""
        c = {"value": "1k", "footprint": "F", "campos": {}, "nombres": "/"}
        a = {"comps": {"R1": c, "R2": c}, "redes": {"/X": {("R1", "1"), ("R2", "1")}, "GND": {("R1", "2"), ("R2", "2")}}}
        b = {"comps": {"R1": c, "R2": c}, "redes": {"/Y": {("R1", "1"), ("R2", "1")}, "GND": {("R1", "2"), ("R2", "2")}}}
        self.assertEqual(_comun.comparar_grupos(a, b), [])
        self.assertNotEqual(_comun.comparar_netlists(a, b), [])
        partida = {"comps": a["comps"], "redes": {"/X": {("R1", "1"), ("R2", "1")}, "GND": {("R1", "2")}, "N": {("R2", "2")}}}
        dif = _comun.comparar_grupos(a, partida)
        self.assertTrue(any("GND" in d and "repartida" in d for d in dif), dif)

    def test_dibujo(self):
        """dibujo.py: puntas de pin, cables pin a pin, conectividad frente a la hoja original y avisos; con la hoja
        generada, el cable del cátodo de un LED no cruza el símbolo (primitivas) y uno entre las placas de un
        condensador sí (núcleo entre los pines)."""
        proy = copia("v2_dibujo")
        d = dibujo.Dibujo(BASE / "v2" / "mcu.kicad_sch", proyecto=BASE / "v2")
        d.pieza("R23", 50.8, 50.8, 90)
        d.pieza("D5", 63.5, 54.61, 90)
        d.pieza("C23", 88.9, 55.88, pines={"1": "L:EN", "2": "P:GND"})
        self.assertEqual((d.p("R23.1"), d.p("D5.2"), d.p("D5.1")), ((46.99, 50.8), (63.5, 50.8), (63.5, 58.42)))
        d.lab("L:LED_STATUS", (38.1, 50.8), "L")
        d.w((38.1, 50.8), "R23.1")
        d.hv("R23.2", "D5.2")
        d.w("D5.1", (63.5, 62.23))
        d.pwr("GND", (63.5, 62.23))
        d.box(25.4, 35.56, 81.28, 38.1, "LED de prueba: D5, R23, C23")
        desc = TMP / "dibujo.json"
        self.assertEqual(d.guardar(desc, todas=False), [])
        with self.assertRaises(_comun.Fallo):
            d.guardar(TMP / "dibujo_todas.json")                      # faltan piezas de la original
        codigo, salida, error = correr("dibujo", "comprobar", desc, BASE / "v2" / "mcu.kicad_sch", "--proyecto", BASE / "v2")
        self.assertEqual(codigo, 0, salida + error)
        self.assertIn("0 diferencias, 0 avisos", salida)
        # R23 al revés y el cátodo sin cable: diferencias y aviso
        original = dibujo.cargar(BASE / "v2" / "mcu.kicad_sch")
        mal = json.loads(desc.read_text(encoding="utf-8"))
        mal["piezas"][0]["giro"] = 270
        mal["cables"] = [c for c in mal["cables"] if [63.5, 62.23] not in c]
        dif, avisos, _ = dibujo.comparar(original, mal, d.pines)
        self.assertTrue(any(x.startswith("R23.1: con") for x in dif), dif)
        self.assertIn("D5.1: «W» sin cable en (63.5, 58.42)", avisos)
        # estilo de la hoja generada
        hoja_led = TMP / "dibujo.kicad_sch"
        codigo, salida, error = correr("hoja", "generar", desc, "--proyecto", proy, "--como", "mcu.kicad_sch", "-o", hoja_led)
        self.assertEqual(codigo, 0, salida + error)
        self.assertEqual(_estilo.cruces(_estilo.analizar(hoja_led)), [])
        texto = _comun.leer(hoja_led).rstrip()
        _comun.escribir(hoja_led, texto[:-1] + '\t(wire (pts (xy 85.09 55.88) (xy 92.71 55.88)) (stroke (width 0) (type default)) (uuid "w1"))\n'
                        '\t(wire (pts (xy 60.96 54.61) (xy 66.04 54.61)) (stroke (width 0) (type default)) (uuid "w2"))\n)\n')
        malas = _estilo.cruces(_estilo.analizar(hoja_led))
        self.assertIn("cable (85.09, 55.88)–(92.71, 55.88) cruza C23", malas)
        self.assertIn("cable (60.96, 54.61)–(66.04, 54.61) cruza D5", malas)

    def test_campos_subhoja(self):
        """La subhoja «Canal» (6 instancias) usa la tabla de Salidas: sin diferencias, y una de más se detecta."""
        archivos = campos.archivos_de([BASE / "v2"])
        tablas = campos.tablas_por_defecto(archivos)
        self.assertIs(tablas["canal.kicad_sch"], tablas["salidas.kicad_sch"])
        r = campos.revisar(archivos, tablas)
        self.assertEqual((r["piezas"], r["tabla"]), (197, []))
        tablas["salidas.kicad_sch"]["U99"] = {"Value": "X"}
        r = campos.revisar(archivos, tablas)
        self.assertEqual(r["tabla"], ["canal.kicad_sch, salidas.kicad_sch: en la tabla y no en la hoja: U99"])

    def test_cables_recuadros_y_subhojas(self):
        """Cables con uniones automáticas, recuadro con título y una subhoja repetida (dos instancias, refs propias)."""
        proy = copia("v2_cables")
        d, perdidos = hoja.extraer(BASE / "v2" / "sensores.kicad_sch")     # la hoja piloto (SPEC-0035)
        self.assertEqual(perdidos, [])
        self.assertEqual(d["piezas"][0]["pines"] if d["piezas"][0]["ref"] == "U13" else d["piezas"][1]["pines"],
                         {"1": "W", "2": "W", "3": "W", "4": "W"})
        self.assertEqual(len(d["recuadros"]), 1)
        d["hojas"] = [{"nombre": n, "archivo": "prueba_canal.kicad_sch", "x": 198.12, "y": y, "ancho": 25.4, "alto": 12.7,
                       "pines": [{"nombre": "ENT", "forma": "input", "lado": "L", "y": y + 5.08}]}
                      for n, y in (("CanalA", 76.2), ("CanalB", 96.52))]
        d["cables"] += [[[167.64, 88.9], [180.34, 88.9], [180.34, 81.28], [198.12, 81.28]],
                        [[180.34, 88.9], [180.34, 101.6], [198.12, 101.6]]]
        archivo = TMP / "cables.json"
        archivo.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        codigo, salida, error = correr("hoja", "generar", archivo, "--proyecto", proy, "-o", proy / "sensores.kicad_sch")
        self.assertEqual(codigo, 0, salida + error)
        self.assertIn("3 uniones, 1 recuadros, 2 subhojas", salida)
        canal = {"papel": "A4", "piezas": [{"refs": {"Sensores/CanalA": "R901", "Sensores/CanalB": "R902"}, "simbolo": "Device:R",
                                            "x": 101.6, "y": 101.6, "giro": 0,
                                            "campos": {"Value": "1k", "Footprint": "Resistor_SMD:R_0603_1608Metric", "MPN": "X",
                                                       "Fabricante": "X", "Datasheet": "http://x", "Description": "x",
                                                       "LCSC Part#": "C21190"},
                                            "pines": {"1": "H:ENT:input", "2": "P:GND"}}]}
        (TMP / "canal.json").write_text(json.dumps(canal), encoding="utf-8")
        codigo, salida, error = correr("hoja", "generar", TMP / "canal.json", "--proyecto", proy, "-o", proy / "prueba_canal.kicad_sch")
        self.assertEqual(codigo, 0, salida + error)
        self.assertIn("2 instancias de la hoja", salida)
        red = _comun.exportar_netlist(proy, "esp-riego", TMP / "cables.net")
        self.assertEqual(red["comps"]["R901"]["nombres"], "/Sensores/CanalA/")
        self.assertEqual(red["comps"]["R902"]["nombres"], "/Sensores/CanalB/")
        self.assertTrue({("U13", "3"), ("C47", "1"), ("R901", "1"), ("R902", "1")} <= red["redes"]["+3V3"])
        r = verificar(proy)
        self.assertEqual(r["erc"]["errores"], 0, r["erc"])
        puntos = {x["punto"]: x for x in comprobar.resumen(proy)["puntos"]}
        self.assertIn("199 piezas", puntos["esquema.campos"]["detalle"][0])          # una pieza por instancia
        self.assertEqual(puntos["esquema.cruces"]["estado"], "OK", puntos["esquema.cruces"])
        self.assertIn("prueba_canal.kicad_sch: R901 fuera de un recuadro", puntos["esquema.recuadros"]["detalle"])
        # extraer conserva las refs de cada instancia y las subhojas; generar desde ahí da la misma netlist
        otra, _ = hoja.extraer(proy / "prueba_canal.kicad_sch")
        self.assertEqual(otra["piezas"][0]["refs"], {"Sensores/CanalA": "R901", "Sensores/CanalB": "R902"})
        sens, _ = hoja.extraer(proy / "sensores.kicad_sch")
        self.assertEqual([h["nombre"] for h in sens["hojas"]], ["CanalA", "CanalB"])
        # errores: pin «W» sin cable y pieza de una hoja repetida sin las refs de cada instancia
        d["cables"] = [c for c in d["cables"] if [142.24, 93.98] not in c]      # sin cable en U13.3 (VDD)
        archivo.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        codigo, _, error = correr("hoja", "generar", archivo, "--proyecto", proy, "-o", TMP / "no.kicad_sch", "--como", "sensores.kicad_sch")
        self.assertEqual(codigo, 2)
        self.assertIn("sin cable", error)
        canal["piezas"][0]["refs"].pop("Sensores/CanalB")
        (TMP / "canal.json").write_text(json.dumps(canal), encoding="utf-8")
        codigo, _, error = correr("hoja", "generar", TMP / "canal.json", "--proyecto", proy, "-o", TMP / "no.kicad_sch", "--como", "prueba_canal.kicad_sch")
        self.assertEqual(codigo, 2)
        self.assertIn("faltan las referencias de Sensores/CanalB", error)
        self.assertFalse((TMP / "no.kicad_sch").exists())

    def test_paginas_en_orden_del_arbol(self):
        """`hoja.py paginas`: cada hoja seguida de sus subhojas (VAL-0035-01-03); sin -o solo comprueba."""
        proy = copia("v2_paginas")
        codigo, salida, error = correr("hoja", "paginas", proy)
        self.assertEqual(codigo, 0, salida + error)                     # el proyecto actual ya está en orden
        raiz, salidas = proy / "esp-riego.kicad_sch", proy / "salidas.kicad_sch"
        texto = _comun.leer(raiz)
        i = texto.index('(property "Sheetname" "MCU"')
        k = texto.index('(page "', i)
        _comun.escribir(raiz, texto[:k] + '(page "3")' + texto[texto.index(")", k) + 1:])   # MCU detrás de Salidas
        texto = _comun.leer(salidas)
        for n in range(1, 7):
            i = texto.index(f'(property "Sheetname" "Canal{n}"')
            k = texto.index('(page "', i)
            texto = texto[:k] + f'(page "{n + 6}")' + texto[texto.index(")", k) + 1:]    # instancias al final
        _comun.escribir(salidas, texto)
        antes = huella_md5(proy)
        codigo, salida, _ = correr("hoja", "paginas", proy)
        self.assertEqual(codigo, 1)
        self.assertIn("/MCU/: 3 → 9", salida)
        self.assertIn("/Salidas/Canal1/: 7 → 3", salida)
        self.assertEqual(antes, huella_md5(proy), "sin -o no escribe")
        codigo, salida, error = correr("hoja", "paginas", proy, "-o", proy)
        self.assertEqual(codigo, 0, salida + error)
        self.assertIn("en 2 archivos", salida)
        self.assertEqual(correr("hoja", "paginas", proy)[0], 0)
        paginas = lambda ruta: re.findall(r'"Sheetname" "(\w+)".*?\(page "(\d+)"\)', _comun.leer(ruta), re.S)  # noqa: E731
        self.assertEqual(paginas(salidas), [(f"Canal{n}", str(n + 2)) for n in range(1, 7)])
        self.assertEqual(paginas(raiz), [("Salidas", "2"), ("MCU", "9"), ("Alimentacion", "10"), ("Conectores", "11"),
                                         ("Sensores", "12")])
        r = verificar(proy)
        self.assertEqual(r["erc"]["total"], 0, r["erc"])
        self.assertEqual(r["paridad"]["total"], 0, r["paridad"])

    def test_tinta_frente_al_svg(self):
        """La caja de cada texto de `_estilo` es la tinta que dibuja KiCad (SVG de kicad-cli), a ±0,03 mm:
        mayúsculas, minúsculas con descendente, cifras, varias líneas, justificaciones y etiquetas giradas."""
        casos = [("text", "TLV1117LV33DCYR", 0, "left bottom"), ("text", "TPS26632RGER", 0, "right bottom"),
                 ("text", "Ag 4.7u 100V", 0, ""), ("text", "ABC\\nDEF\\nGHI", 0, "left top"),
                 ("text", "≤3 mm de U5-2", 0, "left"), ("label", "LED_STATUS", 0, "left bottom"),
                 ("label", "VIN_PROT", 180, "right bottom"), ("label", "I2C_SDA", 90, "left bottom"),
                 ("label", "BTN_INT", 270, "right bottom")]
        cuerpo = ""
        for k, (tipo, t, ang, j) in enumerate(casos):
            jj = f" (justify {j})" if j else ""
            extra = " (exclude_from_sim no)" if tipo == "text" else ""
            cuerpo += (f'\t({tipo} "{t}"{extra} (at 50 {30 + 25 * k} {ang}) (effects (font (size 1.27 1.27)){jj}) '
                       f'(uuid "00000000-0000-4000-8000-{k:012d}"))\n')
        d = TMP / "tinta"
        d.mkdir()
        sch = d / "tinta.kicad_sch"
        _comun.escribir(sch, '(kicad_sch (version 20260306) (generator "eeschema") (generator_version "10.0") '
                             '(uuid "00000000-0000-4000-8000-0000000000ff") (paper "User" 150 280)\n' + cuerpo + ")\n")
        _comun.cli("sch", "export", "svg", "--exclude-drawing-sheet", "-o", d, sch, comprobar=d / "tinta.svg")
        svg = (d / "tinta.svg").read_text(encoding="utf-8")
        import html
        puntos = {}
        for desc, trazos in re.findall(r'<g class="stroked-text"><desc>(.*?)</desc>(.*?)</g>', svg, re.S):
            puntos.setdefault(html.unescape(desc).strip(), []).extend(
                (float(a), float(b)) for a, b in re.findall(r"[ML]([\d.]+) ([\d.]+)", trazos))
        h = _estilo.analizar(sch)
        self.assertEqual(len(h["textos"]), len(casos))
        medio = _estilo.TRAZO / 2
        for t in h["textos"]:
            pts = puntos.get(t["texto"].strip()) or [p for linea in t["texto"].split("\n") for p in puntos[linea]]
            tinta = (min(p[0] for p in pts) - medio, min(p[1] for p in pts) - medio,
                     max(p[0] for p in pts) + medio, max(p[1] for p in pts) + medio)
            for a, b in zip(t["caja"], tinta):
                self.assertAlmostEqual(a, b, delta=0.03, msg=f"{t['texto']!r}: caja {t['caja']} frente a tinta {tinta}")

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
                     "pines": {"1": "P:GND:270", "2": "NC"}},
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
        # el símbolo de alimentación girado (P:GND:270) sale girado y con el Value horizontal a su izquierda
        gnd = next(s for s in _comun.simbolos_hoja(_comun.leer(proy / "salidas.kicad_sch"))
                   if s["lib_id"] == "power:GND" and s["giro"] == 270)
        valor = next(p for p in _comun.hijos(gnd["nodo"], "property") if p[1] == "Value")
        self.assertEqual([float(v) for v in _comun.uno(valor, "at")[1:]], [gnd["x"] - 3.81, gnd["y"], 90.0])
        self.assertEqual(_comun.uno(_comun.uno(valor, "effects"), "justify")[1:], ["right"])
        # falta declarar un pin: error claro y no se escribe
        desc["piezas"][0]["pines"].pop("2")
        archivo.write_text(json.dumps(desc, ensure_ascii=False), encoding="utf-8")
        codigo, _, error = correr("hoja", "generar", archivo, "--proyecto", proy, "-o", TMP / "no.kicad_sch", "--como", "salidas.kicad_sch")
        self.assertEqual(codigo, 2)
        self.assertIn("R901: pines sin conexión declarada: 2", error)
        self.assertFalse((TMP / "no.kicad_sch").exists())

    def test_raiz(self):
        """hoja.py generar escribe la raíz (SPEC-0032) y hoja.py raiz pone etiquetas en sus pines de hoja: extraer + escribir
        la reproduce; un pin cambiado cambia la netlist; errores claros. La raíz del proyecto va con cables (DEC-0015): la
        prueba la regenera sin cables ni etiquetas y le pone en cada pin una etiqueta con su nombre."""
        proy = copia("v2_raiz")
        raiz, desc, gen = proy / "esp-riego.kicad_sch", TMP / "raiz.json", TMP / "raiz_generar.json"
        codigo, salida, error = correr("hoja", "extraer", raiz, "-o", gen)
        self.assertEqual(codigo, 0, salida + error)
        g = json.loads(gen.read_text(encoding="utf-8"))
        self.assertEqual(len(g["hojas"]), 5)
        g.update(cables=[], etiquetas=[], uniones=[])
        gen.write_text(json.dumps(g), encoding="utf-8")
        codigo, salida, error = correr("hoja", "generar", gen, "--proyecto", proy, "-o", raiz)
        self.assertEqual(codigo, 0, salida + error)
        self.assertIn("0 tramos de cable", salida)
        self.assertIn('(sheet_instances\n\t\t(path "/"\n\t\t\t(page "1")', _comun.leer(raiz).replace("\r\n", "\n"))
        cab = lambda ruta: _comun.val(_comun.parse_cabecera(_comun.leer(ruta)), "uuid")  # noqa: E731
        pines = lambda ruta: {(n, p["nombre"]): p["uuid"] for n, h in hoja._hojas_raiz(_comun.leer(ruta)).items()  # noqa: E731
                              for p in h["pines"]}
        self.assertEqual(cab(raiz), cab(BASE / "v2" / "esp-riego.kicad_sch"))             # conserva los UUID de la raíz
        self.assertEqual(pines(raiz), pines(BASE / "v2" / "esp-riego.kicad_sch"))         # y de los pines de hoja
        self.assertEqual(correr("hoja", "paginas", proy)[0], 0)                           # y las páginas
        codigo, salida, error = correr("hoja", "raiz", "--proyecto", proy, "--extraer", "-o", desc)
        self.assertEqual(codigo, 0, salida + error)
        d = json.loads(desc.read_text(encoding="utf-8"))
        self.assertEqual({p["conexion"] for h in d["hojas"] for p in h["pines"]}, {""})
        for h in d["hojas"]:
            for p in h["pines"]:
                p["conexion"] = "L:" + p["nombre"]
        desc.write_text(json.dumps(d), encoding="utf-8")
        sensores = next(h for h in d["hojas"] if h["nombre"] == "Sensores")
        self.assertIn({"nombre": "I2C_SCL", "forma": "input", "lado": "R", "y": 93.98, "conexion": "L:I2C_SCL"}, sensores["pines"])
        _comun.escribir(raiz, _comun.leer(raiz).replace('(pin "I2C_SCL" input', '(pin "I2C_SCL" output', 1))  # la descripción manda
        codigo, salida, error = correr("hoja", "raiz", desc, "--proyecto", proy, "-o", raiz)
        self.assertEqual(codigo, 0, salida + error)
        self.assertIn("5 hojas, 54 pines de hoja, 54 etiquetas o NC · avisos 0", salida)
        self.assertEqual(hoja.extraer_raiz(raiz), d)
        self.assertEqual(pines(raiz), pines(BASE / "v2" / "esp-riego.kicad_sch"))
        codigo, salida, error = correr("hoja", "netlist", BASE / "v2", proy)              # mismas redes, con sus nombres
        self.assertEqual(codigo, 0, salida + error)
        # SCL de Sensores a NC y un pin nuevo en Conectores, sin etiqueta jerárquica en su hoja: se escribe y avisa
        for p in sensores["pines"]:
            if p["nombre"] == "I2C_SCL":
                p["conexion"] = "NC"
        conectores = next(h for h in d["hojas"] if h["nombre"] == "Conectores")
        conectores["pines"].append({"nombre": "NUEVO", "forma": "input", "lado": "L", "y": 78.74, "conexion": "L:NUEVO"})
        desc.write_text(json.dumps(d), encoding="utf-8")
        codigo, salida, error = correr("hoja", "raiz", desc, "--proyecto", proy, "-o", raiz)
        self.assertEqual(codigo, 1, salida + error)
        self.assertIn("Conectores.NUEVO: conectores.kicad_sch no tiene esa etiqueta jerárquica", salida)
        texto = _comun.leer(raiz)
        self.assertIn("(no_connect\n\t\t(at 55.88 93.98)", texto.replace("\r\n", "\n"))
        self.assertIn('(pin "NUEVO" input\n\t\t\t(at 30.48 78.74 180)', texto.replace("\r\n", "\n"))
        red = _comun.exportar_netlist(proy, "esp-riego", TMP / "raiz.net")
        self.assertNotIn(("U13", "2"), red["redes"]["/I2C_SCL"])
        self.assertIn(("U13", "2"), red["redes"]["/Sensores/I2C_SCL"])
        # errores: hoja que no existe, pin fuera del borde, lado no soportado
        for cambio, mensaje in ((lambda x: x["hojas"][0].update(nombre="NoHay"), "no tiene ninguna hoja «NoHay»"),
                                (lambda x: x["hojas"][0]["pines"][0].update(y=500), "fuera del borde"),
                                (lambda x: x["hojas"][0]["pines"][0].update(lado="U"), "(L o R)")):
            otra = json.loads(json.dumps(d))
            cambio(otra)
            desc.write_text(json.dumps(otra), encoding="utf-8")
            codigo, _, error = correr("hoja", "raiz", desc, "--proyecto", proy, "-o", TMP / "raiz_no.kicad_sch")
            self.assertEqual(codigo, 2, error)
            self.assertIn(mensaje, error)
            self.assertFalse((TMP / "raiz_no.kicad_sch").exists())

    def test_netlist_plan(self):
        """hoja.py netlist --plan: cada red del plan, con exactamente esos pines; NC; sección; entradas sin interpretar."""
        doc = TMP / "plan.md"
        doc.write_text("# Doc\n\n## Anexo A. Plan\n\n| Red | Pines |\n|---|---|\n| `/I2C_SDA` = {U5-34, R24-2, U13-1, U18-15} | |\n"
                       "- Internas: ILIM_5V {U14-5, R69-1}; NC {U18-11, U18-12}; BTN1…BTN6 {SWn-1, U18 P0…P5}.\n\n"
                       "## Otra\n\n- X = {U5-34}\n", encoding="utf-8")
        codigo, salida, error = correr("hoja", "netlist", BASE / "v2", "--plan", doc, "--seccion", "Anexo A")
        self.assertEqual(codigo, 0, salida + error)
        self.assertIn("(Anexo A): 3 redes, 8 pines; 0 diferencias; 1 entradas sin interpretar", salida)
        codigo, salida, _ = correr("hoja", "netlist", BASE / "v2", "--plan", doc)
        self.assertEqual(codigo, 1)
        self.assertIn("X: no está en la netlist (sus pines están en /I2C_SDA)", salida)
        plan, ignoradas = hoja.leer_plan(doc.read_text(encoding="utf-8"), "anexo a")
        self.assertEqual(plan[0], ("/I2C_SDA", [("U5", "34"), ("R24", "2"), ("U13", "1"), ("U18", "15")]))
        self.assertEqual(len(ignoradas), 1)
        net = {"redes": {"/I2C_SDA": {("U5", "34"), ("R24", "2"), ("U18", "15"), ("R99", "1")},
                         "/Conectores/ILIM_5V": {("U14", "5"), ("R69", "1")}, "/Otra/ILIM_5V": {("R1", "1")},
                         "unconnected-(U18-P6-Pad11)": {("U18", "11")}, "GND": {("U18", "12"), ("U13", "1")}}}
        dif = hoja.comparar_plan(net, plan)
        self.assertEqual(dif, ["/I2C_SDA: falta U13-1 (está en «GND»)", "/I2C_SDA: pines de más R99-1", "NC: U18-12 está en «GND»"])
        codigo, _, error = correr("hoja", "netlist", BASE / "v2", BASE / "v2", "--plan", doc)
        self.assertEqual(codigo, 2)
        self.assertIn("un solo proyecto", error)


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
        codigo, salida, error = correr("sincronizar", proy, "-o", TMP / "sync.kicad_pcb", "--actualizar", "U6,U13")
        self.assertEqual(codigo, 0, salida + error)
        self.assertIn("nuevas 3 · borradas 1 · recargadas 2", salida)
        self.assertIn("Paridad 0", salida)
        self.assertIn("Nuevas (sin colocar): U5 R16 R17", salida)
        self.assertIn("Borradas: R999", salida)
        # VAL-0029-01-01 (c): U13 (huella oficial sin su STEP en KiCad 10) recargada con el modelo de respaldo
        self.assertIn("Modelo 3D de respaldo (${KIPRJMOD}/../libraries/3d): U13", salida)
        nueva = _comun.leer(TMP / "sync.kicad_pcb")
        i, j = bloque(nueva, "U13")
        self.assertIn('(model "${KIPRJMOD}/../libraries/3d/Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad.step"', nueva[i:j])
        self.assertNotIn("KICAD10_3DMODEL_DIR", nueva[i:j])
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


class Colocacion(unittest.TestCase):
    """colocacion.py (SPEC-0037): extraer cubre todas las huellas en ≤ 8 k tokens; evaluar detecta los cinco fallos del
    criterio (solape, fuera del contorno, zona de la antena, borne en el borde equivocado, SHT40 lejos del borde)
    y puntúa igual una tabla que la PCB que deja colocar.py con ella (ida y vuelta)."""
    REGLAS = REPO / "docs" / "diseno" / "colocacion-reglas.csv"
    # Colocación de control: U5 con el extremo de la antena al ras del borde izquierdo (x 100,2), J4–J6 arriba (entrada
    # hacia fuera), J1, J10 y J7–J9 abajo, J2 al ras del lateral derecho y U13 en él. Contorno de 100 × 70 mm, de
    # (100, 60) a (200, 130).
    BIEN = ("U5,112.95,95,90,F\nJ4,120,66,0,F\nJ5,132,66,0,F\nJ6,144,66,0,F\nU13,197,95,0,F\nJ2,196.1,110,90,F\n"
            "J1,117,124,180,F\nJ10,135,126,90,F\nJ7,165,124,180,F\nJ8,177,124,180,F\nJ9,189,124,180,F\n"
            "R16,150,100,0,F\nR17,160,100,0,F\nC24,150,90,0,F\n")
    # Los cinco fallos: R17 sobre R18; C24 fuera (x 210); R16 en la parte de la zona de la antena que queda dentro
    # de la placa; J4 en el borde inferior; U13 en el centro.
    MAL = ("U5,113,95,90,F\nJ4,120,124,180,F\nJ5,132,66,0,F\nJ6,144,66,0,F\nU13,150,95,0,F\n"
           "R16,101.5,110,0,F\nR17,150,100,0,F\nR18,150.5,100,0,F\nC24,210,95,0,F\n")

    def evaluar(self, *args):
        detalle = TMP / f"col_{len(list(TMP.glob('col_*.txt')))}.txt"
        codigo, salida, error = correr("colocacion", "evaluar", *args, "--reglas", self.REGLAS, "--detalle", detalle)
        self.assertIn(codigo, (0, 1), error)
        self.assertLessEqual(len(salida.strip().splitlines()), 30)
        return salida, detalle.read_text(encoding="utf-8")

    def test_funciones(self):
        self.assertEqual(colocacion.expandir("J4-J6 U5.2 U7-U9.6 U5/antena"),
                         [("J4", None, None), ("J5", None, None), ("J6", None, None), ("U5", "2", None), ("U7", "6", None),
                          ("U8", "6", None), ("U9", "6", None), ("U5", None, "antena")])
        cuadro = [[(0, 0), (2, 0), (2, 1), (0, 1)]]
        self.assertAlmostEqual(colocacion.distancia(cuadro, [[(5, 0), (6, 0), (6, 1), (5, 1)]]), 3)
        self.assertEqual(colocacion.distancia(cuadro, [[(1, 0.5)]]), 0)
        self.assertEqual(colocacion.distancia(cuadro, [[(1, -1), (1.5, -1), (1.5, 3), (1, 3)]]), 0)   # se cruzan
        x, y = colocacion.girar((0, -1), 90)      # −Y de la huella con giro 90 (antihorario en pantalla) → izquierda
        self.assertAlmostEqual(x, -1)
        self.assertAlmostEqual(y, 0)
        self.assertEqual(colocacion.a_borde(cuadro, (0, 0, 10, 10), "lateral"), (0, "izq"))
        self.assertAlmostEqual(colocacion.arbol_minimo([(0, 0), (3, 0), (3, 4), (0, 4)]), 10)
        self.assertEqual(colocacion.alias_redes(["/A/OUT", "/B/OUT", "/VBUS"]), {"/A/OUT": "A/OUT", "/B/OUT": "B/OUT", "/VBUS": "VBUS"})
        self.assertEqual(colocacion.rangos(["1", "2", "3", "7", "EP"]), "1-3,7,EP")
        mala = TMP / "reglas_malas.csv"
        mala.write_text("id;tipo;piezas;objetivo;valor;nivel;origen;nota\nX1;borde;J4;arriba;1;obligatoria;REL-09;\n", encoding="utf-8")
        with self.assertRaises(_comun.Fallo):
            colocacion.leer_reglas(mala)
        mala.write_text("id;tipo;piezas;objetivo;valor;nivel;origen;nota\nX1;borde;J4;sup;1;obligatoria;;\n", encoding="utf-8")
        with self.assertRaises(_comun.Fallo):   # sin origen
            colocacion.leer_reglas(mala)

    def test_reglas_del_repositorio(self):
        reglas, clases = colocacion.leer_reglas(self.REGLAS)
        ids = [r["id"] for r in reglas + clases]
        self.assertEqual(len(ids), len(set(ids)))
        for r in reglas + clases:
            self.assertRegex(r["origen"], r"[A-Z]{3}-\d\d|\.md §|DEC-\d{4}|\.md\b", r["id"])
        self.assertTrue({"borde", "hacia", "cerca_par", "lejos", "fila", "zona", "sale", "libre"} <= {r["tipo"] for r in reglas})
        self.assertEqual(colocacion.clase_de("/Alimentacion/VIN_PROT", clases), ("Power_In", 3))
        self.assertEqual(colocacion.clase_de("/Salidas/Canal1/OUT", clases), ("Salidas", 3))
        self.assertEqual(colocacion.clase_de("GND", clases), ("GND", 0))
        self.assertEqual(colocacion.clase_de("/MCU/EN", clases), ("Default", 1.0))

    def test_extraer(self):
        v2 = BASE / "v2"
        n = _comun.leer(v2 / "esp-riego.kicad_pcb").count("\n\t(footprint ")
        self.assertGreater(n, 150)
        codigo, salida, error = correr("colocacion", "extraer", v2, "-o", TMP / "huellas.txt")
        self.assertEqual(codigo, 0, error)
        texto = (TMP / "huellas.txt").read_text(encoding="utf-8")
        filas = [l for l in texto.splitlines() if l and not l.startswith("#")]
        self.assertEqual(len(filas), n)
        self.assertEqual(len({l.split()[0] for l in filas}), n)
        self.assertLessEqual(colocacion.estimar_tokens(texto), 8000)
        self.assertLessEqual(len(texto), 32000)          # ≤ 8 k tokens aunque fueran 4 caracteres por token
        self.assertIn(f"{n} huellas", salida)
        u5 = next(l for l in filas if l.startswith("U5 "))
        self.assertRegex(u5, r" zona -24,-27\.8,24,-6\.8 .*GND:1,40,41 \+3V3:2 EN:3")
        codigo, salida, error = correr("colocacion", "extraer", v2, "--refs", "J4,U13")
        self.assertEqual(codigo, 0, error)
        self.assertEqual(len(salida.strip().splitlines()), 2)
        self.assertIn("1(0,0)Canal1/OUT 2(5.08,0)GND", salida)
        codigo, _, error = correr("colocacion", "extraer", v2)
        self.assertEqual(codigo, 2)
        codigo, _, error = correr("colocacion", "extraer", v2, "--refs", "ZZ9")
        self.assertEqual(codigo, 2)
        self.assertIn("ZZ9", error)

    def test_cinco_fallos(self):
        bien, mal = TMP / "col_bien.csv", TMP / "col_mal.csv"
        bien.write_text("ref,x,y,giro,cara\n" + self.BIEN, encoding="utf-8")
        mal.write_text("ref,x,y,giro,cara\n" + self.MAL, encoding="utf-8")
        salida, det = self.evaluar(BASE / "v2", bien)
        patron = (r"\tsolape\t\t\tR1[678]/|\tfuera\t\t\t(U5|J[124-9]|J10|U13|R16|R17|C24) |\tzona\t|\tB0[1-9]\t|\tB1[0-3]\t"
                  r"|\tA0[12]\t|\tS01\t")
        self.assertEqual([l for l in det.splitlines() if re.search(patron, l)], [])
        salida, det = self.evaluar(BASE / "v2", mal)
        self.assertRegex(det, r"obligatoria\tsolape\t\t\tR17/R18 [\d.]+ mm²")
        self.assertRegex(det, r"obligatoria\tfuera\t\t\tC24 11\.7 mm")
        self.assertRegex(det, r"obligatoria\tzona\t\t\tR16 en U5/zona [\d.]+ mm²")
        self.assertRegex(det, r"obligatoria\tregla\tB01\t[^\t]*\tJ4 59\.3")
        self.assertRegex(det, r"obligatoria\tregla\tB05\t[^\t]*\tJ4 giro 180")
        self.assertRegex(det, r"obligatoria\tregla\tS01\t[^\t]*\tU13 48\.8")
        self.assertNotRegex(det, r"\tfuera\t\t\tU5 ")          # la zona de la antena puede salir (regla «sale»)
        self.assertRegex(salida, r"Solapes de patio: 1 · R17/R18")
        self.assertRegex(salida, r"En zona prohibida: 1 · R16 en U5/zona")
        self.assertIn("! B01 borde sup ≤ 3: J4 59.3", salida)
        self.assertIn("! S01 borde lateral ≤ 6: U13 48.8 (izq)", salida)

    def test_ida_y_vuelta(self):
        origen = BASE / "v2" / "esp-riego.kicad_pcb"
        todo, tabla = TMP / "col_todo.csv", TMP / "col_tabla.csv"
        codigo, _, error = correr("colocar", origen, "--exportar", todo)
        self.assertEqual(codigo, 0, error)
        filas = todo.read_text(encoding="utf-8").splitlines()
        nuevas = {l.split(",")[0]: l for l in self.BIEN.splitlines()}
        filas = [filas[0]] + [nuevas.get(l.split(",")[0], l) for l in filas[1:]]
        tabla.write_text("\n".join(filas) + "\n", encoding="utf-8")
        antes = origen.read_bytes()
        s1, d1 = self.evaluar(BASE / "v2", tabla)
        self.assertEqual(antes, origen.read_bytes())
        self.assertIn(f"({len(filas) - 1} filas, {len(filas) - 1} aplicadas)", s1)
        proy = copia("v2_colocacion")
        codigo, salida, error = correr("colocar", origen, tabla, "-o", proy / "esp-riego.kicad_pcb")
        self.assertEqual(codigo, 0, salida + error)
        vuelta = TMP / "col_vuelta.csv"
        correr("colocar", proy / "esp-riego.kicad_pcb", "--exportar", vuelta)
        def norm(texto):
            return {l.split(",")[0]: [round(float(c), 3) if c[0] in "-0123456789" else c for c in l.split(",")[1:]]
                    for l in texto.splitlines()[1:]}
        self.assertEqual(norm(vuelta.read_text(encoding="utf-8")), norm(tabla.read_text(encoding="utf-8")))
        s2, d2 = self.evaluar(proy)
        quitar = lambda s: [l for l in s.splitlines() if not l.startswith("evaluar:")]   # noqa: E731
        self.assertEqual(quitar(s1), quitar(s2))
        self.assertEqual(sorted(quitar(d1)), sorted(quitar(d2)))


class ColocacionCriterios(unittest.TestCase):
    """colocacion.py con los criterios de DEC-0016 (SPEC-0037, paso 3): evaluar detecta los seis fallos sembrados
    (separación de JLCPCB, dos textos solapados, texto sobre un pad, referencia lejos de su pieza, dos fuentes de calor
    juntas y placa de más de 100 mm con su aviso de coste); --placa mueve los taladros; referencias coloca las
    referencias sin fallos donde hay sitio y colocar.py las aplica (ida y vuelta)."""
    REGLAS = REPO / "docs" / "diseno" / "colocacion-reglas.csv"
    CAB = "ref,x,y,giro,cara,rx,ry,rgiro,ralto,rtrazo\n"
    # Contorno de 100 × 70 mm, de (100, 60) a (200, 130); el resto de huellas está fuera, lejos.
    # Control: R17/R18 a 2 mm, referencias en su sitio de la librería, U7 y U8 a 12,7 mm.
    BIEN = ("R17,150,100,0,F\nR18,155,100,0,F\nR16,150,90,0,F\nC24,160,90,0,F\nC25,170,90,0,F\nR20,180,90,0,F\n"
            "U7,130,115,0,F\nU8,150,115,0,F\n")
    # Fallos: R18 a 0,05 mm de R17 (patio 2,96 mm); la referencia de C24 encima de la de R16; la de C25 sobre su
    # pad 1; la de R20 a 4 mm; U8 a 1 mm de U7 (patio 7,3 mm). La placa de 110 mm va con --placa.
    MAL = ("R17,150,100,0,F\nR18,153.01,100,0,F\nR16,150,90,0,F\nC24,160,90,0,F,-10,-1.43\nC25,170,90,0,F,-0.78,0\n"
           "R20,180,90,0,F,0,-4\nU7,130,115,0,F\nU8,138.3,115,0,F\n")

    def evaluar(self, tabla, *args, pcb=None):
        detalle = TMP / f"colc_{len(list(TMP.glob('colc_*.txt')))}.txt"
        codigo, salida, error = correr("colocacion", "evaluar", pcb or BASE / "v2", *([tabla] if tabla else []), *args,
                                       "--reglas", self.REGLAS, "--detalle", detalle)
        self.assertIn(codigo, (0, 1), error)
        self.assertLessEqual(len(salida.strip().splitlines()), 30)
        return salida, detalle.read_text(encoding="utf-8")

    def test_funciones(self):
        self.assertEqual(colocacion.excluidas("* !U5 !J4-J5"), {"U5", "J4", "J5"})
        self.assertEqual(colocacion.expandir("* !U5 J2"), [("J2", None, None)])
        self.assertEqual(colocacion.tam_placa("100x85,5"), (100, 85.5))
        self.assertIsNone(colocacion.tam_placa("100"))
        self.assertAlmostEqual(colocacion.dist_cajas((0, 0, 1, 1), (4, 5, 6, 6)), 5)
        self.assertEqual(colocacion.dist_cajas((0, 0, 2, 2), (1, 1, 3, 3)), 0)
        self.assertAlmostEqual(colocacion.a_caja_interior((1, 2, 9, 9.5), (0, 0, 10, 10)), 0.5)
        rej = colocacion.Rejilla()
        rej.poner("a", (0, 0, 1, 1), "A")
        rej.poner("b", (20, 20, 21, 21), "B")
        self.assertEqual([c for c, _, _ in rej.cerca((1.5, 0, 2, 1), 0.6)], ["a"])
        rej.quitar("a")
        self.assertEqual(list(rej.cerca((1.5, 0, 2, 1), 0.6)), [])
        cand = colocacion.candidatos((0, 0, 4, 2), {0: (-1, -0.5, 1, 0.5), 90: (-0.5, -1, 0.5, 1)})
        self.assertEqual(len(cand), 3 * 2 * 4 * 3)
        orden, giro, ancla, caja = cand[0]
        self.assertEqual((giro, [round(v, 6) for v in caja]), (0, [1, -1.15, 3, -0.15]))   # encima, centrada, a 0,15 mm
        self.assertEqual([round(v, 6) for v in ancla], [2, -0.65])
        mala = TMP / "reglas_malas2.csv"
        for fila in ("X1;serigrafia;*;color;1;obligatoria;DEC-0016;", "X1;precio;grande;5;2;objetivo;DEC-0016;",
                     "X1;calor;U7;mucho;0.3;obligatoria;DEC-0016;"):
            mala.write_text("id;tipo;piezas;objetivo;valor;nivel;origen;nota\n" + fila + "\n", encoding="utf-8")
            with self.assertRaises(_comun.Fallo, msg=fila):
                colocacion.leer_reglas(mala)

    def test_reglas_de_dec_0016(self):
        reglas, _ = colocacion.leer_reglas(self.REGLAS)
        tipos = {r["tipo"] for r in reglas}
        self.assertTrue({"separacion", "borde_min", "cobre_borde", "serigrafia", "calor", "reparto", "precio"} <= tipos)
        for r in reglas:
            if "JLCPCB" in r["origen"]:           # cada regla de JLCPCB cita la página (URL) y la fecha de consulta
                self.assertRegex(r["origen"], r"https://jlcpcb\.com/\S+", r["id"])
                self.assertRegex(r["origen"], r"(consultado|actualizado|20\d\d-\d\d-\d\d)", r["id"])
                self.assertRegex(r["origen"], r"20\d\d-\d\d-\d\d", r["id"])
        p = colocacion.param_serigrafia(reglas)
        self.assertGreaterEqual(p["alto"], 1.0)                    # JLCPCB: 1,0 mm de alto mínimo
        self.assertGreaterEqual(p["trazo_ref"], max(0.15, p["alto"] / 6))   # 0,15 mm y 1:6
        calor = {o[0]: r["mm"] for r in reglas if r["tipo"] == "calor" for o in colocacion.expandir(r["piezas"])}
        self.assertTrue({"U1", "U2", "U4", "U7", "U12", "L1", "Q1", "D3", "F1"} <= set(calor))   # DEC-0016 (3)
        self.assertTrue(any(r["tipo"] == "precio" and r["tam"] == (100, 100) for r in reglas))

    def test_seis_fallos(self):
        bien, mal = TMP / "colc_bien.csv", TMP / "colc_mal.csv"
        bien.write_text(self.CAB + self.BIEN, encoding="utf-8")
        mal.write_text(self.CAB + self.MAL, encoding="utf-8")
        s_bien, d_bien = self.evaluar(bien)
        s_mal, d_mal = self.evaluar(mal, "--placa", "110x70")
        casos = [  # (regla, patrón del item en el detalle)
            ("F01", r"R17/R18 0\.0[4-6]"),                   # separación de JLCPCB (IPC-7351B + FAB-02) incumplida
            ("T05", r"(C24/R16|R16/C24) 0"),                 # dos textos de serigrafía solapados
            ("T06", r"C25 0 de C25\.1"),                     # texto sobre un pad
            ("T11", r"R20 [23](\.\d)?$"),                    # referencia lejos de su pieza
            ("Q10", r"U7/U8 (0\.9|1|1\.1)$"),               # dos fuentes de calor demasiado juntas
            ("Z01", r"placa 110×70 > 100x100"),              # placa de más de 100 mm: aviso de coste
        ]
        for regla, item in casos:
            self.assertRegex(d_mal, rf"(?m)\tregla\t{regla}\t[^\t]*\t{item}", regla)
            self.assertNotRegex(d_bien, rf"(?m)\tregla\t{regla}\t[^\t]*\t{item.split(' ')[0]}", regla)
        self.assertRegex(d_mal, r"(?m)^obligatoria\tregla\tT07\t[^\t]*\tC25 sobre C25\.1")   # y sobre la máscara
        self.assertIn("AVISO", s_mal.splitlines()[2])
        self.assertIn("taladros movidos: H1 H2", s_mal)
        self.assertNotIn("AVISO", s_bien)
        self.assertRegex(s_bien.splitlines()[2], r"^Placa 100×70 mm · PCB 2 \$ por 5 uds")
        self.assertRegex(s_mal, r"Serigrafía \(\d+ referencias\): .*texto-texto")
        self.assertRegex(s_mal, r"Térmico: [\d.]+ W en \d+ fuentes")
        self.assertRegex(d_mal, r"(?m)^precio\t110x70\tsin tarifa\t.*https://jlcpcb\.com/")
        self.assertRegex(d_mal, r"(?m)^red\t/BUS_24V\tPower_In\t")    # clase de las reglas en --detalle

    def test_placa_y_taladros(self):
        tabla = TMP / "colc_placa.csv"
        tabla.write_text(self.CAB + "PLACA,90,80,,\n" + self.BIEN, encoding="utf-8")
        salida, det = self.evaluar(tabla)
        self.assertRegex(salida, r"(?m)^Placa 90×80 mm \(taladros movidos: (H\d ?){3}\) · PCB 2 \$")
        self.assertNotRegex(det, r"\t(G03|bloqueada)\t")             # los taladros se mueven con su esquina
        proy = copia("v2_placa")
        codigo, salida, error = correr("colocar", proy / "esp-riego.kicad_pcb", tabla, "-o", proy / "esp-riego.kicad_pcb")
        self.assertEqual(codigo, 0, salida + error)
        self.assertIn("Placa 90 × 80 mm", salida)
        texto = _comun.leer(proy / "esp-riego.kicad_pcb")
        self.assertRegex(texto, r"\(gr_rect\s+\(start 100 60\)\s+\(end 190 140\)")
        vuelta = TMP / "colc_placa_vuelta.csv"
        correr("colocar", proy / "esp-riego.kicad_pcb", "--exportar", vuelta)
        pos = {l.split(",")[0]: l.split(",")[1:3] for l in vuelta.read_text(encoding="utf-8").splitlines()[1:]}
        self.assertEqual(sorted(tuple(map(float, pos[h])) for h in ("H1", "H2", "H3", "H4")),
                         [(104, 64), (104, 136), (186, 64), (186, 136)])

    def test_referencias_y_vuelta(self):
        bien, con = TMP / "colc_bien_r.csv", TMP / "colc_con_refs.csv"
        bien.write_text(self.CAB + self.BIEN, encoding="utf-8")
        codigo, salida, error = correr("colocacion", "referencias", BASE / "v2", bien, "-o", con, "--reglas", self.REGLAS)
        self.assertIn(codigo, (0, 1), error)
        self.assertLessEqual(len(salida.strip().splitlines()), 30)
        filas = {l.split(",")[0]: l.split(",") for l in con.read_text(encoding="utf-8").splitlines()[1:]}
        self.assertEqual(filas["R17"][1:5], ["150", "100", "0", "F"])
        self.assertEqual(filas["R17"][8:10], ["1", "0.18"])          # alto y trazo de T01–T03
        self.assertNotRegex(salida.splitlines()[1], r"\b(R1[678]|R20|C2[45]|U[78]) \(")   # con sitio, sin fallos
        s, det = self.evaluar(con)
        for ref in ("R16", "R17", "R18", "R20", "C24", "C25", "U7", "U8"):
            self.assertNotRegex(det, rf"(?m)\tregla\tT(0[1-9]|1[0-3])\t[^\t]*\t{ref}\b", ref)
        proy = copia("v2_refs")
        codigo, salida, error = correr("colocar", proy / "esp-riego.kicad_pcb", con, "-o", proy / "esp-riego.kicad_pcb")
        self.assertEqual(codigo, 0, salida + error)
        vuelta = TMP / "colc_refs_vuelta.csv"
        codigo, _, error = correr("colocar", proy / "esp-riego.kicad_pcb", "--exportar", vuelta, "--con-referencias")
        self.assertEqual(codigo, 0, error)
        cabecera, *resto = vuelta.read_text(encoding="utf-8").splitlines()
        self.assertEqual(cabecera, self.CAB.strip())
        atras = {l.split(",")[0]: [round(float(c), 3) for c in l.split(",")[5:]] for l in resto}
        for ref in ("R17", "C25", "U7"):
            self.assertEqual(atras[ref], [round(float(c), 3) for c in filas[ref][5:]], ref)
        s2, det2 = self.evaluar(None, pcb=proy / "esp-riego.kicad_pcb")
        quitar = lambda t: sorted(l for l in t.splitlines() if l.startswith(("obligatoria", "objetivo")))   # noqa: E731
        self.assertEqual(quitar(det), quitar(det2))


class ColocacionPaso5(unittest.TestCase):
    """colocacion.py del paso 5 de SPEC-0037 (DEC-0016, tras el paso 4): J2 y la antena de U5 al ras, rieles de JLCPCB
    con su coste, lazos de potencia, longitud del USB, pasillos entre bloques y capacidad de los pasillos, margen del
    cobre de disipación con lo que ocupa cada anillo, cifras que incumplen por redondeo y referencias con vuelta atrás.
    Usa las colocaciones entregadas: colocacion-b2.csv (paso 4) incumple las reglas nuevas y colocacion-b3.csv no."""
    REGLAS = REPO / "docs" / "diseno" / "colocacion-reglas.csv"
    B2 = REPO / "docs" / "diseno" / "colocacion-b2.csv"
    B3 = REPO / "docs" / "diseno" / "colocacion-b3.csv"

    def evaluar(self, tabla, *args):
        detalle = TMP / f"colp5_{len(list(TMP.glob('colp5_*.txt')))}.txt"
        codigo, salida, error = correr("colocacion", "evaluar", BASE / "v2", tabla, *args, "--reglas", self.REGLAS,
                                       "--detalle", detalle)
        self.assertIn(codigo, (0, 1), error)
        self.assertLessEqual(len(salida.strip().splitlines()), 30)
        return codigo, salida, detalle.read_text(encoding="utf-8")

    def test_funciones(self):
        self.assertEqual(colocacion.cifra(299.6, 300, True, 0), "299.6")      # incumple: no se escribe «300»
        self.assertEqual(colocacion.cifra(300.4, 300, True, 0), "300")
        self.assertEqual(colocacion.cifra(8.04, 8, False, 1), "8.04")
        self.assertEqual(colocacion.cifra(7.96, 8, False, 1), "8")
        self.assertEqual(sorted(tuple(sorted(a)) for a in colocacion.aristas_minimas([(0, 0), (3, 0), (3, 4)])),
                         [(0, 1), (1, 2)])
        self.assertEqual(colocacion.huecos_pista([1.0, 0.1, 0.2]), 4)        # 1,0 mm: 3 pistas; 0,2: 1; 0,1: ninguna
        mala = TMP / "reglas_malas_p5.csv"
        for fila in ("X1;lazo;U2 C8;;12;obligatoria;DEC-0016;",              # un lazo pide pads
                     "X1;ras;J2;arriba;0.5;obligatoria;DEC-0016;",           # borde desconocido
                     "X1;corte;*;largo;1;obligatoria;DEC-0016;"):           # tramo no numérico
            mala.write_text("id;tipo;piezas;objetivo;valor;nivel;origen;nota\n" + fila + "\n", encoding="utf-8")
            with self.assertRaises(_comun.Fallo, msg=fila):
                colocacion.leer_reglas(mala)

    def test_reglas_del_paso5(self):
        reglas, _ = colocacion.leer_reglas(self.REGLAS)
        por_id = {r["id"]: r for r in reglas}
        self.assertTrue({"ras", "rieles", "lazo", "largo", "pasillo", "corte", "margen"} <= {r["tipo"] for r in reglas})
        self.assertEqual((por_id["A01"]["tipo"], por_id["A01"]["piezas"]), ("ras", "U5/antena"))
        self.assertRegex(por_id["A01"]["origen"], r"HDG §1\.4\.7, p\. 30")
        self.assertEqual((por_id["B12"]["tipo"], por_id["B12"]["piezas"]), ("ras", "J2"))
        self.assertIn("!J2", por_id["F03"]["piezas"].split())
        self.assertEqual(por_id["A06"]["tipo"], "sale")
        self.assertEqual(por_id["U01"]["mm"], 40)                             # mcu.md §12: USB ≤ 40 mm
        self.assertGreater(por_id["Q13"]["mm"], 1)
        self.assertRegex(por_id["R01"]["origen"], r"https://jlcpcb\.com/help/article/\S*edge-rails")

    def test_b2_incumple_y_b3_cumple(self):
        c2, s2, d2 = self.evaluar(self.B2)
        self.assertEqual(c2, 1)
        casos = [  # (regla, patrón del item en el detalle de colocacion-b2.csv)
            ("A01", r"U5/antena 1[45](\.\d+)? \(izq\)"),                  # antena dentro, lejos del borde
            ("B12", r"J2 2\.\d+ \(izq\)"),                                   # USB-C a 2,75 mm, no al ras
            ("W01", r"C1 \d+"),                                               # C1 lejos de U1
            ("W03", r"(D1|R1) \d+"),                                          # R1/D1 lejos de la puerta de Q1
            ("W07", r"\d+(\.\d+)? \(tramo más largo C11\.2→U2\.9"),      # lazo de salida del buck
            ("U01", r"USB_DP\+USB_DP_C \d+"),                               # USB de J2 a U5 > 40 mm
            ("N01", r"\w+/\w+ 0\.\d+"),                                      # pasillo entre bloques < 1 mm
            ("N02", r"[xy] [\d.]+ [xy] [\d.]+…[\d.]+: [\d.]+ pistas, caben \d+"),   # pasillo sin capacidad
            ("Q13", r"U11 \d+(\.\d+)?/330"),                                  # cobre sin el margen de +10 %
        ]
        for regla, item in casos:
            self.assertRegex(d2, rf"(?m)^obligatoria\tregla\t{regla}\t[^\t]*\t{item}", regla)
        self.assertRegex(d2, r"(?m)^calor\tU11\t.*\tanillo \d+ mm², ocupan: .*½ U1[02] \d+")   # qué ocupa el anillo
        self.assertRegex(s2, r"En zona prohibida: 0 · zona dentro de la placa: U5 1008 mm²")
        c3, s3, d3 = self.evaluar(self.B3)
        self.assertEqual(c3, 0, s3)
        self.assertNotRegex(d3, r"(?m)^obligatoria\t")
        self.assertRegex(s3, r"(?m)^Placa 100×100 mm .*rieles \(izq: J2 0\.2, U5 0\.2\): panel 110×100, sin tarifa")
        self.assertRegex(d3, r"(?m)^objetivo\tregla\tR01\t")               # el coste de los rieles, a la vista
        self.assertRegex(s3, r"zona dentro de la placa: U5 29\d mm²")         # antena al ras: 48 × 6 mm
        _, s4, d4 = self.evaluar(self.B3, "--omitir", "serigrafia")
        self.assertNotRegex(d4, r"(?m)\tregla\tT\d\d\t")
        self.assertEqual(correr("colocacion", "evaluar", BASE / "v2", self.B3, "--omitir", "nada")[0], 2)

    def test_referencias_con_vuelta_atras(self):
        con, sin = TMP / "colp5_con.csv", TMP / "colp5_sin.csv"
        codigo, salida, error = correr("colocacion", "referencias", BASE / "v2", self.B3, "-o", con, "--todas",
                                       "--reglas", self.REGLAS)
        self.assertEqual(codigo, 0, salida + error)
        self.assertRegex(salida, r"vuelta atrás: [1-9]\d* recolocadas")
        self.assertIn("Sin sitio que cumpla todo (0)", salida)
        codigo, salida, error = correr("colocacion", "referencias", BASE / "v2", self.B3, "-o", sin, "--todas",
                                       "--sin-vuelta", "--reglas", self.REGLAS)
        self.assertEqual(codigo, 1, salida + error)                           # la pasada voraz deja alguna sin sitio
        self.assertIn("vuelta atrás: 0 recolocadas", salida)


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
        self.assertEqual(len(puntos), 25)
        self.assertLessEqual(len(r["lineas"]), 30)
        for punto in ("esquema.hojas", "esquema.huellas", "esquema.vias", "layout.incrustados", "layout.salida",
                      "layout.smd_cara", "librerias.formato", "librerias.rutas", "librerias.serigrafia",
                      "esquema.cruces", "esquema.sueltas", "esquema.recuadros", "esquema.etiquetas"):
            self.assertEqual(puntos[punto]["estado"], "OK", puntos[punto])
        self.assertEqual(puntos["esquema.pcb_main"]["estado"], "N/A")      # la copia no está en el repositorio
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

    def test_librerias_3d_respaldo(self):
        """VAL-0029-01-01 (b): U13 usa una huella oficial cuyo STEP falta en KiCad 10; vale el de libraries/3d."""
        sht = "Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad"
        respaldo, fuera = self.libs / "3d" / f"{sht}.step", self.d / f"{sht}.step"
        self.assertFalse((_comun.MODELOS / "Sensor_Humidity.3dshapes" / f"{sht}.step").is_file(), "KiCad ya trae el STEP")
        estado, detalle = self.punto("librerias.3d")
        self.assertEqual(estado, "OK", detalle)
        self.assertIn(f"respaldo en libraries/3d: Sensor_Humidity:{sht}", detalle)
        shutil.move(respaldo, fuera)
        try:
            self.falla("librerias.3d", f"Sensor_Humidity:{sht}: no existe")
        finally:
            shutil.move(fuera, respaldo)
        self.assertEqual(self.punto("librerias.3d")[0], "OK")

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
        usb, led, esp, bloque_, bloque_con = (self.comp / n for n in ("USBLC6-2SC6.md", "KT-0603R.md", "ESP32-S3-WROOM-1.md",
                                                                      "bloque-alimentacion.md", "bloque-conectores.md"))
        self.guardar(usb, led, esp, bloque_, bloque_con)
        antes = {l.split(" ")[0] for l in self.punto("librerias.fichas")[1].splitlines()}
        self.assertFalse({"C7519", "C2913198", "C23137"} & antes, antes)
        sustituir(usb, "tipo_jlcpcb: extended", "tipo_jlcpcb:")
        sustituir(bloque_con, "| C7519 | Extended ·", "| C7519 | ·")     # C7519 también está en la ficha de bloque (SPEC-0031)
        # C2913198 sale de su ficha y solo se cita en otra, como alternativa: no cuenta
        sustituir(esp, "lcsc: C2913198", "lcsc: C1")
        _comun.escribir(led, _comun.leer(led) + "\nAlternativa descartada: C2913198.\n")
        # C23137 (R11) solo está en la columna LCSC de una ficha de bloque; sin tipo en su fila, falla
        sustituir(bloque_, "| C23137 | Basic ·", "| C23137 | ·")
        lineas = {l.split(" ")[0]: l for l in self.falla("librerias.fichas").splitlines()}
        self.assertIn("(bloque-conectores.md) le falta tipo", lineas["C7519"])
        self.assertIn("sin ficha", lineas["C2913198"])
        self.assertIn("(bloque-alimentacion.md) le falta tipo", lineas["C23137"])
        # una alternativa entre paréntesis en el campo lcsc tampoco cuenta como ficha
        self.assertEqual(comprobar.codigos_lcsc("C44479 (alternativa TLC TA10, C2998199)"), ["C44479"])
        self.assertEqual(comprobar.codigos_lcsc("C1858395 (FADDAR) · C2879422 (ADDAR)"), ["C1858395", "C2879422"])

    def anadir(self, ruta, bloque_):
        """Añade un elemento al final de una hoja (antes del paréntesis que la cierra)."""
        self.guardar(ruta)
        texto = _comun.leer(ruta).rstrip()
        _comun.escribir(ruta, texto[:-1] + bloque_ + "\n)\n")

    def test_esquema_estilo(self):
        """Puntos de KIC-06 sobre la hoja piloto (Sensores); todas las hojas los cumplen."""
        sens = self.v2 / "sensores.kicad_sch"
        for punto in ("esquema.cruces", "esquema.sueltas", "esquema.recuadros", "esquema.etiquetas"):
            self.assertEqual(self.punto(punto)[0], "OK", punto)
        self.anadir(sens, '\t(wire (pts (xy 134.62 101.6) (xy 149.86 101.6)) (stroke (width 0) (type default)) (uuid "m1"))\n'
                          '\t(text "SOLAPE" (at 170.18 100.33 0) (effects (font (size 1.27 1.27))) (uuid "m2"))')
        self.falla("esquema.cruces", "sensores.kicad_sch: cable (134.62, 101.6)–(149.86, 101.6) cruza U13",
                   "«SOLAPE» (nota)")
        self.anadir(sens, '\t(label "SUELTA" (at 50.8 50.8 0) (effects (font (size 1.27 1.27))) (uuid "m3"))\n'
                          '\t(hierarchical_label "I2C_SDA" (shape bidirectional) (at 125.73 104.14 180)'
                          ' (effects (font (size 1.27 1.27)) (justify right)) (uuid "m4"))')
        self.falla("esquema.sueltas", "label «SUELTA» suelta en (50.8, 50.8)")
        self.falla("esquema.etiquetas", "«I2C_SDA» 2 veces en el recuadro «Temperatura y humedad")
        sustituir(sens, "(size 86.36 54.61)", "(size 20 20)")
        self.falla("esquema.recuadros", "sensores.kicad_sch: U13 fuera de un recuadro")

    def test_esquema_cruces_texto_largo(self):
        """Un cable a menos de 2 mm del final de un texto largo en mayúsculas lo cruza (VAL-0035-01-01): la caja
        es la tinta real de la fuente (17,29 mm para «TLV1117LV33DCYR» a 1,27 mm; con 0,8 × alto salían 15,2)."""
        sens = self.v2 / "sensores.kicad_sch"
        texto = '\t(text "TLV1117LV33DCYR" (at 25.4 40.64 0) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "m5"))'
        self.anadir(sens, texto + '\n\t(wire (pts (xy 42.164 36.83) (xy 42.164 41.91)) (stroke (width 0) (type default)) (uuid "m6"))')
        self.falla("esquema.cruces", "cruza el texto «TLV1117LV33DCYR»")        # 0,5 mm antes del final de la «R»
        _comun.escribir(sens, self.guardados[sens])
        self.anadir(sens, texto + '\n\t(wire (pts (xy 42.926 36.83) (xy 42.926 41.91)) (stroke (width 0) (type default)) (uuid "m6"))')
        self.assertEqual(self.punto("esquema.cruces")[0], "OK")                 # 0,24 mm después de la tinta: no cruza
        caja = _estilo.caja_texto(0, 0, "TLV1117LV33DCYR", 1.27, 0, "left", "bottom")
        self.assertAlmostEqual(caja[2], 17.29, delta=0.02)
        self.assertAlmostEqual(caja[1], -1.76, delta=0.02)                       # mayúsculas por encima del ancla
        self.assertGreater(_estilo.caja_texto(0, 0, "IIII", 1.27, 0, "left", "bottom")[2], 2.0)
        self.assertLess(_estilo.caja_texto(0, 0, "IIII", 1.27, 0, "left", "bottom")[2], 2.6)   # glifo estrecho

    def test_esquema_pcb_main(self):
        """Huella que cambia frente a main: falla si ni la spec ni sus partes la citan (rangos incluidos)."""
        texto = _comun.leer(self.pcb)
        i, j = bloque(texto, "R16")
        en_main = texto[:i] + texto[i:j].replace('(property "Value" "', '(property "Value" "X', 1) + texto[j:]
        antes = comprobar.pcb_de_referencia, comprobar.textos_de_la_spec
        try:
            comprobar.pcb_de_referencia = lambda p: (texto, "spec/SPEC-0099-prueba")
            self.assertEqual(self.punto("esquema.pcb_main")[0], "OK")
            comprobar.pcb_de_referencia = lambda p: (en_main, "spec/SPEC-0099-prueba")
            comprobar.textos_de_la_spec = lambda p, rama: "Huellas que cambian frente a `main`: D12–D17 y R44."
            self.falla("esquema.pcb_main", "R16: huella cambiada frente a main")
            # citada fuera de la sección marcada: no cuenta (VAL-0035-01-06)
            comprobar.textos_de_la_spec = lambda p, rama: ("- R16 girada en la hoja.\n"
                                                           "- Huellas que cambian frente a `main` (ruta): D12–D17. R16 no cambia.")
            self.falla("esquema.pcb_main", "R16: huella cambiada frente a main")
            comprobar.textos_de_la_spec = lambda p, rama: "- Huellas que cambian frente a `main`: R14-R16 y U7."
            self.assertEqual(self.punto("esquema.pcb_main")[0], "OK")
        finally:
            comprobar.pcb_de_referencia, comprobar.textos_de_la_spec = antes
        self.assertEqual(comprobar.refs_citadas("U7–U12, D12-D17 y R44; SPEC-0035"),
                         {"U7", "U8", "U9", "U10", "U11", "U12", "D12", "D13", "D14", "D15", "D16", "D17", "R44"})
        lista = "## Huellas que cambian frente a main:\n\n- U7–U12\n- R44 (valor)\n\nD4 y D5 se citan por otra cosa.\n"
        self.assertEqual(comprobar.refs_citadas(comprobar.seccion_huellas(lista)),
                         {"U7", "U8", "U9", "U10", "U11", "U12", "R44"})
        self.assertEqual(comprobar.seccion_huellas("Cambian D4 y U6 por el estilo."), "")


if __name__ == "__main__":
    unittest.main()
