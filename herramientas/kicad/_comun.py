"""Utilidades comunes de herramientas/kicad. Solo biblioteca estándar.

Reglas que cumplen todas las herramientas:
- no modifican lo que leen: kicad-cli y pcbnew trabajan sobre una copia temporal del proyecto
  (con `../libraries` al lado) y solo se escribe en el destino que se indica;
- la salida cabe en 30 líneas (`emitir`); el detalle completo va a un archivo si se pide.
"""
import contextlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

KICAD = Path(os.environ.get("KICAD_DIR", r"C:\Program Files\KiCad\10.0"))
KICAD_CLI = Path(os.environ.get("KICAD_CLI", KICAD / "bin" / "kicad-cli.exe"))
KICAD_PY = Path(os.environ.get("KICAD_PYTHON", KICAD / "bin" / "python.exe"))
SIMBOLOS = KICAD / "share" / "kicad" / "symbols"
HUELLAS = KICAD / "share" / "kicad" / "footprints"
MODELOS = KICAD / "share" / "kicad" / "3dmodels"
TFG = Path(r"C:\Users\josan\proyectos\TFG")
MAX_LINEAS = 30
CAMPOS = ("Value", "Footprint", "MPN", "Fabricante", "Datasheet", "Description", "LCSC Part#")


class Fallo(Exception):
    """Error de uso o de entorno: se muestra en una línea y la herramienta sale con 2."""


def principal(funcion):
    """Ejecuta `funcion()` con la salida en UTF-8 y los errores en una línea."""
    for flujo in (sys.stdout, sys.stderr):
        flujo.reconfigure(encoding="utf-8", errors="replace")
    try:
        sys.exit(funcion() or 0)
    except Fallo as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)


def emitir(lineas, maximo=MAX_LINEAS, detalle=None, pista="--detalle ARCHIVO"):
    """Imprime como mucho `maximo` líneas. Si sobran, lo dice (y las guarda en `detalle`)."""
    lineas = [l for bloque in lineas for l in str(bloque).split("\n")]
    if detalle:
        Path(detalle).write_text("\n".join(lineas) + "\n", encoding="utf-8")
    if len(lineas) > maximo:
        resto = len(lineas) - (maximo - 1)
        donde = f"; todo en {detalle}" if detalle else f"; usa {pista} para verlas" if pista else ""
        lineas = lineas[:maximo - 1] + [f"… y {resto} líneas más{donde}"]
    print("\n".join(lineas))


def raiz_repo(desde=None):
    """Carpeta que contiene CLAUDE.md, buscando hacia arriba; None si no la hay."""
    p = Path(desde or __file__).resolve()
    for carpeta in [p, *p.parents]:
        if (carpeta / "CLAUDE.md").is_file():
            return carpeta
    return None


def dentro(ruta, carpeta):
    a, b = os.path.normcase(os.path.abspath(ruta)), os.path.normcase(os.path.abspath(carpeta))
    return a == b or a.startswith(b + os.sep)


def no_tfg(ruta):
    if dentro(ruta, TFG):
        raise Fallo("la carpeta del TFG es de solo lectura: trabaja sobre una copia")


def leer(ruta):
    """Texto de un archivo de KiCad, con sus finales de línea tal cual."""
    with open(ruta, encoding="utf-8", newline="") as f:
        return f.read()


def escribir(ruta, texto):
    ruta = Path(ruta)
    no_tfg(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        f.write(texto)


# ------------------------------------------------------------------ expresiones S

_TOK = re.compile(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()"]+')
_ESC = {"n": "\n", "t": "\t", "r": "\r"}


def quitar_escape(s):
    return re.sub(r"\\(.)", lambda m: _ESC.get(m.group(1), m.group(1)), s)


def esc(s):
    return str(s).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def parse(texto):
    """Expresión S → listas anidadas de cadenas (las comilladas, sin comillas ni escapes)."""
    pila = [[]]
    for m in _TOK.finditer(texto):
        t = m.group()
        if t == "(":
            pila.append([])
        elif t == ")":
            hecho = pila.pop()
            pila[-1].append(hecho)
        else:
            pila[-1].append(quitar_escape(t[1:-1]) if t[0] == '"' else t)
    if len(pila) != 1 or not pila[0]:
        raise Fallo("expresión S mal cerrada")
    return pila[0][0]


def hijos(nodo, clave):
    return [c for c in nodo if isinstance(c, list) and c and c[0] == clave]


def uno(nodo, clave, defecto=None):
    for c in nodo:
        if isinstance(c, list) and c and c[0] == clave:
            return c
    return defecto


def val(nodo, clave, defecto=""):
    h = uno(nodo, clave) if nodo else None
    return h[1] if h and len(h) > 1 else defecto


def trozos(texto, inicio=0):
    """(nombre, i, j) de cada lista hija directa de la lista que abre en texto[inicio]."""
    prof, i = 0, None
    for m in _TOK.finditer(texto, inicio):
        t = m.group()
        if t == "(":
            prof += 1
            if prof == 2:
                i = m.start()
        elif t == ")":
            prof -= 1
            if prof == 1:
                nombre = re.match(r'\(\s*([^\s()"]*)', texto[i:i + 80]).group(1)
                yield nombre, i, m.end()
            elif prof == 0:
                return


def fin_bloque(texto, inicio):
    """Índice siguiente al paréntesis que cierra la lista que abre en texto[inicio]."""
    prof = 0
    for m in _TOK.finditer(texto, inicio):
        t = m.group()
        if t == "(":
            prof += 1
        elif t == ")":
            prof -= 1
            if prof == 0:
                return m.end()
    raise Fallo("bloque sin cerrar")


def num(x):
    """Número con 4 decimales como mucho y sin ceros de relleno."""
    s = ("%.4f" % float(x)).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# ------------------------------------------------------------------ proyecto y hojas

def proyecto(ruta):
    """(carpeta, nombre) del proyecto que indica un .kicad_pro, .kicad_sch, .kicad_pcb o carpeta."""
    ruta = Path(ruta).resolve()
    if ruta.is_dir():
        pros = sorted(ruta.glob("*.kicad_pro"))
        if len(pros) != 1:
            raise Fallo(f"se esperaba un único .kicad_pro en {ruta} y hay {len(pros)}")
        ruta = pros[0]
    if not ruta.exists():
        raise Fallo(f"no existe {ruta}")
    if ruta.suffix == ".kicad_sch" and not ruta.with_suffix(".kicad_pro").exists():
        pros = sorted(ruta.parent.glob("*.kicad_pro"))
        if len(pros) == 1:
            ruta = pros[0]
    return ruta.parent, ruta.stem


def simbolos_hoja(texto):
    """Símbolos colocados en una hoja: lista de dict con ref, lib_id, at, props, flags, uuid, i, j."""
    salida = []
    for nombre, i, j in trozos(texto):
        if nombre != "symbol":
            continue
        n = parse(texto[i:j])
        if not uno(n, "lib_id"):
            continue
        props = {p[1]: (p[2] if len(p) > 2 and isinstance(p[2], str) else "") for p in hijos(n, "property")}
        at = uno(n, "at", ["at", "0", "0", "0"])
        salida.append({
            "ref": props.get("Reference", "?"), "lib_id": val(n, "lib_id"), "props": props,
            "x": float(at[1]), "y": float(at[2]), "giro": int(float(at[3])) if len(at) > 3 else 0,
            "espejo": val(n, "mirror", None), "unidad": int(val(n, "unit", "1")),
            "dnp": val(n, "dnp", "no") == "yes", "in_bom": val(n, "in_bom", "yes") == "yes",
            "on_board": val(n, "on_board", "yes") == "yes", "uuid": val(n, "uuid"),
            "nodo": n, "i": i, "j": j,
        })
    return salida


def es_pieza(s):
    """Símbolo que es una pieza real (no de alimentación ni bandera)."""
    return not s["ref"].startswith("#") and not s["lib_id"].startswith("power:")


def hojas(raiz_sch):
    """Hojas del proyecto en orden jerárquico: dict con nombre, archivo, ruta (UUID) y nombres."""
    raiz_sch = Path(raiz_sch).resolve()
    texto = leer(raiz_sch)
    uuid_raiz = val(parse_cabecera(texto), "uuid")
    lista = [{"nombre": "/", "archivo": raiz_sch, "ruta": "/" + uuid_raiz, "nombres": "/"}]

    def bajar(texto, ruta, nombres, carpeta, vistos):
        for nombre, i, j in trozos(texto):
            if nombre != "sheet":
                continue
            n = parse(texto[i:j])
            props = {p[1]: p[2] for p in hijos(n, "property") if len(p) > 2}
            archivo = (carpeta / props.get("Sheetfile", "")).resolve()
            hoja = {"nombre": props.get("Sheetname", ""), "archivo": archivo,
                    "ruta": ruta + "/" + val(n, "uuid"), "nombres": nombres + props.get("Sheetname", "") + "/",
                    "pines": [(p[1], p[2]) for p in hijos(n, "pin")]}
            lista.append(hoja)
            if archivo.is_file() and archivo not in vistos:
                bajar(leer(archivo), hoja["ruta"], hoja["nombres"], archivo.parent, vistos | {archivo})

    bajar(texto, "/" + uuid_raiz, "/", raiz_sch.parent, {raiz_sch})
    return lista


def parse_cabecera(texto):
    """Elementos sueltos de la cabecera (uuid, paper, title_block…) sin analizar el resto."""
    nodo = ["cabecera"]
    for nombre, i, j in trozos(texto):
        if nombre in ("lib_symbols", "symbol", "footprint"):
            break
        nodo.append(parse(texto[i:j]))
    return nodo


def tabla_libs(carpeta, tipo):
    """{apodo: ruta} de sym-lib-table (tipo 'sym') o fp-lib-table ('fp') del proyecto."""
    archivo = Path(carpeta) / f"{tipo}-lib-table"
    libs = {}
    if archivo.is_file():
        for lib in hijos(parse(leer(archivo)), "lib"):
            uri = val(lib, "uri").replace("${KIPRJMOD}", str(carpeta).replace("\\", "/"))
            libs[val(lib, "name")] = Path(uri)
    return libs


def ruta_simbolos(apodo, carpeta=None):
    libs = tabla_libs(carpeta, "sym") if carpeta else {}
    return libs.get(apodo, SIMBOLOS / f"{apodo}.kicad_sym")


def ruta_huella(fpid, carpeta=None):
    """Ruta del .kicad_mod de «Lib:Nombre», en las librerías del proyecto o en las oficiales."""
    if ":" not in fpid:
        return None
    apodo, nombre = fpid.split(":", 1)
    libs = tabla_libs(carpeta, "fp") if carpeta else {}
    return libs.get(apodo, HUELLAS / f"{apodo}.pretty") / f"{nombre}.kicad_mod"


# ------------------------------------------------------------------ copia de trabajo y kicad-cli

def _ignorar(con_3d):
    patrones = ["*-backups", ".mcp-backups", "*.lck", "~*", "__pycache__"] + ([] if con_3d else ["3d"])
    return shutil.ignore_patterns(*patrones)


@contextlib.contextmanager
def copia_trabajo(carpeta, con_3d=False):
    """Copia temporal del proyecto con `../libraries` al lado; devuelve la carpeta copiada."""
    carpeta = Path(carpeta).resolve()
    tmp = Path(tempfile.mkdtemp(prefix="kicad_"))
    try:
        destino = tmp / carpeta.name
        shutil.copytree(carpeta, destino, ignore=_ignorar(con_3d))
        libs = carpeta.parent / "libraries"
        if libs.is_dir():
            shutil.copytree(libs, tmp / "libraries", ignore=_ignorar(con_3d))
        yield destino
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def cli(*argumentos, comprobar=None):
    """Lanza kicad-cli. `comprobar`: archivo que debe existir al terminar."""
    if not KICAD_CLI.is_file():
        raise Fallo(f"no se encuentra kicad-cli en {KICAD_CLI} (variable KICAD_CLI)")
    r = subprocess.run([str(KICAD_CLI), *map(str, argumentos)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0 or (comprobar and not Path(comprobar).exists()):
        cola = (r.stderr.strip() or r.stdout.strip()).splitlines()[-3:]
        raise Fallo(f"kicad-cli {argumentos[0]} {argumentos[1]} falló ({r.returncode}): " + " | ".join(cola))
    return r.stdout


def con_python_kicad(archivo, modulo="pcbnew"):
    """Si este Python no tiene `modulo` (pcbnew o wx), relanza el script con el de KiCad y termina."""
    try:
        __import__(modulo)
        return
    except ImportError:
        pass
    if not KICAD_PY.is_file():
        raise Fallo(f"no se encuentra el Python de KiCad en {KICAD_PY} (variable KICAD_PYTHON)")
    if os.environ.get("KICAD_RELANZADO"):
        raise Fallo(f"el Python de KiCad no puede importar {modulo}")
    r = subprocess.run([str(KICAD_PY), "-I", str(archivo), *sys.argv[1:]],
                       env={**os.environ, "KICAD_RELANZADO": "1"})
    if r.returncode not in (0, 1, 2):  # pcbnew o wx se han caído sin decir nada
        print(f"ERROR: el Python de KiCad ha terminado con el código {r.returncode} sin acabar {Path(archivo).name}",
              file=sys.stderr)
        sys.exit(2)
    sys.exit(r.returncode)


# ------------------------------------------------------------------ netlist

def leer_netlist(ruta):
    """Netlist kicadsexpr → {'comps': {ref: {...}}, 'redes': {nombre: {(ref, pin)}}}."""
    raiz = parse(leer(ruta))
    comps = {}
    for c in hijos(uno(raiz, "components", []), "comp"):
        campos = {val(f, "name"): (f[2] if len(f) > 2 and isinstance(f[2], str) else "")
                  for f in hijos(uno(c, "fields", []), "field")}
        props = {val(p, "name"): val(p, "value") for p in hijos(c, "property")}
        sp = uno(c, "sheetpath", [])
        comps[val(c, "ref")] = {
            "value": val(c, "value"), "footprint": val(c, "footprint"), "campos": campos, "props": props,
            "datasheet": val(c, "datasheet"), "description": val(c, "description"),
            "nombres": val(sp, "names"), "ruta": val(sp, "tstamps"), "uuid": val(c, "tstamps"),
        }
    redes = {}
    for n in hijos(uno(raiz, "nets", []), "net"):
        redes[val(n, "name")] = {(val(nd, "ref"), val(nd, "pin")) for nd in hijos(n, "node")}
    return {"comps": comps, "redes": redes}


def exportar_netlist(carpeta, nombre, destino):
    """Exporta la netlist del proyecto (sobre una copia) a `destino`."""
    with copia_trabajo(carpeta) as copia:
        salida = copia / "_netlist.net"
        cli("sch", "export", "netlist", "--format", "kicadsexpr", "-o", salida,
            copia / f"{nombre}.kicad_sch", comprobar=salida)
        Path(destino).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(salida, destino)
    return leer_netlist(destino)


def comparar_netlists(a, b, hoja=None):
    """Diferencias entre dos netlists (piezas, huella, valor y nodos de cada red)."""
    dif = []

    def de_hoja(net):
        if not hoja:
            return set(net["comps"])
        return {r for r, c in net["comps"].items() if c["nombres"].strip("/").lower() == hoja.lower()}

    ra, rb = de_hoja(a), de_hoja(b)
    dif += [f"{r}: solo en A" for r in sorted(ra - rb)] + [f"{r}: solo en B" for r in sorted(rb - ra)]
    for r in sorted(ra & rb):
        ca, cb = a["comps"][r], b["comps"][r]
        for k in ("value", "footprint"):
            if ca[k] != cb[k]:
                dif.append(f"{r}: {k} «{ca[k]}» ≠ «{cb[k]}»")
        for k in sorted(set(ca["campos"]) | set(cb["campos"])):
            if ca["campos"].get(k, "") != cb["campos"].get(k, ""):
                dif.append(f"{r}: campo {k} «{ca['campos'].get(k, '')}» ≠ «{cb['campos'].get(k, '')}»")

    def nodos(net, refs):
        return {(ref, pin): nombre for nombre, ns in net["redes"].items() for ref, pin in ns if ref in refs}

    na, nb = nodos(a, ra & rb), nodos(b, ra & rb)
    for k in sorted(set(na) | set(nb)):
        if na.get(k) != nb.get(k):
            dif.append(f"{k[0]}.{k[1]}: red «{na.get(k, '—')}» ≠ «{nb.get(k, '—')}»")
    return dif


def cargar_json(ruta):
    return json.loads(Path(ruta).read_text(encoding="utf-8"))
