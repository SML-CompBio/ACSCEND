import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
import torch.optim as optim
from .utils import compute_ccc, compute_rmse, load_data
from .model import DeconvolutionModel1
import pandas as pd
import numpy as np
from scipy.stats import rankdata, zscore
import joblib
import os

def deconvolution_train(data, sig, freq, org, normalized):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    X_train, X_val, Y_train, Y_val = train_test_split(data.to_numpy(), freq.to_numpy(), test_size=0.2, random_state=42)
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32).to(device)
    Y_train_tensor = torch.tensor(Y_train, dtype=torch.float32).to(device)
    X_val_tensor = torch.tensor(X_val, dtype=torch.float32).to(device)
    Y_val_tensor = torch.tensor(Y_val, dtype=torch.float32).to(device)

    sig_tensor = torch.tensor(sig.values, dtype=torch.float32).to(device)
    X_test_tensor = torch.tensor(org.values, dtype=torch.float32).to(device)

    input_dim = X_train.shape[1]
    output_dim = Y_train.shape[1] 
    hidden_dim = 512
    attention_dim = 2048
    signature_dim = output_dim
    
    model1 = DeconvolutionModel1(input_dim, hidden_dim, attention_dim, output_dim, sig_tensor).to(device)
    loss_function = nn.MSELoss()
    optimizer1 = optim.Adam(model1.parameters(), lr=0.0001)


    l1 = 0.01 # Kl_div loss
    l2 = 0.005 # pseudobulk_reconstruction_loss
    l3 = 0.005  #pseudo loss1
    l4 = 1  #sig_gep_loss


    num_epochs = 100
    kl_loss_function = nn.KLDivLoss(reduction="batchmean")
    print('Model Training Started')
    for epoch in range(num_epochs):
        model1.train()
        cell_fractions_pred, reconstructed1, gep_predictions1 = model1(X_train_tensor)

        train_loss1 = loss_function(cell_fractions_pred, Y_train_tensor)
        pseudobulk_reconstruction_loss1 = loss_function(X_train_tensor, reconstructed1)
        pseudo_bulk_pred_gep_and_Y_train1 = torch.matmul(Y_train_tensor, gep_predictions1.T)
        loss_pseudo_gep1 = loss_function(X_train_tensor, pseudo_bulk_pred_gep_and_Y_train1)
        loss_gep_sig1 = loss_function(gep_predictions1, sig_tensor)
        prior = torch.full_like(Y_train_tensor, fill_value=1.0 / output_dim).to(device)
        kl_div_loss1 = kl_loss_function(torch.log_softmax(cell_fractions_pred, dim=-1), prior)
        loss_ccc = 1 - compute_ccc(Y_train_tensor, cell_fractions_pred)
        total_loss1 = train_loss1 + l1 * kl_div_loss1 + l2 * pseudobulk_reconstruction_loss1 + l3 * loss_pseudo_gep1 + l4 * loss_gep_sig1

        optimizer1.zero_grad()
        total_loss1.backward()
        optimizer1.step()
        model1.eval()
    
        with torch.no_grad():
            val_cell_fractions1, val_reconstructed1, val_gep1 = model1(X_val_tensor)
            val_loss1 = loss_function(val_cell_fractions1, Y_val_tensor)
            val_ccc1 = compute_ccc(Y_val_tensor, val_cell_fractions1)
            val_rmse1 = compute_rmse(Y_val_tensor, val_cell_fractions1)

        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch + 1}/{num_epochs}], Train Loss: {total_loss1.item():.4f}, Val Loss: {val_loss1.item():.4f}, CCC: {val_ccc1:.4f}, RMSE: {val_rmse1:.4f}')

    
    return model1, sig_tensor, X_test_tensor, input_dim, output_dim


def Deconvoluter(data, sig, freq, org, normalized=True):
    data, sig, freq, org = load_data(data, sig, freq, org, normalized)
    model1, sig_tensor, X_test_tensor, input_dim, output_dim = deconvolution_train(data, sig, freq, org, normalized)
    model1.eval()
    with torch.no_grad():
        test_cell_fractions, _, _ = model1(X_test_tensor)
    test_cell_fractions_df = test_cell_fractions.detach().cpu().numpy()
    test_cell_fractions_df = pd.DataFrame(test_cell_fractions_df, index=org.index, columns=sig.columns)
    return test_cell_fractions_df
    
class Predictor:
    def __init__(self):
        # Load the model from the same directory as this script
        self.model = joblib.load(os.path.join(os.path.dirname(__file__), 'lr_model.joblib'))
        self.scaler = joblib.load(os.path.join(os.path.dirname(__file__), 'lr_scaler.joblib'))
        self.feature_names = self.model.feature_names_in_
        self.label_mapping = {0: 'Pluripotent', 1: 'Multipotent', 2: 'Unipotent'}

    def preprocess_data(self, data):
        # Load data from CSV file

        # Reindex columns to match the model's expected features and fill missing columns with zeros
        data = data.reindex(columns=self.feature_names, fill_value=0).fillna(0)

        # Keep the original column and index names for consistency
        data_col = data.columns
        data_ind = data.index

        # Rank the data and scale it
        data = rankdata(data * -1, axis=1, method='average')
        data = np.log2(data + 1)
        data = pd.DataFrame(data, columns=data_col, index=data_ind)
        data = self.scaler.transform(data)
        data = pd.DataFrame(data, columns=data_col, index=data_ind)

        return data, data_ind

    def predict(self, data, prob=False):
        # Preprocess the input data
        test_data, data_ind = self.preprocess_data(data)
        # Return prediction probabilities if prob=True, else return predictions
        if prob:
            probabilities = self.model.predict_proba(test_data)
            probabilities = pd.DataFrame(probabilities, index=data_ind, columns=['Pluripotent', 'Multipotent', 'Unipotent'])
            return probabilities
        else:
            predictions = self.model.predict(test_data)
            predictions = [self.label_mapping[pred] for pred in predictions]
            predictions = pd.DataFrame(predictions, index=data_ind, columns=['Stem Cell Class'])
            return predictions

    def __call__(self, data_path, prob=False):
        # Allow the object to be called like a function
        return self.predict(data_path, prob)
