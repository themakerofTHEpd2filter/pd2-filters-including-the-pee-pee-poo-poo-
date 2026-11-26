from pathlib import Path

root=Path(__file__).resolve().parents[1]
files=sorted(root.glob("Hiim-Hyper-*.filter"))
assert len(files)==5, "Expected five variants"
anchor="ItemDisplay[GROUND SET !ID ALLDISCOVERED !ALLOWNED]: %WHITE%GRAIL %GREEN%%NAME%{%NAME%}\n"
exception="ItemDisplay[GROUND UNI drd]: %GOLD%Spirit Keeper%CONTINUE%{%NAME%}\n"
for path in files:
    old=path.read_text(encoding="utf-8-sig")
    if old.startswith("// v75:"):
        print("Already updated",path.name)
        continue
    assert old.startswith("// v74:"), ("Expected v74",path.name)
    assert old.count(anchor)==1, path.name
    assert old.count("Alias[4_STAR_UNIQUE]:")==1 and old.count("Alias[4_STAR_ETH_UNIQUE]:")==1, path.name
    for alias in ("Alias[4_STAR_UNIQUE]:","Alias[4_STAR_ETH_UNIQUE]:"):
        line=next(l for l in old.splitlines() if l.startswith(alias))
        assert " drd " in line, (path.name,alias)
    assert exception not in old
    new=old.replace(anchor,anchor+"// v75: Explicitly show Hiim 4-star Spirit Keeper on the ground, while Grail labels take priority.\n"+exception,1)
    new="// v75: Protect Spirit Keeper (Earth Spirit, drd) in both normal and ethereal unique variants.\n"+new
    assert new.index(exception)<new.index("ItemDisplay[GROUND UNI !ETH !(4_STAR_UNIQUE")
    assert new.index(anchor)<new.index(exception)
    assert new.count(exception)==1
    path.write_text(new,encoding="utf-8-sig")
    print("Updated",path.name)
