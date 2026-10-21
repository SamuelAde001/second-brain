"""List elements that reach outside the 1080 px page in each built row html (helps keep Canva's bounding box = page)."""
import glob, os, re, subprocess, sys, json
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROF = os.path.join(os.environ.get("TEMP", "."), "c2e-board-chrome")
JS = """<script>window.addEventListener('load',()=>document.fonts.ready.then(()=>{const o=[];document.querySelectorAll('body *').forEach(e=>{const r=e.getBoundingClientRect();if(r.width&&(r.bottom>1082||r.top<-2)){o.push((e.closest('section')||{dataset:{}}).dataset.id+' '+e.tagName+'.'+(e.className.baseVal!==undefined?e.className.baseVal:e.className)+' '+Math.round(r.top)+'..'+Math.round(r.bottom))}});const p=document.createElement('script');p.type='application/json';p.id='ovf';p.textContent=JSON.stringify(o.slice(0,40));document.head.appendChild(p)}))</script>"""
for hp in sorted(glob.glob("row*.html")):
    if len(sys.argv) > 1 and sys.argv[1] not in hp: continue
    s = open(hp, encoding="utf-8").read().replace("</head>", JS + "</head>")
    tmp = hp.replace(".html", ".ovf.html"); open(tmp, "w", encoding="utf-8").write(s)
    dom = subprocess.run([CHROME, "--headless=new", f"--user-data-dir={PROF}", "--virtual-time-budget=15000", "--dump-dom", "file:///" + os.path.abspath(tmp).replace("\\", "/")], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    os.remove(tmp)
    m = re.search(r'id="ovf">(.*?)</script>', dom, re.S)
    print(hp, json.loads(m.group(1)) if m else "?")
