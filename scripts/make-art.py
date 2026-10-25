#!/usr/bin/env python3
"""Генерирует логотип и обои DarkYour (запускать из корня проекта)."""
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BG = (11, 11, 16)
CYAN = (34, 211, 238)
VIOLET = (167, 139, 250)
FONT_BOLD = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FONT_MED = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"

OUT_SHARE = "config/includes.chroot/usr/share/darkyour"
OUT_BG = "config/includes.chroot/usr/share/backgrounds/darkyour"


def glow_layer(size, draw_fn, blur):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(layer))
    return layer.filter(ImageFilter.GaussianBlur(blur))


def logo(px):
    s = 4  # суперсэмплинг для гладких краёв
    S = px * s
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    pad = int(S * 0.06)
    r = int(S * 0.22)
    box = (pad, pad, S - pad, S - pad)

    def frame(d):
        d.rounded_rectangle(box, r, outline=VIOLET + (255,), width=int(S * 0.035))

    img.alpha_composite(glow_layer((S, S), frame, S * 0.025))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, r, fill=(19, 19, 28, 255), outline=VIOLET + (255,), width=int(S * 0.03))

    # Буква «D» как щит: вертикаль + дуга
    cx, cy = S * 0.5, S * 0.5
    h = S * 0.46
    w = S * 0.38
    x0 = cx - w * 0.5
    y0 = cy - h * 0.5
    lw = int(S * 0.07)

    bow = x0 + w * 0.32  # где начинается дуга

    def letter(dd):
        col = CYAN + (255,)
        dd.rectangle([x0, y0, x0 + lw, y0 + h], fill=col)
        dd.rectangle([x0, y0, bow + 1, y0 + lw], fill=col)
        dd.rectangle([x0, y0 + h - lw, bow + 1, y0 + h], fill=col)
        dd.arc([bow - (x0 + w - bow), y0, x0 + w, y0 + h], -90, 90, fill=col, width=lw)

    img.alpha_composite(glow_layer((S, S), letter, S * 0.03))
    letter(ImageDraw.Draw(img))
    # точка-«замок» в центре
    dot = S * 0.045
    dx = x0 + w * 0.5
    ImageDraw.Draw(img).ellipse([dx - dot, cy - dot, dx + dot, cy + dot], fill=VIOLET + (255,))
    return img.resize((px, px), Image.LANCZOS)


def wallpaper(W=1920, H=1080):
    random.seed(7)
    img = Image.new("RGBA", (W, H), BG + (255,))
    d = ImageDraw.Draw(img)

    # еле заметная сетка
    for x in range(0, W, 48):
        d.line([(x, 0), (x, H)], fill=(18, 18, 26, 255))
    for y in range(0, H, 48):
        d.line([(0, y), (W, y)], fill=(18, 18, 26, 255))

    # мягкие цветовые пятна
    def blobs(dd):
        dd.ellipse([W * 0.62, -H * 0.35, W * 1.25, H * 0.55], fill=VIOLET + (38,))
        dd.ellipse([-W * 0.25, H * 0.55, W * 0.35, H * 1.4], fill=CYAN + (30,))

    img.alpha_composite(glow_layer((W, H), blobs, 160))

    # неоновые волны
    def waves(dd, width):
        for i, (col, amp, ph, off) in enumerate([
            (CYAN, 70, 0.0, 0.66),
            (VIOLET, 55, 1.7, 0.71),
            (CYAN, 40, 3.1, 0.76),
        ]):
            pts = []
            for x in range(-20, W + 21, 8):
                y = H * off + amp * math.sin(x / 260 + ph) + 25 * math.sin(x / 97 + ph * 2)
                pts.append((x, y))
            alpha = 255 if i == 0 else 190
            dd.line(pts, fill=col + (alpha,), width=width, joint="curve")

    img.alpha_composite(glow_layer((W, H), lambda dd: waves(dd, 9), 14))
    waves(ImageDraw.Draw(img), 2)

    # «звёзды»
    for _ in range(140):
        x, y = random.randint(0, W), random.randint(0, int(H * 0.6))
        a = random.randint(40, 140)
        d.point((x, y), fill=(200, 200, 230, a))

    # надпись
    font = ImageFont.truetype(FONT_BOLD, 64)
    small = ImageFont.truetype(FONT_MED, 20)
    text = "DarkYour"
    tw = d.textlength(text, font=font)
    tx, ty = W - tw - 90, H - 150

    def word(dd):
        dd.text((tx, ty), text, font=font, fill=VIOLET + (150,))

    img.alpha_composite(glow_layer((W, H), word, 12))
    d = ImageDraw.Draw(img)
    d.text((tx, ty), text, font=font, fill=(44, 44, 66, 255))
    sub = "приватность по умолчанию"
    sw = d.textlength(sub, font=small)
    d.text((W - sw - 92, ty + 80), sub, font=small, fill=(86, 86, 115, 255))
    return img.convert("RGB")


if __name__ == "__main__":
    for size in (512, 256, 128, 64, 48):
        logo(size).save(f"{OUT_SHARE}/darkyour-logo-{size}.png")
    logo(256).save(f"{OUT_SHARE}/darkyour-logo.png")
    wallpaper().save(f"{OUT_BG}/darkyour.png", optimize=True)
    wallpaper(2560, 1440).save(f"{OUT_BG}/darkyour-2k.png", optimize=True)
    print("ok")
