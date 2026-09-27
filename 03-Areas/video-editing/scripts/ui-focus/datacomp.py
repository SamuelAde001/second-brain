# datacomp.py file.json out.comp -> a .comp with one Note (DataNote) whose Comments hold the file's text
import sys
txt = open(sys.argv[1], encoding='utf-8').read()
BS = chr(92)
esc = txt.replace(BS, BS + BS).replace('"', BS + '"').replace('\n', ' ')
s = ('Composition {\n\tCurrentTime = 0,\n\tRenderRange = { 0, 10 },\n\tGlobalRange = { 0, 10 },\n\tTools = {\n'
     '\t\tDataNote = Note {\n\t\t\tInputs = {\n\t\t\t\tComments = Input { Value = "%s", },\n\t\t\t},\n'
     '\t\t\tViewInfo = StickyNoteInfo { Pos = { 0, 0 }, },\n\t\t},\n\t},\n}\n') % esc
open(sys.argv[2], 'w', encoding='utf-8').write(s)
print(len(s))
