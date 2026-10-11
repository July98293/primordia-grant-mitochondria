# Mito Work · Primordia

Static site documenting work on mitochondria funded by a Primordia microgrant.

```
./scripts/serve.sh                 # view at http://localhost:8000
python3 scripts/build_projects.py  # rebuild project pages after editing the script
```

- `index.html`: homepage
- `projects/<slug>/index.html`: one generated page per project. Edit `scripts/build_projects.py`, not these
- `assets/css/style.css`, `assets/js/mito_anim.js`, `assets/img/`

To add a figure, put it in `projects/<slug>/img/` and replace the placeholder in the build script with
`<img src="img/your_figure.png" alt="...">`.

Deploys as-is to GitHub Pages (Settings, Pages, branch `main`, root).
