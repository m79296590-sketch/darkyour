#!/bin/bash
# Запускается внутри контейнера debian:trixie (см. .github/workflows/build.yml)
set -euo pipefail
cd /build

echo "==> Подключаю разделы contrib и non-free для проверки пакетов"
sed -i 's/^Components: main$/Components: main contrib non-free non-free-firmware/' \
	/etc/apt/sources.list.d/debian.sources || true

apt-get update
apt-get install -y --no-install-recommends live-build debootstrap ca-certificates cpio

echo "==> Проверяю, что все пакеты из списка существуют"
LIST=config/package-lists/darkyour.list.chroot
TMP=$(mktemp)
missing=0
while IFS= read -r line; do
	pkg="$(echo "$line" | sed 's/#.*//' | xargs)"
	if [ -z "$pkg" ]; then
		echo "$line" >> "$TMP"
		continue
	fi
	if apt-cache show "$pkg" >/dev/null 2>&1; then
		echo "$line" >> "$TMP"
	else
		echo "::warning::Пакет '$pkg' не найден в Debian trixie — пропускаю"
		echo "# (не найден) $pkg" >> "$TMP"
		missing=$((missing + 1))
	fi
done < "$LIST"
mv "$TMP" "$LIST"
echo "Пропущено пакетов: $missing"

echo "==> Права на скрипты"
chmod +x auto/* config/hooks/normal/*.hook.chroot \
	config/includes.chroot/usr/bin/* 2>/dev/null || true

echo "==> Версия"
VERSION="$(cat VERSION 2>/dev/null || echo dev)"
echo "$VERSION" > config/includes.chroot/usr/share/darkyour/version
echo "DarkYour $VERSION"

echo "==> Брендинг меню загрузки"
if [ -d /usr/share/live/build/bootloaders ]; then
	mkdir -p config/bootloaders
	for bl in /usr/share/live/build/bootloaders/*; do
		name="$(basename "$bl")"
		rm -rf "config/bootloaders/$name"
		cp -a "$bl" "config/bootloaders/$name"
	done
	# фоновые картинки
	while IFS= read -r f; do
		case "$f" in
			*syslinux*|*isolinux*|*extlinux*) src=assets/boot/splash-640x480.png ;;
			*) src=assets/boot/splash-1024x768.png ;;
		esac
		case "$f" in
			*.png) cp "$src" "$f" ;;
			*.svg|*.svg.in)
				case "$src" in *640x480*) w=640; h=480 ;; *) w=1024; h=768 ;; esac
				printf '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%s" height="%s"><image width="%s" height="%s" xlink:href="data:image/png;base64,%s"/></svg>\n' \
					"$w" "$h" "$w" "$h" "$(base64 -w0 "$src")" > "$f" ;;
		esac
		echo "  фон: $f"
	done < <(find config/bootloaders -type f ! -type l \( -name 'splash*.png' -o -name 'splash*.svg' -o -name 'splash*.svg.in' \))
	# надписи «Live system» → «DarkYour»
	grep -rlI "Live system" config/bootloaders /usr/lib/live/build 2>/dev/null | while IFS= read -r f; do
		sed -i 's/Live system/DarkYour/g' "$f"
		echo "  текст: $f"
	done || true
fi

echo "==> Сборка"
lb clean --purge || true
lb config
lb build 2>&1 | tee build.log

ls -lh ./*.iso
