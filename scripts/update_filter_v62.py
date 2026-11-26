from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files) >= 5, "Expected all five active versions"

for p in files:
    original = p.read_text(encoding="utf-8-sig")
    if original.startswith("// v62:"):
        print("Already patched", p.name)
        continue
    assert original.startswith("// v61:"), "Expected v61 baseline: " + p.name
    rebuilt = []
    malformed = 0
    tokens = 0
    for line in original.splitlines(keepends=True):
        if not line.startswith("ItemDisplay[") or "]:" not in line:
            rebuilt.append(line)
            continue
        selector, display = line.split("]:", 1)
        # Never let unsupported formula syntax reach the PD2 ground label.
        # Keep selectors and item visibility exactly as they were.
        if "$f(" in display:
            display = "%NAME%%CONTINUE%{%NAME%}\n"
            malformed += 1
        # Unresolved formula-as-a-text macros are not part of normal item names.
        # They were historically emitted literally on the ground.
        display, n = re.subn(r"%FORMULARARE(?:CASTER|MELEE|DROPBEST|SOCKETCOUNT)[A-Z]*%", "", display)
        tokens += n
        rebuilt.append(selector + "]:" + display)
    updated = "// v62: Verified label cleanup — no literal $f score expressions; v61 item rules retained.\n" + "".join(rebuilt)
    assert "$f(ROUND(RARE" not in updated
    assert not any("$f(" in l.split("]:",1)[1] for l in updated.splitlines() if l.startswith("ItemDisplay[") and "]:" in l)
    assert "ItemDisplay[GROUND SET (ghm OR fhl" in updated
    assert "ItemDisplay[GROUND MAG (ci2 OR ci3)]: %NAME%{%NAME%}" in updated
    p.write_text(updated, encoding="utf-8-sig")
    print(p.name, "malformed ground displays replaced", malformed, "literal score tokens removed", tokens)
