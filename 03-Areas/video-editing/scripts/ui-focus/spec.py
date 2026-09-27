# Focus spec per screen stretch. States: (frame, ease_frames, zoom, (pu, pv) focus point, rect (u0,v0,u1,v1) or None)
# Rect None = no dimming. u,v are fractions of the viewer frame (v down), as the Tella clip is framed now.
from gen import Track, Scroll

S = {}
B = {}
OFF = (1.0, (0.5, 0.5), None)

def st(f, d, z=None, p=None, r=None):
    if z is None:
        return (f, d) + OFF
    return (f, d, z, p, r)

# ---- Clay: Wedge Agent Feeder (2143-3219)
S["clay"] = (2143, 3219, Track([
    st(2177, 10, 1.9, (0.07, 0.03), (0.0, 0.0, 0.15, 0.058)),        # "a workflow called wedge agent feeder"
    st(2212, 10),
    st(2405, 8, 1.35, (0.505, 0.44), (0.40, 0.385, 0.61, 0.495)),     # LinkedIn ads
    st(2452, 8),
    st(2493, 8, 1.35, (0.485, 0.45), (0.38, 0.40, 0.59, 0.50)),       # SDR headcount
    st(2538, 6),
    st(2549, 8, 1.35, (0.46, 0.38), (0.355, 0.33, 0.57, 0.435)),      # email infrastructure
    st(2684, 8),
    st(2697, 8, 1.35, (0.33, 0.45), (0.225, 0.395, 0.43, 0.50)),      # ICP and TAM estimates
    st(2758, 8),
    st(2965, 8, 1.5, (0.48, 0.35), (0.405, 0.15, 0.55, 0.205)),       # not running LinkedIn ads
    st(2993, 6, 1.5, (0.48, 0.35), (0.405, 0.27, 0.55, 0.335)),       # not running meta ads
    st(3016, 6, 1.5, (0.48, 0.35), (0.405, 0.395, 0.55, 0.465)),      # high SDR headcount
    st(3040, 5, 1.5, (0.48, 0.225), (0.405, 0.27, 0.55, 0.335)),      # (canvas scrolls up)
    st(3063, 6, 1.5, (0.48, 0.225), (0.405, 0.395, 0.55, 0.465)),     # bad email infrastructure
    st(3108, 10),
]))
B["clay"] = [
    (2549, 2601, (0.78, 0.575, 1.0, 0.625)),   # email-infra-detector ?key=
    (2601, 2623, (0.78, 0.0, 1.0, 0.64)),      # panel scrolling with the key in it
    (2754, 3219, (0.78, 0.61, 1.0, 0.665)),    # signal-engine-intake ?token=
]

# ---- Railway project (4544-4697)
S["railway"] = (4544, 4697, Track([
    st(4546, 10, 1.55, (0.548, 0.525), (0.35, 0.315, 0.745, 0.735)),  # "here is the project"
    st(4620, 8, 1.7, (0.45, 0.62), (0.355, 0.51, 0.545, 0.725)),      # "a small database"
    st(4654, 8, 1.6, (0.645, 0.525), (0.55, 0.32, 0.74, 0.725)),      # "agents running in the background"
]))

# ---- Claude Code output of the GTM OS demo (7176-8880), content scrolls: track it
sc = Scroll("trk_claude.json")
def step(k):
    o = 0.1245 * (k - 1)
    return (0.325, 0.372 + o, 0.735, 0.487 + o)
LIST = (0.325, 0.36, 0.735, 1.1)
TABLE = (0.335, 0.08, 0.735, 0.375)
COMP, WHO, WHY = (0.335, 0.08, 0.44, 0.375), (0.44, 0.08, 0.555, 0.375), (0.555, 0.08, 0.735, 0.375)
EMAIL = (0.325, 0.405, 0.735, 0.525)
SUBJ = (0.325, 0.425, 0.62, 0.448)
BODY = (0.325, 0.448, 0.735, 0.525)
LAST = (0.325, 0.498, 0.735, 0.525)
S["claude_out"] = (7176, 8923, Track([
    st(7190, 10, 1.25, sc.point(7190, (0.325, 0.36, 0.735, 0.95)), sc.rect(7190, LIST)),   # "all the different steps"
    st(7347, 8, 1.7, sc.point(7190, step(1)), sc.rect(7190, step(1))),   # client file and positioning
    st(7585, 8, 1.7, sc.point(7190, step(2)), sc.rect(7190, step(2))),   # top 10 accounts / signal engine
    st(7803, 6, 1.7, sc.point(7190, step(3)), sc.rect(7190, step(3))),   # picking the right person
    st(7865, 6, 1.7, sc.point(7190, step(4)), sc.rect(7190, step(4))),   # the angle for the copy
    st(7898, 6, 1.7, sc.point(7190, step(5)), sc.rect(7190, step(5))),   # the verified email
    st(7943, 6, 1.7, sc.point(7190, step(6)), sc.rect(7190, step(6))),   # write the entire sequence
    st(8001, 8, 1.6, sc.point(8050, TABLE), sc.rect(8050, COMP)),        # the company
    st(8049, 6, 1.6, sc.point(8050, TABLE), sc.rect(8050, WHO)),         # the position we should target
    st(8095, 6, 1.6, sc.point(8050, TABLE), sc.rect(8050, WHY)),         # why now / event, trigger, signal
    st(8205, 8, 1.7, sc.point(8050, EMAIL), sc.rect(8050, EMAIL)),       # the email we would send
    st(8257, 6, 1.7, sc.point(8050, EMAIL), sc.rect(8050, SUBJ)),        # a new BDR starting
    st(8302, 6, 1.7, sc.point(8050, EMAIL), sc.rect(8050, BODY)),        # reach out to the CRO / reads it
    st(8604, 6, 1.7, sc.point(8050, EMAIL), sc.rect(8050, LAST)),        # send it over, start on day one
    st(8656, 8, 1.7, sc.point(8050, EMAIL), sc.rect(8050, EMAIL)),       # hiring a BDR, free value
    st(8820, 4),
]))
