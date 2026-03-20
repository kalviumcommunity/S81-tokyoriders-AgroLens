# AgroLens - Part A README Documentation

## 1. Project Intent and High-Level Flow

The core problem this project targets is practical uncertainty: farmers make crop and selling decisions before they know future demand, price movement, and climate stress. The intent is not only to predict a number, but to support better decisions under risk. In this context, the central question is: *Which crop and timing choices are most likely to give stable returns in the coming season for a given region?*

The high-level data science workflow reflected by the sample-style repository is typically:

1. Frame the decision question and define success criteria.
2. Gather and combine relevant evidence (market, weather, yield, and local context data).
3. Explore and clean the data to understand quality limits and hidden patterns.
4. Build and evaluate models or analytical logic.
5. Translate outputs into recommendations that a farmer or advisor can act on.

The lifecycle connection is important: question quality decides data relevance, data quality limits model trust, and model results only become useful when converted into interpretable insight. A good repository structure usually mirrors this progression from raw evidence to decision-ready outputs rather than jumping directly to modeling.

## 2. Repository Structure and File Roles

In a standard data science repository, major folders usually represent different kinds of work:

- `data/`: Source files, staged datasets, and cleaned datasets. This is the evidence layer and often the most sensitive to accidental corruption.
- `notebooks/`: Exploratory analysis, profiling, and hypothesis testing. This is where ideas evolve and intermediate observations are documented.
- `scripts/` or `src/`: Reusable, production-style logic for cleaning, feature engineering, training, and evaluation. This should be more stable than notebooks.
- `outputs/` or `reports/`: Generated charts, metrics, model artifacts, and summaries used for communication.

Exploratory work differs from finalized analysis mainly in purpose and stability. Exploration is iterative and often messy by design (trying many paths quickly). Finalized analysis should be reproducible, reviewed, and organized so another contributor can run it with predictable results.

A new contributor should be cautious in three places:

- Raw data files: changing or overwriting these can break traceability.
- Shared pipeline scripts: small edits can silently change downstream results.
- Notebook outputs: committing large or stale outputs can create noise and hide real code changes.

## 3. Assumptions, Gaps, and Open Questions

### Assumptions likely present

- Historical patterns in mandi prices and weather are informative for near-term forecasts.
- Data from public sources is sufficiently accurate and timely for district-level decisions.
- Regional aggregates can still provide meaningful guidance to individual farmers.

### Gaps or unclear points

- Data update frequency and lag are often not clearly documented.
- Feature definitions (for example, what exactly counts as demand pressure) may be implicit.
- The intended decision user (individual farmer, FPO, or policy officer) is sometimes not explicitly defined.
- Reproducibility steps are frequently incomplete (environment setup, run order, and expected outputs).

### One improvement

Add a short **"How to Reproduce End-to-End"** section with:

1. Required environment and dependencies.
2. Input data expectations (schema, date range, source links).
3. Exact execution order (exploration optional, pipeline mandatory).
4. Where final outputs appear and how to interpret them.

This single addition would make the repository easier for reviewers to validate and for new contributors to extend.

## 4. Environment Verification (Python, Conda, Jupyter)

Verification date: `2026-03-20`

### Python is installed and callable

Command used:

```powershell
c:/Users/tarun/Desktop/projects/S81-tokyoriders-AgroLens/.venv/Scripts/python.exe --version
```

Observed result:

```text
Python 3.14.0
```

### Conda is installed and environments work

Conda executable used:

```text
C:\Users\tarun\miniconda3\Scripts\conda.exe
```

Commands used:

```powershell
C:\Users\tarun\miniconda3\Scripts\conda.exe --version
C:\Users\tarun\miniconda3\Scripts\conda.exe env list
C:\Users\tarun\miniconda3\Scripts\conda.exe create -n sprint_verify python=3.11 -y
C:\Users\tarun\miniconda3\Scripts\conda.exe run -n sprint_verify python --version
```

Observed results:

```text
conda 26.1.1
Python 3.11.15
```

### Jupyter launches and executes Python code

Jupyter package check command:

```powershell
C:\Users\tarun\miniconda3\Scripts\conda.exe run -n sprint_verify jupyter --version
```

Notebook execution check command:

```powershell
C:\Users\tarun\miniconda3\Scripts\conda.exe run -n sprint_verify python -c "import nbformat; from nbclient import NotebookClient; nb=nbformat.read('verification/jupyter_smoke.ipynb', as_version=4); NotebookClient(nb, timeout=120, kernel_name='python3').execute(); outs=nb.cells[0].get('outputs', []); print('cell_output:', outs[0].get('text','').strip() if outs else 'NO_OUTPUT')"
```

Observed result:

```text
cell_output: sum: 12
```

This confirms a Jupyter-backed kernel can execute Python code successfully.

## 5. Data Science Project Folder Structure

The repository now uses a clear data science structure so data, experiments, reusable code, and outputs do not mix.

```text
S81-tokyoriders-AgroLens/
  data/
    raw/
    processed/
    output/
  notebooks/
    exploration/
    final/
  scripts/
    data_prep/
    modeling/
  outputs/
    figures/
    reports/
  verification/
```

### Why this structure matters

- `data/raw/` keeps untouched source data for traceability and must remain unmodified.
- `data/processed/` stores cleaned and transformed datasets generated from raw inputs.
- `data/output/` stores final data products used by reports, dashboards, or downstream use.
- `notebooks/exploration/` is for trial-and-error analysis and quick hypothesis checks.
- `notebooks/final/` is for cleaner, presentation-ready notebooks with stable results.
- `scripts/data_prep/` holds reusable preprocessing logic instead of copy-pasting notebook code.
- `scripts/modeling/` separates training/evaluation logic from exploration.
- `outputs/figures/` and `outputs/reports/` centralize non-tabular deliverables.

This separation improves reproducibility, preserves source integrity, reduces accidental overwrites, and makes onboarding easier because contributors can quickly find where each type of work belongs.