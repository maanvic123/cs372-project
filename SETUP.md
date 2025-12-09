# SETUP.md

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