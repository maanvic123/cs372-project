# README.md

# 🎶 VibeCheck: An AI-Powered Music Recommendation System
VibeCheck is an interactive music recommendation system that integrates preprocessing, ML embeddings, vector search, and UI in one unified system. Users can find songs using short vibe or mood descriptions (e.g. "motivational chill study", "roadtrip singalong", "energetic evening run"). User-inputted text is embedded with an OpenAI embedding model, compared against a large FAISS vector index built from 1 million songs + audio features from Spotify, and the top three recommended tracks are displayed with Spotify embeds for easy listening.

# 🚀 What It Does
1. Embeds input user text using **text-embedding-3-small** (OpenAI)
2. Searches a FAISS IVF index containing song embeddings for the three most similar vectors.
3. Returns the top recommended songs as Spotify song previews embedding in the UI.


# 📦 File Structure
```
├── src/
│   ├── streamlit_app.py            # main Streamlit UI + FAISS index search logic
│   ├── preprocessing.py            # preprocessing pipeline for features + track IDs
│   ├── disco.png                   # image for UI
│   ├── final_project.ipynb         # embedding/index generation, evaluation
│
├── data/
│   ├── raw/raw_spotify_data.csv    # raw Kaggle dataset (too large for git)
│   ├── processed/features.npy      # feature matrix
│   ├── processed/scaler.pkl        # StandardScaler info
│   ├── processed/track_ids.npy     # 1D array of track_IDs
│
├── requirements.txt
├── README.md
├── SETUP.md
└── ATTRIBUTION.md
````


# ⚙️ Quick Start

### **1. Install dependencies**
```bash
pip install -r requirements.txt
````

### **2. Download FAISS index file**
Download faiss_ivf_flat.index (7GB) from Box: *(Insert your link here)*

### **3. Create `.env` file**
Copy:
```bash
cp .env.example .env
```
Then edit `.env` with your filepath to downloaded faiss_ivf_flat.index:
```
FAISS_INDEX_PATH=path/to/downloaded/faiss_ivf_flat.index
```

### **4. Run the application**
```bash
streamlit run src/streamlit_app.py
```


# 🎥 Demo Video Links

### **1. High-Level Overview Demo**
*(Insert your link here)*

### **2. Technical Walkthrough / Code Explanation**
*(Insert your link here)*

# 📊 Evaluation
Evaluation results and discussion
are included in the **Evaluation** section of `src/final_project.ipynb`.


# 👥 Individual Contributions
This was an individual project completed by Maanvi Chawla.