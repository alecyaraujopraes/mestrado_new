from Levenshtein import jaro_winkler


def compare_strings(ent_o, ent_h)-> bool:

    if jaro_winkler(ent_o, ent_h)> 0.7 and jaro_winkler(ent_o, ent_h) != 1:
        similar_ent = 1
        print(f"Similar entities")
    else:
        similar_ent = 0
        print(f"Different entities")

    return similar_ent


def get_the_most_similar_string_in_list(strings: str, entity: str)-> str:
    string_0 = strings.replace("[", "")
    string_1 = string_0.replace("]", "")
    string_2 = string_1.replace("'", "")
    list_of_strings = string_2.split(",")
    max_jw = 0
    the_most_similar_str = ""
    for ent in list_of_strings:
        jw = jaro_winkler(entity, ent)
        if jw > max_jw:
            the_most_similar_str = ent
            max_jw = jw

    return the_most_similar_str


def get_the_most_similar_pair_entities_and_relation(df_selected, entity_0, entity_1):
    pairs_and_similarities = {}
    for list_entity_tail, list_entity_head, relation_annotated, code_relation in zip(df_selected.entity_tail, df_selected.entity_head, df_selected.relation, df_selected.code_relation):
        entity_tail = get_the_most_similar_string_in_list(list_entity_tail, entity_0)
        entity_head = get_the_most_similar_string_in_list(list_entity_head, entity_1)
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