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
    
    entity0 = item.get("entity_0")
    entity1 = item.get("entity_1")
    relation = item.get("relation")
    str_line = f"""python3 docred_database/SpacyParse.py -s "{sentence}" -e0 "{entity0}" -e1 "{entity1}" -r "{relation}" """

    with open("docred_database/run_spacy.sh", "a") as my_file:
        my_file.write(str_line)
        my_file.write("\n")
