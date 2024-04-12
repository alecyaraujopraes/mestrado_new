import argparse
import csv
import itertools
import re

import spacy
from Levenshtein import jaro_winkler
from spacy.tokenizer import Tokenizer
from bert_utils import selection_by_bert_sc, selection_by_bert_resume


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

    def merge_punct(doc):
        spans = []
        for word in doc[:-1]:
            if word.is_punct or not word.nbor(1).is_punct:
                continue
            start = word.i
            end = word.i + 1
            while end < len(doc) and doc[end].is_punct:
                end += 1
            span = doc[start:end]
            spans.append((span, word.tag_, word.lemma_, word.ent_type_))
        with doc.retokenize() as retokenizer:
            for span, tag, lemma, ent_type in spans:
                attrs = {"tag": tag, "lemma": lemma, "ent_type": ent_type}
                retokenizer.merge(span, attrs=attrs)
        return doc
    
    doc = nlp(sentence)

    doc = merge_punct(doc)

    dict_dependencies = {}

    for token in doc:
        if token.text in dict_dependencies:
            new_children = [child.text for child in token.children]
            for item in new_children:
                dict_dependencies[token.text].append(item)
                if item in dict_dependencies.keys():
                    if token.text not in dict_dependencies[item]:
                        dict_dependencies[item].append(token.text)
        else:
            dict_dependencies[token.text] = [child.text for child in token.children]

            for child in token.children:
                if child.text in dict_dependencies.keys():
                    if token.text not in dict_dependencies[child.text]:
                        dict_dependencies[child.text].append(token.text)

    return dict_dependencies


def find_entities(text: str)-> list:
    doc = nlp(text)
    list_entities = []

    for entity in doc.ents:
        str1 = entity.text
        if str1 not in list_entities:
            list_entities.append(str1)

    return list_entities


def find_nodes(sentence: str)-> list:
    try:
        nlp.add_pipe("merge_noun_chunks")
        nlp.add_pipe("merge_entities")
    except:
        pass

    def merge_punct(doc):
        spans = []
        for word in doc[:-1]:
            if word.is_punct or not word.nbor(1).is_punct:
                continue
            start = word.i
            end = word.i + 1
            while end < len(doc) and doc[end].is_punct:
                end += 1
            span = doc[start:end]
            spans.append((span, word.tag_, word.lemma_, word.ent_type_))
        with doc.retokenize() as retokenizer:
            for span, tag, lemma, ent_type in spans:
                attrs = {"tag": tag, "lemma": lemma, "ent_type": ent_type}
                retokenizer.merge(span, attrs=attrs)
        return doc
    
    doc = nlp(sentence)

    doc = merge_punct(doc)

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
            if entity in node:
                node_inside = node

        if jaro_winkler(entity, node_choose) > 0.75:
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


def get_path(dict_dependencies, n_0, n_1, node_0, node_1):
    path_nodes = node_0.path(node_1)
    path = []
    for n in path_nodes:
        path.append(n.name)

    if not path and n_1 in dict_dependencies.get(n_0):
        path = [n_0, n_1]

    if not path:
        path_nodes = node_1.path(node_0)
        path = []
        for n in path_nodes:
            path.append(n.name)

    if not path and n_0 in dict_dependencies.get(n_1):
        path = [n_1, n_0]

    return path


paragraph = args.sentence
sents = split_in_sentences(paragraph)


def co_referee(text: str):
    try:
        nlp.add_pipe('coreferee')
    except:
        pass

    doc = nlp(text)

    list_words = re.findall(r"[\w']+|[.,!?;()]", text)

    list_referees = []

    for item in doc._.coref_chains:
        temp_list = []
        print(item)
        for k in item:
            print(k[0])
            temp_list.append(list_words[k[0]])

        list_referees.append(temp_list)
    
    return list_referees

url = sents[0].split(" ")[0]

for sentence in sents:
    print(f"Sentence: {sentence}")
    # list_entities = find_entities(sentence)
    list_entities = [
        "COVID-19",
        "coronavirus disease 2019",
        "virus",
        "severe acute respiratory syndrome coronavirus 2",
        "SARS-CoV-2",
        "pandemic",
        "illness",
        "symptoms",
        "vaccine",
        "hospital care",
        "death",
        "air flow",
        "physical distancing",
        "mask",
        "hygiene",
        "medicine",
        "long-term effects",
        "dry cough",
        "shortness of breath",
        "loss of taste",
        "loss of smell",
        "fatigue",
        "digestive symptoms",
        "upset stomach",
        "vomiting",
        "diarrhea",
        "pain",
        "headaches",
        "body aches",
        "muscle aches",
        "fever",
        "chills",
        "cold-like symptoms",
        "congestion",
        "runny nose",
        "sore throat",
        "asymptomatic",
        "presymptomatic",
        "hospitalization",
        "respiratory system",
        "multisystem inflammatory syndrome",
        "MIS-C",
        "MIS-A",
        "healthcare professional",
        "emergency help",
        "breathing problems",
        "confusion",
        "chest pain",
        "risk factors",
        "infection",
        "transmission",
        "droplets",
        "mutations",
        "pets",
        "surface transmission",
        "COVID-19 vaccine",
        "immune defense",
        "inflammation",
        "blood clots",
        "kidney injury",
        "post-COVID-19 syndrome",
        "long COVID",
        "PASC",
        "vaccination",
        "Pfizer-BioNTech COVID-19 vaccine",
        "Moderna COVID-19 vaccine",
        "Novavax COVID-19 vaccine",
        "immune system",
        "body mass index",
        "risk assessment",
        "serious illness",
        "complications",
        "acute respiratory distress syndrome",
        "shock",
        "inflammatory response",
        "travel",
        "masking",
    ]
    print(f"List entities: {list_entities}")
    # list_referees = co_referee(paragraph)
    # print(f"Referees: {list_referees}")
    dict_dependencies = get_dict_dependencies(sentence)
    print(f"Dict dependencies: {dict_dependencies}")
    list_nodes = find_nodes(sentence)
    print(f"List nodes: {list_nodes}")
    dict_nodes = get_nodes_entities(list_entities, list_nodes)
    print(f"Dict nodes: {dict_nodes}")
    combination_entities = combination_between_noun_phrases(list_entities)
    print(f"Combination entities: {combination_entities}")


    nodes = {}
    for n in [Node(k) for k,v in dict_dependencies.items()]: nodes[n.name] = n
    for k,n in nodes.items():
        children = dict_dependencies[n.name]
        n.set_children([nodes[c] for c in children])
    # print(f"Nodes: {nodes}")


    for tuple_entities in combination_entities:
            print(f"Entidades: {tuple_entities}")
            n_0 = dict_nodes.get(f"{tuple_entities[0]}")
            n_1 = dict_nodes.get(f"{tuple_entities[1]}")
            tuple_nodes = n_0, n_1
            print(f"Nós: {n_0, n_1}")

            try:
                idx_n_0 = list_nodes.index(n_0)
                idx_n_1 = list_nodes.index(n_1)
                tuple_idx_nodes = idx_n_0, idx_n_1
                print(f"Index nodes: {idx_n_0, idx_n_1}")

                node_0 = nodes.get(f"{n_0}")
                node_1 = nodes.get(f"{n_1}")
                print(f"Nodes: {node_0, node_1}")

                if node_0 and node_1:
                    path = get_path(dict_dependencies, n_0, n_1, node_0, node_1)
                    print(f"Path: {path}")
                    if path:
                        relation = " ".join(path)
                        print(f"Relation: {relation}")

                        if tuple_entities[0] != tuple_entities[1]:

                            id, id_rel, way, relation_found_by_bert  = selection_by_bert_sc(tuple_entities[0], tuple_entities[1], f"{tuple_entities[0]} {relation} {tuple_entities[1]}")
                            print(f"Relation found by bert sentence transformer: {relation_found_by_bert, id}")          

                            print(f"Frase: {sentence}, Entidade_0: {tuple_entities[0]}, Entidade_1: {tuple_entities[1]}, Nos: {(n_0, n_1)}, Idx_nodes: {idx_n_0, idx_n_1}, Path: {relation}, Relacao_encontrada: {relation_found_by_bert}, url: {url}")

                            field_names = ["Frase", "Entidade_0", "Entidade_1", "Nos", "Idx_nodes", "Path", "Relacao_encontrada", "url"]

                            with open('medical_database/manual_test_spacy.csv', 'a') as f_object:
                                dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
                                writer = csv.DictWriter(f_object, fieldnames=field_names, quoting=csv.QUOTE_NONE, escapechar='\\', delimiter='|')
                                writer.writerow({'Frase': sentence, 'Entidade_0': tuple_entities[0], 'Entidade_1': tuple_entities[1], 'Nos': tuple_nodes, 'Idx_nodes': tuple_idx_nodes, 'Path': relation, 'Relacao_encontrada': relation_found_by_bert, 'url': url})

                                f_object.close()
                            print("Saved relation in csv")

            except:
                pass