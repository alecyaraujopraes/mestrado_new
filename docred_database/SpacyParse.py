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


def path(sentence: str, begin: str, final: str, list_path=[]):
    doc = nlp(sentence)
    dict_dependencies = {}

    for token in doc:
        dict_dependencies[token.text] = [child.text for child in token.children]
    # print(f"Dict dependencies: {dict_dependencies}")

    if begin not in dict_dependencies:
        for k, v in dict_dependencies.items():
            if begin in k:
                begin = k
    if final not in dict_dependencies:
        for k, v in dict_dependencies.items():
            if final in k:
                final = k
    

    list_path = list_path + [begin]
    if final == begin:
        return list_path
    else:
        if not dict_dependencies.get(begin):
            list_path = list(set(list_path) - set([begin]))
            return list_path
        else:
            for n in dict_dependencies.get(begin):
                path2 = path(n, final, list_path=list_path)
                if len(path2) > len(list_path): return path2
            list_path = list(set(list_path) - set([begin]))
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
