from app.data_ingestion.download_data import DataDownloader
from app.data_ingestion.read_data import DataReader
import pandas as pd

import logging
logging.basicConfig(level=logging.INFO)

downloader = DataDownloader()
downloader.download_and_extract()

reader = DataReader()
data = reader.load_train_test()

train: pd.DataFrame = data[0]
test: pd.DataFrame = data[1]

assert not train.empty
assert not test.empty