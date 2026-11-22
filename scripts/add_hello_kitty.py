from pathlib import Path
root = Path(__file__).resolve().parents[1]
source = root / "Hiim-Hyper-Tailored-.filter"
dest = root / "Hiim-Hyper-Hello-Kitty.filter"
s = source.read_text(encoding="utf-8-sig")
lines = s.splitlines(keepends=True)
out = []
count = 0
for line in lines:
    if line.startswith("ItemDisplayFilterName[]:"):
        line = line.replace("High roller", "Hello Kitty - High Roller").replace("Min Mapper", "Hello Kitty - Min Mapper")
    # Presentation-only changes: selectors and visibility conditions are untouched.
    if line.startswith("ItemDisplay[") and "]:" in line:
        selector, display = line.split("]:", 1)
        ground_style = ("GROUND" in selector and "%NAME%" in display and "%CONTINUE%" in display)
        scored = ("TAILORED_SCORED_GEAR" in selector or "V19_GROUND_PRIORITY_" in selector)
        if ground_style and scored:
            # Pink-and-white kawaii highlights. Keep color distinction:
            # rare names stay yellow; unique names stay gold.
            display = display.replace("%TEAL%", "%PURPLE%").replace("%SAGE%", "%CORAL%")
            display = display.replace("%ORANGE%", "%CORAL%")
            # Decorate priority score labels only, not every tooltip or sublabel.
            if ("%BORDER-" in display or "FORMULARARECASTER%" in display or "FORMULARAREMELEE%" in display):
                display = "%CORAL%[=^.^=]%WHITE% " + display
            count += 1
        if "GROUND" in selector and "UNI" in selector and "%NAME%" in display and "%CONTINUE%" in display:
            display = display.replace("%TEAL%", "%PURPLE%").replace("%SAGE%", "%CORAL%")
        line = selector + "]:" + display
    out.append(line)
theme = (
    "// Hello Kitty-inspired pastel pink, white and bow-accented score labels.\n"
    "// Based on v50 Tailored: identical visibility, 2.50 rare threshold, and item scoring.\n"
    "// Rare names remain visually distinct from gold uniques. Decorations do not change drops.\n"
)
dest.write_text(theme + "".join(out), encoding="utf-8-sig")
print(f"Generated {dest.name} with {count} scored ground-label color changes.")

# Trigger generation after workflow registration.
