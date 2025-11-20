from pydantic import BaseModel, Field
from typing import Any, Dict


class PredictionRequest(BaseModel):
    features: Dict[str, Any] = Field(
        ...,
        description="Mapping of raw feature names to values. Matches the training dataset schema.",
    )