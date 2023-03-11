'''
Created on Sep 5, 2022

@author: lapaesleme
'''
import itertools
import json
from re import compile
from xml.dom.xmlbuilder import DocumentLS

import stanza
from stanza.models.common.doc import Document

stanza.download("en") # download English model

nlp = stanza.Pipeline("en") # initialize English neural pipeline


class Node:

    def __init__(self, nested_list, father=None):
        if len(nested_list) == 1: 
            self.pos = nested_list[0].split(' ')[0]
            self.label = nested_list[0].split(' ')[1]
            self.father = father
            self.children = []
        else: 
            self.pos = nested_list[0]
            self.label = ''
            self.father = father
            self.children = [Node(c, self) for c in nested_list[1:]]
    
    def __repr__(self) -> str: 
        # return f"{self.pos} {self.label} {self.children}"
        return f"{self.pos} {self.label}"
    
    def great_grandchildren(self):
        return [gg for c in self.children for g in c.children for gg in g.children]
    
    def grandchildren(self):
        return [g for c in self.children for g in c.children]

    def depth(self):
        if not self.father: return 0 
        return 1 + self.father.depth()
    
    def local_height(self):
        if not self.children: return 0
        else: return 1 + max([c.local_height() for c in self.children])

    def search(self, pos=None, label=None):
        return [n for n in [self] + [c2 for c in self.children for c2 in c.search(pos=pos, label=label)]
                if (n.pos == pos or not pos) and (n.label == label or not label)]

    def check_items_in_list(self, pos=None) -> bool:
        for n in self.children:
            if n.pos != pos:
                return False
        return True

    def search2(self, list_nodes=[], pos=None, label=None):
        if (self.children) and (self.check_items_in_list(pos=pos) ==  True):
            if self not in list_nodes:
                list_nodes.append(self)

        for n in [self]:
            for c in n.children:
                c.search2(list_nodes, pos=pos, label=label)

    def leaves(self):
        if not self.children: return [self]
        else: return [l for c in self.children for l in c.leaves()]
        
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

    def print(self, level=0):
        print('. . ' * level + str(self))
        for c in self.children:
            c.print(level + 1)

    def search_contain(self, label=None):
        for n in [self]:
            if label in n.label:
                return n
            for c in n.children:
                c.search_contain(label=label)


def aggregate_NNP(node):
    list_nodes = []
    node.search2(list_nodes, pos="NNP")
    if list_nodes:
        for n in list_nodes:
            new_children = ""
            for child in n.children:
                if new_children != "":
                    new_children = new_children + " " + child.label
                else:
                    new_children = child.label
            n.children = []
            n.label = new_children
        return n


def aggregate_named_entities(node):
    for n in node.search(pos='NNP'):
        if not n.great_grandchildren() or n.local_height() < 4:
            n.label = [l.label for l in n.leaves()]
            n.label = ' '.join(n.label)
            n.children = []
    return node


def find_entities(sentence: str) -> list:
    
    entities_list = []

    doc = nlp(sentence)
    for entity in doc.entities:
        entities_list.append(entity.text)

    return entities_list


def all_combinations_entities(entities_list: list)-> list:

    combinations_list = []
    combinations = itertools.combinations(entities_list, 2)
    for combination in combinations:
        combinations_list.append(combination)
    return combinations_list


def constituency(sentence: str) -> list:

    def foo(string: str) -> list:
        resexp = compile(r'([()]|_!)')
        def foo_helper(level=0):
            try:
                token = next(tokens)
            except StopIteration:
                if level != 0:
                    raise Exception('missing closing parenthesis')
                else:
                    return []
            if token == ')':
                if level == 0:
                    raise Exception('missing opening parenthesis')
                else:
                    return []
            elif token == '(':
                return [foo_helper(level+1)] + foo_helper(level)
            else:
                return [token] + foo_helper(level)
        tokens = iter(filter(None, (i.strip() for i in resexp.split(string))))
        return foo_helper()


    doc = nlp(sentence)

    for item in doc.sentences:
        str_constituency = str(item.constituency)
        nested_list = foo(str_constituency)
        return nested_list[0]


def find_verb(verb_list: None, path_list: list)-> list:
    for item in path_list:
        if item.pos == "VP":
            for children in item.children:
                if "VB" in children.pos:
                    verb_list.append(children)
    return verb_list


def find_predicate(verb_node, predicate: None)-> str:
    for children in verb_node.children:
        if predicate is None:
            predicate = children.label
        elif children.label != "":
            predicate = predicate + " " + children.label
        predicate = find_predicate(children, predicate)
    return predicate


def find_relation_between_entities(root, pair_entities: tuple) -> str:
    node1 = root.search(label=pair_entities[0])
    node2 = root.search(label=pair_entities[1])

    if not node1:
        node1 = root.search_contain(label=pair_entities[0])

    if not node2:
        node2 = root.search_contain(label=pair_entities[1])

    if node1 and node2:
        path = node1[0].path(node2[0])
        node_verb = find_verb([], path)
        if node_verb:
            predicate_with_entity = find_predicate(node_verb[0].father, "")
        else:
            node_aux = path[len(path)-1]
            node_aux_father = node_aux.father.father
            predicate_with_entity = find_predicate(node_aux_father, "")
        predicate = predicate_with_entity.replace(pair_entities[0], "")
        predicate = predicate.replace(pair_entities[1], "")
        return predicate


if __name__ == '__main__':
    # files = ["test.json", "train.json", "valid.json"]

    # list_obj = []

    # for file in files:
    #     with open(file, "r") as f:
    #         for line in f.readlines():
    #             obj = json.loads(line)
    #             list_obj.append(obj)


    # for item in list_obj:
    #     print(f"Item: {item}")
        # for sentence in item.get("sentText"):
    # sentence = "Mary L. Schapiro , who earlier this year became the new head of NASD , was more amenable to fashioning a deal to the New York Exchange 's liking than her predecessor , Robert R. Glauber ."
    # print(f"Sentence: {sentence}")
    # nested_list = constituency(sentence)
    # entities_list = find_entities(sentence)
    # print(f"Lista de entidades: {entities_list}")
    # combinations = all_combinations_entities(entities_list)
    # print(f"Lista de combinações: {combinations}")

    # root = Node(nested_list)

    # aggregate_NNP(root)

    # root.print()

    # for pair_entities in combinations:
    #     for relation in item.get("relationMentions"):
    #             if pair_entities[0] == relation.get("em1Text") and pair_entities[1] == relation.get("em2Text"):
    #                 print(f"Pair entities: entity 1 = {pair_entities[0]}, entity 2 = {pair_entities[1]}")
    #                 # find_relation_between_entities((pair_entities[0], pair_entities[1]))
                
        
    # sentence = "The final deal was brokered through the major assistance of Annette L. Nazareth , an S.E.C. commissioner who once led its market regulation office , and Frank G. Zarb , the former chairman of NASD and a major presence on Wall Street and in Washington for much of his career ."
    # sentence = "But that spasm of irritation by a master intimidator was minor compared with what Bobby Fischer , the erratic former world chess champion , dished out in March at a news conference in Reykjavik , Iceland ."
    sentence = "Mary L. Schapiro , who earlier this year became the new head of NASD , was more amenable to fashioning a deal to the New York Exchange 's liking than her predecessor , Robert R. Glauber ."
    # sentence = "It will be the final movie credited to Debra Hill , a film producer and native of Haddonfield , who produced '' Halloween '' and was considered a pioneering woman in film ."
    # sentence = "Under pressure from Mr. Kerkorian and other disgruntled shareholders , Mr. Wagoner started talks on Friday in Detroit with Carlos Ghosn , the chief executive of Renault and Nissan ."
    # sentence = "Gov. Mitt Romney of Massachusetts has also proposed a bill to buy 500,000 of the computers for his state 's children ."

    nested_list = constituency(sentence)
    entities_list = find_entities(sentence)
    print(f"Lista de entidades: {entities_list}")
    combinations = all_combinations_entities(entities_list)
    print(f"Lista de combinações: {combinations}")

    root = Node(nested_list)

    aggregate_NNP(root)

    for pair_entities in combinations:
        print(f"Pair entities: entity 1 = {pair_entities[0]}, entity 2 = {pair_entities[1]}")
        predicate = find_relation_between_entities(root, (pair_entities[0], pair_entities[1]))
        print(f"Printando resultado da find_predicate: {predicate}")
        
    root.print()
#  Calcular precision e recall https://en.wikipedia.org/wiki/Precision_and_recall
