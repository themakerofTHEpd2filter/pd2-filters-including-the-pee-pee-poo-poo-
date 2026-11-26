from pathlib import Path
import re

root=Path(__file__).resolve().parents[1]
files=sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files)==5

# The item filter Formula[] lexer accepts == but NOT a lone '='.
# v51 added SOCK=0 inside a helm bonus, which invalidated melee score formulas
# (and the combined drop score). Leave ItemDisplay[...] predicates unchanged:
# in those, SOCK=0 is VALID syntax.
single_equals=re.compile(r'(?<![=<>!])=(?!=)')
critical={'RAREMELEEHUNDREDTHS','RAREMELEE','RAREDROPBEST'}
for p in files:
    old=p.read_text(encoding="utf-8-sig")
    if old.startswith("// v70:"):
        print("Already patched",p.name)
        continue
    assert old.startswith("// v69:"), (p.name, "expected v69")
    output=[]
    fixed={}
    for line in old.splitlines(keepends=True):
        if line.startswith("Formula[") and "]: " in line:
            name=line.split("]:",1)[0][8:]
            if name in critical:
                k,v=line.split("]: ",1)
                new,n=single_equals.subn("==",v)
                fixed[name]=n
                line=k+"]: "+new
        output.append(line)
    assert set(fixed)==critical, (p.name,fixed)
    assert all(n>0 for n in fixed.values()), (p.name,fixed)
    patched="// v70: Fix invalid score Formula[] equality; restore actual evaluated ratings.\n"+"".join(output)
    assert "%FORMULARAREMELEE%" in patched, p.name
    assert "ItemDisplay[GROUND UNI !ID !ALLDISCOVERED !jew]:" in patched
    p.write_text(patched,encoding="utf-8-sig")
    print("Patched",p.name,fixed)
