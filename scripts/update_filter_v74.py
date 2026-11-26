from pathlib import Path
root=Path(__file__).resolve().parents[1]
files=sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files)==5
S="MAX(ALLSK,CLSK0,CLSK1,CLSK2,CLSK3,CLSK4,CLSK5,CLSK6)"
# Purely additive, conditional grading branches (hundredths of a point),
# using only variables the real Project Diablo 2 BH formula engine supports.
# The existing original formula is never reduced.
jew="AND(MISC,!JEWELRY,!CHARM,!QUIVER,!RUNE,!GEM,(RARE||MAG),ID)"
# Note: PD2's Formula[] parser supports OR() rather than ||, so use OR().
jew=jew.replace("(RARE||MAG)","OR(RARE,MAG)")
jcas=f"IF(AND({jew},OR(FCR>=10,MAEK>=2,RES>=5,STAT86>=3,STR>=8)),MIN(700,45+IF(MAEK>=5,170,IF(MAEK>=3,115,IF(MAEK>=2,70,0)))+IF(STAT86>=5,90,IF(STAT86>=3,55,0))+IF(RES>=15,140,IF(RES>=10,100,IF(RES>=5,60,0)))+IF(STR>=15,75,IF(STR>=8,40,0))+IF(DEX>=15,75,IF(DEX>=8,40,0))+IF(FCR>=10,140,0)+IF(STAT80>=15,50,0)),0)"
jmel=f"IF(AND({jew},OR(EDAM>=15,IAS>=10,STAT136>=5,STAT141>=5)),MIN(700,45+IF(EDAM>=40,230,IF(EDAM>=30,190,IF(EDAM>=20,125,IF(EDAM>=15,80,0))))+IF(IAS>=15,145,IF(IAS>=10,95,0))+IF(STAT136>=10,105,IF(STAT136>=5,60,0))+IF(STAT141>=10,105,IF(STAT141>=5,60,0))+IF(RES>=15,115,IF(RES>=5,60,0))+IF(STR>=15,75,IF(STR>=8,45,0))+IF(DEX>=15,75,IF(DEX>=8,45,0))),0)"
bcas=f"IF(AND(BOOTS,RARE,ID,OR(FRW>=20,FHR>=10,RES>=10,STAT80>=15)),MIN(700,50+IF(FRW>=40,170,IF(FRW>=30,130,IF(FRW>=20,75,0)))+IF(FHR>=30,120,IF(FHR>=20,100,IF(FHR>=10,55,0)))+IF(RES>=30,155,IF(RES>=20,115,IF(RES>=10,65,0)))+IF(STAT80>=25,85,IF(STAT80>=15,55,0))+IF(LIFE>=30,95,IF(LIFE>=20,65,0))+IF(STR>=20,70,IF(STR>=10,40,0))+IF(STAT110>=25,50,IF(STAT110>=15,25,0))),0)"
bmel=f"IF(AND(BOOTS,RARE,ID,OR(FRW>=20,RES>=10,FHR>=10,DEX>=10)),MIN(700,45+IF(FRW>=40,175,IF(FRW>=30,130,IF(FRW>=20,75,0)))+IF(RES>=30,155,IF(RES>=20,115,IF(RES>=10,65,0)))+IF(FHR>=30,115,IF(FHR>=20,90,IF(FHR>=10,50,0)))+IF(LIFE>=30,85,IF(LIFE>=20,55,0))+IF(STR>=20,80,IF(STR>=10,45,0))+IF(DEX>=20,80,IF(DEX>=10,45,0))+IF(STAT36>=10,100,0)),0)"
gcas=f"IF(AND(GLOVES,RARE,ID,OR(FCR>=10,STAT102>=15,MAEK>=2,STAT80>=20)),MIN(700,40+IF(FCR>=20,140,IF(FCR>=10,85,0))+IF(STAT102>=20,85,IF(STAT102>=15,50,0))+IF(STAT80>=25,70,IF(STAT80>=15,40,0))+IF(RES>=25,115,IF(RES>=15,75,0))+IF(MAEK>=5,110,IF(MAEK>=3,75,0))+IF(STAT86>=5,80,IF(STAT86>=3,45,0))+IF(STR>=20,85,IF(STR>=10,45,0))+IF(LIFE>=30,70,0)),0)"
gmel=f"IF(AND(GLOVES,RARE,ID,OR(IAS>=10,STAT136>=10,STAT141>=10,MAX(TABSK0,TABSK2,TABSK50)>=2)),MIN(700,50+IF(IAS>=20,165,IF(IAS>=10,90,0))+IF(MAX(TABSK0,TABSK2,TABSK50)>=2,165,IF(MAX(TABSK0,TABSK2,TABSK50)>=1,75,0))+IF(STAT136>=15,125,IF(STAT136>=10,85,0))+IF(STAT141>=15,125,IF(STAT141>=10,85,0))+IF(RES>=25,100,IF(RES>=15,60,0))+IF(STR>=20,85,IF(STR>=10,45,0))+IF(MAEK>=3,45,0)),0)"
acas=f"IF(AND(JEWELRY,RARE,ID,OR(FCR>=10,{S}>=1,RES>=10)),MIN(700,55+IF(FCR>=20,160,IF(FCR>=10,85,0))+IF({S}>=2,235,IF({S}>=1,130,0))+IF(RES>=30,150,IF(RES>=20,105,IF(RES>=10,55,0)))+IF(STR>=20,90,IF(STR>=10,55,0))+IF(DEX>=20,80,IF(DEX>=10,45,0))+IF(LIFE>=30,85,0)+IF(MAEK>=3,65,0)),0)"
amel=f"IF(AND(JEWELRY,RARE,ID,OR({S}>=1,IAS>=10,STAT141>=10,STR>=15)),MIN(700,45+IF({S}>=2,235,IF({S}>=1,130,0))+IF(IAS>=20,160,IF(IAS>=10,95,0))+IF(STAT141>=15,115,IF(STAT141>=10,75,0))+IF(RES>=30,145,IF(RES>=20,105,IF(RES>=10,55,0)))+IF(STR>=20,90,IF(STR>=10,55,0))+IF(DEX>=20,90,IF(DEX>=10,55,0))+IF(LIFE>=30,75,0)),0)"
ltcas="IF(AND(BELT,RARE,ID,OR(RES>=15,FHR>=20,STAT36>=8)),MIN(650,40+IF(RES>=30,150,IF(RES>=20,105,IF(RES>=15,70,0)))+IF(FHR>=30,130,IF(FHR>=20,95,0))+IF(STAT36>=15,155,IF(STAT36>=8,85,0))+IF(LIFE>=30,85,0)+IF(STR>=15,70,0)+IF(STAT110>=25,65,0)+IF(STAT80>=20,60,0)),0)"
ltmel="IF(AND(BELT,RARE,ID,OR(RES>=15,FHR>=20,STAT36>=8)),MIN(650,40+IF(RES>=30,150,IF(RES>=20,105,IF(RES>=15,70,0)))+IF(FHR>=30,130,IF(FHR>=20,95,0))+IF(STAT36>=15,155,IF(STAT36>=8,85,0))+IF(LIFE>=30,85,0)+IF(STR>=15,70,0)+IF(STAT110>=25,65,0)+IF(DEX>=15,65,0)),0)"
qmel="IF(AND(QUIVER,RARE,ID,OR(EDAM>=50,IAS>=15,AR>=80)),MIN(700,50+IF(EDAM>=200,235,IF(EDAM>=150,180,IF(EDAM>=100,135,IF(EDAM>=50,75,0))))+IF(IAS>=30,170,IF(IAS>=20,120,IF(IAS>=15,80,0)))+IF(AR>=150,110,IF(AR>=80,65,0))+IF(DEX>=20,90,IF(DEX>=10,50,0))+IF(RES>=20,80,0)+IF(STAT136>=10,75,0)),0)"
add_c="MAX("+",".join([jcas,bcas,gcas,acas,ltcas])+")"
add_m="MAX("+",".join([jmel,bmel,gmel,amel,ltmel,qmel])+")"
assert "||" not in add_c+add_m
for p in files:
    old=p.read_text(encoding="utf-8-sig")
    if old.startswith("// v74:"):
        print("Already patched",p.name);continue
    assert old.startswith("// v73:"),(p.name,"v73 required")
    output=[]; n=set()
    for line in old.splitlines(keepends=True):
        if line.startswith("Formula[") and "]: " in line:
            tag,sep,expr=line.partition("]: ")
            name=tag[8:]
            if name in ("RARECASTER","RARECASTERHUNDREDTHS","RAREMELEE","RAREMELEEHUNDREDTHS","RARESCORE","RAREDROPBEST"):
                ratio=("/100" if name in ("RARECASTER","RAREMELEE","RARESCORE") else "")
                if name.startswith("RARECASTER"): score=add_c
                elif name.startswith("RAREMELEE"): score=add_m
                else: score=f"MAX({add_c},{add_m})"
                line=tag+sep+f"MAX({expr.rstrip()},{score}{ratio})\n"
                n.add(name)
        if line.startswith("Alias[V21_SCORE_HOVER_]:"):
            assert "TAILORED_SCORED_GEAR OR (MAG ID CHARM)" in line
            line=line.replace("TAILORED_SCORED_GEAR OR (MAG ID CHARM)","TAILORED_SCORED_GEAR OR (MAG ID CHARM) OR (RARE ID BOOTS)")
        output.append(line)
    assert len(n)==6,(p.name,n)
    result="// v74: Comprehensive additive grading for jewels, gloves, boots, jewelry, belts and quivers; no ground visibility changes.\n"+"".join(output)
    assert "Alias[V21_SCORE_HOVER_]: (!GROUND !SHOP FILTLVL>0 (TAILORED_SCORED_GEAR OR (MAG ID CHARM) OR (RARE ID BOOTS)))" in result
    assert "ItemDisplay[GROUND UNI !ID !ALLDISCOVERED !jew]:" in result
    assert "ItemDisplay[GROUND (GLOVES OR BOOTS) (MAG OR NMAG)]:" in result
    p.write_text(result,encoding="utf-8-sig")
    print("Updated",p.name,"six formula defs + boots inventory tooltip alias")
