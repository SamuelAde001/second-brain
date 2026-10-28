r"""fusion_setting.py - read a Fusion .setting / .comp file into Python (Editor, 2026-10-28). No Resolve needed.

    import fusion_setting as fs
    tools = fs.load(path)              # {name: T}   top-level tools (macros keep their inner Tools under t["Tools"])
    t.type                             # "TextPlus", "MacroOperator", "Fuse.NeoMotionText", "BezierSpline", ...
    fs.inp(t, "Size")                  # static value of an input (number / string / list), None when absent or linked
    fs.src(t, "Size")                  # SourceOp name when the input is linked (a spline, a modifier, another tool)
    fs.keys(tools, t, "Blend")         # [(frame, value), ...] when the input is driven by a BezierSpline, else []

A table is a T: a dict of its named keys plus .arr (positional items) and .type (the constructor name, "" for a bare
{ }). Strings are unescaped. Comments (-- ...) are skipped.
"""
import re

_TOK = re.compile(r'\s*(?:--\[\[.*?\]\]|--[^\n]*|("(?:[^"\\]|\\.)*")|([-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)'
                  r'|([A-Za-z_][\w.]*)|(\[|\]|\{|\}|=|,|;|\(|\)))', re.S)
_ESC = {"n": "\n", "t": "\t", "r": "\r", '"': '"', "\\": "\\", "'": "'", "0": "\0"}


class T(dict):
    __slots__ = ("type", "arr")

    def __init__(self, typ=""):
        super().__init__()
        self.type, self.arr = typ, []

    def __repr__(self):
        return "T(%s, %d keys, %d items)" % (self.type, len(self), len(self.arr))


def _unq(s):
    return re.sub(r'\\(.)', lambda m: _ESC.get(m.group(1), m.group(1)), s[1:-1])


def _tokens(text):
    out, i, n = [], 0, len(text)
    while i < n:
        m = _TOK.match(text, i)
        if not m or m.end() == i:
            if text[i:].strip() == "":
                break
            raise ValueError("bad token at %d: %r" % (i, text[i:i + 40]))
        i = m.end()
        s, num, name, p = m.groups()
        if s is not None:
            out.append(("s", _unq(s)))
        elif num is not None:
            out.append(("n", float(num)))
        elif name is not None:
            out.append(("i", name))
        elif p is not None:
            out.append(("p", p))
    return out


class _P:
    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self, k=0):
        j = self.i + k
        return self.t[j] if j < len(self.t) else ("e", None)

    def take(self):
        x = self.peek(); self.i += 1; return x

    def value(self):
        kind, v = self.take()
        if kind in ("s", "n"):
            return v
        if kind == "p" and v == "{":
            return self.table("")
        if kind == "i":
            if v == "true":
                return True
            if v == "false":
                return False
            if v == "nil":
                return None
            if self.peek() == ("p", "("):                       # ordered() { ... }
                self.take()
                while self.peek() != ("p", ")"):
                    self.take()
                self.take()
            if self.peek() == ("p", "{"):
                self.take()
                return self.table("" if v == "ordered" else v)
            return v                                           # a bare name (rare)
        raise ValueError("unexpected %r at token %d" % (v, self.i))

    def table(self, typ):
        t = T(typ)
        while True:
            k = self.peek()
            if k == ("p", "}"):
                self.take(); return t
            if k[0] == "p" and k[1] in (",", ";"):
                self.take(); continue
            if k == ("p", "["):
                self.take(); key = self.value(); self.take()       # ]
                self.take()                                        # =
                t[int(key) if isinstance(key, float) and key == int(key) else key] = self.value()
                continue
            if k[0] == "i" and self.peek(1) == ("p", "="):
                self.take(); self.take()
                t[k[1]] = self.value()
                continue
            t.arr.append(self.value())


def parse(text):
    p = _P(_tokens(text))
    if p.peek() == ("p", "{"):
        p.take()
        return p.table("")
    return p.value()


def load(path):
    """Top-level tools of a .setting ({Tools = ordered() {...}}) or a .comp (Composition {Tools = ...})."""
    root = parse(open(path, encoding="utf-8", errors="replace").read())
    tools = root.get("Tools") if isinstance(root, T) else None
    return tools if isinstance(tools, T) else T()


def inputs(t):
    x = t.get("Inputs") if isinstance(t, T) else None
    return x if isinstance(x, T) else T()


def _in(t, name):
    x = inputs(t).get(name)
    return x if isinstance(x, T) else None


def inp(t, name, default=None):
    x = _in(t, name)
    if x is None or "SourceOp" in x:
        return default
    v = x.get("Value", default)
    if isinstance(v, T):
        return v.get("Value", v.arr[0] if v.arr else default) if v.type == "FuID" else list(v.arr)
    return v


def src(t, name):
    x = _in(t, name)
    return x.get("SourceOp") if x is not None else None


def expr(t, name):
    x = _in(t, name)
    return x.get("Expression") if x is not None else None


def spline_keys(sp):
    """BezierSpline -> sorted [(frame, value)]."""
    kf = sp.get("KeyFrames") if isinstance(sp, T) else None
    if not isinstance(kf, T):
        return []
    out = []
    for f, v in kf.items():
        if isinstance(v, T) and v.arr:
            out.append((float(f), float(v.arr[0])))
    return sorted(out)


def keys(tools, t, name):
    s = src(t, name)
    sp = tools.get(s) if s else None
    if isinstance(sp, T) and sp.type == "BezierSpline":
        return spline_keys(sp)
    return []


def pos(t):
    vi = t.get("ViewInfo") if isinstance(t, T) else None
    p = vi.get("Pos") if isinstance(vi, T) else None
    return tuple(p.arr) if isinstance(p, T) else None
