import pinecone
from transformers import AutoTokenizer, AutoModel
import torch
import os
from dotenv import load_dotenv

# Load environment variables (if using .env file)
load_dotenv()
api_key = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone with your API key
pinecone.init(api_key=api_key, environment="us-east-1")  # Use your Pinecone environment if different
index_name = "fraud-data"  # The name of the index you've created

# Connect to the Pinecone index
index = pinecone.Index(index_name)

# Load the tokenizer and model
model_name = "huggingface/llama-2-7b"  # Replace with your model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embedding

# Query function to get similar text based on embedding
def query_pinecone(new_text, top_k=3):
    new_embedding = get_embedding(new_text)  # Get embedding for the new text
    results = index.query(queries=[new_embedding], top_k=top_k, include_metadata=True)
    return results

# Test the query function
new_text = "Urgent: Your account is at risk."
results = query_pinecone(new_text)

# Print the results
for match in results['matches']:
    print(f"Match ID: {match['id']}, Score: {match['score']}, Fraudulent: {match['metadata']['Fraudulent']}")
