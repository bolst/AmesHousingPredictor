from argparse import ArgumentError
from loguru import logger
import mlflow
from mlflow.pyfunc import PyFuncModel

from ..config.settings import settings



def get_model(model_name) -> PyFuncModel | None:
    try:
        search = mlflow.search_registered_models(filter_string=f"name = '{model_name}'")
        if not search:
            logger.error(f"Could not find any models with the name {model_name}")
            return None

        result = search[0]
        if not result.latest_versions:
            logger.error(f"No versions found for {model_name}")
            return None

        source = result.latest_versions[0].source
        model = mlflow.pyfunc.load_model(source)
        logger.info(f"loaded model with id {model.model_id}")
        return model
    except Exception as exc:
        logger.error(f"exception loading model {model_name}: {exc}")
        return None


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
        self.model_name = model_name

        mlflow.set_tracking_uri(tracking_uri)
        logger.info(f"mlflow tracking uri set to {tracking_uri}")
        self.model = model or get_model(model_name)

    def predict(self, data, target_transform = None):
        # try to get the model if not gotten in constructor
        self.model = get_model(self.model_name)
        if self.model is None:
            raise ModuleNotFoundError("Failed to load model. Check logs for details")
        processed_data = self.feature_engineer.transform(data)
        prediction = self.model.predict(processed_data)
        return prediction if target_transform is None else target_transform(prediction)
