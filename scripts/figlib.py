"""Minimal SVG primitives for the project figures.

Figures are written as standalone .svg files and referenced with <img>, so they
cannot load webfonts. The font stack below falls back to geometric system sans.
"""

FONT = '"Jost","Avenir Next","Futura","Century Gothic",system-ui,sans-serif'
INK = "#3a3fb8"
DARK = "#16152b"
MUTED = "#5f5d7a"
UP = "#7d5ff0"
DOWN = "#3f8fd4"
FLAT = "#a9a4c0"

STYLE = f"""  <style>
    text {{ font-family: {FONT}; fill: #24233a; }}
    .t  {{ font-size: 15px; font-weight: 600; fill: {DARK}; }}
    .s  {{ font-size: 13px; }}
    .xs {{ font-size: 11.5px; fill: {MUTED}; }}
    .num {{ font-size: 13px; font-weight: 600; fill: {DARK}; }}
    .box {{ fill: #ece7f8; stroke: {INK}; stroke-width: 2; }}
    .boxw {{ fill: #faf8ff; stroke: {INK}; stroke-width: 2; }}
    .dash {{ fill: none; stroke: {INK}; stroke-width: 2; stroke-dasharray: 6 5; }}
    .arr {{ fill: none; stroke: {INK}; stroke-width: 2; marker-end: url(#a); }}
    .ax {{ stroke: #8b87a8; stroke-width: 1.5; }}
    .gl {{ stroke: #ded9ec; stroke-width: 1; }}
  </style>
  <defs>
    <marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 Z" fill="{INK}"/>
    </marker>
  </defs>"""


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def svg(w, h, body, title, desc=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="ti de">\n'
            f'  <title id="ti">{esc(title)}</title>\n  <desc id="de">{esc(desc or title)}</desc>\n'
            f'{STYLE}\n{body}\n</svg>\n')


def wrap(text, width):
    """Greedy wrap into lines of at most `width` characters."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur); cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines


def label(x, y, text, cls="s", anchor="middle", width=18, lh=15):
    lines = wrap(text, width)
    y0 = y - (len(lines) - 1) * lh / 2
    out = []
    for i, ln in enumerate(lines):
        out.append(f'<text class="{cls}" x="{x}" y="{y0 + i * lh:.1f}" text-anchor="{anchor}" '
                   f'dominant-baseline="middle">{esc(ln)}</text>')
    return "\n".join(out)


def box(x, y, w, h, text, cls="box", tcls="s", width=16, r=12, sub=None):
    out = [f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>']
    cy = y + h / 2 - (6 if sub else 0)
    out.append(label(x + w / 2, cy, text, tcls, width=width))
    if sub:
        out.append(label(x + w / 2, y + h - 16, sub, "xs", width=width + 6, lh=13))
    return "\n".join(out)


def arrow(x1, y1, x2, y2):
    return f'<path class="arr" d="M {x1},{y1} L {x2},{y2}"/>'


def chain(items, x, y, bw, bh, gap, width=16):
    """A left-to-right chain of boxes joined by arrows."""
    out = []
    for i, it in enumerate(items):
        bx = x + i * (bw + gap)
        text, sub = (it if isinstance(it, tuple) else (it, None))
        out.append(box(bx, y, bw, bh, text, width=width, sub=sub))
        if i:
            out.append(arrow(bx - gap + 2, y + bh / 2, bx - 6, y + bh / 2))
    return "\n".join(out)


def caption(x, y, text, width=90):
    return label(x, y, text, "xs", anchor="start", width=width, lh=14)
