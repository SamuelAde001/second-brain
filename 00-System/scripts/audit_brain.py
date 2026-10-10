"""Brain health check. Reads every note, prints only problems. No writes.

Usage: python 00-System/scripts/audit_brain.py [section]
Sections: broken, fm, orphans, big, status, encoding, all (default: all but orphans).
"""
import os, re, sys, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SKIP_DIRS = {'.git', '_imports', '.obsidian', '.claude', '.agents', '.gemini', '__pycache__', '_cache', 'node_modules'}
# Not checked for links or frontmatter: templates hold placeholders, the legacy archive is a raw copy.
NO_CHECK = ('00-System/templates/', '08-Archive/accountability-engine/')
NO_FM = {'AGENTS.md', 'CLAUDE.md', 'GEMINI.md'}
# Broken on purpose: the line sits in an append-only log or decision record.
KNOWN_BROKEN = {('07-Agents/content/log.md', '03-Areas/personal-brand/sops/batch-content-day'),
                ('00-System/decisions.md', '00-System/mods/mods')}
# Reached by scripts or tools, not by links.
ORPHAN_OK = ('06-Logs/', '01-Inbox/', '08-Archive/', '00-System/templates/', '00-System/skills/',
             '03-Areas/scripnals/guides/', '03-Areas/video-editing/scripts/', 'CLAUDE.md', 'GEMINI.md')

md, other, badenc = [], set(), []
for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d for d in dns if d not in SKIP_DIRS]
    for f in fns:
        p = os.path.relpath(os.path.join(dp, f), ROOT).replace('\\', '/')
        if f.endswith('.md'): md.append(p)
        else: other.add(p); other.add(f)

text = {}
for p in md:
    raw = open(os.path.join(ROOT, p), 'rb').read()
    try: text[p] = raw.decode('utf-8')
    except UnicodeDecodeError: badenc.append(p); text[p] = raw.decode('utf-8', 'replace')

by_name = collections.defaultdict(list)
for p in md: by_name[os.path.basename(p)[:-3]].append(p)
paths = {p[:-3] for p in md}

code_re = re.compile(r'```.*?```|`[^`\n]*`', re.S)
link_re = re.compile(r'\[\[([^\]|#\\]+)')
fm_re = re.compile(r'^---\r?\n(.*?)\r?\n---', re.S)

inbound, broken, nofm, status, big = collections.Counter(), [], [], collections.defaultdict(list), []
for p, t in text.items():
    lines = t.count('\n')
    if lines > 300: big.append((lines, p))
    if p.startswith(NO_CHECK): continue
    m = fm_re.match(t)
    if not m:
        if p not in NO_FM and '/references/' not in p: nofm.append(p)
    else:
        s = re.search(r'^status:\s*(\S+)', m.group(1), re.M)
        status[s.group(1) if s else 'MISSING'].append(p)
    for tgt in link_re.findall(code_re.sub('', t)):
        tgt = tgt.strip()
        if tgt.endswith('.md'): tgt = tgt[:-3]
        if tgt.startswith('http') or tgt in other: continue
        hit = tgt if tgt in paths else (by_name[tgt][0][:-3] if tgt in by_name else None)
        if hit:
            if hit != p[:-3]: inbound[hit] += 1
        elif (p, tgt) not in KNOWN_BROKEN:
            base = os.path.basename(tgt)
            broken.append(f'{p} -> [[{tgt}]]' + (f'  (moved? {by_name[base][0]})' if base in by_name else ''))

def show(title, rows):
    print(f'\n## {title}: {len(rows)}')
    for r in rows: print('  ', r)

sec = sys.argv[1] if len(sys.argv) > 1 else 'default'
run = lambda s: sec in (s, 'all') or (sec == 'default' and s != 'orphans')
if run('encoding'): show('not UTF-8', badenc)
if run('broken'): show('broken links', broken)
if run('fm'): show('no frontmatter', nofm + status.get('MISSING', []))
if run('big'): show('over 300 lines (split by moving text verbatim)', [f'{n} {p}' for n, p in sorted(big, reverse=True) if not p.startswith(NO_CHECK) and not re.search(r'\d{4}-\d{2}-\d{2}-to-', p)])
if run('status'): show('status: done but not archived', [p for p in status.get('done', []) if p.startswith('04-Projects/')])
if run('orphans'): show('orphans (nothing links here)', sorted(p for p in md if not inbound[p[:-3]] and not p.startswith(ORPHAN_OK)))
print(f'\n{len(md)} notes, {len(other) // 2} other files.')
