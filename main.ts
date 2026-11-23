// day-one-day-seven entry (Node 22, standard library only).
//
// The entry is the video itself: a 30-second vertical TikTok video about the
// same tiny agent-built game — "Kancil Dash" — on the day it was made and
// after a week of daily updates, posted publicly on TikTok, whose address
// VIDEO.json names. The house reads the video's views, likes, comments,
// shares and saves from TikTok; places go by score (views + 10x the rest).
//
// This program reproduces the entry's deliverables deterministically: it
// copies VIDEO.json and the finished video (video/ad.mp4) from the repository
// to the grader's output directory, byte for byte. No network, no clock, no
// randomness: two runs produce identical output files.
//
// The video: a still camera on the same map, same start — Day 1, the bare
// game (run, jump, one log), then Day 7 after seven daily updates (coins,
// birds, hills, flowers, particles, score popups) — closing on the newer
// build being played and a line inviting viewers to start theirs at
// make.fun, ending with make.fun's referral end card carrying referral code
// eaffd4np. The game itself is in game/kancil-dash.html (?day=1 / ?day=7).
// build_video.sh + work/render_game.py show exactly how the video was
// rendered (ffmpeg, from frames drawn in this session; narration in
// Indonesian, generated in this session).
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from 'node:crypto';
import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const FILES: Array<[string, string]> = [
  ['VIDEO.json', 'VIDEO.json'],
  ['video/ad.mp4', 'ad.mp4'],
];

function sha256Hex(path: string): string {
  return createHash('sha256').update(readFileSync(path)).digest('hex');
}

mkdirSync(OUTPUT_DIR, { recursive: true });
for (const [source, dest] of FILES) {
  const from = join(BOT_DIR, source);
  const to = join(OUTPUT_DIR, dest);
  copyFileSync(from, to);
  const { size } = statSync(to);
  console.log(`copied ${source} -> ${dest} (${size} bytes, sha256 ${sha256Hex(to)})`);
}

// The gate reads the video's address from VIDEO.json: fail loudly, instead
// of handing it a malformed file, when the JSON is broken or has no url.
const video = JSON.parse(readFileSync(join(OUTPUT_DIR, 'VIDEO.json'), 'utf8')) as unknown;
if (typeof video !== 'object' || video === null || typeof (video as { url?: unknown }).url !== 'string') {
  console.error('VIDEO.json must be an object with a string "url" field');
  process.exit(1);
}
console.log(`VIDEO.json url: ${(video as { url: string }).url || '(not posted yet)'}`);
