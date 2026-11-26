from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files) >= 5, "Expected five filter variants"

# These selectors run before any broad inherited Hiim filter show rules.
# Only apply to items on the ground, never inventory/equipped items.
# Body armor EQ2 and SHIELD are handled independently to avoid including helms.
header = """// v54: Strict ground-drop body armor and shield overhaul.
// No magic (blue) body armor or shields on ground.
// White/grey bases: only ethereal superior elite bases, with 0 or useful 3/4 sockets.
// Existing runewords, rare/set/unique/crafted items are not affected.
// Early terminal hides prevent later inherited rules from revealing junk.
ItemDisplay[GROUND MAG EQ2]:
ItemDisplay[GROUND MAG SHIELD]:
ItemDisplay[GROUND NMAG !RW EQ2 !(ETH SUP ELT DEF>=750 (SOCK=0 OR SOCK=3 OR SOCK=4))]:
ItemDisplay[GROUND NMAG !RW SHIELD !(ETH SUP ELT (SOCK=0 OR SOCK=3 OR SOCK=4))]:
// Explicitly retain qualifying bases ahead of later generic white/grey hide rules.
ItemDisplay[GROUND NMAG !RW EQ2 ETH SUP ELT DEF>=750 (SOCK=0 OR SOCK=3 OR SOCK=4)]: %NAME%{%NAME%}
ItemDisplay[GROUND NMAG !RW SHIELD ETH SUP ELT (SOCK=0 OR SOCK=3 OR SOCK=4)]: %NAME%{%NAME%}
"""

for path in files:
    old = path.read_text(encoding="utf-8-sig")
    if old.startswith("// v54:"):
        print("Already patched:", path.name)
        continue
    # Prepend ahead of all existing item-display rules; preserve all old formulas,
    # aliases, rare scores, unique labels, and magic jewel variant behavior.
    new = header + old
    path.write_text(new, encoding="utf-8-sig")
    assert new.count("ItemDisplay[GROUND MAG EQ2]:") == 1
    assert new.count("ItemDisplay[GROUND MAG SHIELD]:") == 1
    print("Patched", path.name, len(new))
