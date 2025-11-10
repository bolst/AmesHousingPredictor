from data_ingestion.download_data import DataDownloader
from config.settings import settings


downloader = DataDownloader(settings=settings)
downloader.download_and_extract()