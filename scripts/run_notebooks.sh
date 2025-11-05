#!/usr/bin/env bash

set -euo pipefail

NOTEBOOKS=(
  "notebooks/1_data_ingestion.ipynb"
  "notebooks/2_feature_engineering.ipynb"
  "notebooks/3_model_training.ipynb"
)

for notebook in "${NOTEBOOKS[@]}"; do
  echo "Executing ${notebook}"
  jupyter nbconvert --execute --to notebook --inplace "${notebook}"
done
