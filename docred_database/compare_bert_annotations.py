import csv

import pandas as pd
from bert_utils import selection_by_bert_sc, subproperties, selection_by_bert_resume
from utils import get_the_most_similar_pair_entities_and_relation


df_test_spacy = pd.read_csv("docred_database/manual_test_spacy.csv", delimiter="|")
df_docred = pd.read_csv("docred_database/docred.csv", delimiter="|")
df = df_docred.reset_index() # make sure indexes pair with number of rows


for index, row in df_test_spacy.iterrows():
    phrase = row["Frase"]
    sent = phrase.replace('\\"', '"')
    ent_0 = row["Entidade_x"]
    ent_1 = row["Entidade_1"]
    nodes = row["Nos"]
    idx_nodes = row["Indice_nos"]


    relation_found_by_path = row["Relacao_encontrada"]
    print(f"Frase, ent 0, ent 1, relação encontrada: {sent, ent_0, ent_1, relation_found_by_path}")

    relation_id_found_by_bert, relation_modified_found_by_bert, way, relation_found_by_bert  = selection_by_bert_sc(ent_0, ent_1, relation_found_by_path)
    print(f"Relation found by bert sentence transformer: {relation_found_by_bert, relation_id_found_by_bert}")

    df_docred_selected = df.loc[df.sentences == sent]

    if way == "inverse":
        tuple_ents_inverse, jw_factor, annotated_relation, annotated_code_relation = get_the_most_similar_pair_entities_and_relation(df_docred_selected, ent_1, ent_0)
        tuple_ents = (tuple_ents_inverse[1], tuple_ents_inverse[0])

    else:
        tuple_ents, jw_factor, annotated_relation, annotated_code_relation = get_the_most_similar_pair_entities_and_relation(df_docred_selected, ent_0, ent_1)
    
    print(f"Tuple ents, jw factor, annotated relation and annotated code relation: {tuple_ents, jw_factor, annotated_relation, annotated_code_relation}")

    list_sub_st = subproperties(relation_id_found_by_bert)

    # relation_id_found_by_bert_r, relation_modified_found_by_bert_r, way_r, relation_found_by_bert_r = selection_by_bert_resume(sent, relation_found_by_path, ent_0, ent_1)
    # print(f"Relation found by bert resume: {relation_found_by_bert_r, relation_id_found_by_bert_r}")

    # list_sub_r = subproperties(relation_id_found_by_bert_r)

    if annotated_code_relation == relation_id_found_by_bert or annotated_code_relation in list_sub_st:
        print(f"Annotated code relation, relation id found by bert sentence transformer, list subproperties: {annotated_code_relation, relation_id_found_by_bert, list_sub_st}")
        result_st = 1

    else:
        result_st = 0

    # if annotated_code_relation == relation_id_found_by_bert_r or annotated_code_relation in list_sub_r:
    #     print(f"Annotated code relation, relation id found by bert resume, list subproperties: {annotated_code_relation, relation_id_found_by_bert_r, list_sub_r}")
    #     result_r = 1

    # else:
    #     result_r = 0


    field_names = [
        "sentences", 
        "entities", 
        "nodes",
        "idx_nodes",
        "tuple_most_similar",
        "path",
        "relation_modified_found_by_bert",
        "relation_id_found_by_bert",
        "relation_found_by_bert",
        "relation_id_annotated",
        "result_st",
        # "result_r",
    ]

    with open('docred_database/check_bert_and_annotations.csv', 'a') as f_object:
        dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names, delimiter='|')
        writer = csv.DictWriter(f_object, fieldnames=field_names, delimiter='|')
        writer.writerow({
            "sentences": phrase, 
            "entities": (ent_0, ent_1), 
            "nodes": nodes,
            "idx_nodes":idx_nodes,
            "tuple_most_similar": tuple_ents,
            "path": relation_found_by_path,
            "relation_modified_found_by_bert": relation_modified_found_by_bert,
            "relation_id_found_by_bert": relation_id_found_by_bert,
            "relation_found_by_bert": relation_found_by_bert,
            "relation_id_annotated": annotated_relation,
            "result_st": result_st,
            # "result_r": result_r,
        })

        f_object.close()