from math import dist

import torch
from scipy.spatial.distance import cosine
from transformers import BertModel, BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')


def get_tokens(sentence: str):
    # Preparing the inputs for a model. Split the sentence into tokens.
    tokens = tokenizer.tokenize(sentence)
    return tokens


def get_convert_tokens_to_ids(tokens):
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


def creating_embedings(tensor, tensors):
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
    return embeddings


def sum_vectors_from_last_four_layers(embeddings):
    # Sum the vectors from the last four layers.
    token_vecs_sum = []
    for token in embeddings:
        sum_vec = torch.sum(token[-4:], dim =0)
        token_vecs_sum.append(sum_vec)
    return token_vecs_sum


def create_embeddings(sentence: str):
    tokens = get_tokens(sentence)
    tokens_ids = get_convert_tokens_to_ids(tokens)
    segments_ids = create_segment_ids(tokens)
    tensor, tensors = create_tensor_and_tensors(tokens_ids, segments_ids)
    embeddings = creating_embedings(tensor, tensors)
    token_vecs_sum = sum_vectors_from_last_four_layers(embeddings)

    return tokens, tokens_ids, segments_ids, tensor, tensors, embeddings, token_vecs_sum


def get_idx_tokens_for_created_relations(tokens, relation):
    idx_tokens = []
    for i, token_str in enumerate(tokens):
        if relation == "subclass of":
            size_token = 3
            if token_str == "sub":
                idx_tokens = range(i, i + size_token, 1)
                return idx_tokens
            
        if relation == "mouth of the watercourse":
            size_token = 6
            if token_str == "mouth":
                idx_tokens = range(i, i + size_token, 1)
                return idx_tokens

        if relation == "dissolved, abolished or demolished":
            print("enter correct if")
            size_token = 5
            if token_str == "dissolved":
                idx_tokens = range(i, i + size_token, 1)
                return idx_tokens
        else:
            size_token = len(relation.split(" "))
            if token_str == relation.split(" ")[0]:
                idx_tokens = range(i, i + size_token, 1)
                return idx_tokens
    


def get_vectors(idx_tokens, token_vecs_sum):
    token_vecs_sum_relation = []
    for id in idx_tokens:
        token_vecs_sum_relation.append(token_vecs_sum[id])

    return token_vecs_sum_relation


def create_mean_torch(token_vecs_sum_relation):
    # Compute the sentence embedding, which is the average embedding of the sentence words.
    sente_embedding = torch.mean(torch.stack(token_vecs_sum_relation),dim =0)
    return sente_embedding


def get_idx_tokens_for_found_relations(tokens_r, relation_found):
    relation_found_tokens = tokenizer.tokenize(relation_found)
    idx_tokens_r = []
    for i_r, token_str_r in enumerate(tokens_r):
        size_relation_r = len(relation_found_tokens)
        if token_str_r == relation_found_tokens[0]:
            if size_relation_r == 1:
                idx_tokens_r=[i_r]
            else:
                tmp_list_r = range(i_r, i_r + size_relation_r, 1)
                idx_tokens_r=tmp_list_r
    print(f"idx_tokens_r: {idx_tokens_r}")

    return idx_tokens_r

def cosine_similarity(sente_embedding, sente_embedding_r):
    # Calculate the cosine similarity in context sentence
    token_vecs_sum_1 = sente_embedding
    token_vecs_sum_2 = sente_embedding_r
    diff_sentences = 1 - cosine(token_vecs_sum_1, token_vecs_sum_2)
    
    return diff_sentences

def euclidian_distance(token_vecs_sum_1,token_vecs_sum_2):
    dist_euclidiana = dist(token_vecs_sum_1,token_vecs_sum_2)

    return dist_euclidiana
