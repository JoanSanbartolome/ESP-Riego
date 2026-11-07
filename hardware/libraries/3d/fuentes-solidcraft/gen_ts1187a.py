"""Genera ts1187a.json (SPEC-0021): pulsador XKB TS-1187A-B-A-B, 5,1 x 5,1 mm, altura 1,5 mm.
Regenerar: python gen_ts1187a.py && solidcraft-cli run ts1187a.json --out ../SW_Push_1P1T_XKB_TS-1187A.step
Cotas del PDF (datasheets/TS-1187A-B-A-B.pdf, hoja unica): cuerpo 5,1 +-0,05; ancho con terminales 6,5 +-0,25;
terminal 0,5 de ancho; H (codigo B... A = 1,5); tecla (keystake) diametro 2,0; recorrido 0,2.
Supuestos: cuerpo hasta z = 0,9 (cota 0,9 del alzado), tecla de 0,9 a 1,5 (= H); terminales de 0,3 de grosor;
contorno de la tapa y terminales tomados del dibujo Fab de la huella oficial (y de los pads: +-3 / +-1,875).
Ejes: mm, Z = 0 en la cara superior de la placa, modelo (x, y) = huella (x, -y); en KiCad offset 0, rotacion 0 y escala 1.
"""
import json
BLACK = "#202020"; METAL = "#c8c8c8"; GREY = "#a0a0a0"


def box(name, x0, x1, y0, y1, z0, z1, op="new", targets=None):
    p = {"length": round(x1 - x0, 6), "width": round(y1 - y0, 6), "height": round(z1 - z0, 6),
         "corner": [round(x0, 6), round(y0, 6), round(z0, 6)], "operation": op}
    if op == "new":
        p["body_name"] = name
    if targets:
        p["targets"] = targets
    return {"command": "solid.box", "params": p}


def cyl(name, x, y, z0, h, d, op="new", targets=None):
    p = {"diameter": d, "height": h, "base": [x, y, z0], "operation": op}
    if op == "new":
        p["body_name"] = name
    if targets:
        p["targets"] = targets
    return {"command": "solid.cylinder", "params": p}


def color(bodies, c):
    return {"command": "appearance.assign", "params": {"bodies": bodies, "color": c}}


# tapa: contorno del dibujo Fab (simetrico, asi que x,y de huella = x,y de modelo)
cover = [(-1.25, -2.55), (1.25, -2.55), (1.25, -1.975), (1.575, -1.975), (1.975, -1.575), (1.975, -1.25),
         (2.55, -1.25), (2.55, 1.25), (1.975, 1.25), (1.975, 1.575), (1.575, 1.975), (1.25, 1.975),
         (1.25, 2.55), (-1.25, 2.55), (-1.25, 1.975), (-1.575, 1.975), (-1.975, 1.575), (-1.975, 1.25),
         (-2.55, 1.25), (-2.55, -1.25), (-1.975, -1.25), (-1.975, -1.575), (-1.575, -1.975), (-1.25, -1.975)]
Z_BODY = 0.9
s = [{"command": "sketch.create", "params": {"plane": "XY", "offset": 0.15, "name": "tapa"}},
     {"command": "sketch.line", "params": {"points": [list(p) for p in cover], "closed": True}},
     {"command": "sketch.finish", "params": {}},
     {"command": "solid.extrude", "params": {"distance": Z_BODY - 0.15, "operation": "new", "body_name": "SW_tapa"}}]
terms = []
for i, (sx, sy) in enumerate(((-1, 1), (1, 1), (-1, -1), (1, -1)), 1):
    xa, xb = (1.7, 3.25) if sx > 0 else (-3.25, -1.7)
    yc = 1.85 * sy
    nm = f"SW_terminal{i}"
    s.append(box(nm, xa, xb, yc - 0.25, yc + 0.25, 0.0, 0.3))
    terms.append(nm)
s.append(cyl("SW_tecla", 0, 0, Z_BODY, 1.5 - Z_BODY, 2.0))
# marca de pin 1: hendidura de 0,4 mm en la esquina de la tapa junto al pad 1 (huella (-3,-1,875) = modelo (-3,+1,875))
s.append(cyl("tmp", -1.55, 1.55, Z_BODY - 0.05, 0.05, 0.4, op="cut", targets=["SW_tapa"]))
s += [color(["SW_tapa"] + terms, METAL), color(["SW_tecla"], BLACK),
      {"command": "appearance.assign", "params": {"faces": [[-1.55, 1.55, Z_BODY - 0.05]], "body": "SW_tapa", "color": "#c03030"}}]
json.dump(s, open("ts1187a.json", "w"), indent=1)
