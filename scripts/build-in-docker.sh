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

echo "==> Сборка"
lb clean --purge || true
lb config
lb build 2>&1 | tee build.log

ls -lh ./*.iso
