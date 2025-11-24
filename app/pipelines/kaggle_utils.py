from typing import Literal
from ..config.settings import settings
from loguru import logger

import os
import pandas as pd
from datetime import datetime
from time import sleep
from dotenv import load_dotenv

from kaggle.api.kaggle_api_extended import ApiCreateSubmissionResponse


def get_kaggle_api():
    load_dotenv()
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    return api



def submit_to_kaggle(data: pd.DataFrame, competition: str = settings.KAGGLE_COMPETITION) -> ApiCreateSubmissionResponse | Literal['Could not submit to competition']:
    api = get_kaggle_api()

    # format data for submission
    if 'Id' not in list(data.columns) or 'SalePrice' not in list(data.columns):
        raise ValueError("Dataframe columns must contain 'Id' and 'SalePrice'")
    data = data[['Id', 'SalePrice']]
    
    now = datetime.now().strftime("%D_%T").replace('/', '-')
    
    # save submission file
    os.makedirs('../submissions', exist_ok=True)
    submission_filename = f"submission_{now}.csv"
    submission_path = f"../submissions/{submission_filename}"
    data.to_csv(submission_path, index=False)
    logger.debug(f"Kaggle submission file saved to {submission_path}")
    
    # submit to Kaggle
    message = f"submission {now}"
    logger.debug(f"Submitting {message} to Kaggle")
    response = api.competition_submit(submission_path, message, competition)
    return response



def get_kaggle_submission_score(submission_ref: str, competition: str = settings.KAGGLE_COMPETITION) -> float:
    api = get_kaggle_api()
    
    leaderboard = api.competition_submissions(competition)
    submission = [s for s in leaderboard if s.ref == submission_ref][0]

    # get submission score
    sleep(3)
    leaderboard = api.competition_submissions(competition)
    if not leaderboard or not (submission := [s for s in leaderboard if s.ref == submission_ref][0]):
        raise ValueError(f"No submissions found with ref {submission_ref}")
    
    score = submission.public_score
    return score