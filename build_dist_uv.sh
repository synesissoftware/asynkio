#! /bin/bash

set -e

cd "$(dirname "$0")"

if [ ! -d .venv ]; then
    uv venv
fi

rm -rf build/ dist/ asynkio.egg-info/

uv pip install build twine
.venv/bin/python -m build
.venv/bin/twine check dist/*
