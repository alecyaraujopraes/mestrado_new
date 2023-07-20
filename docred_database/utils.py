from Levenshtein import jaro_winkler


def compare_strings(ent_o, ent_h)-> bool:

    if jaro_winkler(ent_o, ent_h)> 0.7 and jaro_winkler(ent_o, ent_h) != 1:
        similar_ent = 1
        print(f"Similar entities")
    else:
        similar_ent = 0
        print(f"Different entities")

    return similar_ent


def get_the_most_similar_pair_entities(df_selected, entity_0, entity_1):
    pairs_and_similarities = {}

    for entity_tail, entity_head, relation_annotated, code_relation in zip(df_selected.entity_tail, df_selected.entity_head, df_selected.relation, df_selected.code_relation):
        tail_jw = jaro_winkler(entity_tail, entity_0)
        head_jw = jaro_winkler(entity_head, entity_1)
        avg_jw = (tail_jw + head_jw)/2
        pairs_and_similarities[f"{entity_tail}+{entity_head}+{relation_annotated}+{code_relation}"] = avg_jw

    max_jw_pair = max(pairs_and_similarities, key=pairs_and_similarities.get)
    pair_ents = max_jw_pair.split("+")
    tuple_of_ents = (pair_ents[0], pair_ents[1])
    max_jw_value = max(pairs_and_similarities.values())
    relation = pair_ents[2]
    code_relation = pair_ents[3]

    return tuple_of_ents, max_jw_value, relation, code_relation