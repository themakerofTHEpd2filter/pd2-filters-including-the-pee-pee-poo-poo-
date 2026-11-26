from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files) >= 5, "Expected all five variants"

header = """// v58: Remove blue crafting-base equipment drops on the ground at ALL filter levels.
// No [LLD Craft] magic orbs, staves, wands, scepters, weapons, etc.
// Keep magic Diadems (ci3), Tiaras (ci2), small charms and magic jewels.
// Existing rare/crafted/unique/set items are NOT modified.
// Rule deliberately precedes inherited LLD craft show overrides.
ItemDisplay[GROUND MAG WEAPON]:
ItemDisplay[GROUND MAG (GLOVES OR BOOTS OR BELT OR rin)]:
"""

for path in files:
    old = path.read_text(encoding="utf-8-sig")
    if old.startswith("// v58:"):
        print("Already updated", path.name)
        continue
    assert old.startswith("// v57:"), f"Expected v57 as baseline: {path.name}"
    assert "ItemDisplay[GROUND MAG (ci2 OR ci3)]: %NAME%{%NAME%}" in old, path.name
    assert "ItemDisplay[GROUND MAG (HELM OR CIRC OR amu) !(ci2 OR ci3)]:" in old, path.name
    assert "ItemDisplay[GROUND (GLOVES OR BOOTS) (MAG OR NMAG)]:" in old, path.name
    new = header + old
    path.write_text(new, encoding="utf-8-sig")
    print("Updated", path.name)
