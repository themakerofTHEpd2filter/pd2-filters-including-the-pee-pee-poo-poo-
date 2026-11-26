from pathlib import Path
root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files) == 5, "Expected five active filter variants"
header = """// v67: Grail labels using PD2's discovery/ownership conditions.
// Not yet discovered: orange GRAIL. Discovered but not currently owned: white GRAIL.
// These first-match rules are placed before the Hiim level-7 value cutoff;
// ordinary already-owned low-value uniques/sets remain hidden.
// Unique jewels are excluded, following the original Hiim grail tagging convention.
// Ground only; do not replace inventory/hover behavior.
ItemDisplay[GROUND UNI !ID !ALLDISCOVERED !jew]: %ORANGE%GRAIL %GOLD%%NAME%{%NAME%}
ItemDisplay[GROUND SET !ID !ALLDISCOVERED]: %ORANGE%GRAIL %GREEN%%NAME%{%NAME%}
ItemDisplay[GROUND UNI !ID ALLDISCOVERED !ALLOWNED !jew]: %WHITE%GRAIL %GOLD%%NAME%{%NAME%}
ItemDisplay[GROUND SET !ID ALLDISCOVERED !ALLOWNED]: %WHITE%GRAIL %GREEN%%NAME%{%NAME%}
"""
for p in files:
    old = p.read_text(encoding="utf-8-sig")
    if old.startswith("// v67:"):
        print("Already patched", p.name)
        continue
    assert old.startswith("// v66:"), f"Expected v66 baseline in {p.name}"
    assert "ItemDisplay[GROUND UNI !ETH !(4_STAR_UNIQUE" in old, p.name
    updated = header + old
    assert updated.index("ItemDisplay[GROUND UNI !ID !ALLDISCOVERED") < updated.index("ItemDisplay[GROUND UNI !ETH !(4_STAR_UNIQUE")
    assert updated.count("ItemDisplay[GROUND SET !ID !ALLDISCOVERED]:") == 1
    p.write_text(updated, encoding="utf-8-sig")
    print("Updated", p.name)
