"""
This script creates a sub-sample of twitter data
to a .jsonl format from which it can be annotated using Prodigy.

python prodigy_demo/convert_data.py -ts 500
"""
import plac
import srsly

import pandas as pd
from pathlib import Path
import os

@plac.annotations(
    train_size=("train_size", "option", "ts", int),
    random_seed=("random_seed", "option", "rs", int),
)
def make_labelled_data(
    train_size: int = 500, random_seed: int = 42
):
    """Create a sub-sample of the example twitter data and
    convert it to .jsonl format from which it can be annotated
    using Prodigy.

    Args:
        train_size (int, optional): size of labelled data.
            Defaults to 500.
        random_seed (int, optional): random seed for reproducibility.
    """
    data_path = Path.cwd() / 'prodigy_demo'
    unformatted_training_data = data_path / 'raw/text_classification_tweets.csv'

    tweets_df = pd.read_csv(unformatted_training_data)

    # load data to label
    data_to_label = (tweets_df
                     .query('airline_sentiment != "neutral"')
                     .sample(frac=1, random_state=random_seed)[:train_size]
                     .reset_index(drop=True)
                     .to_dict(orient="records"))

    print('converting data to jsonl format...')
    converted_training_data = []
    for data in data_to_label:
        training_data_json = {
            "text": data["text"],
            # you can add additional meta data. This key is used to
            # store metadata related to the task. This could include any additional
            # information about that task that you want to reference later.
            # you could add metadata like the tweeter, the date, source etc.

            # i.e. "meta": {"id": data["tweet_id"], "date": data["date"]}
            "meta": {"id": data["tweet_id"]},
            # storing ground truth label in the label key
            "label": data["airline_sentiment"],
        }
        converted_training_data.append(training_data_json)

    # save data locally
    print('save jsonl data...')
    basic_processed_path = data_path / 'basic_recipe/data'
    llm_processed_path = data_path / 'llm_recipe/data'
    
    if not basic_processed_path.exists():
        os.makedirs(basic_processed_path)
    
    if not llm_processed_path.exists():
        os.makedirs(llm_processed_path)
    
    srsly.write_jsonl(
        os.path.join(
            data_path,
            "basic_recipe",
            "data",
            f"data_to_label_{str(train_size)}.jsonl",
        ),
        converted_training_data,
    )

    srsly.write_jsonl(
        os.path.join(
            data_path,
            "llm_recipe",
            "data",
            f"data_to_label_{str(train_size)}.jsonl",
        ),
        converted_training_data,
    )

if __name__ == "__main__":
    plac.call(make_labelled_data)
