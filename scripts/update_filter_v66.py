from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files) == 5, "Expected five active variants"

# Restore honest rating bands from the existing score predicates.
# The game's display parser previously printed the inline $f() expressions as
# text. Use only static band text computed at build-time from selector bounds.
threshold = re.compile(r'FORMULARARE(?:CASTER|MELEE|DROPBEST)HUNDREDTHS>([0-9]+)')
def rating_floor(selector):
    vals = [int(x) for x in threshold.findall(selector)]
    if not vals:
        return None
    # The V21 bands explicitly bound the score into 0.5-wide intervals.
    return max(vals) // 50 * 0.5

for path in files:
    old = path.read_text(encoding="utf-8-sig")
    if old.startswith("// v66:"):
        print("Already patched", path.name)
        continue
    assert old.startswith("// v65:"), f"Missing v65 baseline: {path.name}"
    out = []
    restored = 0
    for line in old.splitlines(keepends=True):
        if not line.startswith("ItemDisplay[") or "]:" not in line:
            out.append(line)
            continue
        sel, display = line.split("]:", 1)
        # v62 wiped tooltips for these originally scored rules; reattach
        # score band without restoring unsupported expressions.
        if ("V21_SCORE_HOVER_" in sel or "V19_GROUND_PRIORITY_" in sel) and "FORMULARARE" in sel:
            floor = rating_floor(sel)
            if floor is not None:
                floor = max(2.5, min(7.0, floor))
                high = min(7.0, floor + .49)
                label = f"Score {floor:.1f}-{high:.2f}/7" if high < 7 else "Score 7/7"
                clean = display.rstrip("\r\n")
                if clean == "%NAME%%CONTINUE%{%NAME%}":
                    display = f"%NAME%%CONTINUE%{{%TEAL%{label}%CL%%NAME%}}\n"
                else:
                    # Preserve original other labels such as T4 and ED.
                    if clean.endswith("}") and "%CONTINUE%{" in clean:
                        clean = clean[:-1] + f"%CL%%TEAL%{label}" + "}"
                        display = clean + "\n"
                    else:
                        out.append(line)
                        continue
                restored += 1
        out.append(sel + "]:" + display)
    new = "// v66: Restored rare/crafted tooltip score bands using existing scoring thresholds; no dynamic $f markup.\n" + "".join(out)
    assert restored >= 15, f"Too few score rules restored in {path.name}: {restored}"
    assert "$f(ROUND(RARE" not in new
    assert "ItemDisplay[GROUND NMAG (ci0 OR ci1 OR ci2 OR ci3)]:" in new
    path.write_text(new, encoding="utf-8-sig")
    print(path.name, "score bands restored", restored)
