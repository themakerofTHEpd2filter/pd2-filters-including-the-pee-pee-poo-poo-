from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files) >= 5, "Expected all five active variants"

# Narrow list of low-value unique bases (noneth only). Do not suppress
# higher-value uniques, ethereals, jewelry, belts, jewels, class-specific chase
# items or DClone/Rathma rewards. Based on conservative manual review.
# Base aliases are intentionally explicit, not an indiscriminate UNI hide.
junk_codes = [
    "7sm", # Djinn Slayer
    "7vo", # Giant Maimer
    "8cb", # Endlesshail
    "8cs", # Chromatic Ire
    "8lb", # Kuko Shakaku
    "8sw", # Magewrath
    "9b9", # Cloudcrack
    "9fl", # Baezil's Vortex
    "9kr", # Blackbog's Sharp
    "9sr", # The Impaler
    "gix", # Humongous
    "kri", # The Jade Tan Do
    "lbb", # Wizendraw
    "vbt", # Gorefoot
    "xts", # Radament's Sphere
    "xar", # Corpsemourn
]
selector = "ItemDisplay[GROUND UNI !ETH (" + " OR ".join(junk_codes) + ")]:"
header = ("// v59: Suppress conservative list of low-value noneth uniques at ground drop; preserve valuable/eth variants.\n"
          "// Identified and unidentified drops use the same base code. No change to inventories.\n"
          + selector + "\n")
for path in files:
    old = path.read_text(encoding="utf-8-sig")
    if old.startswith("// v59:"):
        print("Already patched", path.name)
        continue
    assert old.startswith("// v58:"), f"Expected previous v58 filter: {path.name}"
    for required in (
        "ItemDisplay[GROUND MAG WEAPON]:",
        "ItemDisplay[GROUND MAG (ci2 OR ci3)]: %NAME%{%NAME%}",
        "ItemDisplay[GROUND (GLOVES OR BOOTS) (MAG OR NMAG)]:",
    ):
        assert required in old, (path.name, required)
    updated = header + old
    assert updated.count(selector) == 1
    path.write_text(updated, encoding="utf-8-sig")
    print("Updated", path.name, len(updated))
