tokenizer = BertTokenizer . from_pretrained ( ' bert - base - uncased ')
tokens = tokenizer . tokenize ( sentence )
tokens_ids = tokenizer . c o n v e r t _ t o k e n s _ t o _ i d s ( tokens )
segments_ids = [1] * len ( tokens )
tensor = torch . tensor ([ tokens_ids ])
tensors = torch . tensor ([ segments_ids ])
model = BertModel . from_pretrained ( ' bert - base - uncased ' ,
o u t p u t _ h i d d e n _ s t a t e s = True )
with torch . no_grad () :
    outputs = model ( tensor , tensors )
    hidden_states = outputs [2]
embeddings = torch . stack ( hidden_states , dim =0)
embeddings = torch . squeeze ( embeddings , dim =1)
embeddings = embeddings . permute (1 ,0 ,2)
token_vecs_sum = []
for token in embeddings :
sum_vec = torch . sum ( token [ -4:] , dim =0)
token_vecs_sum . append ( sum_vec )
sente_embedding = torch . mean ( torch . stack ( token_vecs_sum ) ,
dim =0)