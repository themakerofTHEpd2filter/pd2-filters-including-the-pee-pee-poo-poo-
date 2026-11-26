from pathlib import Path
root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files) >= 5, "Expected all five filter versions"
changed = 0
for path in files:
    original = path.read_text(encoding="utf-8-sig")
    if original.startswith("// v53:"):
        print("Already corrected:", path.name)
        continue
    lines = original.splitlines(keepends=True)
    fixed = []
    replacements = 0
    compacted = 0
    for line in lines:
        if not line.startswith("ItemDisplay[") or "]:" not in line:
            fixed.append(line)
            continue
        selector, display = line.split("]:", 1)
        # Some old rules insert BOTH the name and basename, causing overlapping text.
        # V19 priority rules also contain broken split lines and overlong score tooltips.
        if selector.startswith("ItemDisplay[V19_GROUND_PRIORITY_ (TAILORED_SCORED_GEAR OR CHARM)"):
            if "FORMULARARECASTERHUNDREDTHS" in selector and "FORMULARAREMELEEHUNDREDTHS" in selector:
                # Conditions retain the exact existing score thresholds and item styling.
                # Short name on ground; long stat breakdown is available on identification.
                import re
                numeric = re.findall(r"FORMULARARE(?:CASTER|MELEE)HUNDREDTHS>(\d+)", selector)
                tier = max(map(int,numeric)) if numeric else 249
                band = ("7" if tier >= 699 else "6.5+" if tier >= 649 else
                        "6+" if tier >= 599 else "5.5+" if tier >= 549 else
                        "5+" if tier >= 499 else "4.5+" if tier >= 449 else
                        "4+" if tier >= 399 else "3.5+" if tier >= 349 else "2.5+")
                old_colors = re.findall(r"%((?:CORAL|TEAL|PURPLE|GOLD|WHITE|GREEN|YELLOW|SAGE|ORANGE))%", display)
                color = old_colors[0] if old_colors else "WHITE"
                new_display = f"%{color}%[{band}] %NAME%%CONTINUE%{{%NAME%}}\n"
                fixed.append(selector + "]:" + new_display)
                compacted += 1
                continue
        # All other score labels use $f() inline expressions rather than literal
        # %FORMULA...% strings, which the PD2 display parser does not resolve.
        for name, expression in (
            ("%FORMULARAREMELEE%", "$f(ROUND(RAREMELEEHUNDREDTHS)/100)"),
            ("%FORMULARARECASTER%", "$f(ROUND(RARECASTERHUNDREDTHS)/100)"),
            ("%FORMULARAREDROPBEST%", "$f(ROUND(RAREDROPBEST)/100)"),
        ):
            n = display.count(name)
            if n:
                display = display.replace(name,expression)
                replacements += n
        fixed.append(selector + "]:" + display)
    updated = "// v53: Fix literal score placeholders and overly wide priority ground labels.\n" + "".join(fixed)
    if "%FORMULARAREMELEE%" in updated or "%FORMULARARECASTER%" in updated:
        raise ValueError("Unresolved score macro in " + path.name)
    path.write_text(updated, encoding="utf-8-sig")
    print(path.name, "score tokens fixed:", replacements, "priority labels compacted:", compacted)
    changed += 1
assert changed == len(files) or changed == 0
