import json

files = ["test.json", "train.json", "valid.json"]

list_obj = []

for file in files:
    with open(file, "r") as f:
        for line in f.readlines():
            obj = json.loads(line)
            list_obj.append(obj)

list_relations = []

for item in list_obj:
    for relation in item.get("relationMentions"):
        label = f"\n{relation.get('label')}"
        if label not in list_relations:
            list_relations.append(label)

with open("acervo_de_relacoes.txt", "w") as f:
    f.writelines(list_relations)
