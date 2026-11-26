from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files) >= 5, "Five filter variants required"

before = "ItemDisplay[GROUND MAG (HELM OR CIRC OR amu)]:"
after = """// Magic Tiara (ci2) and Diadem (ci3) are deliberately retained on ground.
ItemDisplay[GROUND MAG (ci2 OR ci3)]: %NAME%{%NAME%}
ItemDisplay[GROUND MAG (HELM OR CIRC OR amu) !(ci2 OR ci3)]:"""

for path in files:
    old = path.read_text(encoding="utf-8-sig")
    if old.startswith("// v57:"):
        print("Already patched", path.name)
        continue
    assert old.startswith("// v56:"), f"Expected v56 baseline in {path.name}"
    assert old.count(before) == 1, f"Expected one v56 helm rule in {path.name}"
    patched = old.replace(before, after, 1)
    patched = "// v57: Show blue Tiaras and Diadems; continue hiding other magic helms and amulets.\n" + patched
    assert patched.index("ItemDisplay[GROUND MAG (ci2 OR ci3)]") < patched.index("ItemDisplay[GROUND MAG (HELM OR CIRC OR amu) !(ci2 OR ci3)]")
    assert "ItemDisplay[GROUND (GLOVES OR BOOTS) (MAG OR NMAG)]:" in patched
    path.write_text(patched, encoding="utf-8-sig")
    print("Updated", path.name)
