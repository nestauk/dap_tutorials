"""
textcat recipe with parameters to experiment with.

We are experimenting with the following aspects of the recipe:

1. Using a different baseline model;
2. Filtering data to label and;
3. Sorting examples based on model predictions.

To run this recipe:

prodigy textcat_hf tweets_annotated \
    data_to_label_500.jsonl \
    -F text_classification_recipe.py
    
"""
from typing import List, Optional, Iterator
import copy

import prodigy
from prodigy.components.loaders import JSONL
from prodigy.components.preprocess import add_tokens
import spacy

from prodigy.components.sorters import prefer_uncertain

# 1. USE A DIFFERENT BASELINE MODEL

# Here, we're using the spacy-huggingface integration to load
# a sentiment analysis transformers model from HuggingFace.

# Can you experiment with different models that are appropriate for the task?
# This could mean changing the model name, or simply using a spaCy model
# instead of huggingface.

# here, we're loading a blank model
nlp = spacy.blank("en")

# now we're adding the huggingface model to the pipeline
nlp.add_pipe(
    "hf_text_pipe",
    config={"model": "distilbert-base-uncased-finetuned-sst-2-english"},
)

# 2. FILTER DATA TO LABEL

# Here, we have a filtering function to exlude examples
# based on some filtering criteria.

# Can you update this function to filter based on different criteria?
# Perhaps its based on key words or POS tags.

# As an extension, look into prodgy's pattern matcher
# to filter based on patterns.


def _filter_data(text: str, example_length: int = 5) -> str:
    """Filter stream based on length of text. 

    Args:
        text (str): Text to filter
        example_length (int, optional): Text length. Defaults to 5.

    Returns:
        str: Filtered text
    """
    # filter based on length of text
    return text if len(text) > example_length else None


def make_tasks(nlp, stream: Iterator[dict]) -> Iterator[dict]:
    """Score stream based on model predictions.

    Args:
        stream (Iterator[dict]): stream

    Yields:
        Iterator[dict]: Stream with model predictions
    """
    texts = ((eg["text"], eg) for eg in stream)
    for doc, eg in nlp.pipe(texts, as_tuples=True):
        task = copy.deepcopy(eg)
        filtered_text = _filter_data(task["text"])
        if filtered_text:
            # 3. SORT DATA TO LABEL

            # here, we're sorting examples based on the model's uncertainty.
            # let's find examples where the model is uncertain about the label
            # i.e. between 0.4 and 0.6
            # can you change this to prefer examples where the model is MOST certain i.e. highest scores?
            # how about least certain i.e. lowest scores?

            # NOTE: Prodigy also offer pre-built sorters like prefer_high_scores

            highest_score_cat = max(doc.cats, key=doc.cats.get)

            if 0.4 <= doc.cats[highest_score_cat] <= 0.6:
                eg["label"] = highest_score_cat
                eg["meta"] = {"score": doc.cats[highest_score_cat]}

                yield eg


@prodigy.recipe("textcat_hf",
                dataset=("The dataset to use", "positional", None, str),
                source=("The source data", "positional", None, str))
def textcat_hf(dataset, source):

    # here, we're loading our data from a jsonl file
    stream = JSONL(source)

    # we're adding tokens to the stream
    stream = add_tokens(nlp, stream)

    # here, we're making tasks based on our filtering criteria and
    # sorting them based on the model's uncertainty
    stream = make_tasks(nlp, stream)

    return {
        "dataset": dataset,
        "stream": stream,
        "view_id": "classification",
        "config": {
            "labels": ["POSITIVE", "NEGATIVE"],  # Customize labels as needed
            "wrap_text": True,
        },
    }
