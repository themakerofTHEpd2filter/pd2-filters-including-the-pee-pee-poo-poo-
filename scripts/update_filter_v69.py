from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files) == 5, "Expected exactly five active filters"

# These are real evaluated PD2 Formula[] outputs, NOT literal $f() and
# NOT fixed score bands. The existing formulas calculate an item's score.
caster = "%FORMULARARECASTER%"
melee = "%FORMULARAREMELEE%"
short = f"%TEAL%[C {caster}/7 M {melee}/7]%CL%"
detail = f"%TEAL%C {caster}/7 | M {melee}/7%CL%"
score_pattern = re.compile(r'(?:Rating|Score) \d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?/7')

for p in files:
    original = p.read_text(encoding="utf-8-sig")
    if original.startswith("// v69:"):
        print("Already patched", p.name)
        continue
    assert original.startswith("// v68:"), f"Unexpected starting version: {p.name}"
    for name in ("RARECASTER", "RAREMELEE"):
        assert original.count(f"Formula[{name}]:") == 1, (p.name, name)

    lines = []
    hover = ground = ground_priority = 0
    for line in original.splitlines(keepends=True):
        if not line.startswith("ItemDisplay[") or "]:" not in line:
            lines.append(line)
            continue
        selector, display = line.split("]:", 1)
        if selector.startswith("ItemDisplay[V21_SCORE_HOVER_ RARE "):
            # Every band already matches computed formula thresholds.
            # Replace only the explanatory text with the real formula value.
            old = score_pattern.findall(display)
            assert len(old) == 1, (p.name, selector[:90], old)
            display = score_pattern.sub(detail, display)
            hover += 1
        elif "V19_GROUND_PRIORITY_" in selector and (
            "FORMULARARECASTERHUNDREDTHS" in selector or
            "FORMULARAREMELEEHUNDREDTHS" in selector
        ) and "RARE" in selector:
            # Preserve the existing priority, color and extra stats.
            # Put actual C/M numbers directly in ground name, not just hover.
            # Stale band snippets in tooltip are also removed.
            display = score_pattern.sub(detail, display)
            if "%CONTINUE%" in display:
                name, rest = display.split("%CONTINUE%", 1)
                # The old bracket tier markers must not masquerade as actual score.
                name = re.sub(r'\[(?:7|[2-6](?:\.\d)?\+?)\]', '', name)
                if caster not in name and melee not in name:
                    name = name.rstrip() + " " + short
                display = name + "%CONTINUE%" + rest
                ground_priority += 1
        lines.append(selector + "]:" + display)

    # Guaranteed exact label for any scored rare not covered by V19 rules;
    # it is placed just before the existing inventory hover rules.
    # It uses %CONTINUE% so other item-detail decorators still operate.
    joined = "".join(lines)
    anchor = "Alias[V21_SCORE_HOVER_]:"
    assert joined.count(anchor) == 1, (p.name, "missing hover anchor")
    supplemental = (
        "// v69: Exact score on scored rare ground items; no approximation.\n"
        "ItemDisplay[GROUND RARE ID TAILORED_SCORED_GEAR "
        "(FORMULARARECASTERHUNDREDTHS>0 OR FORMULARAREMELEEHUNDREDTHS>0)]: "
        f"%NAME% {short}%CONTINUE%{{%NAME%}}\n"
    )
    # Keep supplemental after higher-priority visual rules but before hover section.
    joined = joined.replace(anchor, supplemental + anchor, 1)
    ground += 1

    updated = "// v69: Restored exact caster and melee formula scores (out of 7) in ground labels and hover.\n" + joined
    assert hover == 15, (p.name, hover)
    assert ground_priority >= 10, (p.name, ground_priority)
    assert updated.count("Formula[RARECASTER]:") == 1
    assert updated.count("Formula[RAREMELEE]:") == 1
    assert updated.count(supplemental) == 1
    assert "Rating 4.5-4.99/7" not in updated
    assert "$f(ROUND(RARE" not in updated
    assert "ItemDisplay[GROUND UNI !ID !ALLDISCOVERED !jew]:" in updated
    p.write_text(updated, encoding="utf-8-sig")
    print("Updated", p.name, "exact hover rules:", hover, "ground priority labels:", ground_priority, "ground fallback:", ground)
