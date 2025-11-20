from argparse import ArgumentError

import mlflow
from mlflow.pyfunc import PyFuncModel

from ..config.settings import settings

import logging
logger = logging.getLogger(__name__)

def get_model(model_name) -> PyFuncModel | None:
    search = mlflow.search_registered_models(filter_string=f"name = '{model_name}'")
    if not search:
        return None

    result = search[0]
    if not result.latest_versions:
        return None

    model = mlflow.pyfunc.load_model(result.latest_versions[0].source)
    return model


class AmesPredictor:

    def __init__(
            self,
            feature_engineer,
            tracking_uri: str = settings.MLFLOW_TRACKING_URI,
            model_name: str = settings.PROD_MODEL_NAME,
            model = None
    ):
        self.feature_engineer = feature_engineer
        self.tracking_uri = tracking_uri

        mlflow.set_tracking_uri(tracking_uri)
        if model is not None:
            self.model = model
        else:
            self.model = get_model(model_name)
            if self.model is None:
                raise ArgumentError("There was an error loading the model")

    def predict(self, data, target_transform = None):
        processed_data = self.feature_engineer.transform(data)
        prediction = self.model.predict(processed_data)
        return prediction if target_transform is None else target_transform(prediction)
