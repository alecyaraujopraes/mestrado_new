import itertools
from re import compile
from xml.dom.xmlbuilder import DocumentLS

import spacy
from Levenshtein import distance, jaro_winkler

# text = ("Zest Airways , Inc. operated as AirAsia Zest ( formerly Asian Spirit and Zest Air ) , was a low - cost airline based at the Ninoy Aquino International Airport in Pasay City , Metro Manila in the Philippines .")


# def find_entities(text: str)->list:
#     nlp = spacy.load("en_core_web_sm")

#     doc = nlp(text)
#     list_entities = []
#     noun_phrases = [chunk.text for chunk in doc.noun_chunks]

#     for entity in doc.ents:
#         # compare_old = 0
#         str1 = entity.text
#         list_entities.append(str1)
#         # for str2 in noun_phrases:
#         #     compare = jaro_winkler(str1, str2)
#         #     if compare_old < compare:
#         #         compare_old = compare
#         #         ent_choose = str2
#         # list_entities.append((str1, ent_choose))

#     return list_entities 


class No:
    def __init__(self, father, children) -> None:
        self.father = father
        self.children = children

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


# def find_father(entity: str, dependencies: dict)-> list:
#     father = []

#     for k,v in dependencies:
#         if entity in v:
#             father.append(k)

#     return father


# if __name__ == '__main__':

#     sentence = "Zest Airways , Inc. operated as AirAsia Zest ( formerly Asian Spirit and Zest Air ) , was a low - cost airline based at the Ninoy Aquino International Airport in Pasay City , Metro Manila in the Philippines ."
#     e0 = "Asian Spirit and Zest Air" 
#     e1 = "Pasay City"

#     dict_depedencies = {
#         'Zest Airways , Inc.': [], 
#         'operated': ['Zest Airways , Inc.', 'as'], 
#         'as': ['AirAsia Zest'],
#         'AirAsia Zest': ['(', 'formerly Asian Spirit', ')'], 
#         '(': [], 
#         'formerly Asian Spirit': ['and', 'Zest Air'], 
#         'and': [], 
#         'Zest Air': [], 
#         ')': [], 
#         ',': [], 
#         'was': ['operated', ',', 'a low - cost airline', '.'], 
#         'a low - cost airline': ['based', ',', 'Metro Manila'], 
#         'based': ['at'], 
#         'at': ['the Ninoy Aquino International Airport'], 
#         'the Ninoy Aquino International Airport': ['in'], 
#         'in': ['the Philippines'], 
#         'Pasay City': [], 
#         'Metro Manila': ['in'], 
#         'the Philippines': [], 
#         '.': []
#     }


def split_in_sentences(paragraph: str)-> list:
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(paragraph)
    sents = []
    for sent in doc.sents:
        sents.append(sent.text)

    return sents


def get_dict_dependencies(sentence: str)-> dict:
    nlp = spacy.load("en_core_web_sm")
    try:
        nlp.add_pipe("merge_noun_chunks")
    except:
        pass
    doc = nlp(sentence)
    dict_dependencies = {}

    for token in doc:
        dict_dependencies[token.text] = [child.text for child in token.children]

    return dict_dependencies


def find_entities(text: str)-> list:
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    list_entities = []

    for entity in doc.ents:
        str1 = entity.text
        list_entities.append(str1)

    return list_entities


def find_nodes(sentence: str)-> list:
    nlp = spacy.load("en_core_web_sm")
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