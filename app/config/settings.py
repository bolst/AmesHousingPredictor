from dataclasses import dataclass, field


@dataclass
class AppSettings:
    DATA_DIRECTORY: str = "data"
    RAW_DATA_DIRECTORY: str = "data/raw"
    PROCESSED_DATA_DIRECTORY: str = "data/processed"

    KAGGLE_COMPETITION: str = "house-prices-advanced-regression-techniques"
    KAGGLE_DOWNLOAD_PATH: str = f"{DATA_DIRECTORY}/{KAGGLE_COMPETITION}.zip"


    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"


    # MLflow settings
    MLFLOW_EXPERIMENT_NAME: str = "ames-housing-pricing-experiment"
    MLFLOW_TRACKING_URI: str = "sqlite:///mlflow.db"
    MLRUNS_PATH: str = "mlruns"

# ----------------------------------

settings = AppSettings()