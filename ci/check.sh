#!/usr/bin/env bash
# The site: its API reference and command list are the pinned program's
# (fetched and compared), it builds, and every link in it leads somewhere.
set -euo pipefail
cd "$(dirname "$0")/.."
rev="$(sed -n 's/^ortus = "\([0-9a-f]\{40\}\)"$/\1/p' pins.toml)"
[ -n "$rev" ] || { echo "check: pins.toml names no ortus commit" >&2; exit 1; }
base="https://raw.githubusercontent.com/Ortus-Sovereign-Cloud/ortus/$rev"
for f in api/openapi.json api/commands.txt api/settings.txt; do
  tmp="$(mktemp)"
  curl -fsSL "$base/$f" -o "$tmp"
  if [ -n "${ORTUS_UPDATE_REFERENCE:-}" ]; then cp "$tmp" "$f"; fi
  cmp -s "$tmp" "$f" || { echo "check: $f differs from the program at $rev: run ORTUS_UPDATE_REFERENCE=1 ci/check.sh" >&2; exit 1; }
  rm -f "$tmp"
done
python3 tools/build.py
python3 tools/check_site.py
echo "all checks passed"
