import os
from pathlib import Path
from zipfile import ZipFile

import logging
logger = logging.getLogger(__name__)

from ..config.settings import settings

class DataDownloader:
    
    def __init__(self):
        self.kaggle_competition = settings.KAGGLE_COMPETITION
        self.zip_path = Path(settings.KAGGLE_DOWNLOAD_PATH)
        self.data_dir = Path(settings.DATA_DIRECTORY)
        self.raw_data_dir = Path(settings.RAW_DATA_DIRECTORY)


    def download_and_extract(self) -> None:
        logger.info("Authenticating Kaggle...")
        from dotenv import load_dotenv; load_dotenv()
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()

        logger.info("Downloading Kaggle data...")
        api.competition_download_files(self.kaggle_competition, path=self.data_dir)

        logger.info("Extracting zip file...")
        with ZipFile(self.zip_path, 'r') as zipfile:
            zipfile.extractall(self.raw_data_dir)

        os.remove(self.zip_path)
        logger.info(f"Dataset successfully downloaded and extracted to '{self.raw_data_dir}'")