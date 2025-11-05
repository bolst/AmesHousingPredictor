#!/usr/bin/env bash

# exit if fail
set -e

# activate
uv venv --clear
source .venv/bin/activate

NOTEBOOKS=(
  "notebooks/phase0_kaggle_download.ipynb"
  "notebooks/phase1_eda.ipynb"
  "notebooks/phase2_model_training.ipynb"
  "notebooks/phase3_kaggle_submission.ipynb"
)

for notebook in "${NOTEBOOKS[@]}"; do
  echo "Executing ${notebook}"
  jupyter nbconvert --execute --to notebook --inplace "${notebook}"
done
