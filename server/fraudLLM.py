from google import generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

# Configure the API key
api_key = os.getenv("API_KEY")
if api_key is None:
    raise ValueError("API_KEY is not set in the environment variables.")

genai.configure(api_key=api_key)

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def fraud_detection(message):
    #data = request
    user_input = message

    if not user_input:
        return "No message provided", 400
    
    user_input+= ". Determine if the message above is Fraudulent or not? Format your response as either NOT FRAUDULENT or FRADULENT: x%% fradulent. If the message is not related to financial information, please return: Please enter correct input"
    # Send a message and get the response
    response = model.generate_content(user_input)
    print(response.text)

    # Return the response text as JSON
    return response.text
