from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class FeatureEngineer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):  # noqa: N802
        return self

    def transform(self, df: pd.DataFrame):  # noqa: N802
        df = df.copy()
        df["TotalSF"] = df["GrLivArea"] + df["TotalBsmtSF"]
        df.drop(
            [
                "GrLivArea",
                "1stFlrSF",
                "2ndFlrSF",
                "LowQualFinSF",
                "TotalBsmtSF",
                "BsmtFinSF1",
                "BsmtFinSF2",
                "BsmtUnfSF",
            ],
            axis=1,
            inplace=True,
        )

        df["TotalBathrooms"] = (
            df["FullBath"]
            + df["BsmtFullBath"]
            + 0.5 * (df["HalfBath"] + df["BsmtHalfBath"])
        )
        df.drop(["FullBath", "BsmtFullBath", "HalfBath", "BsmtHalfBath"], axis=1, inplace=True)

        df["HasFireplace"] = (df["Fireplaces"] > 0).astype(int)
        df.drop(["Fireplaces"], axis=1, inplace=True)

        df.drop(["PoolQC", "Alley", "Fence"], axis=1, inplace=True)

        return df


class LogTransformer(BaseEstimator, TransformerMixin):
    def fit(self, y: Any):  # noqa: N802
        return self

    def transform(self, y):  # noqa: N802
        y = np.asarray(y)
        return np.log1p(y)

    def inverse_transform(self, y):  # noqa: N802
        y = np.asarray(y)
        return np.expm1(y)


__all__ = ["FeatureEngineer", "LogTransformer"]
