from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files) == 5, "Expected exactly five active filter variants"

# Exact quality threshold of original Hiim level 7 (FILTLVL<8):
# 4/3/2 star, separately for regular and ethereal uniques.
# Jewelry, facets, and explicitly named pinnacle/boss drops remain protected.
# Do not apply earlier Hiim level 1-6 allowances (1/0/no-star, LLD).
boss = "(ram OR rar OR rbe OR 7qr OR uhn OR uth OR utc OR utb OR 7bs OR (uh9 MAPID=137))"
special = "(MAPID=137 OR MAPID=161 OR MAPID=162 OR MAPID=163)"
header = f"""// v64: Match original Hiim level 7 unique filtering on all ground drops.
// Hiim FILTLVL=7: show 2/3/4-star uniques, with separate ethereal ratings.
// Protect unique jewelry/facets and Hiim's boss/pinnacle drop exceptions.
// Hide unranked, 0-star, no-star and 1-star uniques (including eth variants).
ItemDisplay[GROUND UNI !ETH !(4_STAR_UNIQUE OR 3_STAR_UNIQUE OR 2_STAR_UNIQUE OR amu OR rin OR jew OR {boss} OR {special})]:
ItemDisplay[GROUND UNI ETH !(4_STAR_ETH_UNIQUE OR 3_STAR_ETH_UNIQUE OR 2_STAR_ETH_UNIQUE OR amu OR rin OR jew OR {boss} OR {special})]:
"""

for p in files:
    original = p.read_text(encoding="utf-8-sig")
    if original.startswith("// v64:"):
        print("Already patched", p.name)
        continue
    assert original.startswith("// v63:"), f"Expected v63 baseline: {p.name}"
    for alias in ("4_STAR_UNIQUE", "3_STAR_UNIQUE", "2_STAR_UNIQUE",
                  "4_STAR_ETH_UNIQUE", "3_STAR_ETH_UNIQUE", "2_STAR_ETH_UNIQUE"):
        assert f"Alias[{alias}]:" in original, (p.name, alias)
    assert "ItemDisplay[GROUND MAG (ci2 OR ci3)]:" in original, p.name
    patched = header + original
    assert patched.count("ItemDisplay[GROUND UNI !ETH !(4_STAR_UNIQUE") == 1
    assert patched.count("ItemDisplay[GROUND UNI ETH !(4_STAR_ETH_UNIQUE") == 1
    p.write_text(patched, encoding="utf-8-sig")
    print("Updated", p.name)
