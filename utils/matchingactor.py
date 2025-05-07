import requests
from utils.groq_assistant import GROQ_API_KEY


def match_actor_to_movie_from_groq(actor_name):
    """Fetch movie titles associated with a given actor using Groq."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": f"Which movie starred {actor_name}?"}
        ]
    }

    groq_endpoint = "https://api.groq.com/openai/v1/chat/completions"

    try:
        response = requests.post(groq_endpoint, json=data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            movie_list = response_data.get("choices")[0].get("message").get("content")
            return movie_list
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"
