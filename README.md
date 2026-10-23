# woodshop.househansen.com

Landing page for The Woodshop, Dad's sawmill and woodshop in Trego, WI. One static page, hosted on GitHub Pages.

- Edit `src.html`, then run `python3 build.py`. That inlines the House Hansen mark, the end-grain log, the knot divider and the live-edge bark into `index.html`. Commit both files.
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
- Dad is fine being shown on the site (Levi, 2026-10-23).
- Real footage goes in `raw/` (git-ignored; the phone files carry GPS, so only re-encoded frames and clips are published, with metadata stripped). Real footage is graded with the house LUT plus a green/red tame (`huesaturation`) because the mill is Kelly green and the tractor is orange; the recipe for every file is in `assets/img/SOURCES.txt`. The footer says "Some photos are illustrations" until the AI stand-ins (slab card, furniture cards, ink spots) are replaced.

## Motion and ornament
- All motion sits behind `html.motion`, which is only set when the visitor hasn't asked for reduced motion. Without it the page renders finished and static. One scroll loop at the bottom of `src.html` drives everything scroll-linked.
- **Sketch over stills:** every real photo has an ink tracing (`assets/ink/<name>.webp`). On scroll the ink wipes in over a dark plate, the photo develops under it, and the ink stays on faintly, drifting against the photo (parallax plus pointer). To make one: `systemctl --user start comfyui`, then `python3 tools/lineart.py assets/img/<name>.webp art/lines/<name>.png --coarse`, then `tools/inklayer.sh <name> art/lines/<name>.png <floor%>` (raise the floor for busy foliage). Wrap the image in `<figure class="sketch" data-sketch><div class="plate">photo + ink</div></figure>`.
- **The log:** `assets/endgrain.svg` lives in the Forge band as a pinned diagram. Each step of the "one log" list snaps blue chalk lines on it (slab, flitch, sawdust, timbers and boards). It is sticky on desktop and pinned under the header on phones.
- **Ornament** (`python3 tools/ornament.py`): the knot rule (grain parting around a knot, with one Urnes strand wrapping it, drawn on reveal) and the live-edge bark top and bottom of the Forge band. The thin strand weight is shared with the mark system.
- Also: hero wipe-in, headline word reveals, the price count-up, the rolling calculator total with the board's end grain drawn to scale, the news ticker with knot separators, and the scroll-progress kerf under the header.

## Editing copy
- `python3 tools/copydeck.py extract` writes `pages/YYYY-MM-DD-site-copy.html` (git-ignored, never published): every line of copy, image description and search snippet on the site, editable in place.
- Levi edits, hits **Copy my changes**, pastes the reply to Claude. Claude saves it and runs `python3 tools/copydeck.py apply reply.txt`, which writes each change back to its exact spot in `src.html` and rebuilds `index.html`.
- Re-run `extract` after any layout change so line ids match the current page. `apply` verifies the original text before replacing it and skips anything that moved.
- `_config.yml` keeps tools, art, pages and sources out of the published site.
