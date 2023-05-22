import csv

from functions_bert import (cosine_similarity, create_embeddings,
                            create_mean_torch, euclidian_distance,
                            get_idx_tokens_for_created_relations,
                            get_idx_tokens_for_found_relations, 
                            get_vectors, # sentence_similarity, 
                            sentence_transformer, simcse)

possible_relations = {
    "P6": "is the head of government of", 
    "P17": "is the country of", 
    "P19": "is the place of birth of", 
    "P20": "was the place of death of", 
    "P22": "is father of", 
    "P25": "is mother of", 
    "P26": "is spouse of", 
    "P27": "is the country of citizenship of", 
    "P30": "is the continent of", 
    "P31": "is an instance of", 
    "P35": "is the head of state of", 
    "P36": "is the capital of", 
    "P37": "is the official language of", 
    "P39": "a position held by", 
    "P40": "is the child of", 
    "P50": "is the author of", 
    "P54": "is the member of sports team", 
    "P57": "is the director of", 
    "P58": "is the screenwriter of", 
    "P69": "was educated at", 
    "P86": "is the composer of", 
    "P102": "is the member of political party", 
    "P108": "is the employer of", 
    "P112": "was founded by", 
    "P118": "is in league", 
    "P123": "is the publisher of", 
    "P127": "is owned by", 
    "P131": "is located in the administrative territorial entity in", 
    "P136": "is the genre of", 
    "P137": "is the operator of", 
    "P140": "have the religion of", 
    "P150": "contains administrative territorial entity of", 
    "P155": "follows", 
    "P156": "is followed by", 
    "P159": "headquarters location is in", 
    "P161": "is a cast member of", 
    "P162": "is the producer of", 
    "P166": "is the award received by", 
    "P170": "is the creator of", 
    "P171": "is the parent taxon of", 
    "P172": "is the ethnic group of", 
    "P175": "is the performer of", 
    "P176": "is the manufacturer of", 
    "P178": "is the developer of", 
    "P179": "is a series about", 
    "P190": "is the sister city of", 
    "P194": "is the legislative body of", 
    "P205": "is the basin country of", 
    "P206": "was located in or next to body of water", 
    "P241": "is in the military branch of", 
    "P264": "is the record label of", 
    "P272": "is a production company of", 
    "P276": "is a location at", 
    "P279": "is subclass of",
    "P355": "is subsidiary of", 
    "P361": "is part of", 
    "P364": "is the original language of work in", 
    "P400": "is a platform to", 
    "P403": "is a mouth of the watercourse at",
    "P449": "is the original network in", 
    "P463": "is member of", 
    "P488": "is chairperson at", 
    "P495": "is the country of origin of", 
    "P527": "has part in", 
    "P551": "is the residence of", 
    "P569": "is date of birth of", 
    "P570": "is date of death of", 
    "P571": "is the inception of", 
    "P576": "was dissolved, abolished or demolished by", 
    "P577": "is the publication date of", 
    "P580": "is the start time of", 
    "P582": "is the end time of", 
    "P585": "is the point in time when", 
    "P607": "is a conflict caused by", 
    "P674": "are characters of", 
    "P676": "lyrics by", 
    "P706": "is located on terrain feature where", 
    "P710": "is a participant of", 
    "P737": "was influenced by", 
    "P740": "is the location of formation of", 
    "P749": "is a parent organization of", 
    "P800": "is a notable work of", 
    "P807": "was separated from", 
    "P840": "is the narrative location of", 
    "P937": "is the work location of", 
    "P1001": "applies to jurisdiction on", 
    "P1056": "is the product or material produced by", 
    "P1198": "unemployment rate is", 
    "P1336": "is a territory claimed by", 
    "P1344": "is the participant of", 
    "P1365": "replaces", 
    "P1366": "was replaced by", 
    "P1376": "is the capital of", 
    "P1412": "are the languages spoken, written or signed in", 
    "P1441": "is present in work of", 
    "P3373": "is sibling of"
}

list_relations = [
    {
        "paragraph": "Niklas Bergqvist ( born 6 October 1962 in Stockholm ) , is a Swedish songwriter , producer and musician .His career started in 1984 , as a founding member of the Synthpop band Shanghai , which he started along his school friends .The band released two albums and numerous singles , with their debut single ' Ballerina ' , produced by former Europe guitarist Kee Marcello .Following the success of the single , the album also gained positive attention , resulting in the band touring around Sweden .The second , and final , studio album was produced by Swedish pop star Harpo .After the band split - up in 1987 , Bergqvist formed and played in several other bands until he decided to focus more on songwriting , resulting in several releases ever since .In 2015 , he founded the independent record label Tracks of Sweden with songwriting partner Simon Johansson .",
        "sents":["Niklas Bergqvist ( born 6 October 1962 in Stockholm ) , is a Swedish songwriter , producer and musician .", "His career started in 1984 , as a founding member of the Synthpop band Shanghai , which he started along his school friends .", "The band released two albums and numerous singles , with their debut single \" Ballerina \" , produced by former Europe guitarist Kee Marcello .", "Following the success of the single , the album also gained positive attention , resulting in the band touring around Sweden .", "The second , and final , studio album was produced by Swedish pop star Harpo .", "After the band split - up in 1987 , Bergqvist formed and played in several other bands until he decided to focus more on songwriting , resulting in several releases ever since .", "In 2015 , he founded the independent record label Tracks of Sweden with songwriting partner Simon Johansson ."],
        "entity_0": "Niklas Bergqvist",
        "entity_1": "Stockholm",
        "relation_annotated": "has the place of birth in",
        "relation_found": "born in",
    },
    {
        "paragraph": "Juan Guzmán ( born Hans Gutmann Guster , also known as "" Juanito "" , 28 October 1911 – 1982 ) was a German born Mexican photojournalist .He was known as a war photographer of the Spanish Civil War and later on his work with Mexican painters Frida Kahlo and Diego Rivera .Hans Gutmann was born in Cologne .In 1936 he joined the Spanish Civil War as a volunteer of the International Brigades .Gutmann later became a Spanish citizen and changed his name to Juan Guzmán .There are more than 1,300 photographs from the Spanish Civil War in the archive of Agencia EFE ( Madrid ) .His most famous image is the picture of 17-year - old Marina Ginestà standing in top of Hotel Colón in Barcelona .It is one of the most iconic photographs of the Spanish Civil War .After the war Guzmán fled to Mexico , where he arrived in 1940 .He worked for major Mexican magazines and newspapers and became a friend of Frida Kahlo with whom Guzmán shared similar political views .In the 1950s he took a large number of photographs of Kahlo and her husband Diego Rivera .Guzmán also photographed the artwork of Mexican painters like Gerardo Murillo , Jesús Reyes Ferreira and José Clemente Orozco .Juan Guzmán died in Mexico City in 1982 .",
        "sents": ["Juan Guzmán ( born Hans Gutmann Guster , also known as \" Juanito \" , 28 October 1911 - 1982 ) was a German born Mexican photojournalist .", "He was known as a war photographer of the Spanish Civil War and later on his work with Mexican painters Frida Kahlo and Diego Rivera .", "Hans Gutmann was born in Cologne .", "In 1936 he joined the Spanish Civil War as a volunteer of the International Brigades .", "Gutmann later became a Spanish citizen and changed his name to Juan Guzmán .", "There are more than 1,300 photographs from the Spanish Civil War in the archive of Agencia EFE ( Madrid ) .", "His most famous image is the picture of 17-year - old Marina Ginestà standing in top of Hotel Colón in Barcelona .", "It is one of the most iconic photographs of the Spanish Civil War .", "After the war Guzmán fled to Mexico ,where he arrived in 1940 .", "He worked for major Mexican magazines and newspapers and became a friend of Frida Kahlo with whom Guzmán shared similar political views .", "In the 1950s he took a large number of photographs of Kahlo and her husband Diego Rivera .", "Guzmán also photographed the artwork of Mexican painters like Gerardo Murillo , Jesús Reyes Ferreira and José Clemente Orozco .", "Juan Guzmán died in Mexico City in 1982 ."],
        "entity_0": "Frida Kahlo",
        "entity_1": "Diego Rivera",
        "relation_annotated": "spouse",
        "relation_found": "her husband",
    },
    {
        "paragraph": "Mário Cravo Neto ( Salvador , April 20 , 1947 — Salvador , August 9 , 2009 ) was a Brazilian photographer , sculptor and draughtsman .Mário Cravo , son of the sculptor Mário Cravo Júnior , is considered one of the most important photographers of Brazil .Since his early life , he was in contact with circle of artists and , when an adolescent , he met with Pierre Verger , friend of his father .In 1968 , he studied for two years at the Art Students League of New York .After that , he returned to Brazil and first exhibits the sculptures created in New York at the 12th São Paulo Art Biennial .He worked mainly with black - and - white photography , and representing the religion of Candomble .In 2005 , he exhibited at Rencontres d'Arles festival .He died in 2009 in Salvador due to skin cancer .Neto is the father of Brazilian photographer Christian Cravo . Mário Cravo Neto ( Salvador , April 20 , 1947 — Salvador , August 9 , 2009 ) was a Brazilian photographer , sculptor and draughtsman .",
        "sents": ["Mário Cravo Neto ( Salvador , April 20 , 1947 — Salvador , August 9 , 2009 ) was a Brazilian photographer , sculptor and draughtsman .", "Mário Cravo , son of the sculptor Mário Cravo Júnior , is considered one of the most important photographers of Brazil .", "Since his early life , he was in contact with circle of artists and , when an adolescent , he met with Pierre Verger , friend of his father .", "In 1968 , he studied for two years at the Art Students League of New York .", "After that , he returned to Brazil and first exhibits the sculptures created in New York at the 12th São Paulo Art Biennial .", "He worked mainly with black - and - white photography , and representing the religion of Candomble .", "In 2005 , he exhibited at Rencontres d'Arles festival .", "He died in 2009 in Salvador due to skin cancer .", "Neto is the father of Brazilian photographer Christian Cravo ."],
        "entity_0": "Mário Cravo",
        "entity_1": "Mário Cravo Júnior",
        "relation_annotated": "father",
        "relation_found": "son",
    },
]

for item in list_relations:
    entity_0 = item.get("entity_0")
    entity_1 = item.get("entity_1")
    paragraph = item.get("paragraph")
    relation_found = item.get("relation_found")

    for sent in item.get("sents"):
        if entity_0 and entity_1 in sent:
            sentence = sent
            break

    for relation in possible_relations.values():
        created_relation = entity_0 + " " + relation + " " + entity_1
        sent_relation_found = entity_0 + " " + relation_found + " " + entity_1 

        # Creating vector to created relation
        tokens_cr, tokens_ids_cr, segments_ids_cr, tensor_cr, tensors_cr, embeddings_cr, token_vecs_sum_cr = create_embeddings(created_relation)
        created_relation_embedding = create_mean_torch(token_vecs_sum_cr)

        # Creating vector to sentence and getting vector from sentence relation found
        tokens_sent, tokens_ids_sent, segments_ids_sent, tensor_sent, tensors_sent, embeddings_sent, token_vecs_sum_sent = create_embeddings(sent)
        idx_tokens_vecs_sum = get_idx_tokens_for_created_relations(tokens_sent, sent_relation_found)
        vecs_sum = get_vectors(idx_tokens_vecs_sum, token_vecs_sum_sent)
        sent_embedding = create_mean_torch(vecs_sum)

        # Creating vector to possible relation without context
        tokens_r, tokens_ids_r, segments_ids_r, tensor_r, tensors_r, embeddings_r, token_vecs_sum_r = create_embeddings(relation)
        sente_embedding_r = create_mean_torch(token_vecs_sum_r)

        # Creating vector to relation found without context
        tokens_fr, tokens_ids_fr, segments_ids_fr, tensor_fr, tensors_fr, embeddings_fr, token_vecs_sum_fr = create_embeddings(relation_found)
        sente_embedding_fr = create_mean_torch(token_vecs_sum_fr)

        # Sentence similarity
        # sentence_similarity_c = sentence_similarity(created_relation, sent)
        # sentence_similarity_wc = sentence_similarity(relation, relation_found)

        # Sentence transformer
        sentence_transformer_c = sentence_transformer(created_relation, sent)
        sentence_transformer_wc = sentence_transformer(relation, relation_found)

        # SimCSE
        simcse_c = simcse(created_relation, sent)
        simcse_wc = simcse(relation, relation_found)


        diff_sentences = cosine_similarity(created_relation_embedding, sent_embedding)
        diff_relations = cosine_similarity(sente_embedding_r, sente_embedding_fr)
        dist_euclidiana_sents = euclidian_distance(created_relation_embedding, sent_embedding)
        dist_euclidiana_relations = euclidian_distance(sente_embedding_r, sente_embedding_fr)

        field_names = [
            "created_relation", 
            "relation_found", 
            "similarity_cosine_sents", 
            "similarity_cosine_without_context", 
            "dist_euclidiana_sents", 
            "dist_euclidiana_relations", 
            # "sentence_similarity_context", 
            # "sentence_similarity_wc", 
            "sentence_transformer_c", 
            "sentence_transformer_wc", 
            "simcse_c", 
            "simcse_wc"
        ]

        with open('docred_database/bert_similarities.csv', 'a') as f_object:
            dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
            writer = csv.DictWriter(f_object, fieldnames=field_names)
            writer.writerow({
                "created_relation": created_relation, 
                "relation_found": relation_found, 
                "similarity_cosine_sents": diff_sentences, 
                "similarity_cosine_without_context": diff_relations, 
                "dist_euclidiana_sents": dist_euclidiana_sents, 
                "dist_euclidiana_relations": dist_euclidiana_relations, 
                # "sentence_similarity_context": sentence_similarity_c, 
                # "sentence_similarity_wc": sentence_similarity_wc, 
                "sentence_transformer_c": sentence_transformer_c,
                "sentence_transformer_wc": sentence_transformer_wc, 
                "simcse_c": simcse_c, 
                "simcse_wc": simcse_wc
            })

            f_object.close()
