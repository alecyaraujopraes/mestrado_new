import pandas as pd

df_docred = pd.read_csv("docred_database/docred.csv")
df_spacy = pd.read_csv("docred_database/manual_test_spacy.csv")

for sent in df_docred["sentences"]:
    sent_modify = sent.replace("'", "\\'")
    sent_modify = sent_modify.replace('"', '\\"')
    print(f"Frase: {sent}")
    df_docred_selected = df_docred.loc[df_docred.sentences == sent, :]
    df_spacy_selected = df_spacy.loc[df_spacy.Frase == sent_modify, :]

    for line in df_docred_selected["entity_0"]:
        print(line)

    print(df_docred_selected)
    print(df_spacy_selected)
    break