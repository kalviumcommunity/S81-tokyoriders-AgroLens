from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any, TypeVar

T = TypeVar("T")


def save_pickle(obj: Any, path: str | Path) -> None:
    """Save a Python object to disk using pickle."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as file_handle:
        pickle.dump(obj, file_handle)


def load_pickle(path: str | Path) -> Any:
    """Load a Python object from disk using pickle."""
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Artifact not found: {source}")
    with source.open("rb") as file_handle:
        return pickle.load(file_handle)


def load_pickle_typed(path: str | Path, *, expected_type: type[T]) -> T:
    """Load an object and validate its type."""
    obj = load_pickle(path)
    if not isinstance(obj, expected_type):
        raise TypeError(f"Loaded artifact is not a {expected_type.__name__} instance")
    return obj
