import glob, os
HERE = os.path.dirname(os.path.abspath(__file__))
HEAD = """<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="kit.css">
<script>window.onerror=function(m,s,l){window.__err=m+' @'+(s||'').split('/').pop()+':'+l}</script></head>
<body><div id="stage"></div><script src="kit.js"></script><script src="lib.js"></script><script src="tracker.js"></script><script src="parts.js"></script>
<script src="src/%s.js"></script></body></html>"""
for f in glob.glob(os.path.join(HERE, "src", "*.js")):
    n = os.path.splitext(os.path.basename(f))[0]
    open(os.path.join(HERE, n + ".html"), "w", encoding="utf-8").write(HEAD % n)
print("built", len(glob.glob(os.path.join(HERE, "src", "*.js"))))
