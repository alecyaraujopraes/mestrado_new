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

args = argParser.parse_args()


def get_dict_dependencies(sentence: str)-> dict:
    nlp.add_pipe("merge_noun_chunks")
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
        dict_nodes[f"{node_choose}"] = entity

    return dict_nodes


def combination_between_noun_phrases(list_entities: list)-> list:
    combinations_list = []
    combinations = itertools.combinations(list_entities, 2)
    for combination in combinations:
        combinations_list.append(combination)

    return combinations_list


def find_father(entity: str, dependencies: dict)-> list:
    father = []

    for k,v in dependencies:
        if entity in v:
            father.append(k)

    return father

class Node:

    def __init__(self, noun_phrases, children, father):
        if len(noun_phrases) == 1:
            self.name = noun_phrases
            self.father = father
            self.children = children
        else: 
            for node in noun_phrases:
                Node([node], self, father=find_father(node, dict_dependencies), children=dict_dependencies.get(node))


    def search(self, name=None):
        ???
        return [n for n in [self] + [c2 for c in self.children for c2 in c.search(pos=pos, label=label)]
                if (n.pos == pos or not pos) and (n.label == label or not label)]


    def path(self, to, path=[]):
        path = path + [self]
        neighbours = self.children + [self.father] if self.father else []
        neighbours = list(set(neighbours) - set(path))
        if to == self:
            return path
        else:
            if not neighbours:
                path = list(set(path) - set([self]))
                return path
            else:
                for n in neighbours:
                    path2 = n.path(to, path=path)
                    if len(path2) > len(path): return path2
                path = list(set(path) - set([self]))
                return path

sentence = args.sentence

list_entities = find_entities(sentence)
dict_dependencies = get_dict_dependencies()
list_nodes = find_nodes(sentence)
dict_nodes = get_nodes_entities(list_entities, list_nodes)
combination_noun_phrases = combination_between_noun_phrases(list_entities)

for tuple_nodes in combination_noun_phrases:
    entity_0 = dict_nodes.get(f"{tuple_nodes[0]}")
    entity_1 = dict_nodes.get(f"{tuple_nodes[1]}")
    tuple_of_entities = (entity_0, entity_1)
    print(f"Entidades: {tuple_of_entities}")

    root = Node(list_nodes)

    node_0 = root.search()
    node_1 = root.search()

    path = node_0.path(node_1)






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
