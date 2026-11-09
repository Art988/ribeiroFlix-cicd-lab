# RibeiroFlix

RibeiroFlix is a static website built with HTML and CSS.

## CI validation

GitHub Actions validates the site on every push to `main` and on pull requests targeting `main`. The validator checks that `index.html` exists and that local `href` and `src` references in the root HTML pages point to files inside the site.

Run the same validation locally with Python 3.12 or newer:

```bash
python scripts/validate_site.py
```

## Deployment

After validation succeeds on a push to `main`, the workflow publishes the repository contents to GitHub Pages. Pull requests run validation only; they do not deploy.
