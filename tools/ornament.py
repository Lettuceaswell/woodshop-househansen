"""Draw the woodshop ornaments as ink SVG (House Hansen thin strand, Urnes manner, wood subject).

    python3 tools/ornament.py      -> assets/divider.svg, assets/liveedge.svg

divider: plain-sawn grain lines that part around a knot; one strand rides through them in an
Urnes figure-eight (over/under by background knock-out bands) and ends in tendril curls.
liveedge: a bark contour for the top and bottom of the Forge band, filled with the band colour.
"""
import math, random
from pathlib import Path

root = Path(__file__).resolve().parent.parent
R = random.Random(7)
f = lambda v: f"{v:.1f}"

def smooth(pts):
    """Catmull-Rom through points -> cubic path data."""
    d = f"M{f(pts[0][0])} {f(pts[0][1])}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d

# ---------- divider ----------
W, H, CX, CY = 1200, 80, 600, 40
KRX, KRY = 24, 14  # the knot
paths = []  # (d, width, opacity, delay)

def grain(i, side, half, span):
    """Grain line i (0 = nearest the pith) parts around the knot, then settles flat."""
    base = CY + side * (3.5 + 5.5 * i)
    peak = CY + side * (KRY + 4 + 5.5 * i)
    pts = []
    for k in range(19):
        x = CX + half * span * (k / 18) ** 1.15
        g = math.exp(-((x - CX) / (70 + 14 * i)) ** 2)
        wob = 0.9 * math.sin(x / 57 + i * 1.7) * (1 - g)
        pts.append((x, base + (peak - base) * g + wob))
    return pts

for i, span in enumerate([560, 470, 380, 290]):
    for side in (-1, 1):
        for half in (-1, 1):
            paths.append((smooth(grain(i, side, half, span)), 1.5 - 0.2 * i, 0.95 - 0.15 * i, 0.12 + 0.07 * i))

# The knot: off-round rings, tilted a touch, with a checked eye.
for i, sc in enumerate([1, 0.72, 0.46, 0.2]):
    pts = []
    for t in range(19):
        a = t / 18 * 2 * math.pi + 0.4 * i
        wob = 1 + 0.07 * math.sin(3 * a + i * 2)
        x, y = KRX * sc * wob * math.cos(a), KRY * sc * wob * math.sin(a)
        r = -0.12
        pts.append((CX + x * math.cos(r) - y * math.sin(r), CY + x * math.sin(r) + y * math.cos(r)))
    paths.append((smooth(pts), 1.6 if i == 0 else 1.15, 0.95, 0.03 * i))
paths.append((f"M{CX - 3} {CY - 1}L{CX + 4} {CY + 1.5}", 1.1, 0.9, 0.1))

# The strand: rides in from the left, wraps the knot one and a half turns (widening, so it never
# lies on itself), and leaves to the right. Both ends curl into Urnes tendrils.
def tendril(ax, ay, dirn):
    out = []
    for i in range(1, 19):
        a = i / 18 * 1.8 * math.pi
        r = 9 * (1 - i / 22)
        out.append((ax + dirn * r * math.sin(a), ay - r * (1 - math.cos(a))))
    return out

orbit = []
for i in range(41):
    u = i / 40
    a = math.pi - u * 3 * math.pi          # clockwise from the left, over the top
    rx, ry = 44 + 22 * u, 21 + 9 * u
    orbit.append((CX + rx * math.cos(a), CY - ry * math.sin(a)))
lx, rx_ = orbit[0][0], orbit[-1][0]
left = [(lx - k * 12, CY + 6 * math.sin(k / 3.2) * (k / 26)) for k in range(26, 0, -1)]
right = [(rx_ + k * 12, CY - 6 * math.sin(k / 3.2) * (k / 24)) for k in range(1, 25)]
strand = list(reversed(tendril(*left[0], -1))) + left + orbit + right + tendril(*right[-1], 1)
d_strand = smooth(strand)

body = [f'<path pathLength="1" d="{d}" stroke-width="{w:.2f}" opacity="{o:.2f}" style="--d:{dl:.2f}s"/>' for d, w, o, dl in paths]
# Over-strand: a knock-out band in the ground colour, then the ink, the way the mark resolves crossings.
body.append(f'<path class="ko" pathLength="1" d="{d_strand}" stroke-width="6" style="--d:.4s"/>')
body.append(f'<path class="st" pathLength="1" d="{d_strand}" stroke-width="2" style="--d:.4s"/>')

divider = (f'<svg class="knot-rule" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" aria-hidden="true" '
           f'fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">' + "".join(body) + "</svg>")
(root / "assets/divider.svg").write_text(divider)

# ---------- live edge ----------
# One bark contour, 1600 wide. Long slow swells (the log's taper), bark plates, a few deep fissures.
LW, LH = 1600, 48
pts = []
x = 0
while x <= LW:
    y = 24 + 9 * math.sin(x / 260) + 5 * math.sin(x / 97 + 1) + R.uniform(-2.2, 2.2)
    if R.random() < 0.07:
        y += R.uniform(6, 11)  # fissure
    pts.append((x, y))
    x += R.uniform(14, 30)
pts[-1] = (LW, pts[-1][1])
edge = smooth(pts)
inner = smooth([(px, py + 7 + 1.5 * math.sin(px / 41)) for px, py in pts])
liveedge = (f'<svg class="live-edge" viewBox="0 0 {LW} {LH}" preserveAspectRatio="none" aria-hidden="true">'
            f'<path class="fill" d="{edge}L{LW} {LH}L0 {LH}Z"/>'
            f'<path class="cambium" pathLength="1" d="{inner}" fill="none" vector-effect="non-scaling-stroke"/></svg>')
(root / "assets/liveedge.svg").write_text(liveedge)
print("divider", len(divider), "liveedge", len(liveedge))
