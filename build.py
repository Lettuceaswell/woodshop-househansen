"""Inline the House Hansen marks and the ink log into index.html (no build tools needed)."""
import re
from pathlib import Path

root = Path(__file__).parent

def symbol(file, id):
    body = re.search(r"<svg[^>]*>(.*)</svg>", (root / file).read_text(), re.S).group(1)
    return f'<symbol id="{id}" viewBox="0 0 240 240">{body}</symbol>'

# Size rule (2026-10-23): full cut at 48 px and up, small cut from 24 to 48 px.
marks = symbol("assets/mark.svg", "hh-mark") + symbol("assets/mark-full.svg", "hh-mark-full")
log = (root / "assets/endgrain.svg").read_text()
html = (root / "src.html").read_text().replace("<!--MARK-->", marks).replace("<!--ENDGRAIN-->", log)
(root / "index.html").write_text(html)
print("index.html", len(html), "bytes")
