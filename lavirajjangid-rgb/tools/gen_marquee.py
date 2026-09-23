# Generates assets/marquee.svg — infinitely scrolling keyword tape.
# Interaction is AUTOMATIC (CSS slide loop + staggered per-item pulses + a shine sweep),
# because :hover never fires inside an <img>-embedded SVG on GitHub.
ITEMS = ["⚡ OHM'S LAW", "▸ KIRCHHOFF", "▸ PCB", "▸ ARDUINO", "▸ ESP32", "▸ MQTT", "▸ SENSORS", "▸ SERVO"]
W, H, FS = 1000, 52, 15
X = [20, 173, 317, 407, 533, 641, 740, 866]     # spaced with clearance, group width = 1000

def row(offset):
    out = []
    for i, (x, t) in enumerate(zip(X, ITEMS)):
        out.append(f'        <text x="{x}" y="33" class="kItem">{t}'
                   f'<animate attributeName="fill-opacity" values="0.72;1;0.72" dur="4.4s" begin="{(i*0.5)%4.4:.2f}s" repeatCount="indefinite"/>'
                   f'</text>')
    pad = "      "
    body = "\n".join(out)
    if offset:
        return f'      <g transform="translate({offset},0)">\n{body}\n      </g>'
    return f'      <g>\n{body}\n      </g>'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="scrolling tech keywords">
  <defs>
    <linearGradient id="kGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff2d55"><animate attributeName="stop-color" values="#ff2d55;#00ff9d;#00d4ff;#b026ff;#ff9500;#ff2d55" dur="8s" repeatCount="indefinite"/></stop>
      <stop offset="100%" stop-color="#00d4ff"><animate attributeName="stop-color" values="#00d4ff;#b026ff;#ff2d55;#00ff9d;#ff9500;#00d4ff" dur="8s" repeatCount="indefinite"/></stop>
    </linearGradient>
    <linearGradient id="kShine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="kFade" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#05060f" stop-opacity="1"/>
      <stop offset="10%" stop-color="#05060f" stop-opacity="0"/>
      <stop offset="90%" stop-color="#05060f" stop-opacity="0"/>
      <stop offset="100%" stop-color="#05060f" stop-opacity="1"/>
    </linearGradient>
    <filter id="kGlow" x="-20%" y="-100%" width="140%" height="300%">
      <feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="kClip"><rect width="{W}" height="{H}" rx="14"/></clipPath>
    <style>
      .kTrack {{ animation: kSlide 26s linear infinite; }}
      @keyframes kSlide {{ from {{ transform: translateX(0) }} to {{ transform: translateX(-1000px) }} }}
    </style>
  </defs>

  <rect width="{W}" height="{H}" rx="14" fill="#05060f" stroke="url(#kGrad)" stroke-width="1.6"/>
  <g clip-path="url(#kClip)">
    <!-- shine sweep that keeps travelling across the tape -->
    <rect x="-260" y="0" width="260" height="{H}" fill="url(#kShine)">
      <animate attributeName="x" values="-260;1260" dur="5.5s" repeatCount="indefinite"/>
    </rect>
    <g class="kTrack" font-family="'Fira Code',Consolas,ui-monospace,monospace" font-size="{FS}" fill="url(#kGrad)" filter="url(#kGlow)">
{row(0)}
{row(1000)}
{row(2000)}
    </g>
  </g>
  <rect width="{W}" height="{H}" rx="14" fill="url(#kFade)" pointer-events="none"/>
</svg>
'''
open("assets/marquee.svg","w").write(svg)
print("marquee.svg rebuilt:", len(svg), "bytes")
