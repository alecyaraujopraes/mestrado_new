import torch
from transformers import BertModel, BertTokenizer


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
tokens = tokenizer.tokenize(sentence)
tokens_ids = tokenizer.convert_tokens_to_ids(tokens)
segments_ids = [1] * len (tokens)
tensor = torch.tensor([tokens_ids])
tensors = torch.tensor([segments_ids])
model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)

with torch.no_grad():
    outputs = model(tensor,tensors)
    hidden_states = outputs[2]

embeddings = torch.stack(hidden_states, dim =0)
embeddings = torch.squeeze(embeddings, dim =1)
embeddings = embeddings.permute(1,0,2)
token_vecs_sum = []

for token in embeddings :
    sum_vec = torch.sum(token[ -4:], dim =0)
    token_vecs_sum.append(sum_vec)

sente_embedding = torch.mean(torch.stack(token_vecs_sum ), dim =0)
