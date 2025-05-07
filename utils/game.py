import os
import json
from PIL import Image, ImageFilter, ImageEnhance
import requests
from utils.groq_assistant import ask_groq
from utils.config import TMDB_API_KEY

def get_puzzle_movie_title():
    movie_title = ask_groq("Give me a popular movie title for a puzzle guessing game.")
    print(f"Movie Title for Puzzle: {movie_title}")  # Debugging line
    return movie_title

def get_blur_movie_title():
    movie_title = ask_groq("Give me a famous movie title for a blur guessing game.")
    print(f"Movie Title for Blur: {movie_title}")  # Debugging line
    return movie_title

def get_actor_movie_question():
    prompt = (
        "Give me an actor and one correct movie they starred in, "
        "along with 3 fake ones. Format as JSON: "
        "{\"actor\":\"...\", \"correct\":\"...\", \"options\":[\"...\", \"...\", \"...\", \"...\"]}"
    )
    response = ask_groq(prompt)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        print("Error parsing actor movie question")
        return None

def get_movie_quote():
    prompt = "Give me a famous movie quote and the movie it's from. Format: {\"quote\": \"...\", \"movie\": \"...\"}"
    response = ask_groq(prompt)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        print("Error parsing movie quote")
        return None

def get_emoji_riddle():
    prompt = "Give me an emoji riddle for a famous movie. Format: {\"emojis\": \"...\", \"movie\": \"...\"}"
    response = ask_groq(prompt)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        print("Error parsing emoji riddle")
        return None

def fetch_movie_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        data = response.json()
        
        if data.get("results"):
            poster_path = data["results"][0]["poster_path"]
            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            image = Image.open(requests.get(poster_url, stream=True).raw)
            return image
        else:
            print("No poster found")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return None

def get_blurred_poster(movie_title):
    poster = fetch_movie_poster(movie_title)
    if poster:
        blurred_poster = poster.filter(ImageFilter.GaussianBlur(10))
        enhancer = ImageEnhance.Color(blurred_poster)
        enhanced_poster = enhancer.enhance(1.5)  # Increase color saturation (1.0 is original)
        return enhanced_poster  # Return the enhanced/blurred poster
    return None

def get_jigsaw_piece(image):
    piece = image.crop((0, 0, 250, 250))
    enhancer = ImageEnhance.Color(piece)
    enhanced_piece = enhancer.enhance(1.5)  # Adjust the color saturation as needed
    return enhanced_piece
