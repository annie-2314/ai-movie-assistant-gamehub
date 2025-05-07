import requests
import os
from dotenv import load_dotenv

# Load environment variables (including your API keys)
load_dotenv()

# Groq API Key
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def recommend_movies_from_groq(movie_name):
    """ Use Groq API to get movie recommendations based on the input movie name """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Prepare the data for Groq's model to handle
    data = {
        "model": "llama-3.3-70b-versatile",  # Make sure this model is correct
        "messages": [
            {"role": "user", "content": f"Recommend movies similar to {movie_name}."}
        ]
    }

    groq_endpoint = "https://api.groq.com/openai/v1/chat/completions"

    try:
        response = requests.post(groq_endpoint, json=data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            recommendations = response_data.get("choices")[0].get("message").get("content")
            return recommendations
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"

