from pathlib import Path
import re, subprocess

root=Path(__file__).resolve().parents[1]
s=(root/'Hiim-Hyper-Tailored-.filter').read_text(encoding='utf-8-sig')
want={'RAREMELEE':4.6,'RAREMELEEHUNDREDTHS':460.0,'RARESCORE':4.6,'RAREDROPBEST':460.0}
defs={}
for line in s.splitlines():
 if line.startswith('Formula[') and ']: ' in line:
  name=line.split(']: ',1)[0][8:]
  if name in want:
   defs[name]=line.split(']: ',1)[1]
assert len(defs)==4,defs.keys()
functions={'if','max','min','and','or','ln','exp','floor','ceil','round','mod','average','sqrt','pow','count','countif','xor','abs','sign'}
variables=set()
for body in defs.values():
 variables.update(token for token in re.findall(r'[a-zA-Z_]+',body.lower()) if token not in functions)
resolve_override={'helm':'resolve_helm','rare':'resolve_helm','id':'resolve_helm',
                  'sock':'resolve_sockets','tabsk':'resolve_tabs','stat':'resolve_stat','edam':'resolve_edam',
                  'res':'resolve_res'}
init=''.join('  reg.emplace(L"%s", FormulaVarDefinition<Dummy>(%d, &%s));\n' % (
    v,
    2 if v=='multi' else 1 if v in ('stat','sk','tabsk','clsk','os','charstat','chsk') else 0,
    resolve_override.get(v,'resolve_zero')) for v in sorted(variables))
cpp = r"""
#include <limits>
#include <cmath>
#include <cwchar>
#include <iostream>
#include <string>
#include <memory>
#include <vector>
#include <unordered_map>
#include "Formula.h"
struct Dummy {};
static std::wstring scenario=L"grand";
float resolve_zero(FormulaStatus &,Dummy *,const std::vector<int>&) { return 0; }
float resolve_helm(FormulaStatus &,Dummy *,const std::vector<int>&) { return 1; }
float resolve_sockets(FormulaStatus &,Dummy *,const std::vector<int>&) { return scenario==L"grand"?2:scenario==L"strong"?3:0; }
float resolve_tabs(FormulaStatus &,Dummy *,const std::vector<int>& p) {
 return (scenario==L"grand" && p.size() && p[0]==32) ? 2:0;
}
float resolve_stat(FormulaStatus &,Dummy *,const std::vector<int>& p) {
 if(p.size()==0) return 0;
 if(scenario==L"grand") { if(p[0]==136) return 13; if(p[0]==36) return 10; }
 if(scenario==L"strong") { if(p[0]==141) return 25; if(p[0]==136) return 25; if(p[0]==36) return 20; }
 return 0;
}
float resolve_edam(FormulaStatus &,Dummy *,const std::vector<int>&) { return scenario==L"strong"?250:0; }
float resolve_res(FormulaStatus &,Dummy *,const std::vector<int>&) { return scenario==L"strong"?25:0; }
int main(int argc,char** argv) {
 if (argc>1 && std::string(argv[1])=="junk") scenario=L"junk";
 else if(argc>1 && std::string(argv[1])=="strong") scenario=L"strong";
 std::unordered_map<std::wstring, FormulaVarDefinition<Dummy>> reg;
""" + init + r"""
 std::wstring raw;
 for(wchar_t c;std::wcin.get(c);)raw+=c;
 std::unique_ptr<Formula<Dummy>> out;
 auto status=Formula<Dummy>::Compile(raw,out,reg);
 if(status!=FormulaStatus::OK){std::cout<<"NOT_COMPILED "<<int(status)<<"\n";return 2;}
 float value=0;
 auto e=out->execute(nullptr,value);
 std::cout<<int(e)<<" "<<value<<"\n";
 return e==FormulaStatus::OK?0:3;
}
"""
Path('/tmp/helm_fixture.cpp').write_text(cpp)
r=subprocess.run(['g++','-std=c++17','-O0','-I/tmp','/tmp/helm_fixture.cpp','-o','/tmp/helm_fixture'],capture_output=True,text=True)
assert r.returncode==0, r.stderr[-1400:]
print('COMPILED_FICTURES')
for name,body in defs.items():
 for case in ['grand','junk','strong']:
  p=subprocess.run(['/tmp/helm_fixture',case],input=body,capture_output=True,text=True)
  assert p.returncode==0,(name,case,p.stdout,p.stderr)
  status,value=p.stdout.strip().split()
  val=float(value)
  assert status=='0'
  print('FIXTURE',name,case,val)
  if case=='grand': assert abs(val-want[name])<0.015,(name,case,val,want[name])
  if case=='junk': assert val==0,(name,case,val)
  if case=='strong': assert val>=want[name] and val<= (7.01 if name in ('RAREMELEE','RARESCORE') else 701),(name,case,val)
