from pathlib import Path
import re
p=Path(__file__).resolve().parents[1]/"Hiim-Hyper-Tailored-.filter"
lines=p.read_text(encoding="utf-8-sig").splitlines()
print("AUDIT_SCORE_LABELS_BEGIN")
for i,line in enumerate(lines):
 if not line.startswith("ItemDisplay[") or "]:" not in line: continue
 selector,action=line.split("]:",1)
 if ("SCORE_HOVER_" in selector or "GROUND_PRIORITY_" in selector or "CASTER SCORE" in action.upper() or "RATING" in action.upper() or "SCORE" in action.upper() or "4.8" in action or "6.5" in action or "%FORMULARARE" in action):
  if re.search(r'(score|rating|FORMULARARE|4\.8|6\.5)',action,re.I):
   print(f"LINE {i+1} SEL {selector[:235]} ACT {action[:440]}")
print("AUDIT_SCORE_LABELS_END")
