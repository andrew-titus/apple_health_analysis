#!/bin/bash -euxo pipefail
echo "Clearing notebook outputs..."
uv run --with jupyter jupyter nbconvert --clear-output --inplace notebooks/*

echo "Running ruff..."
for subdir in src tests notebooks; do
    echo "-> Checking ${subdir}..."
    uvx ruff format "${subdir}/"
    uvx ruff check --fix "${subdir}/"
done
echo "DONE!"
