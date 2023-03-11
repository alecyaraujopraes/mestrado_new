import spacy
import argparse
import csv


nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("merge_noun_chunks")


argParser = argparse.ArgumentParser()
argParser.add_argument("-s", "--sentence", help="Complete sentence")
argParser.add_argument("-e0", "--entities0", help="Entity 0")
argParser.add_argument("-e1", "--entities1", help="Entity 1")


args = argParser.parse_args()


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
    entity_2 = entities[1]

    paths_list = paths(sentence)

    for path in paths_list:
        if entity_1 in path and entity_2 in path:
            path.remove(entity_1)
            path.remove(entity_2)
            path_str = ' '.join([str(elem) for elem in path])
            return path_str

tuple_of_entities = (args.entities0, args.entities1)

relation = find_relation_between_entities_spacy(args.sentence, tuple_of_entities)
print(relation)

if relation:
    field_names = ["Frase", "Entidades", "Relação_encontrada_por_mim", "Relação_encontrada_no_benchmark"]

    with open('manual_test_spacy.csv', 'a') as f_object:
        dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
        writer = csv.DictWriter(f_object, fieldnames=field_names)
        writer.writerow({'Frase': args.sentence, 'Entidades': tuple_of_entities, 'Relação_encontrada_por_mim': relation})

        f_object.close()
    print("Saved relation in csv")


# with open('test.txt', 'w') as f:
#     f.write(r)
