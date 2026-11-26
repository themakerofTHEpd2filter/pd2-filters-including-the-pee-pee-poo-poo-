from pathlib import Path
import re
p=Path(__file__).resolve().parents[1]/"Hiim-Hyper-Tailored-.filter"
s=p.read_text(encoding="utf-8-sig")
line_defs=s.splitlines()
for name in ("TAILORED_SCORED_GEAR","V21_SCORE_HOVER_","V22_SHOW_MAIN_","TAILORED_V49_SCORED_EQUIPMENT"):
    for l in line_defs:
        if l.startswith(f"Alias[{name}]:"):
            print("ALIAS",l[:1500])
for name in ["RARECASTER","RAREMELEE","RARECASTERHUNDREDTHS","RAREMELEEHUNDREDTHS"]:
    defs=[l.split("]: ",1)[1] for l in line_defs if l.startswith(f"Formula[{name}]: ")]
    assert len(defs)==1,(name,len(defs))
    body=defs[0]
    print("FORMULA",name,"len",len(body))
    for tok in ["CHEST","HELM","DRU","BAR","CIRC","WEAPON","SHIELD","GLOVES","BOOTS","BELT","QUIVER","JEWEL","JEWELRY","AMU","RIN","CHARM","TABSK","CLSK"]:
        occurrences=list(re.finditer(r'(?<![A-Z0-9])'+re.escape(tok)+r'(?![A-Z0-9])',body))
        print("SLOT_TOKEN",name,tok,len(occurrences))
        if tok in ("BOOTS","BELT","JEWEL","JEWELRY","AMU","RIN","GLOVES","QUIVER","CHARM"):
            for m in occurrences[:4]:
                print("EXCERPT",name,tok,body[max(0,m.start()-115):m.start()+205])
for l in line_defs:
    if l.startswith("ItemDisplay[") and "FORMULARARESCORE" in l:
        print("TOTAL_SCORE_REF",l[:500])
print("AUDIT_COMPLETE")
