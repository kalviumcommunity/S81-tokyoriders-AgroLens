from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


def project_root() -> Path:
    """Return the repository root (parent of the `src/` package folder)."""
    return Path(__file__).resolve().parents[1]


ROOT_DIR = project_root()

DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

MODELS_DIR = ROOT_DIR / "models"
REPORTS_DIR = ROOT_DIR / "reports"
LOGS_DIR = ROOT_DIR / "logs"

DEFAULT_MODEL_PATH = MODELS_DIR / "model.pkl"
DEFAULT_PREPROCESSOR_PATH = MODELS_DIR / "preprocessor.pkl"
DEFAULT_PREDICTIONS_PATH = REPORTS_DIR / "predictions.csv"
DEFAULT_EVALUATION_REPORT_PATH = REPORTS_DIR / "evaluation_report.json"
DEFAULT_EXPERIMENT_LOG_PATH = LOGS_DIR / "experiment_log.csv"

DEFAULT_RANDOM_STATE = 42
DEFAULT_TEST_SIZE = 0.2


@dataclass(frozen=True)
class Paths:
    """Optional convenience wrapper for standard project paths."""

    root_dir: Path = ROOT_DIR
    data_dir: Path = DATA_DIR
    raw_data_dir: Path = RAW_DATA_DIR
    processed_data_dir: Path = PROCESSED_DATA_DIR
    external_data_dir: Path = EXTERNAL_DATA_DIR
    models_dir: Path = MODELS_DIR
    reports_dir: Path = REPORTS_DIR
    logs_dir: Path = LOGS_DIR
