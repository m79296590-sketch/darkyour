#!/usr/bin/env python3
"""Экран загрузки DarkYour: тема Plymouth + картинки для меню загрузки.
Запускать из корня проекта."""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

PLY = "config/includes.chroot/usr/share/plymouth/themes/darkyour"
ASSETS = "assets/boot"
LOGO = "config/includes.chroot/usr/share/darkyour/darkyour-logo-512.png"
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FONT_S = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
BG = (11, 11, 16)
CYAN = (34, 211, 238)
VIOLET = (167, 139, 250)

SCRIPT = r"""// DarkYour — экран загрузки
Window.SetBackgroundTopColor(0.043, 0.043, 0.063);
Window.SetBackgroundBottomColor(0.043, 0.043, 0.063);

cx = Window.GetX() + Window.GetWidth() / 2;
cy = Window.GetY() + Window.GetHeight() / 2;

logo.image = Image("logo.png");
logo.sprite = Sprite(logo.image);
logo.sprite.SetPosition(cx - logo.image.GetWidth() / 2, cy - logo.image.GetHeight() / 2 - 60, 10);

word.image = Image("wordmark.png");
word.sprite = Sprite(word.image);
word.sprite.SetPosition(cx - word.image.GetWidth() / 2, cy + logo.image.GetHeight() / 2 - 30, 10);

// три точки загрузки
dot_on = Image("dot-on.png");
dot_off = Image("dot-off.png");
for (i = 0; i < 3; i = i + 1) {
  dots[i] = Sprite(dot_off);
  dots[i].SetPosition(cx - 28 + i * 22, cy + logo.image.GetHeight() / 2 + 40, 10);
}
tick = 0;
fun refresh_callback() {
  tick = tick + 1;
  active = Math.Int(tick / 12) - Math.Int(tick / 36) * 3;
  for (i = 0; i < 3; i = i + 1) {
    if (i == active) {
      dots[i].SetImage(dot_on);
    } else {
      dots[i].SetImage(dot_off);
    }
  }
}
Plymouth.SetRefreshFunction(refresh_callback);

// ---- ввод пароля (шифрование диска) ----
entry.image = Image("entry.png");
entry.sprite = Sprite(entry.image);
entry.sprite.SetPosition(cx - entry.image.GetWidth() / 2, cy + logo.image.GetHeight() / 2 + 80, 20);
entry.sprite.SetOpacity(0);
prompt.sprite = Sprite();
bullets.sprite = Sprite();

fun display_password_callback(prompt_text, bullet_count) {
  entry.sprite.SetOpacity(1);
  for (i = 0; i < 3; i = i + 1) {
    dots[i].SetOpacity(0);
  }
  if (prompt_text == "") {
    prompt_text = "Введите пароль для расшифровки диска";
  }
  p = Image.Text(prompt_text, 0.84, 0.84, 0.88, 1, "Sans 12");
  prompt.sprite.SetImage(p);
  prompt.sprite.SetPosition(cx - p.GetWidth() / 2, cy + logo.image.GetHeight() / 2 + 52, 21);
  prompt.sprite.SetOpacity(1);
  s = "";
  for (i = 0; i < bullet_count && i < 32; i = i + 1) {
    s = s + "•";
  }
  b = Image.Text(s, 0.13, 0.83, 0.93, 1, "Sans 16");
  bullets.sprite.SetImage(b);
  bullets.sprite.SetPosition(cx - b.GetWidth() / 2, cy + logo.image.GetHeight() / 2 + 80 + entry.image.GetHeight() / 2 - b.GetHeight() / 2, 22);
  bullets.sprite.SetOpacity(1);
}
fun display_normal_callback() {
  entry.sprite.SetOpacity(0);
  prompt.sprite.SetOpacity(0);
  bullets.sprite.SetOpacity(0);
  for (i = 0; i < 3; i = i + 1) {
    dots[i].SetOpacity(1);
  }
}
Plymouth.SetDisplayPasswordFunction(display_password_callback);
Plymouth.SetDisplayNormalFunction(display_normal_callback);

// ---- сообщения системы ----
msg.sprite = Sprite();
fun message_callback(text) {
  m = Image.Text(text, 0.54, 0.54, 0.64, 1, "Sans 10");
  msg.sprite.SetImage(m);
  msg.sprite.SetPosition(cx - m.GetWidth() / 2, Window.GetY() + Window.GetHeight() - 50, 30);
}
Plymouth.SetMessageFunction(message_callback);
"""

PLYMOUTH = """[Plymouth Theme]
Name=DarkYour
Description=Экран загрузки DarkYour
ModuleName=script

[script]
ImageDir=/usr/share/plymouth/themes/darkyour
ScriptFile=/usr/share/plymouth/themes/darkyour/darkyour.script
"""


def glow_paste(base, im, xy, blur):
    g = Image.new("RGBA", base.size, (0, 0, 0, 0))
    g.alpha_composite(im, xy)
    base.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))
    base.alpha_composite(im, xy)


def wordmark(size):
    f = ImageFont.truetype(FONT, size)
    w = int(f.getlength("DarkYour")) + 20
    img = Image.new("RGBA", (w, int(size * 1.4)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((10, 0), "Dark", font=f, fill=(232, 232, 240, 255))
    d.text((10 + f.getlength("Dark"), 0), "Your", font=f, fill=CYAN + (255,))
    return img


def dot(color, r=6):
    s = 4
    img = Image.new("RGBA", (r * 2 * s + 8 * s, r * 2 * s + 8 * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = img.width / 2
    d.ellipse([c - r * s, c - r * s, c + r * s, c + r * s], fill=color)
    return img.resize((img.width // s, img.height // s), Image.LANCZOS)


def entry_box():
    s = 4
    w, h = 320, 44
    img = Image.new("RGBA", (w * s, h * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w * s - 1, h * s - 1], radius=10 * s, fill=(19, 19, 28, 255),
                        outline=CYAN + (255,), width=2 * s)
    return img.resize((w, h), Image.LANCZOS)


def splash(W, H):
    """Фон меню загрузки: логотип сверху, середина свободна под пункты меню."""
    img = Image.new("RGBA", (W, H), BG + (255,))
    k = H / 480
    lg = Image.open(LOGO).convert("RGBA").resize((int(54 * k), int(54 * k)), Image.LANCZOS)
    wm = wordmark(int(26 * k))
    total = lg.width + int(8 * k) + wm.width
    x0 = (W - total) // 2
    y0 = int(H * 0.07)
    glow_paste(img, lg, (x0, y0), 6 * k)
    img.alpha_composite(wm, (x0 + lg.width + int(8 * k), y0 + (lg.height - wm.height) // 2 + int(4 * k)))
    d = ImageDraw.Draw(img)
    d.line([(W * 0.2, y0 + lg.height + 18 * k), (W * 0.8, y0 + lg.height + 18 * k)], fill=(34, 34, 52, 255), width=max(1, int(k)))
    fs = ImageFont.truetype(FONT_S, int(12 * k))
    d.text((W / 2, H * 0.94), "приватность по умолчанию", font=fs, fill=(82, 80, 110, 255), anchor="mm")
    return img.convert("RGB")


def main():
    os.makedirs(PLY, exist_ok=True)
    os.makedirs(ASSETS, exist_ok=True)
    lg = Image.open(LOGO).convert("RGBA").resize((140, 140), Image.LANCZOS)
    pad = 40
    canvas = Image.new("RGBA", (140 + pad * 2, 140 + pad * 2), (0, 0, 0, 0))
    glow_paste(canvas, lg, (pad, pad), 14)
    canvas.save(f"{PLY}/logo.png")
    wordmark(40).save(f"{PLY}/wordmark.png")
    dot(CYAN + (255,)).save(f"{PLY}/dot-on.png")
    dot((44, 44, 68, 255)).save(f"{PLY}/dot-off.png")
    entry_box().save(f"{PLY}/entry.png")
    with open(f"{PLY}/darkyour.script", "w") as f:
        f.write(SCRIPT)
    with open(f"{PLY}/darkyour.plymouth", "w") as f:
        f.write(PLYMOUTH)
    # фоны меню загрузки (syslinux требует ровно 640x480)
    splash(640, 480).save(f"{ASSETS}/splash-640x480.png")
    splash(1024, 768).save(f"{ASSETS}/splash-1024x768.png")
    print("boot ok")


if __name__ == "__main__":
    main()
