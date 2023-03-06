from stanfordcorenlp import StanfordCoreNLP
# from opencc import OpenCC

# Preset
nlp = StanfordCoreNLP('stanford-corenlp-4.4.0-models-english-kbp/', memory='8g')
# cc = OpenCC('t2s')

# The sentence you want to parse
sentence = 'I eat a big and red apple.'

# POS
print('POS：', nlp.pos_tag(sentence))

# Tokenize
print('Tokenize：', nlp.word_tokenize(sentence))

# NER
print('NER：', nlp.ner(sentence))

# Parser
print('Parser：')
print(nlp.parse(sentence))
print(nlp.dependency_parse(sentence))

# Close Stanford Parser
nlp.close()