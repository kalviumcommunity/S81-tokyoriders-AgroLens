from __future__ import annotations

import argparse
from pathlib import Path

from .config import DEFAULT_MODEL_PATH, DEFAULT_PREPROCESSOR_PATH
from .training_pipeline import run_training_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AgroLens training entry point")
    parser.add_argument("--data-path", type=str, default=None, help="Optional CSV path")
    parser.add_argument(
        "--target-column",
        type=str,
        default=None,
        help="Target column name (optional for demo yield_kg)",
    )
    parser.add_argument(
        "--model-path",
        type=str,
        default=str(DEFAULT_MODEL_PATH),
        help="Destination path for trained model",
    )
    parser.add_argument(
        "--preprocessor-path",
        type=str,
        default=str(DEFAULT_PREPROCESSOR_PATH),
        help="Destination path for fitted preprocessor",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metrics = run_training_pipeline(
        data_path=args.data_path,
        target_column=args.target_column,
        model_output_path=Path(args.model_path),
        preprocessor_output_path=Path(args.preprocessor_path),
    )

    print("Training completed.")
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1 score:  {metrics['f1_score']:.4f}")


if __name__ == "__main__":
    main()
