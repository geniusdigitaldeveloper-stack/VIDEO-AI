#!/usr/bin/env python3
"""Bina semula aset + index.html untuk video "Setup Global Streamer".

Guna:  python3 scripts/build.py <source.mp4> [--html-only]

Langkah:
  1. Edit decision list (EDL) dari transcript.json: buang pause, 2x bahagian senyap, buang ayat ulang.
  2. ffmpeg -> assets/base.mp4 (hook cold-open + tutorial, 2560x1440 supaya zoom kekal tajam).
  3. Sintesis muzik latar + SFX (numpy) -> assets/*.wav
  4. Jana index.html (zoom, ring, callout, subtitle, logo, outro) dengan masa yang sudah dipetakan.
"""
import json, math, os, subprocess, sys, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets")
os.makedirs(A, exist_ok=True)
SRC = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else None
HTML_ONLY = "--html-only" in sys.argv
SRC_DUR = 126.29

# ---------------------------------------------------------------- transcript
T = json.load(open(os.path.join(ROOT, "transcript.json")))
words = [w for s in T for w in s["words"]]
FIX = {"mock": "more", "bagian": "Bahagian", "buat": None}  # 'buat turun' -> 'muat turun' handled below
EN = set("""ok okay first set up setup email scroll link copy ctrl direct suggestion download paste enter auto
file extract so open more info run anyway device only for me next browser install finish live stream key
streaming c v""".split())

REMOVE = [(79.08, 80.66)]          # ayat ulang: "atau apa-apa memang takkan ada"
HOOK = (62.90, 66.95)              # klik OPEN -> dijadikan opening

def clean(w):
    return w.strip().strip(".,?!").strip()

# ---------------------------------------------------------------- EDL
SIL = json.load(open(os.path.join(ROOT, "silences.json")))   # ffmpeg silencedetect -38dB, >=0.45s

def build_edl():
    """-> list of (src_start, src_end, speed). Pause pendek dibuang, pause panjang (loading/aksi skrin) 2x."""
    PAD = 0.16
    cuts = []                                   # (a, b, mode) mode: 'cut' | '2x'
    for a, b in SIL:
        a, b = a + PAD, b - PAD
        if b - a < 0.12:
            continue
        cuts.append((a, b, "cut" if b - a <= 0.9 else "2x"))
    for a, b in REMOVE:
        cuts = [c for c in cuts if c[1] <= a or c[0] >= b]
        cuts.append((a, b, "cut"))
    cuts.sort()
    segs, cur = [], 0.0
    for a, b, mode in cuts:
        if a > cur:
            segs.append((cur, a, 1.0))
        if mode == "2x":
            segs.append((a, b, 2.0))
        cur = b
    if SRC_DUR - cur > 0.05:
        segs.append((cur, SRC_DUR, 1.0))
    return segs

EDL = build_edl()
HOOK_DUR = HOOK[1] - HOOK[0]
FPS = 30
def q(x):  # kunci pada grid frame
    return round(x * FPS) / FPS

# peta masa sumber -> masa output (bahagian tutorial)
MAP = []
t = HOOK_DUR
for s, e, v in EDL:
    d = (e - s) / v
    MAP.append((s, e, v, t))
    t += d
MAIN_END = t
OUTRO = 4.6
TOTAL = q(MAIN_END + OUTRO)

def m(ts):
    """source time -> output time (tutorial). Masa dalam bahagian yang dipotong jatuh ke potongan seterusnya."""
    for s, e, v, o in MAP:
        if ts < s:
            return o
        if s <= ts <= e:
            return o + (ts - s) / v
    return MAIN_END

def mh(ts):  # source time -> output time (hook)
    return ts - HOOK[0]

# ---------------------------------------------------------------- ffmpeg base
def render_base():
    """Encode setiap segmen berasingan (jimat memori), kemudian concat + loudnorm."""
    parts = [(HOOK[0], HOOK[1], 1.0)] + EDL
    tmp = os.path.join(A, "_seg"); os.makedirs(tmp, exist_ok=True)
    lst = []
    for i, (s, e, v) in enumerate(parts):
        out = os.path.join(tmp, f"s{i:03d}.mp4")
        d = (e - s) / v
        vf = f"setpts=(PTS-STARTPTS)/{v},fps={FPS},scale=2560:1440:flags=lanczos,unsharp=5:5:0.45:5:5:0.0,format=yuv420p"
        af = "asetpts=PTS-STARTPTS" + (f",atempo={v},volume=0.35" if v != 1.0 else "")
        af += f",afade=t=in:d=0.02,afade=t=out:st={max(0, d - 0.03):.3f}:d=0.03,aresample=48000"
        subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-t", f"{e - s:.3f}", "-i", SRC,
                               "-vf", vf, "-af", af, "-c:v", "libx264", "-preset", "medium", "-crf", "15",
                               "-threads", "3", "-g", str(FPS), "-c:a", "pcm_s16le", "-t", f"{d:.3f}",
                               out.replace(".mp4", ".mov")])
        lst.append(f"file '{out.replace('.mp4', '.mov')}'")
    open(os.path.join(tmp, "list.txt"), "w").write("\n".join(lst))
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "list.txt"),
                           "-c:v", "copy", "-af", "highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000",
                           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", os.path.join(A, "base.mp4")])
    import shutil; shutil.rmtree(tmp)

# ---------------------------------------------------------------- audio synth
SR = 48000
def save_wav(name, x):
    x = np.clip(x, -1, 1)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    w = wave.open(os.path.join(A, name), "wb")
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()

def lowpass(x, fc):
    a = math.exp(-2 * math.pi * fc / SR)
    y = np.empty_like(x); acc = 0.0
    # satu kutub, cukup untuk pad lembut
    from numpy.lib.stride_tricks import sliding_window_view  # noqa
    for i in range(0, len(x), 1):
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y

def synth_music(dur):
    """Pad ambient tenang: Cmaj7 - Am7 - Fmaj7 - G6, 8s setiap kord, + not loceng perlahan."""
    n = int(dur * SR); tt = np.arange(n) / SR
    chords = [[130.81, 196.00, 246.94, 329.63], [110.00, 164.81, 196.00, 261.63],
              [87.31, 174.61, 220.00, 329.63], [98.00, 146.83, 196.00, 293.66]]
    bells = [[659.25, 783.99], [523.25, 659.25], [698.46, 523.25], [587.33, 783.99]]
    L = np.zeros(n); R = np.zeros(n); CH = 8.0
    for k in range(int(dur / CH) + 1):
        c = chords[k % 4]; s0 = k * CH
        env = np.clip((tt - s0) / 2.5, 0, 1) * np.clip((s0 + CH + 2.5 - tt) / 2.5, 0, 1)
        env = np.sin(env * np.pi / 2) ** 2
        for j, f in enumerate(c):
            for det, ch in ((-0.25, L), (0.25, R)):
                ph = 2 * np.pi * (f + det) * tt
                ch += env * (0.5 * np.sin(ph) + 0.12 * np.sin(2 * ph) + 0.04 * np.sin(3 * ph)) * (0.9 - 0.12 * j)
        for j, f in enumerate(bells[k % 4]):
            b0 = s0 + 1.0 + 3.5 * j
            e = np.where(tt >= b0, np.exp(-(tt - b0) / 1.6), 0.0)
            tone = e * np.sin(2 * np.pi * f * tt) * 0.22
            (L if j == 0 else R)[:] += tone * 0.8; (R if j == 0 else L)[:] += tone * 0.4
    lfo = 0.85 + 0.15 * np.sin(2 * np.pi * 0.07 * tt)
    x = np.stack([L * lfo, R * lfo], 1)
    x /= np.abs(x).max() + 1e-9
    fade = np.clip(tt / 2.0, 0, 1) * np.clip((dur - tt) / 3.0, 0, 1)
    save_wav("music.wav", x * 0.6 * fade[:, None])

def synth_sfx():
    # impact lembut: sub thump + udara
    d = 1.4; tt = np.arange(int(d * SR)) / SR
    f = 46 + 70 * np.exp(-tt * 18)
    thump = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 4.2)
    rng = np.random.default_rng(7)
    air = lowpass(rng.standard_normal(len(tt)), 900) * np.exp(-tt * 7) * 1.6
    pre = int(0.35 * SR); tp = np.arange(pre) / SR
    whoosh = lowpass(rng.standard_normal(pre), 1400) * (tp / 0.35) ** 3 * 1.2
    x = np.concatenate([whoosh, thump * 0.9 + air * 0.35])
    save_wav("impact.wav", x / (np.abs(x).max() + 1e-9) * 0.85)
    # pop kecil untuk callout step
    d = 0.16; tt = np.arange(int(d * SR)) / SR
    pop = np.sin(2 * np.pi * (520 + 500 * np.exp(-tt * 40)) * tt) * np.exp(-tt * 34)
    save_wav("pop.wav", pop * 0.5)

# ---------------------------------------------------------------- overlay data (masa sumber)
# (nombor step, label, [(t_src, x, y), ...] laluan cursor, t_end_src)
STEPS = [
    (1, "Buka email", [(6.2, 850, 440), (9.0, 700, 530), (9.8, 750, 485)], 10.4),
    (2, "Highlight link", [(11.8, 730, 468), (12.8, 1125, 482)], 17.8),
    (2, "Klik kanan → Copy", [(18.4, 1128, 520), (19.4, 1183, 650)], 20.2),
    (3, "Buka Chrome", [(27.6, 1396, 1012), (28.9, 1364, 1040)], 29.7),
    (4, "Klik address bar", [(30.5, 448, 68)], 33.6),
    (4, "Paste (Ctrl+V)", [(37.9, 548, 244)], 40.0),
    (5, "Tekan Enter", [(40.2, 560, 228), (41.6, 690, 172)], 42.2),
    (6, "Auto download", [(42.9, 1822, 70), (44.8, 1808, 124), (45.4, 1700, 170)], 48.6),
    (7, "Tekan Open", [(58.2, 1782, 160), (61.6, 1814, 158)], 66.5),
    (8, "More info", [(67.0, 770, 392), (67.6, 756, 388)], 68.9),
    (9, "Run anyway", [(80.9, 1010, 680), (81.2, 1032, 718)], 82.0),
    (10, "Only for me", [(87.7, 780, 528), (89.4, 772, 482), (90.1, 782, 528)], 90.9),
    (11, "Next", [(91.1, 1074, 672), (91.4, 1074, 684)], 92.2),
    (12, "Install", [(95.2, 1072, 682)], 96.6),
    (13, "Finish", [(105.3, 1100, 726), (105.6, 1073, 716)], 107.5),
    (14, "Masukkan Stream Key", [(114.2, 1470, 497)], 117.9),
    (15, "Mula Live", [(118.1, 1527, 128)], 120.6),
]
# zoom: (t_in_src, t_out_src, cx, cy, scale)
ZOOMS = [
    (11.4, 25.4, 930, 500, 1.30),
    (30.2, 41.9, 520, 170, 1.30),
    (42.5, 66.6, 1680, 170, 1.30),
    (66.9, 82.1, 960, 540, 1.22),
    (84.2, 107.4, 960, 580, 1.30),
    (113.6, 120.8, 1500, 300, 1.25),
]
HOOK_TEXT = ("SETUP GLOBAL STREAMER", "siap dalam 2 minit — ikut je step ni")
CLICK_OUT = mh(65.85)

def zoom_xy(cx, cy, s):
    x = min(0, max(1920 - 1920 * s, 960 - cx * s))
    y = min(0, max(1080 - 1080 * s, 540 - cy * s))
    return round(x, 1), round(y, 1)

# ---------------------------------------------------------------- subtitles
def subtitle_chunks():
    chunks = []
    def emit(ws, mapper, limit=None):
        cur = []
        def flush():
            nonlocal cur
            if cur:
                chunks.append(cur); cur = []
        prev_e = None
        for w in ws:
            txt = clean(w["w"])
            if not txt:
                continue
            low = txt.lower()
            if low == "way" and prev_e is not None:        # serpihan "anyway" berganda
                continue
            if low == "mock": txt = "more"
            if low == "bagian": txt = "bahagian"
            if low == "buat" and abs(w["s"] - 20.9) < 1.0: txt = "muat"
            low = txt.lower()
            if prev_e is not None and (w["s"] - prev_e > 0.45 or len(cur) >= 4):
                flush()
            cur.append({"t": txt, "en": low in EN, "s": mapper(w["s"]), "e": mapper(w["e"])})
            prev_e = w["e"]
            if w["w"].strip()[-1:] in ".?!":
                flush()
        flush()
    hook_w = [w for w in words if HOOK[0] - 0.05 <= w["s"] and w["e"] <= HOOK[1]]
    emit(hook_w, mh)
    nh = len(chunks)
    main_w = [w for w in words if not any(a <= w["s"] < b for a, b in REMOVE)]
    emit(main_w, m)
    out = []
    for i, c in enumerate(chunks):
        s = c[0]["s"]; e = c[-1]["e"] + 0.25
        if i + 1 < len(chunks) and i + 1 != nh:
            e = min(e, chunks[i + 1][0]["s"])
        if i + 1 == nh:
            e = min(e, HOOK_DUR - 0.02)
        e = max(e, s + 0.3)
        out.append({"s": q(s), "e": q(e), "w": [(x["t"], x["en"]) for x in c]})
    # paksa tiada tindihan
    for a, b in zip(out, out[1:]):
        if a["e"] > b["s"]:
            a["e"] = b["s"]
    return out

# ---------------------------------------------------------------- HTML
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def build_html():
    subs = subtitle_chunks()
    sub_html = []
    for i, c in enumerate(subs):
        inner = " ".join(f"<i>{esc(t)}</i>" if en else esc(t) for t, en in c["w"])
        sub_html.append(f'<div class="sub" id="sub{i}">{inner}</div>')

    steps_js, step_html, pops = [], [], []
    for i, (num, label, path, t_end) in enumerate(STEPS):
        pts = [(q(m(ts)), x, y) for ts, x, y in path]
        end = q(m(t_end))
        if end - pts[0][0] < 0.7:
            end = q(pts[0][0] + 0.7)
        flip_x = pts[-1][1] > 1480 or pts[0][1] > 1480
        flip_y = max(p[2] for p in pts) > 900
        cls = "co" + (" fx" if flip_x else "") + (" fy" if flip_y else "")
        step_html.append(
            f'<div class="cur" id="cur{i}"><div class="ring"></div><div class="ring r2"></div>'
            f'<div class="{cls}"><span class="n">{num}</span><span class="l">{esc(label)}</span></div></div>')
        steps_js.append({"pts": pts, "end": end})
        pops.append(pts[0][0])

    zoom_js = []
    for a, b, cx, cy, s in ZOOMS:
        x, y = zoom_xy(cx, cy, s)
        zoom_js.append({"a": q(m(a)), "b": q(m(b)), "x": x, "y": y, "s": s})

    logos = [float(tt) for tt in range(10, int(MAIN_END) - 3, 10)]
    hz = zoom_xy(1812, 160, 1.55); hz2 = zoom_xy(1812, 160, 1.72)
    main_d = q(MAIN_END)

    pop_audio = "\n".join(
        f'      <audio id="pop{i}" class="clip" data-start="{max(0, tt - 0.02):.3f}" data-duration="0.16" '
        f'data-track-index="{6 + i % 2}" data-volume="0.22" src="assets/pop.wav"></audio>'
        for i, tt in enumerate(pops))

    html = f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Poppins"; font-weight: 600; font-style: normal; src: url("assets/fonts/poppins-600.woff2") format("woff2"); }}
      @font-face {{ font-family: "Poppins"; font-weight: 600; font-style: italic; src: url("assets/fonts/poppins-600-italic.woff2") format("woff2"); }}
      @font-face {{ font-family: "Poppins"; font-weight: 800; font-style: normal; src: url("assets/fonts/poppins-800.woff2") format("woff2"); }}
      :root {{ --sky: #38BDF8; --ink: #0B1020; --ground: #0e1116; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: var(--ground); }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; font-family: "Poppins", sans-serif; background: var(--ground); }}
      .clip {{ position: absolute; left: 0; top: 0; }}

      /* pentas yang di-zoom: rakaman skrin + ring + callout bergerak bersama */
      #stage {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; transform-origin: 0 0; will-change: transform; }}
      /* gred neutral, sangat halus: skrin kekal nampak asli */
      #base {{ width: 1920px; height: 1080px; object-fit: cover; filter: contrast(1.035) saturate(1.03) brightness(0.995); }}

      .cur {{ position: absolute; left: 0; top: 0; width: 0; height: 0; opacity: 0; }}
      .ring {{ position: absolute; left: -30px; top: -30px; width: 60px; height: 60px; border-radius: 50%;
               border: 3px solid rgba(56,189,248,.95); background: rgba(56,189,248,.10);
               box-shadow: 0 0 0 1px rgba(11,16,32,.25), 0 0 18px rgba(56,189,248,.35); }}
      .ring.r2 {{ background: none; box-shadow: none; border-width: 2px; opacity: 0; }}
      .co {{ position: absolute; left: 40px; top: 30px; display: flex; align-items: center; gap: 10px; white-space: nowrap;
             padding: 7px 16px 7px 7px; border-radius: 999px; background: rgba(14,17,22,.92);
             box-shadow: 0 6px 18px rgba(0,0,0,.28); transform-origin: 0 0; }}
      .co.fx {{ left: auto; right: 40px; transform-origin: 100% 0; }}
      .co.fy {{ top: auto; bottom: 34px; }}
      .co .n {{ width: 34px; height: 34px; border-radius: 50%; background: var(--sky); color: var(--ink);
                font: 800 19px/34px "Poppins", sans-serif; text-align: center; }}
      .co .l {{ color: #fff; font: 600 22px/1 "Poppins", sans-serif; letter-spacing: .01em; }}

      /* subtitle ucapan: Poppins SemiBold, #38BDF8, Inggeris italic — di bawah frame */
      #subs {{ position: absolute; left: 0; right: 0; bottom: 64px; height: 70px; }}
      .sub {{ position: absolute; left: 0; right: 0; bottom: 0; text-align: center; opacity: 0;
              font: 600 50px/1.25 "Poppins", sans-serif; color: var(--sky);
              -webkit-text-stroke: 6px var(--ink); paint-order: stroke fill;
              text-shadow: 0 3px 10px rgba(11,16,32,.5); }}
      .sub i {{ font-style: italic; }}

      /* hook */
      #hook {{ position: absolute; left: 90px; top: 500px; opacity: 0; padding: 38px 48px 42px; border-radius: 28px;
               background: rgba(14,17,22,.90); box-shadow: 0 18px 50px rgba(0,0,0,.35); transform-origin: 0 100%; }}
      #hook .h1 {{ font: 800 112px/1.04 "Poppins", sans-serif; color: #fff; letter-spacing: -0.02em; }}
      #hook .h2 {{ margin-top: 22px; display: inline-block; padding: 10px 22px; border-radius: 12px; background: var(--sky);
                   color: var(--ink); font: 600 40px/1.15 "Poppins", sans-serif; }}
      #dip {{ position: absolute; inset: 0; background: var(--ground); opacity: 0; }}

      /* logo popup */
      #logo {{ position: absolute; left: 22px; top: 22px; width: 128px; height: 128px; opacity: 0;
               filter: drop-shadow(0 6px 14px rgba(0,0,0,.35)); }}
      #logo img, #outro .lg img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}

      /* outro */
      #outro {{ position: absolute; inset: 0; background: var(--ground); opacity: 0; display: flex; flex-direction: column;
                align-items: center; justify-content: center; }}
      #outro .lg {{ width: 420px; height: 420px; filter: drop-shadow(0 20px 50px rgba(0,0,0,.5)); }}
      #outro .t1 {{ margin-top: 26px; font: 800 76px/1 "Poppins", sans-serif; color: #fff; letter-spacing: -0.01em; }}
      #outro .t2 {{ margin-top: 20px; font: 600 36px/1 "Poppins", sans-serif; color: var(--sky); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1920" data-height="1080" data-fps="{FPS}">
      <div id="stage">
        <video id="base" class="clip" data-start="0" data-duration="{main_d:.3f}" data-track-index="0" data-has-audio="true" src="assets/base.mp4" playsinline></video>
        {"".join(step_html)}
      </div>
      <div id="dip"></div>
      <div id="hook"><div class="h1">{esc(HOOK_TEXT[0]).replace(" GLOBAL", "<br />GLOBAL")}</div><div class="h2">{esc(HOOK_TEXT[1])}</div></div>
      <div id="subs">{"".join(sub_html)}</div>
      <div id="logo"><img src="assets/logo.png" alt="Global Streamer" /></div>
      <div id="outro">
        <div class="lg"><img src="assets/logo.png" alt="Global Streamer" /></div>
        <div class="t1">Global Streamer</div>
        <div class="t2">Selamat mencuba, semoga berjaya!</div>
      </div>

      <audio id="music" class="clip" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="4" data-volume="0.10" data-fade-in="1.5" data-fade-out="3" src="assets/music.wav"></audio>
      <audio id="impact" class="clip" data-start="{max(0, CLICK_OUT - 0.35):.3f}" data-duration="1.75" data-track-index="5" data-volume="0.55" src="assets/impact.wav"></audio>
{pop_audio}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const SUBS = {json.dumps([[c["s"], c["e"]] for c in subs])};
      const STEPS = {json.dumps(steps_js)};
      const ZOOMS = {json.dumps(zoom_js)};
      const LOGOS = {json.dumps(logos)};
      const HOOK_DUR = {HOOK_DUR:.3f}, CLICK = {CLICK_OUT:.3f}, MAIN_END = {main_d:.3f}, TOTAL = {TOTAL:.3f};

      // ---- hook: push-in sinematik ke butang Open, punch masa klik, teks pop-in
      tl.set("#stage", {{ x: 0, y: 0, scale: 1 }}, 0);
      tl.to("#stage", {{ x: {hz[0]}, y: {hz[1]}, scale: 1.55, duration: CLICK - 0.1, ease: "power2.inOut" }}, 0.05);
      tl.to("#stage", {{ x: {hz2[0]}, y: {hz2[1]}, scale: 1.72, duration: 0.22, ease: "power3.out" }}, CLICK);
      tl.fromTo("#hook", {{ opacity: 0, scale: 0.72, y: 40 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.42, ease: "back.out(1.9)" }}, CLICK - 0.02);
      tl.to("#dip", {{ opacity: 1, duration: 0.2, ease: "power1.in" }}, HOOK_DUR - 0.2);
      tl.set("#hook", {{ opacity: 0 }}, HOOK_DUR);
      tl.set("#stage", {{ x: 0, y: 0, scale: 1 }}, HOOK_DUR);
      tl.to("#dip", {{ opacity: 0, duration: 0.3, ease: "power1.out" }}, HOOK_DUR);

      // ---- zoom lembut ikut kawasan cursor
      ZOOMS.forEach((z) => {{
        tl.to("#stage", {{ x: z.x, y: z.y, scale: z.s, duration: 0.7, ease: "power2.inOut" }}, z.a);
        tl.to("#stage", {{ x: 0, y: 0, scale: 1, duration: 0.7, ease: "power2.inOut" }}, z.b);
      }});

      // ---- ring + callout step ikut mouse
      STEPS.forEach((s, i) => {{
        const el = "#cur" + i, p0 = s.pts[0];
        tl.set(el, {{ x: p0[1], y: p0[2] }}, 0);
        tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, ease: "power1.out" }}, p0[0]);
        tl.fromTo(el + " .ring", {{ scale: 0.55 }}, {{ scale: 1, duration: 0.35, ease: "back.out(2)" }}, p0[0]);
        tl.fromTo(el + " .r2", {{ scale: 1, opacity: 0.8 }}, {{ scale: 2.1, opacity: 0, duration: 0.7, ease: "power2.out" }}, p0[0] + 0.05);
        tl.fromTo(el + " .co", {{ scale: 0.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.28, ease: "back.out(1.6)" }}, p0[0] + 0.08);
        for (let k = 1; k < s.pts.length; k++) {{
          const a = s.pts[k - 1], b = s.pts[k];
          tl.to(el, {{ x: b[1], y: b[2], duration: Math.max(0.1, b[0] - a[0]), ease: "power1.inOut" }}, a[0]);
        }}
        tl.to(el, {{ opacity: 0, duration: 0.25, ease: "power1.in" }}, s.end - 0.25);
      }});

      // ---- subtitle
      SUBS.forEach((c, i) => {{
        tl.set("#sub" + i, {{ opacity: 1 }}, c[0]);
        tl.set("#sub" + i, {{ opacity: 0 }}, c[1]);
      }});

      // ---- logo popup setiap 10s (kiri atas)
      LOGOS.forEach((t) => {{
        tl.fromTo("#logo", {{ opacity: 0, scale: 0.4, rotation: -25 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(1.8)" }}, t);
        tl.to("#logo", {{ scale: 1.06, duration: 0.5, ease: "sine.inOut" }}, t + 0.9);
        tl.to("#logo", {{ scale: 1, duration: 0.5, ease: "sine.inOut" }}, t + 1.4);
        tl.to("#logo", {{ opacity: 0, scale: 0.6, duration: 0.35, ease: "power2.in" }}, t + 2.6);
      }});

      // ---- outro
      tl.fromTo("#outro", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "power2.inOut" }}, MAIN_END - 0.55);
      tl.fromTo("#outro .lg", {{ scale: 0.55, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 1.1, ease: "power3.out" }}, MAIN_END - 0.15);
      tl.fromTo("#outro .t1", {{ y: 34, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.8, ease: "power3.out" }}, MAIN_END + 0.45);
      tl.fromTo("#outro .t2", {{ y: 24, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.8, ease: "power3.out" }}, MAIN_END + 0.8);
      tl.to("#outro .lg", {{ scale: 1.045, duration: TOTAL - MAIN_END - 1.2, ease: "sine.inOut" }}, MAIN_END + 1.0);
      tl.set({{}}, {{}}, TOTAL);

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w").write(html)
    json.dump({"hook": HOOK, "edl": EDL, "main_end": MAIN_END, "total": TOTAL,
               "steps_out": [(n, l, round(m(p[0][0]), 2)) for n, l, p, _ in STEPS]},
              open(os.path.join(ROOT, "edl.json"), "w"), indent=1, ensure_ascii=False)

if __name__ == "__main__":
    print(f"EDL {len(EDL)} segmen | sumber {SRC_DUR:.1f}s -> tutorial {MAIN_END - HOOK_DUR:.1f}s + hook {HOOK_DUR:.1f}s + outro {OUTRO}s = {TOTAL:.1f}s")
    if not HTML_ONLY:
        if not SRC:
            sys.exit("perlu path video sumber")
        render_base(); synth_music(TOTAL); synth_sfx()
    build_html()
