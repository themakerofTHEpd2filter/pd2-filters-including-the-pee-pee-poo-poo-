from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = sorted(root.glob("Hiim-Hyper-*.filter"))

# This scores rolled damage/DS/CB together with sockets and resistance.
# A near-perfect ED + DS + 3 sockets + 25 all res helm reaches ~6.5 / 7.
# 20 ED + 10 DS + 2 sockets + 15 all res gets ~4.55 / 7.
helm = (
    "IF(AND(HELM,!CIRC,!DRU,!BAR,RARE,ID,"
    "OR(AND(EDAM>=10,MAX(STAT141,STAT136)>=5),"
    "AND(EDAM>=20,SOCK>=3,RES>=10),"
    "AND(STAT141>=15,SOCK>=3,RES>=10))),"
    "MIN(690,175+MIN(100,EDAM*3)+MIN(160,STAT141*8)"
    "+MIN(115,STAT136*6)"
    "+IF(SOCK>=3,120,IF(SOCK>=2,65,IF(AND(SOCK=0,MAXSOCKETS>=3),85,0)))"
    "+IF(RES>=25,105,IF(RES>=15,75,IF(RES>=8,40,0)))"
    "+IF(FHR>=15,25,0)),0)"
)

def change_one(s, before, after, tag):
    n = s.count(before)
    if n != 1:
        raise ValueError(f"{tag}: expected one match, found {n}: {before[:80]}")
    return s.replace(before, after, 1)

for p in files:
    s = p.read_text(encoding="utf-8-sig")
    if s.startswith("// v51:"):
        print("Already patched:", p.name)
        continue

    # Keep top-end / specialist unique belts. Everything else stays suppressed.
    # Item codes come from the existing base-to-unique mapping.
    best_belts = "(zlb OR zvb OR ztb OR zhb OR ulc OR uvc OR umc OR utc OR uhc)"
    s = change_one(s, "ItemDisplay[GROUND BELT !UNI]:",
        "ItemDisplay[GROUND BELT !(UNI "+best_belts+")]:",p.name)
    # Unique rings, like unique amulets, should actually be visible.
    s = change_one(s, "ItemDisplay[GROUND rin]:",
        "ItemDisplay[GROUND rin !UNI]:",p.name)

    # Enhance only ground-drop unique rings and amulets, without changing their identity colors.
    anchor = "// v49: HARD SCORE CUTOFF ON IDENTIFIED SCORABLE EQUIPMENT."
    jewelry = (
        "// v51: More noticeable gold unique jewelry drops; preserve ID odds tooltips.\n"
        "ItemDisplay[GROUND UNI (amu OR rin)]: %BORDER-9B%%MAP-9B%%DOT-9B%%GOLD%* %NAME% *%CONTINUE%{%NAME%}\n"
    )
    s = change_one(s, anchor, jewelry + anchor, p.name)

    # Do not allow identified rare mauls to bypass later weapon hide rules.
    s = change_one(s,
        "ItemDisplay[GROUND TAILORED_ALWAYS_SHOW_MAUL]: %NAME%{%NAME%}",
        "ItemDisplay[GROUND RARE !ID TAILORED_ALWAYS_SHOW_MAUL]: %NAME%{%NAME%}",
        p.name)

    # Previously these two later rules used the maul exemption even after ID.
    for before in (
        "FILTLVL>6 (MAG OR RARE OR CRAFT) WEAPON ID !(EDAM>419",
        "FILTLVL>4 FILTLVL<7 (MAG OR RARE OR CRAFT) WEAPON ID !(",
    ):
        # Existing later broad weapon hide rules can still apply; no special maul exemption.
        pass
    s = s.replace("!TAILORED_ID_KEEP_ !TAILORED_ALWAYS_SHOW_MAUL]:",
                  "!TAILORED_ID_KEEP_]:")
    # An earlier rare unid maul rule remains intentionally.

    lines = s.splitlines(keepends=True)
    for name, divided in (
        ("RAREMELEEHUNDREDTHS", False),
        ("RAREMELEE", True),
        ("RAREDROPBEST", False),
    ):
        prefix = "Formula[" + name + "]: "
        ix = [i for i, line in enumerate(lines) if line.startswith(prefix)]
        if len(ix) != 1:
            raise ValueError("Missing/ambiguous score formula: " + name)
        i = ix[0]
        body = lines[i][len(prefix):].rstrip("\r\n")
        ending = lines[i][len(prefix)+len(body):]
        floor = "(" + helm + ")/100" if divided else helm
        lines[i] = prefix + "MAX(" + body + "," + floor + ")" + ending

    s = (
        "// v51: Unique jewelry highlights; premium belts; helms ED+DS/CB+sockets+res; identified mauls scored normally.\n"
        + "".join(lines)
    )
    p.write_text(s, encoding="utf-8-sig")
    print("Updated", p.name, "bytes", len(s))

assert len(files) >= 5, f"Expected five active filter variants, found {len(files)}"

# Regenerate filters when this v51 script changes.
