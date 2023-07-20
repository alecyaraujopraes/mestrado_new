import csv

import pandas as pd
from bert_utils import selection_by_bert
from Levenshtein import jaro_winkler
from ParseSyntaticTree import (Node, combination_between_noun_phrases,
                               find_entities, find_nodes,
                               get_dict_dependencies, get_nodes_entities,
                               split_in_sentences)
from utils import compare_strings, get_the_most_similar_pair_entities

df_docred = pd.read_csv("docred_database/docred.csv")

df = df_docred.reset_index() # make sure indexes pair with number of rows

sentences_used = []
result = 0
for index, row in df.iterrows():
    sentences = row["sentences"]

    if sentences not in sentences_used:
        # list_sentences = split_in_sentences(row["sentences"])
        # entity_tail = row["entity_tail"]
        # entity_head = row["entity_head"]
        # relation_id = row["code_relation"]
        # relation = row["relation"]

        # print(f"Entity tail: {entity_tail}, entity head: {entity_head}, relation id: {relation_id}, relation: {relation}")

        # for sentence in list_sentences:
        #     print(f"Sentence: {sentence}")
        list_entities = find_entities(sentences)
        # print(f"List entities: {list_entities}")
        dict_dependencies = get_dict_dependencies(sentences)
        # print(f"Dict dependencies: {dict_dependencies}")
        list_nodes = find_nodes(sentences)
        # print(f"List nodes: {list_nodes}")
        dict_nodes = get_nodes_entities(list_entities, list_nodes)
        # print(f"Dict nodes: {dict_nodes}")
        combination_noun_phrases = combination_between_noun_phrases(list_entities)
        # print(f"Combination noun phrases: {combination_noun_phrases}")


        nodes = {}
        for n in [Node(k) for k,v in dict_dependencies.items()]: nodes[n.name] = n
        for k,n in nodes.items():
            children = dict_dependencies[n.name]
            n.set_children([nodes[c] for c in children])


        for tuple_nodes in combination_noun_phrases:
            entity_0 = dict_nodes.get(f"{tuple_nodes[0]}")
            entity_1 = dict_nodes.get(f"{tuple_nodes[1]}")
            tuple_of_entities = (entity_0, entity_1)

            df_docred_selected = df.loc[df.sentences == sentences]

            node_0 = nodes.get(f"{entity_0}")
            node_1 = nodes.get(f"{entity_1}")

            path_nodes = node_0.path(node_1)
            path = []
            for n in path_nodes:
                path.append(n.name)

            relation_found_by_path = " ".join(path)

            if relation_found_by_path and entity_0 != entity_1:
                print(f"Relation found by path: {relation_found_by_path}")
                print(f"Entities: {tuple_of_entities}")
                relation_id_found_by_bert, relation_found_by_bert = selection_by_bert(entity_0, entity_1, relation_found_by_path)

                tuple_ents, jw_factor, relation_ant, code_relation = get_the_most_similar_pair_entities(df_docred_selected, entity_0, entity_1)
                print(f"Codes: {code_relation}, {relation_id_found_by_bert}")
                # similar_ents = False

                # for entity_tail, entity_head, relation_annotated, code_relation in zip(df_docred_selected.entity_tail, df_docred_selected.entity_head, df_docred_selected.relation, df_docred_selected.code_relation):
                #     if compare_strings(entity_tail, entity_0) and compare_strings(entity_head, entity_1):
                #         similar_ents = True

                if code_relation == relation_id_found_by_bert:
                    result = 1


                field_names = [
                    "sentences", 
                    "entity_0", 
                    "entity_1",
                    "tuple_most_similar",
                    "relation_found_by_path",
                    "relation_found_by_bert",
                    "relation_annotated",
                    "result",
                ]

                with open('docred_database/check_bert_and_annotations.csv', 'a') as f_object:
                    dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
                    writer = csv.DictWriter(f_object, fieldnames=field_names)
                    writer.writerow({
                        "sentences": sentences, 
                        "entity_0": entity_0, 
                        "entity_1": entity_1,
                        "tuple_most_similar": tuple_ents,
                        "relation_found_by_path": relation_found_by_path,
                        "relation_found_by_bert": relation_found_by_bert,
                        "relation_annotated": relation_ant,
                        "result": result,
                    })

                    f_object.close()

    sentences_used.append(sentences)