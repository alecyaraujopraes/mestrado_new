import csv

from functions_bert import (
    cosine_similarity, create_embeddings,
    create_mean_torch, euclidian_distance,
    get_idx_tokens_for_created_relations,
    get_idx_tokens_for_found_relations, 
    get_vectors, sentence_transformer,
)

possible_relations_direct = {
    "P6": "is the head of government of", 
    "P17": "is the country of", 
    "P19": "is the place of birth of", 
    "P20": "is the place of death of", 
    "P22": "is the father of", 
    "P25": "is the mother of", 
    "P26": "is the spouse of", 
    "P27": "is the country of citizenship of", 
    "P30": "is the continent of", 
    "P31": "has an instance of", 
    "P35": "is the head of state of", 
    "P36": "is the capital of", 
    "P37": "is the official language of", 
    "P39": "is a position held by", 
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
    "P118": "is the league of", 
    "P123": "is the publisher of", 
    "P127": "is owned by", 
    "P131": "is located in the administrative territorial entity of", 
    "P136": "is the genre of", 
    "P137": "is the operator of", 
    "P140": "is the religion of", 
    "P150": "contains administrative territorial entity of", 
    "P155": "follows", 
    "P156": "is followed by", 
    "P159": "has headquarters location in", # ??
    "P161": "is a cast member of", 
    "P162": "is the producer of", 
    "P166": "is the award received by", 
    "P170": "is the creator of", 
    "P171": "is the parent taxon of", 
    "P172": "is the ethnic group from", 
    "P175": "is the performer of", 
    "P176": "is the manufacturer of", 
    "P178": "is the developer of", 
    "P179": "is a series from", 
    "P190": "is the sister city of", 
    "P194": "is the legislative body of", 
    "P205": "is the basin country of", 
    "P206": "is located in or next to body of water of", 
    "P241": "is in the military branch of", 
    "P264": "is the record label of", 
    "P272": "is a production company of", 
    "P276": "is the location of", 
    "P279": "is a subclass of",
    "P355": "is the subsidiary of", 
    "P361": "is part of", 
    "P364": "is the original language of work of", 
    "P400": "is the platform of", 
    "P403": "is the mouth of the watercourse of",
    "P449": "is the original network of", 
    "P463": "has as member of", 
    "P463": "is member of", 
    "P488": "is chairperson of", 
    "P495": "is the country of origin of", 
    "P527": "has part of", 
    "P551": "is the residence of", 
    "P569": "is date of birth of", 
    "P570": "is date of death of", 
    "P571": "is the inception of", 
    "P576": "was dissolved, abolished or demolished the", 
    "P577": "is the publication date of", 
    "P580": "is the start time of", 
    "P582": "is the end time of", 
    "P585": "is the point in time of", 
    "P607": "is a conflict that envolved", 
    "P674": "is characters of", 
    "P676": "is a lyrics by", 
    "P706": "is located on terrain feature on", 
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
    "P1198": "is the unemployment rate of", 
    "P1336": "is a territory claimed by", 
    "P1344": "is the participant of", 
    "P1344": "is the participant of", 
    "P1365": "replaces", 
    "P1366": "was replaced by", 
    "P1376": "is the capital of", 
    "P1412": "are the languages spoken, written or signed by", 
    "P1441": "is present in work of", 
    "P3373": "is sibling of",
    "P6⁻¹": "has as head of government",
    "P17⁻¹": "has as country of", 
    "P19⁻¹": "has as place of birth", 
    "P20⁻¹": "has as place of death of",
    "P26⁻¹": "is the spouse of",
    "P27⁻¹": "has as country of citizenship",
    "P30⁻¹": "has as continent", 
    "P31⁻¹": "is an instance of",
    "P35⁻¹": "has as head of state", 
    "P36⁻¹": "has as capital", 
    "P37⁻¹": "has as official language",
    "P39⁻¹": "has as position held by",
    "P40⁻¹": "has as child of", 
    "P50⁻¹": "has as author",
    "P54⁻¹": "has as member of sports team", 
    "P58⁻¹": "has as screenwriter", 
    "P69⁻¹": "is the education place from", #?? 
    "P86⁻¹": "has as composer", 
    "P102⁻¹": "has as member of political party", 
    "P108⁻¹": "had as employee", 
    "P112⁻¹": "is the founder of", 
    "P118⁻¹": "has as league",
    "P123⁻¹": "has as publisher", 
    "P127⁻¹": "is the owner of", 
    "P131⁻¹": "was the location in the administrative territorial entity of", 
    "P136⁻¹": "has as genre of", 
    "P137⁻¹": "is operated by", 
    "P140⁻¹": "has as religion", 
    "P150⁻¹": "was the location in the administrative territorial entity of", 
    "P159⁻¹": "is the headquarters location of", # ??
    "P161⁻¹": "has as a cast member",
    "P162⁻¹": "is produced by", 
    "P166⁻¹": "has received the award",
    "P170⁻¹": "was created by",
    "P171⁻¹": "is the parent taxon of", 
    "P172⁻¹": "has as ethnic group", 
    "P175⁻¹": "is performed by", 
    "P176⁻¹": "is manufactured by", 
    "P178⁻¹": "is developed by", 
    "P179⁻¹": "is a series from", 
    "P194⁻¹": "has as legislative body of", 
    "P205⁻¹": "has as basin country the", 
    "P206⁻¹": "has as location in or next to body of water of", 
    "P241⁻¹": "has as military branch of", 
    "P264⁻¹": "has as record label", 
    "P272⁻¹": "has as production company", 
    "P276⁻¹": "was located in", 
    "P279⁻¹": "has as subclass of",
    "P355⁻¹": "has as subsidiary",
    "P364⁻¹": "has as original language of work", 
    "P400⁻¹": "has as platform",
    "P403⁻¹": "has as mouth of the watercourse",
    "P449⁻¹": "has as original network", 
    "P463⁻¹": "has as member", 
    "P463⁻¹": "is member of", 
    "P488⁻¹": "has as chairperson", 
    "P495⁻¹": "has as country of origin", 
    "P551⁻¹": "has as residence", 
    "P569⁻¹": "has as date of birth", 
    "P570⁻¹": "has as date of death", 
    "P571⁻¹": "has as inception", 
    "P576⁻¹": "dissolved, abolished or demolished", 
    "P577⁻¹": "has as publication date", 
    "P580⁻¹": "has as start time", 
    "P582⁻¹": "has as end time", 
    "P585⁻¹": "has as point in time", 
    "P607⁻¹": "were envolved in the conflict", 
    "P674⁻¹": "has as characters", 
    "P676⁻¹": "has as lyrics", 
    "P706⁻¹": "has as location on terrain feature on", #??
    "P710⁻¹": "has as participant of", 
    "P737⁻¹": "has as influencer", 
    "P740⁻¹": "has as location of formation", 
    "P749⁻¹": "has as parent organization", 
    "P800⁻¹": "has as notable work", 
    "P840⁻¹": "has as narrative location", 
    "P937⁻¹": "has as work location", 
    "P1001⁻¹": "applies to jurisdiction on", #??
    "P1056⁻¹": "produced the product or material", 
    "P1198⁻¹": "has as unemployment rate", 
    "P1336⁻¹": "claimed as territory", 
    "P1344⁻¹": "has as participant", 
    "P1376⁻¹": "has as capital", 
    "P1412⁻¹": "has as languages spoken, written or signed", 
    "P1441⁻¹": "has present in work", 
}

similar_inverses = {
    # relation code: reverse relation code
    "P22": "P40", 
    "P25": "P40",
    "P155": "P156",
    "P156": "P155",
    "P171": "P171",
    "P190": "P190",
    "P361": "P527",
    "P1365": "P1366",
    "P1366": "P1365",
    "P807": "P807",
    "P3373": "P3373"
}

list_relations = [
    {
        "paragraph": "Niklas Bergqvist ( born 6 October 1962 in Stockholm ) , is a Swedish songwriter , producer and musician .His career started in 1984 , as a founding member of the Synthpop band Shanghai , which he started along his school friends .The band released two albums and numerous singles , with their debut single ' Ballerina ' , produced by former Europe guitarist Kee Marcello .Following the success of the single , the album also gained positive attention , resulting in the band touring around Sweden .The second , and final , studio album was produced by Swedish pop star Harpo .After the band split - up in 1987 , Bergqvist formed and played in several other bands until he decided to focus more on songwriting , resulting in several releases ever since .In 2015 , he founded the independent record label Tracks of Sweden with songwriting partner Simon Johansson .",
        "sents":["Niklas Bergqvist ( born 6 October 1962 in Stockholm ) , is a Swedish songwriter , producer and musician .", "His career started in 1984 , as a founding member of the Synthpop band Shanghai , which he started along his school friends .", "The band released two albums and numerous singles , with their debut single \" Ballerina \" , produced by former Europe guitarist Kee Marcello .", "Following the success of the single , the album also gained positive attention , resulting in the band touring around Sweden .", "The second , and final , studio album was produced by Swedish pop star Harpo .", "After the band split - up in 1987 , Bergqvist formed and played in several other bands until he decided to focus more on songwriting , resulting in several releases ever since .", "In 2015 , he founded the independent record label Tracks of Sweden with songwriting partner Simon Johansson ."],
        "entity_0": "Niklas Bergqvist",
        "entity_1": "Stockholm",
        "relation_annotated": "has as place of birth in",
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

    for relation in possible_relations_direct.values():
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

        # Sentence transformer
        sentence_transformer_c = sentence_transformer(created_relation, sent)
        sentence_transformer_wc = sentence_transformer(relation, relation_found)

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
            "sentence_transformer_c", 
            "sentence_transformer_wc", 
        ]

        with open('docred_database/bert_similarities_ap_voice.csv', 'a') as f_object:
            dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
            writer = csv.DictWriter(f_object, fieldnames=field_names)
            writer.writerow({
                "created_relation": created_relation, 
                "relation_found": relation_found, 
                "similarity_cosine_sents": diff_sentences, 
                "similarity_cosine_without_context": diff_relations, 
                "dist_euclidiana_sents": dist_euclidiana_sents, 
                "dist_euclidiana_relations": dist_euclidiana_relations, 
                "sentence_transformer_c": sentence_transformer_c,
                "sentence_transformer_wc": sentence_transformer_wc, 
            })

            f_object.close()
