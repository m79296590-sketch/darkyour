#!/usr/bin/env python3
"""Генерирует тему окон DarkYour для xfwm4 (рамки, заголовки, кнопки).
Запускать из корня проекта."""
import os
import shutil

from PIL import Image, ImageDraw

OUT = "config/includes.chroot/usr/share/themes/DarkYour/xfwm4"
SS = 4  # суперсэмплинг

H = 36          # высота заголовка
R = 10          # радиус верхних углов
BW = 2          # толщина боковых рамок

STATES = {
    "active": {
        "fill": (19, 19, 28, 255),
        "border": (52, 52, 78, 255),
        "sep": (34, 34, 52, 255),
        "glyph": (154, 154, 176, 255),
    },
    "inactive": {
        "fill": (14, 14, 21, 255),
        "border": (36, 36, 54, 255),
        "sep": (26, 26, 38, 255),
        "glyph": (74, 74, 96, 255),
    },
}
CYAN = (34, 211, 238, 255)
VIOLET = (167, 139, 250, 255)
ROSE = (247, 118, 142, 255)


def big(w, h):
    return Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))


def small(img):
    return img.resize((img.width // SS, img.height // SS), Image.LANCZOS)


def title_strip(w, st):
    """Кусок заголовка: заливка + верхняя рамка + разделитель снизу."""
    img = Image.new("RGBA", (w, H), st["fill"])
    d = ImageDraw.Draw(img)
    d.line([(0, 0), (w - 1, 0)], fill=st["border"])
    d.line([(0, H - 1), (w - 1, H - 1)], fill=st["sep"])
    return img


def corner(st, right=False):
    img = big(R, H)
    d = ImageDraw.Draw(img)
    s = SS
    # скруглённый прямоугольник шире картинки, чтобы взять только угол
    box = [0, 0, R * 2 * s, (H + R) * s]
    d.rounded_rectangle(box, radius=R * s, fill=st["border"])
    d.rounded_rectangle([s, s, R * 2 * s, (H + R) * s], radius=(R - 1) * s, fill=st["fill"])
    img = small(img)
    d = ImageDraw.Draw(img)
    d.line([(0, H - 1), (R - 1, H - 1)], fill=st["sep"])
    d.line([(0, H - 1), (0, H - 1)], fill=st["border"])
    if right:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return img


def side(st):
    img = Image.new("RGBA", (BW, 4), st["fill"])
    ImageDraw.Draw(img).line([(0, 0), (0, 3)], fill=st["border"])
    return img


def bottom(st):
    img = Image.new("RGBA", (4, BW), st["fill"])
    ImageDraw.Draw(img).line([(0, BW - 1), (3, BW - 1)], fill=st["border"])
    return img


def bottom_corner(st):
    img = Image.new("RGBA", (BW, BW), st["fill"])
    d = ImageDraw.Draw(img)
    d.line([(0, 0), (0, BW - 1)], fill=st["border"])
    d.line([(0, BW - 1), (BW - 1, BW - 1)], fill=st["border"])
    return img


BTN_W = 34


def button(kind, st, mode):
    """mode: normal | prelight | pressed"""
    base = title_strip(BTN_W, st).resize((BTN_W * SS, H * SS), Image.NEAREST)
    d = ImageDraw.Draw(base)
    s = SS
    cx, cy = BTN_W * s / 2, H * s / 2
    color = st["glyph"]
    if mode in ("prelight", "pressed") and kind != "menu":
        bg = (31, 31, 46, 255) if mode == "prelight" else (40, 40, 60, 255)
        d.rounded_rectangle([cx - 13 * s, cy - 11 * s, cx + 13 * s, cy + 11 * s], radius=7 * s, fill=bg)
        color = ROSE if kind == "close" else CYAN
    w = int(1.5 * s)
    g = 5.5 * s
    if kind == "hide":
        d.line([(cx - g, cy + 0.5 * s), (cx + g, cy + 0.5 * s)], fill=color, width=w)
    elif kind == "maximize":
        d.rounded_rectangle([cx - g, cy - g, cx + g, cy + g], radius=2 * s, outline=color, width=w)
    elif kind == "maximize-toggled":
        o = 2.4 * s
        d.rounded_rectangle([cx - g + o, cy - g - o / 2, cx + g + o / 2, cy + g - o], radius=1.6 * s, outline=color, width=w)
        d.rounded_rectangle([cx - g - o / 2, cy - g + o, cx + g - o, cy + g + o / 2], radius=1.6 * s, outline=color, width=w)
    elif kind == "close":
        d.line([(cx - g, cy - g), (cx + g, cy + g)], fill=color, width=w)
        d.line([(cx - g, cy + g), (cx + g, cy - g)], fill=color, width=w)
    elif kind == "menu":
        dot = (58, 58, 80, 255) if st is STATES["active"] else (40, 40, 58, 255)
        if mode != "normal":
            dot = CYAN
        for i, x in enumerate((-9, 0, 9)):
            r = 3.2 * s
            d.ellipse([cx + x * s - r, cy - r, cx + x * s + r, cy + r], fill=dot)
    return small(base)


THEMERC = """# DarkYour — тема окон
full_width_title=true
title_alignment=center
title_vertical_offset_active=0
title_vertical_offset_inactive=0
title_horizontal_offset=6
title_shadow_active=false
title_shadow_inactive=false
active_text_color=#d6d6e0
inactive_text_color=#6b6b80
active_text_shadow_color=#000000
inactive_text_shadow_color=#000000
button_offset=6
button_spacing=0
maximized_offset=0
show_app_icon=false
"""


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for name, st in STATES.items():
        sfx = f"-{name}.png"
        corner(st).save(f"{OUT}/top-left{sfx}")
        corner(st, right=True).save(f"{OUT}/top-right{sfx}")
        for i in range(1, 6):
            title_strip(2, st).save(f"{OUT}/title-{i}{sfx}")
        side(st).save(f"{OUT}/left{sfx}")
        side(st).transpose(Image.FLIP_LEFT_RIGHT).save(f"{OUT}/right{sfx}")
        bottom(st).save(f"{OUT}/bottom{sfx}")
        bottom_corner(st).save(f"{OUT}/bottom-left{sfx}")
        bottom_corner(st).transpose(Image.FLIP_LEFT_RIGHT).save(f"{OUT}/bottom-right{sfx}")
        for kind in ("hide", "maximize", "maximize-toggled", "close", "menu"):
            button(kind, st, "normal").save(f"{OUT}/{kind}{sfx}")
            if name == "active":
                button(kind, st, "prelight").save(f"{OUT}/{kind}-prelight.png")
                button(kind, st, "pressed").save(f"{OUT}/{kind}-pressed.png")
        # кнопки, которых нет в раскладке, — пустые, чтобы xfwm4 не ругался
        for kind in ("shade", "shade-toggled", "stick", "stick-toggled"):
            title_strip(BTN_W, st).save(f"{OUT}/{kind}{sfx}")
            if name == "active":
                title_strip(BTN_W, st).save(f"{OUT}/{kind}-prelight.png")
                title_strip(BTN_W, st).save(f"{OUT}/{kind}-pressed.png")
    with open(f"{OUT}/themerc", "w") as f:
        f.write(THEMERC)
    print("xfwm4 theme ok:", len(os.listdir(OUT)), "files")


if __name__ == "__main__":
    main()
