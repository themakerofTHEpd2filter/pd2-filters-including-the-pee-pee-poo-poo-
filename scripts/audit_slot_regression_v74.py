from pathlib import Path
import re, subprocess
root=Path(__file__).resolve().parents[1]
s=(root/'Hiim-Hyper-Tailored-.filter').read_text(encoding='utf-8-sig')
wanted={'RARECASTER','RAREMELEE','RARESCORE'}
d={}
for line in s.splitlines():
 if line.startswith("Formula[") and "]: " in line:
  name,formula=line.split("]: ",1)
  if name[8:] in wanted:d[name[8:]]=formula
assert set(d)==wanted
functions={'if','max','min','and','or','ln','exp','floor','ceil','round','mod','average','sqrt','pow','count','countif','xor','abs','sign'}
names=set()
for expr in d.values():names.update(x for x in re.findall(r'[a-zA-Z_]+',expr.lower()) if x not in functions)
special=set("boots gloves belt jewelry misc quiver rare id fcr fbr ias edam frw fhr res cres str dex life ar maek stat clsk sock".split())
init="".join('reg.emplace(L"%s",FormulaVarDefinition<Dummy>(%d,&%s));\n'%(v,1 if v in ('stat','sk','tabsk','clsk','os','charstat','chsk') else 2 if v=='multi' else 0,'get_'+v if v in special else 'zero') for v in sorted(names))
getters=r'''
float zero(FormulaStatus&,Dummy*,const std::vector<int>&){return 0;}
float get_rare(FormulaStatus&,Dummy*,const std::vector<int>&){return 1;}
float get_id(FormulaStatus&,Dummy*,const std::vector<int>&){return 1;}
float get_boots(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="boots";}
float get_gloves(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="gloves";}
float get_belt(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="belt";}
float get_jewelry(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="amulet";}
float get_misc(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="jewel";}
float get_quiver(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="quiver";}
float get_fcr(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="gloves"||test=="amulet"?20:0;}
float get_fbr(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="gloves"?20:0;}
float get_ias(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="gloves"?20:(test=="jewel"?15:(test=="quiver"?30:0));}
float get_edam(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="jewel"?40:(test=="quiver"?150:0);}
float get_frw(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="boots"?40:0;}
float get_fhr(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="boots"||test=="belt"?30:0;}
float get_res(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="boots"?30:(test=="belt"?30:(test=="amulet"?20:10));}
float get_cres(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="boots"?30:0;}
float get_str(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="amulet"?20:10;}
float get_dex(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="quiver"?20:0;}
float get_life(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="boots"?30:0;}
float get_ar(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="quiver"?100:0;}
float get_maek(FormulaStatus&,Dummy*,const std::vector<int>&){return test=="gloves"?3:0;}
float get_sock(FormulaStatus&,Dummy*,const std::vector<int>&){return 0;}
float get_clsk(FormulaStatus&,Dummy*,const std::vector<int>&p){return test=="amulet"&&!p.empty()&&p[0]==3?2:0;}
float get_stat(FormulaStatus&,Dummy*,const std::vector<int>&p){
 if(p.empty())return 0;
 if(p[0]==102&&test=="gloves")return 20;
 if(p[0]==80&&test=="gloves")return 25;
 if(p[0]==36&&test=="belt")return 10;
 if(p[0]==110&&test=="belt")return 25;
 if(p[0]==136&&test=="jewel")return 10;
 return 0;
}
'''
cpp=r'''
#include <iostream>
#include <memory>
#include <vector>
#include <string>
#include <unordered_map>
#include <cwchar>
#include <cmath>
#include "Formula.h"
struct Dummy{};
static std::string test;
'''+getters+r'''
int main(int argc,char**argv){
 test=argc>1?argv[1]:"junk";
 std::unordered_map<std::wstring,FormulaVarDefinition<Dummy>> reg;
'''+init+r'''
 std::wstring expr;
 for(wchar_t c;std::wcin.get(c);)expr+=c;
 std::unique_ptr<Formula<Dummy>> compiled;
 auto st=Formula<Dummy>::Compile(expr,compiled,reg);
 if(st!=FormulaStatus::OK){std::cout<<"COMPILE_FAILED "<<int(st)<<"\n";return 2;}
 float score=0;
 auto er=compiled->execute(nullptr,score);
 std::cout<<int(er)<<" "<<score<<"\n";
 return er==FormulaStatus::OK?0:3;
}
'''
Path('/tmp/slot_fixture.cpp').write_text(cpp)
b=subprocess.run(['g++','-std=c++17','-O0','-I/tmp','/tmp/slot_fixture.cpp','-o','/tmp/slot_fixture'],capture_output=True,text=True)
assert b.returncode==0,b.stderr[-1800:]
for n in ["RARECASTER","RAREMELEE","RARESCORE"]:
 for case in ["jewel","gloves","boots","amulet","belt","quiver","junk"]:
  p=subprocess.run(['/tmp/slot_fixture',case],input=d[n],capture_output=True,text=True)
  assert p.returncode==0,(n,case,p.stdout,p.stderr)
  st,score=p.stdout.split()
  score=float(score)
  print("SLOT_FIXTURE",n,case,score)
  if case=="junk": assert score==0,(n,case,score)
  if n=="RARESCORE" and case!="junk": assert 1.0<score<=7.01,(n,case,score)
assert "Alias[V21_SCORE_HOVER_]: (!GROUND !SHOP FILTLVL>0 (TAILORED_SCORED_GEAR OR (MAG ID CHARM) OR (RARE ID BOOTS)))" in s
print("SLOT_TESTS_PASS")
