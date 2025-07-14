import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import StandardScaler
import torch

def compute_ccc(y_true, y_pred):
    """Compute Concordance Correlation Coefficient (CCC)"""
    mean_true = torch.mean(y_true)
    mean_pred = torch.mean(y_pred)
    covariance = torch.mean((y_true - mean_true) * (y_pred - mean_pred))
    variance_true = torch.var(y_true)
    variance_pred = torch.var(y_pred)

    ccc = (2 * covariance) / (variance_true + variance_pred + (mean_true - mean_pred) ** 2)
    return ccc.item()

def compute_rmse(y_true, y_pred):
    """Compute Root Mean Square Error (RMSE)"""
    rmse = torch.sqrt(torch.mean((y_true - y_pred) ** 2))
    return rmse.item()

def raw_to_cpm(df):
    column_sums = df.sum(axis=0)
    cpm_df = (df / column_sums) * 1e6
    return cpm_df

def load_data(data, sig, freq, org, normalized=None):
    sig = pd.read_csv(sig, index_col=0)
    sig = sig[~np.all(sig == 0, axis=1)].sort_index()
    sig = pd.DataFrame(stats.zscore(sig, axis=0, ddof=1), index=sig.index, columns=sig.columns)

    data = pd.read_csv(data, index_col=(0))
    data = data[data.index.isin(sig.index)].sort_index()
    data_column = data.index
    data_index = data.columns
    if normalized == False:
        data = raw_to_cpm(data)
    else:
        data
    data = np.log2(data + 1).T
    scaler = StandardScaler()
    data = scaler.fit_transform(data)
    data = pd.DataFrame(data, index=data_index, columns=data_column)

    freq = pd.read_csv(freq, index_col=(0))

    org = pd.read_csv(org, index_col=(0))
    org = org[~org.index.duplicated(keep='first')]
    org = org.reindex(index = sig.index, fill_value = 0).fillna(0).sort_index()
    org_column = org.index
    org_index = org.columns
    if normalized == False:
        org = raw_to_cpm(org)
    else:
        org
    org = np.log2(org + 1).T
    org = scaler.transform(org)
    org = pd.DataFrame(data, index=org_index, columns=org_column)
    
    return data, sig, freq, org
