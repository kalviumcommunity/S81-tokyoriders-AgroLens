from __future__ import annotations

import argparse
from pathlib import Path

from .config import (
    DEFAULT_MODEL_PATH,
    DEFAULT_PREDICTIONS_PATH,
    DEFAULT_PREPROCESSOR_PATH,
    DEFAULT_RANDOM_STATE,
    DEFAULT_TEST_SIZE,
)
from .prediction_pipeline import run_prediction_pipeline
from .training_pipeline import run_training_pipeline


def print_metrics(metrics: dict[str, float | str]) -> None:
    """Print evaluation metrics in a compact and readable form."""
    print("Training pipeline completed successfully.")
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1 score:  {metrics['f1_score']:.4f}")
    print("\nClassification report:")
    print(metrics["classification_report"])


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for training and prediction flows."""
    parser = argparse.ArgumentParser(description="AgroLens modular ML entry point")
    subparsers = parser.add_subparsers(dest="command", required=True)

    train_parser = subparsers.add_parser("train", help="Train model and save artifacts")
    train_parser.add_argument("--data-path", type=str, default=None, help="Optional CSV path")
    train_parser.add_argument("--target-column", type=str, default=None, help="Target column name")
    train_parser.add_argument(
        "--model-path",
        type=str,
        default=str(DEFAULT_MODEL_PATH),
        help="Destination path for trained model",
    )
    train_parser.add_argument(
        "--preprocessor-path",
        type=str,
        default=str(DEFAULT_PREPROCESSOR_PATH),
        help="Destination path for fitted preprocessor",
    )
    train_parser.add_argument(
        "--test-size",
        type=float,
        default=float(DEFAULT_TEST_SIZE),
        help="Proportion of data held out for testing (0-1)",
    )
    train_parser.add_argument(
        "--random-state",
        type=int,
        default=int(DEFAULT_RANDOM_STATE),
        help="Random seed for reproducible splitting",
    )
    train_parser.add_argument(
        "--time-column",
        type=str,
        default=None,
        help="Optional column name for chronological splitting (time-series)",
    )

    predict_parser = subparsers.add_parser("predict", help="Run inference from saved artifacts")
    predict_parser.add_argument("--data-path", type=str, required=True, help="CSV path for inference")
    predict_parser.add_argument(
        "--target-column",
        type=str,
        default=None,
        help="Optional target column to drop if present",
    )
    predict_parser.add_argument(
        "--model-path",
        type=str,
        default=str(DEFAULT_MODEL_PATH),
        help="Path to trained model",
    )
    predict_parser.add_argument(
        "--preprocessor-path",
        type=str,
        default=str(DEFAULT_PREPROCESSOR_PATH),
        help="Path to fitted preprocessor",
    )
    predict_parser.add_argument(
        "--output-path",
        type=str,
        default=str(DEFAULT_PREDICTIONS_PATH),
        help="Destination for predictions CSV",
    )

    return parser.parse_args()


def main() -> None:
    """Execution entry point for the command line interface."""
    arguments = parse_args()

    if arguments.command == "train":
        metrics = run_training_pipeline(
            data_path=arguments.data_path,
            target_column=arguments.target_column,
            model_output_path=arguments.model_path,
            preprocessor_output_path=arguments.preprocessor_path,
            test_size=arguments.test_size,
            random_state=arguments.random_state,
            time_column=arguments.time_column,
        )
        print_metrics(metrics)
        print(f"Model saved to: {Path(arguments.model_path)}")
        print(f"Preprocessor saved to: {Path(arguments.preprocessor_path)}")
        return

    prediction_frame = run_prediction_pipeline(
        data_path=arguments.data_path,
        model_path=arguments.model_path,
        preprocessor_path=arguments.preprocessor_path,
        target_column=arguments.target_column,
        output_path=arguments.output_path,
    )
    print("Prediction pipeline completed successfully.")
    print(f"Predictions generated: {len(prediction_frame)}")
    print(f"Output saved to: {Path(arguments.output_path)}")


if __name__ == "__main__":
    main()