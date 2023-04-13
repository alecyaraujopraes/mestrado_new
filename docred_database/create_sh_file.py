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

    str_line = f"""python3 docred_database/SpacyParse.py -s "{sentence}" """

    with open("docred_database/run_spacy.sh", "a") as my_file:
        my_file.write(str_line)
        my_file.write("\n")
