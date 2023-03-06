import json

files = ["test.json"]

list_obj = []


for file in files:
    with open(file, "r") as f:
        for line in f.readlines():
            obj = json.loads(line)
            list_obj.append(obj)

for item in list_obj:
    sentence = item["sentText"].replace(". ''", ". ")
    # sentence = sentence.replace("'", "\'")
    for relation in item["relationMentions"]:
        entity0 = relation["em1Text"]
        entity1 = relation["em2Text"]
        str_line = f"""python3 SpacyParse2.py -s "{sentence}" -e0 "{entity0}" -e1 "{entity1}" """

        with open("run_spacy.sh", "a") as my_file:
            my_file.write(str_line)
            my_file.write("\n")
