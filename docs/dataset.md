# Datasets and Training

## Classification

### Datasets
| Source        | Type        | Use        | Cell Type        | Count | Paper DOI                                         | Author            |
|---------------|-------------|------------|------------------|------------|---------------------------------------------------|-------------------|
| GSE36552      | hESC        | Validation | Embryonic         | 124        | [https://doi.org/10.1038/nsmb.2660](https://doi.org/10.1038/nsmb.2660) | Yan et al.        |
| GSM3370006    | hESC        | Validation | Embryonic         | 370        | [https://doi.org/10.1038/s41467-020-16214-8](https://doi.org/10.1038/s41467-020-16214-8) | Lau et al.        |
| E-MTAB-3929   | hESC        | Training   | Embryonic         | 1356       | [https://doi.org/10.1016/j.cell.2016.03.023](https://doi.org/10.1016/j.cell.2016.03.023) | Petropoulos et al.|
| E-MTAB-6819   | hESC        | Training   | Embryonic         | 1462       | [https://doi.org/10.1016/j.celrep.2018.12.099](https://doi.org/10.1016/j.celrep.2018.12.099) | Messmer et al.    |
| GSM5519457    | hMSC        | Training   | Dermis            | 15563      | [https://doi.org/10.1002/ctm2.650](https://doi.org/10.1002/ctm2.650) | Wang et al.       |
| GSM5519466    | hMSC        | Training   | Adipose           | 9039       | [https://doi.org/10.1002/ctm2.650](https://doi.org/10.1002/ctm2.650) | Wang et al.       |
| GSM5519456    | hMSC        | Validation | Dermis            | 24241      | [https://doi.org/10.1002/ctm2.650](https://doi.org/10.1002/ctm2.650) | Wang et al.       |
| GSM5519465    | hMSC        | Validation | Adipose           | 12740      | [https://doi.org/10.1002/ctm2.650](https://doi.org/10.1002/ctm2.650) | Wang et al.       |
| GSE221853     | hMSC        | Training   | Neuron            | 5859       | [https://doi.org/10.1038/s41467-024-47945-7](https://doi.org/10.1038/s41467-024-47945-7) | Guerrero et al.   |
| GSE147482     | hMSC        | Training   | Skin              | 486        | [https://doi.org/10.1038/s41467-020-18075-7](https://doi.org/10.1038/s41467-020-18075-7) | Wang et al.       |
| GSE248995     | hUSC        | Training   | Neuron            | 63         | [https://doi.org/10.1016/j.isci.2024.109342](https://doi.org/10.1016/j.isci.2024.109342) | Baig et al.       |
| GSE136831     | hUSC        | Training   | Lung              | 1154       | [https://doi.org/10.1126/sciadv.aba1983](https://doi.org/10.1126/sciadv.aba1983) | Adams et al.      |
| GSE143704     | hUSC        | Training   | Satellite Cells   | 2757       | [https://doi.org/10.1186/s13395-020-00236-3](https://doi.org/10.1186/s13395-020-00236-3) | Micheli et al.    |
| Dryad         | hUSC        | Validation | Satellite Cells   | 65085      | [https://doi.org/10.7554/elife.51576](https://doi.org/10.7554/elife.51576) | Barruet et al.    |
| GSE97390      | Mix         | Validation | Mouse             | 3379       | [https://doi.org/10.7554/elife.26945](https://doi.org/10.7554/elife.26945) | Briggs et al.     |

### Workflow

1. **Aggregation of Experimentally Annotated Datasets**  
    - Datasets were aggregated from multiple publicly available sources to train the classifier model.
    - The aggregation included ensuring consistency and quality control measures.

- **SCENT Score Calculation**  
    - The SCENT score was calculated for all samples to assess their biological consistency.
    - Samples with original annotations misaligned with their SCENT score were removed, improving dataset accuracy.

- **Handling Class Imbalance**  
    - A class imbalance was identified: Multipotent samples were approximately 8 times more abundant than Pluripotent and Unipotent samples.
    - To address this, we employed an **ensemble learning strategy**.
      - Eight distinct ensemble models were trained, each with shared Pluripotent and Unipotent samples but unique subsets of Multipotent samples, balancing the dataset across models.

- **Conversion to Rank Space**  
    - All gene expression data was transformed to rank space to:
        - Remove batch effects.
        - Mitigate the influence of extreme values and outliers.
        - Reduce the risk of overfitting.
    - This transformation normalized gene expression differences across samples for consistent downstream analysis.

- **Log2 Transformation**  
    - Rank-transformed data was then log2-transformed to compress the scale of gene expression data.

- **Standardization to Z-Scores**  
    - The log2-transformed data was standardized by converting to z-scores, ensuring all variables had a mean of zero and a standard deviation of one.
    - This final step facilitated uniformity and improved model performance during training.

- **Model Validation on Independent Datasets**  
    - To ensure robustness and prevent overfitting, traditional k-fold cross-validation was avoided as it can introduce bias when biological replicates are present in both training and validation sets, leading to double-dipping.
    - Instead, models were validated on completely independent datasets from different sources to ensure an unbiased evaluation of model performance.
    - The trained models were evaluated for their ability to generalize to novel, unseen data.

- **SCENT-Based Smoothening and Test Data Integrity**  
    - SCENT-based smoothening was not applied to the test data to maintain the integrity of the unseen test data during prediction, ensuring accurate evaluation.

- **Model Selection**  
    - Five different models were developed, and the one demonstrating the highest accuracy on the independent test dataset was selected for subsequent analysis.

## Deconvolution

### Datasets
The single-cell RNA sequencing (scRNA-seq) gene expression matrix for various cancer types was obtained from the publicly available [**Weizmann Institute's 3CA dataset**](https://www.weizmann.ac.il/sites/3CA/), which contains high-resolution data on cancer-associated cell types.

### Workflow

---

#### Data Preprocessing
Preprocessing was performed using the **Seurat package (v5.1.0) in R** to ensure stringent quality control. The following steps were applied:

1. Initial Filtering
    - **Cells with fewer than 200 genes** were excluded to avoid low-quality cells.
    - **Cells with more than 6,000 genes** were removed to eliminate potential doublets.
    - Cells with a **mitochondrial gene fraction >10%** were excluded to remove dying or stressed cells.

2. Doublet Removal
    - The **DoubletFinder package (v2.0)** was used for doublet detection and removal.
    - **Optimal pK parameter** was determined using the `paramSweep` function, and `find.pK` was used to summarize results.
    - Adjustments were made for **homotypic doublets** using the `nExp_poi.adj` parameter.
    - Classified doublets were removed, leaving only high-confidence singlets for downstream analysis.

---

#### Malignant and Stromal Cell Annotation
- Annotations for non-immune populations (malignant cells, fibroblasts, epithelial cells, endothelial cells) were preserved from the **Weizmann Institute’s 3CA dataset**.

---

#### Immune Cell Annotation
- The **SCINA (Semi-supervised Category Identification and Assignment) package** was employed for immune cell classification.
- The **LM22 matrix** (from the study by Newman et al.) was used as the reference for major immune populations (T cells, B cells, macrophages, NK cells).
- **Custom MDSC markers** were curated from external studies (cite: [Science paper on MDSCs]) and combined with the LM22 matrix for MDSC identification.

---

#### Cancer Stem Cell (CSC) Annotation

1. Isolation of Malignant Cells
    - The **annotation of CSCs** was restricted to malignant cells only to distinguish them from normal stem cells in cancer tissues.

2. Data Normalization
    - The **NormalizeData** function was used to normalize gene expression using the **LogNormalize** method (scales gene expression levels by a factor of 10,000, followed by log transformation).

3. Detection of Variable Features
    - **FindVariableFeatures** detected the top 2,000 highly variable genes using the **variance-stabilizing transformation (vst)** method.

4. Data Scaling
    - **ScaleData** was used to standardize expression levels, reducing bias from overrepresented genes.

5. Dimensionality Reduction
    - **Principal Component Analysis (PCA)** was performed using the top 2,000 highly variable genes, retaining the first 20 principal components (PCs).

6. Batch Effect Correction
    - **RunHarmony** from the **Harmony package** was employed to correct batch effects, preserving biological variation.

7. Clustering
    - The **FindNeighbors** function constructed a nearest neighbor graph.
    - **FindClusters** applied the **Louvain algorithm** (resolution = 0.3) to partition cells into clusters.

8. Marker Expression Visualization
    - **Violin plots** were generated to visualize known cancer stem cell markers in each cancer type across clusters.

9. UCell Analysis
    - **UCell** was used to calculate enrichment scores based on **stem cell marker genes** tailored to each cancer type.
    - Clusters with high **UCell scores** and **elevated stem cell marker expression** were identified as potential CSC clusters.