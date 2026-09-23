r"""Read a DaVinci Resolve crash dump (.dmp) without a debugger.

Resolve writes dumps to %APPDATA%\Blackmagic Design\DaVinci Resolve\Support\logs\ (older ones in LogArchive\).
Prints the exception code, the module+offset it happened in, the address it tried to read
(params[1]; 0x0 = null pointer), and a heuristic stack: every value on the faulting
thread's stack that points into a loaded module, top first. Usage:
    python resolve_crash_dump.py <file.dmp> [...]
Part of [[03-Areas/video-editing/troubleshooting|Troubleshooting]] section 7.
"""
import struct, sys, os
def parse(path):
    d=open(path,"rb").read()
    sig,ver,n,dirrva=struct.unpack_from("<4sIII",d,0)
    streams={}
    for i in range(n):
        t,sz,rva=struct.unpack_from("<III",d,dirrva+12*i); streams.setdefault(t,(sz,rva))
    def mstr(rva):
        ln=struct.unpack_from("<I",d,rva)[0]; return d[rva+4:rva+4+ln].decode("utf-16-le","replace")
    mods=[]
    if 4 in streams:
        _,rva=streams[4]; cnt=struct.unpack_from("<I",d,rva)[0]
        for i in range(cnt):
            o=rva+4+108*i
            base,size,_,_,namerva=struct.unpack_from("<QIIII",d,o)
            mods.append((base,size,os.path.basename(mstr(namerva))))
    def where(a):
        for b,s,nm in mods:
            if b<=a<b+s: return f"{nm}+0x{a-b:x}"
        return None
    print("==", os.path.basename(path))
    if 6 in streams:
        _,rva=streams[6]
        tid,_,code,flags,rec,addr,np_=struct.unpack_from("<IIIIQQI",d,rva)
        params=struct.unpack_from("<15Q",d,rva+8+32)[:np_]
        ctxsz,ctxrva=struct.unpack_from("<II",d,rva+8+32+120)
        print(f"thread {tid:#x} code {code:#010x} at {addr:#x} = {where(addr)} params {[hex(p) for p in params]}")
        rsp=struct.unpack_from("<Q",d,ctxrva+0x98)[0]; rip=struct.unpack_from("<Q",d,ctxrva+0xF8)[0]
        print(f"ctx rip {rip:#x} = {where(rip)}")
        # faulting thread stack
        if 3 in streams:
            _,trva=streams[3]; tc=struct.unpack_from("<I",d,trva)[0]
            for i in range(tc):
                o=trva+4+48*i
                t_id=struct.unpack_from("<I",d,o)[0]
                if t_id!=tid: continue
                start,msz,mrva=struct.unpack_from("<QII",d,o+24)
                off=max(0,rsp-start); hits=[]; seen=set()
                for p in range(mrva+off, mrva+msz-7, 8):
                    v=struct.unpack_from("<Q",d,p)[0]; w=where(v)
                    if w and w not in seen:
                        seen.add(w); hits.append(w)
                    if len(hits)>=45: break
                print("stack scan (candidate return addresses, top first):")
                for h in hits: print("   ", h)
    else:
        print("no exception stream; streams:", sorted(streams))
    return mods
for p in sys.argv[1:]: parse(p)
