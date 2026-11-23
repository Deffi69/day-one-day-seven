#!/bin/bash
# Build the day-one-day-seven TikTok video (1080x1920, 30.0s, with narration).
# Creative: "Kancil Dash" — the same tiny agent-built game, Day 1 vs Day 7.
# Still camera, same map, same start; Day 7 has a week of daily updates.
# Frames: render_game.py (Python + Pillow, deterministic, drawn in-session).
# Narration: 5 Indonesian sentences, synthesized in-session, one voice.
# Music: a low looped bed under the narration.
#
# !!! FINAL STEP (PENDING) — the referral end card !!!
# The video must end with make.fun's referral end card (9:16 transparent
# WebM from the press pack, https://make.fun/press/manifest.json), laid over
# the last 2.5s with referral code eaffd4np typed into its field, per
# https://make.fun/press/llms.txt. That step is NOT run by this script yet:
# the freshly downloaded press files were held for approval in this session,
# so run it separately (from the entry folder) once approved:
#
#   CLIP=repo/video/ad.mp4 CARD=<path to makefun-card-9x16-transparent.webm>
#   FONT=work/JetBrainsMono-Bold.ttf CODE=eaffd4np
#   D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$CLIP")
#   T=$(awk "BEGIN{print $D-2.5}")
#   ffmpeg -y -i "$CLIP" -c:v libvpx-vp9 -i "$CARD" -filter_complex "
#   [0:v]format=yuva420p[base];[base]split[clip][soft];
#   [soft]gblur=sigma=28,eq=saturation=0.35,fade=t=in:st=$T:d=0.8:alpha=1[soft2];
#   [clip][soft2]overlay[bg];
#   [1:v]format=yuva420p,setpts=PTS-STARTPTS+$T/TB[card];
#   [bg][card]overlay=eof_action=pass,
#   drawbox=x=208:y=1230:w=9:h=82:color=white:t=fill:enable='gte(t,22.933)',
#   drawtext=fontfile=$FONT:text=$CODE:fontsize=62:fontcolor=0x191419:x=210:y=1271-(ascent-descent)/2:enable='gte(t,22.933)'[v]" \
#     -map '[v]' -map '0:a' -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac \
#     -movflags +faststart repo/video/ad.mp4
#
# Then verify the last frame shows the code in the white field:
#   ffmpeg -y -v error -sseof -0.1 -i repo/video/ad.mp4 -frames:v 1 work/qa-last.png
set -euo pipefail

E=~/workspace/tools/makefun/entries/post-tiktok-day-one-day-seven-20261123-0327
W=$E/work
A=$W/audio
MUSIC=~/workspace/tools/makefun/entries/bring-the-humans-03/work/music.wav
OUT=$E/repo/video/ad.mp4
mkdir -p "$E/repo/video"

# 1. Frames -> silent clip (30 fps, 900 frames = 30.0 s).
ffmpeg -y -v error -framerate 30 -i "$W/frames/f%04d.png" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart "$W/clip.mp4"

# 2. Narration track: 5 sentences at their start times (durations measured).
#    s1 0.15s (2.21s), s2 2.65s (4.56s), s3 11.05s (2.35s),
#    s4 13.50s (6.05s), s5 26.15s (2.93s).
ffmpeg -y -v error -i "$A/s1.mp3" -i "$A/s2.mp3" -i "$A/s3.mp3" -i "$A/s4.mp3" -i "$A/s5.mp3" \
  -filter_complex "\
[0:a]adelay=150|150[a0];[1:a]adelay=2650|2650[a1];[2:a]adelay=11050|11050[a2];\
[3:a]adelay=13500|13500[a3];[4:a]adelay=26150|26150[a4];\
[a0][a1][a2][a3][a4]amix=inputs=5:normalize=0,apad=whole_dur=30[aout]" \
  -map "[aout]" -t 30 -c:a pcm_s16le "$W/narration.wav"

# 3. Mix narration + low music bed, mux with the clip.
ffmpeg -y -v error -i "$W/clip.mp4" -i "$W/narration.wav" -stream_loop -1 -i "$MUSIC" \
  -filter_complex "[1:a]volume=1.0[narr];[2:a]volume=0.12,atrim=0:30[mus];\
[narr][mus]amix=inputs=2:normalize=0:duration=first[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 160k -t 30 -movflags +faststart "$OUT"

ffprobe -v error -show_entries stream=width,height,r_frame_rate,codec_name \
  -show_entries format=duration,size -of default=nw=1 "$OUT"
echo "BUILT (PRE-CARD) $OUT — end-card step still pending, see header."
