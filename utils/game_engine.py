from utils.groq_assistant import ask_groq

# Function to get a random movie title for the puzzle game (from Groq)
def get_puzzle_movie_title():
    prompt = "Give me a random popular movie title for a puzzle game."
    movie_title = ask_groq(prompt)  # Make Groq API call here
    return movie_title.strip() if movie_title else "Inception"  # Fallback if Groq response is empty

# Function to get a movie title for the blurred poster game (from Groq)
def get_blur_movie_title():
    prompt = "Give me a random popular movie title for a blur guessing game."
    movie_title = ask_groq(prompt)  # Make Groq API call here
    return movie_title.strip() if movie_title else "The Matrix"  # Fallback if Groq response is empty

# Function to get actor and movie question (from Groq)
def get_actor_movie_question():
    prompt = "Give me an actor and one correct movie they starred in, along with 3 fake ones. Format as JSON: {\"actor\":\"...\", \"correct\":\"...\", \"options\":[\"...\"]}"
    response = ask_groq(prompt)  # Make Groq API call here
    try:
        data = eval(response)  # Or json.loads(response) if the response is JSON
        return data
    except Exception as e:
        return {"actor": "Unknown", "correct": "Unknown", "options": []}

# Function to get a random movie quote (from Groq)
def get_movie_quote():
    prompt = "Give me a famous movie quote and the movie it's from. Format: 'quote - movie'"
    quote = ask_groq(prompt)  # Make Groq API call here
    return quote.strip() if quote else "Here's looking at you, kid. - Casablanca"  # Fallback if Groq response is empty

# Function to generate a movie emoji riddle (from Groq)
def get_emoji_riddle():
    prompt = "Give me an emoji riddle representing a popular movie and the answer. Format: 'emojis - movie'"
    riddle = ask_groq(prompt)  # Make Groq API call here
    return riddle.strip() if riddle else "👨‍🚀👽🌌 - Interstellar"  # Fallback if Groq response is empty
from utils.groq_assistant import ask_groq
import random

# Function to get a random movie trivia question from Groq
def get_random_question():
    # Ask Groq for a random trivia question
    prompt = "Give me a random movie trivia question along with four answer options and the correct answer. Format as JSON: {\"question\":\"...\", \"options\":[\"...\", \"...\", \"...\", \"...\"], \"answer\":\"...\"}"
    
    response = ask_groq(prompt)  # Get the response from Groq
    try:
        data = eval(response)  # If Groq returns JSON-like format as string, use eval() to parse it
        question = data['question']
        options = data['options']
        answer = data['answer']
        
        # Randomize options for variety
        random.shuffle(options)
        
        return question, options, answer
    except Exception as e:
        print(f"Error while getting trivia question: {e}")
        return "Error fetching trivia question.", ["Option 1", "Option 2", "Option 3", "Option 4"], "Option 1"
