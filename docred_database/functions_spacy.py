import spacy

nlp = spacy.load("en_core_web_sm")

def split_text_into_sentences(text: str)->list:
    doc = nlp(text)

    return doc.sents