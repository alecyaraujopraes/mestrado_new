import csv
import pandas as pd

file = "docred_database/docred.csv"

docred = pd.read_csv("docred_database/docred.csv")

list_obj = []

with open(file, "r") as f:
    for line in csv.DictReader(f):
        list_obj.append(line)


for item in list_obj:
    sentence = item.get("sentences").replace("'", "\\'")
    sentence = sentence.replace('"', '\\"')
    entity_tail = item.get("entity_tail")
    entity_head = item.get("entity_head")
    relation = item.get("relation")
    code_relation = item.get("code_relation")


    str_line = f"""python3 docred_database/SpacyParse.py -s "{sentence}" -et "{entity_tail}" -eh "{entity_head}" -r "{relation}" -cr "{code_relation}" """

    with open("docred_database/run_spacy.sh", "a") as my_file:
        my_file.write(str_line)
        my_file.write("\n")
