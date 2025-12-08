# SETUP.md

### **1. Install dependencies**
```bash
pip install -r requirements.txt
````

### **2. Download FAISS index file**
Download `faiss_ivf_flat.index` (7GB): [FAISS Index Download (Box)](https://duke.box.com/s/mb95gtp3egrfdvu7i874b9dgt1ubxaiy)

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