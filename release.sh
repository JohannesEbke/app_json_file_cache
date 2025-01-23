#!/bin/bash
set -eux

python -m pip install --upgrade flake8 yapf pytest twine
python -m pip install -e .
pytest
flake8
yapf -d -r app_json_file_cache/

rm -rf dist/
python -m build
twine check dist/*
twine upload dist/*
