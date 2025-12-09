# README.md

# 🎶 VibeCheck: An AI-Powered Music Recommendation System
VibeCheck is an interactive music recommendation system for users looking to expand their music tastes, soundtrack a certain vibe, or find similar songs without needing to know genres, artists, or music theory. People often just know the mood they want, but maybe not which songs fit that mood. VibeCheck bridges that gap by helping users find music that meaningfully matches their emotional context. With just a short prompt, VibeCheck will search and recommend three songs from a database of over 1 million songs.

# 🚀 What It Does
1. User inputs a short vibe or mood description (e.g. "motivational chill study", "roadtrip singalong", "energetic evening run").
2. User text input is embedded using OpenAI embedding model **text-embedding-3-small**.
3. System searches FAISS IVFF (Facebook AI Similarity Search, Inverted File Indexing, Flat) index that contains song embeddings to find the top three most similar songs to the user input.
4. The top recommended songs are displayed as Spotify song previews.


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
### **1. Clone repository**
```bash
git clone https://github.com/maanvic123/cs372-project.git
cd cs372-project
````

### **2. Install dependencies**
```bash
pip install -r requirements.txt
````

### **3. Download FAISS index file**
Download `faiss_ivf_flat.index` (7GB): [FAISS Index Download (Box)](https://duke.box.com/s/mb95gtp3egrfdvu7i874b9dgt1ubxaiy)

### **4. Create `.env` file**
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

### **5. Run app with Streamlit**
```
streamlit run src/streamlit_app.py
```

### **6. Search for songs by vibe**
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