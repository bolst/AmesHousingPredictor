import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class MyFeatureEngineer(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        # Total Square Footage
        df['TotalSF'] = df['GrLivArea'] + df['TotalBsmtSF']
        df.drop(['GrLivArea', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 
                'TotalBsmtSF', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF'], axis=1, inplace=True)
        return df
