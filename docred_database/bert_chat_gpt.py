from transformers import BertTokenizer, BertForSequenceClassification
import torch


print(f"Load the pre-trained BERT model and tokenizer")
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

print(f"Define the two sentences to compare")
sentence1 = "The cat sat on the mat."
sentence2 = "The dog played in the park."

print(f"Tokenize the sentences and convert them to BERT input format")
input_ids = []
attention_masks = []

for sentence in [sentence1, sentence2]:
    encoded_dict = tokenizer.encode_plus(
                        sentence,
                        add_special_tokens=True,
                        max_length=64,
                        pad_to_max_length=True,
                        return_attention_mask=True,
                        return_tensors='pt'
                   )
    
    input_ids.append(encoded_dict['input_ids'])
    attention_masks.append(encoded_dict['attention_mask'])

print(f"Compare the two sentences using the pre-trained BERT model")
with torch.no_grad():
    inputs = {
        'input_ids': torch.stack(input_ids),
        'attention_mask': torch.stack(attention_masks)
    }
    outputs = model(**inputs)
    logits = outputs.logits
    softmax_logits = torch.softmax(logits, dim=1)
    scores = softmax_logits[:, 1]

print(f"Print the similarity score")
print("The similarity score between the two sentences is:", scores[0].item())