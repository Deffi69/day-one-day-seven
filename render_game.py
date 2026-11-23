#!/usr/bin/env python3
"""Render 'Kancil Dash' gameplay frames for the Day one, day seven TikTok video.
Same map, same start, both builds: Day 1 (bare) vs Day 7 (a week of daily updates).
Camera still (fixed viewport); the world scrolls. 1080x1920, 30 fps, 900 frames.
World: speed 12 px/frame, ground y=1450, kancil x=270. Jump: vy0=44, g=2.6.
Logs at world x = 1200 + i*1300 (same in both builds). Coins above each log (Day 7).
Segments: A hook 0-74 (day7), B day1 75-329 (world 0-254), C transition 330-389,
D day7 390-779 (world 0-389), E CTA 780-899 (world 390-509).
"""
import math, os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 30
GROUND = 1450
KX = 270
SPEED = 12
LOG_W, LOG_H = 92, 128
LOG_X0, LOG_GAP = 1200, 1300
VY0, G = 44.0, 2.6
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")
FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Inter-Bold.otf")

def font(sz):
    return ImageFont.truetype(FONT, sz)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def vgrad(d, top, bot):
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(top, bot, y / H))

# --- world state for a given world-frame f (same for both builds) ---
def jump_height(f):
    """Kancil height above ground-rest at world frame f (0 when not jumping)."""
    h = 0.0
    air_until = -1
    for i in range(12):
        lx0 = LOG_X0 + i * LOG_GAP
        trig = (lx0 - 240 - KX) / SPEED  # frame when jump triggers
        if f < trig:
            break
        t = f - trig
        air = 2 * VY0 / G
        if t < air:
            return VY0 * t - 0.5 * G * t * t
    return 0.0

def log_screen_x(i, dist):
    return LOG_X0 + i * LOG_GAP - dist

def draw_kancil(d, x, y, f, jumping):
    """y = feet baseline (ground contact). Body rides above the legs."""
    body_c = (139, 90, 43)
    # tail
    d.polygon([(x - 64, y - 52), (x - 92, y - 72), (x - 84, y - 44)], fill=body_c)
    # body (bottom at y-30, clear of the ground)
    d.ellipse([x - 68, y - 118, x + 68, y - 30], fill=body_c)
    # head
    d.ellipse([x + 30, y - 150, x + 90, y - 90], fill=body_c)
    # ear
    d.polygon([(x + 44, y - 144), (x + 52, y - 172), (x + 64, y - 144)], fill=body_c)
    # eye
    d.ellipse([x + 66, y - 128, x + 78, y - 116], fill=(255, 255, 255))
    d.ellipse([x + 69, y - 125, x + 76, y - 118], fill=(18, 34, 51))
    # belly patch
    d.ellipse([x - 30, y - 92, x + 30, y - 48], fill=(196, 148, 96))
    # legs (visible below the body; alternating lift while running)
    phase = math.sin(f * 0.55)
    for i, lx in enumerate((-44, -12, 16, 40)):
        lift = 0 if jumping else (20 if (phase > 0) == (i % 2 == 0) else 0)
        top = y - 52
        bot = y + 2 - (16 if jumping else lift)
        d.rectangle([x + lx - 7, top, x + lx + 7, bot], fill=body_c)

def draw_world(f, day):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img, "RGBA")
    dist = f * SPEED
    ky = GROUND - 104 - jump_height(f)  # feet baseline (body centre offset)
    jumping = jump_height(f) > 0
    if day == 1:
        vgrad(d, (191, 227, 240), (232, 246, 250))
    else:
        vgrad(d, (255, 217, 160), (255, 246, 224))
        # sun
        d.ellipse([820, 120, 960, 260], fill=(255, 207, 77))
        # clouds (parallax 0.3)
        for i in range(3):
            cx = ((i * 520 - dist * 0.3) % 1400 + 1400) % 1400 - 160
            cy = 180 + i * 110
            d.ellipse([cx, cy, cx + 150, cy + 56], fill=(255, 255, 255))
            d.ellipse([cx + 60, cy - 26, cx + 190, cy + 40], fill=(255, 255, 255))
        # hills (parallax 0.5)
        for i in range(5):
            hx = ((i * 560 - dist * 0.5) % 1700 + 1700) % 1700 - 300
            d.pieslice([hx - 260, GROUND - 260, hx + 260, GROUND + 260], 180, 360,
                       fill=(143, 203, 122))
        # birds
        for i in range(2):
            bx = ((i * 840 + f * 4.4) % 1400) - 160
            by = 300 + i * 120 + math.sin(f * 0.09 + i) * 20
            d.arc([bx - 24, by - 18, bx + 24, by + 18], 200, 340, fill=(18, 34, 51), width=5)
            d.arc([bx - 24, by - 18, bx + 24, by + 18], 20, 160, fill=(18, 34, 51), width=5)
    # ground
    d.rectangle([0, GROUND, W, H], fill=(124, 184, 92) if day == 1 else (93, 162, 68))
    d.rectangle([0, GROUND, W, GROUND + 16], fill=(106, 168, 79) if day == 1 else (76, 138, 56))
    if day == 7:
        # flowers + grass tufts
        for i in range(16):
            fx = ((i * 194 - dist) % 1240 + 1240) % 1240 - 80
            fy = GROUND + 70 + (i % 3) * 110
            d.ellipse([fx - 10, fy - 10, fx + 10, fy + 10], fill=(255, 143, 179))
            d.ellipse([fx - 3, fy - 3, fx + 3, fy + 3], fill=(255, 207, 77))
    # logs (same map both days)
    for i in range(12):
        lx = log_screen_x(i, dist)
        if lx < -140 or lx > W + 140:
            continue
        d.rectangle([lx, GROUND - LOG_H, lx + LOG_W, GROUND], fill=(107, 68, 35))
        d.rectangle([lx - 8, GROUND - LOG_H - 16, lx + LOG_W + 8, GROUND - LOG_H], fill=(139, 90, 43))
        d.line([lx + 20, GROUND - LOG_H + 10, lx + 20, GROUND - 10], fill=(90, 56, 28), width=4)
    # coins (day 7) + popups
    popups = []
    if day == 7:
        for i in range(12):
            lx0 = LOG_X0 + i * LOG_GAP
            for k, (dx, ch) in enumerate(((10, 280), (46, 350), (82, 280))):
                cx = lx0 + dx - dist
                cy = GROUND - 104 - ch
                if cx < -30 or cx > W + 30:
                    continue
                # collected?
                if abs(cx - KX) < 55 and abs(cy - ky) < 80:
                    popups.append((cx, cy))
                    continue
                # skip coins already passed
                if cx < KX - 55:
                    continue
                r = 22
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 207, 77),
                          outline=(201, 147, 10), width=4)
                d.text((cx, cy), "$", font=font(26), fill=(160, 110, 0), anchor="mm")
        for (px, py) in popups:
            d.text((px, py - 60), "+10", font=font(52), fill=(255, 207, 77),
                   anchor="mm", stroke_width=3, stroke_fill=(120, 80, 0))
    # dust puffs (day 7)
    if day == 7 and not jumping and f % 5 == 0:
        for k in range(3):
            px = KX - 70 - k * 26
            py = GROUND - 8 - k * 6
            d.ellipse([px - 12, py - 12, px + 12, py + 12], fill=(255, 255, 255, 110))
    # ground shadow under the kancil (shrinks/fades while airborne)
    jh = jump_height(f)
    sh_a = max(25, int(85 - jh * 0.22))
    sh_rx = max(30, int(72 - jh * 0.09))
    d.ellipse([KX - sh_rx, GROUND + 4, KX + sh_rx, GROUND + 26], fill=(0, 0, 0, sh_a))
    draw_kancil(d, KX, ky + 104, f, jumping)
    return img, d

def pill(d, text, xy, bg, fg):
    f = font(46)
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x, y = xy
    d.rounded_rectangle([x, y, x + tw + 44, y + th + 30], radius=40, fill=bg)
    d.text((x + 22, y + 15), text, font=f, fill=fg)

def hud(img, day, f):
    d = ImageDraw.Draw(img, "RGBA")
    dist = f * SPEED
    score = int(dist / 50)
    coins = 0
    if day == 7:
        for i in range(12):
            lx0 = LOG_X0 + i * LOG_GAP
            for dx, ch in ((10, 280), (46, 350), (82, 280)):
                cx = lx0 + dx - dist
                if cx < KX - 55:
                    coins += 10
    pill(d, "DAY 1" if day == 1 else "DAY 7", (36, 48), (18, 34, 51), (255, 255, 255))
    txt = f"SKOR {score}" + (f"   $ {coins}" if day == 7 else "")
    fw = d.textlength(txt, font=font(54))
    d.text((W - 36 - fw, 60), txt, font=font(54), fill=(18, 34, 51),
           stroke_width=4, stroke_fill=(255, 255, 255))
    if day == 7:
        # update progress bar
        d.rounded_rectangle([36, 150, 420, 168], radius=9, fill=(255, 255, 255, 170))
        d.rounded_rectangle([36, 150, 36 + 384, 168], radius=9, fill=(196, 28, 131))
        d.text((36, 182), "UPDATE HARIAN 7/7", font=font(34), fill=(18, 34, 51))
    return img

def big_text(img, lines, y0, size=118, fill=(255, 255, 255), stroke=(18, 34, 51)):
    d = ImageDraw.Draw(img, "RGBA")
    y = y0
    for line in lines:
        f = font(size)
        w = d.textlength(line, font=f)
        d.text(((W - w) / 2, y), line, font=f, fill=fill,
               stroke_width=6, stroke_fill=stroke)
        y += size + 24
    return img

def main():
    os.makedirs(OUT, exist_ok=True)
    total = 900
    for n in range(total):
        if n < 75:            # A hook: day 7, world 0-74
            img, _ = draw_world(n, 7)
            img = hud(img, 7, n)
            big_text(img, ["GAME INI", "DIBUAT AI"], 560, size=150)
            big_text(img, ["HARI 1  vs  HARI 7"], 960, size=72)
        elif n < 330:         # B day 1: world 0-254
            wf = n - 75
            img, _ = draw_world(wf, 1)
            img = hud(img, 1, wf)
            big_text(img, ["DAY 1 — BARU JADI"], 300, size=64)
        elif n < 390:         # C transition: magenta card
            img = Image.new("RGB", (W, H), (196, 28, 131))
            d = ImageDraw.Draw(img, "RGBA")
            t = (n - 330) / 60
            slide = int((1 - t) * 120)
            big_text(img, ["7 HARI UPDATE", "TIAP HARI..."], 700 + slide, size=110)
            d.text((W / 2, 1150 + slide), "DAY 1  →  DAY 7", font=font(64),
                   fill=(255, 207, 77), anchor="mm")
        elif n < 780:         # D day 7: world 0-389 (same moments as B, more going on)
            wf = n - 390
            img, _ = draw_world(wf, 7)
            img = hud(img, 7, wf)
            big_text(img, ["DAY 7 — SUDAH 7× UPDATE"], 300, size=60)
        else:                 # E CTA: day 7 world 390-509
            wf = n - 390
            img, _ = draw_world(wf, 7)
            img = hud(img, 7, wf)
            big_text(img, ["MULAI PUNYAMU", "DI make.fun"], 560, size=120)
        img.save(os.path.join(OUT, f"f{n:04d}.png"))
        if n % 150 == 0:
            print(f"frame {n}/{total}", flush=True)
    print("DONE", total, "frames")

if __name__ == "__main__":
    main()
