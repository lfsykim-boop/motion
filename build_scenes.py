"""Generates index.html and compositions/*.html for 「ㅇ 속으로」.
Timing follows the beats of assets/bgm/fresh-morning.mp3 (139.5 BPM, music enters at 3.75 s).
Edit the scene files directly afterwards if you prefer; re-running this script overwrites them."""
from pathlib import Path

ROOT = Path(__file__).parent
CREAM, INK, ORANGE = "#F3EBDD", "#1E1B18", "#F26B1D"
COFFEE, DARKCOFFEE, GREEN = "#5A3720", "#3B2414", "#2FA35B"

# scene id, film start, duration, local beats (seconds from scene start)
SCENES = [
    ("s0", 0.00, 3.75, []),
    ("w1", 3.75, 3.44, [0, .43, .84, 1.29, 1.72, 2.15, 2.57, 3.01]),
    ("w2", 7.19, 3.42, [0, .42, .85, 1.27, 1.71, 2.14, 2.57, 2.99]),
    ("w3", 10.61, 3.43, [0, .42, .85, 1.29, 1.71, 2.14, 2.57, 3.00]),
    ("w4", 14.04, 3.42, [0, .42, .86, 1.28, 1.71, 2.15, 2.57, 3.00]),
    ("w5", 17.46, 3.41, [0, .45, .86, 1.29, 1.71, 2.14, 2.56, 3.00]),
    ("w6", 20.87, 3.45, [0, .44, .86, 1.31, 1.73, 2.16, 2.60, 3.03]),
    ("end", 24.32, 5.68, [0, .43, .85, 1.29, 1.71, 2.15, 2.57, 3.00]),
]

FONT_CSS = """
    @font-face { font-family: "Pretendard"; src: url('assets/fonts/Pretendard-ExtraBold.woff2') format('woff2'); font-weight: 800; }
    @font-face { font-family: "Pretendard"; src: url('assets/fonts/Pretendard-Medium.woff2') format('woff2'); font-weight: 500; }"""


def scene(sid, ground, body, script, dur):
    return f"""<template>
  <style>{FONT_CSS}
    #root {{ position: absolute; inset: 0; overflow: hidden; background: {ground}; font-family: "Pretendard", sans-serif; }}
    .cam, .stage {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }}
    .art {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; overflow: visible; }}
    .w {{ position: absolute; font-weight: 800; letter-spacing: -0.02em; line-height: 1; white-space: nowrap; }}
    .w span {{ display: inline-block; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080" data-layout-allow-overflow>
{body}
  </div>
  <script>
    const B = window.__B_{sid} = null;
    const tl = gsap.timeline({{ paused: true }});
{script}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""


def emerge(sid):
    return f'    tl.fromTo("#{sid}-stage", {{ scale: 0.12 }}, {{ scale: 1, duration: 0.9, ease: "expo.out", transformOrigin: "960px 540px" }}, 0);\n'


def dive(sid, px, py, scale, dur):
    start = round(dur - 0.62, 3)
    return (f'    tl.fromTo("#{sid}-cam", {{ scale: 1 }}, {{ scale: {scale}, duration: 0.58, ease: "power3.in", '
            f'transformOrigin: "{px}px {py}px" }}, {start});\n')


def rays(cx, cy, r0, r1, n, color, width, sid):
    import math
    out = []
    for i in range(n):
        a = math.radians(i * 360 / n - 90)
        x0, y0 = cx + r0 * math.cos(a), cy + r0 * math.sin(a)
        x1, y1 = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
        out.append(f'        <path id="{sid}-ray{i}" d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}" pathLength="100" '
                   f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" fill="none" '
                   f'stroke-dasharray="100 120" stroke-dashoffset="110"/>')
    return "\n".join(out)


def ticks(cx, cy, r0, r1, sid):
    import math
    out = []
    for i in range(12):
        a = math.radians(i * 30 - 90)
        w = 18 if i % 3 == 0 else 11
        out.append(f'          <line x1="{cx + r0 * math.cos(a):.1f}" y1="{cy + r0 * math.sin(a):.1f}" '
                   f'x2="{cx + r1 * math.cos(a):.1f}" y2="{cy + r1 * math.sin(a):.1f}" stroke="{INK}" '
                   f'stroke-width="{w}" stroke-linecap="round"/>')
    return "\n".join(out)


files = {}

# ---------- s0: 10월의 아침 ----------
L0, T0 = 476, 290
O0 = (round(L0 + 148.4), round(T0 + 242.7))  # centre of the ㅇ counter in 아
files["s0"] = scene("s0", CREAM, f"""    <div id="s0-cam" class="cam">
      <div id="s0-sub" class="w" style="left:{L0 + 10}px; top:178px; font-size:112px; font-weight:500; color:{INK};">10월의</div>
      <div id="s0-word" class="w" style="left:{L0}px; top:{T0}px; font-size:560px; color:{INK};">아침</div>
    </div>""", f"""    tl.fromTo("#s0-cam", {{ scale: 6 }}, {{ scale: 1, duration: 1.6, ease: "expo.out", transformOrigin: "{O0[0]}px {O0[1]}px" }}, 0);
    tl.fromTo("#s0-sub", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.5, ease: "power4.out" }}, 1.17);
    tl.to("#s0-cam", {{ scale: 24, duration: 0.56, ease: "power3.in", transformOrigin: "{O0[0]}px {O0[1]}px" }}, 3.15);
""", 3.75)

# ---------- w1: 해 ----------
SUN = (1300, 500)
files["w1"] = scene("w1", CREAM, f"""    <div id="w1-cam" class="cam"><div id="w1-stage" class="stage">
      <svg class="art" viewBox="0 0 1920 1080">
        <circle cx="{SUN[0]}" cy="{SUN[1]}" r="230" fill="{ORANGE}"/>
{rays(SUN[0], SUN[1], 292, 372, 12, ORANGE, 30, "w1")}
      </svg>
      <div class="w" style="left:190px; top:318px; font-size:150px; color:{INK}; overflow:hidden; padding-bottom:12px;">
        <span id="w1-a0">해</span><span id="w1-a1">가</span><span>&nbsp;</span><span id="w1-a2">먼</span><span id="w1-a3">저</span></div>
      <div class="w" style="left:190px; top:500px; font-size:150px; color:{INK}; overflow:hidden; padding-bottom:12px;">
        <span id="w1-b0">일</span><span id="w1-b1">어</span><span id="w1-b2">났</span><span id="w1-b3">다</span></div>
    </div></div>""", emerge("w1") + """    const B = [0, .43, .84, 1.29, 1.72, 2.15, 2.57, 3.01];
    [0, 1, 2].forEach((g) => { for (let k = 0; k < 4; k++) {
      tl.fromTo("#w1-ray" + (g * 4 + k), { strokeDashoffset: 110 }, { strokeDashoffset: 0, duration: 0.3, ease: "expo.out" }, B[g + 1] - 0.04);
    } });
    ["#w1-a0", "#w1-a1", "#w1-a2", "#w1-a3"].forEach((s, i) => tl.fromTo(s, { yPercent: 110 }, { yPercent: 0, duration: 0.45, ease: "expo.out" }, B[1] - 0.08 + i * 0.05));
    ["#w1-b0", "#w1-b1", "#w1-b2", "#w1-b3"].forEach((s, i) => tl.fromTo(s, { yPercent: 110 }, { yPercent: 0, duration: 0.45, ease: "expo.out" }, B[3] - 0.08 + i * 0.05));
""" + dive("w1", SUN[0], SUN[1], 8, 3.44), 3.44)

# ---------- w2: 알람시계 ----------
C = (640, 560)
files["w2"] = scene("w2", ORANGE, f"""    <div id="w2-cam" class="cam"><div id="w2-stage" class="stage">
      <svg class="art" viewBox="0 0 1920 1080">
        <g id="w2-clock">
          <line x1="{C[0] - 150}" y1="{C[1] + 215}" x2="{C[0] - 205}" y2="{C[1] + 300}" stroke="{INK}" stroke-width="30" stroke-linecap="round"/>
          <line x1="{C[0] + 150}" y1="{C[1] + 215}" x2="{C[0] + 205}" y2="{C[1] + 300}" stroke="{INK}" stroke-width="30" stroke-linecap="round"/>
          <path d="M{C[0] - 270} {C[1] - 165} A 82 82 0 0 1 {C[0] - 120} {C[1] - 275} Z" fill="{INK}"/>
          <path d="M{C[0] + 120} {C[1] - 275} A 82 82 0 0 1 {C[0] + 270} {C[1] - 165} Z" fill="{INK}"/>
          <line x1="{C[0]}" y1="{C[1] - 262}" x2="{C[0]}" y2="{C[1] - 315}" stroke="{INK}" stroke-width="22" stroke-linecap="round"/>
          <circle cx="{C[0]}" cy="{C[1]}" r="260" fill="{CREAM}" stroke="{INK}" stroke-width="28"/>
{ticks(C[0], C[1], 200, 228, "w2")}
          <line id="w2-hour" x1="{C[0]}" y1="{C[1]}" x2="{C[0]}" y2="{C[1] - 118}" stroke="{INK}" stroke-width="24" stroke-linecap="round"/>
          <line id="w2-min" x1="{C[0]}" y1="{C[1]}" x2="{C[0]}" y2="{C[1] - 182}" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>
          <circle cx="{C[0]}" cy="{C[1]}" r="20" fill="{INK}"/>
        </g>
      </svg>
      <div id="w2-c0" class="w" style="left:1010px; top:372px; font-size:230px; color:{INK};">따</div>
      <div id="w2-c1" class="w" style="left:1240px; top:440px; font-size:230px; color:{INK};">르</div>
      <div id="w2-c2" class="w" style="left:1470px; top:372px; font-size:230px; color:{INK};">릉</div>
    </div></div>""", emerge("w2") + f"""    const B = [0, .42, .85, 1.27, 1.71, 2.14, 2.57, 2.99];
    tl.fromTo("#w2-min", {{ rotation: 0, svgOrigin: "{C[0]} {C[1]}" }}, {{ rotation: 1080, duration: B[2], ease: "power2.inOut", svgOrigin: "{C[0]} {C[1]}" }}, 0);
    tl.fromTo("#w2-hour", {{ rotation: 120, svgOrigin: "{C[0]} {C[1]}" }}, {{ rotation: 210, duration: B[2], ease: "power2.inOut", svgOrigin: "{C[0]} {C[1]}" }}, 0);
    for (let k = 0; k < 12; k++) {{
      tl.to("#w2-clock", {{ rotation: k % 2 ? -4 : 4, duration: 0.07, ease: "none", svgOrigin: "{C[0]} {C[1] + 260}" }}, B[2] + k * 0.0717);
    }}
    tl.to("#w2-clock", {{ rotation: 0, duration: 0.08, ease: "power2.out", svgOrigin: "{C[0]} {C[1] + 260}" }}, B[2] + 12 * 0.0717);
    [["#w2-c0", -8, 2], ["#w2-c1", 6, 3], ["#w2-c2", -5, 4]].forEach(([s, r, b]) => {{
      tl.set(s, {{ opacity: 0 }}, 0);
      tl.set(s, {{ opacity: 1, scale: 1.3, rotation: r * 2 }}, B[b]);
      tl.to(s, {{ scale: 1, rotation: r, duration: 0.22, ease: "expo.out" }}, B[b] + 0.001);
    }});
""" + dive("w2", C[0] + 60, C[1] + 90, 24, 3.42), 3.42)

# ---------- w3: 눈 ----------
files["w3"] = scene("w3", CREAM, f"""    <div id="w3-cam" class="cam"><div id="w3-stage" class="stage">
      <svg class="art" viewBox="0 0 1920 1080">
        <defs><clipPath id="w3-clip"><path d="M470 540 Q960 215 1450 540 Q960 865 470 540 Z"/></clipPath></defs>
        <g id="w3-eye">
          <path d="M470 540 Q960 215 1450 540 Q960 865 470 540 Z" fill="#FFFFFF"/>
          <g clip-path="url(#w3-clip)">
            <circle cx="960" cy="540" r="168" fill="{COFFEE}"/>
            <circle cx="960" cy="540" r="80" fill="{INK}"/>
            <circle cx="1032" cy="468" r="26" fill="{CREAM}"/>
          </g>
          <path d="M470 540 Q960 215 1450 540 Q960 865 470 540 Z" fill="none" stroke="{INK}" stroke-width="20" stroke-linejoin="round"/>
        </g>
      </svg>
      <div id="w3-l" class="w" style="left:150px; top:400px; font-size:280px; color:{INK};">번</div>
      <div id="w3-r" class="w" style="left:1490px; top:400px; font-size:280px; color:{INK};">쩍</div>
    </div></div>""", emerge("w3") + """    const B = [0, .42, .85, 1.29, 1.71, 2.14, 2.57, 3.00];
    tl.set("#w3-eye", { scaleY: 0.04, svgOrigin: "960 540" }, 0);
    tl.to("#w3-eye", { scaleY: 1, duration: 0.16, ease: "expo.out", svgOrigin: "960 540" }, B[2] - 0.04);
    tl.fromTo("#w3-l", { x: -620 }, { x: 0, duration: 0.24, ease: "expo.out" }, B[2] - 0.12);
    tl.fromTo("#w3-r", { x: 620 }, { x: 0, duration: 0.24, ease: "expo.out" }, B[2] - 0.12);
""" + dive("w3", 960, 540, 16, 3.43), 3.43)

# ---------- w4: 커피 ----------
K = (1240, 540)
files["w4"] = scene("w4", INK, f"""    <div id="w4-cam" class="cam"><div id="w4-stage" class="stage">
      <svg class="art" viewBox="0 0 1920 1080">
        <circle cx="{K[0]}" cy="{K[1]}" r="330" fill="{CREAM}"/>
        <circle cx="{K[0]}" cy="{K[1]}" r="282" fill="none" stroke="#DCCFB9" stroke-width="8"/>
        <ellipse cx="{K[0] + 262}" cy="{K[1]}" rx="62" ry="40" fill="none" stroke="#FFFFFF" stroke-width="30"/>
        <circle cx="{K[0]}" cy="{K[1]}" r="235" fill="#FFFFFF"/>
        <circle cx="{K[0]}" cy="{K[1]}" r="200" fill="{COFFEE}"/>
        <circle id="w4-crema" cx="{K[0]}" cy="{K[1]}" r="150" fill="none" stroke="#B07A4C" stroke-width="12"/>
      </svg>
      <div class="w" style="left:170px; top:450px; font-size:180px; color:{CREAM};">
        <span id="w4-c0">첫</span><span>&nbsp;</span><span id="w4-c1">모</span><span id="w4-c2">금</span></div>
    </div></div>""", emerge("w4") + f"""    const B = [0, .42, .86, 1.28, 1.71, 2.15, 2.57, 3.00];
    ["#w4-c0", "#w4-c1", "#w4-c2"].forEach((s, i) => {{ tl.set(s, {{ opacity: 0 }}, 0); tl.set(s, {{ opacity: 1 }}, B[i + 1]); }});
    tl.fromTo("#w4-crema", {{ scale: 0.55, svgOrigin: "{K[0]} {K[1]}" }}, {{ scale: 1, duration: 0.7, ease: "expo.out", svgOrigin: "{K[0]} {K[1]}" }}, B[4]);
""" + dive("w4", K[0], K[1], 12, 3.42), 3.42)

# ---------- w5: 문손잡이 ----------
N = (1340, 560)
files["w5"] = scene("w5", COFFEE, f"""    <div id="w5-cam" class="cam"><div id="w5-stage" class="stage">
      <svg class="art" viewBox="0 0 1920 1080">
        <rect x="1652" y="-40" width="18" height="1160" fill="{DARKCOFFEE}"/>
        <circle cx="{N[0]}" cy="{N[1]}" r="160" fill="#E2D4BC"/>
        <g id="w5-knob">
          <circle cx="{N[0]}" cy="{N[1]}" r="112" fill="{CREAM}" stroke="{DARKCOFFEE}" stroke-width="10"/>
          <line x1="{N[0]}" y1="{N[1] - 62}" x2="{N[0]}" y2="{N[1] - 96}" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>
        </g>
      </svg>
      <div class="w" style="left:220px; top:450px; font-size:200px; color:{CREAM};">
        <span id="w5-c0">문</span><span>&nbsp;</span><span id="w5-c1">열</span><span id="w5-c2">고</span></div>
    </div></div>""", emerge("w5") + f"""    const B = [0, .45, .86, 1.29, 1.71, 2.14, 2.56, 3.00];
    tl.fromTo("#w5-c0", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.3, ease: "power4.out" }}, B[1] - 0.05);
    tl.fromTo("#w5-knob", {{ rotation: 0, svgOrigin: "{N[0]} {N[1]}" }}, {{ rotation: -90, duration: 0.35, ease: "power3.out", svgOrigin: "{N[0]} {N[1]}" }}, B[2] - 0.06);
    tl.fromTo(["#w5-c1", "#w5-c2"], {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.3, ease: "power4.out", stagger: 0.06 }}, B[3] - 0.05);
""" + dive("w5", N[0], N[1], 40, 3.41), 3.41)

# ---------- w6: 신호등 ----------
files["w6"] = scene("w6", CREAM, f"""    <div id="w6-cam" class="cam"><div id="w6-stage" class="stage">
      <svg class="art" viewBox="0 0 1920 1080">
        <rect x="940" y="600" width="40" height="520" fill="{INK}"/>
        <rect x="470" y="330" width="980" height="280" rx="70" fill="{INK}"/>
        <circle cx="640" cy="470" r="112" fill="#5A2A25"/>
        <circle cx="960" cy="470" r="112" fill="#5A4A20"/>
        <circle cx="1280" cy="470" r="112" fill="#1F3B2A"/>
        <circle id="w6-red" cx="640" cy="470" r="112" fill="#E0453A"/>
        <circle id="w6-yel" cx="960" cy="470" r="112" fill="#F2B33D"/>
        <circle id="w6-grn" cx="1280" cy="470" r="112" fill="{GREEN}"/>
      </svg>
      <div id="w6-go" class="w" style="left:300px; top:660px; font-size:300px; color:{INK};">가자</div>
    </div></div>""", emerge("w6") + """    const B = [0, .44, .86, 1.31, 1.73, 2.16, 2.60, 3.03];
    tl.set("#w6-red", { opacity: 1 }, 0); tl.set("#w6-yel", { opacity: 0 }, 0); tl.set("#w6-grn", { opacity: 0 }, 0); tl.set("#w6-go", { opacity: 0 }, 0);
    tl.set("#w6-red", { opacity: 0 }, B[1]); tl.set("#w6-yel", { opacity: 1 }, B[1]);
    tl.set("#w6-yel", { opacity: 0 }, B[2]); tl.set("#w6-grn", { opacity: 1 }, B[2]);
    tl.set("#w6-go", { opacity: 1, scale: 1.4 }, B[2]);
    tl.to("#w6-go", { scale: 1, duration: 0.3, ease: "expo.out", transformOrigin: "0% 100%" }, B[2] + 0.001);
""" + dive("w6", 1280, 470, 22, 3.45), 3.45)

# ---------- end: 오늘 ----------
LE, TE = 511, 260
OE = (round(LE + 224.2), round(TE + 179.3))
files["end"] = scene("end", CREAM, f"""    <div id="end-cam" class="cam">
      <svg class="art" viewBox="0 0 1920 1080"><ellipse cx="{OE[0]}" cy="{OE[1]}" rx="112" ry="80" fill="{GREEN}"/></svg>
      <div id="end-word" class="w" style="left:{LE}px; top:{TE}px; font-size:520px; color:{INK};">오늘</div>
    </div>
    <div id="end-sub" class="w" style="left:1060px; top:800px; font-size:100px; color:{INK};">10월, 시작</div>""", f"""    const B = [0, .43, .85, 1.29, 1.71, 2.15, 2.57, 3.00];
    tl.fromTo("#end-cam", {{ scale: 20 }}, {{ scale: 1, duration: B[4], ease: "expo.out", transformOrigin: "{OE[0]}px {OE[1]}px" }}, 0);
    tl.fromTo("#end-sub", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.5, ease: "power4.out" }}, B[6] - 0.08);
""", 5.68)

comp = ROOT / "compositions"
comp.mkdir(exist_ok=True)
for sid, text in files.items():
    (comp / f"{sid}.html").write_text(text.replace("    const B = window.__B_" + sid + " = null;\n", ""), encoding="utf-8")

# ---------- index.html ----------
hosts = []
for i, (sid, start, dur, _) in enumerate(SCENES):
    hosts.append(f'''      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" class="clip"
        data-start="{start}" data-duration="{dur}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>''')

audio = [('bgm', 'assets/bgm/fresh-morning.mp3', 3.75, 26.25, 0, 0.9)]
for k, t in enumerate([0.74, 1.17, 1.60, 2.03, 2.46, 2.89]):
    audio.append((f"tick{k}", "assets/sfx/click-soft.mp3", t, 0.36, 0, 0.55))
# whoosh peaks 0.1 s into the file, whoosh-cinematic at 2.7 s: both peak on the cut that ends each dive
for k, (t, f, ms, d) in enumerate([(3.68, "whoosh", 0, 0.57), (6.69, "whoosh-cinematic", 2.2, 0.9), (10.54, "whoosh", 0, 0.57),
                                    (13.54, "whoosh-cinematic", 2.2, 0.9), (17.39, "whoosh", 0, 0.57), (20.37, "whoosh-cinematic", 2.2, 0.9)]):
    audio.append((f"dive{k}", f"assets/sfx/{f}.mp3", t, d, ms, 0.8))
audio += [("hit-clock", "assets/sfx/impact-bass-1.mp3", 8.04, 1.5, 0, 0.5),
          ("riser", "assets/sfx/riser.mp3", 21.80, 2.52, 1.9, 0.6),
          ("hit-end", "assets/sfx/impact-bass-2.mp3", 26.03, 2.0, 0, 0.8)]
aud = []
for k, (aid, src, start, dur, ms, vol) in enumerate(audio):
    extra = ' data-fade-out="1.5"' if aid == "bgm" else ""
    aud.append(f'      <audio id="{aid}" class="clip" src="{src}" data-start="{start}" data-duration="{dur}" '
               f'data-media-start="{ms}" data-volume="{vol}" data-track-index="{2 if aid == 'bgm' else (4 if aid.startswith('tick') else 3)}"{extra}></audio>')

index = f"""<!doctype html>
<html lang="ko" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: {CREAM}; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="30" data-width="1920" data-height="1080">
{chr(10).join(hosts)}
{chr(10).join(aud)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
(ROOT / "index.html").write_text(index, encoding="utf-8")
print("wrote", len(files), "scenes")
