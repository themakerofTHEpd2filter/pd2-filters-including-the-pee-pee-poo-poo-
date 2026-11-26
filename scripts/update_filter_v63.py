from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files) >= 5, "All five variants required"

header = """// v63: Use Hiim's star rankings to suppress junk sets/uniques.
// Milabrega's Rod (War Scepter, wsp) and Sigon's Visor (Great Helm, ghm)
// are explicitly hidden on the ground, including unid drops.
// Preserve high tier sets, jewelry, LLD sets, and eth set weapons.
// All other unranked, zero-star, and one-star sets stay hidden.
// Preserve unique jewelry, facets and all higher-tier or ethereal uniques.
// Hiim's star aliases use the highest-rated unique where bases overlap.
ItemDisplay[GROUND SET (wsp OR ghm)]:
ItemDisplay[GROUND SET !(2_STAR_SET OR 3_STAR_SET OR 4_STAR_SET OR amu OR rin OR LLD_SET OR (ETH WEAPON))]:
ItemDisplay[GROUND UNI !ETH (0_STAR_UNIQUE OR NO_STAR_UNIQUE) !(amu OR rin OR jew)]:
"""

for p in files:
    old = p.read_text(encoding="utf-8-sig")
    if old.startswith("// v63:"):
        print("Already updated", p.name)
        continue
    assert old.startswith("// v62:"), f"Expected v62 baseline: {p.name}"
    for required in (
        "Alias[2_STAR_SET]:",
        "Alias[3_STAR_SET]:",
        "Alias[4_STAR_SET]:",
        "Alias[0_STAR_UNIQUE]:",
        "Alias[NO_STAR_UNIQUE]:",
        "Alias[LLD_SET]:",
        "ItemDisplay[GROUND MAG (ci2 OR ci3)]",
    ):
        assert required in old, (p.name, required)
    updated = header + old
    p.write_text(updated, encoding="utf-8-sig")
    print("Updated", p.name)
