from pathlib import Path
import re, subprocess
root=Path(__file__).resolve().parents[1]
source=(root/'Hiim-Hyper-Tailored-.filter').read_text(encoding='utf-8-sig')
names={'RARECASTER','RAREMELEE','RARECASTERHUNDREDTHS','RAREMELEEHUNDREDTHS','RARESCORE','RAREDROPBEST'}
defs={}
for line in source.splitlines():
 if line.startswith("Formula[") and "]: " in line:
  k,v=line.split("]: ",1)
  if k[8:] in names:defs[k[8:]]=v
assert set(defs)==names,defs.keys()
functions={'if','max','min','and','or','ln','exp','floor','ceil','round','mod','average','sqrt','pow','count','countif','xor','abs','sign'}
vars=set()
for v in defs.values():vars.update(x for x in re.findall(r'[a-zA-Z_]+',v.lower()) if x not in functions)
init=''.join('reg.emplace(L"%s",FormulaVarDefinition<Dummy>(%d,&resolve));\n' %
 (v,2 if v=='multi' else 1 if v in ('stat','sk','tabsk','clsk','os','charstat','chsk') else 0)
 for v in sorted(vars))
# Since the engine resolves variables by registered function pointer, create one
# callback for each variable used in the simulated scenarios.
specific={'chest','rare','id','fcr','str','cres','res','stat','edam','clsk3','sock','helm'}
init=''.join('reg.emplace(L"%s",FormulaVarDefinition<Dummy>(%d,&%s));\n' %
 (v,2 if v=='multi' else 1 if v in ('stat','sk','tabsk','clsk','os','charstat','chsk') else 0,
 'get_'+v if v in specific else 'get_zero') for v in sorted(vars))
funcs="""
float get_zero(FormulaStatus &,Dummy *,const std::vector<int>&){return 0;}
float get_chest(FormulaStatus &,Dummy *,const std::vector<int>&){return 1;}
float get_rare(FormulaStatus &,Dummy *,const std::vector<int>&){return 1;}
float get_id(FormulaStatus &,Dummy *,const std::vector<int>&){return 1;}
float get_helm(FormulaStatus &,Dummy *,const std::vector<int>&){return 0;}
float get_fcr(FormulaStatus &,Dummy *,const std::vector<int>&){return scenario==L"fcr"?20:0;}
float get_str(FormulaStatus &,Dummy *,const std::vector<int>&){return scenario==L"fcr"?19:9;}
float get_cres(FormulaStatus &,Dummy *,const std::vector<int>&){return scenario==L"fcr"?15:(scenario==L"ed"?26:0);}
float get_res(FormulaStatus &,Dummy *,const std::vector<int>&){return scenario==L"ed"?26:0;}
float get_edam(FormulaStatus &,Dummy *,const std::vector<int>&){return scenario==L"ed"?155:0;}
float get_sock(FormulaStatus &,Dummy *,const std::vector<int>&){return 0;}
float get_clsk3(FormulaStatus &,Dummy *,const std::vector<int>&){return scenario==L"ed"?1:0;}
float get_stat(FormulaStatus &,Dummy *,const std::vector<int>& p){
 if(p.empty()) return 0;
 if(scenario==L"fcr" && p[0]==86) return 4;
 if(scenario==L"ed" && p[0]==110) return 25;
 return 0;
}
"""
cpp=r"""
#include <iostream>
#include <memory>
#include <vector>
#include <unordered_map>
#include <cwchar>
#include <cmath>
#include <string>
#include "Formula.h"
struct Dummy{};
static std::wstring scenario=L"fcr";
""" + funcs + r"""
int main(int argc,char**argv){
 if(argc>1 && std::string(argv[1])=="ed")scenario=L"ed";
 else if(argc>1 && std::string(argv[1])=="junk")scenario=L"junk";
 std::unordered_map<std::wstring,FormulaVarDefinition<Dummy>> reg;
 """+init+r"""
 std::wstring raw;
 for(wchar_t c;std::wcin.get(c);)raw+=c;
 std::unique_ptr<Formula<Dummy>> out;
 auto st=Formula<Dummy>::Compile(raw,out,reg);
 if(st!=FormulaStatus::OK){std::cout<<"COMPILE_FAILED "<<int(st)<<"\n";return 2;}
 float v=0;
 auto e=out->execute(nullptr,v);
 std::cout<<int(e)<<" "<<v<<"\n";
 return e==FormulaStatus::OK?0:3;
}
"""
Path('/tmp/armor_fixture.cpp').write_text(cpp)
r=subprocess.run(['g++','-std=c++17','-O0','-I/tmp','/tmp/armor_fixture.cpp','-o','/tmp/armor_fixture'],capture_output=True,text=True)
assert r.returncode==0,r.stderr[-1900:]
for name,formula in defs.items():
 for case in ['fcr','ed','junk']:
  p=subprocess.run(['/tmp/armor_fixture',case],input=formula,capture_output=True,text=True)
  assert p.returncode==0,(name,case,p.stdout,p.stderr)
  status,val=p.stdout.strip().split()
  value=float(val)
  assert status=='0'
  print('ARMOR_FIXTURE',name,case,value)
  if case=='fcr':
   if name in ('RARECASTER','RARESCORE'): assert 2.74<=value<=5,(name,value)
   if name in ('RARECASTERHUNDREDTHS','RAREDROPBEST'):assert 274<=value<=500,(name,value)
  if case=='ed':
   if name in ('RAREMELEE','RARESCORE'):assert 4.74<=value<=6,(name,value)
   if name in ('RAREMELEEHUNDREDTHS','RAREDROPBEST'): assert 474<=value<=600,(name,value)
  if case=='junk':assert value==0,(name,value)
