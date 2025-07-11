#!/bin/bash -euxo pipefail
for subdir in src tests notebooks; do
    echo "Checking ${subdir}..."
    uvx ruff format "${subdir}/"
    uvx ruff check --fix "${subdir}/"
done
echo "DONE!"
