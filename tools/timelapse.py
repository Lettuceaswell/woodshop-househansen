#!/usr/bin/env python3
"""Barn timelapse prep: raw Brinno TLC300 clips -> one cleaned clip per day + a Kdenlive project.

    python3 tools/timelapse.py            # process new clips, rebuild the project
    python3 tools/timelapse.py --force    # reprocess every clip

Input:  raw/barn-timelapse/TLC*.MP4 (camera: one file per day, a frame every 2 min, 06:00-18:58 camera clock)
Output: raw/barn-timelapse/edit/days/YYYY-MM-DD[-b].mp4  daylight frames only, timestamp bar cropped off,
                                                         deflickered, 1080p30, one camera frame per video frame
        raw/barn-timelapse/edit/barn-timelapse.kdenlive  every day in date order on one video track

Edit in Kdenlive: delete days with no progress, trim, then speed up the track or the whole
sequence (right-click clip > Change Speed) and render.
"""
import datetime as dt
import json
import pathlib
import re
import subprocess
import sys
import uuid

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "raw" / "barn-timelapse"
EDIT = RAW / "edit"
DAYS = EDIT / "days"
BRIGHT = 55          # mean luma (0-255) a frame needs to count as daylight
FPS = 30


def luma(clip):
    out = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(clip), "-vf",
         "scale=64:36,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-",
         "-f", "null", "-"], capture_output=True, text=True, check=True).stdout
    return [float(v) for v in re.findall(r"YAVG=([\d.]+)", out)]


def day_name(clip, taken):
    # FAT mtime from the camera lands ~6 h early; the clip's date is that of its frames.
    d = (dt.datetime.fromtimestamp(clip.stat().st_mtime) + dt.timedelta(hours=6)).date().isoformat()
    name = d
    n = 1
    while name in taken:
        n += 1
        name = f"{d}-{chr(ord('a') + n - 1)}"
    taken.add(name)
    return name


def process(clip, out):
    y = luma(clip)
    lit = [i for i, v in enumerate(y) if v >= BRIGHT]
    if not lit:
        return None
    a, b = lit[0], lit[-1]
    vf = (f"trim=start_frame={a}:end_frame={b + 1},setpts=N/{FPS}/TB,"
          "crop=1848:1040:36:0,scale=1920:1080:flags=lanczos,"
          "deflicker=size=5:mode=pm,format=yuv420p")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(clip), "-an", "-vf", vf, "-r", str(FPS),
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-g", "10",
         "-movflags", "+faststart", str(out)], check=True)
    return b + 1 - a


def frames(path):
    return int(subprocess.run(
        ["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v",
         "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True).stdout.strip())


def project(days):
    """Minimal Kdenlive 25+/26 project: one video track, one empty audio track, days in order."""
    seq = "{" + str(uuid.uuid4()) + "}"
    total = sum(n for _, n in days)
    x = ['<?xml version="1.0" encoding="utf-8"?>',
         f'<mlt LC_NUMERIC="C" version="7.22.0" producer="main_bin" root="{EDIT}">',
         f'  <profile description="HD 1080p 30 fps" width="1920" height="1080" progressive="1" '
         f'sample_aspect_num="1" sample_aspect_den="1" display_aspect_num="16" display_aspect_den="9" '
         f'frame_rate_num="{FPS}" frame_rate_den="1" colorspace="709"/>',
         f'  <producer id="black" in="0" out="{total - 1}">',
         '    <property name="length">2147483647</property>',
         '    <property name="eof">continue</property>',
         '    <property name="resource">black</property>',
         '    <property name="mlt_service">color</property>',
         '    <property name="kdenlive:playlistid">black_track</property>',
         '    <property name="mlt_image_format">rgba</property>',
         '  </producer>']

    def chain(cid, kid, name, n, bin_=False):
        return [f'  <chain id="{cid}" out="{n - 1}">',
                f'    <property name="length">{n}</property>',
                f'    <property name="resource">days/{name}.mp4</property>',
                '    <property name="mlt_service">avformat-novalidate</property>',
                '    <property name="audio_index">-1</property>',
                '    <property name="video_index">0</property>',
                f'    <property name="kdenlive:id">{kid}</property>',
                f'    <property name="kdenlive:clipname">{name}</property>',
                '    <property name="kdenlive:clip_type">2</property>' if bin_ else
                '    <property name="set.test_audio">1</property>',
                '  </chain>']

    # timeline instances
    for k, (name, n) in enumerate(days):
        x += chain(f"t{k}", k + 2, name, n)
    # audio track (empty)
    x += ['  <playlist id="a0"><property name="kdenlive:audio_track">1</property></playlist>',
          '  <playlist id="a1"><property name="kdenlive:audio_track">1</property></playlist>',
          f'  <tractor id="audio" in="0" out="{total - 1}">',
          '    <property name="kdenlive:audio_track">1</property>',
          '    <property name="kdenlive:timeline_active">1</property>',
          '    <track producer="a0" hide="video"/>', '    <track producer="a1" hide="video"/>',
          '  </tractor>']
    # video track
    x.append('  <playlist id="v0">')
    for k, (name, n) in enumerate(days):
        x.append(f'    <entry producer="t{k}" in="0" out="{n - 1}">'
                 f'<property name="kdenlive:id">{k + 2}</property></entry>')
    x += ['  </playlist>', '  <playlist id="v1"/>',
          f'  <tractor id="video" in="0" out="{total - 1}">',
          '    <property name="kdenlive:trackname">Barn</property>',
          '    <property name="kdenlive:timeline_active">1</property>',
          '    <track producer="v0" hide="audio"/>', '    <track producer="v1" hide="audio"/>',
          '  </tractor>']
    # bin instances
    for k, (name, n) in enumerate(days):
        x += chain(f"b{k}", k + 2, name, n, bin_=True)
    x += [f'  <tractor id="{seq}" in="0" out="{total - 1}">',
          f'    <property name="kdenlive:uuid">{seq}</property>',
          '    <property name="kdenlive:clipname">Barn timelapse</property>',
          '    <property name="kdenlive:sequenceproperties.groups">[]</property>',
          '    <property name="kdenlive:sequenceproperties.hasAudio">0</property>',
          '    <property name="kdenlive:sequenceproperties.hasVideo">1</property>',
          '    <property name="kdenlive:sequenceproperties.tracksCount">2</property>',
          '    <property name="kdenlive:producer_type">17</property>',
          '    <track producer="black"/>', '    <track producer="audio"/>',
          '    <track producer="video"/>', '  </tractor>',
          '  <playlist id="main_bin">',
          f'    <property name="kdenlive:docproperties.uuid">{seq}</property>',
          f'    <property name="kdenlive:docproperties.opensequences">{seq}</property>',
          f'    <property name="kdenlive:docproperties.activetimeline">{seq}</property>',
          '    <property name="kdenlive:docproperties.version">1.1</property>',
          '    <property name="kdenlive:docproperties.profile">atsc_1080p_30</property>',
          '    <property name="xml_retain">1</property>',
          f'    <entry producer="{seq}" in="0" out="0"/>']
    x += [f'    <entry producer="b{k}" in="0" out="{n - 1}"/>' for k, (_, n) in enumerate(days)]
    x += ['  </playlist>',
          f'  <tractor id="root" in="0" out="{total - 1}">',
          '    <property name="kdenlive:projectTractor">1</property>',
          f'    <track producer="{seq}" in="0" out="{total - 1}"/>', '  </tractor>', '</mlt>']
    return "\n".join(x) + "\n"


def main():
    force = "--force" in sys.argv
    DAYS.mkdir(parents=True, exist_ok=True)
    index_path = EDIT / "index.json"
    index = json.loads(index_path.read_text()) if index_path.exists() else {}
    taken = set()
    for clip in sorted(RAW.glob("TLC*.MP4")):
        name = index.get(clip.name) or day_name(clip, taken)
        taken.add(name)
        out = DAYS / f"{name}.mp4"
        if out.exists() and not force:
            index[clip.name] = name
            continue
        n = process(clip, out)
        print(f"{clip.name} -> {name}: {n or 0} daylight frames", flush=True)
        if n:
            index[clip.name] = name
    index_path.write_text(json.dumps(index, indent=1) + "\n")
    days = [(p.stem, frames(p)) for p in sorted(DAYS.glob("*.mp4"))]
    (EDIT / "barn-timelapse.kdenlive").write_text(project(days))
    secs = sum(n for _, n in days) / FPS
    print(f"{len(days)} days, {secs / 60:.1f} min at 1x -> {EDIT / 'barn-timelapse.kdenlive'}")


if __name__ == "__main__":
    main()
