from functions_bert import sentence_transformer, bert_resume
from transformers import logging

logging.set_verbosity_error()

relations = {
    "P1": "cause",
    "P2": "treatment",
    "P3": "symptons",
    "P4": "complication",
    "P5": "prevention",
    "P6": "risk factor",
}

possible_relations = {
    "direct": {
        "P1": ["is caused by"],
        "P2": ["is the treatment of", "to treat", "is prescribed"], 
        "P3": ["cause symptons of"], 
        "P4": ["can have complications"], 
        "P5": ["is prevented by"], 
        "P6": ["has as risk factor"], 
    }, 
    "inverse": {
        "P1": ["causes"],
        "P2": ["is treated by"], 
        "P3": ["is a symptom of"], 
        "P4": ["is a complication of"],
        "P5": ["prevents", "is the prevention of"],
        "P6": ["is a risk factor of"],
    }
}


def selection_by_bert_resume(paragraph: str, path: str, entity_0: str, entity_1: str):

    created_relations = []
    for k,v in possible_relations.items():
        for relation_id, list_relation in v.items():
            for relation in list_relation:
                created_relation = entity_0 + " " + relation + " " + entity_1
                cos_diff = bert_resume(paragraph, path, created_relation)
                created_relations.append({"relation_id": relation_id, "created_relation": created_relation, "similarity": cos_diff, "k": k})

    max_tensor = 0
    id = 0
    relation = ""
    for item in created_relations:
        if item.get("similarity") > max_tensor:
            id = item.get("relation_id")
            relation = item.get("created_relation")
            max_tensor = item.get("similarity")
            way = item.get("k")

    rel = relations.get(id)

    print(f"Relation found by bert resume: id {id, rel}, relation {relation}, similarity {max_tensor}, way {k}")

    return id, relation, k, rel


def selection_by_bert_sc(entity_0: str, entity_1: str, sent: str):

    created_relations = []
    for k,v in possible_relations.items():
        for relation_id, list_relation in v.items():
            for relation in list_relation:
                created_relation = f"{entity_0} {relation} {entity_1}"
                sentence_transformer_c = sentence_transformer(sent, created_relation)
                created_relations.append({"relation_id": relation_id, "created_relation": created_relation, "similarity": sentence_transformer_c[0].item(), "k": k})

    max_tensor = 0
    id = 0
    relation = ""
    for item in created_relations:
        if item.get("similarity") > max_tensor:
            id = item.get("relation_id")
            relation = item.get("created_relation")
            max_tensor = item.get("similarity")
            way = item.get("k")

    rel = relations.get(id)

    print(f"Relation found by bert: id {id, rel}, relation {relation}, similarity {max_tensor}, way {k}")

    return id, relation, k, rel