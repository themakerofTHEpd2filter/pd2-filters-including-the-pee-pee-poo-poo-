from pathlib import Path

root=Path(__file__).resolve().parents[1]
files=sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files)==5, "Expected five filter variants"

def band_rule(low):
    hi=low+49
    if low == 700:
        condition="(FORMULARARECASTERHUNDREDTHS>699 OR FORMULARAREMELEEHUNDREDTHS>699)"
        label="Rating 7.0/7"
    else:
        upper=low+50
        cap=f"FORMULARARECASTERHUNDREDTHS<{upper} FORMULARAREMELEEHUNDREDTHS<{upper}"
        if low == 0:
            condition=cap
        else:
            condition=cap+f" (FORMULARARECASTERHUNDREDTHS>{low-1} OR FORMULARAREMELEEHUNDREDTHS>{low-1})"
        label=f"Rating {low/100:.1f}-{hi/100:.2f}/7"
        if low == 650:
            label="Rating 6.5-7.0/7"
    return f"ItemDisplay[V21_SCORE_HOVER_ RARE {condition}]: %NAME%%CONTINUE%{{%TEAL%{label}%CL%%NAME%}}"

rules=[band_rule(x) for x in range(0,701,50)]
assert len(rules)==15
replacement=(
    "// v68: Full 0-7 rating bands for identified rare inventory tooltip.\n"
    "// Numeric score predicates unchanged; no unsupported dynamic display tokens.\n"
    + "\n".join(rules)+"\n"
)
for p in files:
    old=p.read_text(encoding="utf-8-sig")
    if old.startswith("// v68:"):
        print("Already patched",p.name)
        continue
    assert old.startswith("// v67:"), f"Expected v67 baseline: {p.name}"
    lines=old.splitlines(keepends=True)
    matched=[i for i,line in enumerate(lines) if line.startswith("ItemDisplay[V21_SCORE_HOVER_")]
    assert len(matched)>=9, f"Missing V21 rating rules in {p.name}: {len(matched)}"
    start=matched[0]
    for i in reversed(matched):
        lines.pop(i)
    lines.insert(start,replacement)
    new="// v68: Complete 0-7 rare tooltip rating bands for all identifiable rare gear.\n"+"".join(lines)
    assert new.count("ItemDisplay[V21_SCORE_HOVER_ RARE ")==15
    assert "Rating 0.0-0.49/7" in new
    assert "Rating 6.5-7.0/7" in new
    assert "ItemDisplay[GROUND UNI !ID !ALLDISCOVERED !jew]:" in new
    assert "ItemDisplay[GROUND NMAG (ci0 OR ci1 OR ci2 OR ci3)]:" in new
    p.write_text(new,encoding="utf-8-sig")
    print("Updated",p.name,"replaced",len(matched),"old score rules with",len(rules),"complete bands")
