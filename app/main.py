from app.routes import ames, health
from app.data_ingestion.download_data import DataDownloader
from app.data_ingestion.read_data import DataReader
from app.pipelines.preprocessing import get_fitted_pipelines
from app.inference.predict import AmesPredictor
from app.utils.logging_config import setup_logging

from fastapi.staticfiles import StaticFiles
from loguru import logger
from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    # load data
    downloader = DataDownloader()
    downloader.download_and_extract()
    reader = DataReader()
    train, test = reader.load_train_test()
    # get pipelines/transformers/models
    feature_preprocessor, target_transformer = get_fitted_pipelines(train)
    predictor = AmesPredictor(feature_preprocessor)
    # attach to app lifespan
    yield {
        "predictor": predictor,
        "target_transform": target_transformer.inverse_transform,
    }


app = FastAPI(
    title="Ames Housing Price Predictor",
    version="0.1.0",
    description="Predicts sale prices using the trained Ames Housing model.",
    lifespan=lifespan,
)

# add routes
app.include_router(health.health_router)
app.include_router(ames.ames_router)

# mount static files
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")