import csv

import pandas as pd
from Levenshtein import jaro_winkler

df_docred = pd.read_csv("docred_database/docred.csv")
df_spacy = pd.read_csv("docred_database/manual_test_spacy.csv")

for sent in df_docred["sentences"]:
    sent_modify = sent.replace("'", "\\'")
    sent_modify = sent_modify.replace('"', '\\"')
    df_docred_selected = df_docred.loc[df_docred.sentences == sent, :]
    df_spacy_selected = df_spacy.loc[df_spacy.Frase == sent_modify, :]

    for entity_tail, entity_head, relation in zip(df_docred_selected.entity_tail, df_docred_selected.entity_head, df_docred_selected.relation):
        for Entidade_0, Entidade_1, Relacao_encontrada in zip(df_spacy_selected.Entidade_0, df_spacy_selected.Entidade_1, df_spacy_selected.Relacao_encontrada):
            if (jaro_winkler(entity_tail, Entidade_0)> 0.7 or jaro_winkler(entity_tail, Entidade_1)>0.7) and (jaro_winkler(entity_head, Entidade_0)> 0.7 or jaro_winkler(entity_head, Entidade_1)>0.7):
                print(f"Frase: {sent}")
                print(f"Entidades: {entity_tail, entity_head, Entidade_0, Entidade_1, relation, Relacao_encontrada}")
            else:
                print(f"No entities")
                # field_names = ["Frase", "Entidade_0", "Entidade_1", "Relacao_anotada", "Relacao_encontrada"]
                # with open('docred_database/measure_relations.csv', 'a') as f_object:
                #     dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
                #     writer = csv.DictWriter(f_object, fieldnames=field_names)
                #     writer.writerow({'Frase': sent, 'Entidade_0': entity_0, 'Entidade_1': entity_1, 'Relacao_anotada': relation, 'Relacao_encontrada': Relacao_encontrada})

                #     f_object.close()
                # print("Saved relations in csv")
