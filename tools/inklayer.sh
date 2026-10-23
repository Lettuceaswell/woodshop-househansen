#!/bin/bash
# Lineart PNG (tools/lineart.py) -> oat-light ink on transparent, at the photo's size.
#   tools/inklayer.sh shop [lines-file] [low%]
# low% lifts the floor: higher keeps only confident lines (busy foliage needs 40+).
set -e
cd "$(dirname "$0")/.."
n=$1; lines=${2:-art/lines/$n.png}; low=${3:-30}
wh=$(magick identify -format "%wx%h" assets/img/$n.webp)
mkdir -p assets/ink
magick "$lines" -colorspace gray -resize "$wh!" -level "$low%,88%" -gamma 1.5 /tmp/ink-alpha-$$.png
magick -size "$wh" xc:"#F0E9DA" /tmp/ink-alpha-$$.png -alpha off -compose CopyOpacity -composite \
  -define webp:alpha-quality=70 -quality 80 assets/ink/$n.webp
rm /tmp/ink-alpha-$$.png
ls -la assets/ink/$n.webp | awk '{print $5, $9}'
