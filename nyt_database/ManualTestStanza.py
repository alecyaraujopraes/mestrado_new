import json

import pandas as pd

from nyt_database.ParseSyntaticTree import (Node, aggregate_NNP, all_combinations_entities,
                               constituency, find_entities,
                               find_relation_between_entities)

files = ["test.json"]
# , "train.json", "valid.json"]

list_obj = []

for file in files:
    with open(file, "r") as f:
        for line in f.readlines():
            obj = json.loads(line)
            list_obj.append(obj)


# Relações encontradas pelo benchmark e encontradas pelo Stanza ou não
i = 0
relations_dict = {}

for item in list_obj:

    sentence = item.get("sentText")
    nested_list = constituency(sentence)
    entities_list = find_entities(sentence)
    combinations = all_combinations_entities(entities_list)

    root = Node(nested_list)

    aggregate_NNP(root)

    for relation in item.get("relationMentions"):
        if "location" not in relation.get("label"):

            if ((relation.get("em1Text"), relation.get("em2Text")) in combinations):
                print(f"Relação encontrada: {relation.get('em1Text'), relation.get('em2Text')}")
                entity_0 = relation.get("em1Text")
                entity_1 = relation.get("em2Text")
                relation_found = find_relation_between_entities(root, (entity_0, entity_1))
                print(f"Relation found: {relation_found}")
                print(f"Relation dataset: {relation.get('label')}")
                relations_dict[f"row_{i}"] = [sentence, f"({entity_0, entity_1})", f"{relation_found}", f"{relation.get('label')}"]
                print([sentence, f"({entity_0, entity_1})", f"{relation_found}", f"{relation.get('label')}"])
                print(f"Salvo sentença {i}")

            elif ((relation.get("em2Text"), relation.get("em1Text")) in combinations):
                print(f"Relação encontrada: {relation.get('em2Text'), relation.get('em1Text')}")
                entity_0 = relation.get("em2Text")
                entity_1 = relation.get("em1Text")
                relation_found = find_relation_between_entities(root, (entity_0, entity_1))
                print(f"Relation found: {relation_found}")
                print(f"Relation dataset: {relation.get('label')}")
                print([sentence, f"({entity_0, entity_1})", f"{relation_found}", f"{relation.get('label')}"])
                relations_dict[f"row_{i}"] = [sentence, f"({entity_0, entity_1})", f"{relation_found}", f"{relation.get('label')}"]
                print(f"Salvo sentença {i}")

            else:
                print(f"Relação não encontrada: {relation.get('em1Text'), relation.get('em2Text')}")
                relations_dict[f"row_{i}"] = [sentence, f"{relation.get('em1Text'), relation.get('em2Text')}", "Relation not found", f"{relation.get('label')}"]
                print([sentence, f"{relation.get('em1Text'), relation.get('em2Text')}", "Relation not found", f"{relation.get('label')}"])
                print(f"Salvo sentença {i}")
            i += 1

df = pd.DataFrame.from_dict(relations_dict, orient='index')
df.to_csv("manual_test_spacy.csv", encoding="utf-8", index=False)

# Relações encontradas pelo Stanza e não encontradas pelo benchmark
# j = 0
# relations_dict_nf = {}

# for relation_found in relations_dict:


#     for relation in combinations:
#         if ((relation.get("em1Text"), relation.get("em2Text")) in combinations) or ((relation.get("em2Text"), relation.get("em1Text")) in combinations):
#             print(f"Relação encontrada: {relation.get('em1Text'), relation.get('em2Text')}")
#             entity_0 = relation.get("em1Text")
#             entity_1 = relation.get("em2Text")
#             relation_found = find_relation_between_entities(root, (entity_0, entity_1))
#             print(f"Relation found: {relation_found}")
#             print(f"Relation dataset: {relation.get('label')}")
#             relations_dict_nf[f"row_{j}"] = [sentence, f"({entity_0, entity_0})", f"{relation_found}", f"{relation.get('label')}"]
#             j += 1
#             print(f"Salvo sentença {j}")

#         else:
#             print(f"Relação não encontrada: {relation.get('em1Text'), relation.get('em2Text')}")
#             relations_dict_nf[f"row_{j}"] = [sentence, f"{relation.get('em1Text', relation.get('em2Text'))}", "Relation not found", f"{relation.get('label')}"]
#             j += 1

# df = pd.DataFrame.from_dict(relations_dict_nf, orient='index')
# df.to_csv("manual_test_nf.csv", encoding="utf-8", index=False)
