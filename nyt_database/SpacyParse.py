import json

import spacy

from nyt_database.ParseSyntaticTree import all_combinations_entities, find_entities

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("merge_noun_chunks")
sentence = "Mary L. Schapiro , who earlier this year became the new head of NASD , was more amenable to fashioning a deal to the New York Exchange 's liking than her predecessor , Robert R. Glauber ."


def dependency_between_words(sentence: str, words_tuple: tuple) -> bool:
    doc = nlp(sentence)
    dict_dependencies = {}

    for token in doc:
        dict_dependencies[token.text] = [child.text for child in token.children]

    print(f"DICT DEPENDENCIES: {dict_dependencies}")
    word1 = words_tuple[0]
    word2 = words_tuple[1]

    if " " in word1:
        word1 = word1.split()

    if " " in word2:
        word2 = word2.split()

    def child_get(head, list_childs: list) -> list:
        if type(head) == list:
            for item in head:
                child = dict_dependencies.get(item)
                if child:
                    list_childs.extend(child)
                    child_get(child, list_childs)

        elif type(head) == str:
            child = dict_dependencies.get(head)
            list_childs.append(child)
            child_get(child, list_childs)
        
        return list_childs
    
    list_childs = child_get(word1, [])

    print(f"LIST CHILDS: {list_childs}")
    print(f"WORD2: {word2}")

    if type(word2) == list:
        print(f"ENTRADA CONDIÇÃO LISTA WORD2")
        for item2 in word2:
            if item2 in list_childs:
                return True

    if type(word2) == str:
        print(f"ENTRADA CONDIÇÃO STRING WORD2")
        if word2 in list_childs:
            return True

    return False


def paths(sentence: str) -> list:
    doc = nlp(sentence)
    dict_dependencies = {}

    for token in doc:
        dict_dependencies[token.text] = [child.text for child in token.children]

    def path_item(key: str, value: list, path_list: list) -> list:

        for ch in value:
            path_list.append([key, ch])

        for path in path_list:
            if key in path:
                len_path = len(path)
                last_item = path[len_path - 1]
                if key == last_item and value:
                    for child in value:
                        path_new = path.copy()
                        path_new.append(child)
                        path_list.append(path_new)
                    path_list.remove(path)

        return path_list

    path_list = []
    for key, value in dict_dependencies.items():
        path_item(key, value, path_list)

    return path_list


def find_relation_between_entities_spacy(sentence: str, entities: tuple) -> str:
    entity_1 = entities[0]
    print(f"entity_1: {entity_1}")
    entity_2 = entities[1]
    print(f"entity_2: {entity_2}")

    paths_list = paths(sentence)
    print(f"paths_list: {paths_list}")

    for path in paths_list:
        if entity_1 in path and entity_2 in path:
            path.remove(entity_1)
            path.remove(entity_2)
            path_str = ' '.join([str(elem) for elem in path])
            print(f"path_str: {path_str}")
            return path_str
