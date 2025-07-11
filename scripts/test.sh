#!/bin/bash -euxo pipefail
uv run pytest --cov=src --cov-report term-missing:skip-covered tests/
