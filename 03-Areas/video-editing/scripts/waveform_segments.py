"""Waveform gap pass for a talking-head mic track (Routerise cut SOP, step 2).

Input: peaks5.json, the mic's 5 ms peak levels in dB, made with
  ffmpeg -i mic.wav -af "asetnsamples=n=240:p=0,astats=metadata=1:reset=1:measure_perchannel=Peak_level:measure_overall=none,ametadata=print:key=lavfi.astats.1.Peak_level:file=peaks5.txt" -f null -
  then parsed into a JSON list.
Output: segs.json = speech clips [start_s, end_s, peak_db] in mic time + phrase groups.
Settings: client threshold -38 dB, 3-timeline-frame minimum gap, tight starts (5 ms before
the first 30 ms of sustained sound, which skips mouth smacks), 50 ms tails, breath and
click runs dropped. First used on Route Rise #3 (2026-09-24).
Place the result on a timeline only with a mic clip that reads at the timeline frame
rate (see the SOP, "Frame grid"), or audio cuts land off the video cuts.
"""
import json, math
W=0.005
v=json.load(open('peaks5.json')); n=len(v)
TH=-38.0            # client threshold (SOP)
MIN_GAP=3*1001/24000  # 3 timeline frames
PRE=0.005; POST=0.05
SUS=6               # 30 ms sustained
on=[x>TH for x in v]
# sound runs bridged across gaps < MIN_GAP
g=int(MIN_GAP/W)
runs=[];i=0
while i<n:
    if not on[i]: i+=1; continue
    j=i
    while True:
        while j<n and on[j]: j+=1
        k=j
        while k<n and not on[k]: k+=1
        if k<n and k-j<g: j=k; continue
        break
    runs.append([i,j]); i=j
def sustained_start(a,b):
    for k in range(a,b-SUS+1):
        if sum(on[k:k+SUS])>=SUS-1 and on[k]: return k
    return None
def sustained_end(a,b):
    for k in range(b,a+SUS-1,-1):
        if sum(on[k-SUS:k])>=SUS-1 and on[k-1]: return k
    return None
segs=[];drop=[]
for a,b in runs:
    mx=max(v[a:b]); dur=(b-a)*W
    s=sustained_start(a,b); e=sustained_end(a,b)
    if s is None or e is None or e<=s: drop.append((a*W,dur,mx,'nosus')); continue
    if mx< -30 and dur<0.4: drop.append((a*W,dur,mx,'breath')); continue
    if (e-s)*W<0.08: drop.append((a*W,dur,mx,'click')); continue
    segs.append([s*W-PRE, e*W+POST, round(mx,1)])
# bridge segments closer than MIN_GAP after trimming
m=[]
for s,e,mx in segs:
    if m and s-m[-1][1]<MIN_GAP: m[-1][1]=e; m[-1][2]=max(m[-1][2],mx)
    else: m.append([s,e,mx])
tot=sum(e-s for s,e,_ in m)
print('runs',len(runs),'segs',len(m),'kept %.1f s of %.1f'%(tot,n*W),'dropped',len(drop))
import collections
print(collections.Counter(d[3] for d in drop))
print('dropped sample',[tuple(round(x,2) if isinstance(x,float) else x for x in d) for d in drop[:25]])
# phrase groups: gap > 0.35 s
grp=[];cur=[m[0]]
for s in m[1:]:
    if s[0]-cur[-1][1]>0.35: grp.append(cur); cur=[s]
    else: cur.append(s)
grp.append(cur)
print('phrase groups',len(grp), 'longest %.1f s'%max(g_[-1][1]-g_[0][0] for g_ in grp))
json.dump({"segs":m,"groups":[[m.index(x) for x in g_] for g_ in grp]},open('segs.json','w'))
