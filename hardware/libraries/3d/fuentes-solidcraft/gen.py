import json
BLACK="#202020"; METAL="#c8c8c8"; GREEN="#1f8a3c"
def box(name,x0,x1,y0,y1,z0,z1,op="new",targets=None):
    p={"length":round(x1-x0,6),"width":round(y1-y0,6),"height":round(z1-z0,6),"corner":[round(x0,6),round(y0,6),round(z0,6)],"operation":op}
    if op=="new": p["body_name"]=name
    if targets: p["targets"]=targets
    return {"command":"solid.box","params":p}
def cyl(name,x,y,z0,h,d,op="new",targets=None):
    p={"diameter":d,"height":h,"base":[x,y,z0],"operation":op}
    if op=="new": p["body_name"]=name
    if targets: p["targets"]=targets
    return {"command":"solid.cylinder","params":p}
def color(bodies,c): return {"command":"appearance.assign","params":{"bodies":bodies,"color":c}}
def save(fn,steps): json.dump(steps,open(fn,"w"),indent=1)

# ---------- SHT4x ----------
s=[box("SHT4x_cuerpo",-0.75,0.75,-0.75,0.75,0,0.54)]
# huella (x,y)->modelo (x,-y)
pads={1:(-0.7,0.4),2:(-0.7,-0.4),3:(0.7,-0.4),4:(0.7,0.4)}
pb=[]
for n,(x,y) in pads.items():
    x0,x1=(-0.75,-0.45) if x<0 else (0.35,0.75)
    s.append(box("tmp",x0,x1,y-0.15,y+0.15,0,0.2,op="cut",targets=["SHT4x_cuerpo"]))
for n,(x,y) in pads.items():
    x0,x1=(-0.75,-0.45) if x<0 else (0.35,0.75)
    s.append(box(f"SHT4x_pad{n}",x0,x1,y-0.15,y+0.15,0,0.2)); pb.append(f"SHT4x_pad{n}")
s.append(cyl("tmp",0,0,0.39,0.15,0.6,op="cut",targets=["SHT4x_cuerpo"]))
s.append(cyl("tmp",-0.5,0.55,0.49,0.05,0.2,op="cut",targets=["SHT4x_cuerpo"]))  # marca pin 1 (huella pad1 = (-0.7,-0.4) -> modelo (-0.7,+0.4))
s+= [color(["SHT4x_cuerpo"],BLACK),color(pb,METAL),{"command":"appearance.assign","params":{"faces":[[-0.5,0.55,0.49]],"body":"SHT4x_cuerpo","color":"#a0a0a0"}}]
save("sht4x.json",s)

# ---------- PG-TDSO-14 ----------
s=[box("TDSO_cuerpo",-1.95,1.95,-4.325,4.325,0.05,1.15)]
s.append(box("TDSO_slug",-1.325,1.325,-3.2,3.2,0.0,0.05))
leads=[]
for n in range(1,15):
    if n<=7: x=-2.6; y=3.81-1.27*(n-1); sg=-1
    else: x=2.6; y=-3.81+1.27*(n-8); sg=1
    nm=f"TDSO_pin{n}"; leads.append(nm)
    def X(a,b): # a<b in |x|, mirrored by side
        return (a,b) if sg>0 else (-b,-a)
    # hombro dentro del cuerpo hasta |x|=2.5 a media altura; tramo vertical; pie hasta |x|=3.0
    xa,xb=X(1.95,2.5); s.append(box(nm,xa,xb,y-0.2,y+0.2,0.45,0.65))
    xa,xb=X(2.3,2.5); s.append(box("t",xa,xb,y-0.2,y+0.2,0.0,0.65,op="join",targets=[nm]))
    xa,xb=X(2.3,3.0); s.append(box("t",xa,xb,y-0.2,y+0.2,0.0,0.2,op="join",targets=[nm]))
s.append(cyl("tmp",-1.2,3.4,1.05,0.1,0.8,op="cut",targets=["TDSO_cuerpo"]))  # marca pin 1 junto al pad 1 (-2.6,+3.81 modelo)
s+=[color(["TDSO_cuerpo"],BLACK),color(["TDSO_slug"]+leads,METAL),{"command":"appearance.assign","params":{"faces":[[-1.2,3.4,1.05]],"body":"TDSO_cuerpo","color":"#a0a0a0"}}]
save("pgtdso14.json",s)

# ---------- Borne ----------
Xl,Xr=-2.54,7.62
prof=[(5.5,0),(5.5,7.1),(3.86,14.0),(-2.26,14.0),(-3.46,9.8),(-4.5,9.8),(-4.5,0)]
s=[{"command":"sketch.create","params":{"plane":"YZ","offset":Xl,"name":"perfil"}},
   {"command":"sketch.line","params":{"points":[list(p) for p in prof],"closed":True}},
   {"command":"sketch.finish","params":{}},
   {"command":"solid.extrude","params":{"distance":Xr-Xl,"operation":"new","body_name":"Borne_cuerpo"}}]
screws=[];pins=[]
for i,px in enumerate((0.0,5.08),1):
    s.append(box("t",px-1.3,px+1.3,5.5-6.0,5.5+0.1,2.2,5.3,op="cut",targets=["Borne_cuerpo"]))
    s.append(cyl("t",px,0.6,12.0,2.1,3.9,op="cut",targets=["Borne_cuerpo"]))
s.append(box("t",Xl,Xl+0.4,-2.26,3.86,13.6,14.0,op="cut",targets=["Borne_cuerpo"]))  # marca lado pin 1
for i,px in enumerate((0.0,5.08),1):
    s.append(cyl(f"Borne_tornillo{i}",px,0.6,12.0,1.2,3.5)); screws.append(f"Borne_tornillo{i}")
    s.append(box(f"Borne_pin{i}",px-0.45,px+0.45,-0.4,0.4,-4.5,0.0)); pins.append(f"Borne_pin{i}")
s+=[color(["Borne_cuerpo"],GREEN),color(screws+pins,METAL)]
save("borne.json",s)

# ---------- Fusible Littelfuse NANO2 451/453 (SPEC-0018) ----------
# Cotas: 0451010.MRL, p. 4: 6,10 x 2,69 x 2,69 mm; casquillo 1,45 mm (supuesto: sin chaflan).
s=[box("Fusible_cuerpo",-1.6,1.6,-1.345,1.345,0,2.69)]
s.append(box("Fusible_tapa1",-3.05,-1.6,-1.345,1.345,0,2.69))
s.append(box("Fusible_tapa2",1.6,3.05,-1.345,1.345,0,2.69))
s+=[color(["Fusible_cuerpo"],"#d8c9a0"),color(["Fusible_tapa1","Fusible_tapa2"],METAL)]
save("nano2.json",s)
