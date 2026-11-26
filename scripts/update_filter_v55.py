from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files) >= 5, "Expected all five variants"

header = """// v55: Hide all magic and nonmagic gloves and boots on the ground.
// Gloves and boots cannot be socketed; no runeword base exception applies.
// Rare/set/unique/crafted boots and gloves keep their prior scoring/display rules.
// This terminal rule precedes all inherited visibility rules.
ItemDisplay[GROUND (GLOVES OR BOOTS) (MAG OR NMAG)]:
"""

for path in files:
    old = path.read_text(encoding="utf-8-sig")
    if old.startswith("// v55:"):
        print("Already updated:", path.name)
        continue
    assert old.startswith("// v54:"), f"Missing prior v54 overhaul: {path.name}"
    new = header + old
    assert new.count("ItemDisplay[GROUND (GLOVES OR BOOTS) (MAG OR NMAG)]:") == 1
    path.write_text(new, encoding="utf-8-sig")
    print("Updated", path.name)
