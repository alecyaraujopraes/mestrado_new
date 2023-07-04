import csv

import pandas as pd
from bert_utils import selection_by_bert
from functions_bert import sentence_transformer
from functions_spacy import split_text_into_sentences
from ParseSyntaticTree import (Node, combination_between_noun_phrases,
                               find_entities, find_nodes,
                               get_dict_dependencies, get_nodes_entities,
                               split_in_sentences)


df_docred = pd.read_csv("docred_database/docred.csv")

df = df_docred.reset_index() # make sure indexes pair with number of rows

for index, row in df.iterrows():
    list_sentences = split_in_sentences(row["sentences"])
    entity_tail = row["entity_tail"]
    entity_head = row["entity_head"]
    relation_id = row["code_relation"]
    relation = row["relation"]

    # print(f"Entity 0: {entity_0}, entity 1: {entity_1}, relation id: {relation_id}, relation: {relation}")

    for sentence in list_sentences:
        print(f"Sentence: {sentence}")
        list_entities = find_entities(sentence)
        dict_dependencies = get_dict_dependencies(sentence)
        list_nodes = find_nodes(sentence)
        dict_nodes = get_nodes_entities(list_entities, list_nodes)
        combination_noun_phrases = combination_between_noun_phrases(list_entities)

        nodes = {}
        for n in [Node(k) for k,v in dict_dependencies.items()]: nodes[n.name] = n
        for k,n in nodes.items():
            children = dict_dependencies[n.name]
            n.set_children([nodes[c] for c in children])

        for tuple_nodes in combination_noun_phrases:
            entity_0 = dict_nodes.get(f"{tuple_nodes[0]}")
            entity_1 = dict_nodes.get(f"{tuple_nodes[1]}")
            tuple_of_entities = (entity_0, entity_1)
            print(f"Entidades: {tuple_of_entities}")

            node_0 = nodes.get(f"{entity_0}")
            node_1 = nodes.get(f"{entity_1}")

            path_nodes = node_0.path(node_1)
            path = []
            for n in path_nodes:
                path.append(n.name)

            relation = " ".join(path)

            if relation:
                relation_found = relation
                relation_id_found_by_bert, relation_found_by_bert = selection_by_bert(entity_0, entity_1, relation_found)
            else:
                relation_found = "relation not found"

            field_names = [
                "sentence", 
                "sent_relation_found", 
                "sentence_transformer_c", 
            ]

            if relation_id == relation_id_found_by_bert:
                result = "correct"
            else:
                result = "incorrect"

            with open('docred_database/check_bert_and_annotations.csv', 'a') as f_object:
                dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
                writer = csv.DictWriter(f_object, fieldnames=field_names)
                writer.writerow({
                    "created_relation": created_relation, 
                    "sent_relation_found": sent_relation_found, 
                    "sentence_transformer_c": sentence_transformer_c,
                })

                f_object.close()

