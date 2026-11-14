# Insert generator output into index.html: python3 tools/fp-insert.py <generator.py> [strip names] ...
# Replaces existing lines for the generated keys (placed before 'TL Audio VTC'). Optional args after the generator:
#   --gear 'Kategorie|Hersteller|Modell' (adds to GEAR_DB) and --builtin 'Kategorie|Gerätename' (adds to the builtin list).
import subprocess, sys, json, re
gen=sys.argv[1]; args=sys.argv[2:]
out=subprocess.check_output(['python3',gen]).decode()
keys=[json.loads(l.split(':',1)[0].strip()) for l in out.splitlines()]
s=open('index.html',encoding='utf-8').read()
L=[l for l in s.split('\n') if not any(l.startswith('  '+json.dumps(k)+':') for k in keys)]
s='\n'.join(L); a="  'TL Audio VTC': {"; i=s.index(a); s=s[:i]+out+s[i:]
it=iter(args)
for flag in it:
    val=next(it)
    if flag=='--gear':
        cat,man,mod=val.split('|')
        m=re.search(r"\n  '"+re.escape(cat)+r"': \{\n    (.*)\n  \},",s)
        line=m.group(1)
        if f"['{mod}', 'hw']" in line and f"'{man}'" in line: continue
        mm=re.search(r"'"+re.escape(man)+r"': \[(.*?)\]\](,|$)",line)
        if mm: new=line[:mm.end(1)]+f"], ['{mod}', 'hw'"+line[mm.end(1):]
        else: new=line+f", '{man}': [['{mod}', 'hw']]"
        s=s[:m.start(1)]+new+s[m.end(1):]
    elif flag=='--builtin':
        cat,name=val.split('|')
        m=re.search(r"\n  '"+re.escape(cat)+r"': \[('TL Audio VTC.*)\]",s)
        if f"'{name}'" in m.group(1): continue
        s=s[:m.end(1)]+f", '{name}'"+s[m.end(1):]
open('index.html','w',encoding='utf-8').write(s)
print('inserted',keys)
