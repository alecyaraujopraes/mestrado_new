import csv

import pandas as pd
from bert_utils import selection_by_bert
from Levenshtein import jaro_winkler
from ParseSyntaticTree import (Node, combination_between_noun_phrases,
                               find_entities, find_nodes,
                               get_dict_dependencies, get_nodes_entities,
                               split_in_sentences, get_nodes_from_entities)
from utils import compare_strings, get_the_most_similar_pair_entities

df_docred = pd.read_csv("docred_database/docred.csv")

df = df_docred.reset_index() # make sure indexes pair with number of rows

sentences_used = []
# for index, row in df.iterrows():
result = 0

# sentences = row["sentences"]
sentences = "Zest Airways , Inc. operated as AirAsia Zest ( formerly Asian Spirit and Zest Air ) , was a low - cost airline based at the Ninoy Aquino International Airport in Pasay City , Metro Manila in the Philippines .It operated scheduled domestic and international tourist services , mainly feeder services linking Manila and Cebu with 24 domestic destinations in support of the trunk route operations of other airlines .In 2013 , the airline became an affiliate of Philippines AirAsia operating their brand separately .Its main base was Ninoy Aquino International Airport , Manila .The airline was founded as Asian Spirit , the first airline in the Philippines to be run as a cooperative .On August 16 , 2013 , the Civil Aviation Authority of the Philippines ( CAAP ) , the regulating body of the Government of the Republic of the Philippines for civil aviation , suspended Zest Air flights until further notice because of safety issues .Less than a year after AirAsia and Zest Air 's strategic alliance , the airline has been rebranded as AirAsia Zest .The airline was merged into AirAsia Philippines in January 2016 ."

if sentences not in sentences_used:
    list_entities = find_entities(sentences)
    print(f"List entitites: {list_entities}")
    dict_dependencies = get_dict_dependencies(sentences)
    list_nodes = find_nodes(sentences)
    print(f"List nodes: {list_nodes}")
    nodes_from_entities = get_nodes_from_entities(list_entities, list_nodes)
    print(f"Nodes from entities: {nodes_from_entities}")
#     combination_nodes = combination_between_noun_phrases(nodes_from_entities)
#     print(f"Combination noun phrases: {combination_nodes}")

#     nodes = {}
#     for n in [Node(k) for k,v in dict_dependencies.items()]: nodes[n.name] = n
#     for k,n in nodes.items():
#         children = dict_dependencies[n.name]
#         n.set_children([nodes[c] for c in children])


#     for pair_nodes in combination_nodes:
#         entity_0 = pair_nodes[0]
#         entity_1 = pair_nodes[1]
#         print(f"Nodes: {entity_0, entity_1}")
#         tuple_of_entities = (entity_0, entity_1)
#         print(f"Tuple of entities: {tuple_of_entities}")

#         df_docred_selected = df.loc[df.sentences == sentences]

#         node_0 = nodes.get(f"{entity_0}")
#         node_1 = nodes.get(f"{entity_1}")

#         path_nodes = node_0.path(node_1)
#         path = []

#         if not path:
#             path_nodes = node_1.path(node_0)
#         path = []
#         for n in path_nodes:
#             path.append(n.name)

#         relation_found_by_path = " ".join(path)
#         print(f"Relation found by path: {relation_found_by_path}")

#         if relation_found_by_path and entity_0 != entity_1:
#             print(f"Relation found by path: {relation_found_by_path}")
#             print(f"Entities: {tuple_of_entities}")
#             relation_id_found_by_bert, relation_found_by_bert = selection_by_bert(entity_0, entity_1, relation_found_by_path)

#             tuple_ents, jw_factor, annotated_relation, annotated_code_relation = get_the_most_similar_pair_entities(df_docred_selected, entity_0, entity_1)

#             if annotated_code_relation == relation_id_found_by_bert:
#                 print(f"Codes: {annotated_code_relation}, {relation_id_found_by_bert}")
#                 result = 1

#             else:
#                 result = 0


#             field_names = [
#                 "sentences", 
#                 "entity_0", 
#                 "entity_1",
#                 "tuple_most_similar",
#                 "relation_found_by_path",
#                 "relation_found_by_bert",
#                 "relation_annotated",
#                 "result",
#             ]

#             with open('docred_database/check_bert_and_annotations.csv', 'a') as f_object:
#                 dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names, delimiter=';')
#                 writer = csv.DictWriter(f_object, fieldnames=field_names, delimiter=';')
#                 writer.writerow({
#                     "sentences": sentences, 
#                     "entity_0": entity_0, 
#                     "entity_1": entity_1,
#                     "tuple_most_similar": tuple_ents,
#                     "relation_found_by_path": relation_found_by_path,
#                     "relation_found_by_bert": relation_found_by_bert,
#                     "relation_annotated": annotated_relation,
#                     "result": result,
#                 })

#                 f_object.close()

# sentences_used.append(sentences)