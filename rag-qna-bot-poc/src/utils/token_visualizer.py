from transformers import AutoTokenizer
tokenizer=AutoTokenizer.from_pretrained('openai/gpt-oss-20b')
def visualize_tokens(text):
 ids=tokenizer.encode(text)
 return {'count':len(ids),'token_ids':ids,'tokens':[tokenizer.decode([i]) for i in ids]}
