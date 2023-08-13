import csv

import pandas as pd
from bert_utils import selection_by_bert, selection_by_bert_location
from utils import get_the_most_similar_pair_entities

#  manual_test_spacy.csv Frase,Entidade_0,Entidade_1,Relacao_encontrada
#  docred.csv ,sentences,sentences_evidence,entity_tail,entity_head,relation,code_relation

df_test_spacy = pd.read_csv("docred_database/manual_test_spacy.csv")
df_docred = pd.read_csv("docred_database/docred.csv")
df = df_docred.reset_index() # make sure indexes pair with number of rows

# sentences_used = []
for index, row in df_test_spacy.iterrows():
    sentences_used = []
    phrase = row["Frase"]
    if phrase not in sentences_used:
        sent = phrase.replace("\\", "")
        ent_0 = row["Entidade_0"]
        ent_1 = row["Entidade_1"]
        relation_found_by_path = row["Relacao_encontrada"]
        print(f"Frase, ent 0, ent 1, relação encontrada: {sent, ent_0, ent_1, relation_found_by_path}")

        relation_id_found_by_bert, relation_found_by_bert, way = selection_by_bert_location(ent_0, ent_1, relation_found_by_path)
        print(f"Relation found by bert: {relation_found_by_bert, relation_id_found_by_bert}")

        df_docred_selected = df.loc[df.sentences == sent]

        if ent_0 == "Australia":
            ent_0 = "country Australia"
            print(f"Change entity ent_0 to {ent_0}")

        if ent_1 == "Australia":
            ent_1 == "country Australia"
            print(f"Change entity ent_0 to {ent_0}")

        if way == "inverse":
            tuple_ents_inverse, jw_factor, annotated_relation, annotated_code_relation = get_the_most_similar_pair_entities(df_docred_selected, ent_1, ent_0)
            tuple_ents = (tuple_ents_inverse[1], tuple_ents_inverse[0])

        else:
            tuple_ents, jw_factor, annotated_relation, annotated_code_relation = get_the_most_similar_pair_entities(df_docred_selected, ent_0, ent_1)
        
        print(f"Tuple ents, jw factor, annotated relation and annotated code relation: {tuple_ents, jw_factor, annotated_relation, annotated_code_relation}")


        if annotated_code_relation == relation_id_found_by_bert:
            print(f"Codes: {annotated_code_relation}, {relation_id_found_by_bert}")
            result = 1

        else:
            result = 0


        field_names = [
            "sentences", 
            "entity_0", 
            "entity_1",
            "tuple_most_similar",
            "relation_found_by_path",
            "relation_found_by_bert",
            "relation_annotated",
            "result",
        ]

        with open('docred_database/check_bert_and_annotations.csv', 'a') as f_object:
            dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names, delimiter=';')
            writer = csv.DictWriter(f_object, fieldnames=field_names, delimiter=';')
            writer.writerow({
                "sentences": phrase, 
                "entity_0": ent_0, 
                "entity_1": ent_1,
                "tuple_most_similar": tuple_ents,
                "relation_found_by_path": relation_found_by_path,
                "relation_found_by_bert": relation_found_by_bert,
                "relation_annotated": annotated_relation,
                "result": result,
            })

            f_object.close()

        sentences_used.append(phrase)
