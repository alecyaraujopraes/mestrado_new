from re import compile
from xml.dom.xmlbuilder import DocumentLS

import stanza
from stanza.models.common.doc import Document

stanza.download("en") # download English model

nlp = stanza.Pipeline("en") # initialize English neural pipeline

def find_entities(sentence: str) -> list:
    entities_list = []

    doc = nlp(sentence)
    # print(f"Frase: {sentence}")
    for entity in doc.entities:
        entities_list.append(entity.text)

    return entities_list


def foo(string: str) -> list:
    resexp = compile(r'([()]|_!)')
    def foo_helper(level=0):
        try:
            token = next(tokens)
        except StopIteration:
            if level != 0:
                raise Exception('missing closing paren')
            else:
                return []
        if token == ')':
            if level == 0:
                raise Exception('missing opening paren')
            else:
                return []
        elif token == '(':
            return [foo_helper(level+1)] + foo_helper(level)
        else:
            return [token] + foo_helper(level)
    tokens = iter(filter(None, (i.strip() for i in resexp.split(string))))
    return foo_helper()


def constituency(setence: str) -> list:
    doc = nlp(sentence)

    for item in doc.sentences:
        str_constituency = str(item.constituency)
        nested_list = foo(str_constituency)
        return nested_list


def find_nodes(constituency_list: list):
    for item in constituency_list:
        print(item)

    return 

eg = [
    {
        "sentText": "But that spasm of irritation by a master intimidator was minor compared with what Bobby Fischer , the erratic former world chess champion , dished out in March at a news conference in Reykjavik , Iceland .", 
        "articleId": "/m/vinci8/data1/riedel/projects/relation/kb/nyt1/docstore/nyt-2005-2006.backup/1677367.xml.pb", 
        "relationMentions": [
            {"em1Text": "Bobby Fischer", "em2Text": "Iceland", "label": "/people/person/nationality"}, 
            {"em1Text": "Iceland", "em2Text": "Reykjavik", "label": "/location/country/capital"}, 
            {"em1Text": "Iceland", "em2Text": "Reykjavik", "label": "/location/location/contains"}, 
            {"em1Text": "Bobby Fischer", "em2Text": "Reykjavik", "label": "/people/deceased_person/place_of_death"}
        ], 
        "entityMentions": [
            {"start": 0, "label": "PERSON", "text": "Bobby Fischer"}, 
            {"start": 1, "label": "LOCATION", "text": "Reykjavik"}, 
            {"start": 2, "label": "LOCATION", "text": "Iceland"}
        ], 
        "sentId": "1"},
    {
        "sentText": "The final deal was brokered through the major assistance of Annette L. Nazareth , an S.E.C. commissioner who once led its market regulation office , and Frank G. Zarb , the former chairman of NASD and a major presence on Wall Street and in Washington for much of his career .", 
        "articleId": "/m/vinci8/data1/riedel/projects/relation/kb/nyt1/docstore/nyt-2005-2006.backup/1808144.xml.pb", 
        "relationMentions": [
            {"em1Text": "Frank G. Zarb", "em2Text": "NASD", "label": "/business/person/company"}
        ],
        "entityMentions": [
            {"start": 2, "label": "PERSON", "text": "Frank G. Zarb"}, 
            {"start": 3, "label": "ORGANIZATION", "text": "NASD"}, 
            {"start": 4, "label": "LOCATION", "text": "Washington"}
        ], 
        "sentId": "1"},
    {
        "sentText": "Mary L. Schapiro , who earlier this year became the new head of NASD , was more amenable to fashioning a deal to the New York Exchange 's liking than her predecessor , Robert R. Glauber .", 
        "articleId": "/m/vinci8/data1/riedel/projects/relation/kb/nyt1/docstore/nyt-2005-2006.backup/1808144.xml.pb", 
        "relationMentions": [
            {"em1Text": "Robert R. Glauber", "em2Text": "NASD", "label": "/business/person/company"}
        ],
        "entityMentions": [
            {"start": 1, "label": "ORGANIZATION", "text": "NASD"}, 
            {"start": 3, "label": "PERSON", "text": "Robert R. Glauber"}
        ], 
        "sentId": "2"},
    {
        "sentText": "It will be the final movie credited to Debra Hill , a film producer and native of Haddonfield , who produced '' Halloween '' and was considered a pioneering woman in film .", 
        "articleId": "/m/vinci8/data1/riedel/projects/relation/kb/nyt1/docstore/nyt-2005-2006.backup/1713720.xml.pb", 
        "relationMentions": [
            {"em1Text": "Debra Hill", "em2Text": "Haddonfield", "label": "/people/person/place_of_birth"}
        ],
        "entityMentions": [
            {"start": 0, "label": "LOCATION", "text": "Debra Hill"},
            {"start": 1, "label": "LOCATION", "text": "Haddonfield"}
        ], 
        "sentId": "1"},
    {
        "sentText": "Under pressure from Mr. Kerkorian and other disgruntled shareholders , Mr. Wagoner started talks on Friday in Detroit with Carlos Ghosn , the chief executive of Renault and Nissan .", 
        "articleId": "/m/vinci8/data1/riedel/projects/relation/kb/nyt1/docstore/nyt-2005-2006.backup/1777410.xml.pb", 
        "relationMentions": [
            {"em1Text": "Carlos Ghosn", "em2Text": "Renault", "label": "/business/person/company"}
        ], 
        "entityMentions": [
            {"start": 1, "label": "PERSON", "text": "Wagoner"}, 
            {"start": 2, "label": "LOCATION", "text": "Detroit"}, 
            {"start": 3, "label": "PERSON", "text": "Carlos Ghosn"}, 
            {"start": 4, "label": "ORGANIZATION", "text": "Renault"}
        ], 
        "sentId": "1"},
    {
        "sentText": "Gov. Mitt Romney of Massachusetts has also proposed a bill to buy 500,000 of the computers for his state 's children .", 
        "articleId": "/m/vinci8/data1/riedel/projects/relation/kb/nyt1/docstore/nyt-2005-2006.backup/1723883.xml.pb", 
        "relationMentions": [
            {"em1Text": "Mitt Romney", "em2Text": "Massachusetts", "label": "/people/person/place_lived"}
        ], 
        "entityMentions": [
            {"start": 0, "label": "PERSON", "text": "Mitt Romney"}, 
            {"start": 1, "label": "LOCATION", "text": "Massachusetts"}
        ], 
        "sentId": "1"},
]


# for examples in eg:
#     sentence = examples["sentText"]

class TreeNode:
  "Create sentence tree"
  def __init__(self, sentence: str):
    self.sentence = sentence # data
    # self.children = [] # references to other nodes



sentence = "The final deal was brokered through the major assistance of Annette L. Nazareth , an S.E.C. commissioner who once led its market regulation office , and Frank G. Zarb , the former chairman of NASD and a major presence on Wall Street and in Washington for much of his career ."

entities = find_entities(sentence)
constituencies = constituency(sentence)

# print(f"List of entities: {entities}")
# print(f"Constituency: {constituencies}")

constituency_list = constituencies

def find_first_child(constituency_list: list):
    def find_node(const_list: list, nodes_f: list):
        for item in const_list:
            if len(item) == 1 and type(item) == list:
                print(f"Adicionando a lista de nodes: {item}")
                nodes_f.append(item)
            elif len(item) > 1 and type(item) == list:
                print(f"Nova lista: {item}")
                find_node(item, nodes_f)
        return nodes_f

    nodes = []
    for lists in constituency_list:
        nodes = find_node(lists, nodes)
        print(f"Nodes: {nodes}")

    return nodes


nodes_newest = find_first_child(constituency_list)

for no in nodes_newest:
    print(no)

#   def add_child(self, child_node):
#     # creates parent-child relationship
#     print("Adding " + child_node.value)
#     self.children.append(child_node)
    
#   def remove_child(self, child_node):
#     # removes parent-child relationship
#     print("Removing " + child_node.value + " from " + self.value)
#     self.children = [child for child in self.children 
#                      if child is not child_node]

#   def traverse(self):
#     # moves through each node referenced from self downwards
#     nodes_to_visit = [self]
#     while len(nodes_to_visit) > 0:
#       current_node = nodes_to_visit.pop()
#       print(current_node.value)
#       nodes_to_visit += current_node.children


# tree = TreeNode(sentence)



# Manipular a tree children tree.children[0].children
# 
# dicts = doc.to_dict()

# for list in dicts:
#     for word in list:
#         if word.get("upos") == "VERB":
#             print(word.get("text"))


# print("Entidades:")
# print(doc.entities)
