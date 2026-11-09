"""Validate the static site's HTML pages and local file references."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(ROOT.glob("*.html"))


class LocalReferenceParser(HTMLParser):
    """Collect href and src attributes from an HTML document."""

    def __init__(self):
        super().__init__()
        self.references = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.references.append((name, value.strip()))


def main():
    if not HTML_FILES:
        raise SystemExit("Validation failed: no HTML pages found.")
    if not (ROOT / "index.html").is_file():
        raise SystemExit("Validation failed: index.html is missing.")

    failures = []
    checked = 0

    for html_file in HTML_FILES:
        parser = LocalReferenceParser()
        parser.feed(html_file.read_text(encoding="utf-8"))

        for attribute, reference in parser.references:
            parsed = urlsplit(reference)
            if parsed.scheme or parsed.netloc or reference.startswith("#"):
                continue

            local_path = unquote(parsed.path)
            if not local_path:
                continue

            target = (html_file.parent / local_path).resolve()
            if target != ROOT and ROOT not in target.parents:
                failures.append(
                    f"{html_file.relative_to(ROOT)}: reference escapes site root: {reference}"
                )
                continue

            checked += 1
            if not target.is_file():
                failures.append(
                    f"{html_file.relative_to(ROOT)}: missing {attribute} target: {reference}"
                )

    if failures:
        print("Static site validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print(
        f"Static site validation passed: {len(HTML_FILES)} HTML pages "
        f"and {checked} local references checked."
    )


if __name__ == "__main__":
    main()
