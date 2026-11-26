from pathlib import Path
import re, subprocess, urllib.request

repo = Path(__file__).resolve().parents[1]
s = (repo / 'Hiim-Hyper-Tailored-.filter').read_text(encoding='utf-8-sig')
keys = ['RARECASTER', 'RAREMELEE', 'RARECASTERHUNDREDTHS', 'RAREMELEEHUNDREDTHS', 'RAREDROPBEST']
defs = {}
for line in s.splitlines():
    if line.startswith('Formula[') and ']: ' in line:
        name = line.split(']: ', 1)[0].split('[', 1)[1]
        if name in keys:
            defs[name] = line.split(']: ', 1)[1]
assert len(defs)==len(keys),defs.keys()
source = 'https://raw.githubusercontent.com/Project-Diablo-2/BH/main/BH/Formula.h'
h = urllib.request.urlopen(source,timeout=25).read().decode('utf-8-sig')
h=h.replace('std::fmodf(', 'std::fmod(')
Path('/tmp/Formula.h').write_text(h)
variables=set()
functions={'if','max','min','and','or','ln','exp','floor','ceil','round','mod','average','sqrt','pow','count','countif','xor','abs','sign'}
for f in defs.values():
    variables.update(x for x in re.findall(r'[a-zA-Z_]+', f.lower()) if x not in functions)
# Add every referenced variable to the compiler registry; the real engine supplies them.
init = ''.join('  reg.emplace(L"%s", FormulaVarDefinition<Dummy>(%d, &resolve));\n' % (v, 2 if v=='multi' else 1 if v in ('stat','sk','tabsk','clsk','os','charstat','chsk') else 0) for v in sorted(variables))
cpp= r'''
#include <limits>
#include <cwchar>
#include <iostream>
#include <memory>
#include <unordered_map>
#include <vector>
#include "Formula.h"
struct Dummy {};
float resolve(FormulaStatus &s, Dummy *d,const std::vector<int>& p) { return 0; }
int main(int argc,char**argv) {
  std::unordered_map<std::wstring, FormulaVarDefinition<Dummy>> reg;
''' + init + r'''
  std::wstring raw;
  for (wchar_t c; std::wcin.get(c);) raw+=c;
  std::unique_ptr<Formula<Dummy>> out;
  auto st=Formula<Dummy>::Compile(raw, out, reg);
  std::wcout << L"COMPILE_STATUS " << static_cast<int>(st) << L'\n';
  if(st==FormulaStatus::OK) {
    float result=0;
    auto e=out->execute(nullptr,result);
    std::wcout<<L"EVAL_STATUS "<< static_cast<int>(e)<<L" VALUE "<<result<<L'\n';
  }
}
'''
Path('/tmp/test_formula.cpp').write_text(cpp)
r=subprocess.run(['g++','-std=c++17','-O0','-fmax-errors=2','-I/tmp','/tmp/test_formula.cpp','-o','/tmp/test_formula'],capture_output=True,text=True)
print('COMPILER_BUILD',r.returncode,r.stderr[-1300:])
if r.returncode:
    raise SystemExit(1)
for name, body in defs.items():
    p=subprocess.run(['/tmp/test_formula'],input=body,capture_output=True,text=True)
    print('ACTUAL_BH_PARSER',name,len(body),p.returncode,p.stdout.strip(),p.stderr[-200:])
