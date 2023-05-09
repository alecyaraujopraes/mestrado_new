import csv

from functions_bert import (cosine_similarity, create_embeddings,
                            create_mean_torch, euclidian_distance,
                            get_idx_tokens_for_created_relations,
                            get_idx_tokens_for_found_relations, get_vectors)

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
    "P279": "subclass of", #'sub', '##class', 'of',
    "P355": "subsidiary", 
    "P361": "part of", 
    "P364": "original language of work", 
    "P400": "platform", 
    "P403": "mouth of the watercourse", #'mouth', 'of', 'the', 'water', '##co', '##urse'
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

list_relations = [
    {
        "paragraph": "Niklas Bergqvist ( born 6 October 1962 in Stockholm ) , is a Swedish songwriter , producer and musician .His career started in 1984 , as a founding member of the Synthpop band Shanghai , which he started along his school friends .The band released two albums and numerous singles , with their debut single ' Ballerina ' , produced by former Europe guitarist Kee Marcello .Following the success of the single , the album also gained positive attention , resulting in the band touring around Sweden .The second , and final , studio album was produced by Swedish pop star Harpo .After the band split - up in 1987 , Bergqvist formed and played in several other bands until he decided to focus more on songwriting , resulting in several releases ever since .In 2015 , he founded the independent record label Tracks of Sweden with songwriting partner Simon Johansson .",
        "entity_0": "Niklas Bergqvist",
        "entity_1": "Stockholm",
        "relation_annotated": "place of birth",
        "relation_found": "born in",
    },
    {
        "paragraph": "Juan Guzmán ( born Hans Gutmann Guster , also known as "" Juanito "" , 28 October 1911 – 1982 ) was a German born Mexican photojournalist .He was known as a war photographer of the Spanish Civil War and later on his work with Mexican painters Frida Kahlo and Diego Rivera .Hans Gutmann was born in Cologne .In 1936 he joined the Spanish Civil War as a volunteer of the International Brigades .Gutmann later became a Spanish citizen and changed his name to Juan Guzmán .There are more than 1,300 photographs from the Spanish Civil War in the archive of Agencia EFE ( Madrid ) .His most famous image is the picture of 17-year - old Marina Ginestà standing in top of Hotel Colón in Barcelona .It is one of the most iconic photographs of the Spanish Civil War .After the war Guzmán fled to Mexico , where he arrived in 1940 .He worked for major Mexican magazines and newspapers and became a friend of Frida Kahlo with whom Guzmán shared similar political views .In the 1950s he took a large number of photographs of Kahlo and her husband Diego Rivera .Guzmán also photographed the artwork of Mexican painters like Gerardo Murillo , Jesús Reyes Ferreira and José Clemente Orozco .Juan Guzmán died in Mexico City in 1982 .",
        "entity_0": "Frida Kahlo",
        "entity_1": "Diego Rivera",
        "relation_annotated": "spouse",
        "relation_found": "her husband",
    },
    {
        "paragraph": "Mário Cravo Neto ( Salvador , April 20 , 1947 — Salvador , August 9 , 2009 ) was a Brazilian photographer , sculptor and draughtsman .Mário Cravo , son of the sculptor Mário Cravo Júnior , is considered one of the most important photographers of Brazil .Since his early life , he was in contact with circle of artists and , when an adolescent , he met with Pierre Verger , friend of his father .In 1968 , he studied for two years at the Art Students League of New York .After that , he returned to Brazil and first exhibits the sculptures created in New York at the 12th São Paulo Art Biennial .He worked mainly with black - and - white photography , and representing the religion of Candomble .In 2005 , he exhibited at Rencontres d'Arles festival .He died in 2009 in Salvador due to skin cancer .Neto is the father of Brazilian photographer Christian Cravo .","Mário Cravo Neto ( Salvador , April 20 , 1947 — Salvador , August 9 , 2009 ) was a Brazilian photographer , sculptor and draughtsman .",
        "entity_0": "Mário Cravo Neto",
        "entity_1": "Mário Cravo Júnior",
        "relation_annotated": "father",
        "relation_found": "",
    },
]

for item in list_relations:
    entity_0 = item.get("entity_0")
    entity_1 = item.get("entity_1")
    paragraph = item.get("paragraph")
    relation_found = item.get("relation_found")

    for relation in possible_relations.values():
        created_relation = entity_0 + " " + relation + " " + entity_1
        # created_relation = "Niklas Bergqvist was born in Stockholm"
        # created_relation = "Niklas born in Stockholm"

        tokens, tokens_ids, segments_ids, tensor, tensors, embeddings, token_vecs_sum = create_embeddings(created_relation)
        idx_tokens = get_idx_tokens_for_created_relations(tokens, relation)
        print(f"idx_tokens: {idx_tokens}")
        token_vecs_sum_relation = get_vectors(idx_tokens, token_vecs_sum)
        sente_embedding = create_mean_torch(token_vecs_sum_relation)

        tokens_wc, tokens_ids_wc, segments_ids_wc, tensor_wc, tensors_wc, embeddings_wc, token_vecs_sum_wc = create_embeddings(relation)
        idx_tokens_wc = range(0, len(tokens_wc)-1, 1)
        sente_embedding_wc = create_mean_torch(token_vecs_sum_wc)
        

        relation_found_r = entity_0 + " " + relation_found + " " + entity_1
        tokens_r, tokens_ids_r, segments_ids_r, tensor_r, tensors_r, embeddings_r, token_vecs_sum_r = create_embeddings(relation_found_r)
        idx_tokens_r = get_idx_tokens_for_found_relations(tokens_r, relation_found_r)
        token_vecs_sum_relation_r = get_vectors(idx_tokens_r, token_vecs_sum_r)
        sente_embedding_r = create_mean_torch(token_vecs_sum_relation_r)

        tokens_r_wc, tokens_ids_r_wc, segments_ids_r_wc, tensor_r_wc, tensors_r_wc, embeddings_r_wc, token_vecs_sum_r_wc = create_embeddings(relation_found)
        idx_tokens_r_wc = range(0, len(tokens_r_wc)-1, 1)
        sente_embedding_r_wc = create_mean_torch(token_vecs_sum_r_wc)

        diff_sentences = cosine_similarity(sente_embedding, sente_embedding_r)
        diff_relations = cosine_similarity(sente_embedding_wc, sente_embedding_r_wc)
        dist_euclidiana = euclidian_distance(sente_embedding, sente_embedding_r)

        field_names = ["created_relation", "relation_found_r", "similarity_cosine_with_context", "similarity_cosine_without_context", "dist_euclidiana"]
        with open('docred_database/bert_cosine_similarity.csv', 'a') as f_object:
            dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
            writer = csv.DictWriter(f_object, fieldnames=field_names)
            writer.writerow({'created_relation': created_relation, 'relation_found_r': relation_found_r, 'similarity_cosine_with_context': diff_sentences, 'similarity_cosine_without_context': diff_relations, 'dist_euclidiana': dist_euclidiana})

            f_object.close()
