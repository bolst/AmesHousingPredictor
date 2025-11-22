from app.schemas.requests import PredictionRequest
from app.schemas.responses import PredictionResponse
from loguru import logger
from fastapi import APIRouter, Request, HTTPException
import pandas as pd


ames_router = APIRouter(prefix="/api", tags=["api_v1"])

@ames_router.post("/prediction")
def predict(request: Request, input_data: PredictionRequest):
    """
    Endpoint that accepts feature data, runs the data through the model,
    and returns a sale price prediction.
    """
    try:
        raw_frame = pd.DataFrame([input_data.features])
        prediction = request.state.predictor.predict(raw_frame, target_transform=request.state.target_transform)
        print(f"prediction: {prediction}")
    except Exception as exc:  # noqa: BLE001
        logger.exception("Prediction failed")
        raise HTTPException(status_code=400, detail=f"Failed to generate prediction: {exc}") from exc

    return PredictionResponse(prediction=float(prediction.flat[0]), model_path='???')