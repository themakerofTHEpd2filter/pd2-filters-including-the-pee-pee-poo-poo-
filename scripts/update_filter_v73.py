from pathlib import Path
root=Path(__file__).resolve().parents[1]
files=sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files)==5

skills="MAX(ALLSK,CLSK0,CLSK1,CLSK2,CLSK3,CLSK4,CLSK5,CLSK6)"
# Conservative lower/middle-tier scores for RARE identified chest armour.
# Original GG scoring remains the maximum: no existing higher score is reduced.
# Caster: 20 FCR + 19 str + 15 cold res + 4 LAEK -> 2.75/7.
caster=f"""IF(AND(CHEST,RARE,ID,OR(FCR>=10,{skills}>=1,SOCK>=2)),MIN(585,
55+
IF(FCR>=30,150,IF(FCR>=20,120,IF(FCR>=10,65,0)))+
IF({skills}>=2,170,IF({skills}>=1,100,0))+
IF(STR>=20,85,IF(STR>=15,65,IF(STR>=10,40,0)))+
IF(RES>=25,85,IF(RES>=15,55,IF(RES>=10,30,0)))+
IF(MAX(FRES,CRES,LRES,PRES)>=15,20,0)+
IF(STAT86>=4,15,0)+
IF(SOCK>=4,145,IF(SOCK>=3,105,IF(SOCK>=2,55,0)))+
IF(STAT36>=15,115,IF(STAT36>=10,75,0))+
IF(FHR>=20,35,0)
),0)"""
# Melee: 155 ED +1 class skill +26 all res +25 PLR -> 4.75/7.
melee=f"""IF(AND(CHEST,RARE,ID,OR(EDAM>=75,{skills}>=1,SOCK>=2,STAT36>=10)),MIN(605,
75+
IF(EDAM>=250,245,IF(EDAM>=200,220,IF(EDAM>=180,200,IF(EDAM>=150,170,IF(EDAM>=100,120,IF(EDAM>=75,80,0))))))+
IF({skills}>=2,165,IF({skills}>=1,100,0))+
IF(RES>=25,80,IF(RES>=15,55,IF(RES>=10,35,0)))+
IF(STAT110>=25,50,IF(STAT110>=15,25,0))+
IF(SOCK>=4,155,IF(SOCK>=3,110,IF(SOCK>=2,65,0)))+
IF(STAT36>=15,120,IF(STAT36>=10,85,0))+
IF(STR>=15,40,0)+
IF(FHR>=20,40,0)
),0)"""
caster="".join(caster.split())
melee="".join(melee.split())
suff={'RARECASTER':(caster,'/100'),'RARECASTERHUNDREDTHS':(caster,''),
      'RAREMELEE':(melee,'/100'),'RAREMELEEHUNDREDTHS':(melee,''),
      'RARESCORE':(None,None),'RAREDROPBEST':(None,None)}
for p in files:
    old=p.read_text(encoding="utf-8-sig")
    if old.startswith("// v73:"):
        print('Already patched',p.name)
        continue
    assert old.startswith("// v72:"),f"Expected v72 baseline: {p.name}"
    lines=[]
    seen={}
    for line in old.splitlines(keepends=True):
        if line.startswith("Formula[") and "]: " in line:
            left,sep,right=line.partition("]: ")
            name=left[8:]
            if name in suff:
                score,unit=suff[name]
                # RARESCORE and RAREDROPBEST are based on both C/M formulas.
                # Update these too so all UI and visibility thresholds agree.
                if name=="RARESCORE":
                    value=f"MAX({caster}/100,{melee}/100)"
                elif name=="RAREDROPBEST":
                    value=f"MAX({caster},{melee})"
                else:
                    value=f"{score}{unit}"
                line=left+sep+f"MAX({right.rstrip()},{value})\n"
                seen[name]=1
        lines.append(line)
    assert set(seen)==set(suff),(p.name,seen)
    result="// v73: Score midrange rare chest armor using actual FCR, skill, ED, strength, res, PLR and sockets.\n"+"".join(lines)
    assert 'Formula[RARESCORE]:' in result
    assert 'ItemDisplay[GROUND UNI !ID !ALLDISCOVERED !jew]:' in result
    p.write_text(result,encoding="utf-8-sig")
    print("Updated",p.name,"six formula definitions")
