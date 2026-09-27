# One focus track per V5 adjustment clip (the screen-recording stretches). Frame coords u,v (v down).
import spec
from spec import st
from gen import Track

S, B = {}, {}
S["clay"] = spec.S["clay"]
B["clay"] = spec.B["clay"]
S["railway"] = spec.S["railway"]

# ---- Frontal website: form -> playbook -> booking (4064-4475)
FORM = (0.59, 0.2, 0.845, 0.57)
S["frontal"] = (4064, 4475, Track([
    st(4078, 10, 1.7, (0.715, 0.38), FORM),                           # "if you go on the blog"
    st(4107, 6, 1.7, (0.715, 0.38), (0.595, 0.285, 0.84, 0.355)),     # "type your email"
    st(4132, 6, 1.7, (0.715, 0.38), (0.595, 0.39, 0.84, 0.46)),       # "and give your websites"
    st(4162, 6, 1.7, (0.715, 0.38), (0.595, 0.505, 0.72, 0.57)),      # "we're going to generate a playbook"
    st(4205, 8),
    st(4400, 8, 1.3, (0.53, 0.71), (0.235, 0.545, 0.825, 0.875)),     # "in the lead magnet"
    st(4418, 6, 1.5, (0.66, 0.71), (0.6, 0.69, 0.765, 0.775)),        # "book a 30-minute meeting"
    st(4442, 6, 1.4, (0.775, 0.5), (0.595, 0.24, 0.955, 0.765)),      # booking page
]))

# ---- GitHub repo -> Claude Code demo -> GitHub repo (6383-9216)
TITLE = (0.145, 0.13, 0.31, 0.178)
ABOUT = (0.735, 0.21, 0.915, 0.35)
TAGS = (0.735, 0.37, 0.915, 0.445)
FILES = (0.155, 0.335, 0.715, 0.99)
CLIENTS = (0.155, 0.43, 0.715, 0.457)
gh1 = [
    st(6415, 8, 1.45, (0.3, 0.3), TITLE),                           # "the Frontal go-to-market OS"
    st(6461, 8, 1.5, (0.82, 0.3), ABOUT),                           # built over months / every GTM engineer
    st(6671, 6, 1.5, (0.82, 0.3), TAGS),                            # "inside of Claude or inside of Codex"
    st(6758, 8),
    st(6887, 8, 1.6, (0.47, 0.86), (0.405, 0.845, 0.54, 0.875)),    # "look for the folder"
    st(6983, 8, 1.5, (0.6, 0.9), (0.395, 0.925, 0.8, 0.985)),       # the demo prompt, dictated
    st(7176, 6),
]
gh2 = [
    st(9011, 8, 1.2, (0.43, 0.62), FILES),                          # "compacted all of that knowledge"
    st(9176, 6, 1.4, (0.43, 0.46), CLIENTS),                        # "working for new clients"
]
S["gtm"] = (6383, 9216, Track(gh1 + spec.S["claude_out"][2].s + gh2))

# ---- Wispr Flow app (9973-11879)
CARDS = (0.325, 0.285, 0.845, 0.69)
S["wispr"] = (9973, 11879, Track([
    st(9978, 8, 1.35, (0.585, 0.49), CARDS),                        # "you can choose the style"
    st(10050, 6, 1.6, (0.5, 0.2), (0.325, 0.055, 0.68, 0.1)),       # personal vs business messages
    st(10201, 6, 1.35, (0.585, 0.49), CARDS),
    st(10240, 4, 1.35, (0.585, 0.49), (0.325, 0.3, 0.49, 0.685)),   # formal
    st(10258, 4, 1.35, (0.585, 0.49), (0.495, 0.3, 0.655, 0.685)),  # casual
    st(10270, 4, 1.35, (0.585, 0.49), (0.66, 0.3, 0.835, 0.685)),   # very casual
    st(10292, 6, 1.5, (0.07, 0.286), (0.005, 0.268, 0.125, 0.305)), # Transforms
    st(10320, 8, 1.35, (0.6, 0.15), (0.325, 0.03, 0.87, 0.26)),     # mumbling, "uh uh"
    st(10500, 8, 1.8, (0.53, 0.92), (0.48, 0.935, 0.585, 0.99)),    # "double press, now it's going to record"
    st(10753, 8, 1.5, (0.41, 0.5), (0.33, 0.415, 0.49, 0.585)),     # the transform feature: Polish
    st(10999, 8),
    st(11045, 8, 1.5, (0.345, 0.24), (0.265, 0.12, 0.425, 0.345)),  # words per minute
    st(11131, 8, 1.35, (0.76, 0.56), (0.595, 0.38, 0.925, 0.745)),  # all the days
    st(11198, 8, 1.35, (0.43, 0.56), (0.265, 0.38, 0.595, 0.745)),  # which app
    st(11273, 8, 1.5, (0.515, 0.24), (0.425, 0.12, 0.59, 0.345)),   # fixes Wispr Flow made
    st(11344, 10),
]))

# ================= A-roll inserts (V8 Tella footage, focus on V9 adjustment clips)
RW_TOP = (0.005, 0.008, 0.28, 0.065)
RW_ALL = (0.355, 0.318, 0.74, 0.728)
RW_WEB = (0.355, 0.318, 0.545, 0.495)
S["ins_railway1"] = (3218, 3304, Track([
    st(3222, 8, 1.5, (0.16, 0.12), RW_TOP),                          # "the second tool is Railway"
    st(3262, 8, 1.45, (0.548, 0.523), RW_ALL),                      # "Railway is a hosting platform"
]))
S["ins_railway2"] = (3422, 3542, Track([
    st(3424, 8, 1.45, (0.548, 0.523), RW_ALL),                      # "a place to deploy it"
    st(3479, 8, 1.7, (0.45, 0.41), RW_WEB),                         # "let other people use it and see it"
]))
S["ins_claude"] = (5846, 5972, Track([
    st(5848, 8, 1.5, (0.53, 0.34), (0.39, 0.3, 0.67, 0.385)),       # "The third tool is Claude"
    st(5880, 8, 1.5, (0.53, 0.47), (0.325, 0.4, 0.74, 0.535)),      # research / review / draft -> the prompt box
    st(5948, 6, 1.5, (0.53, 0.5), (0.36, 0.56, 0.415, 0.61)),       # "write a first draft" -> Write
]))
def row(v):
    return (0.15, v - 0.022, 0.72, v + 0.022)
S["ins_repo"] = (6118, 6383, Track([
    st(6120, 8, 1.45, (0.3, 0.3), (0.14, 0.13, 0.31, 0.18)),        # "a GTM operating system"
    st(6189, 8, 1.2, (0.43, 0.6), (0.15, 0.33, 0.72, 0.98)),        # "brings together all of the working context"
    st(6230, 6, 1.3, (0.43, 0.6), row(0.446)),                      # clients
    st(6261, 6, 1.3, (0.43, 0.6), row(0.582)),                      # tools -> skills
    st(6284, 6, 1.3, (0.43, 0.6), row(0.538)),                      # workflows -> scripts
    st(6305, 6, 1.3, (0.43, 0.6), row(0.718)),                      # reusable instructions -> CLAUDE.md
    st(6338, 6, 1.3, (0.43, 0.6), row(0.671)),                      # the tools to do the work -> .mcp.json
    st(6368, 14),
]))
S["ins_dictate"] = (9313, 9461, Track([
    st(9315, 8, 1.6, (0.53, 0.85), (0.49, 0.932, 0.577, 0.99)),     # "dictate" -> the Wispr pill
    st(9356, 8, 1.5, (0.53, 0.47), (0.325, 0.4, 0.74, 0.56)),       # "where you would normally type"
]))
