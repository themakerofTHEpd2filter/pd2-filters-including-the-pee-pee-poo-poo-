from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files) == 5, "Expected five active filter variants"

# The ONLY overall score is max(actual caster formula, actual melee formula).
# Both source formulas have already been validated by PD2's BH Formula compiler.
score_token="%FORMULARARESCORE%"
combined_header=f"%TEAL%[Score {score_token}/7]%CL%"
combined_tip=(f"%TEAL%Score {score_token}/7 %TAN%"
              f"(C %FORMULARARECASTER% / M %FORMULARAREMELEE%)%CL%")
static_score=re.compile(r'\b(?:Score|Rating|Caster score|Melee score)\s*[0-9](?:\.[0-9]+)?(?:[-+][0-9.]+)?/7',re.I)

for p in files:
    raw=p.read_text(encoding="utf-8-sig")
    if raw.startswith("// v71:"):
        print("Already updated", p.name)
        continue
    assert raw.startswith("// v70:"), (p.name,"Expected v70")
    lines=raw.splitlines(keepends=True)
    formulas={}
    for line in lines:
        if line.startswith("Formula[") and "]: " in line:
            name=line.split("]:",1)[0][8:]
            formulas[name]=line.split("]: ",1)[1].strip()
    assert "RARESCORE" not in formulas, p.name
    assert {"RARECASTER","RAREMELEE"} <= formulas.keys(),p.name
    exact=(f"Formula[RARESCORE]: MAX({formulas['RARECASTER']},{formulas['RAREMELEE']})\n")
    score_count=hover_count=removed_legacy=priority_count=obsolete_count=0
    patched=[]
    inserted=False
    for line in lines:
        if line.startswith("Formula[RAREMELEE]: "):
            patched.append(line)
            patched.append(exact)
            inserted=True
            continue
        if not line.startswith("ItemDisplay[") or "]:" not in line:
            patched.append(line)
            continue
        sel,action=line.split("]:",1)
        # These legacy V21 hover rules contain stale hard-coded 0.5-score bands,
        # sometimes mislabeled a full 0.5 below their actual numeric predicate.
        # They have no other stat/key-information and are redundant.
        if "V21_SCORE_HOVER_" in sel and not sel.startswith("ItemDisplay[V21_SCORE_HOVER_ RARE "):
            if static_score.search(action):
                removed_legacy+=1
                continue
        if sel.startswith("ItemDisplay[V21_SCORE_HOVER_ RARE "):
            action=f"%NAME%%CONTINUE%{{{combined_tip}%NAME%}}\n"
            hover_count+=1
        # Replace v69 duplicate C/M score labels in the ground-priority selectors.
        elif "V19_GROUND_PRIORITY_" in sel and (
            "FORMULARARECASTERHUNDREDTHS" in sel or "FORMULARAREMELEEHUNDREDTHS" in sel
        ):
            action=action.replace("%TEAL%[C %FORMULARARECASTER%/7 M %FORMULARAREMELEE%/7]%CL%",combined_header)
            action=action.replace("%CL%%TEAL%%TEAL%C %FORMULARARECASTER%/7 | M %FORMULARAREMELEE%/7%CL%",f"%CL%%TEAL%Score {score_token}/7%CL%")
            action=action.replace("%TEAL%%TEAL%C %FORMULARARECASTER%/7 | M %FORMULARAREMELEE%/7%CL%",f"%TEAL%Score {score_token}/7%CL%")
            priority_count+=1
        # Any remaining 4.8+ label is merely a threshold, NOT an item's grade.
        # Preserve the rule's scope and %CONTINUE%, but show its real formula.
        if "4.8+/7" in action:
            if re.search(r'\bGROUND\b',sel) and not re.search(r'!GROUND',sel):
                action=f"{combined_header} %NAME%%CONTINUE%{{%NAME%}}\n"
            else:
                action=f"%NAME%%CONTINUE%{{{combined_tip}%NAME%}}\n"
            obsolete_count+=1
        if static_score.search(action):
            # A remaining fixed score is disallowed: it can disagree with the
            # actual score. Safely replace label-only actions, not hide rules.
            action=f"%NAME%%CONTINUE%{{{combined_tip}%NAME%}}\n"
            obsolete_count+=1
        if score_token in action: score_count+=1
        patched.append(sel+"]: "+action.lstrip() if action.startswith(" ") else sel+"]:"+action)
    assert inserted,p.name
    assert hover_count==15,(p.name,hover_count)
    assert removed_legacy>=20,(p.name,removed_legacy)
    assert priority_count>=10,(p.name,priority_count)
    assert obsolete_count>=10,(p.name,obsolete_count)
    output="// v71: One exact 0-7 rating everywhere; obsolete score bands and 4.8+ labels removed.\n"+"".join(patched)
    assert output.count("Formula[RARESCORE]:")==1,p.name
    assert "4.8+/7" not in output,p.name
    assert all(not static_score.search(line.partition("]:")[2]) for line in output.splitlines() if line.startswith("ItemDisplay[") and "]:" in line),p.name
    assert "ItemDisplay[GROUND UNI !ID !ALLDISCOVERED !jew]:" in output,p.name
    assert "ItemDisplay[GROUND NMAG (ci0 OR ci1 OR ci2 OR ci3)]:" in output,p.name
    p.write_text(output,encoding="utf-8-sig")
    print("Updated",p.name,"15 exact hover rules",priority_count,"ground priority rules",obsolete_count,"threshold-only displays",removed_legacy,"obsolete hover rules","dynamic labels:",score_count)
