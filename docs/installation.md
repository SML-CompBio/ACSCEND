## Installation
ACSCeND is based on the deep learning framework [PyTorch](https://pytorch.org). It is important for users to choose the suitable version of PyTorch based on different compute platforms. The [official instruction](https://pytorch.org/get-started/locally/) may help you install PyTorch correctly.

### Step 1: Create a Python 3.13.0 Environment
You can use either `conda` or Python's built-in `venv` to create an isolated environment.

#### Option A: Using Conda
⚠️ Requires [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/)
```bash
# Create and activate a new conda environment
conda create -n acscend_env python=3.13.0
conda activate acscend_env
```

#### Option B: Using venv
⚠️ Requires Python 3.13.0 to be installed and available as python3.13
```bash
# Create and activate a new virtual environment
python3.13 -m venv acscend_env
source acscend_env/bin/activate       # On Windows: acscend_env\Scripts\activate
```

### Step 2: Install Required Dependencies

```bash
pip install pandas==2.3.1 \
            numpy==2.3.1 \
            torch==2.7.1 \
            scikit-learn==1.7.0 \
            joblib==1.5.1 \
            scipy==1.16.0
```

### Step 3: Install ACSCeND
After successfully installing PyTorch and Required Dependencies, you can install ACSCeND directly from PyPI:

```bash
# pip
pip install ACSCeND
```

You’re all set! Start exploring the features of ACSCeND.

---
