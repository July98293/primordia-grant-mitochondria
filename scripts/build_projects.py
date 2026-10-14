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

ORDER = ["neutrophil_transfer", "secondary_transfer", "leukemia", "chlorella", "impact_review"]
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


def gallery(folder, caption):
    """A square grid of lab photographs from assets/img/<folder>/, four per row.

    Renders nothing while the folder is empty, so dropping files in and
    rebuilding is all that is needed."""
    d = ROOT / "assets" / "img" / folder
    shots = sorted(q.name for q in d.glob("*") if q.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"})
    if not shots:
        return ""
    tiles = "\n".join(
        f'    <figure><img src="../../assets/img/{folder}/{n}" alt="Lab photograph from the transfer runs." loading="lazy"></figure>'
        for n in shots)
    return (f'  <div class="gallery">\n{tiles}\n  </div>\n'
            f'  <p class="gallery-cap">{caption}</p>')


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
     "signal was lost within about 20 minutes. Two constraints came out of it: the cells are fragile, and uptake is "
     "genetically limited.",
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
             "Lipid-mediated delivery was the first hypothesis for the loss. It was dropped once the cause became clearer."]),
         fig(2, "f2_activity", "Decay curve of the activity signal reaching the detection floor at about 20 minutes.",
             "Shape of the observed loss of signal. Schematic, not measured values."),
         VERNE,

         h("What explained it"),
         ul(["The neutrophils were too fragile.",
             'Mitochondrial uptake is genetically limited. This came out of the '
             '<a href="../secondary_transfer/">secondary transfer analysis</a> running in parallel.',
             "Another team is doing this with finer technology, transferring mitochondria into whole blood without "
             "separating them first."]),

         h("From the bench"),
         gallery("neutrophil_gallery",
                 "Isolation, labelling and transfer runs. Pellets, gradient fractions and the bench they were done on."),
     ]))

# ============================================================== 02
# ============================================================== 02
page("secondary_transfer",
     "Secondary Mitochondrial Transfer", "Ongoing", "ongoing", "Computational",
     "Rather than delivering isolated mitochondria directly, use a cell as the carrier. This project built a "
     "single-cell pipeline across the immune system to rank which populations can receive, hold and redistribute "
     "mitochondria. The myeloid progenitor ranks highest, with a highly specific surface marker but a narrow "
     "tissue distribution.",
     '  <p class="banner">Still ongoing. The full write-up will follow.</p>',
     [("Analysis code", GH)])

# ============================================================== 03
page("leukemia",
     "Comparison of Mitochondrial Expression against Disease: Leukemia", "Partially done", "ongoing", "Computational",
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

         h("What is measured"),
         ul(["Two gene families carry the signal: the respiratory chain itself, and the ribosome that builds it.",
             "Neither family moves far on its own. They move together, which is what makes the shift readable."]),
         fig(2, "f3_genesets", "The two mitochondrial gene families feeding the per cell type score.",
             "Oxidative phosphorylation and mitochondrial ribosome genes, scored together per cell type."),

         h("Results"),
         ul(["T and NK cells: up, modest but consistent.",
             "B cells: same direction, short of significance.",
             "Erythroid cells: down.",
             "The six remaining groups of the ten tested: no reliable signal.",
             "The effect is a coordinated shift rather than a few strongly changed genes."]),
         fig(3, "f2_direction", "Direction of change by cell type in AML against healthy donors, across ten cell groups.",
             "Direction of change by cell type. Effect sizes are modest, so direction and consistency carry the result, not magnitude."),

         h("Limits"),
         ul(["Datasets come from different studies and experimental conditions, so batch correction drives the outcome.",
             "Dataset selection for multi-disease comparison is still open.",
             "Review of the code is still outstanding."]),

         h("This is the beginning"),
         ul(["Leukemia is the first disease through the pipeline, not the point of it.",
             "Microgravity, infarct, obesity, PCOS and others are queued.",
             "The intent is to see how mitochondria vary across disease, rather than to characterise any one of them.",
             "With enough comparisons the shared response can be modelled directly, at the level of the organelle."]),
         fig(4, "f4_roadmap", "Completed and queued disease datasets feeding a shared model.",
             "Each comparison adds one view of how mitochondrial programs shift. The model is only worth building once several agree."),
     ]),
     [("Analysis code", GH)])

# ============================================================== 04
# ============================================================== 04
page("chlorella",
     "Cross-Species Transfer: Chlorella to Mammalian Cells", "Attempted, unsuccessful", "ongoing", "Wet lab",
     "A pilot testing whether mitochondria from a photosynthetic eukaryote are recognised and functionally tolerated "
     "by mammalian recipient cells. Isolation was attempted by differential centrifugation, following the published "
     "plant protocol. It did not yield a usable preparation. A density gradient is the obvious next attempt.",
     "\n".join([
         h("Objective"),
         ul(["Determine whether mammalian cells take up mitochondria from a photosynthetic eukaryote.",
             "If they do, determine whether the mitochondria are retained or cleared."]),

         h("Design"),
         ol(["Culture the algae and concentrate the cells.",
             "Isolate mitochondria.",
             "Add to mammalian recipient cells.",
             "Score against three outcomes: no uptake, transient uptake, functional tolerance."]),
         fig(1, "f1_design", "Three step pilot design with three distinguishable outcomes.",
             "Pilot design. The three outcomes are separable, so a negative result is still a result."),
         photo(2, "chlorella_culture.jpg",
               "A gloved hand holding a conical tube of dense green algal culture.",
               "Algal culture concentrated ahead of isolation."),
         photo(3, "plant_material.jpg",
               "A potato tuber held next to a sealed bag of 50 ml bio-reaction tubes containing green material.",
               "Plant material and 50 ml reaction tubes on the way to the lab. Potato tuber is the starting material "
               "in the published protocol the procedure was taken from."),

         h("Isolation procedure"),
         ul(["Adapted from the published method for isolating mitochondria from potato tubers "
             "(Havelund et al., <i>Bio-protocol</i> e1226). Every step is carried out at 0 to 4 &deg;C."]),
         ol(["Homogenise the tissue into roughly half its volume of extraction medium, containing cysteine as an "
             "antioxidant and bovine serum albumin to bind fatty acids and phenolics.",
             "Adjust to pH 7.2 with potassium hydroxide and leave the homogenate to stand for 5 minutes, so starch sediments.",
             "Filter through two layers of cotton.",
             "Spin at 3,000 &times; g for 5 minutes to clear debris and residual starch. Keep the supernatant.",
             "Spin the supernatant at 18,000 &times; g for 10 minutes to pellet crude mitochondria.",
             "Resuspend the pellet in mannitol gradient buffer."]),
         ul(["In the published method, steps 4 and 5 are followed by a step Percoll gradient of 50%, 28% and 20% layers, "
             "spun at 40,000 &times; g for 30 minutes, then washes at 18,000 &times; g.",
             "Only the differential centrifugation part was attempted here. The gradient was not."]),

         h("Outcome"),
         ul(["Differential centrifugation alone did not produce a usable mitochondrial preparation.",
             "This is the expected failure mode: without a density step, chloroplasts and other organelles of similar "
             "sedimentation behaviour are not separated out.",
             "The algal cell wall is also hard to break gently, which limits what the first spin can recover.",
             "No transfer into mammalian cells was reached, so the three outcomes above remain untested."]),

         h("Next attempt"),
         ul(["Add a density gradient. Ficoll is the candidate, in place of or alongside Percoll. It is the step the "
             "published protocol relies on, and the step that was skipped here.",
             "Ficoll is normally run as a two-layer gradient, around 8% over 14%, with the crude pellet loaded on top "
             "and left unmixed. Free mitochondria collect in the pellet rather than at an interface, which is the "
             "difference from a Percoll preparation.",
             "The wall has to come apart first. Published work on thick-walled algae reports that these protocols "
             "transfer across species with minor optimisation, provided the disruption step is adapted "
             "(F&uuml;ssy et al. on <i>Chromera velia</i>). Sonication is the obvious candidate.",
             "<i>Chlorella vulgaris</i> walls are specifically documented as resistant to disruption, so this is the "
             "step most likely to need the work.",
             "No Chlorella-specific mitochondrial isolation protocol appears to be published. The method has to be "
             "assembled from the plant and thick-walled algae literature."]),

         h("Prior expectation"),
         ul(["Most likely no uptake.",
             "Otherwise transient uptake followed by clearance, on the grounds that these mitochondria are not "
             "efficient in a mammalian cell.",
             "A functional effect would open the broader question of cross-species compatibility and the limits of "
             "mitochondrial transplantation."]),
     ]),
     [("Protocol and supporting material", DRIVE),
      ("Source protocol: Isolation of Mitochondria from Potato Tubers", "https://bio-protocol.org/e1226"),
      ("Plastids and mitochondria from the thick-walled alga Chromera velia", "https://pubmed.ncbi.nlm.nih.gov/31422509"),
      ("Cell wall disintegration of Chlorella vulgaris", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8759652/")])

# ============================================================== 05
page("impact_review",
     "Review, Impact Analysis and Dose Modeling", "Analysis done, writing", "done", "Review",
     "A review of mitochondrial transfer carrying what appears to be the first combined ethical, environmental and "
     "market assessment of the field, a dose-modeling proposal, and a case for revisiting mitochondrial transfer in IVF.",
     '  <p class="banner">Still being written. The document is linked below.</p>',
     [("Review document", REVIEW), ("Supporting material", DRIVE)])


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
    <span>Made by a human on 🌍</span>
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
