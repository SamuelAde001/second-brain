# build3.py name... -> data_<start>.json (plan per adjustment clip) and a data .comp carrying it in a Note
import sys, json
import gen, spec2, subprocess
for name in sys.argv[1:]:
    f0, f1, track = spec2.S[name]
    p = gen.plan(track, spec2.B.get(name, []), [(f0, f1)])[0]
    js = json.dumps(p, separators=(',', ':'))
    open('data_%d.json' % f0, 'w').write(js)
    subprocess.run([sys.executable, 'datacomp.py', 'data_%d.json' % f0, 'comps/data_%d.comp' % f0], check=True)
    print(name, f0, len(js), {k: len(v) for k, v in p['keys'].items()})
