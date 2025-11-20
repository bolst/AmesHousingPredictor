from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ames_predictor")

app = FastAPI(
    title="Ames Housing Price Predictor",
    version="0.1.0",
    description="Predicts sale prices using the trained Ames Housing model.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionRequest(BaseModel):
    features: Dict[str, Any] = Field(
        ...,
        description="Mapping of raw feature names to values. Matches the training dataset schema.",
    )


class PredictionResponse(BaseModel):
    prediction: float = Field(..., description="Predicted sale price.")
    model_path: str = Field(..., description="Filesystem path of the model used for inference.")


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
INDEX_PATH = FRONTEND_DIR / "index.html"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="frontend-static")


@app.get("/", include_in_schema=False, response_class=HTMLResponse)
def serve_frontend() -> HTMLResponse:
    if not INDEX_PATH.exists():
        raise HTTPException(status_code=404, detail="Frontend not built")
    api_url = os.getenv("FRONTEND_API_URL", "http://127.0.0.1:8000/predict")
    html = INDEX_PATH.read_text().replace("__API_URL__", api_url)
    return HTMLResponse(html)


def _resolve_path(env_key: str, default: Path) -> Path:
    """Read a path from the environment or fall back to the provided default."""
    override = os.getenv(env_key)
    return Path(override) if override else default


def _load_model_artifacts() -> tuple[Any, Any, Optional[Any], Path]:
    """Load the preprocessor, model, and optional target transformer from disk."""
    model_dir = _resolve_path("MODEL_DIR", Path("models"))

    feature_preprocessor_path = _resolve_path(
        "FEATURE_PREPROCESSOR_PATH", model_dir / "feature_preprocessor.joblib"
    )
    target_transformer_path = _resolve_path(
        "TARGET_TRANSFORMER_PATH", model_dir / "target_transformer.joblib"
    )

    candidate_paths = [
        model_dir / "optimized_xgboost.joblib",
        model_dir / "baseline_xgboost.joblib",
    ]

    model_path = next((candidate for candidate in candidate_paths if candidate and candidate.exists()), None)
    if not model_path:
        raise FileNotFoundError(
            "No trained model artifact found. Ensure the training pipeline has written "
            "an XGBoost model to the models directory."
        )

    if not feature_preprocessor_path.exists():
        raise FileNotFoundError(
            f"Feature preprocessor missing at {feature_preprocessor_path}. "
            "Run the feature engineering pipeline before starting the API."
        )

    feature_preprocessor = joblib.load(feature_preprocessor_path)
    model = joblib.load(model_path)

    target_transformer = None
    if target_transformer_path.exists():
        target_transformer = joblib.load(target_transformer_path)
    else:
        logger.warning(
            "Target transformer not found at %s. Predictions will be returned without inverse transformation.",
            target_transformer_path,
        )

    logger.info("Loaded model from %s", model_path)
    return feature_preprocessor, model, target_transformer, model_path


FEATURE_PREPROCESSOR, MODEL, TARGET_TRANSFORMER, MODEL_PATH = _load_model_artifacts()


@app.get("/health", response_model=dict[str, str])
def healthcheck() -> dict[str, str]:
    """
    Healthcheck endpoint to verify that the service is running.
    """
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    """
    Endpoint that accepts feature data, runs the data through the model,
    and returns a sale price prediction.
    """
    if FEATURE_PREPROCESSOR is None or MODEL is None:
        raise HTTPException(
            status_code=500,
            detail="Model artifacts failed to load. Check application logs for details.",
        )

    try:
        raw_frame = pd.DataFrame([request.features])
        transformed_features = FEATURE_PREPROCESSOR.transform(raw_frame)
        prediction = MODEL.predict(transformed_features)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Prediction failed")
        raise HTTPException(status_code=400, detail=f"Failed to generate prediction: {exc}") from exc

    prediction = np.asarray(prediction, dtype=float).reshape(-1, 1)
    if TARGET_TRANSFORMER is not None and hasattr(TARGET_TRANSFORMER, "inverse_transform"):
        try:
            prediction = TARGET_TRANSFORMER.inverse_transform(prediction)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Target inverse transformation failed")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to apply target inverse transformation: {exc}",
            ) from exc

    return PredictionResponse(prediction=float(prediction.flat[0]), model_path=str(MODEL_PATH))
