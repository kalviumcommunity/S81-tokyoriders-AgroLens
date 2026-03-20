# Jupyter Launch and Navigation Verification

Date: 2026-03-20

## 1. Launch Jupyter Notebook from Terminal
Command used from project root:

```powershell
$conda='C:\Users\tarun\miniconda3\Scripts\conda.exe'; Set-Location 'C:\Users\tarun\Desktop\projects\S81-tokyoriders-AgroLens'; & $conda run -n sprint_verify jupyter notebook --no-browser --ip=127.0.0.1 --port=8888 --NotebookApp.token='' --NotebookApp.password=''
```

## 2. Jupyter Home Interface Reachability
Verified URL:

```text
http://127.0.0.1:8888/tree
```

Observed directory entries included:
- `verification/`
- `Readme.md`

This confirms the Jupyter Home (tree) interface is serving the correct project directory.

## 3. Notebook Creation in Correct Folder
Notebook created at:

```text
verification/jupyter_navigation_demo.ipynb
```

## 4. Notebook Execution Proof
Executed code cell output:

```text
Notebook execution OK for S81-tokyoriders-AgroLens
2 + 3 = 5
```

This validates that the notebook runs correctly in this project environment.
