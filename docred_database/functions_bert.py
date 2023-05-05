import torch
from transformers import BertModel, BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def get_tokens(sentence: str):
    # Preparing the inputs for a model. Split the sentence into tokens.
    tokens = tokenizer.tokenize(sentence)
    return tokens

def convert_tokens_to_ids(tokens):
    # Map the token strings to their vocabulary indeces.
    tokens_ids = tokenizer.convert_tokens_to_ids(tokens)
    # print(f"tokens_ids: {tokens_ids}")
    return tokens_ids

def create_segment_ids(tokens):
    # Mark each of the 22 tokens as belonging to sentence "1".
    segments_ids = [1] * len(tokens)
    # print(f"segments_ids: {segments_ids}")
    return segments_ids

def create_tensor_and_tensors(tokens_ids, segments_ids):
    tensor = torch.tensor([tokens_ids])
    # print(f"tensor: {tensor}")
    tensors = torch.tensor([segments_ids])
    # print(f"tensors: {tensors}")
    return tensor, tensors

# Load pre-trained model (weights)
model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)

with torch.no_grad():
    outputs = model(tensor, tensors)
    hidden_states = outputs [2]

# Concatenando uma sequência de vetores
embeddings = torch.stack(hidden_states, dim =0)
# print(f"embeddings: {embeddings}")
# Reduz a dimensãodo vetor para um melhor processamento
embeddings = torch.squeeze(embeddings, dim =1)
# print(f"embeddings: {embeddings}")
# Returns a view of the original tensor input with its dimensions permuted.
embeddings = embeddings.permute(1,0,2)
# print(f"embeddings: {embeddings}")