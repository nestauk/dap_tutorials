"""
Script to preprocess the tiktok songs dataset

In the terminal, run the following commands:

$ cd data
$ python preprocess_tiktok.py
"""
from pathlib import Path
import pandas as pd

DATA_PATH = 'TikTok_songs_2022.csv'
OUTPUT_PATH = 'TikTok_songs_2022_preprocessed.csv'

if __name__ == '__main__':
    
    (
        pd.read_csv(DATA_PATH)
        # Create unique song identifiers
        .assign(track=lambda df: df.index.astype(str) + '_' + df.track_name + ' by ' + df.artist_name)
        .to_csv(OUTPUT_PATH, index=False)
    )