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
│   ├── images/                     # folder with images
│   ├── streamlit_app.py            # main Streamlit UI + FAISS index search logic
│   ├── preprocessing.py            # preprocessing pipeline for features + track IDs
│   ├── final_project.ipynb         # embedding/index generation
│   ├── evaluation.ipynb            # evaluation + discussion of model performance
│
├── data/
│   ├── raw/raw_spotify_data.csv    # raw Kaggle dataset (too large for git)
│   ├── processed/features.npy      # feature matrix
│   ├── processed/scaler.pkl        # StandardScaler info
│   ├── processed/track_ids.npy     # 1D array of Spotify track IDs
│
├── .env.example                    # .env file to copy during setup
├── requirements.txt
├── README.md
├── SETUP.md
└── ATTRIBUTION.md

├── Duke Box
│   ├── faiss_ivf_flat.index        # FAISS index file generated in colab
````


# ⚙️ Quick Start

### **1. Install dependencies**
```bash
pip install -r requirements.txt
````

### **2. Download FAISS index file**
Download `faiss_ivf_flat.index` (7GB) from Box: *(Insert link here)*

### **3. Create `.env` file**
Copy:
```bash
cp .env.example .env
```
Copy and paste the following information into new `.env` file. Replace OpenAI and Spotify credentials with values from Gradescope submission, and replace *FAISS_INDEX_PATH* with your filepath from downloaded file.
```
OPENAI_API_KEY=<copy from gradescope>
SPOTIFY_CLIENT_ID=<copy from gradescope>
SPOTIFY_CLIENT_SECRET=<copy from gradescope>
FAISS_INDEX_PATH=/your/downloaded/path/to/faiss_ivf_flat.index
```

### **4. Run app with Streamlit**
```
streamlit run src/streamlit_app.py
```

### **5. Search for songs by vibe**
Enter a few words about your mood or current vibe, and press enter.
![VibeCheck Home Page](src/images/UI.png "VibeCheck Home Page")



# 🎥 Demo Video Links

### **1. High-Level Overview Demo**
*(Insert link here)*

### **2. Technical Walkthrough / Code Explanation**
*(Insert link here)*

# 📊 Evaluation
Detailed evaluation results and discussion are included in `src/evaluation.ipynb`. The plot below shows the results of three example queries and their corresponding recommended songs in a 2D embedding space.
![Evaluation PCA Plot](src/images/pcaplot.png "Evaluation PCA Plot")


# 👥 Individual Contributions
This was an individual project completed by Maanvi Chawla.