from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.base import RegressorMixin


def evaluate_regression_model(
    model: RegressorMixin,
    x_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict[str, float]:
    """Evaluate a trained regressor and return standard regression metrics."""
    predictions = model.predict(x_test)
    mse = mean_squared_error(y_test, predictions)
    rmse = float(np.sqrt(mse))
    mae = mean_absolute_error(y_test, predictions)

    # r2_score warns when fewer than 2 samples are present.
    if len(y_test) < 2:
        r2 = float("nan")
    else:
        r2 = r2_score(y_test, predictions)

    return {
        "mse": float(mse),
        "rmse": rmse,
        "mae": float(mae),
        "r2": float(r2),
    }
