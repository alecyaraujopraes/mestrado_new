import json

import pandas as pd
# import nyt_database.SpacyParse2 as SpacyParse2
# from nyt_database.ParseSyntaticTree import (Node, aggregate_NNP, all_combinations_entities,
#                                constituency, find_entities)
# from nyt_database.SpacyParse import find_relation_between_entities_spacy

docred = pd.read_csv("docred_database/docred.csv")

list_sentences = []

for sentence in docred["sentences"].tolist():
    list_sentences.append(sentence)

i = 0
# df = pd.DataFrame(list())
relations_dict = {}

for item in list_sentences:

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
                relations_dict[f"row_{i}"] = [sentence, f"({entity_0, entity_1})"]
                relation_found = find_relation_between_entities_spacy(sentence, (entity_0, entity_1))
                print(f"Relation found: {relation_found}")
                print(f"Relation dataset: {relation.get('label')}")
                relations_dict[f"row_{i}"] = [sentence, f"({entity_0, entity_1})", f"{relation_found}", f"{relation.get('label')}"]
                print([sentence, f"({entity_0, entity_1})", f"{relation_found}", f"{relation.get('label')}"])
                print(f"Salvo sentença {i}")

            elif ((relation.get("em2Text"), relation.get("em1Text")) in combinations):
                print(f"Relação encontrada: {relation.get('em2Text'), relation.get('em1Text')}")
                entity_0 = relation.get("em2Text")
                entity_1 = relation.get("em1Text")
                relations_dict[f"row_{i}"] = [sentence, f"({entity_0, entity_1})"]
                relation_found = find_relation_between_entities_spacy(sentence, (entity_0, entity_1))
                print(f"Relation found: {relation_found}")
                print(f"Relation dataset: {relation.get('label')}")
                print([sentence, f"({entity_0, entity_1})", f"{relation_found}", f"{relation.get('label')}"])
                relations_dict[f"row_{i}"] = [sentence, f"({entity_0, entity_1})", f"{relation_found}", f"{relation.get('label')}"]
                print(f"Salvo sentença {i}")

            else:
                print(f"Relação não encontrada: {relation.get('em1Text'), relation.get('em2Text')}")
                relations_dict[f"row_{i}"] = [sentence, f"{relation.get('em1Text'), relation.get('em2Text')}"]
                relations_dict[f"row_{i}"] = [sentence, f"{relation.get('em1Text'), relation.get('em2Text')}", "Relation not found", f"{relation.get('label')}"]
                print([sentence, f"{relation.get('em1Text'), relation.get('em2Text')}", "Relation not found", f"{relation.get('label')}"])
                print(f"Salvo sentença {i}")
            i += 1




# import json

# import pandas as pd

# from ParseSyntaticTree import (Node, aggregate_NNP, all_combinations_entities,
#                                constituency, find_entities)
# from SpacyParse import find_relation_between_entities_spacy

# files = ["test.json"]
# # , "train.json", "valid.json"]

# list_obj = []

# for file in files:
#     with open(file, "r") as f:
#         for line in f.readlines():
#             obj = json.loads(line)
#             list_obj.append(obj)

# i = 0
# df = pd.DataFrame(list())
# df.to_csv('manual_test_spacy.csv')
# relations_dict = {}

# for item in list_obj:

#     sentence = item.get("sentText")
#     nested_list = constituency(sentence)
#     entities_list = find_entities(sentence)
#     combinations = all_combinations_entities(entities_list)

#     root = Node(nested_list)

#     aggregate_NNP(root)

#     for relation in item.get("relationMentions"):
#         if "location" not in relation.get("label"):

#             if ((relation.get("em1Text"), relation.get("em2Text")) in combinations):
#                 print(f"Relação encontrada: {relation.get('em1Text'), relation.get('em2Text')}")
#                 entity_0 = relation.get("em1Text")
#                 entity_1 = relation.get("em2Text")
#                 relations_dict[f"row_{i}"] = [sentence, f"({entity_0, entity_1})"]
#                 relation_found = find_relation_between_entities_spacy(sentence, (entity_0, entity_1))
#                 print(f"Relation found: {relation_found}")
#                 print(f"Relation dataset: {relation.get('label')}")
#                 relations_dict[f"row_{i}"] = [sentence, f"({entity_0, entity_1})", f"{relation_found}", f"{relation.get('label')}"]
#                 print([sentence, f"({entity_0, entity_1})", f"{relation_found}", f"{relation.get('label')}"])
#                 print(f"Salvo sentença {i}")

#             elif ((relation.get("em2Text"), relation.get("em1Text")) in combinations):
#                 print(f"Relação encontrada: {relation.get('em2Text'), relation.get('em1Text')}")
#                 entity_0 = relation.get("em2Text")
#                 entity_1 = relation.get("em1Text")
#                 relations_dict[f"row_{i}"] = [sentence, f"({entity_0, entity_1})"]
#                 relation_found = find_relation_between_entities_spacy(sentence, (entity_0, entity_1))
#                 print(f"Relation found: {relation_found}")
#                 print(f"Relation dataset: {relation.get('label')}")
#                 print([sentence, f"({entity_0, entity_1})", f"{relation_found}", f"{relation.get('label')}"])
#                 relations_dict[f"row_{i}"] = [sentence, f"({entity_0, entity_1})", f"{relation_found}", f"{relation.get('label')}"]
#                 print(f"Salvo sentença {i}")

#             else:
#                 print(f"Relação não encontrada: {relation.get('em1Text'), relation.get('em2Text')}")
#                 relations_dict[f"row_{i}"] = [sentence, f"{relation.get('em1Text'), relation.get('em2Text')}"]
#                 relations_dict[f"row_{i}"] = [sentence, f"{relation.get('em1Text'), relation.get('em2Text')}", "Relation not found", f"{relation.get('label')}"]
#                 print([sentence, f"{relation.get('em1Text'), relation.get('em2Text')}", "Relation not found", f"{relation.get('label')}"])
#                 print(f"Salvo sentença {i}")
#             i += 1
    
        # if i == 50:
            # print(relations_dict)
            # field_names = ["Frase", "Entidades", "Relação encontrada no código", "Relação encontrada no benchmark"]
            # with open('manual_test_spacy.csv', 'a') as f_object:
            #     dictwriter_object = DictWriter(f_object, fieldnames=field_names)
            #     dictwriter_object.writerow(relations_dict)
            #     f_object.close()
            # i = 0

            # relations_dict = {}
            # gc.collect()

            # if ((relation.get("em1Text"), relation.get("em2Text")) in combinations):
            #     print(f"Relação encontrada: {relation.get('em1Text'), relation.get('em2Text')}")
            #     entity_0 = relation.get("em1Text")
            #     entity_1 = relation.get("em2Text")
            #     relation_found = find_relation_between_entities_spacy(sentence, (entity_0, entity_1))
            #     print(f"Relation found: {relation_found}")
            #     print(f"Relation dataset: {relation.get('label')}")
            #     relations_dict[f"row_{i}"] = [sentence, f"({entity_0, entity_1})", f"{relation_found}", f"{relation.get('label')}"]
            #     print([sentence, f"({entity_0, entity_1})", f"{relation_found}", f"{relation.get('label')}"])
            #     print(f"Salvo sentença {i}")

            # elif ((relation.get("em2Text"), relation.get("em1Text")) in combinations):
            #     print(f"Relação encontrada: {relation.get('em2Text'), relation.get('em1Text')}")
            #     entity_0 = relation.get("em2Text")
            #     entity_1 = relation.get("em1Text")
            #     relation_found = find_relation_between_entities_spacy(sentence, (entity_0, entity_1))
            #     print(f"Relation found: {relation_found}")
            #     print(f"Relation dataset: {relation.get('label')}")
            #     print([sentence, f"({entity_0, entity_1})", f"{relation_found}", f"{relation.get('label')}"])
            #     relations_dict[f"row_{i}"] = [sentence, f"({entity_0, entity_1})", f"{relation_found}", f"{relation.get('label')}"]
            #     print(f"Salvo sentença {i}")

            # else:
            #     print(f"Relação não encontrada: {relation.get('em1Text'), relation.get('em2Text')}")
            #     relations_dict[f"row_{i}"] = [sentence, f"{relation.get('em1Text'), relation.get('em2Text')}", "Relation not found", f"{relation.get('label')}"]
            #     print([sentence, f"{relation.get('em1Text'), relation.get('em2Text')}", "Relation not found", f"{relation.get('label')}"])
            #     print(f"Salvo sentença {i}")
            # i += 1
    
        # if i == 50:
            # print(relations_dict)
            # field_names = ["Frase", "Entidades", "Relação encontrada no código", "Relação encontrada no benchmark"]
            # with open('manual_test_spacy.csv', 'a') as f_object:
            #     dictwriter_object = DictWriter(f_object, fieldnames=field_names)
            #     dictwriter_object.writerow(relations_dict)
            #     f_object.close()
            # i = 0

            # relations_dict = {}

# print(relations_dict)

df = pd.DataFrame.from_dict(relations_dict, orient='index')
df.to_csv("manual_test_spacy.csv", encoding="utf-8", index=False)