from xml.dom.xmlbuilder import DocumentLS
import stanza

stanza.download('en') # download English model

nlp = stanza.Pipeline('en') # initialize English neural pipeline

doc = nlp("The Fluminense Federal University is a public higher education institution located mainly in Niterói.") # run annotation over a sentence

print(doc)
print("Entidades:")
print(doc.entities)
print("Dependências:")
for sentence in doc.sentences:
    print(sentence.dependencies)
    print(sentence.constituency)

# Processing multiple DocumentLSimport stanza
# nlp = stanza.Pipeline(lang="en") # Initialize the default English pipeline
# documents = ["This is a test document.", "I wrote another document for fun."] # Documents that we are going to process
# in_docs = [stanza.Document([], text=d) for d in documents] # Wrap each document with a stanza.Document object
# out_docs = nlp(in_docs) # Call the neural pipeline on this list of documents
# print(out_docs[1]) # The output is also a list of stanza.Document objects, each output corresponding to an input Document object