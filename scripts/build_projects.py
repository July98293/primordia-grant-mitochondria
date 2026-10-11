"""Generates projects/<slug>/index.html for every project.
All project text lives in this file. Edit it, then run: python3 scripts/build_projects.py"""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
out = ROOT / "projects"

GH = "https://github.com/July98293/mito"
DRIVE = "https://drive.google.com/drive/folders/17nLbYjkUvkEW27cAddLuNI1Nr_VTc1U7"
REVIEW = "https://docs.google.com/document/d/1kj4KnFPToj63mUdTQlj4Y36CZ2tQBBy-ZaOkEYCL3Wo/edit?tab=t.0"
PROTO_IT = "https://docs.google.com/document/d/1kcMtympZKznmKZOCmk6glHhtj8bLUTGe6FA3WrZYADY/edit?usp=sharing"

ORDER = ["neutrophil_transfer", "microgravity_blood", "secondary_transfer", "leukemia",
         "disease_modeling", "chlorella", "impact_review", "archie"]
NAMES = {}
PAGES = []

NAMES_BY_NUM = {"1.1": "the neutrophil project", "1.2": "the microgravity project", "1.3": "the secondary transfer project",
                "1.4": "the leukemia project", "1.5": "the disease modeling project", "1.6": "the Chlorella project",
                "1.7": "the review", "1.8": "the ARCHIE shadowing"}

def clean(html):
    html = re.sub(r'<span class="secnum">\d+</span>', "", html)
    html = re.sub(r'<h3 class="sub">\d+\.\d+ ', '<h3 class="sub">', html)
    html = re.sub(r'project (1\.\d)', lambda m: NAMES_BY_NUM[m.group(1)], html)
    return html

def page(slug, num, title, status, cls, kind, abstract, body, refs):
    PAGES.append((slug, num, title, status, cls, kind, abstract, body, refs))
    NAMES[slug] = title

def render():
    for slug, num, title, status, cls, kind, abstract, body, refs in PAGES:
        i = ORDER.index(slug)
        prev_ = ORDER[i - 1] if i > 0 else None
        next_ = ORDER[i + 1] if i < len(ORDER) - 1 else None
        nav = '<div class="next-prev">'
        nav += f'<a class="pill" href="../{prev_}/">← {NAMES[prev_]}</a>' if prev_ else '<span></span>'
        nav += f'<a class="pill dark" href="../{next_}/">{NAMES[next_]} →</a>' if next_ else '<a class="pill dark" href="../../index.html#projects">All projects →</a>'
        nav += '</div>'
        links = "".join(f'<li><a href="{u}">↗ {t}</a></li>' for t, u in refs)
        links_block = f'<h2>Links</h2><ul class="links">{links}</ul>' if refs else ""
        html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · Mito Work</title>
  <link rel="stylesheet" href="../../assets/css/style.css">
</head>
<body>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="../../index.html">Mito Work <span>· Primordia</span></a>
    <nav class="nav-links">
      <a href="../../index.html#projects">Projects</a>
      <a href="{GH}">GitHub</a>
      <a class="pill small" href="https://primordiagrants.com">Primordia ↗</a>
    </nav>
  </div>
</header>

<main class="wrap narrow">
  <div class="back-row"><a class="pill small" href="../../index.html#projects">← All projects</a></div>

  <section class="p-hero grain">
    <div class="sheet">
      <div class="tags"><span class="tag">Project {i + 1:02d}</span><span class="tag">{kind}</span><span class="tag {cls}">{status}</span></div>
      <h1>{title}</h1>
    </div>
  </section>

  <article class="article">
    <p class="lead">{abstract}</p>
{clean(body)}
    {links_block}
    {nav}
  </article>
</main>

<footer class="foot">
  <div class="wrap">
    <span>Jules · Italy</span>
    <span>Supported by <a href="https://primordiagrants.com">Primordia Grants</a> · <a href="{GH}">GitHub</a></span>
  </div>
</footer>
</body>
</html>
"""
        d = out / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(html)

def fig(n, caption):
    return f"""  <figure>
    <div class="fig-placeholder grain"><span>figure coming soon</span></div>
    <figcaption><b>Figure {n}.</b> {caption}</figcaption>
  </figure>"""

# 1.1 ---------------------------------------------------------------
page("neutrophil_transfer", "1.1", "Mitochondrial Transfer into Neutrophils", "Ongoing", "ongoing", "Wet lab",
"Between May and June I ran several experiments transferring isolated mitochondria into granulocytes. Uptake stayed low, and the transferred mitochondria lost detectable activity after about 20 minutes. Shadowing an active lab and talking with the PORTER team showed why: isolated mitochondria are very fragile, and uptake is genetically limited. Their approach keeps mitochondria in blood and stabilises them there, which matches what I had hypothesised.",
f'''  <h2 class="sec"><span class="secnum">1</span>Timeline</h2>
  <ul class="timeline">
    <li><span class="when">May – June</span>Multiple mitochondrial transfer experiments in granulocytes.</li>
    <li><span class="when">End of June</span>Reagent ordering, once grant money reached the lab account. Ordering needed the lab ID, so I could not do it alone.</li>
    <li><span class="when">Sep 19</span>Planned run at the Stanford lab. Postponed because the professor had to leave town.</li>
    <li><span class="when">Sep 22</span>Rescheduled run: a variation of the PORTER-style experiment.</li>
  </ul>

  <h2 class="sec"><span class="secnum">2</span>First attempts</h2>
  <p>Uptake was low in every run. Based on the fluorescent activity assay, the mitochondria that did get in consistently
  lost signs of activity after roughly 20 minutes. My first idea was that lipid-mediated delivery might fix this.</p>

  <h2 class="sec"><span class="secnum">3</span>What changed my mind</h2>
  <p>While shadowing Coco in the lab (see <a href="../archie/">project 1.8</a>), I learned that mitochondrial extraction is done
  quite differently from what the published papers suggest. The lab uses a gentler protocol, with less filtration, a different
  buffer and a different way of breaking the cells open, all to avoid damaging the mitochondria.</p>
  <p>In parallel, the <a href="../secondary_transfer/">secondary transfer analysis</a> suggested that mitochondrial uptake is
  genetically limited. I discussed this with the PORTER team, who use the PORTER machine to transfer mitochondria into neutrophils.
  Instead of extracting mitochondria, they keep them in blood, stabilise them to preserve their activity, and do the transfer
  in that environment.</p>
  <span class="note">their result is what I expected, but it isn't published yet, so I couldn't have known from the literature</span>

  <h2 class="sec"><span class="secnum">4</span>Results so far</h2>
  <p>My initial hypothesis about granulocytes was correct, even though I had no way to test it at the time.
  The useful negative result is that isolated mitochondria seem too fragile for this cell type without stabilisation.</p>
  <blockquote class="quote"><p>“Science, my lad, is made up of mistakes, but they are mistakes which it is useful to make, because they lead little by little to the truth.”</p><cite>Jules Verne, <i>Journey to the Center of the Earth</i></cite></blockquote>

  <h2 class="sec"><span class="secnum">5</span>Next steps</h2>
  <ul>
    <li>Run a variation of the PORTER-style experiment.</li>
    <li>If time runs out here, try to reproduce it in Italy. I won't have a PORTER machine there, and I worry the mitochondria are too sensitive to survive without it.</li>
    <li>Run the <a href="../microgravity_blood/">microgravity variation</a>.</li>
  </ul>''',
[("Protocol (Italy)", PROTO_IT)])

# 1.2 ---------------------------------------------------------------
page("microgravity_blood", "1.2", "Mitochondrial Transfer in Blood after Microgravity", "Planned", "planned", "Wet lab",
"A planned variation of the neutrophil transfer experiment. Blood would first be exposed to simulated microgravity, then used for mitochondrial transfer, to see whether the altered environment changes uptake or activity.",
'''  <h2 class="sec"><span class="secnum">1</span>Idea</h2>
  <p>This is one of the variations of <a href="../neutrophil_transfer/">project 1.1</a> I would most like to run.
  The question is whether exposure to microgravity changes how blood cells take up and keep mitochondria.</p>

  <h2 class="sec"><span class="secnum">2</span>Status</h2>
  <p>I am looking for a clinostat. I can't just use one I build myself, because the experiment needs to be reproducible
  by other labs.</p>
  <span class="note">if you have a clinostat I could borrow, please reach out!</span>

  <h2 class="sec"><span class="secnum">3</span>Connection to other work</h2>
  <p>Microgravity is also queued as a dataset in the <a href="../disease_modeling/">disease comparison work</a>,
  so the wet-lab and computational sides can eventually be compared.</p>''',
[])

# 1.3 ---------------------------------------------------------------
page("secondary_transfer", "1.3", "Secondary Mitochondrial Transfer", "Code done · in review", "done", "Computational",
"The idea is to use cells as “Uber vehicles” for mitochondria. Instead of transferring isolated mitochondria directly, we identify or engineer cells that can take up mitochondria and deliver them to specific recipient cells. I built a single-cell RNA-seq pipeline across the immune system to find which cells are the best candidates to receive, carry and redistribute mitochondria, and which biological programs drive successful uptake. The strongest candidate is the myeloid progenitor.",
f'''  <h2 class="sec"><span class="secnum">1</span>Motivation</h2>
  <p>In principle, one cell could act as a mitochondrial donor or carrier and deliver mitochondria to another cell type.
  That would allow more controlled and potentially targeted delivery than injecting fragile isolated mitochondria.</p>

  <h2 class="sec"><span class="secnum">2</span>Method</h2>
  <p>I had never worked with single-cell data before. At the start of July I spent about two weeks learning single-cell
  RNA-seq analysis from zero: data structures, normalisation, pseudobulk analysis, batch structure and cell-state scoring.</p>
  <p>I then built the pipeline and reworked it about three times, refining the method and validating the results each round.
  The pipeline is now final and waiting for review.</p>

  <h3 class="sub">2.1 Questions the pipeline answers</h3>
  <ol>
    <li>Which pathways correlate with mitochondrial uptake and transfer?</li>
    <li>Which immune cells are strongest at producing, receiving and donating mitochondria?</li>
    <li>Which cells can talk to each other, and which immune cells are best at donating to others?</li>
  </ol>

{fig(1, "Pathway correlation.")}
{fig(2, "Immune cells with the strongest ability to produce, receive and donate mitochondria.")}
{fig(3, "Cell–cell communication: which immune cells are best placed to donate.")}

  <h2 class="sec"><span class="secnum">3</span>Results</h2>
  <div class="table-wrap">
  <table>
    <caption><b>Table 1:</b> Top candidate carrier populations and their best surface markers.</caption>
    <thead><tr><th>Cell population</th><th class="num">Score</th><th>Best marker</th><th>Notes</th></tr></thead>
    <tbody>
      <tr><td>Myeloid progenitor</td><td class="num">8.43</td><td>ITGA2B (CD41)</td><td>In 87% of its cells vs 3% of other types. Found in only 1 organ.</td></tr>
      <tr><td>HSC / progenitors</td><td class="num">5.49</td><td>FLT3 (CD135)</td><td>8 organs, 2,825 cells.</td></tr>
    </tbody>
  </table>
  </div>
  <p>The myeloid progenitor scores highest and has a very specific marker, but it appears in a single organ.
  Haematopoietic stem cells and progenitors score lower, yet are found much more broadly, which may make them more practical.</p>''',
[("Analysis code: github.com/July98293/mito", GH)])

# 1.4 ---------------------------------------------------------------
page("leukemia", "1.4", "Comparison against Disease: Leukemia", "Partially done", "ongoing", "Computational",
"I built a pipeline to identify and characterise mitochondrial receiver programs in disease contexts, starting with acute myeloid leukemia (AML). Compared with healthy donors, mitochondrial genes are modestly but consistently up in T and NK cells, down in erythroid cells, and show no reliable signal elsewhere.",
f'''  <h2 class="sec"><span class="secnum">1</span>Approach</h2>
  <p>The pipeline reuses the foundation of <a href="../secondary_transfer/">project 1.3</a> and applies it to disease datasets.
  Because datasets come from different studies and conditions, much of the work is choosing comparable datasets and building
  robust batch correction and normalisation.</p>

{fig(1, "Data used.")}
{fig(2, "Mitochondrial genes that vary most between leukemia and healthy donors in T cells.")}

  <p>The same analysis was re-run for 10 cell groups. Not every group shows significant pathway changes.</p>

{fig(3, "Re-run across 10 cell groups.")}
{fig(4, "Final check: cell types against the mitochondrial pathways affected.")}

  <h2 class="sec"><span class="secnum">2</span>Results</h2>
  <div class="table-wrap">
  <table>
    <caption><b>Table 1:</b> Mitochondrial gene expression in AML vs healthy donors, by cell type.</caption>
    <thead><tr><th>Cell type</th><th>Direction</th><th>Notes</th></tr></thead>
    <tbody>
      <tr><td>T cells</td><td>↑ up</td><td>Modest but consistent. Driven by oxidative-phosphorylation and mitochondrial-ribosome genes.</td></tr>
      <tr><td>NK cells</td><td>↑ up</td><td>Same pattern as T cells.</td></tr>
      <tr><td>B cells</td><td>↑ trend</td><td>Same direction, just short of significance.</td></tr>
      <tr><td>Erythroid</td><td>↓ down</td><td></td></tr>
      <tr><td>Other types tested</td><td>—</td><td>No reliable signal.</td></tr>
    </tbody>
  </table>
  </div>

  <h2 class="sec"><span class="secnum">3</span>Status</h2>
  <p>The code is partially complete and still needs review. I am evaluating which datasets are best for comparing
  several diseases at once.</p>''',
[("Analysis code: github.com/July98293/mito", GH)])

# 1.5 ---------------------------------------------------------------
page("disease_modeling", "1.5", "More Diseases and Organelle-Level Modeling", "Ongoing", "ongoing", "Computational",
"After leukemia, comparisons against microgravity, infarct, obesity, PCOS and other conditions are queued, together with integration into the secondary transfer project. With enough disease datasets, we could start modeling mitochondrial perturbations computationally: similar in concept to a virtual cell, but focused on the organelle.",
'''  <h2 class="sec"><span class="secnum">1</span>Queue</h2>
  <ul>
    <li>Microgravity</li>
    <li>Infarct</li>
    <li>Obesity</li>
    <li>PCOS</li>
    <li>Others to come</li>
  </ul>

  <h2 class="sec"><span class="secnum">2</span>Where this is going</h2>
  <p>Each new disease adds a view of how mitochondrial programs shift across cell types. Combined with the
  <a href="../secondary_transfer/">donor and receiver map</a>, this could become a focused model of mitochondrial
  perturbations, a kind of "virtual mitochondrion".</p>
  <span class="note">ambitious, I know. one dataset at a time</span>''',
[])

# 1.6 ---------------------------------------------------------------
page("chlorella", "1.6", "Cross-Species Mitochondrial Transfer: Chlorella → Mammalian Cells", "Scheduled", "planned", "Wet lab",
"A pilot experiment testing whether mitochondria from a photosynthetic eukaryote, the alga Chlorella, can be recognised and functionally tolerated by mammalian recipient cells. A positive effect would open broader questions about cross-species mitochondrial compatibility, uptake, and the limits of mitochondrial transplantation.",
'''  <h2 class="sec"><span class="secnum">1</span>Hypothesis</h2>
  <p>I suspect it won't work. Or maybe the mitochondria will be used for a while and then expelled because they are not efficient enough.
  Either outcome is informative.</p>

  <h2 class="sec"><span class="secnum">2</span>Status</h2>
  <ul class="timeline">
    <li><span class="when">Sep</span>Waiting for the algae to arrive.</li>
    <li><span class="when">Sep 20</span>Experiment scheduled.</li>
  </ul>''',
[("Protocol for the plant experiment (Drive folder)", DRIVE)])

# 1.7 ---------------------------------------------------------------
page("impact_review", "1.7", "Review, Impact Analysis and Dose Modeling", "Analysis done · writing", "done", "Review",
"A review of mitochondrial transfer that includes what I believe is the first combined ethical, environmental and market assessment of the field. It also proposes a dose-modeling approach and puts together a case for revisiting mitochondrial transfer in IVF.",
'''  <h2 class="sec"><span class="secnum">1</span>How it grew</h2>
  <p>I initially thought this would be a quick win. I ended up rewriting it about five times, because every conversation with
  experts on the topic changed something. It is much better for it.</p>
  <span class="note">the "side quest" of dose modeling turned into its own chapter</span>

  <h2 class="sec"><span class="secnum">2</span>Contents</h2>
  <ul>
    <li>Ethical assessment</li>
    <li>Environmental impact assessment</li>
    <li>Market assessment</li>
    <li>Dose-modeling proposal</li>
    <li>A case for reopening mitochondrial transfer in IVF</li>
  </ul>
  <p>The dose-modeling, environmental, ethical and market analyses are in chapters 4 and 5 of the review.</p>

  <h2 class="sec"><span class="secnum">3</span>Status</h2>
  <p>The analysis is complete. The writing needs polishing, and the figures and ordering still need to be finalised.</p>''',
[("Review document", REVIEW), ("Supporting material (Drive folder)", DRIVE)])

# 1.8 ---------------------------------------------------------------
page("archie", "1.8", "Shadowing the ARCHIE Project", "Done", "done", "Training",
"I shadowed the ARCHIE project to learn how mitochondrial transplantation into granulocytes is done in practice. I learned a different wet-lab approach using the PORTER machine, which directly reshaped my own neutrophil experiments.",
'''  <h2 class="sec"><span class="secnum">1</span>What I learned</h2>
  <ul>
    <li>Mitochondrial extraction in practice differs a lot from what published papers describe, with a gentler protocol overall.</li>
    <li>The PORTER approach keeps mitochondria in blood and stabilises them, instead of isolating them.</li>
    <li>Isolated mitochondria are highly sensitive, which explains my earlier results.</li>
  </ul>

  <h2 class="sec"><span class="secnum">2</span>Why it mattered</h2>
  <p>This training is what turned my May–June negative results into a clear next experiment. See
  <a href="../neutrophil_transfer/">project 1.1</a>.</p>''',
[])
render()
print("ok")
