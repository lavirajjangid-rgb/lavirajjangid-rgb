# Builds preview.html: the README look, offline. SVGs are inlined so animations
# and :hover interactions work without any network access.
import re, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
a = root / "assets"

EXTRA = {"snake-dark.svg": root / "profile-snake" / "github-snake-dark.svg",
         "3d-night-rainbow.svg": root / "profile-3d-contrib" / "profile-night-rainbow.svg"}

def svg(name, extra=""):
    s = (EXTRA[name] if name in EXTRA else a / name).read_text()
    s = s.replace("<svg ", f'<svg style="width:100%;height:auto;display:block" {extra} ', 1)
    return s

mono  = svg("monogram.svg").replace('style="width:100%;height:auto;display:block"', 'style="width:240px;height:auto;display:block;margin:auto"')

BADGES = lambda t,c: f'<span class="badge" style="--c:{c}">{t}</span>'
langs = [(BADGES("C","#00599C"),), (BADGES("Python","#00d4ff"),)]

stack = "".join(BADGES(t, c) for t, c in [
    ("C","#00599C"),("Python","#00d4ff"),("Embedded C","#00ff9d"),("MATLAB","#ff9500"),
    ("Arduino","#00979D"),("ESP32 / ESP8266","#ff2d55"),("Raspberry Pi","#00d4ff"),("KiCad","#c9d6f5"),
    ("Tinkercad","#00ff9d"),("MQTT","#b026ff"),("Firebase","#ff9500"),("Git","#F05032"),
    ("GitHub","#c9d6f5"),("Linux","#ff9500"),("VS Code","#007ACC"),("Markdown","#00d4ff"),
    ("Social Media","#b026ff")])

html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Laviraj Jangid — RGB Profile README · live preview</title>
<style>
  :root {{ --red:#ff2d55; --grn:#00ff9d; --blu:#00d4ff; --pur:#b026ff; --ink:#c9d6f5; }}
  * {{ box-sizing:border-box }}
  body {{ margin:0; padding:0 0 60px; background:#02030a; color:var(--ink);
         font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
  .wrap {{ max-width:1010px; margin:0 auto; padding:18px 20px 0; }}
  .note {{ border:1px solid #2a3358; background:#0a0e20; border-radius:14px; padding:12px 16px;
           font-size:13px; color:#8ea0c9; margin-bottom:18px; }}
  .note b {{ color:#e6efff }}
  h2 {{ font-size:24px; margin:44px 0 6px; color:#fff; letter-spacing:.4px; }}
  h2 span {{ background:linear-gradient(90deg,var(--red),#ff9500,var(--grn),var(--blu),var(--pur));
             -webkit-background-clip:text; background-clip:text; color:transparent; }}
  .rule {{ height:2px; background:linear-gradient(90deg,var(--red),var(--grn),var(--blu),var(--pur));
           border-radius:2px; opacity:.85; margin:6px 0 18px; }}
  p, li {{ line-height:1.65; font-size:15px }}
  .dim {{ color:#8ea0c9; font-size:13.5px }}
  a {{ color:var(--blu) }}
  pre {{ background:#080b18; border:1px solid #1b2340; border-radius:12px; padding:14px 16px; overflow:auto;
         font-family:ui-monospace,Consolas,monospace; font-size:12.5px; color:#d7e3ff }}
  code {{ font-family:ui-monospace,Consolas,monospace }}
  .card {{ background:#080b18; border:1px solid #1b2340; border-radius:16px; padding:16px }}
  .grid {{ display:grid; grid-template-columns:34% 66%; gap:18px; align-items:center }}
  table {{ width:100%; border-collapse:collapse; font-size:14px }}
  th,td {{ border:1px solid #1b2340; padding:9px 11px; text-align:left; vertical-align:top }}
  th {{ background:#0c1226; color:#e6efff; font-weight:600 }}
  .badge {{ display:inline-block; margin:3px; padding:5px 11px; border-radius:7px; background:#0a0a18;
            border:1px solid var(--c); color:var(--c); font-family:ui-monospace,Consolas,monospace;
            font-size:11.5px; letter-spacing:.4px }}
  details {{ margin:12px 0; background:#080b18; border:1px solid #1b2340; border-radius:12px; padding:12px 16px }}
  summary {{ cursor:pointer; color:#e6efff; font-size:15px }}
  .ph {{ display:flex; gap:14px; flex-wrap:wrap; justify-content:center }}
  .ph div {{ flex:1 1 300px; min-height:120px; border:1px dashed #33406e; border-radius:14px; display:grid;
             place-items:center; color:#5f6f9c; font-size:12.5px; text-align:center; padding:14px }}
  .chips {{ display:flex; gap:10px; flex-wrap:wrap; justify-content:center; margin-top:8px }}
  .chips a {{ text-decoration:none; padding:6px 13px; border:1px solid #ff2d55; border-radius:20px;
              color:#e6efff; font-size:13px; font-family:ui-monospace,Consolas,monospace }}
  .chips a:nth-child(2) {{ border-color:#00ff9d }} .chips a:nth-child(3) {{ border-color:#00d4ff }}
  .chips a:nth-child(4) {{ border-color:#b026ff }} .chips a:nth-child(5) {{ border-color:#ff9500 }}
  .center {{ text-align:center }}
</style></head><body>
<div class="wrap">

  <div class="note">
    <b>Offline preview — this is exactly what the README looks like.</b>
    Every animation runs on a timer (no hover needed, because <b>:hover does not fire inside images on GitHub</b>).
    The five live stat cards are fetched from the internet, so they only appear once the files are on GitHub — the
    dashed boxes mark where they land. The snake and 3D city below are the animated placeholders that ship with the repo.
  </div>

  {svg("banner.svg")}
  <div style="height:12px"></div>
  {svg("typing.svg")}
  <div style="height:12px"></div>
  {svg("marquee.svg")}

  <div class="chips">
    <a href="#about">⚡ About</a><a href="#circuit">🔌 Circuit</a><a href="#stack">🧰 Stack</a>
    <a href="#stats">📊 Stats</a><a href="#vault">🎓 Beginner Vault</a>
  </div>
  <div style="height:16px"></div>
  {svg("divider.svg")}

  <h2 id="about">About Me <span>⚡</span></h2><div class="rule"></div>
  <div class="grid">
    <div>{mono}</div>
    <div>
      <pre>class Laviraj:
    name      = "Laviraj Jangid"
    role      = "B.Tech Electrical Engineering · 2nd year"
    location  = "Jaipur, Rajasthan, India"
    languages = ["C", "Python", "a little Embedded C"]
    learning  = ["Circuit design", "Robotics", "Automation"]
    experience= ["IoT projects", "Social media management"]
    mindset   = "simulate first, solder second, document always"</pre>
      <p>I'm an EE student who likes the moment when a schematic finally blinks on a breadboard.
      Career path is set around <b>circuits + electronics</b>, with <b>robotics &amp; automation</b>
      as the direction and <b>IoT</b> as the area I already have hands-on experience in.</p>
    </div>
  </div>

  <div style="height:18px"></div>
  {svg("skills.svg")}

  <h2 id="circuit">Inside My Breadboard <span>🔌</span></h2><div class="rule"></div>
  <p class="dim">Watch the signal travel — each block lights up in turn, and the dashes carry live current.</p>
  {svg("circuit.svg")}

  <h2 id="stack">Tech Stack <span>🧰</span></h2><div class="rule"></div>
  <div class="center">{stack}</div>

  <h2 id="stats">GitHub Stats <span>📊</span></h2><div class="rule"></div>
  <div class="ph">
    <div>github-readme-stats<br/>stats card<br/><span style="color:#7f8fbb">(loads on GitHub)</span></div>
    <div>top languages<br/>card<br/><span style="color:#7f8fbb">(loads on GitHub)</span></div>
    <div>streak card<br/><span style="color:#7f8fbb">(loads on GitHub)</span></div>
    <div>trophy case<br/><span style="color:#7f8fbb">(loads on GitHub)</span></div>
    <div>contribution activity graph<br/><span style="color:#7f8fbb">(loads on GitHub)</span></div>
  </div>
  <div style="height:14px"></div>
  {svg("snake-dark.svg")}
  <div style="height:14px"></div>
  {svg("3d-night-rainbow.svg")}

  <h2 id="vault">Beginner Vault <span>🎓</span></h2><div class="rule"></div>
  <table>
    <tr><th>#</th><th>Basic skill</th><th>Time</th><th>Free place to learn</th><th>Proof-of-work project</th></tr>
    <tr><td>1</td><td>Git &amp; GitHub</td><td>1 evening</td><td>github.com/skills</td><td>Repo + README + 3 commits</td></tr>
    <tr><td>2</td><td>Markdown + badges</td><td>1 hour</td><td>GitHub Docs</td><td>A profile README like this</td></tr>
    <tr><td>3</td><td>Simulate before you solder</td><td>1 weekend</td><td>Tinkercad · Wokwi · Falstad</td><td>Blink + sensor in simulation</td></tr>
    <tr><td>4</td><td>Electronics basics</td><td>1 week</td><td>All About Circuits (DC vol.)</td><td>Voltage divider, measured &amp; proven</td></tr>
    <tr><td>5</td><td>Python ↔ hardware bridge</td><td>1 weekend</td><td>pyserial + matplotlib docs</td><td>Live sensor plot on your laptop</td></tr>
  </table>
  <details open><summary><b>💡 6th skill: document your own project</b></summary>
    <p class="dim">What / Why / Parts / How to run / What broke / Next — a 5-line README beats a perfect circuit photo.</p>
  </details>
  <details><summary><b>🗓️ My 30-day starter plan</b> (tick boxes work on GitHub)</summary>
    <p class="dim">Week 1 tools · Week 2 sensing · Week 3 IoT · Week 4 motion — full checklist lives in the README.</p>
  </details>
  <details><summary><b>🧩 Steal my snippets</b> — typing SVG, badge, stats, details, doodle-a-schematic</summary>
    <p class="dim">Copy-paste blocks for every animation in this page are in the README's collapsible section.</p>
  </details>

  <h2>Connect <span>📬</span></h2><div class="rule"></div>
  <div class="center">
    <div class="chips">
      <a href="mailto:lavirajjangid@gmail.com">Email</a><a href="#">LinkedIn</a>
      <a href="#">Instagram</a><a href="https://github.com/lavirajjangid-rgb">GitHub</a>
    </div>
  </div>

  <div style="height:22px"></div>
  {svg("footer.svg")}
  <p class="center dim">Readme crafted with circuits, caffeine and zero JavaScript.</p>
</div>
</body></html>
"""
out = root / "preview.html"
out.write_text(html)
print("preview.html:", len(html), "bytes")
