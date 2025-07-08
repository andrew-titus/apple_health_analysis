#!/bin/bash -euxo pipefail
uvx ruff check
uvx pynblint notebooks/
