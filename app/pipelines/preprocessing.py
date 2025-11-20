from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from typing import Tuple
import pandas as pd
import numpy as np

import logging
logger = logging.getLogger(__name__)


class FeatureEngineer(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
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
class LogTransformer(BaseEstimator, TransformerMixin):
    
    def fit(self, y):
        return self

    def transform(self, y):
        y = np.asarray(y)
        return np.log1p(y)

    def inverse_transform(self, y):
        y = np.asarray(y)
        return np.expm1(y)




def get_fitted_pipelines(df: pd.DataFrame) -> Tuple[Pipeline, LogTransformer]:
    df = df.copy()

    feature_engineer = FeatureEngineer()
    fe_df = feature_engineer.transform(df)
    # get numerical and categorical features
    numeric_features = fe_df.select_dtypes(include=['int64', 'float64']).columns.drop('SalePrice')
    categorical_features = fe_df.select_dtypes(include=['string']).columns

    # Create preprocessing pipelines for numeric and categorical data
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(missing_values=pd.NA, strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
    ])

    # build pipelines/transformers
    feature_pipeline = Pipeline([
        ('feature_engineer', FeatureEngineer()),
        ('column_transformer', ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])
        ),
        ])
    target_transformer = LogTransformer()

    # fit pipelines/transformers
    feature_pipeline.fit(df)
    target_transformer.fit(df['SalePrice'])

    return feature_pipeline, target_transformer