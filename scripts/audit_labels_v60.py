from pathlib import Path
p=Path(__file__).resolve().parents[1]/"Hiim-Hyper-Tailored-.filter"
s=p.read_text(encoding="utf-8-sig")
print("DIAGNOSTIC START")
lines=s.splitlines()
for needle in ("$f(", "20FCR", "25%C", "Manald", "V19_GROUND_PRIORITY_", "GROUND UNI rin"):
    hits=[(i+1,l) for i,l in enumerate(lines) if needle in l and (l.startswith("ItemDisplay[") or needle=="Manald")]
    print("PATTERN",needle,"COUNT",len(hits))
    for i,l in hits[:8]:
        print("LINE",i,l[:1200])
print("DIAGNOSTIC END")
