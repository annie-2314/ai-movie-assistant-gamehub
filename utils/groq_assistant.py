import openai
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

groq_endpoint = "https://api.groq.com/openai/v1/chat/completions"

def ask_groq(question):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}",
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": question}]
    }

    try:
        response = requests.post(groq_endpoint, json=data, headers=headers)
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get("choices")[0].get("message").get("content")
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
