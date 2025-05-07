import requests
import os
from dotenv import load_dotenv

# Load environment variables (including your API keys)
load_dotenv()

# Groq API Key
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def fetch_movie_poster_from_groq(movie_name):
    """Fetch movie poster using Groq API."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",  # Make sure this model fits your needs
        "messages": [
            {"role": "user", "content": f"Find the poster for the movie titled '{movie_name}'."}
        ]
    }

    groq_endpoint = "https://api.groq.com/openai/v1/chat/completions"

    try:
        response = requests.post(groq_endpoint, json=data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            poster_url = response_data.get("choices")[0].get("message").get("content")
            return poster_url
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"
