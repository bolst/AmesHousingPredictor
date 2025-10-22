import pandas as pd
import json

train_df = pd.read_csv('./data/house-prices-advanced-regression-techniques/train.csv')

from fastapi import FastAPI, APIRouter
app = FastAPI()
router = APIRouter()



@router.get('/')
def root():
    return {'message': 'hello there'}



@router.get('/houses')
def get_houses(offset: int = 0, limit: int = 50):
    df = train_df.iloc[offset : offset + limit]
    jsonStr = df.to_json(orient='records')
    houses = json.loads(jsonStr)
    return {
        'houses': houses,
        'offset': offset,
        'limit': limit,
        'total': train_df.shape[0]
    }



app.include_router(router)