import csv

import pandas as pd
from functions_bert import sentence_transformer
from functions_spacy import split_text_into_sentences

# from nyt_database.ParseSyntaticTree import (Node, aggregate_NNP,
#                                             all_combinations_entities,
#                                             constituency, find_entities)
# from nyt_database.SpacyParse import find_relation_between_entities_spacy

possible_relations = {
    "direct": {
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
        "P1365": "replaces", 
        "P1366": "was replaced by", 
        "P1376": "is the capital of", 
        "P1412": "are the languages spoken, written or signed by", 
        "P1441": "is present in work of", 
        "P3373": "is sibling of",
    }, 
    "inverse": {
        "P6": "is ruled",
        "P17": "has as country of", 
        "P19": "was born in", 
        "P20": "died in",
        "P27": "is a citizen of",
        "P30": "has as continent", 
        "P31": "is an instance of",
        "P36": "has as capital", 
        "P37": "has as official language",
        "P39": "holds the position of",
        "P50": "is authored by",
        "P54": "is starter of", 
        "P58": "is scripted", 
        "P69": "is the education place from", #?? 
        "P86": "was composed by", 
        "P102": "has as member of political party", 
        "P108": "is the employee of", 
        "P112": "is the founder of", 
        "P118": "has as league",
        "P123": "was published by", 
        "P127": "is the owner of", 
        "P131": "was the location in the administrative territorial entity of", 
        "P136": "has as genre of", 
        "P137": "is operated by", 
        "P140": "has as religion", #??
        "P150": "was the location in the administrative territorial entity of", 
        "P159": "is the headquarters location of",
        "P161": "has as a cast member",
        "P162": "is produced by", 
        "P166": "received the award of",
        "P170": "was created by",
        "P171": "is the parent taxon of", #??
        "P172": "has as ethnic group", 
        "P175": "is performed by", 
        "P176": "is manufactured by", 
        "P178": "is developed by", 
        "P179": "has as series", 
        "P194": "has as legislative body of", 
        "P205": "has as basin country the", 
        "P206": "is the location in or next to body of water of", #??
        "P241": "is the military branch of", 
        "P264": "has as record label", 
        "P272": "has as production company", 
        "P276": "was located in", 
        "P279": "has as subclass",
        "P355": "is subsidized by",
        "P364": "has as original language of work", 
        "P400": "has as platform",
        "P403": "has as mouth of the watercourse",
        "P449": "has as original network", 
        "P463": "has as member", 
        "P488": "has as chairperson", 
        "P495": "is from country of origin", 
        "P527": "is part of", 
        "P551": "live-in", 
        "P569": "was born on the date", 
        "P570": "was dead on the date", 
        "P571": "starts the", #??
        "P576": "dissolved, abolished or demolished", 
        "P577": "was published on the date", 
        "P580": "was started at", 
        "P582": "was ended at", 
        "P585": "has as point in time", 
        "P607": "were envolved in the conflict", 
        "P674": "has the characters", 
        "P676": "was writen by", 
        "P706": "has as location on terrain feature on", #??
        "P710": "has as participant of", 
        "P737": "influenced", 
        "P740": "was formed in", 
        "P749": "has as parent organization", 
        "P800": "has as notable work", 
        "P840": "has as narrative location", 
        "P937": "has as work location", 
        "P1001": "was applied to jurisdiction on", #??
        "P1056": "produced the product or material", 
        "P1198": "has unemployment rate", 
        "P1336": "is claimed as territory", 
        "P1344": "has as participant", 
        "P1376": "has as capital", 
        "P1412": "speak, write or sign the languages", 
        "P1441": "has present in work",
    }
}

similar_inverses = {
    # relation code: reverse relation code
    "P6": "P35",
    "P22": "P40",
    "P26": "P26",
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

df_docred = pd.read_csv("docred_database/docred.csv")

df = df_docred.reset_index()  # make sure indexes pair with number of rows

for index, row in df.iterrows():
    list_sentences = split_text_into_sentences(row["sentences"])
    entity_0 = row["entity_tail"]
    entity_1 = row["entity_head"]
    relation_id = row["code_relation"]
    relation = row["relation"]

    print(entity_0, entity_1, relation_id, relation)
    # checar como encontrar ordem das entidades no texto
    # checar como encontrar as entidades no texto
    # agrupar as frases criadas em uma lista
    # checar se o id da relação encontrada é igual ao id anotado

    # for sent in list_sentences:
    #     if entity_0 and entity_1 in sent:
    #         sentence = sent
    #         break

    # for k,v in possible_relations.items():
    #     for relation in v.values():
    #         created_relation = entity_0 + " " + relation + " " + entity_1
    #         sent_relation_found = entity_0 + " " + relation_found + " " + entity_1

    #         # Sentence transformer
    #         sentence_transformer_c = sentence_transformer(created_relation, sent)

    #         field_names = [
    #             "created_relation", 
    #             "sent_relation_found", 
    #             "sentence_transformer_c", 
    #         ]

    #         with open('docred_database/bert_similarities_ap_voice.csv', 'a') as f_object:
    #             dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
    #             writer = csv.DictWriter(f_object, fieldnames=field_names)
    #             writer.writerow({
    #                 "created_relation": created_relation, 
    #                 "sent_relation_found": sent_relation_found, 
    #                 "sentence_transformer_c": sentence_transformer_c,
    #             })

    #             f_object.close()

