import argparse
import csv
import itertools

import spacy
from Levenshtein import jaro_winkler

nlp = spacy.load("en_core_web_sm")

argParser = argparse.ArgumentParser()
argParser.add_argument("-s", "--sentence", help="Complete sentence")
# argParser.add_argument("-e0", "--entities0", help="Entity 0")
# argParser.add_argument("-e1", "--entities1", help="Entity 1")
# argParser.add_argument("-r", "--relation_annotated", help="Relation between entities")

# args = argParser.parse_args()
# doc = nlp(args.sentence)


def get_dict_dependencies(sentence: str)-> dict:
    doc = nlp(sentence)
    dict_dependencies = {}

    for token in doc:
        dict_dependencies[token.text] = [child.text for child in token.children]
    
    return dict_dependencies


def find_entities(text: str)-> list:
    doc = nlp(text)
    list_entities = []
    
    for entity in doc.ents:
        str1 = entity.text
        list_entities.append(str1)
    return list_entities


def find_nodes(sentence: str)-> list:
    nlp.add_pipe("merge_noun_chunks")
    doc = nlp(sentence)

    noun_phrases = [chunk.text for chunk in doc.noun_chunks]

    return noun_phrases


def get_nodes_entities(list_entities: str, list_nodes: str)-> dict:
    dict_nodes = {}
    for entity in list_entities:
        compare = 0
        for node in list_nodes:
            compare = jaro_winkler(entity, node)
            if compare_old < compare:
                compare_old = compare
                node_choose = node
        dict_nodes[f"{node}"] = entity
    
    return dict_nodes



def combination_between_noun_phrases(list_entities: list)-> list:
    combinations_list = []
    combinations = itertools.combinations(list_entities, 2)
    for combination in combinations:
        combinations_list.append(combination)

    return combinations_list


def path(sentence: str, list_path=[]):
    dict_dependencies = get_dict_dependencies(sentence)

    list_entities, dict_ent_nodes = find_entities_and_noun_phrases(sentence)

    print(list_entities)
    print(dict_ent_nodes)

    # combination_list = combination_between_noun_phrases(list_entities)

    # for combination in combination_list:
    #     entity_0 = dict_ent_nodes.get(combination[0])
    #     entity_1 = dict_ent_nodes.get(combination[1])

# path("Zest Airways , Inc. operated as AirAsia Zest ( formerly Asian Spirit and Zest Air ) , was a low - cost airline based at the Ninoy Aquino International Airport in Pasay City , Metro Manila in the Philippines .")

# tuple_of_entities = (args.entities0, args.entities1)
# # print(f"Entidades: {tuple_of_entities}")

# dict_dependencies = get_dict_dependencies(args.sentence)

# relation = find_relation_between_entities_spacy(args.sentence, tuple_of_entities)
# print(relation)
# relation_annotated = args.relation_annotated

# print(f"Frase: {args.sentence}, Entidades: {tuple_of_entities}, Relação_encontrada_por_mim: {relation}, Relação_encontrada_no_benchmark: {relation_annotated}")


# if relation:
#     field_names = ["Frase", "Entidades", "Relação_encontrada_por_mim", "Relação_encontrada_no_benchmark"]

#     with open('docred_database/manual_test_spacy.csv', 'a') as f_object:
#         dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
#         writer = csv.DictWriter(f_object, fieldnames=field_names)
#         writer.writerow({'Frase': args.sentence, 'Entidades': tuple_of_entities, 'Relação_encontrada_por_mim': relation, 'Relação_encontrada_no_benchmark': relation_annotated})

#         f_object.close()
#     print("Saved relation in csv")


# with open('test.txt', 'w') as f:
#     f.write(r)
