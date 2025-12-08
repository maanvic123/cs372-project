from pathlib import Path
import os
import time
from typing import List

import streamlit as st
import numpy as np
import pandas as pd
import faiss
import openai
import requests
import base64
from dotenv import load_dotenv, find_dotenv

# load .env file from project dir
load_dotenv(find_dotenv())

# ----- config -----
# set file paths
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH")
TRACK_IDS_PATH = Path("data/processed/track_ids.npy")

# set embedding model and OpenAI/Spotify API keys
EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
_spotify_token = {"access_token" : None, "expires_at" : 0}


# ----- streamlit page config -----
st.set_page_config(page_title="VibeCheck", layout="centered")

# ----- streamlit UI -----
# function to encode local file with base64 for global access
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

BASE_DIR = Path(__file__).resolve().parent
DISCO_PATH = BASE_DIR / "images" / "disco.png"
disco_ball_base64 = get_base64_image(DISCO_PATH)

if 'page' not in st.session_state:
    st.session_state.page = 'search'
if 'vibe_query' not in st.session_state:
    st.session_state.vibe_query = ''

# inline CSS style file
base_styles = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fascinate&family=Roboto:wght@400;500&display=swap');

    .stApp {{
        background-color: #B84C65;
    }}

    .main .block-container {{
        padding-top: 1rem;
        max-width: 800px;
    }}

    .disco-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }}

    .disco-ball {{
        width: 180px;
        height: auto;
        margin-bottom: 30px;
        filter: drop-shadow(0 10px 20px rgba(0,0,0,0.3));
    }}

    .title {{
        font-family: 'Fascinate', cursive;
        font-size: 4.5rem;
        color: white;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }}

    .subtitle {{
        font-family: 'Fascinate', cursive;
        font-size: 2.5rem;
        color: white;
        text-align: center;
        margin-bottom: 0px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }}

    .search-container {{
        width: 100%;
        max-width: 550px;
        margin: 0 auto;
    }}

    .stTextInput {{
        max-width: 550px;
        margin: 0 auto;
    }}

    .stTextInput > div > div {{
        position: relative;
        border-radius: 25px;
        overflow: hidden;
    }}

    .stTextInput > div {{
        border-radius: 25px;
    }}

    .stTextInput > div > div::before {{
        content: '';
        position: absolute;
        left: 15px;
        top: 50%;
        transform: translateY(-50%);
        width: 18px;
        height: 18px;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23555555' viewBox='0 0 24 24'%3E%3Cpath d='M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z'/%3E%3C/svg%3E");
        background-size: contain;
        background-repeat: no-repeat;
        z-index: 1;
        pointer-events: none;
    }}

    .stTextInput > div > div > input {{
        font-family: 'Roboto', sans-serif;
        font-size: 1rem;
        padding: 12px 20px 12px 45px;
        border-radius: 25px;
        border: none;
        background-color: #FFFFFF;
        color: #333333;
        caret-color: black;
    }}

    .stTextInput > div > div > input::placeholder {{
        color: #888888;
    }}

    .stTextInput > div > div > input:focus {{
        outline: none;
        box-shadow: 0 0 10px rgba(255,255,255,0.2);
        border: none;
    }}

    .stTextInput > label {{
        display: none;
    }}

    .spotify-embed {{
        margin: 5px auto;
        max-width: 400px;
        background: transparent;
    }}

    .spotify-embed iframe {{
        background: transparent;
    }}

    .back-button {{
        font-family: 'Roboto', sans-serif;
        background-color: transparent;
        color: white;
        border: 2px solid white;
        padding: 10px 25px;
        border-radius: 25px;
        cursor: pointer;
        font-size: 1rem;
        margin-top: 50px;
        transition: all 0.3s ease;
    }}

    .back-button:hover {{
        background-color: white;
        color: #B84C65;
    }}

    .stButton {{
        display: flex;
        justify-content: center;
        max-width: 400px;
        margin: 0 auto;
    }}

    .stButton > button {{
        font-family: 'Roboto', sans-serif;
        background-color: transparent;
        color: white;
        border: 2px solid white;
        padding: 10px 25px;
        border-radius: 25px;
        cursor: pointer;
        font-size: 1rem;
        margin-top: 10px;
        transition: all 0.3s ease;
    }}

    .stButton > button:hover {{
        background-color: white;
        color: #B84C65;
        border: 2px solid white;
    }}

    header {{
        visibility: hidden;
    }}

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    .stDeployButton {{
        display: none;
    }}
    .stSpinnerMessage {{
        font-size: 24px !important;
        font-weight: 600 !important;
        color: white !important;
    }}
    .stSpinner > div {{
        gap: 12px !important;
    }}
    .stSpinner {{
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        padding-top: 40px !important;
    }}
"""

st.markdown(base_styles, unsafe_allow_html=True)


# ----- functions to load resources once and cache -----
# load FAISS index file
@st.cache_resource(show_spinner=False)
def load_faiss_index(path: str):
    faiss_index = faiss.read_index(str(path))
    faiss_index.nprobe = 16     # inference parameter - number of clusters to search at query times
    return faiss_index

# load track_ids csv file
@st.cache_resource(show_spinner=False)
def load_track_ids(path: str):
    return np.load(str(path), allow_pickle=True).astype(str)

# get OpenAI client
@st.cache_resource(show_spinner=False)
def get_openai_client():
    return openai.OpenAI(api_key=OPENAI_API_KEY)

# get spotify access token 
@st.cache_resource(show_spinner=False)
def get_spotify_token():
    now = time.time()
    # token already exists
    if _spotify_token["access_token"] and _spotify_token["expires_at"] > now + 10:
        return _spotify_token["access_token"]
    # get and cache new access token if current token not valid
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type" : "client_credentials",
        "client_id" : SPOTIFY_CLIENT_ID,
        "client_secret" : SPOTIFY_CLIENT_SECRET
    }
    headers = {"Content-Type" : "application/x-www-form-urlencoded"}
    resp = requests.post(url, data=data, headers=headers)
    resp.raise_for_status()
    jd = resp.json()
    # store token and expiration time
    _spotify_token["access_token"] = jd["access_token"]
    _spotify_token["expires_at"] = now + jd.get("expires_in", 3600)
    # return spotify access token
    return _spotify_token["access_token"]


# ----- OpenAI API call -----
# function to embed user input text with OpenAI API call
def embed_text(text: str):
    resp = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[text]
    )
    emb = np.array(resp.data[0].embedding, dtype=np.float32)
    emb = emb / (np.linalg.norm(emb) + 1e-12)
    return emb.reshape(1, -1)


# ----- load heavy resources (one time) -----
# get FAISS index, track_id, OpenAI client
with st.spinner("Getting things ready..."):
    index = load_faiss_index(str(FAISS_INDEX_PATH))
    track_ids = load_track_ids(str(TRACK_IDS_PATH))
    openai_client = get_openai_client()


# ----- streamlit page functions -----
def show_search_page():
    st.markdown(f"""
    <div class="disco-container">
        <img src="data:image/jpeg;base64,{disco_ball_base64}" class="disco-ball" alt="Disco Ball">
        <h1 class="title">What's the vibe?</h1>
    </div>
    """, unsafe_allow_html=True)

    vibe_input = st.text_input("Search vibes",
                               placeholder="motivational chill study",
                               label_visibility="collapsed",
                               key="vibe_search")

    # embed user-inputted query vector, search for similar songs, return top 3 matches
    if vibe_input:
        st.session_state.vibe_query = vibe_input

        with st.spinner("Embedding + searching for similar songs..."):
            qvec = embed_text(vibe_input)   # embed user input with OpenAI API call
            D, I = index.search(qvec, 3)    # search FAISS index for top 3 similar song vectors
        
        # extract track IDs returned by FAISS
        ranked_track_ids = [track_ids[idx] for idx in I[0]]
        ranked_scores = [float(s) for s in D[0]]

        # store results to be used in results page
        st.session_state.recommended_tracks = ranked_track_ids
        st.session_state.recommended_scores = ranked_scores

        st.session_state.page = 'results'
        st.rerun()


def show_results_page():
    st.markdown(f"""
    <div class="disco-container">
        <h1 class="subtitle">Give these songs a listen!</h1>
    </div>
    """, unsafe_allow_html=True)

    # get recommended tracks + scores from search
    recommended_tracks = st.session_state.get("recommended_tracks", [])
    scores = st.session_state.get("recommended_scores", [])

    # get Spotify embeds for each recommended song via Spotify API call
    for track_id, score in zip(recommended_tracks, scores):
        st.markdown(f"""
        <div class="spotify-embed">
            <p style="color:white; font-size:16px; margin-bottom:5px;">
                Score: {score:.2f}
            </p>
            <iframe 
                style="border-radius:12px" 
                src="https://open.spotify.com/embed/track/{track_id}?utm_source=generator&theme=0" 
                width="100%" 
                height="152" 
                frameBorder="0" 
                allowfullscreen="" 
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                loading="lazy">
            </iframe>
        </div>
        """, unsafe_allow_html=True)

    # reset recommendations for another search
    if st.button("Search again"):
        st.session_state.page = 'search'
        st.session_state.vibe_query = ''
        st.session_state.recommended_tracks = []
        st.rerun()

# run streamlit pages
if st.session_state.page == 'search':
    show_search_page()
elif st.session_state.page == 'results':
    show_results_page()