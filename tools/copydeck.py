"""Copy deck: every line of copy on the site, editable in one page.

  python3 tools/copydeck.py extract          -> pages/YYYY-MM-DD-site-copy.html (open it, edit, Copy my changes)
  python3 tools/copydeck.py apply reply.txt  -> writes the pasted changes into src.html and rebuilds index.html
  (apply also reads the pasted reply from stdin when no file is given)

Extract and apply share one tokenizer, so a line's id is its position in src.html. Apply checks that the
original text is still at that id before replacing it, and falls back to a unique search if src.html moved.
"""
import hashlib, html, json, re, subprocess, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src.html"
PAGES = ROOT / "pages"

SECTION_NAMES = {
    "head": "Browser tab & search preview", "header": "Top bar", "hero": "Hero", "strip": "Status strip",
    "available": "Available now", "calculator": "Lumber calculator", "story": "The mill (dark band)",
    "shop": "From the shop", "order": "Place an order", "footer": "Footer",
}
ATTR_KIND = {"alt": "image description", "aria-label": "screen-reader label", "placeholder": "placeholder", "content": "search preview"}
COMPUTED_IDS = ("c-total", "c-bf")  # filled in by the calculator script
TAG_KIND = {"title": "browser tab", "h1": "headline", "h2": "heading", "h3": "heading", "p": "paragraph", "a": "button",
            "button": "button", "li": "list item", "b": "list item", "label": "form label", "option": "dropdown choice",
            "figcaption": "caption", "blockquote": "quote", "cite": "quote credit", "em": "headline"}


def masked(src):
    """Copy of src with style, script, svg and comments blanked out, same length, so offsets line up."""
    out = src
    for pat in (r"<style\b.*?</style>", r"<script\b.*?</script>", r"<svg\b.*?</svg>", r"<!--.*?-->"):
        out = re.sub(pat, lambda m: " " * len(m.group(0)), out, flags=re.S)
    return out


def sections(src):
    marks = []
    for m in re.finditer(r'<(head|header|footer)\b|<section\b[^>]*?(?:id="([^"]+)"|class="(hero)")|<div class="(strip)"', src):
        marks.append((m.start(), next(g for g in m.groups() if g)))
    return marks


def section_at(marks, pos):
    name = "head"
    for start, key in marks:
        if start > pos:
            break
        name = key
    return name


def tokens(src):
    """Ordered list of editable spans: dict(kind, start, end, raw, section, context)."""
    m_src, marks, found = masked(src), sections(src), []
    for m in re.finditer(r">([^<>]+)<", m_src):
        if "  " * 4 in m.group(1) and not m.group(1).strip():
            continue  # a masked style/script/svg/comment region
        raw = src[m.start(1):m.end(1)]
        core = html.unescape(m.group(1)).strip()
        if not core or re.fullmatch(r"[\d\s.,]+", core):
            continue  # whitespace, or bare numbers (calculator option values)
        tag = src[src.rfind("<", 0, m.start(1)):m.start(1)]
        if any(f'id="{i}"' in tag for i in COMPUTED_IDS):
            continue
        name = re.match(r"</?([a-zA-Z0-9]+)", tag)
        found.append(dict(kind="text", start=m.start(1), end=m.end(1), raw=raw, context=TAG_KIND.get(name.group(1).lower() if name else "", "text")))
    for m in re.finditer(r'\b(alt|aria-label|placeholder)="([^"]+)"|<meta (?:name|property)="(?:description|og:title|og:description)" content="([^"]+)"', m_src):
        g = 2 if m.group(2) is not None else 3
        attr = m.group(1) or "content"
        found.append(dict(kind="attr", start=m.start(g), end=m.end(g), raw=src[m.start(g):m.end(g)], context=ATTR_KIND[attr]))
    found.sort(key=lambda t: t["start"])
    for i, t in enumerate(found):
        t["id"] = i
        t["section"] = section_at(marks, t["start"])
        t["text"] = re.sub(r"\s+", " ", html.unescape(t["raw"])).strip()
    return found


def esc(s):
    return html.escape(s, quote=True)


def build_page(src, toks):
    digest = hashlib.sha1(src.encode()).hexdigest()[:10]
    order = list(SECTION_NAMES)
    groups = {}
    for t in toks:
        groups.setdefault(t["section"], []).append(t)
    secs = []
    for key in sorted(groups, key=lambda k: order.index(k) if k in order else 99):
        rows = "\n".join(
            f'<div class="line" data-id="{t["id"]}"><div class="ctx">{esc(t["context"])}</div>'
            f'<textarea rows="1" data-id="{t["id"]}" data-orig="{esc(t["text"])}" spellcheck="true">{esc(t["text"])}</textarea>'
            f'<div class="was"><span>was:</span> {esc(t["text"])} <button type="button" class="revert">Revert</button></div></div>'
            for t in groups[key])
        secs.append(f'<section id="s-{key}"><h2>{esc(SECTION_NAMES.get(key, key))}</h2>\n{rows}\n</section>')
    tpl = (ROOT / "tools" / "copydeck.template.html").read_text()
    return (tpl.replace("{{DATE}}", date.today().isoformat()).replace("{{COUNT}}", str(len(toks)))
               .replace("{{SECTIONS}}", str(len(secs))).replace("{{DIGEST}}", digest).replace("{{BODY}}", "\n".join(secs)))


def write_index():
    items = sorted(PAGES.glob("20*.html"), reverse=True)
    li = "\n".join(f'<li><a href="{p.name}">{p.stem}</a> <span class="tag">Review</span> <span class="badge">needs your input</span>'
                   f'<br><small>Every line of copy on woodshop.househansen.com, editable.</small></li>' for p in items[:1]) + \
         "\n".join(f'<li><a href="{p.name}">{p.stem}</a> <span class="tag">Review</span></li>' for p in items[1:])
    (PAGES / "index.html").write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Woodshop pages</title>
<style>:root{{--bg:#fafaf9;--text:#1c1917;--muted:#78716c;--accent:#3C7585}}@media (prefers-color-scheme:dark){{:root{{--bg:#0c0a09;--text:#f5f5f4;--muted:#a8a29e;--accent:#5A95A6}}}}
body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}}main{{max-width:760px;margin:0 auto;padding:32px 20px}}
a{{color:var(--accent);font-weight:600}}li{{margin:0 0 14px}}.tag{{font-size:12px;color:var(--muted)}}.badge{{font-size:12px;background:var(--accent);color:#fff;border-radius:999px;padding:2px 8px}}small{{color:var(--muted)}}</style></head>
<body><main><h1>Woodshop pages</h1><ul>{li}</ul></main></body></html>""")


def extract():
    src = SRC.read_text()
    toks = tokens(src)
    PAGES.mkdir(exist_ok=True)
    out = PAGES / f"{date.today().isoformat()}-site-copy.html"
    out.write_text(build_page(src, toks))
    write_index()
    print(f"{len(toks)} lines -> {out}")


def apply(text):
    data = json.loads(text[text.index("{"):text.rindex("}") + 1])
    src = SRC.read_text()
    toks = {t["id"]: t for t in tokens(src)}
    edits, problems = [], []
    for ch in data.get("changes", []):
        t = toks.get(ch["id"])
        if not (t and t["text"] == ch["from"]):
            # src.html moved since the page was made: fall back to a unique match on the old text
            hits = [x for x in toks.values() if x["text"] == ch["from"]]
            if len(hits) != 1:
                problems.append(f'#{ch["id"]} "{ch["from"][:50]}": {"not found" if not hits else "matches %d places" % len(hits)}')
                continue
            t = hits[0]
        lead = t["raw"][:len(t["raw"]) - len(t["raw"].lstrip())]
        trail = t["raw"][len(t["raw"].rstrip()):]
        new = esc(ch["to"]) if t["kind"] == "attr" else html.escape(ch["to"], quote=False)
        edits.append((t["start"], t["end"], lead + new + trail, ch))
    for start, end, new, _ in sorted(edits, key=lambda e: -e[0]):
        src = src[:start] + new + src[end:]
    SRC.write_text(src)
    subprocess.run([sys.executable, str(ROOT / "build.py")], check=True)
    for *_, ch in edits:
        print(f'ok  #{ch["id"]}: "{ch["from"][:40]}" -> "{ch["to"][:40]}"')
    for p in problems:
        print("SKIP", p)
    if data.get("notes"):
        print("notes:", data["notes"])


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "extract"
    if cmd == "extract":
        extract()
    elif cmd == "apply":
        apply(Path(sys.argv[2]).read_text() if len(sys.argv) > 2 else sys.stdin.read())
    else:
        sys.exit(__doc__)
