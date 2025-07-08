#!/bin/bash -euxo pipefail
uvx ruff format notebooks/
uvx ruff check notebooks/
