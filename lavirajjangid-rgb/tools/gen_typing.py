# Generates assets/typing.svg : a self-animating typewriter (no JS, works inside <img> on GitHub).
#
# Design note: each tagline gets its OWN clipPath mask whose width is 0 except during that
# tagline's slot in the 15s cycle. Nothing relies on opacity keyframe windows (Chromium
# mishandles keyTimes that don't start at 0), so only one line can ever be visible.
CW   = 14.4                     # monospace advance width at font-size 24
FS   = 24
PROMPT = "$ laviraj@jaipur:~ "
PHRASES = [
    ("Robotics & Automation Enthusiast", "#00ff9d"),
    ("IoT + Embedded Systems Builder",   "#00d4ff"),
    ("Circuit Design, Day by Day",       "#ff2d55"),
    ("C  \u2022  Python  \u2022  Arduino  \u2022  ESP32", "#b026ff"),
    ("B.Tech EE \u00b7 2nd Year \u00b7 Jaipur", "#ff9500"),
]
STEPS    = 24                   # keystroke steps per tagline
TYPE_T   = 1.6                  # seconds of typing
SLOT     = 3.0                  # seconds per tagline
CYCLE    = SLOT*len(PHRASES)    # 15s
X0       = 40 + len(PROMPT)*CW  # text start x (313.6)
Y_BASE, BOX_W, BOX_H = 58, 900, 92

def fmt(v): return str(round(v, 6))

masks, texts, kt_all, xv_all = [], [], [], []
for i, (txt, col) in enumerate(PHRASES):
    L = len(txt)*CW
    t0 = i*SLOT
    kt, vals, xs = [0.0], [0], [X0]                       # idle at start of cycle
    kt.append(fmt(t0/1e0/CYCLE)*1); vals.append(0); xs.append(X0)   # park at 0 until this slot
    kt = [0.0]; vals = [0]; xs = [X0]
    kt.append(round(t0/CYCLE, 6)); vals.append(0); xs.append(X0)
    for j in range(1, STEPS+1):
        kt.append(round((t0 + j*TYPE_T/STEPS)/CYCLE, 6))
        vals.append(round(L*j/STEPS, 2)); xs.append(round(X0 + L*j/STEPS, 2))
    end = t0 + SLOT
    kt.append(round((end - 0.02)/CYCLE, 6)); vals.append(L);  xs.append(round(X0+L, 2))
    kt.append(round(end/CYCLE, 6));          vals.append(0);  xs.append(X0)
    if end >= CYCLE - 0.001:                                   # close the loop cleanly
        kt[-1] = 1.0; vals[-1] = 0; xs[-1] = X0
    else:
        kt.append(1.0); vals.append(0); xs.append(X0)
    masks.append(f'''    <clipPath id="tMask{i}"><rect x="{X0-6}" y="24" height="44" width="0">
      <animate attributeName="width" calcMode="discrete" values="{";".join(str(v) for v in vals)}" keyTimes="{";".join(str(k) for k in kt)}" dur="{CYCLE}s" repeatCount="indefinite"/>
    </rect></clipPath>''')
    texts.append(f'''    <g clip-path="url(#tMask{i})">
      <text x="{X0}" y="{Y_BASE}" fill="{col}">{txt.replace('&','&amp;')}</text>
    </g>''')
    kt_all += kt; xv_all += xs

# one shared cursor that tracks whichever tagline is typing
cursor_kt = ";".join(str(k) for k in kt_all)
cursor_xv = ";".join(str(v) for v in xv_all)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{BOX_W}" height="{BOX_H}" viewBox="0 0 {BOX_W} {BOX_H}" role="img" aria-label="Typing animation: robotics, IoT, circuits, C and Python">
  <defs>
    <linearGradient id="tEdge" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff2d55"><animate attributeName="stop-color" values="#ff2d55;#00ff9d;#00d4ff;#b026ff;#ff2d55" dur="7s" repeatCount="indefinite"/></stop>
      <stop offset="50%" stop-color="#00d4ff"><animate attributeName="stop-color" values="#00d4ff;#ff2d55;#00ff9d;#b026ff;#00d4ff" dur="7s" repeatCount="indefinite"/></stop>
      <stop offset="100%" stop-color="#00ff9d"><animate attributeName="stop-color" values="#00ff9d;#00d4ff;#ff2d55;#b026ff;#00ff9d" dur="7s" repeatCount="indefinite"/></stop>
    </linearGradient>
    <filter id="tGlow" x="-30%" y="-60%" width="160%" height="260%">
      <feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
{chr(10).join(masks)}
    <style>
      #tCursor {{ animation: tBlink 1s steps(1,end) infinite; }}
      @keyframes tBlink {{ 0%,49% {{opacity:1}} 50%,100% {{opacity:0}} }}
      #tLeds circle {{ animation: tLed 1.6s ease-in-out infinite; }}
      @keyframes tLed {{ 0%,100% {{opacity:.25}} 50% {{opacity:1}} }}
    </style>
  </defs>

  <rect x="1.5" y="1.5" width="{BOX_W-3}" height="{BOX_H-3}" rx="16" fill="#05060f"/>
  <rect id="tEdgeLine" x="1.5" y="1.5" width="{BOX_W-3}" height="{BOX_H-3}" rx="16" fill="none" stroke="url(#tEdge)" stroke-width="1.8"/>

  <g id="tLeds">
    <circle cx="30" cy="24" r="5" fill="#ff2d55"/><circle cx="50" cy="24" r="5" fill="#ff9500"/><circle cx="70" cy="24" r="5" fill="#00ff9d"/>
  </g>
  <text x="{BOX_W-18}" y="28" text-anchor="end" font-family="Consolas,ui-monospace,monospace" font-size="11" letter-spacing="1.5" fill="#6d7ca8">README.sh \u2014 autoplay</text>
  <line x1="18" y1="38" x2="{BOX_W-18}" y2="38" stroke="#1b2340" stroke-width="1"/>

  <text x="40" y="{Y_BASE}" font-family="'Fira Code',Consolas,ui-monospace,monospace" font-size="{FS}" filter="url(#tGlow)" fill="#5ce1a0">{PROMPT}</text>

  <g id="tTyped" font-family="'Fira Code',Consolas,ui-monospace,monospace" font-size="{FS}" font-weight="600">
{chr(10).join(texts)}
  </g>

  <rect id="tCursor" x="{X0}" y="40" width="12" height="24" rx="2" fill="#00ff9d">
    <animate attributeName="x" calcMode="discrete" values="{cursor_xv}" keyTimes="{cursor_kt}" dur="{CYCLE}s" repeatCount="indefinite"/>
  </rect>

  <g font-family="Consolas,ui-monospace,monospace" font-size="11" fill="#6d7ca8">
    <text x="40" y="84">\u25cf online</text>
    <text x="140" y="84">\u25e6 building circuits at 3 AM</text>
    <text x="{BOX_W-40}" y="84" text-anchor="end">Rajasthan, IN</text>
  </g>
</svg>
'''
open("assets/typing.svg","w").write(svg)
print("typing.svg rebuilt:", len(svg), "bytes;", len(PHRASES), "masks;", len(kt_all), "cursor keyframes")
