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
    doc = nlp(sentence)

    noun_phrases = [chunk.text for chunk in doc.noun_chunks]

    return noun_phrases


def get_nodes_entities(list_entities: str, list_nodes: str)-> dict:
    dict_nodes = {}
    for entity in list_entities:
        compare_old = 0
        for node in list_nodes:
            compare = jaro_winkler(entity, node)
            if compare_old < compare:
                compare_old = compare
                node_choose = node
        dict_nodes[f"{entity}"] = node_choose

    return dict_nodes


def combination_between_noun_phrases(list_entities: list)-> list:
    combinations_list = []
    combinations = itertools.combinations(list_entities, 2)
    for combination in combinations:
        combinations_list.append(combination)

    return combinations_list


def find_father(entity: str, dependencies: dict)-> list:
    father = []

    for k,v in dependencies.items():
        if entity in v:
            father.append(k)

    return father

class Node:

    def __init__(self, name):
        self.name = name
        self.father = None
        self.children = []

    def set_children(self, children):
        self.children = children
        for c in children:
            c.set_father(self)

    def set_father(self, father):
        self.father = father

    def search(self, name_of_node=None):
        for item in self:
            if item.name == name_of_node:
                return item

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
print(f"List entities: {list_entities}")
dict_dependencies = get_dict_dependencies(sentence)
print(f"Dict dependencies: {dict_dependencies}")
list_nodes = find_nodes(sentence)
print(f"List nodes: {list_nodes}")
dict_nodes = get_nodes_entities(list_entities, list_nodes)
print(f"Dict nodes: {dict_nodes}")
combination_noun_phrases = combination_between_noun_phrases(list_entities)
print(f"Combination noun phrases: {combination_noun_phrases}")

nodes = {}
for n in [Node(k) for k,v in dict_dependencies.items()]: nodes[n.name] = n
for k,n in nodes.items():
    children = dict_dependencies[n.name]
    n.set_children([nodes[c] for c in children])

for tuple_nodes in combination_noun_phrases:
    print(f"Nós: {tuple_nodes}")
    entity_0 = dict_nodes.get(f"{tuple_nodes[0]}")
    entity_1 = dict_nodes.get(f"{tuple_nodes[1]}")
    tuple_of_entities = (entity_0, entity_1)
    print(f"Entidades: {tuple_of_entities}")

    node_0 = nodes.get(f"{tuple_nodes[0]}")
    node_1 = nodes.get(f"{tuple_nodes[1]}")

    path_nodes = node_0.path(node_1)
    path = []
    for n in path_nodes:
        if n not in (entity_1, entity_0, node_0, node_1):
            path.append(n.name)

    relation = " ".join(path)

    print(f"Frase: {args.sentence}, Entidade 0: {entity_0}, Entidade 1: {entity_1}, Relação_encontrada: {relation}")


    if relation:
        field_names = ["Frase", "Entidade 0", "Entidade 1", "Relação_encontrada"]

        with open('docred_database/manual_test_spacy.csv', 'a') as f_object:
            dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
            writer = csv.DictWriter(f_object, fieldnames=field_names)
            writer.writerow({'Frase': args.sentence, 'Entidade 0': entity_0, 'Entidade 1': entity_1, 'Relação_encontrada': relation})

            f_object.close()
        print("Saved relation in csv")


# with open('test.txt', 'w') as f:
#     f.write(r)
