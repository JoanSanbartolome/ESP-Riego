"""Puntos `[auto]` de las checklists de esquema, layout y librerías, sobre un proyecto KiCad.

Uso:
    python herramientas/kicad/comprobar.py hardware/v2
    python herramientas/kicad/comprobar.py hardware/v2 --punto esquema.campos
    python herramientas/kicad/comprobar.py hardware/v2 --json

Una línea por punto: OK, FALLA, N/A (no hay con qué comprobarlo todavía) o ERROR, con el número
de incidencias y la primera. --punto enseña todas las de uno. Busca al lado del proyecto
`../libraries`, `../componentes` (fichas y `campos-<hoja>.csv`), la tabla de restricciones
(`restricciones.csv` en la carpeta del proyecto o `../../docs/diseno/restricciones.csv`) y el
`.gitattributes` del repositorio. Solo lee archivos; no lanza kicad-cli. Sale con 1 si algún
punto falla. `herramientas/verificar.py` lo llama con `para_verificar()` y añade las líneas a su informe.

Puntos (checklist · lo que se comprueba):
  esquema.hojas        hojas por bloque: todo cuelga de la raíz, sin piezas en ella ni hojas huérfanas
  esquema.campos       Value, Footprint, LCSC Part#, MPN, Datasheet y Description en lo que va al BOM
  esquema.huellas      la huella asignada existe (librerías del proyecto u oficiales de KiCad 10)
  esquema.vias         las huellas con vías cumplen FAB-02 (taladro ≥ 0,3, corona ≥ 0,6)
  esquema.dnp          DNP igual en la hoja, en la tabla de campos y en la PCB
  layout.zonas         todas las zonas de cobre están rellenadas
  layout.incrustados   la PCB no lleva archivos incrustados
  layout.salida        `outputdirectory` vacío o dentro de fabricacion/
  layout.restricciones anchos, separaciones y vías de la tabla de restricciones (restricciones.py)
  layout.smd_cara      ningún componente SMD en la cara inferior
  layout.3d            todas las huellas montadas tienen modelo 3D y el archivo existe
  librerias.formato    librerías en formato nativo, sin JSON de EasyEDA ni formatos antiguos
  librerias.rutas      tablas de librerías y modelos 3D con ${KIPRJMOD}, sin rutas absolutas
  librerias.campos     los símbolos propios llevan los seis campos
  librerias.patio      las huellas propias tienen patio con margen ≥ 0,1 mm
  librerias.serigrafia las huellas propias no tienen serigrafía sobre los pads
  librerias.3d         modelo 3D de cada huella usada o propia: existe y es STEP
  librerias.gitattributes  las extensiones de los modelos 3D están como `binary`
  librerias.fichas     cada código LCSC del BOM tiene ficha con tipo, fecha y datasheet
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import (Fallo, emitir, es_pieza, hijos, hojas, leer, parse, principal, proyecto, ruta_huella,  # noqa: E402
                    simbolos_hoja, tabla_libs, trozos, uno, val)
import campos as _campos  # noqa: E402
import huella as _huella  # noqa: E402
import restricciones as _restricciones  # noqa: E402

SEIS = ("Value", "Footprint", "LCSC Part#", "MPN", "Datasheet", "Description")
ANTIGUOS = (".json", ".lib", ".dcm", ".mod", ".lbr", ".epl", ".elibz", ".wrl")
MODELOS_3D = ("step", "stp", "wrl", "igs", "iges")
NA = "N/A"


class Proyecto:
    """Lo que leen los puntos, cargado una sola vez."""

    def __init__(self, ruta):
        self.carpeta, self.nombre = proyecto(ruta)
        self.sch = self.carpeta / f"{self.nombre}.kicad_sch"
        self.pcb = self.carpeta / f"{self.nombre}.kicad_pcb"
        self.libs = self.carpeta.parent / "libraries"
        self.componentes = self.carpeta.parent / "componentes"
        self._hojas = self._piezas = self._pcb = self._huellas = None

    def hojas(self):
        if self._hojas is None:
            self._hojas = hojas(self.sch) if self.sch.is_file() else []
        return self._hojas

    def piezas(self):
        """[(archivo de hoja, símbolo)] de las piezas reales, cada archivo una vez."""
        if self._piezas is None:
            self._piezas, vistos = [], set()
            for h in self.hojas():
                if h["archivo"].is_file() and h["archivo"] not in vistos:
                    vistos.add(h["archivo"])
                    self._piezas += [(h["archivo"], s) for s in simbolos_hoja(leer(h["archivo"])) if es_pieza(s)]
        return self._piezas

    def huellas_pcb(self):
        """Huellas de la PCB: dict con ref, fpid, capa, attr, modelos y dnp."""
        if self._pcb is None:
            self._pcb = []
            if self.pcb.is_file():
                texto = leer(self.pcb)
                self.texto_pcb = texto
                for nombre, i, j in trozos(texto):
                    if nombre == "footprint":
                        n = parse(texto[i:j])
                        props = {p[1]: p[2] for p in hijos(n, "property") if len(p) > 2 and isinstance(p[2], str)}
                        attr = uno(n, "attr", ["attr"])[1:]
                        self._pcb.append({"ref": props.get("Reference", "?"), "fpid": n[1], "capa": val(n, "layer"),
                                          "attr": attr, "modelos": [m[1] for m in hijos(n, "model")]})
        return self._pcb

    def analisis(self, fpid):
        """Cotas de una huella «Lib:Nombre» (None si no existe)."""
        if self._huellas is None:
            self._huellas = {}
        if fpid not in self._huellas:
            archivo = ruta_huella(fpid, self.carpeta)
            self._huellas[fpid] = _huella.analizar(archivo, self.carpeta) if archivo and archivo.is_file() else None
        return self._huellas[fpid]

    def huellas_propias(self):
        return sorted(f"{apodo}:{p.stem}" for apodo, carpeta in tabla_libs(self.carpeta, "fp").items()
                      if carpeta.is_dir() for p in carpeta.glob("*.kicad_mod"))

    def huellas_usadas(self):
        return sorted({s["props"].get("Footprint", "") for _, s in self.piezas() if s["props"].get("Footprint")})


# ------------------------------------------------------------------ esquema

def esquema_hojas(p):
    if not p.sch.is_file():
        return NA, ["no hay esquema"]
    hs, malas = p.hojas(), []
    if len(hs) < 2:
        malas.append("la raíz no tiene hojas jerárquicas")
    malas += [f"{h['nombre']}: falta {h['archivo'].name}" for h in hs if not h["archivo"].is_file()]
    usados = {h["archivo"] for h in hs}
    malas += [f"{f.name}: hoja huérfana (no cuelga de la raíz)" for f in sorted(p.carpeta.glob("*.kicad_sch")) if f.resolve() not in usados]
    malas += [f"{s['ref']}: pieza en la hoja raíz" for a, s in p.piezas() if a == p.sch.resolve()]
    return ("FALLA" if malas else "OK"), malas or [f"{len(hs) - 1} hojas bajo la raíz"]


def esquema_campos(p):
    malas = [f"{s['ref']} ({a.name}): falta {c}" for a, s in p.piezas() if s["in_bom"]
             for c in SEIS if _campos.vacio(c, s["props"].get(c, ""))]
    malas += [f"{s['ref']} ({a.name}): falta {c}" for a, s in p.piezas() if not s["in_bom"]
              for c in _campos.SIN_PIEZA if _campos.vacio(c, s["props"].get(c, ""))]
    return ("FALLA" if malas else "OK"), malas or [f"{len(p.piezas())} piezas"]


def esquema_huellas(p):
    malas = [f"{s['ref']}: no existe la huella «{s['props'].get('Footprint', '')}»" for _, s in p.piezas()
             if s["on_board"] and p.analisis(s["props"].get("Footprint", "")) is None]
    return ("FALLA" if malas else "OK"), malas or [f"{len(p.huellas_usadas())} huellas distintas"]


def esquema_vias(p):
    con_vias = [(f, p.analisis(f)) for f in p.huellas_usadas() if p.analisis(f) and p.analisis(f)["n_vias"]]
    malas = [f"{f}: vías {a['vias_tipos']} por debajo de 0,3/0,6" for f, a in con_vias if not a["vias_fab02"]]
    return ("FALLA" if malas else "OK"), malas or [f"{len(con_vias)} huellas con vías"]


def esquema_dnp(p):
    archivos = sorted({a for a, _ in p.piezas()})
    tablas = _campos.tablas_por_defecto(archivos)
    malas = []
    en_pcb = {h["ref"]: "dnp" in h["attr"] for h in p.huellas_pcb()}
    for a, s in p.piezas():
        fila = tablas.get(a.name, {}).get(s["ref"])
        if fila and fila.get("DNP") is not None and fila["DNP"] != s["dnp"]:
            malas.append(f"{s['ref']}: DNP {'sí' if s['dnp'] else 'no'} en la hoja y {'sí' if fila['DNP'] else 'no'} en la tabla")
        if s["ref"] in en_pcb and en_pcb[s["ref"]] != s["dnp"]:
            malas.append(f"{s['ref']}: DNP {'sí' if s['dnp'] else 'no'} en la hoja y {'sí' if en_pcb[s['ref']] else 'no'} en la PCB")
        texto = s["props"].get("Value", "") + " " + s["props"].get("Description", "")
        if not s["dnp"] and re.search(r"\bDNP\b|no montar|no se monta|sin montar", texto, re.I):
            malas.append(f"{s['ref']}: el texto dice que no se monta y no está marcado DNP")
    dnp = [s["ref"] for _, s in p.piezas() if s["dnp"]]
    return ("FALLA" if malas else "OK"), malas or [f"{len(dnp)} DNP ({_campos.rangos(dnp) or '—'}); tablas de campos: {len(tablas)}"]


# ------------------------------------------------------------------ layout

def _zonas(p):
    p.huellas_pcb()
    return [parse(p.texto_pcb[i:j]) for n, i, j in trozos(p.texto_pcb) if n == "zone"]


def layout_zonas(p):
    if not p.pcb.is_file():
        return NA, ["no hay PCB"]
    cobre = [z for z in _zonas(p) if not uno(z, "keepout")]
    malas = [f"zona de {val(z, 'net_name') or val(z, 'net') or 'sin red'} en {val(z, 'layer') or ' '.join(uno(z, 'layers', ['', '?'])[1:])}: sin rellenar"
             for z in cobre if not hijos(z, "filled_polygon")]
    if not cobre:
        return NA, ["la PCB no tiene zonas de cobre todavía"]
    return ("FALLA" if malas else "OK"), malas or [f"{len(cobre)} zonas rellenadas"]


def layout_incrustados(p):
    if not p.pcb.is_file():
        return NA, ["no hay PCB"]
    p.huellas_pcb()
    malas = []
    for n, i, j in trozos(p.texto_pcb):
        if n == "embedded_files":
            malas += [f"archivo incrustado: {val(f, 'name')}" for f in hijos(parse(p.texto_pcb[i:j]), "file")]
    return ("FALLA" if malas else "OK"), malas or ["sin archivos incrustados"]


def layout_salida(p):
    if not p.pcb.is_file():
        return NA, ["no hay PCB"]
    p.huellas_pcb()
    m = re.search(r'\(outputdirectory "((?:\\.|[^"\\])*)"\)', p.texto_pcb)
    carpeta = m.group(1) if m else ""
    bien = not carpeta or "fabricacion/" in carpeta.replace("\\", "/") + "/"
    return ("OK" if bien else "FALLA"), [f"outputdirectory «{carpeta}»"]


def tabla_restricciones(p):
    for candidata in (p.carpeta / "restricciones.csv", p.carpeta.parent.parent / "docs" / "diseno" / "restricciones.csv"):
        if candidata.is_file():
            return candidata
    return None


def layout_restricciones(p):
    tabla = tabla_restricciones(p)
    if not p.pcb.is_file() or tabla is None:
        return NA, ["no hay tabla de restricciones (restricciones.csv) todavía"]
    r = _restricciones.comprobar(p.pcb, _restricciones.leer_tabla(tabla), p.carpeta, p.nombre)
    malas = [f"{f['red']}: {'; '.join(f['motivos'])}" for f in r["filas"] if f["estado"] == "FALLA"]
    if r["vias_bajo_fab02"]:
        malas.append(f"{r['vias_bajo_fab02']} vías por debajo de FAB-02")
    if not malas and r["sin_datos"] == len(r["filas"]):
        return NA, [f"{tabla.name}: ninguna de las {len(r['filas'])} filas tiene pistas todavía"]
    return ("FALLA" if malas else "OK"), malas or [f"{tabla.name}: {len(r['filas'])} filas, {r['sin_datos']} sin datos"]


def layout_smd_cara(p):
    if not p.pcb.is_file():
        return NA, ["no hay PCB"]
    malas = [f"{h['ref']}: SMD en la cara inferior" for h in p.huellas_pcb() if "smd" in h["attr"] and h["capa"] == "B.Cu"]
    return ("FALLA" if malas else "OK"), malas or [f"{sum('smd' in h['attr'] for h in p.huellas_pcb())} SMD, todos arriba"]


def _montada(h):
    return not ({"board_only", "exclude_from_bom"} & set(h["attr"]))


def layout_3d(p):
    if not p.pcb.is_file():
        return NA, ["no hay PCB"]
    malas = []
    for h in p.huellas_pcb():
        if not _montada(h):
            continue
        if not h["modelos"]:
            malas.append(f"{h['ref']}: sin modelo 3D")
        malas += [f"{h['ref']}: no existe {m}" for m in h["modelos"] if not _huella.resolver_modelo(m, p.carpeta).is_file()]
    return ("FALLA" if malas else "OK"), malas or [f"{sum(_montada(h) for h in p.huellas_pcb())} huellas montadas con modelo"]


# ------------------------------------------------------------------ librerías

def librerias_formato(p):
    malas = []
    for tipo in ("sym", "fp"):
        archivo = p.carpeta / f"{tipo}-lib-table"
        if archivo.is_file():
            malas += [f"{tipo}-lib-table: {val(lib, 'name')} es de tipo {val(lib, 'type')}"
                      for lib in hijos(parse(leer(archivo)), "lib") if val(lib, "type") != "KiCad"]
    if p.libs.is_dir():
        for f in sorted(p.libs.rglob("*")):
            if f.is_file() and f.suffix.lower() in ANTIGUOS and "3d" not in f.relative_to(p.libs).parts[:1]:
                malas.append(f"{f.relative_to(p.libs).as_posix()}: formato no nativo")
            elif f.is_file() and f.parent.suffix == ".pretty" and f.suffix != ".kicad_mod":
                malas.append(f"{f.relative_to(p.libs).as_posix()}: no es .kicad_mod")
            elif f.suffix == ".kicad_sym" and not leer(f).lstrip().startswith("(kicad_symbol_lib"):
                malas.append(f"{f.name}: no es una librería de símbolos de KiCad")
    return ("FALLA" if malas else "OK"), malas or ["librerías en formato nativo"]


def _absoluta(ruta):
    return bool(re.match(r"^([A-Za-z]:[\\/]|/|\\\\)", ruta))


def librerias_rutas(p):
    malas, n = [], 0
    for tipo in ("sym", "fp"):
        archivo = p.carpeta / f"{tipo}-lib-table"
        if archivo.is_file():
            for lib in hijos(parse(leer(archivo)), "lib"):
                n += 1
                if not val(lib, "uri").startswith("${KIPRJMOD}"):
                    malas.append(f"{tipo}-lib-table: {val(lib, 'name')} → {val(lib, 'uri')}")
    malas += [f"{h['ref']} (PCB): modelo con ruta absoluta {m}" for h in p.huellas_pcb() for m in h["modelos"] if _absoluta(m)]
    for fpid in p.huellas_propias():
        malas += [f"{fpid}: modelo con ruta absoluta {m['ruta']}" for m in p.analisis(fpid)["modelos"] if m["absoluta"]]
    return ("FALLA" if malas else "OK"), malas or [f"{n} librerías en las tablas, todas con ${{KIPRJMOD}}"]


def librerias_campos(p):
    malas, n = [], 0
    for apodo, archivo in tabla_libs(p.carpeta, "sym").items():
        if not archivo.is_file():
            malas.append(f"{apodo}: no existe {archivo.name}")
            continue
        texto = leer(archivo)
        for nombre, i, j in trozos(texto):
            if nombre != "symbol":
                continue
            nodo = parse(texto[i:j])
            props = {c[1]: c[2] for c in hijos(nodo, "property") if len(c) > 2 and isinstance(c[2], str)}
            n += 1
            faltan = [c for c in SEIS if _campos.vacio(c, props.get(c, ""))]
            if faltan:
                malas.append(f"{apodo}:{nodo[1]}: falta {', '.join(faltan)}")
    return ("FALLA" if malas else "OK"), malas or [f"{n} símbolos propios"]


def librerias_patio(p):
    malas = []
    for fpid in p.huellas_propias():
        a = p.analisis(fpid)
        if not a["patio"]:
            malas.append(f"{fpid}: sin patio")
        elif a["patio_margen"] is not None and a["patio_margen"] < _huella.MARGEN_PATIO - 1e-9:
            malas.append(f"{fpid}: margen del patio {a['patio_margen']:g} mm")
    return ("FALLA" if malas else "OK"), malas or [f"{len(p.huellas_propias())} huellas propias"]


def librerias_serigrafia(p):
    malas = [f"{fpid}: {p.analisis(fpid)['serigrafia_sobre_pads']} gráficos de serigrafía sobre pads"
             for fpid in p.huellas_propias() if p.analisis(fpid)["serigrafia_sobre_pads"]]
    return ("FALLA" if malas else "OK"), malas or [f"{len(p.huellas_propias())} huellas propias"]


def librerias_3d(p):
    malas, fuera_bom = [], {s["props"].get("Footprint") for _, s in p.piezas() if not s["in_bom"]}
    en_bom = {s["props"].get("Footprint") for _, s in p.piezas() if s["in_bom"]}
    todas = sorted(set(p.huellas_propias()) | set(p.huellas_usadas()))
    for fpid in todas:
        a = p.analisis(fpid)
        if a is None:
            continue
        if not a["modelos"]:
            if fpid in en_bom or fpid not in fuera_bom and fpid not in p.huellas_usadas():
                malas.append(f"{fpid}: sin modelo 3D")
            continue
        for m in a["modelos"]:
            if not m["existe"]:
                malas.append(f"{fpid}: no existe {m['ruta']}")
            elif m["ext"].lower() not in (".step", ".stp"):
                malas.append(f"{fpid}: el modelo no es STEP ({m['ext']})")
    return ("FALLA" if malas else "OK"), malas or [f"{len(todas)} huellas usadas o propias"]


def librerias_gitattributes(p):
    raiz = next((c for c in p.carpeta.parents if (c / ".gitattributes").is_file()), None)
    if raiz is None or not (p.libs / "3d").is_dir():
        return NA, ["no hay .gitattributes o carpeta libraries/3d"]
    binarias = set(re.findall(r"^\*\.(\S+)\s+.*\bbinary\b", (raiz / ".gitattributes").read_text(encoding="utf-8"), re.M))
    usadas = {f.suffix[1:] for f in (p.libs / "3d").rglob("*") if f.is_file() and f.suffix[1:].lower() in MODELOS_3D}
    malas = [f"*.{ext} no está como binary en .gitattributes" for ext in sorted(usadas - binarias)]
    for ext in MODELOS_3D:
        malas += [f"*.{v} no está como binary en .gitattributes" for v in (ext, ext.upper())
                  if (ext in binarias or ext.upper() in binarias) and v not in binarias]
    return ("FALLA" if malas else "OK"), sorted(set(malas)) or [f"extensiones en uso: {', '.join(sorted(usadas)) or '—'}"]


def librerias_fichas(p):
    if not p.componentes.is_dir():
        return NA, ["no hay carpeta ../componentes"]
    fichas = {f.name: f.read_text(encoding="utf-8", errors="replace") for f in p.componentes.glob("*.md")}
    codigos = {}
    for _, s in p.piezas():
        if s["in_bom"] and s["props"].get("LCSC Part#", "").strip():
            codigos.setdefault(s["props"]["LCSC Part#"].strip(), []).append(s["ref"])
    malas = []
    for codigo, refs in sorted(codigos.items()):
        patron = re.compile(r"(?<![A-Za-z0-9])" + re.escape(codigo) + r"(?!\d)")
        mias = [t for t in fichas.values() if patron.search(t)]
        if not mias:
            malas.append(f"{codigo} ({_campos.rangos(refs)}): sin ficha en componentes/")
            continue
        faltan = [que for que, pat in (("tipo Basic/Extended", r"basic|extended"), ("fecha", r"20\d\d-\d\d-\d\d"),
                                       ("datasheet", r"datasheet")) if not any(re.search(pat, t, re.I) for t in mias)]
        if faltan:
            malas.append(f"{codigo} ({_campos.rangos(refs)}): a su ficha le falta {', '.join(faltan)}")
    return ("FALLA" if malas else "OK"), malas or [f"{len(codigos)} códigos LCSC con ficha"]


PUNTOS = [
    ("esquema.hojas", esquema_hojas), ("esquema.campos", esquema_campos), ("esquema.huellas", esquema_huellas),
    ("esquema.vias", esquema_vias), ("esquema.dnp", esquema_dnp),
    ("layout.zonas", layout_zonas), ("layout.incrustados", layout_incrustados), ("layout.salida", layout_salida),
    ("layout.restricciones", layout_restricciones), ("layout.smd_cara", layout_smd_cara), ("layout.3d", layout_3d),
    ("librerias.formato", librerias_formato), ("librerias.rutas", librerias_rutas), ("librerias.campos", librerias_campos),
    ("librerias.patio", librerias_patio), ("librerias.serigrafia", librerias_serigrafia), ("librerias.3d", librerias_3d),
    ("librerias.gitattributes", librerias_gitattributes), ("librerias.fichas", librerias_fichas),
]


def resumen(ruta, solo=None):
    """Resultado de los puntos: {'puntos': [...], 'lineas': [...], 'fallan': n}. No lanza excepciones."""
    try:
        p = Proyecto(ruta)
    except Exception as e:  # el informe de verificar.py no debe caerse por esto
        return {"puntos": [], "lineas": [f"Puntos [auto]: no se pudieron comprobar ({e})"], "fallan": 0}
    puntos = []
    for clave, funcion in PUNTOS:
        if solo and clave != solo:
            continue
        try:
            estado, detalle = funcion(p)
        except Exception as e:
            estado, detalle = "ERROR", [f"{type(e).__name__}: {e}"]
        puntos.append({"punto": clave, "estado": estado, "n": len(detalle) if estado == "FALLA" else 0, "detalle": detalle})
    cuenta = {e: sum(x["estado"] == e for x in puntos) for e in ("OK", "FALLA", NA, "ERROR")}
    lineas = [f"Puntos [auto] {len(puntos):>3}  (OK {cuenta['OK']}, fallan {cuenta['FALLA']}, no aplican {cuenta[NA]}"
              + (f", error {cuenta['ERROR']}" if cuenta["ERROR"] else "") + ")"]
    for x in puntos:
        primero = x["detalle"][0] if x["detalle"] else ""
        cuantas = f"{x['n']} · " if x["estado"] == "FALLA" else ""
        lineas.append(f"  {x['estado']:<5} {x['punto']:<24} {cuantas}{primero}"[:150])
    return {"puntos": puntos, "lineas": lineas, "fallan": cuenta["FALLA"] + cuenta["ERROR"]}


def para_verificar(carpeta):
    """Lo que `herramientas/verificar.py` añade a su resumen: no cambia su resultado ni puede hacerlo fallar."""
    r = resumen(carpeta)
    return {"fallan": r["fallan"], "puntos": {x["punto"]: x["estado"] for x in r["puntos"]}, "lineas": r["lineas"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("proyecto", help="carpeta del proyecto o .kicad_pro")
    ap.add_argument("--punto", help="enseña todas las incidencias de un punto")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--detalle", metavar="ARCHIVO", help="guarda todas las incidencias de todos los puntos")
    args = ap.parse_args()
    if args.punto and args.punto not in dict(PUNTOS):
        raise Fallo(f"no existe el punto {args.punto}: {', '.join(k for k, _ in PUNTOS)}")
    r = resumen(args.proyecto, args.punto)
    if args.json:
        print(json.dumps({"puntos": r["puntos"], "fallan": r["fallan"]}, ensure_ascii=False))
    elif args.punto:
        x = r["puntos"][0]
        emitir([f"{x['punto']}: {x['estado']} ({len(x['detalle'])} líneas)"] + x["detalle"], detalle=args.detalle)
    else:
        if args.detalle:
            Path(args.detalle).write_text("\n".join(f"{x['punto']}\t{x['estado']}\t{d}" for x in r["puntos"] for d in x["detalle"]) + "\n",
                                          encoding="utf-8")
        emitir(r["lineas"], pista="--punto NOMBRE")
    return 1 if r["fallan"] else 0


if __name__ == "__main__":
    principal(main)
