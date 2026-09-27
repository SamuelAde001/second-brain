import re,os
NEO=os.path.expandvars(r"%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Macros\Neo folder\Neo Bevel.setting")
s=open(NEO,encoding="utf-8").read()
a=s.index("Tools = ordered() {")+len("Tools = ordered() {"); body=s[a:s.rindex("\n\t}")]
k=body.find("\n\t\t\tTools = ordered() {")
inner=set(re.findall(r"\n\t*(\w+) = (?!Instance|Input\b|\w+Info\b)[\w.]+ \{", body[k:]))-{"NeoBevel"}
def ren(text,sfx,top):
    new=lambda n: top if n=="NeoBevel" else (n+sfx if n in inner else n)
    text=re.sub(r"(\n\t*)(\w+)( = (?!Instance)[\w.]+ \{)",lambda m:m.group(1)+new(m.group(2))+m.group(3),text)
    text=re.sub(r'SourceOp = "(\w+)"',lambda m:'SourceOp = "%s"'%new(m.group(1)),text)
    return re.sub(r'Expression = "[^"]*"',lambda m:re.sub(r"\b(\w+)\.",lambda q:new(q.group(1))+".",m.group(0)),text)
CX=[0.203125,0.401042,0.598958,0.796875]
W,H,TOP=349.0,453.0,4.0
out=[]
for n in range(1,5):
    b=ren(body,"_NB%d"%n,"NeoBevel_Card%d"%n)
    b=re.sub(r'\n\t*Input = Input \{\s*SourceOp = "\w+",\s*Source = "Output",\s*\},?(?=[^{}]*PipeRouter)','',b)  # no-op safety
    out.append(b.rstrip().rstrip(","))
    y=1-(TOP+H-7)/1080.0
    out.append('''
		Rectangle_Strip%d = RectangleMask {
			Inputs = {
				Filter = Input { Value = FuID { "Fast Gaussian" }, },
				PaintMode = Input { Value = FuID { "Multiply" }, },
				MaskWidth = Input { Value = 1920, },
				MaskHeight = Input { Value = 1080, },
				PixelAspect = Input { Value = { 1, 1 }, },
				UseFrameFormatSettings = Input { Value = 1, },
				ClippingMode = Input { Value = FuID { "None" }, },
				Center = Input { Value = { %f, %f }, },
				Width = Input { Value = %f, },
				Height = Input { Value = %f, },
			},
			ViewInfo = OperatorInfo { Pos = { 0, %d } },
		}'''%(n,CX[n-1],y,W/1920.0,14/1080.0,n*200))
    out.append('''
		Background_Strip%d = Background {
			Inputs = {
				GlobalOut = Input { Value = 48, },
				Width = Input { Value = 1920, },
				Height = Input { Value = 1080, },
				UseFrameFormatSettings = Input { Value = 1, },
				TopLeftRed = Input { Value = 1, },
				TopLeftGreen = Input { Value = 0.3529, },
				TopLeftBlue = Input { Value = 0.1216, },
				EffectMask = Input { SourceOp = "Rectangle_Strip%d", Source = "Mask", },
			},
			ViewInfo = OperatorInfo { Pos = { 0, %d } },
		}'''%(n,n,n*200+33))
    out.append('''
		Merge_Strip%d = Merge {
			Inputs = {
				Foreground = Input { SourceOp = "Background_Strip%d", Source = "Output", },
				PerformDepthMerge = Input { Value = 0, },
			},
			ViewInfo = OperatorInfo { Pos = { 0, %d } },
		}'''%(n,n,n*200+66))
open("cardA_paste.setting","w",encoding="utf-8").write("{\n\tTools = ordered() {%s\n\t},\n}\n"%",".join(out))
t=open("cardA_paste.setting",encoding="utf-8").read()
print(len(t),re.findall(r"\n\t\t(\w+) = [\w.]+ \{",t))
print(re.findall(r'SourceOp = "(\w+)"',t))
