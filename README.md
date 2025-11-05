# Ames Housing Predictor

## Using notebooks

This project uses [uv](https://github.com/astral-sh/uv) for package management. You can install it by running
This project uses [uv](https://github.com/astral-sh/uv) for package management. You can install it by running

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
uv self update
```
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
uv self update
```

```bash
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv self update
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv self update
```

Once [uv](https://github.com/astral-sh/uv) is installed you just need to create a virtual environment, activate it, and sync
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
2. Build the API container:
   ```bash
   docker build -t ames-housing-api .
   ```
3. Start the container and mount the models directory:
   ```bash
   docker run -p 8000:8000 -v "$(pwd)/models:/models" ames-housing-api
   ```
4. Send a prediction request:
   ```bash
   curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"features": {"OverallQual": 7, "GrLivArea": 1710, "...": "..."}}'
   ```

Environment variables:
- `MODEL_DIR` (default: `/models`) – directory containing the serialized artifacts.
- `MODEL_PATH`, `FEATURE_PREPROCESSOR_PATH`, `TARGET_TRANSFORMER_PATH` – override specific files when needed.

On Railway, create a persistent volume that holds the model artifacts and mount it at `/models`, keeping port `8000` exposed.
