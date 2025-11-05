#! /usr/bin/env sh

# exit in case of error
set -e

uv venv --clear
source .venv/bin/activate
uv sync

jupyter nbconvert --to notebook --execute notebooks/phase0_kaggle_download.ipynb
rm notebooks/phase0_kaggle_download.nbconvert.ipynb

jupyter nbconvert --to notebook --execute notebooks/phase1_eda.ipynb
rm notebooks/phase1_eda.nbconvert.ipynb

jupyter nbconvert --to notebook --execute notebooks/phase2_model_training.ipynb
rm notebooks/phase2_model_training.nbconvert.ipynb

jupyter nbconvert --to notebook --execute notebooks/phase3_kaggle_submission.ipynb
rm notebooks/phase3_kaggle_submission.nbconvert.ipynb