import torch.nn as nn
import torch
import torch.nn.functional as F

class AttentionBlock(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super(AttentionBlock, self).__init__()
        self.attn = nn.MultiheadAttention(embed_dim=input_dim, num_heads=8, dropout=0.1)
        self.fc = nn.Linear(input_dim, hidden_dim)

    def forward(self, x):
        attn_output, _ = self.attn(x, x, x)
        return self.fc(attn_output)

class Encoder(nn.Module):
    def __init__(self, input_dim, hidden_dim, attention_dim):
        super(Encoder, self).__init__()
        self.fc1 = nn.Linear(input_dim, 2048)
        self.attention = AttentionBlock(2048, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, 512)
        self.dropout = nn.Dropout(0.1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.attention(x.unsqueeze(0)).squeeze(0)
        x = F.relu(self.fc2(x))
        return self.dropout(x)

class Decoder(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, signature_matrix):
        super(Decoder, self).__init__()
        self.fc2 = nn.Linear(512, 1024)
        self.fc3_fractions = nn.Linear(1024, output_dim)  # Output for cell fractions
        self.gep_matrix = nn.Parameter(torch.randn(input_dim, output_dim))
        self.signature_matrix = signature_matrix  # Store the signature matrix

    def forward(self, x):
        x = F.relu(self.fc2(x))
        cell_fractions = self.fc3_fractions(x)  # Get raw values
        min_vals, _ = cell_fractions.min(dim=-1, keepdim=True)  # Min values per row
        max_vals, _ = cell_fractions.max(dim=-1, keepdim=True)  # Max values per row
        cell_fractions = (cell_fractions - min_vals) / (max_vals - min_vals + 1e-6)
        cell_fractions = cell_fractions / cell_fractions.sum(dim=-1, keepdim=True)  # Normalize rows to sum to 1
        reconstructed_pseudobulk = torch.matmul(cell_fractions, self.signature_matrix.T)
    
        return cell_fractions, reconstructed_pseudobulk, self.gep_matrix

class DeconvolutionModel1(nn.Module):
    def __init__(self, input_dim, hidden_dim, attention_dim, output_dim, signature_matrix):
        super(DeconvolutionModel1, self).__init__()
        self.encoder = Encoder(input_dim, hidden_dim, attention_dim)
        self.decoder = Decoder(input_dim, hidden_dim, output_dim, signature_matrix)

    def forward(self, x):
        encoded = self.encoder(x)
        return self.decoder(encoded)
