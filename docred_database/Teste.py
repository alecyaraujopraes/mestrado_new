# '''
# Created on Sep 6, 2022

# @author: lapaesleme
# '''

# seq = [ 1, 2, 6, 9, 3, 23, 45, 17, 5]

# if  seq:
#     print('List is empty')
# else:
#     print('List is not empty')

# from itertools import chain
# import sys

# print(sys.getrecursionlimit())

# print ([n for n in seq if n < 10])

# print ('abc' + 'def ' + ', '.join([str(n) for n in seq if n < 10]))
# print (len(seq))

# seq = [1, [3, 4], [5, 6]]
# print (seq[0])
# print (seq[1])

# for c in seq[1:]:
#     print (c)
    
# seq = []
# seq.append(0)
# seq.append([1, 2])
# seq.append([3, 4])
# print(seq)


# class MyClass:
#     nome = None

#     def __init__(self, nome):
#         self.nome = nome
    
    
# o1 = MyClass('Luiz')
# o2 = MyClass('Andre')

# print (o1 == o1)

# print (o1.nome)
# print (o2.nome)

# print (list(set([o1, o2]) - set([o1])))
# print ('DT The'.split(' '))

# print([MyClass(c) for c in []])

# print (max([1, 2, 3, 4]))

# print ([1, 2] + [3, 4])

# list_of_lists = [[1, 2, 3], [4, 5, 6], [7, 8, [9, 10, 11]]]

# flat_list = list(chain(*list_of_lists))

# print(flat_list)
# [[], []]

# print ([ c2 for c in [[], []] for c2 in c])

# print ('abd\tefg')

# print([1, 2, 3, 4, 5])

# str = "Ohio Coach Frank Solich said : \"keke\" This would not have made our season i"
# print(str)
# .replace("'", "\'"))

# from sentence_transformers import SentenceTransformer, util
# model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

# query_embedding = model.encode('How big is London')
# passage_embedding = model.encode('London is known for its finacial district')

# print("Similarity:", util.dot_score(query_embedding, passage_embedding), util.cos_sim(query_embedding, passage_embedding))

# for i in util.dot_score(query_embedding, passage_embedding):
#     print(i)
#     for index, im in enumerate(i):
#         print(index, im.item())


from bert_utils import selection_by_bert

entity_0 = "Mário Cravo Neto"
entity_1 = "Mário Cravo Júnior"
relation_annotated = "father"
relation_found = "son"

sent = "Mário Cravo Neto son Mário Cravo Júnior"

i, x = selection_by_bert(entity_0, entity_1, sent)

print(i, x)