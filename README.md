# woodshop.househansen.com

Landing page for Dad's sawmill and woodshop in Trego, WI. One static page, hosted on GitHub Pages.

- Edit `src.html`, then run `python3 build.py`. That inlines the House Hansen mark and the end-grain log into `index.html`. Commit both files.
- Prices match `monetization/ideas/dad-concrete-barn-sawmill/first-sale/` (2026-10-23).
- **The order form is a placeholder**: it confirms on screen and sends nothing. Before going public, wire it to a real inbox and remove `<meta name="robots" content="noindex">`.
- Brand tokens and mark come from `modern-viking-brand/` (tokens/tokens.css, approvals/portal/final/househansen-mark-small.svg).
- DNS: Porkbun, CNAME `woodshop` → `lettuceaswell.github.io`.
