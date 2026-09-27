# quad.py out.jpg f1 f2 ... -> 2-col tiles of 960x540 frames with 5% grid, labelled
import data, subprocess, sys, os, glob
from concurrent.futures import ThreadPoolExecutor
x,y,w,h = data.VIEW
out=sys.argv[1]; fr=list(map(int,sys.argv[2:]))
os.makedirs('q',exist_ok=True)
for p in glob.glob('q/*.png'): os.remove(p)
def g(i_f):
    i,f=i_f; t=data.tella_at(f)
    vf=(f"crop={w}:{h}:{x}:{y},scale=960:540,drawgrid=w=48:h=27:t=1:c=red@0.3,drawgrid=w=96:h=54:t=1:c=blue@0.35,"
        f"drawtext=fontfile=arial.ttf:text='{f}':x=4:y=4:fontsize=22:fontcolor=yellow:box=1:boxcolor=black")
    subprocess.run([data.FF,'-hide_banner','-loglevel','error','-ss',f'{t:.3f}','-i',data.TELLA,'-frames:v','1','-vf',vf,'-y',f'q/{i:03d}.png'])
with ThreadPoolExecutor(6) as ex: list(ex.map(g, enumerate(fr)))
rows=(len(fr)+1)//2
subprocess.run([data.FF,'-hide_banner','-loglevel','error','-i','q/%03d.png','-frames:v','1','-vf',f'tile=2x{rows}:color=white','-y',out])
