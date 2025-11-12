from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class FeatureEngineer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, df: pd.DataFrame):
        df = df.copy()
        # Total Square Footage
        df['TotalSF'] = df['GrLivArea'] + df['TotalBsmtSF']
        df.drop(['GrLivArea', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 
                'TotalBsmtSF', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF'], axis=1, inplace=True)
        
        # Total Bathrooms
        df['TotalBathrooms'] = df['FullBath'] + df['BsmtFullBath'] + \
            0.5 * (df['HalfBath'] + df['BsmtHalfBath'])
        df.drop(['FullBath', 'BsmtFullBath', 'HalfBath', 'BsmtHalfBath'], axis=1, inplace=True)

        # Has Fireplace
        df['HasFireplace'] = (df['Fireplaces'] > 0).astype(int)
        df.drop(['Fireplaces'], axis=1, inplace=True)

        # drop poorly correlated values
        df.drop(['PoolQC', 'Alley', 'Fence'], axis=1, inplace=True)

        return df
    

# transformer for target variable SalePrice
import numpy as np
class LogTransformer(BaseEstimator, TransformerMixin):
    def fit(self, y):
        return self

    def transform(self, y):
        y = np.asarray(y)
        return np.log1p(y)

    def inverse_transform(self, y):
        y = np.asarray(y)
        return np.expm1(y)
