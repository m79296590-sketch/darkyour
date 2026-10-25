#!/usr/bin/env python3
"""Генерирует тему иконок DarkYour (SVG). Запускать из корня проекта.

Стиль: тонкие бирюзовые линии + одна фиолетовая деталь на тёмной плитке (программы),
залитые бирюзовые/фиолетовые папки со значком внутри (места).
Всё, чего здесь нет, тема берёт из Papirus-Dark.
"""
import math
import os

ROOT = "config/includes.chroot/usr/share/icons/DarkYour"
CYAN, CYAN_D = "#22d3ee", "#0e8fa3"
VIOLET, VIOLET_D = "#a78bfa", "#6d55c9"
TILE, TILE_LINE = "#13131c", "#2c2c44"
INK = "#0b0b10"
SW = 3.6  # толщина линий


def svg(body):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">\n'
        f"{body}\n</svg>\n"
    )


def tile(inner):
    return svg(
        f'<rect x="3" y="3" width="58" height="58" rx="14" fill="{TILE}" stroke="{TILE_LINE}" stroke-width="1.5"/>\n'
        f'<g fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="{SW}">\n{inner}\n</g>'
    )


def c(d):  # бирюзовая линия
    return f'<path d="{d}" stroke="{CYAN}"/>'


def v(d):  # фиолетовая линия
    return f'<path d="{d}" stroke="{VIOLET}"/>'


def gear_path(cx, cy, r_out, r_in, teeth=8):
    pts = []
    step = 2 * math.pi / teeth
    for i in range(teeth):
        a = i * step
        for da, r in ((-0.30, r_in), (-0.16, r_out), (0.16, r_out), (0.30, r_in)):
            pts.append((cx + r * math.cos(a + da * step * 2), cy + r * math.sin(a + da * step * 2)))
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"


APPS = {
    "dy-files": c("M14 23a4 4 0 0 1 4-4h9l5 5h14a4 4 0 0 1 4 4v15a4 4 0 0 1-4 4H18a4 4 0 0 1-4-4Z")
    + v("M33 19.5h10a3.5 3.5 0 0 1 3.5 3.5"),
    "dy-browser": f'<circle cx="32" cy="32" r="13" stroke="{CYAN}"/>'
    + f'<ellipse cx="32" cy="32" rx="22" ry="6" transform="rotate(-35 32 32)" stroke="{VIOLET}"/>',
    "dy-terminal": c("M14 21a4 4 0 0 1 4-4h28a4 4 0 0 1 4 4v22a4 4 0 0 1-4 4H18a4 4 0 0 1-4-4Z")
    + c("M14 25h36")
    + "".join(f'<circle cx="{x}" cy="21" r="0.8" stroke="{VIOLET}" stroke-width="2.4"/>' for x in (19.5, 24, 28.5))
    + c("M21 31l6 5-6 5")
    + v("M31 42h9"),
    "dy-settings": f'<path d="{gear_path(32, 32, 17, 12.5)}" stroke="{CYAN}"/>'
    + f'<circle cx="32" cy="32" r="5.5" stroke="{VIOLET}"/>',
    "dy-shield": c("M32 13l15 5.5v11c0 10-6.5 17-15 21-8.5-4-15-11-15-21v-11Z") + v("M25 32l5 5 9-10"),
    "dy-store": c("M17 26h30l-2.2 21.5a3.5 3.5 0 0 1-3.5 3.5H22.7a3.5 3.5 0 0 1-3.5-3.5Z")
    + c("M25 26v-4a7 7 0 0 1 14 0v4")
    + v("M27.5 45l4.5-11.5 4.5 11.5M29.3 40.5h5.4"),
    "dy-trash": c("M17 21h30M27 21v-4h10v4M20.5 21l2.2 25.5a3.5 3.5 0 0 0 3.5 3.5h11.6a3.5 3.5 0 0 0 3.5-3.5l2.2-25.5")
    + f'<path d="M27 28v15M32 28v15M37 28v15" stroke="{VIOLET}" stroke-width="2.6"/>',
    "dy-editor": c("M21 13h15l10 10v24a4 4 0 0 1-4 4H21a4 4 0 0 1-4-4V17a4 4 0 0 1 4-4Z")
    + v("M36 13v10h10")
    + c("M23 31h17M23 37h17M23 43h10"),
    "dy-image": c("M13 21a4 4 0 0 1 4-4h30a4 4 0 0 1 4 4v22a4 4 0 0 1-4 4H17a4 4 0 0 1-4-4Z")
    + c("M14 43l10-10 8 8 5-5 13 11")
    + f'<circle cx="41" cy="26" r="3.6" stroke="{VIOLET}"/>',
    "dy-music": c("M28 43V20l17-5v23M28 25l17-5")
    + f'<circle cx="23.5" cy="43.5" r="4.8" stroke="{VIOLET}"/><circle cx="40.5" cy="38.5" r="4.8" stroke="{VIOLET}"/>',
    "dy-video": c("M13 23a5 5 0 0 1 5-5h28a5 5 0 0 1 5 5v18a5 5 0 0 1-5 5H18a5 5 0 0 1-5-5Z")
    + v("M28.5 26v12l10-6Z"),
    "dy-archive": c("M15 20a4 4 0 0 1 4-4h26a4 4 0 0 1 4 4v24a4 4 0 0 1-4 4H19a4 4 0 0 1-4-4Z")
    + c("M15 28h34M15 37h34")
    + v("M32 14v36")
    + f'<rect x="28.5" y="29" width="7" height="7" rx="1.5" stroke="{VIOLET}" fill="{TILE}"/>',
    "dy-installer": v("M32 14v21M24 27l8 8 8-8") + c("M16 37v7a4 4 0 0 0 4 4h24a4 4 0 0 0 4-4v-7"),
    "dy-monitor": c("M14 33h8l4.5-11 6.5 20 5-13 3 6h9"),
    "dy-screenshot": c("M15 23v-4a4 4 0 0 1 4-4h4M41 15h4a4 4 0 0 1 4 4v4M49 41v4a4 4 0 0 1-4 4h-4M23 49h-4a4 4 0 0 1-4-4v-4")
    + f'<circle cx="32" cy="32" r="7" stroke="{VIOLET}"/>',
    "dy-sound": c("M15 27h7l9-8v26l-9-8h-7Z") + v("M38 25a10 10 0 0 1 0 14M43 20a17 17 0 0 1 0 24"),
    "dy-welcome": f'<g stroke="none"><rect x="17" y="15" width="7" height="34" rx="1" fill="{CYAN}"/>'
    f'<rect x="17" y="15" width="13" height="7" fill="{CYAN}"/><rect x="17" y="42" width="13" height="7" fill="{CYAN}"/></g>'
    + c("M30 18.5a13.5 13.5 0 0 1 0 27")
    + f'<circle cx="33" cy="32" r="3.2" fill="{VIOLET}" stroke="none"/>',
}

# Какие системные имена иконок заменяем нашими
APP_ALIASES = {
    "dy-files": ["org.xfce.thunar", "thunar", "system-file-manager", "org.xfce.filemanager", "file-manager", "nautilus"],
    "dy-browser": ["firefox-esr", "firefox", "web-browser", "org.xfce.webbrowser", "internet-web-browser"],
    "dy-terminal": ["org.xfce.terminal", "org.xfce.terminalemulator", "utilities-terminal", "xfce4-terminal", "terminal"],
    "dy-settings": ["org.xfce.settings.manager", "preferences-system", "xfce4-settings-manager", "preferences-desktop", "systemsettings"],
    "dy-shield": ["gufw", "security-high", "darkyour-vpn", "preferences-system-firewall"],
    "dy-store": ["org.gnome.Software", "gnome-software", "system-software-install", "software-store", "softwarecenter"],
    "dy-trash": [],
    "dy-editor": ["org.xfce.mousepad", "mousepad", "accessories-text-editor", "text-editor"],
    "dy-image": ["org.xfce.ristretto", "ristretto", "image-viewer", "eog", "org.gnome.eog"],
    "dy-music": ["multimedia-audio-player", "audio-player", "rhythmbox"],
    "dy-video": ["vlc", "multimedia-video-player", "video-player", "totem", "org.gnome.Totem", "mpv"],
    "dy-archive": ["org.gnome.FileRoller", "file-roller", "archive-manager", "utilities-file-archiver", "xarchiver"],
    "dy-installer": ["calamares", "system-installer", "install-debian"],
    "dy-monitor": ["org.xfce.taskmanager", "xfce4-taskmanager", "utilities-system-monitor", "gnome-system-monitor"],
    "dy-screenshot": ["org.xfce.screenshooter", "applets-screenshooter", "xfce4-screenshooter", "accessories-screenshot"],
    "dy-sound": ["pavucontrol", "multimedia-volume-control", "org.pulseaudio.pavucontrol"],
    "dy-welcome": ["darkyour-welcome", "darkyour"],
}


# ---------- Папки ----------
def folder(front, back, glyph=""):
    return svg(
        f'<path d="M6 16a5 5 0 0 1 5-5h13.5a4 4 0 0 1 3 1.4L31 17h22a5 5 0 0 1 5 5v4H6Z" fill="{back}"/>\n'
        f'<path d="M6 23a4 4 0 0 1 4-4h44a4 4 0 0 1 4 4v26a5 5 0 0 1-5 5H11a5 5 0 0 1-5-5Z" fill="{front}"/>\n'
        f'<g fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" '
        f'transform="translate(32 37) scale(0.62) translate(-32 -32)">{glyph}</g>'
    )


def g(d):
    return f'<path d="{d}"/>'


GLYPHS = {
    "home": g("M18 31l14-12 14 12M22 28v15h20V28M28 43v-8h8v8"),
    "doc": g("M23 15h12l8 8v22a3 3 0 0 1-3 3H23a3 3 0 0 1-3-3V18a3 3 0 0 1 3-3ZM35 15v8h8M25 32h13M25 39h13"),
    "down": g("M32 16v24M22 30l10 10 10-10M20 48h24"),
    "pic": g("M15 20a3 3 0 0 1 3-3h28a3 3 0 0 1 3 3v24a3 3 0 0 1-3 3H18a3 3 0 0 1-3-3ZM16 42l10-10 8 8 5-5 10 10")
    + '<circle cx="40" cy="25" r="3"/>',
    "music": g("M27 43V20l17-5v23M27 25l17-5") + '<circle cx="22.5" cy="43.5" r="4.5"/><circle cx="39.5" cy="38.5" r="4.5"/>',
    "video": g("M27 20v24l18-12Z"),
    "desktop": g("M14 18a3 3 0 0 1 3-3h30a3 3 0 0 1 3 3v19a3 3 0 0 1-3 3H17a3 3 0 0 1-3-3ZM26 49h12M32 40v9"),
    "templates": g("M20 16h24v32H20ZM26 25h12M26 32h12M26 39h7"),
    "public": '<circle cx="32" cy="32" r="14"/>' + g("M18 32h28M32 18c5 4 5 24 0 28M32 18c-5 4-5 24 0 28"),
    "remote": g("M22 40a9 9 0 0 1 1-18 12 12 0 0 1 22 3 8 8 0 0 1-1 15Z"),
}

PLACES = {
    "folder": ("cyan", ""),
    "user-home": ("cyan", "home"),
    "folder-documents": ("violet", "doc"),
    "folder-download": ("cyan", "down"),
    "folder-pictures": ("violet", "pic"),
    "folder-music": ("cyan", "music"),
    "folder-videos": ("violet", "video"),
    "user-desktop": ("cyan", "desktop"),
    "folder-templates": ("violet", "templates"),
    "folder-publicshare": ("cyan", "public"),
    "folder-remote": ("violet", "remote"),
}
PLACE_ALIASES = {
    "folder": ["inode-directory", "folder-open", "folder-drag-accept"],
    "folder-download": ["folder-downloads"],
    "folder-pictures": ["folder-images"],
    "folder-videos": ["folder-video"],
    "folder-publicshare": ["folder-public"],
    "folder-remote": ["folder-network"],
}


def trash(full=False):
    paper = (
        f'<path d="M28 13l3-4 5 1 1 4-3 3h-5Z" stroke="{VIOLET}" stroke-width="2.6"/>' if full else ""
    )
    return tile(APPS["dy-trash"] + paper)


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(data)


def link(dirpath, target, name):
    p = os.path.join(dirpath, name + ".svg")
    if os.path.lexists(p):
        os.remove(p)
    os.symlink(target + ".svg", p)


def main():
    apps_dir = os.path.join(ROOT, "scalable/apps")
    places_dir = os.path.join(ROOT, "scalable/places")
    for d in (apps_dir, places_dir):
        if os.path.isdir(d):
            for f in os.listdir(d):
                os.remove(os.path.join(d, f))

    for name, body in APPS.items():
        write(os.path.join(apps_dir, name + ".svg"), tile(body))
        for alias in APP_ALIASES.get(name, []):
            link(apps_dir, name, alias)

    for name, (color, glyph) in PLACES.items():
        front, back = (CYAN, CYAN_D) if color == "cyan" else (VIOLET, VIOLET_D)
        write(os.path.join(places_dir, name + ".svg"), folder(front, back, GLYPHS.get(glyph, "")))
        for alias in PLACE_ALIASES.get(name, []):
            link(places_dir, name, alias)

    write(os.path.join(places_dir, "user-trash.svg"), trash(False))
    write(os.path.join(places_dir, "user-trash-full.svg"), trash(True))

    write(
        os.path.join(ROOT, "index.theme"),
        "[Icon Theme]\n"
        "Name=DarkYour\n"
        "Comment=Неоновые иконки DarkYour\n"
        "Inherits=Papirus-Dark,Adwaita,hicolor\n"
        "Example=folder\n"
        "Directories=scalable/apps,scalable/places\n\n"
        "[scalable/apps]\nContext=Applications\nSize=64\nMinSize=16\nMaxSize=512\nType=Scalable\n\n"
        "[scalable/places]\nContext=Places\nSize=64\nMinSize=16\nMaxSize=512\nType=Scalable\n",
    )
    print("ok:", len(APPS), "apps,", len(PLACES) + 2, "places")


if __name__ == "__main__":
    main()
