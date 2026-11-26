from pathlib import Path

root=Path(__file__).resolve().parents[1]
files=sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files)>=5, "Expected five active variants"

header="""// v61: Hide low-value normal-tier set helms and worthless white/blue arrow/bolt quivers.
// Keep valuable set items, unique quivers, rare quivers and rare 2.5+ scoring unchanged.
// Sigon's Visor is ghm; identified and unidentified Great Helm sets are filtered.
// Covers low-value normal set helm bases and Dangoon's Teaching.
ItemDisplay[GROUND SET (ghm OR fhl OR bnh OR msk OR hlm OR skp OR cap OR 7ma)]:
// No plain or magic quiver bases, including 2-socket Heavy Bolts cqv2.
// Preserve rare, crafted, unique and set variants for their existing item rules.
ItemDisplay[GROUND (NMAG OR MAG) (aqv OR aqv2 OR aqv3 OR cqv OR cqv2 OR cqv3)]:
"""
for p in files:
    old=p.read_text(encoding="utf-8-sig")
    if old.startswith("// v61:"):
        print("Already patched",p.name)
        continue
    assert old.startswith("// v60:"), "Expected v60 baseline: "+p.name
    assert "ItemDisplay[GROUND MAG (ci2 OR ci3)]: %NAME%{%NAME%}" in old
    assert "ItemDisplay[GROUND UNI !ETH (7sm OR 7vo" in old
    updated=header+old
    assert updated.count("ItemDisplay[GROUND SET (ghm OR fhl") == 1
    assert updated.count("ItemDisplay[GROUND (NMAG OR MAG) (aqv OR aqv2 OR aqv3 OR cqv OR cqv2 OR cqv3)]:") == 1
    p.write_text(updated,encoding="utf-8-sig")
    print("Updated",p.name)
