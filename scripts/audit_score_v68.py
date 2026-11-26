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


import re, subprocess
for label in ['RAREMELEE','RAREMELEEHUNDREDTHS','RARECASTER','RARECASTERHUNDREDTHS','RAREDROPBEST']:
  hits=[line.partition(': ')[2] for line in s.splitlines() if line.startswith('Formula['+label+']:')]
  if not hits: continue
  v=hits[0]
  dep=len(re.findall(r'\\(',v))-len(re.findall(r'\\)',v))
  print('FORMULACHECK',label,'LEN',len(v),'BAL',dep,'TRAIL',repr(v[-280:]))
try:
  orig=subprocess.check_output(['git','show','80be1fe66ea8:Hiim-Hyper-Tailored-.filter'],text=True)
  for label in ['RAREMELEE','RAREMELEEHUNDREDTHS','RARECASTER','RARECASTERHUNDREDTHS']:
    hits=[line.partition(': ')[2] for line in orig.splitlines() if line.startswith('Formula['+label+']:')]
    if hits:
      v=hits[0]
      print('BASELINEFORMULA',label,'LEN',len(v),'BAL',v.count('(')-v.count(')'),'TRAIL',repr(v[-280:]))
except Exception as e:
  print('BASELINEFORMULA ERROR',str(e)[:300])
