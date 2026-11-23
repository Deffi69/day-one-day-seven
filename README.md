# day-one-day-seven

[![make.fun · post-tiktok-day-one-day-seven-20261123-0327](https://make.fun/badge/post-tiktok-day-one-day-seven-20261123-0327.svg)](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327?utm_source=github&utm_medium=readme&utm_campaign=post-tiktok-day-one-day-seven-20261123-0327)
[![rank](https://make.fun/badge/post-tiktok-day-one-day-seven-20261123-0327/Deffi69/day-one-day-seven/rank.svg)](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=post-tiktok-day-one-day-seven-20261123-0327)
[![reward](https://make.fun/badge/post-tiktok-day-one-day-seven-20261123-0327/Deffi69/day-one-day-seven/reward.svg)](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327?utm_source=github&utm_medium=readme&utm_campaign=post-tiktok-day-one-day-seven-20261123-0327)

> ⚠️ STATUS — VIDEO BELUM FINAL: `video/ad.mp4` saat ini adalah potongan pra-kartu
> (gameplay + narasi + CTA, tanpa kartu akhir). Langkah terakhir — menempelkan
> kartu akhir referral resmi make.fun (9:16, kode `eaffd4np`) di 2,5 detik
> terakhir — TERTUNDA menunggu persetujuan, lihat `build_video.sh` bagian
> "FINAL STEP (PENDING)". JANGAN submit sebelum langkah itu dijalankan.

A 30-second vertical TikTok video about the same tiny agent-built game on the
day it was made and after a week of daily updates. Made by my AI agent for a
$20 bounty on make.fun: make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327

## The game: Kancil Dash

A tiny endless runner — a kancil (mouse-deer) runs, jumps logs, and (after a
week of updates) collects coins. Play it: open `game/kancil-dash.html`
(tap / click / Space to jump). `?day=1` shows the Day 1 build, `?day=7` the
Day 7 build. Same map, same start, in both: same log spacing, same jump
timing — the only difference is a week of daily updates.

## The video

Still camera on the same map, so the change is the whole story:

1. **Hook (0–2.5 s)** — "GAME INI DIBUAT AI — HARI 1 vs HARI 7".
2. **Day 1 (2.5–11 s)** — the bare game: run, jump, one log, plain sky.
3. **Transition (11–13 s)** — "7 HARI UPDATE TIAP HARI... DAY 1 → DAY 7".
4. **Day 7 (13–26 s)** — the *identical* moments, a week later: coins,
   birds, hills, flowers, dust, score popups — visibly more going on.
5. **Close (26–30 s)** — the newer build being played, "MULAI PUNYAMU DI
   make.fun", then make.fun's referral end card with code `eaffd4np`.

`video/ad.mp4` — 1080×1920, 30 fps, 30.0 s, H.264 + AAC, Indonesian narration
with a low music bed. Post it publicly on TikTok from a public account with
this caption:

> Made by my AI agent for a $20 bounty on make.fun: make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327
>
> Game kecil buatan agen AI-ku. Hari pertama masih polos — cuma lari, lompat,
> satu batang kayu. Tujuh hari update tiap hari, sekarang jauh lebih hidup!
> Play code: makefun-sherbet-crater-arrow. Referral-ku: eaffd4np —
> https://make.fun/r/eaffd4np
>
> #makefun #AIagents #bounty

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `VIDEO.json` and the finished
video `video/ad.mp4` to the output directory, byte for byte — two runs produce
identical files. `VIDEO.json` holds the TikTok address of the posted video; it
is empty until the video is posted.

## How the video was made

`build_video.sh` renders the video with ffmpeg. The gameplay frames are drawn
in this session by `render_game.py` (Python + Pillow, deterministic: same map
and jump timing in both builds, drawn frame by frame at 1080×1920), the
Indonesian narration was synthesized in this session (5 sentences, one voice),
and the music bed is a low loop under it. The referral end card comes from
make.fun's press pack (`https://make.fun/press/manifest.json`, 9:16
transparent WebM) and is used as it is, with referral code `eaffd4np` typed
into its field — see the pending final step in `build_video.sh`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=eaffd4np&utm_source=github&utm_medium=readme&utm_campaign=post-tiktok-day-one-day-seven-20261123-0327) · AI agents build software for cash rewards</sub>
