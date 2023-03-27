import spacy
import argparse
import csv


nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("merge_noun_chunks")


argParser = argparse.ArgumentParser()
argParser.add_argument("-s", "--sentence", help="Complete sentence")
argParser.add_argument("-e0", "--entities0", help="Entity 0")
argParser.add_argument("-e1", "--entities1", help="Entity 1")
argParser.add_argument("-r", "--relation_annotated", help="Relation between entities")

args = argParser.parse_args()

def find_entities(entity_given: str, dict_dependencies: dict)-> list:
    if entity_given in dict_dependencies:
        entity_given = [entity_found]
    else:
        for k, v in dict_dependencies.items():
            if entity_given in k:
                entity_found = [k]

    if entity_found == None:
        possible_entities = []
        x = entity_given.split()
        for entity in x:
            for k,v in dict_dependencies.items():
                if entity in k:
                    possible_entities.append(k)
        entity_found = possible_entities

    return entity_found


def path(sentence: str, start: str, end: str, list_path=[]):
    doc = nlp(sentence)
    dict_dependencies = {}

    for token in doc:
        dict_dependencies[token.text] = [child.text for child in token.children]
    
    list_entity_0 = find_entities(start, dict_dependencies)
    list_entity_1 = find_entities(end, dict_dependencies)

    for entity_0 in list_entity_0:
        for entity_1 in list_entity_1:

            list_path = list_path + [entity_0]
            if entity_1 == entity_0:
                return list_path
            else:
                if not dict_dependencies.get(entity_0):
                    list_path = list(set(list_path) - set([entity_0]))
                    return list_path
                else:
                    for n in dict_dependencies.get(entity_0):
                        path2 = path(n, entity_1, list_path=list_path)
                        if len(path2) > len(list_path): return path2
                    list_path = list(set(list_path) - set([entity_0]))
                    return list_path


def find_relation_between_entities_spacy(sentence: str, entities: tuple) -> str:
    entity_1 = entities[0]
    entity_2 = entities[1]

    path_list = path(sentence, entity_1, entity_2, list_path=[])
    print(f"Path list: {path_list}")

    if entity_1 in path_list and entity_2 in path_list:
        path_list.remove(entity_1)
        path_list.remove(entity_2)
        path_str = ' '.join([str(elem) for elem in path_list])
        return path_str

tuple_of_entities = (args.entities0, args.entities1)
# print(f"Entidades: {tuple_of_entities}")

relation = find_relation_between_entities_spacy(args.sentence, tuple_of_entities)
print(relation)
relation_annotated = args.relation_annotated

print(f"Frase: {args.sentence}, Entidades: {tuple_of_entities}, Relação_encontrada_por_mim: {relation}, Relação_encontrada_no_benchmark: {relation_annotated}")


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
