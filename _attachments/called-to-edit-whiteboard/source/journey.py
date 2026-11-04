"""The Journey of a Video Editor: the eight steps from Samuel's whiteboard (photo, 2026-11-04), as one pathway map
for a Community teaching on Discord. Step names are his, word for word; the lines under each are his teaching
(05-Knowledge/teachings/teachings-02 … teachings-11). Build: C2E_THEME=white python native.py journey"""
from maplib import *

NAME = "journey-video-editor"
W = 5720


def lead(text, size=44):
    return f'<span style="font:600 {size}px \'Plus Jakarta Sans\';color:#fff">{text}</span>'


STEPS = [
    ("Learn the Software", "laptop", "Master the tool first", [
        ("Master the one you'll actually use", "CapCut, Resolve, Premiere. Sit through the long tutorials. <b>This is the part you can't skip.</b>", "monitor-play", "gold"),
        ("Never use cracked software", "I got hacked on my computer, and it affected my work.", "shield-alert", ""),
    ]),
    ("Learn the Skill of Editing", "scissors", "The art, not the buttons", [
        ("The skill", "Cutting, pacing, sound. What makes the kind of video you chose work.", "scissors", "gold"),
        ("Recreate, don't only watch", "Pick raw videos close to your niche, not the biggest creators.", "copy", ""),
        ("Every video has a goal", "Edit for the client's reason, not to look fancy.", "target", ""),
    ]),
    ("Become Visible", "eye", "Your work is your advert", [
        ("Editing is a visible skill", "Where can people find you? Where can they see your work?", "eye", "gold"),
        ("Surround yourself with editing", "Follow editors in your niche, so your feed teaches you.", "users", ""),
        ("Post your work, 3 times a day", "Your timeline, screenshots, you working. <b>Getting seen is what makes people find you.</b>", "camera", ""),
    ]),
    ("Position Yourself to a Certain Client", "crosshair", "Pick who you serve", [
        ("Your offer in one sentence", "<b>Who</b> you help · <b>what result</b> · <b>how</b> · <b>how fast</b>.", "crosshair", "gold"),
        ("Business people pay more", "In any niche, people selling something understand marketing.", "briefcase", ""),
        ("Have something to show", "A portfolio: your best videos, 8 at most.", "folder-open", ""),
    ]),
    ("Start to Outreach", "send", "Go to them", [
        ("Name the video", "Not \"I saw your videos\". Say which one, and something from inside it.", "message-square", "gold"),
        ("Value first", "Edit a piece of their video for free. <b>Never more than 30 seconds.</b>", "gift", ""),
        ("Inbound and outbound", "You can't rely on only one. Follow up.", "repeat", ""),
    ]),
    ("Close Your First Clients", "handshake", "Real work, real stakes", [
        ("Work with someone first", "Whoever it is. Real projects are the fastest way to grow.", "handshake", "gold"),
        ("Ask questions before a price", "What style? What do you want this video to achieve?", "circle-help", ""),
        ("Charge per video", "Not monthly, not per minute. Price it on a call.", "receipt", ""),
    ]),
    ("Build a Bigger Network", "users", "People bring people", [
        ("Editors at your level", "On LinkedIn and Twitter. Engage with them.", "users", "gold"),
        ("Turn every job into proof", "Screenshot the results. Ask for a testimonial. Make it a case study.", "trophy", ""),
        ("Join editor communities", "They challenge you. You see what others are doing.", "users-round", ""),
    ]),
    ("Offer More Than Video Editing", "layers", "Grow what one client pays", [
        ("Upsell once you've landed them", "Ideation, scripting, thumbnails on top of the edit. <b>USD 1,000 instead of USD 500.</b>", "layers", "gold"),
        ("Retainer clients", "Clients who post consistently. Money that comes back every month.", "calendar", ""),
    ]),
]


def build():
    reset()
    branches = []
    for k, (title_, ic, sub, leaves) in enumerate(STEPS, 1):
        items = [L(f"s{k}l{j}", h, b, i, c) for j, (h, b, i, c) in enumerate(leaves)]
        branches.append(B(k, str(k), title_, ic, items, sub, f"s{k}l0"))
    side = '<img src="kit/called-to-edit-logo-dark.svg" style="width:480px">'
    body = assemble("", "The Journey of a", "Video Editor", "Eight steps, in order.<br>Each one leads to the next.",
                    "Don't learn without implementation.", branches,
                    [(str(k), s[0]) for k, s in enumerate(STEPS, 1)], None, side)
    return body, W, None
