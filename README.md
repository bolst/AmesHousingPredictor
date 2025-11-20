# Ames Housing Predictor

## Using notebooks

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

## Serving the model via Docker

1. Run the training workflow so the following artifacts exist in the `models/` directory:
   - `feature_preprocessor.joblib`
   - `target_transformer.joblib` (optional but recommended)
   - `optimized_xgboost.joblib` (falls back to `baseline_xgboost.joblib` if present)
2. Build and run the API:
   ```bash
   docker compose up
   ```
3. Send a prediction request with inline JSON:
   ```bash
   curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"features": {"OverallQual": 7, "GrLivArea": 1710, "YearBuilt": 2003, "Neighborhood": "CollgCr"}}'
   ```
4. Or use the full example payload stored at `examples/sample_request.json` (generated from the first row of `train.csv`):
   ```bash
   curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     --data-binary @examples/sample_request.json
   ```

Environment variables:
- `MODEL_PATH`, `FEATURE_PREPROCESSOR_PATH`, `TARGET_TRANSFORMER_PATH` – override specific files when needed.
- `FRONTEND_API_URL` – endpoint that the in-browser estimator should call (defaults to `http://127.0.0.1:8000/predict`). Store this in your `.env` (or export it) and run Uvicorn with `--env-file .env` so FastAPI can inject it into the HTML before serving it.

On Railway, create a persistent volume that holds the model artifacts and mount it at `/models`, keeping port `8000` exposed.

## Running the UI locally

1. Ensure you have the backend running (either via Docker as above or directly with uv):
   ```bash
   uv venv
   source .venv/bin/activate
   uv sync
   uvicorn app.main:app --env-file .env --reload
   ```
2. Visit `http://localhost:8000/` in your browser. FastAPI serves `frontend/index.html` and injects the `FRONTEND_API_URL` value automatically, so the UI always sends predictions to the backend you configured.
3. Adjust sliders, click **Predict**, and the price card updates with the latest estimate.
