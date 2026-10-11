"""Generates projects/<slug>/index.html for every project.

All project text lives in this file. Figures are generated separately by
scripts/build_figures.py into projects/<slug>/img/ and referenced from here.

Run: python3 scripts/build_figures.py && python3 scripts/build_projects.py
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "projects"

GH = "https://github.com/July98293/mito"
DRIVE = "https://drive.google.com/drive/folders/17nLbYjkUvkEW27cAddLuNI1Nr_VTc1U7"
REVIEW = "https://docs.google.com/document/d/1kj4KnFPToj63mUdTQlj4Y36CZ2tQBBy-ZaOkEYCL3Wo/edit?tab=t.0"
PROTO_IT = "https://docs.google.com/document/d/1kcMtympZKznmKZOCmk6glHhtj8bLUTGe6FA3WrZYADY/edit?usp=sharing"

ORDER = ["neutrophil_transfer", "microgravity_blood", "secondary_transfer", "leukemia",
         "disease_modeling", "chlorella", "impact_review", "archie"]
PAGES = {}
NAMES = {}


def page(slug, title, status, cls, kind, lead, body, links=()):
    PAGES[slug] = dict(title=title, status=status, cls=cls, kind=kind, lead=lead, body=body, links=links)
    NAMES[slug] = title


def photo(n, src, alt, cap):
    """A figure backed by a static image under assets/img/, not a generated SVG."""
    return (f'  <figure>\n'
            f'    <img class="photo" src="../../assets/img/{src}" alt="{alt}">\n'
            f'    <figcaption><b>Figure {n}.</b> {cap}</figcaption>\n'
            f'  </figure>')


def fig(n, src, alt, cap):
    return (f'  <figure>\n'
            f'    <img src="img/{src}.svg" alt="{alt}">\n'
            f'    <figcaption><b>Figure {n}.</b> {cap}</figcaption>\n'
            f'  </figure>')


def ul(items):
    return "  <ul>\n" + "\n".join(f"    <li>{i}</li>" for i in items) + "\n  </ul>"


def ol(items):
    return "  <ol>\n" + "\n".join(f"    <li>{i}</li>" for i in items) + "\n  </ol>"


def h(text):
    return f"  <h2>{text}</h2>"


VERNE = ('  <blockquote class="quote"><p>&ldquo;Science, my lad, is made up of mistakes, but they are mistakes which '
         'it is useful to make, because they lead little by little to the truth.&rdquo;</p>'
         '<cite>Jules Verne, <i>Journey to the Center of the Earth</i></cite></blockquote>')


# ============================================================== 01
page("neutrophil_transfer",
     "Mitochondrial Transfer into Neutrophils", "Ongoing", "ongoing", "Wet lab",
     "Isolated mitochondria were transferred into granulocytes across several runs. Uptake was low and the activity "
     "signal was lost within about 20 minutes. Two causes were identified: the isolation step itself damages "
     "mitochondria, and uptake is genetically constrained. A route that avoids isolation is the next experiment.",
     "\n".join([
         h("Objective"),
         ul(["Deliver functional mitochondria into neutrophils.",
             "Keep them active long enough to produce a measurable effect."]),

         h("Method"),
         ol(["Isolate mitochondria from donor cells by differential centrifugation.",
             "Label with a fluorescent activity dye.",
             "Co-incubate with granulocytes.",
             "Follow the fluorescent signal over time."]),
         fig(1, "f1_workflow", "Five step workflow from donor cells to fluorescence readout.",
             "Workflow used in the May and June runs. The two failure points sit at co-incubation and readout."),

         h("Results"),
         ul(["Uptake was low in every run.",
             "Transferred mitochondria lost detectable activity after about 20 minutes.",
             "Lipid-mediated delivery was the first hypothesis for the loss. It was dropped once the cause became clearer.",
             "Negative result: isolated mitochondria are too fragile for this cell type without stabilisation."]),
         fig(2, "f2_activity", "Decay curve of the activity signal reaching the detection floor at about 20 minutes.",
             "Shape of the observed loss of signal. Schematic, not measured values."),
         VERNE,

         h("What explained it"),
         ol(['The isolation protocol in the literature is not the one the lab uses. Less filtration, a different '
             'buffer, and sonication rather than a fine needle, all to limit damage. Learned while '
             '<a href="../archie/">shadowing the ARCHIE project</a>.',
             'Mitochondrial uptake is genetically limited. This came out of the '
             '<a href="../secondary_transfer/">secondary transfer analysis</a> running in parallel.',
             'The PORTER team keeps mitochondria in blood, stabilises them there, and performs the transfer in that '
             'environment rather than extracting them. Their result matches the hypothesis I started from. It is '
             'unpublished, so it was not available from the literature.']),
         fig(3, "f3_routes", "Comparison of the isolated route used here and the in-blood route used by the PORTER team.",
             "The two routes differ in one respect that matters: whether mitochondria ever leave the blood."),

         h("Status and next steps"),
         ul(["<b>19 September.</b> Run scheduled at the Stanford lab, postponed when the professor had to leave town.",
             "<b>22 September.</b> Rescheduled as a variation of the in-blood route.",
             "<b>Fallback.</b> Reproduce in Italy. No PORTER machine there, and the mitochondria may not survive without it.",
             'Reagent ordering was blocked until grant funds reached the lab account, since ordering requires a lab ID.']),

         h("Assessment"),
         ul(["The initial hypothesis about granulocytes was correct, but not testable with the method available at the time.",
             "The limiting factor was the preparation, not the cell type."]),
     ]),
     [("Protocol, Italy", PROTO_IT)])

# ============================================================== 02
page("microgravity_blood",
     "Mitochondrial Transfer in Blood after Microgravity", "Planned", "planned", "Wet lab",
     "A variation of the neutrophil experiment in which blood is exposed to simulated microgravity before transfer. "
     "The design is fixed. The work is blocked on access to a calibrated clinostat.",
     "\n".join([
         h("Objective"),
         ul(["Test whether exposure to simulated microgravity changes mitochondrial uptake or how long activity persists.",
             "Keep every other variable identical to the <a href=\"../neutrophil_transfer/\">neutrophil experiment</a>."]),

         h("Design"),
         ul(["Two factors: gravity condition and transfer.",
             "Four arms, each read out for uptake and for persistence of activity."]),
         fig(1, "f1_design", "Two by two design crossing static against clinostat with no transfer against transfer.",
             "The two by two design. The microgravity and transfer arm is the condition of interest; the other three bound it."),

         h("Protocol order"),
         ol(["Draw blood.",
             "Expose to simulated microgravity in a clinostat for a fixed duration.",
             "Perform the transfer in blood, following the in-blood route.",
             "Read out uptake and persistence."]),
         fig(2, "f2_protocol", "Four step protocol from drawing blood to readout.",
             "Protocol order. The exposure step is the only addition to the existing transfer protocol."),

         h("Blocker"),
         ul(["Requires a calibrated clinostat. A self-built unit would not make the experiment reproducible by other labs.",
             "Microgravity is also queued as a dataset in the <a href=\"../disease_modeling/\">disease comparison work</a>, "
             "so the wet-lab and computational sides can eventually be compared."]),
     ]))

# ============================================================== 03
page("secondary_transfer",
     "Secondary Mitochondrial Transfer", "Code done, in review", "done", "Computational",
     "Rather than delivering isolated mitochondria directly, use a cell as the carrier. This project built a "
     "single-cell pipeline across the immune system to rank which populations can receive, hold and redistribute "
     "mitochondria. The myeloid progenitor ranks highest, with a highly specific surface marker but a narrow "
     "tissue distribution.",
     "\n".join([
         photo(1, "nanotube_sem.png",
               "Scanning electron micrograph of a T cell joined to a cancer cell by a single long nanotube.",
               "Two cells joined by a single nanotube. Connections like this are the physical route cargo takes "
               "between cells, and the reason a carrier cell is worth looking for."),

         h("Rationale"),
         ul(["Isolated mitochondria are fragile in transit and poorly taken up. That is the constraint from the "
             "<a href=\"../neutrophil_transfer/\">wet-lab work</a>.",
             "A cell that takes up mitochondria and delivers them elsewhere avoids exposing them to a buffer.",
             "This makes delivery more controlled and potentially targeted."]),
         fig(2, "f1_concept", "Direct transfer compared with transfer through an intermediate carrier cell.",
             "Direct delivery against carrier-mediated delivery. The analysis is about who should play the middle role."),

         h("Method"),
         ul(["No prior single-cell experience. Two weeks at the start of July to learn data structures, normalisation, "
             "pseudobulk analysis, batch structure and cell-state scoring.",
             "The pipeline was rebuilt three times, each pass tightening normalisation and the scoring definition.",
             "Now final and awaiting review."]),
         fig(3, "f2_pipeline", "Five stage pipeline from single cell datasets to ranked candidates.",
             "Analysis pipeline. Scoring combines uptake and donation programs rather than a single marker."),

         h("Questions"),
         ol(["Which pathways correlate with mitochondrial uptake and transfer?",
             "Which immune cells are strongest at producing, receiving and donating mitochondria?",
             "Which cells can reach each other, and which are best placed to donate?"]),

         h("Results"),
         ul(["Myeloid progenitor is the strongest candidate, at a composite score of 8.43.",
             "Its marker, ITGA2B (CD41), is present in 87% of its cells against 3% across other cell types.",
             "It is found in a single organ, which limits where it can be sourced.",
             "Haematopoietic stem cells and progenitors score 5.49 but span 8 organs and 2,825 cells, with FLT3 (CD135) as the marker."]),
         fig(4, "f3_scores", "Bar chart of composite carrier scores: 8.43 for myeloid progenitor, 5.49 for HSC and progenitors.",
             "Composite carrier score for the two leading populations, with their tissue breadth alongside."),
         fig(5, "f4_marker", "Bar chart showing ITGA2B present in 87 percent of myeloid progenitor cells against 3 percent elsewhere.",
             "ITGA2B specificity. A marker this clean makes the population straightforward to sort for."),
         """  <div class="table-wrap">
  <table>
    <caption>Table 1. Leading candidate carrier populations.</caption>
    <thead><tr><th>Population</th><th class="num">Score</th><th>Marker</th><th>Breadth</th></tr></thead>
    <tbody>
      <tr><td>Myeloid progenitor</td><td class="num">8.43</td><td>ITGA2B (CD41)</td><td>1 organ</td></tr>
      <tr><td>HSC / progenitors</td><td class="num">5.49</td><td>FLT3 (CD135)</td><td>8 organs, 2,825 cells</td></tr>
    </tbody>
  </table>
  </div>""",

         h("Trade-off"),
         ul(["Highest score with the cleanest marker, but one organ.",
             "Lower score, but broadly distributed and far easier to obtain.",
             "Which matters more depends on whether the carrier has to be sourced from the patient."]),
     ]),
     [("Analysis code", GH)])

# ============================================================== 04
page("leukemia",
     "Comparison against Disease: Leukemia", "Partially done", "ongoing", "Computational",
     "The receiver-program pipeline was extended to disease. In acute myeloid leukemia against healthy donors, "
     "mitochondrial genes are modestly but consistently up in T and NK cells, down in erythroid cells, and flat "
     "elsewhere. Batch structure across studies is the limiting factor.",
     "\n".join([
         h("Objective"),
         ul(["Identify and characterise mitochondrial receiver programs in a disease context.",
             "Establish a comparison that holds up across datasets from different studies."]),

         h("Method"),
         ol(["Select patient and healthy donor datasets.",
             "Harmonise batch structure and normalisation.",
             "Aggregate to pseudobulk per cell type, per donor.",
             "Score against mitochondrial gene sets, chiefly oxidative phosphorylation and mitochondrial ribosome genes.",
             "Test per cell type. Run across 10 cell groups."]),
         fig(1, "f1_pipeline", "Five stage disease comparison pipeline.",
             "Disease comparison pipeline. Steps 1 and 2 are where most of the work sits."),

         h("Results"),
         ul(["T and NK cells: up, modest but consistent.",
             "B cells: same direction, short of significance.",
             "Erythroid cells: down.",
             "Remaining cell types tested: no reliable signal.",
             "Not every one of the 10 groups shows significant variation in pathways."]),
         fig(2, "f2_direction", "Direction of change by cell type in AML against healthy donors.",
             "Direction of change by cell type. Effect sizes are modest, so direction and consistency carry the result, not magnitude."),

         h("Limits"),
         ul(["Datasets come from different studies and experimental conditions, so batch correction drives the outcome.",
             "Dataset selection for multi-disease comparison is still open.",
             "Review of the code is still outstanding."]),
     ]),
     [("Analysis code", GH)])

# ============================================================== 05
page("disease_modeling",
     "More Diseases and Organelle-Level Modeling", "Ongoing", "ongoing", "Computational",
     "With leukemia complete, further disease comparisons are queued. The aim is a shared model of how mitochondrial "
     "programs shift under perturbation: similar in concept to a virtual cell, but scoped to the organelle.",
     "\n".join([
         h("Queue"),
         ul(["Microgravity, which pairs with the <a href=\"../microgravity_blood/\">wet-lab experiment</a>.",
             "Infarct.", "Obesity.", "PCOS.", "Further conditions as suitable datasets appear."]),
         fig(1, "f1_roadmap", "Completed and queued disease datasets feeding a shared model.",
             "Each comparison adds one view of how mitochondrial programs shift. The model is only worth building once several agree."),

         h("Objective"),
         ul(["Combine the disease comparisons with the "
             "<a href=\"../secondary_transfer/\">donor and receiver map</a>.",
             "Model mitochondrial perturbation directly rather than inferring it from whole-cell behaviour."]),

         h("Requirement"),
         ul(["Enough disease datasets for the shared signal to separate from batch effects.",
             "That threshold has not been reached yet."]),
     ]))

# ============================================================== 06
page("chlorella",
     "Cross-Species Transfer: Chlorella to Mammalian Cells", "Scheduled", "planned", "Wet lab",
     "A pilot testing whether mitochondria from a photosynthetic alga are recognised and functionally tolerated by "
     "mammalian recipient cells. The design distinguishes three outcomes, and all three are informative.",
     "\n".join([
         h("Objective"),
         ul(["Determine whether mammalian cells take up Chlorella-derived mitochondria.",
             "If they do, determine whether the mitochondria are retained or cleared."]),

         h("Design"),
         ol(["Culture Chlorella.",
             "Isolate mitochondria.",
             "Add to mammalian recipient cells.",
             "Score against three outcomes: no uptake, transient uptake, functional tolerance."]),
         fig(1, "f1_design", "Three step pilot design with three distinguishable outcomes.",
             "Pilot design. The three outcomes are separable, so a negative result is still a result."),

         h("Prior expectation"),
         ul(["Most likely no uptake.",
             "Otherwise transient uptake followed by clearance, on the grounds that these mitochondria are not efficient in a mammalian cell.",
             "A functional effect would open the broader question of cross-species compatibility and the limits of mitochondrial transplantation."]),

         h("Status"),
         ul(["Waiting on the algae.", "Experiment scheduled for 20 September."]),
     ]),
     [("Protocol and supporting material", DRIVE)])

# ============================================================== 07
page("impact_review",
     "Review, Impact Analysis and Dose Modeling", "Analysis done, writing", "done", "Review",
     "A review of mitochondrial transfer carrying what appears to be the first combined ethical, environmental and "
     "market assessment of the field, a dose-modeling proposal, and a case for revisiting mitochondrial transfer in IVF.",
     "\n".join([
         h("Structure"),
         ul(["Ethical assessment.", "Environmental impact assessment.", "Market assessment.",
             "Dose-modeling proposal.", "A case for reopening mitochondrial transfer in IVF.",
             "The dose-modeling, environmental, ethical and market analyses sit in chapters 4 and 5."]),
         fig(1, "f1_structure", "Five parts of the review, two of which were added after expert review.",
             "Structure of the review. The last two parts were added as the scope grew."),

         h("Dose modeling"),
         ul(["No dosing basis currently exists for mitochondrial transfer.",
             "Too small a dose produces no effect. Too large a dose adds material the recipient cell has to clear.",
             "A usable window is therefore expected, and the proposal is to establish where it sits."]),
         fig(2, "f2_dose", "Schematic dose response curve with a candidate therapeutic window.",
             "Why a window is expected. Schematic: the shape is the argument, the position is what the proposal sets out to determine."),

         h("How it grew"),
         ul(["Started as a short piece.",
             "Rewritten roughly five times as conversations with subject experts changed the scope each round.",
             "The result is one argument rather than five separate notes."]),

         h("Status"),
         ul(["Analysis complete.", "Writing needs tightening.", "Figures and ordering still to be finalised."]),
     ]),
     [("Review document", REVIEW), ("Supporting material", DRIVE)])

# ============================================================== 08
page("archie",
     "Shadowing the ARCHIE Project", "Done", "done", "Training",
     "Training placement on a project performing mitochondrial transplantation into granulocytes. It established "
     "that the working protocol differs from the published one at three points, each reducing mechanical stress on "
     "the mitochondria.",
     "\n".join([
         h("Objective"),
         ul(["Observe mitochondrial transplantation performed by a lab doing it routinely.",
             "Compare the working protocol against the published one."]),

         h("Findings"),
         ol(["Cells are broken open by sonication rather than with a fine needle.",
             "Filtration is kept to a minimum, to avoid damaging the mitochondria.",
             "A different buffer is used.",
             "Isolated mitochondria are highly sensitive, which is why the PORTER approach keeps them in blood instead."]),
         fig(1, "f1_protocols", "Published protocol against the protocol used in the lab, differing at three steps.",
             "Where the two protocols diverge. None of these differences are stated in the papers."),

         h("Consequence"),
         ul(["Explains the low uptake and rapid loss of activity in the "
             "<a href=\"../neutrophil_transfer/\">neutrophil experiments</a>.",
             "Turned a set of negative results into a defined next experiment."]),
     ]))


# =========================================================== render
def render():
    for i, slug in enumerate(ORDER):
        p = PAGES[slug]
        prev_, next_ = (ORDER[i - 1] if i else None), (ORDER[i + 1] if i < len(ORDER) - 1 else None)
        nav = '  <div class="next-prev">'
        nav += f'<a class="pill" href="../{prev_}/">&larr; {NAMES[prev_]}</a>' if prev_ else "<span></span>"
        nav += (f'<a class="pill dark" href="../{next_}/">{NAMES[next_]} &rarr;</a>' if next_
                else '<a class="pill dark" href="../../index.html#projects">All projects &rarr;</a>')
        nav += "</div>"
        links = "".join(f'<li><a href="{u}">&#8599; {t}</a></li>' for t, u in p["links"])
        links_block = f'  <h2>Links</h2>\n  <ul class="links">{links}</ul>\n' if links else ""
        html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{p['title']} &middot; Mitochondria</title>
  <link rel="stylesheet" href="../../assets/css/style.css">
</head>
<body>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="../../index.html" aria-label="Home"><svg viewBox="0 0 40 18" width="40" height="18" aria-hidden="true"><rect x="1.4" y="1.4" width="37.2" height="15.2" rx="7.6" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M 8,9 Q 11,3.6 14,9 T 20,9 T 26,9 T 32,9" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></a>
    <nav class="nav-links">
      <a href="../../index.html#projects">Projects</a>
      <a href="{GH}">GitHub</a>
      <a class="pill small" href="https://primordiagrants.com">Primordia &#8599;</a>
    </nav>
  </div>
</header>

<main class="wrap narrow">
  <div class="back-row"><a class="pill small" href="../../index.html#projects">&larr; All projects</a></div>

  <section class="p-hero grain">
    <div class="sheet">
      <div class="tags"><span class="tag">Project {i + 1:02d}</span><span class="tag">{p['kind']}</span><span class="tag {p['cls']}">{p['status']}</span></div>
      <h1>{p['title']}</h1>
    </div>
  </section>

  <article class="article">
  <p class="lead">{p['lead']}</p>
{p['body']}
{links_block}{nav}
  </article>
</main>

<footer class="foot">
  <div class="wrap">
    <span>Jules &middot; Italy</span>
    <span>Supported by <a href="https://primordiagrants.com">Primordia Grants</a> &middot; <a href="{GH}">GitHub</a></span>
  </div>
</footer>
</body>
</html>
"""
        d = OUT / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(html)
    print(f"{len(ORDER)} project pages written")


render()
