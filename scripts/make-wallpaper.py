#!/usr/bin/env python3
"""Обои DarkYour 1.2 по концепту: тёмная сетка и пучки неоновых волн.
Запускать из корня проекта."""
import math
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = "config/includes.chroot/usr/share/backgrounds/darkyour"
BG = (13, 12, 20)
CYAN = (34, 211, 238)
VIOLET = (167, 139, 250)
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FONT_S = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"


def smooth(e0, e1, u):
    t = min(1.0, max(0.0, (u - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


def ribbon(W, d, color, n, y_fn, spread_fn, env_fn, width, a_hi, a_lo):
    """Пучок из n линий; у каждой участки с прозрачностью по огибающей env."""
    xs = list(range(-20, W + 21, 5))
    for i in range(n):
        t = i / max(1, n - 1)
        core = 1 - abs(t - 0.5) * 2
        base_a = a_lo + (a_hi - a_lo) * core
        prev = None
        for x in xs:
            u = x / W
            pt = (x, y_fn(u) + (t - 0.5) * spread_fn(u))
            if prev is not None:
                a = int(base_a * env_fn(u))
                if a > 2:
                    d.line([prev, pt], fill=color + (a,), width=width)
            prev = pt


def make(W, H, A=CYAN, B=VIOLET, waves=True):
    k = W / 1920
    CYAN, VIOLET = A, B
    img = Image.new("RGBA", (W, H), BG + (255,))

    # мягкие пятна цвета
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W * 0.55, H * 0.15, W * 1.15, H * 1.05], fill=VIOLET + (26,))
    gd.ellipse([-W * 0.2, H * 0.35, W * 0.35, H * 1.1], fill=CYAN + (18,))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(220 * k)))

    # сетка
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    step = int(132 * k)
    for x in range(0, W, step):
        gd.line([(x, 0), (x, H)], fill=(120, 110, 200, 22), width=1)
    for y in range(0, H, step):
        gd.line([(0, y), (W, y)], fill=(120, 110, 200, 22), width=1)
    img.alpha_composite(grid)

    def layer(color, n, y_fn, spread_fn, env_fn, blur):
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ribbon(W, ImageDraw.Draw(lay), color, n, y_fn, spread_fn, env_fn, max(1, round(1.6 * k)), 220, 40)
        g = lay.filter(ImageFilter.GaussianBlur(blur * k))
        img.alpha_composite(g)
        img.alpha_composite(g)
        img.alpha_composite(lay)

    if not waves:
        return finish(img, W, H, k)
    # бирюзовая «чаша» слева
    layer(
        CYAN, 16,
        lambda u: H * (0.30 + 0.40 * math.sin(math.pi * min(1, max(0, u / 0.44)))),
        lambda u: k * (70 + 200 * max(0, 0.45 - u)),
        lambda u: 1 - smooth(0.30, 0.46, u),
        7,
    )
    # бирюзовый подъём справа
    layer(
        CYAN, 18,
        lambda u: H * (1.06 - 0.84 / (1 + math.exp(-(u - 0.80) * 8))),
        lambda u: k * (60 + 300 * max(0, u - 0.4)),
        lambda u: smooth(0.40, 0.58, u),
        7,
    )
    # фиолетовый холм посередине
    layer(
        VIOLET, 11,
        lambda u: H * (0.47 - 0.17 * math.exp(-((u - 0.73) ** 2) / 0.0045)
                       + 0.05 * math.exp(-((u - 0.61) ** 2) / 0.0025)),
        lambda u: k * 56,
        lambda u: smooth(0.44, 0.56, u) * (1 - smooth(0.86, 0.97, u)),
        8,
    )

    return finish(img, W, H, k)


def finish(img, W, H, k):
    # точки-«звёзды»
    random.seed(11)
    d = ImageDraw.Draw(img)
    for _ in range(int(110 * k)):
        x, y = random.randint(0, W), random.randint(0, int(H * 0.55))
        d.point((x, y), fill=(200, 200, 235, random.randint(30, 110)))

    # надпись в углу
    f = ImageFont.truetype(FONT, int(54 * k))
    fs = ImageFont.truetype(FONT_S, int(18 * k))
    tx, ty = W - int(90 * k), H - int(150 * k)
    d.text((tx, ty), "DarkYour", font=f, fill=(46, 44, 70, 255), anchor="ra")
    d.text((tx, ty + int(70 * k)), "приватность по умолчанию", font=fs, fill=(82, 80, 110, 255), anchor="ra")
    return img.convert("RGB")




LOGO = "config/includes.chroot/usr/share/darkyour/darkyour-logo-512.png"


def minimal(W, H):
    img = make(W, H, waves=False).convert("RGBA")
    lg = Image.open(LOGO).convert("RGBA").resize((int(H * 0.34),) * 2, Image.LANCZOS)
    a = lg.split()[3].point(lambda v: int(v * 0.22))
    lg.putalpha(a)
    img.alpha_composite(lg, ((W - lg.width) // 2, (H - lg.height) // 2 - int(H * 0.04)))
    return img.convert("RGB")


def aurora(W, H):
    k = W / 1920
    img = Image.new("RGBA", (W, H), (9, 9, 14, 255))
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    d.ellipse([-W * 0.1, H * 0.25, W * 0.55, H * 0.95], fill=CYAN + (70,))
    d.ellipse([W * 0.35, -H * 0.2, W * 1.05, H * 0.6], fill=VIOLET + (80,))
    d.ellipse([W * 0.6, H * 0.55, W * 1.2, H * 1.3], fill=(236, 72, 153, 45))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(260 * k)))
    return finish(img, W, H, k)


if __name__ == "__main__":
    make(1920, 1080).save(f"{OUT}/darkyour.png", optimize=True)
    make(2560, 1440).save(f"{OUT}/darkyour-2k.png", optimize=True)
    make(1920, 1080, VIOLET, (236, 72, 153)).save(f"{OUT}/darkyour-violet.png", optimize=True)
    minimal(1920, 1080).save(f"{OUT}/darkyour-minimal.png", optimize=True)
    aurora(1920, 1080).save(f"{OUT}/darkyour-aurora.png", optimize=True)
    print("ok")
