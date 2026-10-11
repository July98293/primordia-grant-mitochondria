# Mito Work · Primordia

Static site documenting work on mitochondria funded by a Primordia microgrant.

```
./scripts/serve.sh                 # view at http://localhost:8000
python3 scripts/build_figures.py   # rebuild the project figures
python3 scripts/build_projects.py  # rebuild the project pages
```

- `index.html`: homepage
- `projects/<slug>/index.html`: one generated page per project. Edit `scripts/build_projects.py`, not these
- `projects/<slug>/img/*.svg`: generated figures. Edit `scripts/build_figures.py`
- `assets/css/style.css`, `assets/js/mito_anim.js`, `assets/img/`

Deploys as-is to GitHub Pages (Settings, Pages, branch `main`, root).
