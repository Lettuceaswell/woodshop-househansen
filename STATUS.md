# Status: woodshop.househansen.com
Last session: 2026-10-23. Read this first next time.

## Where it stands
- **Site:** one static page (`src.html` → `python3 build.py` → `index.html`) on GitHub Pages, repo `Lettuceaswell/woodshop-househansen`, branch `main`. Follows the House Hansen system in `../modern-viking-brand` (tokens, Quiet weighting, imprint rule, mark size rule, ink-sketch illustrations, wool grain). Rules are summarized in `README.md`.
- **Name and imprint:** the site is "Hansen Woodshop" (renamed from "The Woodshop" by Levi, 2026-10-23). "House Hansen" appears only in the footer imprint. The link-preview image `assets/og.jpg` still shows the old "The Woodshop" lockup.
- **Live at the domain over HTTP** (CNAME in place, DNS verified 2026-10-23). GitHub had not issued the HTTPS certificate yet that evening. Once it exists, run `gh api -X PUT repos/Lettuceaswell/woodshop-househansen/pages -F https_enforced=true`. If it is still missing after a day, remove and re-add the custom domain in Pages settings to restart issuance.
- **Motion pass (2026-10-23):** ink tracings over every real photo, scroll parallax, the end-grain log back as a pinned "how we open a log" diagram, the knot-rule dividers, the live-edge Forge band, and more. See README, "Motion and ornament".
- **noindex is on** and the **order form is a placeholder** (confirms on screen, sends nothing). Don't share the link publicly until the form goes somewhere real. Then remove the `robots` meta tag.
- **Preview locally:** `python3 -m http.server 8790 --bind 127.0.0.1` in this folder → http://127.0.0.1:8790/

## Content
- **Real footage (Levi's 4K clips in `raw/`, git-ignored, phone files carry GPS):** hero loop (IMG_4905, 60 fps, half speed), custom sawing card (4896), lumber card (4900), Dad at the log pile in the Forge band (4852), Dad's portrait by his quote (4852), Dad at the miter saw (4827, 24 fps), and the mill redrawn as ink (4893 via Klein). Recipes are in `assets/img/SOURCES.txt`.
- **Still AI placeholders:** slab/campfire card, the four furniture cards (chair, table, vanity, mantel), the five small ink spots on the "One log" list. The footer says "Some photos are illustrations" until these are replaced.
- **Unused real footage:** 4892 (tractor carrying a log off the pile, very red), 4901 (slow push toward the log pile), 4906 (macro of a board), and the saw-shed still (`assets/img/shed.webp`, off the page).
- **Grading:** real footage = green/red `huesaturation` tame + `house-natural-hald.png` LUT; Forge band = `grade.sh forge`. The mill is Kelly green and the tractor orange. Always tame them.
- Dad is fine being shown on the site (Levi, 2026-10-23). The quote is credited to "The sawyer" until Dad picks a name.

## Copy
- `python3 tools/copydeck.py extract` → `pages/YYYY-MM-DD-site-copy.html` (local only). Levi edits, pastes the reply, then save it to a file and run `python3 tools/copydeck.py apply reply.txt`. Re-run extract after layout changes.
- **Prices now live in `monetization-wt/wood-first-sale/ideas/dad-concrete-barn-sawmill/first-sale/price-book.md`** (Dad sent real prices 2026-10-23; each line is marked Dad's or placeholder). The site was synced to it 2026-10-23: Dad's prices plus placeholders. The printed price sheet and listings were not.
- Furniture prices are placeholders: chair $325 and table $895 are from Etsy comps, vanity $650 and shelf $85 are guesses. 

## Next, in order
1. Enforce HTTPS once GitHub issues the cert, and switch the `og:url`/`og:image` tags in `src.html` to https. Levi reacts to the motion pass.
2. Dad settles the open price notes (sawing rule, biochar label, siding, bundle sizes). Update the price book first, then site, calculator `PIECE` table, price sheet and listings together.
3. Wire the order form to a real inbox (text or email), then remove noindex.
4. Replace AI placeholders with real photos: slab bundle, anything Dad has built.
5. Optional: second motion moment from 4900 pan or 4906 macro; Lighthouse pass on mobile.

## Open questions for Levi
- Dad's name for the quote credit.
- Where order requests should go once wired (phone number or email to publish).
