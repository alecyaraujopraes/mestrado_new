import csv
import pandas as pd

file = "docred_database/docred.csv"

docred = pd.read_csv("docred_database/docred.csv", delimiter="|")

sentences_used = []
for index, row in docred.iterrows():
    sentence_0 = row["sentences"]
    if sentence_0 not in sentences_used:
        sentence = sentence_0.replace('"', '\\"')

        str_line = f"""python3 docred_database/SpacyParse.py -s "{sentence}" """

        with open("docred_database/run_spacy.sh", "a") as my_file:
            my_file.write(str_line)
            my_file.write("\n")
        
        sentences_used.append(sentence_0)
