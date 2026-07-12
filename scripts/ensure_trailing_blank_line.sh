#! /usr/bin/env bash
# Ensures every text file ends with a trailing blank line (final "\n\n").
# Run after black/ruff format. Inverse: scripts/strip_trailing_blank_line.sh
# (needed before black --check in CI).

set -euo pipefail

ScriptPath=$0
Dir=$(cd "$(dirname "$ScriptPath")/.." && pwd)

cd "$Dir"

python3 <<'PY'
from pathlib import Path

ROOT = Path('.')
SKIP_DIRS = {
	'.git',
	'.venv',
	'.ruff_cache',
	'.pytest_cache',
	'dist',
	'build',
	'asynkio.egg-info',
	'__pycache__',
}
TEXT_SUFFIXES = {
	'.py',
	'.md',
	'.toml',
	'.yml',
	'.yaml',
	'.txt',
	'.sh',
	'.in',
	'.json',
	'.editorconfig',
}
TEXT_NAMES = {
	'.gitignore',
	'.gitattributes',
	'.vimrc',
}

changed = 0
for path in sorted(ROOT.rglob('*')):
	if any(part in SKIP_DIRS for part in path.parts):
		continue
	if not path.is_file():
		continue
	if path.suffix not in TEXT_SUFFIXES and path.name not in TEXT_NAMES:
		continue

	data = path.read_bytes()
	if b'\0' in data[:1024]:
		continue

	try:
		text = data.decode('utf-8')
	except UnicodeDecodeError:
		continue

	new_text = text.rstrip('\n') + '\n\n'
	if new_text != text:
		path.write_text(new_text, encoding='utf-8')
		changed += 1
		print(path)

print(f'{changed} file(s) updated')
PY

