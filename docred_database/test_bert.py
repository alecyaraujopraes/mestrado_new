import torch
from transformers import BertModel, BertTokenizer
from scipy.spatial.distance import cosine
import csv
from math import dist

# paragraph = "Niklas Bergqvist ( born 6 October 1962 in Stockholm ) , is a Swedish songwriter , producer and musician .His career started in 1984 , as a founding member of the Synthpop band Shanghai , which he started along his school friends .The band released two albums and numerous singles , with their debut single ' Ballerina ' , produced by former Europe guitarist Kee Marcello .Following the success of the single , the album also gained positive attention , resulting in the band touring around Sweden .The second , and final , studio album was produced by Swedish pop star Harpo .After the band split - up in 1987 , Bergqvist formed and played in several other bands until he decided to focus more on songwriting , resulting in several releases ever since .In 2015 , he founded the independent record label Tracks of Sweden with songwriting partner Simon Johansson ."
# entity_0 = "Niklas Bergqvist"
# entity_1 = "Stockholm"
# relation_annotated = "place of birth"
# relation_found = "born in"
paragraph = "Juan Guzmán ( born Hans Gutmann Guster , also known as "" Juanito "" , 28 October 1911 – 1982 ) was a German born Mexican photojournalist .He was known as a war photographer of the Spanish Civil War and later on his work with Mexican painters Frida Kahlo and Diego Rivera .Hans Gutmann was born in Cologne .In 1936 he joined the Spanish Civil War as a volunteer of the International Brigades .Gutmann later became a Spanish citizen and changed his name to Juan Guzmán .There are more than 1,300 photographs from the Spanish Civil War in the archive of Agencia EFE ( Madrid ) .His most famous image is the picture of 17-year - old Marina Ginestà standing in top of Hotel Colón in Barcelona .It is one of the most iconic photographs of the Spanish Civil War .After the war Guzmán fled to Mexico , where he arrived in 1940 .He worked for major Mexican magazines and newspapers and became a friend of Frida Kahlo with whom Guzmán shared similar political views .In the 1950s he took a large number of photographs of Kahlo and her husband Diego Rivera .Guzmán also photographed the artwork of Mexican painters like Gerardo Murillo , Jesús Reyes Ferreira and José Clemente Orozco .Juan Guzmán died in Mexico City in 1982 ."
# entity_0 = "Frida Kahlo"
# entity_1 = "Diego Rivera"
# relation_annotated = "spouse"
relation_found = "her husband"
# paragraph = "Mário Cravo Neto ( Salvador , April 20 , 1947 — Salvador , August 9 , 2009 ) was a Brazilian photographer , sculptor and draughtsman .Mário Cravo , son of the sculptor Mário Cravo Júnior , is considered one of the most important photographers of Brazil .Since his early life , he was in contact with circle of artists and , when an adolescent , he met with Pierre Verger , friend of his father .In 1968 , he studied for two years at the Art Students League of New York .After that , he returned to Brazil and first exhibits the sculptures created in New York at the 12th São Paulo Art Biennial .He worked mainly with black - and - white photography , and representing the religion of Candomble .In 2005 , he exhibited at Rencontres d'Arles festival .He died in 2009 in Salvador due to skin cancer .Neto is the father of Brazilian photographer Christian Cravo .","Mário Cravo Neto ( Salvador , April 20 , 1947 — Salvador , August 9 , 2009 ) was a Brazilian photographer , sculptor and draughtsman .",
# entity_0 = "Mário Cravo Neto"
# entity_1 = "Mário Cravo Júnior"
# relation_annotated = "father"

possible_relations = {
    "P6": "head of government", 
    "P17": "country", 
    "P19": "place of birth", 
    "P20": "place of death", 
    "P22": "father", 
    "P25": "mother", 
    "P26": "spouse", 
    "P27": "country of citizenship", 
    "P30": "continent", 
    "P31": "instance of", 
    "P35": "head of state", 
    "P36": "capital", 
    "P37": "official language", 
    "P39": "position held", 
    "P40": "child", 
    "P50": "author", 
    "P54": "member of sports team", 
    "P57": "director", 
    "P58": "screenwriter", 
    "P69": "educated at", 
    "P86": "composer", 
    "P102": "member of political party", 
    "P108": "employer", 
    "P112": "founded by", 
    "P118": "league", 
    "P123": "publisher", 
    "P127": "owned by", 
    "P131": "located in the administrative territorial entity", 
    "P136": "genre", 
    "P137": "operator", 
    "P140": "religion", 
    "P150": "contains administrative territorial entity", 
    "P155": "follows", 
    "P156": "followed by", 
    "P159": "headquarters location", 
    "P161": "cast member", 
    "P162": "producer", 
    "P166": "award received", 
    "P170": "creator", 
    "P171": "parent taxon", 
    "P172": "ethnic group", 
    "P175": "performer", 
    "P176": "manufacturer", 
    "P178": "developer", 
    "P179": "series", 
    "P190": "sister city", 
    "P194": "legislative body", 
    "P205": "basin country", 
    "P206": "located in or next to body of water", 
    "P241": "military branch", 
    "P264": "record label", 
    "P272": "production company", 
    "P276": "location", 
    "P279": "subclass of", 
    "P355": "subsidiary", 
    "P361": "part of", 
    "P364": "original language of work", 
    "P400": "platform", 
    "P403": "mouth of the watercourse", 
    "P449": "original network", 
    "P463": "member of", 
    "P488": "chairperson", 
    "P495": "country of origin", 
    "P527": "has part", 
    "P551": "residence", 
    "P569": "date of birth", 
    "P570": "date of death", 
    "P571": "inception", 
    "P576": "dissolved, abolished or demolished", 
    "P577": "publication date", 
    "P580": "start time", 
    "P582": "end time", 
    "P585": "point in time", 
    "P607": "conflict", 
    "P674": "characters", 
    "P676": "lyrics by", 
    "P706": "located on terrain feature", 
    "P710": "participant", 
    "P737": "influenced by", 
    "P740": "location of formation", 
    "P749": "parent organization", 
    "P800": "notable work", 
    "P807": "separated from", 
    "P840": "narrative location", 
    "P937": "work location", 
    "P1001": "applies to jurisdiction", 
    "P1056": "product or material produced", 
    "P1198": "unemployment rate", 
    "P1336": "territory claimed by", 
    "P1344": "participant of", 
    "P1365": "replaces", 
    "P1366": "replaced by", 
    "P1376": "capital of", 
    "P1412": "languages spoken, written or signed", 
    "P1441": "present in work", 
    "P3373": "sibling"
}

for relation in possible_relations.values():
    created_relation = entity_0 + " " + relation + " " + entity_1

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    token_vecs_sum = []
    idx_tokens = []
    # print(f"tokenizer: {tokenizer}")
    # Preparing the inputs for a model. Split the sentence into tokens.
    tokens = tokenizer.tokenize(created_relation)

    # print(f"tokens: {tokens}")
    # Map the token strings to their vocabulary indeces.
    tokens_ids = tokenizer.convert_tokens_to_ids(tokens)
    # print(f"tokens_ids: {tokens_ids}")

    # Mark each of the 22 tokens as belonging to sentence "1".
    segments_ids = [1] * len(tokens)
    # print(f"segments_ids: {segments_ids}")
    tensor = torch.tensor([tokens_ids])
    # print(f"tensor: {tensor}")
    tensors = torch.tensor([segments_ids])
    # print(f"tensors: {tensors}")

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
    token_vecs_sum = []
    # Sum the vectors from the last four layers.
    for token in embeddings:
        sum_vec = torch.sum(token[-4:], dim =0)
        token_vecs_sum.append(sum_vec)

    for i, token_str in enumerate(tokens):
        # print(f"i, token_str: {i, token_str}")
        size_relation = len(relation.split(" "))
        if token_str == relation.split(" ")[0]:
            if size_relation == 1:
                idx_tokens = [i]
            else:
                tmp_list = range(i, i + size_relation, 1)
                idx_tokens = tmp_list
    # print(f"idx_tokens: {idx_tokens}")

    token_vecs_sum_relation = []
    for id in idx_tokens:
        token_vecs_sum_relation.append(token_vecs_sum[id])

    # Compute the sentence embedding, which is the average embedding of the sentence words.
    sente_embedding = torch.mean(torch.stack(token_vecs_sum_relation),dim =0)

    relation_found_r = entity_0 + " " + relation_found + " " + entity_1
    tokens_r = tokenizer.tokenize(relation_found_r)
    tokens_ids_r = tokenizer.convert_tokens_to_ids(tokens_r)
    segments_ids_r = [1] * len(tokens_r)
    tensor_r = torch.tensor([tokens_ids_r])
    tensors_r = torch.tensor([segments_ids_r])

    model_r = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)

    with torch.no_grad():
        outputs_r = model(tensor_r, tensors_r)
        hidden_states_r = outputs_r[2]

    embeddings_r = torch.stack(hidden_states_r, dim =0)
    embeddings_r = torch.squeeze(embeddings_r, dim =1)
    embeddings_r = embeddings_r.permute(1,0,2)
    token_vecs_sum_r = []
    for token_r in embeddings_r:
        sum_vec_r = torch.sum(token_r[-4:] ,dim =0)
        token_vecs_sum_r.append(sum_vec_r)

    idx_tokens_r = []
    for i_r, token_str_r in enumerate(tokens_r):
        # print(f"i_r, token_str_r: {i_r, token_str_r}")
        size_relation_r = len(relation_found.split(" "))
        if token_str_r == relation_found.split(" ")[0]:
            if size_relation_r == 1:
                idx_tokens_r=[i_r]
            else:
                tmp_list_r = range(i_r, i_r + size_relation_r, 1)
                idx_tokens=tmp_list_r
    print(f"idx_tokens_r: {idx_tokens_r}")

    token_vecs_sum_relation_r = []
    for id_r in idx_tokens_r:
        token_vecs_sum_relation_r.append(token_vecs_sum_r[id_r])

    sente_embedding_r = torch.mean(torch.stack(token_vecs_sum_r),dim =0)

    # # Calculate the cosine similarity
    token_vecs_sum_1 = sente_embedding
    token_vecs_sum_2 = sente_embedding_r
    diff_sentences = 1 - cosine(token_vecs_sum_1, token_vecs_sum_2)
    dist_euclidiana = dist(token_vecs_sum_1,token_vecs_sum_2)
    print(f'Vector similarity for {created_relation, relation_found_r} meanings:  %.2f' % diff_sentences)

    field_names = ["created_relation", "relation_found_r", "similarity_cosine", "dist_euclidiana"]
    with open('docred_database/bert_cosine_similarity.csv', 'a') as f_object:
        dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
        writer = csv.DictWriter(f_object, fieldnames=field_names)
        writer.writerow({'created_relation': created_relation, 'relation_found_r': relation_found_r, 'similarity_cosine': diff_sentences, 'dist_euclidiana': dist_euclidiana})

        f_object.close()