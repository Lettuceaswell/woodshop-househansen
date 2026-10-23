#!/usr/bin/env bash
# Placeholder art for woodshop.househansen.com, made with the House Hansen pipeline
# (modern-viking-brand/.claude/skills/sketch). Photos: Klein (objects) / RealVis (hands),
# then scripts/grade.sh. Ink spots: Z-Image house hand. Runs land in modern-viking-brand/gen/.
set -u
cd /mnt/g/Projects/modern-viking-brand
P=/mnt/g/ai/tools-venv/bin/python
PHOTO="photograph, 50mm lens, soft overcast daylight, muted natural colors, fine film grain, editorial, no text"
INK="loose confident ink line drawing, hand-drawn pen sketch, black ink on plain white paper, minimal, no color, no text"
run() { tag=$1; shift; echo "== $tag"; $P scripts/comfy.py gen "$@" 2>&1 | grep -E "gen/|Error|error" | tail -2; }

run hero      "a small portable bandsaw sawmill in a clearing of tall Norway pine forest, a fresh-sawn pine log on the mill bed, a neat stack of rough-sawn boards beside it, sawdust on sandy ground, no people, wide shot, lots of quiet empty space, northern Wisconsin" --model klein --n 4 --seed 101 --w 1600 --h 896 --style "$PHOTO"
run sawing    "close-up of a bandsaw sawmill blade cutting through a Norway pine log, a fresh board peeling away, sawdust in the air, bright pale pine wood, no people" --model klein --n 4 --seed 102 --w 1152 --h 864 --style "$PHOTO"
run lumber    "a neat sticker-stacked pile of rough-sawn pine boards drying under a simple board-and-batten shed roof, end grain facing camera, pine trees behind" --model klein --n 4 --seed 103 --w 1152 --h 864 --style "$PHOTO"
run slab      "bundles of split pine slab firewood tied with twine, stacked beside a stone fire ring with a small campfire burning at dusk, pine forest behind, one warm firelight" --model klein --n 4 --seed 104 --w 1152 --h 864 --style "photograph, 50mm lens, dusk, one warm firelight, muted natural colors, fine film grain, editorial, no text"
run chair     "a single Adirondack chair built from weathered reclaimed deck boards standing on a wooden dock at a calm northern lake, pine shoreline, no people" --model klein --n 4 --seed 105 --w 1152 --h 864 --style "$PHOTO"
run table     "a handmade pine farmhouse dining table with a matching bench in a quiet farmhouse room, wide plank floor, plaster wall, light from a north window, minimal, no people" --model klein --n 4 --seed 106 --w 1152 --h 864 --style "$PHOTO"
run vanity    "a handmade rustic pine bathroom vanity with two drawers and a stone vessel sink, plaster wall, daylight from a small window, minimal, no people" --model klein --n 4 --seed 107 --w 1152 --h 864 --style "$PHOTO"
run mantel    "a thick live-edge pine slab mantel shelf above a fieldstone fireplace in a cabin, natural bark edge, soft daylight, minimal, no people" --model klein --n 4 --seed 108 --w 1152 --h 864 --style "$PHOTO"
run barn      "the timber frame of a small horse-barn style wood shop under construction, fresh pine posts and beams on concrete piers, a raised center roof, pine woods behind, overcast, no people" --model klein --n 4 --seed 109 --w 1344 --h 896 --style "$PHOTO"
run hands     "close-up of the weathered hands of an older carpenter running his palm along a fresh-sawn pine board, sawdust on the board, workshop, soft window light, no face" --model sdxl --ckpt RealVisXL_V5.0_fp16.safetensors --n 4 --seed 110 --w 1344 --h 896 --style "$PHOTO"

run ink-log    "the end of a single sawn pine log with growth rings, one subject, lots of white space" --model zimage --n 2 --seed 201 --style "$INK"
run ink-flitch "a single long board with a wavy live bark edge on both sides, one subject, lots of white space" --model zimage --n 2 --seed 202 --style "$INK"
run ink-slab   "a small stack of split firewood with bark, one subject, lots of white space" --model zimage --n 2 --seed 203 --style "$INK"
run ink-chips  "a few curled wood shavings and offcuts, one subject, lots of white space" --model zimage --n 2 --seed 204 --style "$INK"
run ink-barn   "a small timber barn with a raised center roof, one subject, lots of white space" --model zimage --n 2 --seed 205 --style "$INK"
echo DONE

# Round 2 (2026-10-23): rerolls for the axe-test failures in round 1.
# Round 1 mill read as a table saw, sawing close-ups showed handsaws, flitch became skateboards, barn was a gambrel.
run hero2   "a portable band sawmill in a clearing of tall Norway pine forest: a long low steel track lying on the ground, a large pine log clamped on the track, a steel sawhead frame straddling the log with a horizontal band saw blade, a small engine on the sawhead, a stack of fresh rough-sawn boards beside it, sawdust on sandy ground, no people, wide shot, lots of quiet empty space" --model klein --n 4 --seed 111 --w 1600 --h 896 --style "$PHOTO"
run sawing2 "close-up of a horizontal band saw blade on a portable sawmill slicing a thin board off the top of a large pine log lying on a steel track, sawdust spraying from the cut, steel sawhead frame and blade guard visible, no people" --model klein --n 4 --seed 112 --w 1152 --h 864 --style "$PHOTO"
run ink-flitch2 "a single rough-sawn lumber plank lying flat, with wavy natural bark still on both long edges, seen in three-quarter view, one subject, lots of white space" --model zimage --n 2 --seed 206 --style "$INK"
run ink-barn2 "a small timber monitor barn: a tall center section with its own gable roof and a row of small windows, and lower shed roofs on both sides, built from rough boards, one subject, lots of white space" --model zimage --n 2 --seed 207 --style "$INK"
