from app.routes import ames, health
from app.data_ingestion.download_data import DataDownloader
from app.data_ingestion.read_data import DataReader
from app.pipelines.preprocessing import get_fitted_pipelines
from app.inference.predict import AmesPredictor
from app.utils.logging_config import setup_logging

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

app.include_router(health.health_router)
app.include_router(ames.ames_router)


import os
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
INDEX_PATH = FRONTEND_DIR / "index.html"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="frontend-static")


@app.get("/", include_in_schema=False, response_class=HTMLResponse)
def serve_frontend() -> HTMLResponse:
    if not INDEX_PATH.exists():
        raise HTTPException(status_code=404, detail="Frontend not built")
    api_url = os.getenv("FRONTEND_API_URL", "http://127.0.0.1:8000/predict")
    html = INDEX_PATH.read_text().replace("__API_URL__", api_url)
    return HTMLResponse(html)