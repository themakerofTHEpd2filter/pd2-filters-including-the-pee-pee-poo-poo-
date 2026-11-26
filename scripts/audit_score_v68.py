from pathlib import Path
p=Path(__file__).resolve().parents[1]/"Hiim-Hyper-Tailored-.filter"
s=p.read_text(encoding="utf-8-sig")
lines=s.splitlines()
for needle in ("Formula[RARECASTER]", "Formula[RAREMELEE]", "Formula[RAREDROPBEST]", "Formula[RARECASTERHUNDREDTHS]", "Formula[RAREMELEEHUNDREDTHS]", "Alias[V21_SCORE_HOVER_]", "Alias[V19_GROUND_PRIORITY_]", "Alias[TAILORED_SCORED_GEAR]", "ItemDisplay[V21_SCORE_HOVER_", "Score ", "FORMULARAREMELEEHUNDREDTHS>249", "ItemDisplay[RARE ID", "ItemDisplay[GROUND RARE ID"):
    matches=[(i+1,l) for i,l in enumerate(lines) if needle in l]
    print("MATCH",needle,"COUNT",len(matches))
    for i,l in matches[:12]: print("LINE",i,l[:1400])
for needle in ("[C ", "[M ", "/7]", "Formula[RARE", "FORMULARARECASTER%", "FORMULARAREMELEE%"):
    hits=[(i+1,l) for i,l in enumerate(lines) if needle in l]
    print("DEEP",needle,"COUNT",len(hits))
    for i,l in hits[:15]: print("DEEP LINE",i,l[:900])
print("LATEST TOP", '\n'.join(lines[:17]))
