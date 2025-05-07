import base64
import streamlit as st
import requests
from PIL import Image, ImageFilter
import random
import os
from utils.config import TMDB_API_KEY, GROQ_API_KEY
from dotenv import load_dotenv
from utils.groq_assistant import ask_groq
from utils.voice_input import transcribe_voice
from utils.recommend import recommend_movies_from_groq
from utils.game_engine import get_random_question
from utils.game import fetch_movie_poster, get_blurred_poster, get_jigsaw_piece


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

st.set_page_config(page_title="🎮 Movie Game Hub", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("bg.png");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
h1, h2, h3 {
    color: white;
}
.white-text {
    color: white;
}
/* Override default Streamlit colors */
.starkdown, .sttext, .stsuccess, .sterror, .stwarning {
    color: white !important;
}

/* Target Groq results specifically */
.stGroqResult {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ---------- Game Logic ----------
def fetch_movie_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
    response = requests.get(url).json()
    if response.get("results"):
        poster_path = response["results"][0]["poster_path"]
        poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        image = Image.open(requests.get(poster_url, stream=True).raw)
        return image
    return None

def get_blurred_poster(movie_title):
    poster = fetch_movie_poster(movie_title)
    return poster.filter(ImageFilter.GaussianBlur(10)) if poster else None

def get_jigsaw_piece(image):
    return image.crop((0, 0, 250, 250))

# ---------- Tabs ----------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎞 Recommend", "🧠 Movie Quiz", "🎙 Voice", "🤖 Assistant", "🎮 Game Hub"
])

# ---------- Game Hub ----------
with tab5:
    st.header("🎮 Welcome to the Ultimate Movie Game Hub")
    game = st.selectbox("Choose a Game", [
        "🧩 Jigsaw Puzzle: Guess the Movie",
        "🕵️ Blurred Poster: Guess the Movie",
        "🎭 Match the Actor to the Movie",
        "🧠 Guess the Dialog Line",
        "🎬 Movie Emoji Riddle"
    ])

    # --- Game 1: Jigsaw Puzzle ---
    if game == "🧩 Jigsaw Puzzle: Guess the Movie":
        st.subheader("🧩 Guess the Movie from a Puzzle Piece")
        prompt = "Give me a popular movie title for a puzzle game."
        movie_title = ask_groq(prompt)
        poster = fetch_movie_poster(movie_title)
        if poster:
            piece = get_jigsaw_piece(poster)
            st.image(piece, caption="Guess the movie from this piece")
            guess = st.text_input("Your guess:")
            if st.button("Submit Guess"):
                if guess.strip().lower() in movie_title.lower():
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Nope! It was: {movie_title}")
        else:
            st.warning("Could not fetch the poster. Try again later.")

    # --- Game 2: Blurred Poster Guess ---
    elif game == "🕵️ Blurred Poster: Guess the Movie":
        st.subheader("🕵️ Can you guess the movie from this blur?")
        movie_title = ask_groq("Give me a famous movie title for a blur guessing game.")
        blurred = get_blurred_poster(movie_title)
        if blurred:
            st.image(blurred, caption="Which movie is this?")
            guess = st.text_input("Your guess:")
            if st.button("Submit Guess"):
                if guess.strip().lower() in movie_title.lower():
                    st.success("🎉 Right on!")
                else:
                    st.error(f"Oops! The movie was: {movie_title}")
        else:
            st.warning("Unable to fetch blurred poster.")

    # --- Game 3: Match Actor to Movie ---
    elif game == "🎭 Match the Actor to the Movie":
        st.subheader("🎭 Which movie did this actor star in?")
        prompt = "Give me an actor and one correct movie they starred in, along with 3 fake ones. Format as JSON: {\"actor\":\"...\", \"correct\":\"...\", \"options\":[\"...\"]}"
        response = ask_groq(prompt)
        try:
            data = eval(response)  # Replace with json.loads(response) if Groq returns strict JSON
            actor = data['actor']
            correct = data['correct']
            options = data['options']
            random.shuffle(options)
            st.write(f"Which movie did **{actor}** star in?")
            selected = st.radio("Choose the correct movie:", options, key=f"actor_movie_{actor}")  # Add unique key
            if st.button("Submit Answer", key=f"submit_actor_movie_{actor}"):  # Add unique key
                if selected == correct:
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Nope. The right answer is: {correct}")
        except:
            st.error("Error parsing actor and movies. Try again.")


    # --- Game 4: Guess the Dialog Line ---
    elif game == "🧠 Guess the Dialog Line":
        st.subheader("🧠 Can you guess which movie this quote is from?")
        quote = ask_groq("Give me a famous movie quote and the movie it's from. Format: 'quote - movie'")
        if " - " in quote:
            line, movie_title = quote.split(" - ", 1)
            st.write(f"**Quote:** \"{line.strip()}\"")
            guess = st.text_input("Which movie is this quote from?")
            if st.button("Submit Guess"):
                if guess.strip().lower() in movie_title.lower():
                    st.success("🎯 You nailed it!")
                else:
                    st.error(f"It was from: {movie_title}")
        else:
            st.error("Couldn't parse quote. Try again.")

    # --- Game 5: Movie Emoji Riddle ---
    elif game == "🎬 Movie Emoji Riddle":
        st.subheader("🎬 Can you guess the movie from emojis?")
        riddle = ask_groq("Give me an emoji riddle representing a popular movie and the answer. Format: 'emojis - movie'")
        if " - " in riddle:
            emoji_hint, movie_title = riddle.split(" - ", 1)
            st.write(f"**Emoji Clue:** {emoji_hint.strip()}")
            guess = st.text_input("Your guess:")
            if st.button("Submit Guess"):
                if guess.strip().lower() in movie_title.lower():
                    st.success("👏 Correct!")
                else:
                    st.error(f"Answer was: {movie_title}")
        else:
            st.error("Couldn't parse emoji riddle. Try again.")

# ---------- Movie Recommendation Tab ----------
with tab1:
    st.header("🎞 Get Movie Recommendations")
    movie_name = st.text_input("Enter your favorite movie:")
    if st.button("Show Recommendations") and movie_name:
        results = recommend_movies_from_groq(movie_name)
        st.write(results or "No recommendations found.")

# ---------- Movie Quiz Tab ----------
with tab2:
    st.header("🧠 Movie Trivia Challenge")
    question, options, answer = get_random_question()
    st.write(question)
    selected = st.radio("Your answer:", options)
    if st.button("Submit Answer"):
        if selected == answer:
            st.success("🎉 Correct!")
        else:
            st.error(f"❌ Wrong. The correct answer: {answer}")

# ---------- Voice Tab ----------
with tab3:
    st.header("🎙 Talk to the App")
    if st.button("Record Voice"):
        transcript = transcribe_voice()
        st.write("You said:", transcript)

# ---------- Assistant Tab ----------
with tab4:
    st.header("🤖 Chat with Movie Assistant")
    query = st.text_input("Ask anything about movies:")
    if query:
        reply = ask_groq(query)
        st.markdown(f"**Groq Assistant:** {reply}")

# ---------- Footer ----------
st.markdown("""
<div style='text-align:center; font-size:14px; margin-top:50px; color:gray;'>
    
</div>
""", unsafe_allow_html=True)
def get_base64_bg(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set a background image using CSS (choose one method, here we are using base64 encoding)
bg_base64 = get_base64_bg("bg.png")  # Adjust path if necessary

# CSS with base64-encoded image
bg_css = f"""
<style>
.stApp {{
    background-image: url("data:image/png;base64,{bg_base64}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
"""

# Apply the CSS for the background image
st.markdown(bg_css, unsafe_allow_html=True)