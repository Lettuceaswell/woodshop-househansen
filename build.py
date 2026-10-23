"""Inline the House Hansen mark and the end-grain log into index.html (no build tools needed)."""
import re
from pathlib import Path

root = Path(__file__).parent
mark = (root / "assets/mark.svg").read_text()
paths = re.search(r"<svg[^>]*>(.*)</svg>", mark, re.S).group(1)
symbol = f'<symbol id="hh-mark" viewBox="0 0 240 240">{paths}</symbol>'
log = (root / "assets/endgrain.svg").read_text()
html = (root / "src.html").read_text().replace("<!--MARK-->", symbol).replace("<!--ENDGRAIN-->", log)
(root / "index.html").write_text(html)
print("index.html", len(html), "bytes")
