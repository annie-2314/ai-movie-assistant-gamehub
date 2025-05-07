import pickle
import pandas as pd

df = pd.DataFrame(pickle.load(open("movies.pkl", "rb")))
cs = pickle.load(open("cs.pkl", "rb"))

def recommend(movie_title):
    idx = df[df['title'] == movie_title].index[0]
    distances = cs[idx]
    similar = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
    return [(df.iloc[i]["id"], df.iloc[i]["title"]) for i, _ in similar]
