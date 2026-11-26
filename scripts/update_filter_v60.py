from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files) >= 5, "Missing active filter variants"

score_expr = re.compile(r'\$f\(ROUND\((RARECASTERHUNDREDTHS|RAREMELEEHUNDREDTHS|RAREDROPBEST)\)/100\)')
# The engine prints these expressions literally; infer a conservative
# band from the rule selector instead of trying to evaluate them in display.
def band(selector, formula):
    bounds = [int(v)+1 for v in re.findall(r'FORMULA' + re.escape(formula) + r'>(\d+)', selector)]
    lower = max(bounds) if bounds else None
    if lower is None:
        # Don't misstate an exact value when the selector lacks a floor.
        return "scored"
    return f"{lower / 100:.1f}+"

for path in files:
    original = path.read_text(encoding="utf-8-sig")
    if original.startswith("// v60:"):
        print("Already fixed", path.name)
        continue
    assert original.startswith("// v59:"), "Expected v59 baseline: " + path.name
    lines = []
    updated_expressions = 0
    isolated_rules = 0
    for line in original.splitlines(keepends=True):
        if not line.startswith("ItemDisplay[") or "]:" not in line:
            lines.append(line)
            continue
        selector, display = line.split("]:", 1)
        # V19 and V21 originally supply rare score formulas, but some
        # overrides also fire on UNI rin. Apply them only to rolled rares
        # and crafts. This preserves the existing unique-jewelry styling.
        if ("V19_GROUND_PRIORITY_" in selector or "V21_SCORE_HOVER_" in selector) and ("RAREMELEEHUNDREDTHS" in selector or "RARECASTERHUNDREDTHS" in selector):
            if not re.search(r'\b(RARE|CRAFT)\b', selector):
                selector = selector.replace("ItemDisplay[", "ItemDisplay[(RARE OR CRAFT) ", 1)
                isolated_rules += 1
        n = len(score_expr.findall(display))
        if n:
            display = score_expr.sub(lambda m: band(selector, m.group(1)), display)
            updated_expressions += n
        lines.append(selector + "]:" + display)
    patched = "// v60: Repair literal rare-score expressions; stop rare/craft score overlays on unique rings.\n" + "".join(lines)
    assert "$f(ROUND(RARE" not in patched, path.name
    assert "ItemDisplay[GROUND UNI !ETH (7sm OR 7vo" in patched
    assert "ItemDisplay[GROUND MAG (ci2 OR ci3)]:" in patched
    path.write_text(patched, encoding="utf-8-sig")
    print(path.name, "replaced", updated_expressions, "score expressions; isolated", isolated_rules, "rare score rules")
