import json
import pandas as pd

file = "DocRED/train_annotated.json"
rel_file = "DocRED/rel_info.json"

list_obj = []

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

        print(f"Sentences: {sentence}")
        entity_0 = ""
        entity_1 = ""

        for label in item.get("labels"):
            relation_id = label.get("r")
            with open(rel_file, "r") as r:
                rels = r.readlines()
                r = json.loads(rels[0])
            relation = r.get(f"{relation_id}")
            print(f"Relation: {relation}")

            sentence_about = ""
            for sentence_id in label["evidence"]:
                print(f"Sentence id: {sentence_id}")

                list_sentences_about = item.get("sents")[sentence_id]
                print(f"List sentences about: {list_sentences_about}")
                sentences_about = " ".join(list_sentences_about)
                sentence_about = sentence_about + sentences_about
                print(f"Sentence about: {sentences_about}")
                idx_entity_0 = int(f"{label.get('h')}")
                idx_entity_1 = int(f"{label.get('t')}")
                print(f"IDX entities: {idx_entity_0, idx_entity_1}")

                for i in item.get("vertexSet"):
                    for entity in i:
                        pos = entity.get("pos")
                        entity_name = " ".join(list_sentences_about[pos[0]:pos[1]])
                                                
                        if entity.get("sent_id") == sentence_id and entity.get("name") in sentences_about and entity.get("name") in entity_name:
                            print(entity_name)

                

                # if entity_0 and entity_1:
                #     dict_relations = {
                #         "sentences": sentence,
                #         "sentence": sentence_about,
                #         "entity_0": entity_0,
                #         "entity_1": entity_1,
                #         "relation": relation,
                #     }
                #     print(f"Dict: {dict_relations}")
                #     entity_0 = ""
                #     entity_1 = ""
                #     continue

                # list_obj.append(dict_relations)
            break
        break

# str_obj = "".join([str(item) for item in list_obj])
# print(type(str_obj))
# df = pd.DataFrame(list_obj)
# df.to_csv("docrem.csv")