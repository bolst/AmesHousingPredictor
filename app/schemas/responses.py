from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    prediction: float = Field(..., description="Predicted sale price.")
    model_path: str = Field(..., description="Filesystem path of the model used for inference.")