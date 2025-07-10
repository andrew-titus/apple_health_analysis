#!/bin/bash -euxo pipefail
echo "Checking src..."
uvx ruff format src/
uvx ruff check --fix src/

echo "Checking notebooks..."
uvx ruff format notebooks/
uvx ruff check --fix notebooks/

echo "DONE!"
