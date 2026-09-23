# Final QA: proves every SVG animates inside an <img> (the GitHub context),
# that nothing depends on :hover, and that the README only uses tags GitHub allows.
import glob, os, re, sys
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
FILES = sorted(glob.glob("assets/*.svg")) + ["profile-snake/github-snake-dark.svg",
          "profile-snake/github-snake.svg", "profile-3d-contrib/profile-night-rainbow.svg"]
fails = []

print("── 1. XML well-formedness ──────────────────────────────")
import xml.dom.minidom
for f in FILES:
    try: xml.dom.minidom.parse(f)
    except Exception as e: fails.append(f"{f}: {e}")

print("── 2. self-contained (no scripts, no external refs) ────")
for f in FILES:
    s = open(f).read()
    if "<script" in s: fails.append(f"{f}: contains <script>")
    for u in re.findall(r'(?:src|href)\s*=\s*"(?!data:|#)([^"]+)"', s): fails.append(f"{f}: external ref {u}")
print("   ok" if not fails else "   ISSUES: " + str(fails))

print("── 3. no :hover dependency (dead on GitHub) ────────────")
for f in FILES:
    if ":hover" in open(f).read(): fails.append(f"{f}: still uses :hover")
print("   ok - 0 hover rules" if ":hover" not in "".join(open(f).read() for f in FILES) else "   ISSUES")

print("── 4. every SVG animates inside an <img> ───────────────")
os.makedirs("/tmp/vq", exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1020, "height":520})
    errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    for f in FILES:
        abs_ = os.path.abspath(f)
        open("/tmp/vq/p.html","w").write(
            f'<html><body style="margin:0;background:#02030a">'
            f'<img src="file://{abs_}" width="1000"></body></html>')
        pg.goto("file:///tmp/vq/p.html"); pg.wait_for_timeout(900)
        pg.screenshot(path="/tmp/vq/a.png"); pg.wait_for_timeout(1400)
        pg.screenshot(path="/tmp/vq/b.png")
        A, B = Image.open("/tmp/vq/a.png").convert("L"), Image.open("/tmp/vq/b.png").convert("L")
        diff = sum(1 for i in range(0, A.width, 3) for j in range(0, A.height, 3)
                   if abs(A.getpixel((i,j)) - B.getpixel((i,j))) > 12)
        status = "OK " if diff > 60 else "STATIC"
        if diff <= 60: fails.append(f"{f}: no animation detected (diff={diff})")
        print(f"   {status} {f:52} changed pixels≈{diff*9}")
    if errs: fails.append("console errors: " + str(errs[:3]))
    print("   console errors:", errs or "none")
    b.close()

print("── 5. circuit auto-cycle shows + hides details ─────────")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1000,"height":440})
    pg.goto("file://" + os.path.abspath("assets/circuit.svg"))   # standalone: SMIL runs
    def band(path): 
        im = Image.open(path).convert("L")
        return sum(im.getpixel((x,y)) for x in range(70,180) for y in range(272,292))
    pg.wait_for_timeout(1200); pg.screenshot(path="/tmp/vq/c1.png"); v1 = band("/tmp/vq/c1.png")
    pg.wait_for_timeout(10000); pg.screenshot(path="/tmp/vq/c2.png"); v2 = band("/tmp/vq/c2.png")
    print(f"   sensors detail brightness: t≈1s {v1}  vs  t≈11s {v2}")
    if v1 <= v2: fails.append("circuit: detail text did not appear/disappear on schedule")
    b.close()

print("── 6. README tags vs GitHub's sanitiser allow-list ─────")
ALLOWED = set("""h1 h2 h3 h4 h5 h6 h7 h8 br b i strong em a pre code img tt div ins del sup sub p
ol ul table thead tbody tfoot blockquote dl dt dd kbd q samp var hr ruby rt rp li tr td th s strike
summary details""".split())
md = open("README.md").read()
tags = set(t.lower() for t in re.findall(r'<\s*/?\s*([a-zA-Z][a-zA-Z0-9]*)', md))
# tags inside fenced code blocks / inline code are shown as text, not parsed
stripped = re.sub(r'<!--.*?-->', '', md, flags=re.S)   # comments never render
stripped = re.sub(r'```.*?```', '', stripped, flags=re.S)
stripped = re.sub(r'`[^`]*`', '', stripped)
tags = set(t.lower() for t in re.findall(r'<\s*/?\s*([a-zA-Z][a-zA-Z0-9]*)', stripped))
bad = sorted(tags - ALLOWED)
print("   tags used:", " ".join(sorted(tags)))
print("   disallowed:", bad or "none")
if bad: fails.append(f"README uses tags GitHub strips: {bad}")

print("── 7. local image paths exist ─────────────────────────")
for src in re.findall(r'src="(?!http)([^"#]+)', md):
    if not os.path.exists(src): fails.append(f"missing image: {src}")
print("   ok" if not any('missing image' in f for f in fails) else "   ISSUES")

print("\n" + ("✅ ALL CHECKS PASSED — no glitches found." if not fails else "❌ PROBLEMS:\n - " + "\n - ".join(fails)))
sys.exit(1 if fails else 0)
