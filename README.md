# woodshop.househansen.com

Landing page for The Woodshop, Dad's sawmill and woodshop in Trego, WI. One static page, hosted on GitHub Pages.

- Edit `src.html`, then run `python3 build.py`. That inlines the House Hansen mark and the end-grain log into `index.html`. Commit both files.
- Prices match `monetization/ideas/dad-concrete-barn-sawmill/first-sale/` (2026-10-23).
- **The order form is a placeholder**: it confirms on screen and sends nothing. Before going public, wire it to a real inbox and remove `<meta name="robots" content="noindex">`.
- Follows the House Hansen system in `modern-viking-brand/`:
  - `assets/tokens.css` is a verbatim copy of `tokens/tokens.css`. Re-copy it when the palette changes; never edit it here.
  - Quiet weighting (oat 72 / charcoal 20 / woad 6 / auburn 2). Auburn only on the eyebrow strand. Forge band for the story.
  - Imprint rule: the site is "The Woodshop"; "House Hansen" appears once, in the footer imprint. A child mark can replace the H later.
  - Mark size rule: full cut (`mark-full.svg`) at 48 px and up, small cut (`mark.svg`) from 24 to 48 px.
  - Illustration is the on-screen ink sketch voice: charcoal line, no fills (`assets/endgrain.svg`, drawn in on load, static under reduced motion).
  - Wool grain on the page ground only, never on cards. Small text on blue goes on deep fjord; button labels on woad are 19 px semibold.
- DNS: Porkbun, CNAME `woodshop` → `lettuceaswell.github.io`.

## Images
- `assets/img/` holds placeholder art from the House Hansen pipeline (`modern-viking-brand/.claude/skills/sketch`). Photos: Flux Klein (objects) and RealVis (hands), graded with `scripts/grade.sh natural` (hands: `forge`). Ink spots: Z-Image house hand, finished in oat ink. `art/shots.sh` regenerates every run; `assets/img/SOURCES.txt` maps each file to its run and seed.
- Real footage goes in `raw/` (git-ignored). Real photos replace the placeholders one for one, same file names. The footer says "Some photos are illustrations" until they're all real.
