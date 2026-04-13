from __future__ import annotations

import pandas as pd
from sklearn.base import ClassifierMixin


def predict(model: ClassifierMixin, features: pd.DataFrame) -> pd.Series:
    """Run model inference and return predicted labels."""
    predictions = model.predict(features)
    return pd.Series(predictions, index=features.index, name="prediction")