from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files) >= 5, "Expected all five filters"

header = """// v56: Hide all blue (magic) helm/circlet/amulet ground drops.
// Blue Diadems, Tiara, Coronets, circlets, class helms, and magic amulets are included.
// Filtering is GROUND only: picked-up items remain visible in inventory.
ItemDisplay[GROUND MAG (HELM OR CIRC OR amu)]:
"""
for path in files:
    old = path.read_text(encoding="utf-8-sig")
    if old.startswith("// v56:"):
        print("Already updated", path.name)
        continue
    assert old.startswith("// v55:"), f"v55 glove/boot rule missing: {path.name}"
    updated = header + old
    assert updated.count("ItemDisplay[GROUND MAG (HELM OR CIRC OR amu)]:") == 1
    assert "ItemDisplay[GROUND (GLOVES OR BOOTS) (MAG OR NMAG)]:" in updated
    assert "ItemDisplay[GROUND MAG EQ2]:" in updated
    path.write_text(updated, encoding="utf-8-sig")
    print("Updated", path.name)
