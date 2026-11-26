from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files) == 5, "Expected five active variants"

header = """// v65: Hide all nonmagical white/grey circlet-family ground drops.
// ci0 Circlet, ci1 Coronet, ci2 Tiara, ci3 Diadem.
// Keep magic Tiaras and Diadems, plus existing rare/unique/set/craft rules.
ItemDisplay[GROUND NMAG (ci0 OR ci1 OR ci2 OR ci3)]:
"""
for path in files:
    old = path.read_text(encoding="utf-8-sig")
    if old.startswith("// v65:"):
        print("Already updated", path.name)
        continue
    assert old.startswith("// v64:"), f"Missing v64 baseline: {path.name}"
    assert "ItemDisplay[GROUND MAG (ci2 OR ci3)]: %NAME%{%NAME%}" in old, path.name
    patched = header + old
    assert patched.count("ItemDisplay[GROUND NMAG (ci0 OR ci1 OR ci2 OR ci3)]:") == 1
    path.write_text(patched, encoding="utf-8-sig")
    print("Updated", path.name)
