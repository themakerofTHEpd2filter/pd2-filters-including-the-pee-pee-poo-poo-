from pathlib import Path
root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files) >= 5, "Expected all existing variants"
for path in files:
    s = path.read_text(encoding="utf-8-sig")
    if s.startswith("// v52:"):
        print("Already corrected", path.name)
        continue
    anchor = "// v49: HARD SCORE CUTOFF ON IDENTIFIED SCORABLE EQUIPMENT."
    if s.count(anchor) != 1:
        raise ValueError("Missing unique insertion anchor: " + path.name)
    # Early exclusion rules, limited to map/endgame tiers 3-11.
    # Leave rares, uniques, sets, crafts and blue jewels untouched.
    # Magic javelins/orbs/staves/wands/scepters and class helms retain existing rules.
    rules = (
       "// v52: Remove low-value ordinary blue and white dropped helms/weapons at strict tiers.\n"
       "// White/grey premium bases and identified magic items remain subject to existing checks.\n"
       "ItemDisplay[GROUND FILTLVL>2 MAG !ID HELM !CIRC !DRU !BAR]:\n"
       "ItemDisplay[GROUND FILTLVL>2 MAG !ID WEAPON !SOR !STAFF !WAND !THROWING !SCEPTER]:\n"
       "ItemDisplay[GROUND FILTLVL>2 NMAG !RW !SUP HELM !(SOCK>=3 MAXSOCKETS>=3)]:\n"
       "ItemDisplay[GROUND FILTLVL>2 NMAG !RW !SUP WEAPON !(ETH OR (SOCK>=4 TAILORED_RARE_WEAPON_BASE_OK))]:\n"
       "ItemDisplay[GROUND FILTLVL>2 NMAG !RW SUP HELM !TAILORED_SUPERIOR_BEST]:\n"
       "ItemDisplay[GROUND FILTLVL>2 NMAG !RW SUP WEAPON !TAILORED_SUPERIOR_BEST]:\n"
    )
    s = s.replace(anchor, rules + anchor, 1)
    # Preserve the existing endgame rare/unique behavior, decoration and jewel variants.
    path.write_text("// v52: Targeted junk blue/white gear fix; rare helm scoring and blue jewels preserved.\n" + s, encoding="utf-8-sig")
    print("Corrected", path.name)
