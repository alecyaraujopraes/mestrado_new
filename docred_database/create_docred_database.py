import json
import pandas as pd

file = "DocRED/train_annotated.json"
rel_file = "DocRED/rel_info.json"

list_obj = []

def try_find(vertex_set:list, idx: int, list_sent: list):
    entities = vertex_set[idx]
    if len(entities)==1:
        entity = entities[0].get("name")
        return entity
    else:
        for ent in entities:
            sent_id = ent.get("sent_id")
            pos_0 = ent.get("pos")[0]
            pos_1 = ent.get("pos")[1]
            ent_name_list = list_sent[sent_id][pos_0:pos_1]
            ent_name = " ".join(ent_name_list)
            if ent.get("name") in ent_name:
                entity = ent.get("name")
                return entity

def find_entities(vertex_set:list, idx: int, list_sent: list)-> str:
    entity = try_find(vertex_set, idx, list_sent)
    entities = vertex_set[idx]

    if entity == None:
        entity = []
        for ent in entities:
            entity.append(ent.get("name"))

    return entity


with open(file, "r") as f:
    list_db = f.readlines()
    l = json.loads(list_db[0])
    for item in l:
        print(f"Item: {item}")

        sentences = item.get("sents")
        sentence = ""
        for list_sentence in sentences:
            sentence_str = " ".join(list_sentence)
            sentence = sentence + sentence_str

        for label in item.get("labels"):
            relation_id = label.get("r")
            with open(rel_file, "r") as r:
                rels = r.readlines()
                r = json.loads(rels[0])
            relation = r.get(f"{relation_id}")
            print(f"Relation: {relation}")

            list_sentences_about = []
            sentence_about = ""
            for sentence_ids in label["evidence"]:
                list_sentences_about.append(item.get("sents")[sentence_ids])
                sa = " ".join(item.get("sents")[sentence_ids])
                sentence_about = sentence_about + sa
            print(f"Sentence evidence: {label['evidence']}")
            print(f"Sentence about: {sentence_about}")

            sentence_id = label["evidence"]

            idx_entity_0 = int(f"{label.get('h')}")
            idx_entity_1 = int(f"{label.get('t')}")
            print(f"Idx entities: {idx_entity_0, idx_entity_1}")

            entity_0 = find_entities(item.get("vertexSet"), idx_entity_0, sentences)
            entity_1 = find_entities(item.get("vertexSet"), idx_entity_1, sentences)

            print(f"Entity 0: {entity_0}")
            print(f"Entity 1: {entity_1}")

            dict_s = {
                "sentences": sentence,
                "sentences_evidence": sentence_about,
                "entity_0": entity_0,
                "entity_1": entity_1,
                "relation": relation
            }

            if dict_s not in list_obj:
                list_obj.append(dict_s)

df = pd.DataFrame(list_obj)
df.to_csv("docred.csv")
