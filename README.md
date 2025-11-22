# Ames Housing Predictor

## Usage

You have two options to run this locally (with or without Docker). You will need the following environment variables. It is suggested to place these in an `.env` file located at the project root.

- `KAGGLE_username` (required): your Kaggle username
- `KAGGLE_key` (required): your Kaggle API key
  - more details on the Kaggle environment variables in [phase 0 notebook](./notebooks/phase0_kaggle_download.ipynb)
- `MLFLOW_BACKEND_URI` (required): URI to the database for logging
- `MLFLOW_TRACKING_URI` (optional): URI to MLflow tracking server
- `MLFLOW_S3_ENDPOINT_URL` (optional): URL to S3 bucket
  - if you set this then you will also need `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`

### Build and run with Docker

```bash
docker compose up --build
```

That's it. MLflow will run at [localhost:8500](http://localhost:8500) and the API will run at [localhost:8000](http://localhost:8000).


### Build and run without Docker


This project uses [uv](https://github.com/astral-sh/uv) for package management. You can install it by running:

```bash
# MacOS or Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
uv self update
```

```bash
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv self update
```

Once [uv](https://github.com/astral-sh/uv) is installed you just need to create a virtual environment, activate it, and sync

```bash
uv venv
source .venv/bin/activate
uv sync
```

Then start MLflow (if you are using a `.env` file, activate it with `source .env`)
```bash
mlflow server --host 0.0.0.0 -p 8500 --backend-store-uri $MLFLOW_BACKEND_URI --default-artifact-root s3://mlflow-artifacts/mlruns --allowed-hosts "*" 
```

followed by the API
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

MLflow will run at [localhost:8500](http://localhost:8500) and the API will run at [localhost:8000](http://localhost:8000).

## Generate a prediction with the API

There is a full payload stored at `examples/sample_request.json` (generated from the first row of `train.csv`). You can use that to try a request for a prediction:
```bash
curl -X POST "http://localhost:8000/predict" \
 -H "Content-Type: application/json" \
 --data examples/sample_request.json
```

Or send your own...
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": {"OverallQual": 7, "GrLivArea": 1710, "YearBuilt": 2003, "Neighborhood": "CollgCr"}}'
```