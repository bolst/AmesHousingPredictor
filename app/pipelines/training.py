import mlflow
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from ..config.settings import settings

import logging
logger = logging.getLogger(__name__)


def evaluate_model(model, X, y, prefix=''):
    y_pred = model.predict(X)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    return {
        f'{prefix}rmse': rmse,
        f'{prefix}mae': mae,
        f'{prefix}r2': r2
    }


class XGBModelTrainer:

    def __init__(
            self,
            experiment_name: str = settings.MLFLOW_EXPERIMENT_NAME,
            tracking_uri: str = settings.MLFLOW_TRACKING_URI
    ):
        self.experiment_name = experiment_name
        self.tracking_uri = tracking_uri
        self.train_metrics = None
        self.val_metrics = None
        self.model_info = None

        mlflow.set_tracking_uri(tracking_uri)
        self.experiment = mlflow.set_experiment(experiment_name)

    
    def train(self, model, model_name: str, X_train, y_train, X_test, y_test):
        with mlflow.start_run(run_name = f"train-run-{model_name}"):
            # train model
            model.fit(
                X_train, 
                y_train,
                eval_set=[(X_test, y_test)],
                verbose=100
            )
            
            # get metrics
            self.train_metrics = evaluate_model(model, X_train, y_train, prefix='train_')
            self.val_metrics = evaluate_model(model, X_test, y_test, prefix='val_')

            # log to mlflow
            mlflow.log_params(model.get_params())
            mlflow.log_metrics({**self.train_metrics, **self.val_metrics})
            self.model_info = mlflow.xgboost.log_model(
                model,
                name=model_name,
                registered_model_name=model_name,
                input_example=X_train
            )
            
            logger.info("\nTraining Metrics:")
            for metric, value in self.train_metrics.items():
                logger.info(f"{metric}: {value:.4f}")
            
            logger.info("\nValidation Metrics:")
            for metric, value in self.val_metrics.items():
                logger.info(f"{metric}: {value:.4f}")
        
            return model
