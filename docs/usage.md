# Usage

OncoMark provides a Python API for two core functionalities:

1. **Stem Cell Type Classification** – Classifies transcriptomic samples into one of three categories:  
    - *Pluripotent*  
    - *Multipotent*  
    - *Unipotent*

2. **Transcriptomic Deconvolution** – Estimates and quantifies the relative proportions of different cell types within bulk RNA-seq samples.

This page outlines the steps for using both modules with example data and scripts.

---

## 📁 Example Data

Example input files for testing can be found in the `test` directory of the GitHub repository:

- `classifier_test.csv` – For cell-type classification
- `PBMC_PSEUDOBULK.csv` – Bulk RNA-seq input data
- `signature_matrix_pbmc.csv` – Signature matrix for deconvolution
- `cell_fractions_PBMC.csv` – True cell-type frequencies (optional)
- `PBMC_PSEUDOBULK_INDEPENDENT.csv` – Independent test data

---

## 🛠️ Installation

Install the `ACSCeND` package:

```bash
pip install ACSCeND
````

---

## 📦 Step 1: Import Required Modules

Start by importing the required classes from the package. Make sure your transcriptomics data is loaded into a `pandas.DataFrame`.

```python
import pandas as pd
from ACSCeND import Predictor, Deconvoluter
```

---

## 🔬 Step 2a: Stem Cell Type Classification

The `Predictor` class allows you to classify transcriptomic samples into stem cell types.

> ⚠️ **Note**: The classifier handles all necessary preprocessing internally. You may use either raw counts or normalized expression data.
> ❗ Do **not** use the raw model file from GitHub directly — the Python API is required to ensure preprocessing and normalization are done correctly.

### ✅ Example Usage

```python
# Load sample input data
df_pred = pd.read_csv('classifier_test.csv', index_col=0)

# Initialize classifier
predictor = Predictor()

# Predict stem cell type (returns class labels)
predictions = predictor('classifier_test.csv', prob=False)
print(predictions)

# Predict class probabilities
probabilities = predictor('classifier_test.csv', prob=True)
print(probabilities)
```

---

## 🧬 Step 2b: Bulk RNA-seq Deconvolution

The `Deconvoluter` class can be used to infer cell-type compositions from bulk RNA-seq samples.

### ✅ Required Inputs

* `data` – Bulk RNA-seq gene expression matrix (samples × genes)
* `sig` – Signature gene expression matrix (cell types × genes)
* `freq` – Known cell-type fractions (for evaluation; optional)
* `org` – Independent bulk test dataset
* `normalized` – Whether the input data is already normalized (`True`/`False`)

### ✅ Example Usage

```python
# File paths
data_path = 'PBMC_PSEUDOBULK.csv'
signature_path = 'signature_matrix_pbmc.csv'
true_frequencies = 'cell_fractions_PBMC.csv'
independent_data = 'PBMC_PSEUDOBULK_INDEPENDENT.csv'

# Run deconvolution (set normalized=False for raw counts)
org_freq, org_gep = Deconvoluter(
    data_path,
    signature_path,
    true_frequencies,
    independent_data,
    normalized=False
)

# org_freq contains the estimated cell-type frequencies for each bulk sample
print(org_freq)
```

---

## 📎 Notes

* Input gene expression data should be in the form of a `.csv` file where rows are **genes** and columns are **samples**.
* Ensure consistent gene naming across bulk data and signature matrices.
* If you're running on a large dataset, ensure enough memory is available for processing.

---

## 📚 References

* For full details and source code: [ACSCeND GitHub Repository](https://github.com/SML-CompBio/ACSCeND)
* Package: [`ACSCeND`](https://pypi.org/project/ACSCeND)

```
