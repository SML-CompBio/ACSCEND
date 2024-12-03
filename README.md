# AI-based Cancer Stem Cell profiler and Neoplasia Deconvoluter (ACSCeND)

**ACSCeND** is a Python package designed to analyze and process stem cell transcriptomics data. It includes two core modules for predicting stem cell subtypes and deconvoluting bulk RNA-seq data using deep learning.

## Features

1. **Stem Cell Subtypes Predictor**  
   Identify stem cell subtypes — Pluripotent, Multipotent, or Unipotent — from single-cell stem cell transcriptomics data.

2. **Deep Learning-based Deconvoluter**  
   Deconvolute bulk RNA-seq data into meaningful components using cutting-edge deep learning techniques.

---

## Installation

Install ACSCeND using pip:

```bash
pip install ACSCeND
```

---

## Documentation

Comprehensive documentation is available at:  
[ACSCeND Documentation](https://acscend.readthedocs.io/en/latest/)

---

## Usage

### Stem Cell Subtypes Predictor

```python
from ACSCeND import Predictor

# Example usage
predictor = Predictor()
subtypes = predictor(input_data)
```

### Deep Learning-based Deconvoluter

```python
from ACSCeND import Deconvoluter

# Example usage
real_freq, real_gep = Deconvoluter(pseudo_data, sig_matrix, pseudo_freq, real_data, normalized=False)
```

For detailed examples and API reference, visit the [documentation](https://acscend.readthedocs.io/en/latest/).

---

## Suggestions and Issues

We welcome suggestions and issues! If you have any ideas or feedback to improve ACSCeND, please reach out to [Shreyansh Priyadarshi](mailto:shreyansh.priyadarshi02@gmail.com).
If you find any bugs or have problems when you are using ACSCeND, feel free to raise issues.

---

## Citation
```bibtex
@article {ACSCeND,
	author = {Chowdhury*, Debojyoti and Priyadarshi*, Shreyansh and Biswas, Sayan and Neekhra, Bhavesh and Gupta, Debayan and Haldar, Shubhasis},
	title = {Comprehensive Enumeration of Cancer Stem-like Cell Heterogeneity Using Deep Neural Network},
	elocation-id = {2024.11.26.625418},
	year = {2024},
	doi = {10.1101/2024.11.26.625418},
	publisher = {Cold Spring Harbor Laboratory},
	URL = {https://www.biorxiv.org/content/early/2024/12/01/2024.11.26.625418},
	eprint = {https://www.biorxiv.org/content/early/2024/12/01/2024.11.26.625418.full.pdf},
	journal = {bioRxiv}
}
