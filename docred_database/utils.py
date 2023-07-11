from Levenshtein import jaro_winkler


def compare_strings(list_entities: list)-> list:
    similar_entities = []

    for ent in list_entities:
        list_ent = []
        for ent0 in list_entities:
            if jaro_winkler(ent, ent0)> 0.65 and jaro_winkler(ent, ent0) < 1:
                list_ent.append(ent0)
                print(jaro_winkler(ent, ent0))
                print(f"Same entities")
            else:
                print(jaro_winkler(ent, ent0))
                print(f"Different entities")
        ent_similar = {ent: list_ent}
        similar_entities.append(ent_similar)
    
    print(similar_entities)

    return similar_entities