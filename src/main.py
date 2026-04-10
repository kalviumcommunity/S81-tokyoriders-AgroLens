from __future__ import annotations

import argparse

from data_loader import load_data
from evaluate import evaluate_model
from model import train_model
from preprocessing import preprocess_data


def run_pipeline(data_path: str | None = None, target_column: str | None = None) -> dict[str, float | str]:
    """Run the complete ML workflow and return evaluation metrics."""
    features, target = load_data(data_path=data_path, target_column=target_column)
    x_train, x_test, y_train, y_test, _ = preprocess_data(features, target)
    trained_model = train_model(x_train, y_train)
    metrics = evaluate_model(trained_model, x_test, y_test)

    print("ML pipeline completed successfully.")
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1 score:  {metrics['f1_score']:.4f}")
    print("\nClassification report:")
    print(metrics["classification_report"])

    return metrics


def parse_args() -> argparse.Namespace:
    """Parse optional command line arguments."""
    parser = argparse.ArgumentParser(description="Run a modular ML pipeline.")
    parser.add_argument(
        "--data-path",
        type=str,
        default=None,
        help="Optional CSV path. If omitted, synthetic data is generated.",
    )
    parser.add_argument(
        "--target-column",
        type=str,
        default=None,
        help="Target column name when using --data-path.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    run_pipeline(data_path=arguments.data_path, target_column=arguments.target_column)