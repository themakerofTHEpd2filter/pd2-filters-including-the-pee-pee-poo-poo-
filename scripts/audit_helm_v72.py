from pathlib import Path
import re
p=Path(__file__).resolve().parents[1]/"Hiim-Hyper-Tailored-.filter"
s=p.read_text(encoding="utf-8-sig")
d={}
for l in s.splitlines():
 if l.startswith("Formula[") and "]: " in l:
  k,v=l.split("]: ",1)
  d[k[8:]]=v
for n in ['RARECASTER','RAREMELEE','RARESCORE','RAREMELEEHUNDREDTHS']:
 v=d[n]
 print("\nFORMULA",n,"length",len(v))
 if len(v)<5000:print('WHOLE',v)
 else:
  for term in ('HELM','CIRC','STAT136','STAT141','CB','PDR','TABSK','CLSK','MAXSOCKETS','SOCK','EDAM','FORMULA'):
   spans=[m.start() for m in re.finditer(re.escape(term),v,re.I)]
   print("TERM",term,"COUNT",len(spans))
   for x in spans[:8]:print("NEAR",v[max(0,x-160):x+220])
for l in s.splitlines():
 if l.startswith('Alias[') and any(t in l for t in ['HELM','TAILORED_SCORED_GEAR','BARB','CIRC']):
  print("ALIAS",l[:500])
for l in s.splitlines():
 if l.startswith('ItemDisplay[') and ("HELM" in l or "V21_SCORE_HOVER_" in l):
  if 'STAT136' in l or 'RARESCORE' in l or 'CLASS' in l:
   print("RULE",l[:550])
