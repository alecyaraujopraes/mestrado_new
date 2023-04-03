import itertools
import json
from re import compile
from xml.dom.xmlbuilder import DocumentLS

import spacy
from Levenshtein import distance, jaro_winkler

nlp = spacy.load("en_core_web_sm")

text = ("Zest Airways , Inc. operated as AirAsia Zest ( formerly Asian Spirit and Zest Air ) , was a low - cost airline based at the Ninoy Aquino International Airport in Pasay City , Metro Manila in the Philippines .")

def find_entities(text: str)->list:

    doc = nlp(text)
    list_entities = []
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]

    for entity in doc.ents:
        # compare_old = 0
        str1 = entity.text
        list_entities.append(str1)
        # for str2 in noun_phrases:
        #     compare = jaro_winkler(str1, str2)
        #     if compare_old < compare:
        #         compare_old = compare
        #         ent_choose = str2
        # list_entities.append((str1, ent_choose))
    print(list_entities)
    return list_entities 

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


def find_father(entity: str, dependencies: dict)-> list:
    father = []

    for k,v in dependencies:
        if entity in v:
            father.append(k)

    return father


if __name__ == '__main__':

    sentence = "Zest Airways , Inc. operated as AirAsia Zest ( formerly Asian Spirit and Zest Air ) , was a low - cost airline based at the Ninoy Aquino International Airport in Pasay City , Metro Manila in the Philippines ."
    e0 = "Asian Spirit and Zest Air" 
    e1 = "Pasay City"

    dict_depedencies = {
        'Zest Airways , Inc.': [], 
        'operated': ['Zest Airways , Inc.', 'as'], 
        'as': ['AirAsia Zest'],
        'AirAsia Zest': ['(', 'formerly Asian Spirit', ')'], 
        '(': [], 
        'formerly Asian Spirit': ['and', 'Zest Air'], 
        'and': [], 
        'Zest Air': [], 
        ')': [], 
        ',': [], 
        'was': ['operated', ',', 'a low - cost airline', '.'], 
        'a low - cost airline': ['based', ',', 'Metro Manila'], 
        'based': ['at'], 
        'at': ['the Ninoy Aquino International Airport'], 
        'the Ninoy Aquino International Airport': ['in'], 
        'in': ['the Philippines'], 
        'Pasay City': [], 
        'Metro Manila': ['in'], 
        'the Philippines': [], 
        '.': []
    }

