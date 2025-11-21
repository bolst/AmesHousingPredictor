import pandas as pd
from pathlib import Path
import numpy as np
from loguru import logger


from ..config.settings import settings

class DataReader:

    def __init__(self):
        self.raw_data_dir = Path(settings.RAW_DATA_DIRECTORY)


    def load_train_test(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        train_path: Path = self.raw_data_dir / "train.csv"
        test_path: Path = self.raw_data_dir / "test.csv"

        train_df = pd.read_csv(train_path, index_col="Id")
        test_df = pd.read_csv(test_path, index_col="Id")

        cols = train_df.select_dtypes('object').columns
        train_df[cols] = train_df[cols].astype('string')
        test_df[cols] = test_df[cols].astype('string')

        train_df = train_df.fillna(np.nan)
        test_df = test_df.fillna(np.nan)

        return train_df, test_df