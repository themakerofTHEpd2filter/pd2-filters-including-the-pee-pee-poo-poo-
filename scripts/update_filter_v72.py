from pathlib import Path
import re

root=Path(__file__).resolve().parents[1]
files=sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files)==5,"Expected five variants"

# v72: general non-class rare helmets with Barbarian combat tabs, CB/DS,
# %PDR, sockets, ED and res had no melee grade unless they also had EDAM.
# Evaluate all actual item stats dynamically, in the same hundredths units
# as existing rare-melee threshold selectors. Cap this supplementary branch
# at 5.8, preserving the older GG 6.0-7.0 socket/ED/DS rules unchanged.
#
# STAT136 = Crushing Blow, STAT141 = Deadly Strike, STAT36 = % PDR.
# TABSK32/33/34 are Barbarian skill tabs, including Combat Skills.
tabs="MAX(TABSK32,TABSK33,TABSK34)"
bonus=f"""IF(AND(HELM,!CIRC,!DRU,!BAR,RARE,ID),MIN(580,
 IF({tabs}>=2,205,IF({tabs}>=1,95,0))+
 IF(STAT36>=15,140,IF(STAT36>=10,110,IF(STAT36>=5,60,0)))+
 IF(STAT136>=15,110,IF(STAT136>=10,75,IF(STAT136>=5,35,0)))+
 IF(STAT141>=15,115,IF(STAT141>=10,80,IF(STAT141>=5,35,0)))+
 IF(SOCK>=3,110,IF(SOCK>=2,70,0))+
 IF(EDAM>=30,90,IF(EDAM>=15,45,0))+
 IF(RES>=20,60,IF(RES>=10,30,0))
 ),0)"""
bonus="".join(bonus.split())  # Existing formulas are single-line.
critical={'RAREMELEE': '/100', 'RAREMELEEHUNDREDTHS': '', 'RAREDROPBEST': '', 'RARESCORE':'/100'}
for p in files:
    old=p.read_text(encoding='utf-8-sig')
    if old.startswith('// v72:'):
        print('Already patched',p.name)
        continue
    assert old.startswith('// v71:'),f"Need v71 baseline: {p.name}"
    updated=[]
    seen={}
    for line in old.splitlines(keepends=True):
        if line.startswith('Formula[') and ']: ' in line:
            key,sep,expr=line.partition(']: ')
            name=key[len('Formula['):]
            if name in critical:
                calc=expr.rstrip('\r\n')
                wrapped=f"MAX({calc},{bonus}{critical[name]})"
                line=key+sep+wrapped+'\n'
                seen[name]=1
        updated.append(line)
    assert set(seen)==set(critical), (p.name,seen)
    result='// v72: Dynamic barbarian-combat rare helm scoring including CB, PDR and sockets; existing top-tier scores retained.\n'+''.join(updated)
    assert result.count('Formula[RAREMELEE]:')==1
    assert 'TABSK32' in result and 'STAT136>=10' in result
    assert 'Formula[RARESCORE]:' in result
    assert 'ItemDisplay[GROUND UNI !ID !ALLDISCOVERED !jew]:' in result
    p.write_text(result,encoding='utf-8-sig')
    print('Updated',p.name,'four dependent score formula definitions')
