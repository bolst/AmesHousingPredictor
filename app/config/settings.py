import os, json
from loguru import logger
from dataclasses import dataclass, asdict
from dotenv import load_dotenv
load_dotenv()

@dataclass
class AppSettings:
    DATA_DIRECTORY: str = os.getenv("DATA_DIRECTORY") or "data"
    RAW_DATA_DIRECTORY: str = os.getenv("RAW_DATA_DIRECTORY") or "data/raw"
    PROCESSED_DATA_DIRECTORY: str = os.getenv("PROCESSED_DATA_DIRECTORY") or "data/processed"

    KAGGLE_COMPETITION: str = os.getenv("KAGGLE_COMPETITION") or "house-prices-advanced-regression-techniques"
    KAGGLE_DOWNLOAD_PATH: str = os.getenv("KAGGLE_DOWNLOAD_PATH") or f"{DATA_DIRECTORY}/{KAGGLE_COMPETITION}.zip"

    PROD_MODEL_NAME: str = os.getenv("PROD_MODEL_NAME") or "prod"

    LOG_LEVEL: str = os.getenv("LOG_LEVEL") or "INFO"
    LOG_FILE: str = os.getenv("LOG_FILE") or "logs/app.log"


    # for some reason pandas/sklearn has very ambiguous NaN handling...
    # e.g., if we have a NaN in a string column doing df['string_col'] == pd.NA doesn't return True
    # you'd typically do df.isna() or something but we can't use that for pipelines
    # use this as workaround
    CATEGORICAL_NAN: str = "N/A"


    # MLflow settings
    MLFLOW_EXPERIMENT_NAME: str = os.getenv("MLFLOW_EXPERIMENT_NAME") or "ames-housing-pricing-experiment"
    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI") or "http://127.0.0.1:8500"

# ----------------------------------

settings = AppSettings()
logger.debug(f"loaded settings: {json.dumps(asdict(settings), indent=4)}")