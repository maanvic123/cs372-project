'''
1. Preprocess "spotify_data.csv" - clean and filter data, impute medians if needed
2. Output: features.npy (feature matrix), scaler.pkl (scaling to be used during inference), track_ids.npy (1D array of track_id aligned with features.npy rows)
'''

from pathlib import Path
import logging

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# ----- config -----
# logging / debugging
LOG = logging.getLogger("preprocessing")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# set dir and file paths
INPUT_CSV = Path("data/raw/raw_spotify_data.csv")   # downloaded Kaggle dataset
OUT_DIR = Path("data/processed")

# feature set for modeling/similarity
FEATURE_COLUMNS = [
    "danceability",
    "energy",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "loudness",
    "duration_ms",
    "popularity",
    "key",
    "mode",
    "time_signature",
]

# numerical columns to median impute if data missing 
IMPUTE_COLUMNS = [
    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "duration_ms",
    "popularity",
]


# ----- main preprocessing code -----
def preprocess():
    LOG.info("starting preprocessing")
    
    # load input csv to df
    df = pd.read_csv(INPUT_CSV)
    LOG.info("loaded %d rows", len(df))

    # clean data - remove rows with duplicate track_ids or missing info 
    before = len(df)
    df = df.drop_duplicates(subset=["track_id"])
    LOG.info("dropped %d duplicate track_id rows", before-len(df))

    before = len(df)
    df = df.dropna(subset=["track_id", "track_name", "artist_name"])
    LOG.info("dropped %d rows with missing data", before-len(df))

    # filter data - set bounds for tempo, duration, valence, energy, danceability to remove outliers
    before = len(df)
    df = df[(df["tempo"] > 0) & (df["tempo"] < 300)]
    df = df[(df["duration_ms"] > 10_000) & (df["duration_ms"] < 30 * 60 * 1000)]
    df = df[(df["valence"] >= 0) & (df["valence"] <= 1)]
    df = df[(df["energy"] >= 0) & (df["energy"] <= 1)]
    df = df[(df["danceability"] >= 0) & (df["danceability"] <= 1)]
    LOG.info("dropped %d rows during filtering. remaining rows: %d", before-len(df), len(df))

    # create new column with main genre (first value in "genre" column) if not null 
    df["main_genre"] = df["genre"].fillna("unknown").astype(str).str.split(",", n=1).str[0].str.lower()
    LOG.info("new column created: 'main_genre'")

    # convert all data in feature columns to numeric format (errors = NaN)
    for c in set(FEATURE_COLUMNS):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    # impute median for numeric columns if missing values
    for c in IMPUTE_COLUMNS:
        median = df[c].median(skipna=True)
        df[c] = df[c].fillna(median)
    LOG.info("all data convert to numeric format. missing data median imputed.")
    
    # build feature matrix
    X = df[FEATURE_COLUMNS].to_numpy(dtype=np.float32)
    LOG.info("feature matrix created. shape: %s", X.shape)

    # fit StandardScaler on entire dataset (standardize input features) and save scaler.pkl
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, OUT_DIR / "scaler.pkl")
    LOG.info("saved scaler to %s", OUT_DIR / "scaler.pkl")

    # save scaled features as np feature matrix
    np.save(OUT_DIR / "features.npy", X_scaled)
    LOG.info("saved scaled features to %s", OUT_DIR / "features.npy")

    # save track IDs in array aligned with features.npy rows for lookup
    track_ids = df["track_id"].astype(str).to_numpy()
    np.save(OUT_DIR / "track_ids.npy", track_ids)
    LOG.info("track IDs array saved to %s. rows: %d", OUT_DIR / "track_ids.npy", len(track_ids))

    LOG.info("preprocessing done. files saved to %s", OUT_DIR)


if __name__ == "__main__":
    preprocess()