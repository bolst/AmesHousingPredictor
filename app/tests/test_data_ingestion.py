from app.data_ingestion.download_data import DataDownloader
from app.data_ingestion.read_data import DataReader
from app.config.settings import settings
import pandas as pd


downloader = DataDownloader(settings=settings)
downloader.download_and_extract()

reader = DataReader(settings=settings)
data = reader.load_train_test()

train: pd.DataFrame = data[0]
test: pd.DataFrame = data[1]

assert not train.empty
assert not test.empty