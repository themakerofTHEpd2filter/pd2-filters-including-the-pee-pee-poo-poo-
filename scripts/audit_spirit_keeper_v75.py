from pathlib import Path
p=Path(__file__).resolve().parents[1]/"Hiim-Hyper-Tailored-.filter"
ls=p.read_text(encoding="utf-8-sig").splitlines()
print("SPIRIT_AUDIT_BEGIN")
for term in ("Alias[4_STAR_UNIQUE]", "Alias[4_STAR_ETH_UNIQUE]", "Alias[3_STAR_UNIQUE]", "Alias[2_STAR_UNIQUE]", "Alias[NO_STAR_UNIQUE]", "Alias[0_STAR_UNIQUE]", "Alias[UNIQUE]", "drd", "GROUND UNI"):
 hits=[(i+1,l) for i,l in enumerate(ls) if term in l]
 print("TERM",term,"COUNT",len(hits))
 for n,l in hits[:35]:
  print("RULE",n,l[:1400], "INCLUDES_DRD", "drd" in l)
print("SPIRIT_AUDIT_END")
