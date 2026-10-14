"""Generates every project figure as an .svg under projects/<slug>/img/.

Run: python3 scripts/build_figures.py
Figures are schematic unless a caption says otherwise; all numbers shown are
taken from the project results and are not simulated.
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from figlib import (DARK, DOWN, FLAT, INK, MUTED, UP, arrow, box, caption,  # noqa: E402
                    chain, esc, label, svg)

ROOT = pathlib.Path(__file__).resolve().parent.parent
W = 760
FIGS = {}


def fig(slug, name, title, desc, w, h, body):
    FIGS.setdefault(slug, []).append((name, svg(w, h, body, title, desc)))


def hbar(x, y, w, h, frac, value, name, color=UP, note=None):
    """One horizontal bar with its label above and value at the end."""
    bw = max(2.0, w * frac)
    out = [f'<text class="s" x="{x}" y="{y - 8}">{esc(name)}</text>']
    if note:
        out.append(f'<text class="xs" x="{x + w + 56}" y="{y - 8}" text-anchor="end">{esc(note)}</text>')
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="#ece7f8"/>')
    out.append(f'<rect x="{x}" y="{y}" width="{bw:.1f}" height="{h}" rx="{h/2}" fill="{color}"/>')
    out.append(f'<text class="num" x="{x + bw + 10:.1f}" y="{y + h/2}" dominant-baseline="middle">{esc(value)}</text>')
    return "\n".join(out)


def axis_x(x0, x1, y, ticks, fmt=str):
    out = [f'<line class="ax" x1="{x0}" y1="{y}" x2="{x1}" y2="{y}"/>']
    for t, frac in ticks:
        tx = x0 + (x1 - x0) * frac
        out.append(f'<line class="ax" x1="{tx}" y1="{y}" x2="{tx}" y2="{y + 5}"/>')
        out.append(f'<text class="xs" x="{tx}" y="{y + 18}" text-anchor="middle">{esc(fmt(t))}</text>')
    return "\n".join(out)


# ---------------------------------------------------------------- project 01
fig("neutrophil_transfer", "f1_workflow",
    "Transfer workflow used in the May to June experiments",
    "Five steps: donor cells, mitochondrial isolation, fluorescent labelling, co-incubation with granulocytes, readout.",
    W, 196,
    chain([("Donor cells", "cultured"), ("Isolate mitochondria", "differential centrifugation"),
           ("Label", "fluorescent activity dye"), ("Co-incubate", "with granulocytes"),
           ("Read out", "fluorescence over time")], 12, 26, 128, 86, 25, width=15)
    + f'\n<path class="dash" d="M 140,150 L 140,168 L 652,168 L 652,150"/>'
    + label(396, 182, "uptake low at step 4, signal gone by about 20 min at step 5", "xs", width=100))

_t = [0, 5, 10, 15, 20, 25, 30, 35, 40]
_pts = [(70 + 650 * (t / 40), 48 + 142 * (1 - math.exp(-t / 7.5))) for t in _t]
_path = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in _pts)
fig("neutrophil_transfer", "f2_activity",
    "Loss of mitochondrial activity signal after transfer",
    "Schematic decay curve: the fluorescent activity signal falls to the detection floor by roughly 20 minutes.",
    W, 250,
    f'<rect x="70" y="170" width="650" height="20" fill="#ece7f8"/>'
    f'<text class="xs" x="716" y="182" text-anchor="end">detection floor</text>'
    + "".join(f'<line class="gl" x1="70" y1="{48 + 142 * f:.0f}" x2="720" y2="{48 + 142 * f:.0f}"/>'
              for f in (0, .25, .5, .75, 1))
    + f'<path d="{_path}" fill="none" stroke="{INK}" stroke-width="2.8" stroke-linecap="round"/>'
    + "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{INK}"/>' for x, y in _pts)
    + f'<line class="dash" x1="{70 + 650 * 0.5}" y1="40" x2="{70 + 650 * 0.5}" y2="190"/>'
    + f'<text class="xs" x="{70 + 650 * 0.5 + 8}" y="54">activity no longer detectable</text>'
    + axis_x(70, 720, 190, [(t, t / 40) for t in _t])
    + f'<text class="xs" x="396" y="226" text-anchor="middle">minutes after transfer</text>'
    + f'<text class="xs" x="24" y="119" text-anchor="middle" transform="rotate(-90,24,119)">activity signal</text>'
    + '<text class="xs" x="70" y="24">Schematic. Shape of the observed decay, not measured values.</text>')

fig("neutrophil_transfer", "f3_routes",
    "Two routes for delivering mitochondria",
    "The isolated route used in this project compared with the in-blood route used by the PORTER team.",
    W, 300,
    f'<text class="t" x="12" y="24">A &#160; Isolated mitochondria (this project)</text>'
    + chain([("Whole blood", None), ("Isolate", "mitochondria removed from cells"),
             ("Add to granulocytes", None), ("Low uptake", "activity lost")], 12, 38, 170, 76, 20, width=17)
    + f'<text class="t" x="12" y="176">B &#160; Mitochondria kept in blood (PORTER)</text>'
    + chain([("Whole blood", None), ("Stabilise in place", "no isolation step"),
             ("Transfer in blood", "PORTER machine"), ("Uptake retained", "activity preserved")],
            12, 190, 170, 76, 20, width=17)
    + f'<text class="xs" x="12" y="290">Difference: route B never exposes mitochondria to an isolation buffer.</text>')

# ---------------------------------------------------------------- project 02
fig("microgravity_blood", "f1_design",
    "Planned two by two design",
    "Blood is either held in simulated microgravity or static, then either receives mitochondria or does not.",
    W, 300,
    f'<text class="xs" x="250" y="30" text-anchor="middle">no transfer</text>'
    f'<text class="xs" x="500" y="30" text-anchor="middle">mitochondrial transfer</text>'
    f'<text class="s" x="118" y="90" text-anchor="end">static</text>'
    f'<text class="s" x="118" y="200" text-anchor="end">clinostat</text>'
    + box(130, 44, 240, 92, "Baseline", "boxw", sub="reference state")
    + box(382, 44, 240, 92, "Transfer only", "box", sub="uptake in normal gravity")
    + box(130, 154, 240, 92, "Microgravity only", "boxw", sub="effect of exposure alone")
    + box(382, 154, 240, 92, "Microgravity + transfer", "box", sub="the condition of interest")
    + f'<text class="xs" x="12" y="282">Each arm is read out for uptake and for how long activity persists.</text>')

fig("microgravity_blood", "f2_protocol",
    "Planned protocol order",
    "Draw blood, expose to simulated microgravity, perform the transfer, then read out.",
    W, 170,
    chain([("Draw blood", None), ("Clinostat exposure", "fixed duration"),
           ("Transfer", "in blood, as in route B"), ("Read out", "uptake and persistence")],
          12, 28, 170, 86, 20, width=17)
    + f'<text class="xs" x="12" y="150">Blocked on access to a calibrated clinostat; a self-built unit would not be reproducible.</text>')

# ---------------------------------------------------------------- project 03
fig("secondary_transfer", "f1_concept",
    "Direct transfer compared with carrier mediated transfer",
    "Instead of adding isolated mitochondria to a target cell, a carrier cell takes them up and delivers them.",
    W, 290,
    f'<text class="t" x="12" y="24">A &#160; Direct</text>'
    + box(90, 36, 150, 68, "Isolated mitochondria", "boxw", width=18)
    + arrow(250, 70, 320, 70)
    + box(330, 36, 150, 68, "Target cell", "box")
    + f'<text class="xs" x="500" y="74">fragile in transit, uptake limited</text>'
    + f'<text class="t" x="12" y="152">B &#160; Carrier mediated</text>'
    + box(64, 164, 150, 68, "Donor cell", "boxw")
    + arrow(224, 198, 284, 198)
    + box(294, 164, 170, 68, "Carrier cell", "box", sub="takes up and holds")
    + arrow(474, 198, 534, 198)
    + box(544, 164, 150, 68, "Recipient cell", "boxw")
    + f'<text class="xs" x="12" y="268">The analysis asks which immune populations are best suited to the middle role.</text>')

fig("secondary_transfer", "f2_pipeline",
    "Single cell analysis pipeline",
    "Five stages from raw single cell data to ranked candidate carrier populations.",
    W, 170,
    chain([("Single cell datasets", None), ("Normalise", "and check batch structure"),
           ("Pseudobulk", "per cell type"), ("Score cell states", "uptake and donation programs"),
           ("Rank candidates", None)], 14, 26, 130, 86, 18, width=14)
    + f'<text class="xs" x="12" y="150">Rebuilt three times; each pass tightened normalisation and the scoring definition.</text>')

fig("secondary_transfer", "f3_scores",
    "Composite carrier score for the two leading populations",
    "Myeloid progenitor scores 8.43 and haematopoietic stem cells and progenitors score 5.49.",
    W, 210,
    hbar(170, 44, 430, 26, 8.43 / 10, "8.43", "Myeloid progenitor", UP, note="1 organ")
    + hbar(170, 116, 430, 26, 5.49 / 10, "5.49", "HSC / progenitors", DOWN, note="8 organs, 2,825 cells")
    + axis_x(170, 600, 172, [(t, t / 10) for t in (0, 2, 4, 6, 8, 10)])
    + f'<text class="xs" x="385" y="200" text-anchor="middle">composite carrier score</text>')

fig("secondary_transfer", "f4_marker",
    "Specificity of ITGA2B as a surface marker",
    "ITGA2B is present in 87 percent of myeloid progenitor cells and 3 percent of all other cell types.",
    W, 216,
    hbar(230, 40, 380, 26, .87, "87%", "Myeloid progenitor", UP)
    + hbar(230, 112, 380, 26, .03, "3%", "All other cell types", FLAT)
    + axis_x(230, 610, 164, [(f"{t}%", t / 100) for t in (0, 25, 50, 75, 100)])
    + f'<text class="xs" x="420" y="206" text-anchor="middle">cells positive for ITGA2B (CD41)</text>')

# ---------------------------------------------------------------- project 04
fig("leukemia", "f1_pipeline",
    "Disease comparison pipeline",
    "Datasets are harmonised, aggregated per cell type, scored against mitochondrial gene sets, then tested.",
    W, 196,
    chain([("Patient and donor datasets", None), ("Harmonise", "batch and normalisation"),
           ("Pseudobulk", "per cell type, per donor"), ("Mitochondrial gene sets", "OXPHOS, mitoribosome"),
           ("Test per cell type", None)], 14, 26, 130, 92, 18, width=14)
    + f'<text class="xs" x="12" y="158">Batch structure is the limiting factor: the datasets come from different studies and conditions.</text>'
    + f'<text class="xs" x="12" y="176">Run across 10 cell groups.</text>')

_rows = [("T cells", 1, True), ("NK cells", 1, True), ("B cells", 1, False),
         ("Erythroid", -1, True)]
_AX, _ANN = 400, 548
_body = [f'<line class="ax" x1="{_AX}" y1="30" x2="{_AX}" y2="212"/>',
         f'<text class="xs" x="{_AX}" y="24" text-anchor="middle">no change</text>']
for i, (nm, d, sig) in enumerate(_rows):
    y = 56 + i * 36
    _body.append(f'<text class="s" x="250" y="{y}" text-anchor="end" dominant-baseline="middle">{esc(nm)}</text>')
    x2 = _AX + d * 110
    col = UP if d > 0 else DOWN
    _body.append(f'<line x1="{_AX}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="3"/>')
    _body.append(f'<circle cx="{x2}" cy="{y}" r="8" fill="{col if sig else "#faf8ff"}" stroke="{col}" stroke-width="2.5"/>')
    txt = ("up, consistent" if d > 0 else "down, consistent") if sig else "same direction, not significant"
    _body.append(f'<text class="xs" x="{_ANN}" y="{y}" dominant-baseline="middle">{esc(txt)}</text>')
# the remaining six of the ten groups tested, as a row of open markers on the axis
_y = 232
_body.append(f'<text class="s" x="250" y="{_y}" text-anchor="end" dominant-baseline="middle">6 further groups</text>')
for k in range(6):
    _body.append(f'<circle cx="{_AX - 35 + k * 14}" cy="{_y}" r="5.5" fill="none" stroke="{FLAT}" stroke-width="1.8"/>')
_body.append(f'<text class="xs" x="{_ANN}" y="{_y}" dominant-baseline="middle">no reliable signal</text>')
_body.append(f'<text class="xs" x="12" y="268">Ten cell groups were tested in all. Filled marker: significant. Open marker: same direction, not significant.</text>')
_body.append(f'<text class="xs" x="12" y="284">Effect sizes are modest; horizontal positions are qualitative.</text>')
fig("leukemia", "f2_direction",
    "Direction of change in mitochondrial gene expression, AML against healthy donors",
    "T and NK cells move up, B cells trend up without reaching significance, erythroid cells move down, the six remaining groups show no reliable signal.",
    W, 292, "\n".join(_body))

_dis = [("Leukemia (AML)", "complete"), ("Microgravity", "queued"), ("Infarct", "queued"),
        ("Obesity", "queued"), ("PCOS", "queued")]
_b = []
_SPINE = 404
for i, (nm, st) in enumerate(_dis):
    y = 30 + i * 52
    done = st == "complete"
    _b.append(box(12, y, 220, 42, nm, "box" if done else "boxw", width=24, r=10))
    _b.append(f'<text class="xs" x="244" y="{y + 21}" dominant-baseline="middle">{esc(st)}</text>')
    _b.append(f'<line x1="340" y1="{y + 21}" x2="{_SPINE}" y2="{y + 21}" stroke="{INK}" stroke-width="2"/>')
_b.append(f'<line x1="{_SPINE}" y1="51" x2="{_SPINE}" y2="259" stroke="{INK}" stroke-width="2"/>')
_b.append(arrow(_SPINE, 155, 448, 155))
_b.append(box(460, 100, 180, 110, "Shared mitochondrial response model", "box", width=16))
_b.append(arrow(640, 155, 684, 155))
_b.append(label(722, 155, "per-organelle predictions", "xs", width=13))
fig("leukemia", "f4_roadmap",
    "Disease datasets feeding a shared model",
    "One completed disease comparison and four queued ones feed a shared model of mitochondrial perturbation.",
    W, 300, "\n".join(_b))


fig("leukemia", "f3_genesets",
    "The two mitochondrial gene families that carry the signal",
    "Oxidative phosphorylation genes and mitochondrial ribosome genes are the families whose coordinated movement produces the result.",
    W, 250,
    box(60, 46, 250, 86, "Oxidative phosphorylation", "box", sub="the respiratory chain itself", width=22)
    + box(60, 148, 250, 86, "Mitochondrial ribosome", "box", sub="the machinery that builds it", width=22)
    + arrow(310, 89, 404, 120)
    + arrow(310, 191, 404, 160)
    + box(416, 92, 200, 96, "Coordinated shift", "boxw", sub="scored per cell type", width=18)
    + f'<text class="xs" x="12" y="24">Both families move together, which is what makes a modest change readable.</text>')

# ---------------------------------------------------------------- project 05, Chlorella
fig("chlorella", "f1_design",
    "Cross species pilot design and the outcomes it distinguishes",
    "Mitochondria isolated from Chlorella are added to mammalian cells; three outcomes are distinguishable.",
    W, 320,
    chain([("Chlorella culture", None), ("Isolate mitochondria", None),
           ("Add to mammalian cells", None)], 12, 26, 200, 80, 34, width=18)
    + f'<path class="arr" d="M 346,106 L 346,140"/>'
    + box(12, 152, 232, 92, "No uptake", "boxw", sub="recognised and excluded")
    + box(264, 152, 232, 92, "Transient uptake", "box", sub="taken up, then cleared")
    + box(516, 152, 232, 92, "Functional tolerance", "boxw", sub="retained and used")
    + f'<text class="xs" x="12" y="276">Prior expectation: no uptake, or transient uptake followed by clearance on efficiency grounds.</text>'
    + f'<text class="xs" x="12" y="296">A functional effect would raise the broader question of cross species compatibility limits.</text>')

# ---------------------------------------------------------------- project 07
_ch = ["Ethical assessment", "Environmental impact", "Market assessment", "Dose modeling proposal", "Case for IVF review"]
_b = [box(12 + i * 151, 40, 139, 92, c, "box" if i < 3 else "boxw", width=14) for i, c in enumerate(_ch)]
_b.append(f'<text class="xs" x="12" y="24">Five parts, written as one argument rather than five notes.</text>')
_b.append(f'<path class="dash" d="M 466,142 L 466,158 L 692,158 L 692,142"/>')
_b.append(f'<text class="xs" x="579" y="176" text-anchor="middle">added after expert review</text>')
fig("impact_review", "f1_structure",
    "Structure of the review",
    "Five parts: ethical, environmental and market assessment, a dose modeling proposal and a case for revisiting IVF.",
    W, 196, "\n".join(_b))

_x0, _x1, _y0, _y1 = 80, 700, 44, 186
_curve = "M " + " L ".join(
    f"{_x0 + (_x1 - _x0) * (i / 60):.1f},{_y1 - (_y1 - _y0) * (lambda d: 4 * d * (1 - d))(i / 60):.1f}"
    for i in range(61))
fig("impact_review", "f2_dose",
    "Dose modeling: why a window is expected",
    "Schematic showing benefit rising with dose, then falling, with a usable window in the middle.",
    W, 272,
    f'<rect x="{_x0 + (_x1 - _x0) * 0.3:.0f}" y="{_y0}" width="{(_x1 - _x0) * 0.4:.0f}" height="{_y1 - _y0}" fill="#ece7f8"/>'
    + f'<text class="xs" x="{(_x0 + _x1) / 2:.0f}" y="{_y0 - 8}" text-anchor="middle">candidate window</text>'
    + f'<path d="{_curve}" fill="none" stroke="{INK}" stroke-width="2.8"/>'
    + f'<line class="ax" x1="{_x0}" y1="{_y1}" x2="{_x1}" y2="{_y1}"/>'
    + f'<line class="ax" x1="{_x0}" y1="{_y0 - 4}" x2="{_x0}" y2="{_y1}"/>'
    + f'<text class="xs" x="{(_x0 + _x1) / 2:.0f}" y="{_y1 + 26}" text-anchor="middle">mitochondrial dose</text>'
    + f'<text class="xs" x="40" y="115" text-anchor="middle" transform="rotate(-90,40,115)">expected benefit</text>'
    + f'<text class="xs" x="{_x0}" y="{_y1 + 52}">Schematic. The proposal is to establish where this window sits, since no dosing basis exists.</text>'
    + f'<text class="xs" x="{_x0}" y="{_y1 + 70}">Too little has no effect; too much adds material the recipient cell has to clear.</text>')

# ---------------------------------------------------------------- project 08
fig("archie", "f1_protocols",
    "Published protocol compared with the protocol used in the lab",
    "Three steps differ: how cells are broken open, how much filtration is used, and the buffer.",
    W, 300,
    f'<text class="t" x="12" y="24">As described in the literature</text>'
    + chain([("Break cells", "fine needle"), ("Filter", "repeated"), ("Standard buffer", None)],
            12, 36, 232, 76, 22, width=18)
    + f'<text class="t" x="12" y="164">As performed in the lab</text>'
    + chain([("Break cells", "sonication"), ("Filter", "minimal, to limit damage"), ("Different buffer", None)],
            12, 176, 232, 76, 22, width=18)
    + f'<text class="xs" x="12" y="288">Each change reduces mechanical stress on the mitochondria. None of it is stated in the papers.</text>')

# ---------------------------------------------------------------------------
n = 0
for slug, items in FIGS.items():
    d = ROOT / "projects" / slug / "img"
    d.mkdir(parents=True, exist_ok=True)
    for name, content in items:
        (d / f"{name}.svg").write_text(content)
        n += 1
print(f"{n} figures written across {len(FIGS)} projects")
