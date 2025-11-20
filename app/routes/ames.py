from app.schemas.requests import PredictionRequest
from app.schemas.responses import PredictionResponse

from fastapi import APIRouter, Request, HTTPException
import pandas as pd

import logging
logger = logging.getLogger(__name__)

ames_router = APIRouter(prefix="/api", tags=["api_v1"])

@ames_router.post("/prediction")
def predict(request: Request, input_data: PredictionRequest):
    """
    Endpoint that accepts feature data, runs the data through the model,
    and returns a sale price prediction.
    """
    if request.state.predictor.model is None:
        raise HTTPException(
            status_code=500,
            detail="Model artifacts failed to load. Check application logs for details.",
        )

    try:
        raw_frame = pd.DataFrame([input_data.features])
        prediction = request.state.predictor.predict(raw_frame, target_transform=request.state.target_transform)
        print(f"prediction: {prediction}")
    except Exception as exc:  # noqa: BLE001
        logger.exception("Prediction failed")
        raise HTTPException(status_code=400, detail=f"Failed to generate prediction: {exc}") from exc

    return PredictionResponse(prediction=float(prediction.flat[0]), model_path='???')