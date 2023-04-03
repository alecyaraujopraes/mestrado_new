from Levenshtein import distance, jaro_winkler
import spacy

sentence = "Zest Airways , Inc. operated as AirAsia Zest ( formerly Asian Spirit and Zest Air ) , was a low - cost airline based at the Ninoy Aquino International Airport in Pasay City , Metro Manila in the Philippines ."
# str1 = "Zest Air"
# str2 = "Asian Spirit and Zest Air"

# print(distance(str1, str2))
# print(max(len(str1), len(str2)))
# print(1-(distance(str1, str2)/(max(len(str1), len(str2)))))


# print("jaro_winkler")
# print(jaro_winkler(str1, str2))
nlp = spacy.load("en_core_web_sm")

doc = nlp(sentence)

# Analyze syntax
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text)