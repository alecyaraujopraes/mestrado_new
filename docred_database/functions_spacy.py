import spacy

nlp = spacy.load("en_core_web_sm")

def split_text_into_sentences(text: str)->list:
    doc = nlp(text)

    list_sentences = []

    for sent in doc.sents:
        list_sentences.append(sent.text)

    return list_sentences