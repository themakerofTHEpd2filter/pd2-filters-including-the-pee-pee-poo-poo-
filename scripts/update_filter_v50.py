from pathlib import Path
root = Path(__file__).resolve().parents[1]
names = ["Hiim-Hyper-Glacial-Prismatic-Frost.filter","Hiim-Hyper-Tailored-.filter","Hiim-Hyper-Tailored-Poop-and-Pee-.filter"]
def update(s):
    if s.startswith("// v50:"): return s
    def rep(a,b):
        nonlocal s
        n=s.count(a)
        if n!=1: raise Exception(f"Expected exactly one match, got {n}: {a[:70]}")
        s=s.replace(a,b,1)
    rep("Alias[TAILORED_RARE_WEAPON_EXCEPTION]: (TAILORED_ALWAYS_SHOW_MAUL OR","Alias[TAILORED_RARE_WEAPON_EXCEPTION]: ((TAILORED_ALWAYS_SHOW_MAUL !ID) OR")
    rep("ItemDisplay[GROUND BELT]:","ItemDisplay[GROUND BELT !UNI]:")
    rep("TAILORED_V49_SCORED_EQUIPMENT !TAILORED_ALWAYS_SHOW_MAUL FORMULARARECASTERHUNDREDTHS<250","TAILORED_V49_SCORED_EQUIPMENT FORMULARARECASTERHUNDREDTHS<250")
    rep("FORMULARAREMELEEHUNDREDTHS<250 !TAILORED_ID_KEEP_ !TAILORED_ALWAYS_SHOW_MAUL]:","FORMULARAREMELEEHUNDREDTHS<250 !TAILORED_ID_KEEP_]:")
    rep("ItemDisplay[GROUND RARE ID !TAILORED_ALWAYS_SHOW_MAUL !TAILORED_ID_KEEP_","ItemDisplay[GROUND RARE ID !TAILORED_ID_KEEP_")
    rep("ItemDisplay[SUP !RW GROUND !(TAILORED_SUPERIOR_BEST OR TAILORED_SUPERIOR_HEAVY_ARMOR) !TAILORED_VISIBLE_PELT !TAILORED_ALWAYS_SHOW_MAUL]:","ItemDisplay[SUP !RW GROUND !(TAILORED_SUPERIOR_BEST OR TAILORED_SUPERIOR_HEAVY_ARMOR) !TAILORED_VISIBLE_PELT]:")
    rep("// v47: Ground items only; never obscure inventory or equipped items. All rarities.","// v50: Unidentified rare mauls retained; identified rare mauls obey 2.50 threshold.\nItemDisplay[GROUND RARE !ID TAILORED_ALWAYS_SHOW_MAUL]: %NAME%%CONTINUE%{%NAME%}\n// v47: Ground items only; never obscure inventory or equipped items. All rarities.")
    rep("// Mauls are intentionally exempt because the user expressly requested every Maul to show.","// Identified mauls are not exempt from the 2.50 score threshold.")
    rep("// Only Maul-family bases may bypass the v49 <2.50 identified-gear score gate.","// Identified mauls follow the usual 2.50 cutoff.")
    floor="IF(AND(CIRC,ID,RARE,OR(TABSK18>=2,TABSK8>=2,TABSK9>=2,TABSK10>=2)),IF(FCR>=20,480,IF(FCR>=10,430,350)),0)"
    lines=s.splitlines(keepends=True)
    for key,decimal in (("RARECASTERHUNDREDTHS",False),("RARECASTER",True),("RAREDROPBEST",False)):
        prefix=f"Formula[{key}]: "
        ix=[i for i,line in enumerate(lines) if line.startswith(prefix)]
        if len(ix)!=1: raise Exception("Formula not unique: "+key)
        i=ix[0]
        content=lines[i][len(prefix):].rstrip("\r\n")
        end=lines[i][len(prefix)+len(content):]
        lines[i]=f"{prefix}MAX({content},{'('+floor+')/100' if decimal else floor}){end}"
    return "// v50: Show unique belts; +2 Necro Summon/Sorc elemental circlets stronger; ID mauls require 2.5.\n"+''.join(lines)
for name in names:
    p=root/name
    s=p.read_text(encoding="utf-8-sig")
    new=update(s)
    p.write_text(new,encoding="utf-8-sig")
    print(name,"updated",len(new))
p=root/"Hiim-Hyper-Tailored-Blue-Jewels.filter"
s=(root/names[1]).read_text(encoding="utf-8-sig")
old="ItemDisplay[GROUND jew !(RARE OR UNI)]:"
assert s.count(old)==1
p.write_text(s.replace(old,"ItemDisplay[GROUND jew !(RARE OR UNI OR MAG)]:\nItemDisplay[GROUND jew MAG]: %BLUE%%NAME%%CONTINUE%{%NAME%}",1),encoding="utf-8-sig")
print("Blue-jewel variant generated")

# Trigger the v50 workflow after installation.
