import torch
from transformers import BertModel, BertTokenizer

paragraph = "Niklas Bergqvist ( born 6 October 1962 in Stockholm ) , is a Swedish songwriter , producer and musician .His career started in 1984 , as a founding member of the Synthpop band Shanghai , which he started along his school friends .The band released two albums and numerous singles , with their debut single ' Ballerina ' , produced by former Europe guitarist Kee Marcello .Following the success of the single , the album also gained positive attention , resulting in the band touring around Sweden .The second , and final , studio album was produced by Swedish pop star Harpo .After the band split - up in 1987 , Bergqvist formed and played in several other bands until he decided to focus more on songwriting , resulting in several releases ever since .In 2015 , he founded the independent record label Tracks of Sweden with songwriting partner Simon Johansson ."
entity_0 = "Niklas Bergqvist"
entity_1 = "Stockholm"
relation_annotated = "place of birth"
relation_found = "born in"

tokenizer = BertTokenizer.from_pretrained ('bert-base-uncased')

token_vecs_sum = []
for relation in [relation_annotated, relation_found]:
    print(f"tokenizer: {tokenizer}")
    # Preparing the inputs for a model. Split the sentence into tokens.
    tokens = tokenizer.tokenize(relation)
    print(f"tokens: {tokens}")
    # Map the token strings to their vocabulary indeces.
    tokens_ids = tokenizer.convert_tokens_to_ids(tokens)
    print(f"tokens_ids: {tokens_ids}")

    # Mark each of the 22 tokens as belonging to sentence "1".
    segments_ids = [1] * len(tokens)
    print(f"segments_ids: {segments_ids}")
    tensor = torch.tensor([tokens_ids])
    print(f"tensor: {tensor}")
    tensors = torch.tensor([segments_ids])
    print(f"tensors: {tensors}")

    # Load pre-trained model (weights)
    model = BertModel.from_pretrained('bert-base-uncased',output_hidden_states=True)

    with torch.no_grad():
        outputs = model(tensor, tensors)
        hidden_states = outputs [2]

    # Concatenando uma sequência de vetores
    embeddings = torch.stack(hidden_states, dim =0)
    print(f"embeddings: {embeddings}")
    # Reduz a dimensãodo vetor para um melhor processamento
    embeddings = torch.squeeze(embeddings, dim =1)
    print(f"embeddings: {embeddings}")
    # Returns a view of the original tensor input with its dimensions permuted.
    embeddings = embeddings.permute(1,0,2)
    print(f"embeddings: {embeddings}")
    token_vecs_sum = []
    # # Sum the vectors from the last four layers.
    for token in embeddings:
        sum_vec = torch.sum(token[ -4:] ,dim =0)
        token_vecs_sum.append(sum_vec)

    # Compute the sentence embedding, which is the average embedding of the sentence words.
    sente_embedding = torch.mean(torch.stack(token_vecs_sum),dim =0)


    print(f"sente_embedding: {sente_embedding}")
    token_vecs_sum.append(token_vecs_sum)

from scipy.spatial.distance import cosine
# Calculate the cosine similarity between the word bank 
# in "bank robber" vs "river bank" (different meanings).
token_vecs_sum_1 = token_vecs_sum[0]
token_vecs_sum_2 = token_vecs_sum[1]
diff_sentences = 1 - cosine(token_vecs_sum_1, token_vecs_sum_2)
print('Vector similarity for  *similar*  meanings:  %.2f' % diff_sentences)
