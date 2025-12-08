# SETUP.md

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
Copy and paste the following information into `.env` file, and replace *FAISS_INDEX_PATH* with filepath from downloaded file.
```
OPENAI_API_KEY=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
SPOTIFY_CLIENT_ID=1a16f34fb6824359b976119b8c8450cc
SPOTIFY_CLIENT_SECRET=d32daae82d8f4a16b1c0a10b32e41000
FAISS_INDEX_PATH=/your/downloaded/path/to/faiss_ivf_flat.index
```

### **4. Run app with Streamlit**
```
streamlit run src/streamlit_app.py
```

### **5. Search for songs by vibe**
1. On Streamlit UI, enter a few words about your mood or current vibe, and press enter.
2. Check out the recommended songs!
3. Click "search again" to try again.