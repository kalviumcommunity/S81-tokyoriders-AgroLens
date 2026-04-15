# outputs/

Legacy/optional folder for generated materials.

This repository’s ML pipelines write their primary artifacts to:
- `models/` (trained model + preprocessor)
- `reports/` (evaluation reports + predictions)
- `logs/` (experiment logs)

`outputs/` is kept for non-pipeline assets such as figures or older coursework outputs.
To avoid duplication and confusion, the pipelines do not mirror artifacts into `outputs/`.
