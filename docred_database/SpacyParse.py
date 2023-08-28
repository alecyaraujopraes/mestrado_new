import argparse
import csv
import itertools
import re

import spacy
from Levenshtein import jaro_winkler
from spacy.tokenizer import Tokenizer

nlp = spacy.load("en_core_web_sm")

argParser = argparse.ArgumentParser()
argParser.add_argument("-s", "--sentence", help="Complete paragraph")

args = argParser.parse_args()

def split_in_sentences(paragraph: str)-> list:
    doc = nlp(paragraph)
    sents = []
    for sent in doc.sents:
        sents.append(sent.text)

    return sents


def get_dict_dependencies(sentence: str)-> dict:
    try:
        nlp.add_pipe("merge_noun_chunks")
        nlp.add_pipe("merge_entities")
    except:
        pass
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
    suffix_re = re.compile(r"""[\\]\\"']$""")
    def custom_tokenizer(nlp):
        return Tokenizer(nlp.vocab, suffix_search=suffix_re.search)

    nlp.tokenizer = custom_tokenizer(nlp)
    doc = nlp(sentence)

    noun_phrases = []

    for token in doc:
        noun_phrases.append(token.text)

    return noun_phrases


def get_nodes_entities(list_entities: str, list_nodes: str)-> dict:
    dict_nodes = {}
    for entity in list_entities:
        compare_old = 0
        node_choose = ""
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


paragraph = args.sentence
sents = split_in_sentences(paragraph)

for sentence in sents:
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
    print(f"Nodes: {nodes}")

    for tuple_nodes in combination_noun_phrases:
        print(f"Nós: {tuple_nodes}")
        entity_0 = dict_nodes.get(f"{tuple_nodes[0]}")
        entity_1 = dict_nodes.get(f"{tuple_nodes[1]}")
        tuple_of_entities = (entity_0, entity_1)
        print(f"Entidades: {tuple_of_entities}")

        node_0 = nodes.get(f"{tuple_nodes[0]}")
        node_1 = nodes.get(f"{tuple_nodes[1]}")

        if node_0 and node_1:
            path_nodes = node_0.path(node_1)
            path = []
            for n in path_nodes:
                path.append(n.name)

            relation = " ".join(path)

            if relation:

                print(f"Frase: {paragraph}, Entidade_0: {entity_0}, Entidade_1: {entity_1}, Relacao_encontrada: {relation}")

                field_names = ["Frase", "Entidade_0", "Entidade_1", "Relacao_encontrada"]

                with open('docred_database/manual_test_spacy.csv', 'a') as f_object:
                    dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
                    writer = csv.DictWriter(f_object, fieldnames=field_names, quoting=csv.QUOTE_NONE, escapechar='\\', delimiter='|')
                    writer.writerow({'Frase': paragraph, 'Entidade_0': entity_0, 'Entidade_1': entity_1, 'Relacao_encontrada': relation})

                    f_object.close()
                print("Saved relation in csv")