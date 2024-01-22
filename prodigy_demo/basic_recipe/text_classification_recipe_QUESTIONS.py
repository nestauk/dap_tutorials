"""
textcat recipe with parameters to experiment with.

We are experimenting with the following aspects of the recipe:

1. Using a different baseline model;
2. Filtering data to label and;
3. Sorting examples based on model predictions.

To run this recipe:

prodigy textcat_hf tweets_annotated \
    ./data/data_to_label_500.jsonl \
    -F text_classification_recipe_QUESTIONS.py
    
"""
from typing import List, Optional, Iterator
import copy

import prodigy
from prodigy.components.loaders import JSONL
from prodigy.components.preprocess import add_tokens
import spacy

# 1. USE A DIFFERENT BASELINE MODEL

# Here, we're using the spacy-huggingface integration to load
# a sentiment analysis transformers model from HuggingFace.

# Can you experiment with different models that are appropriate for the task?
# For example, you might want to use a transformers model fine tuned on tweets
# 
# i.e. finiteautomata/bertweet-base-sentiment-analysis. What's changed with the labels 
# when you re-run the instance?

#alternatively, you can simply use a spaCy model. 

# here, we're loading a blank model
nlp = spacy.blank("en")

# now we're adding the huggingface model to the pipeline
nlp.add_pipe(
    "hf_text_pipe",
    config={"model": "finiteautomata/bertweet-base-sentiment-analysis"},
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
    """Make tasks for annotation. This includes:
        - filtering text based on criteria;
        - sorting examples based on model predictions.

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

#Below is the recipe that we use to call the functions above and
#render the annotation interface.

#here we are passing arguments like the name of the dataset to be used (aka a SQLite table)
#and the relative path of the .jsonl dataset to be annotated

#can you pass an additional parameter to the recipe? 

# i.e. You might want to pass the nlp object and allow 
# the end user to pass the model name as a parameter instead.
@prodigy.recipe("textcat_hf",
                dataset=("The dataset to use", "positional", None, str),
                source=("The source data", "positional", None, str))
def textcat_hf(dataset, source):

    # here, we're loading our data from a jsonl file
    stream = JSONL(source)

    # now we're adding tokens to the stream
    stream = add_tokens(nlp, stream)

    # Finally, we're making tasks based on our filtering criteria and
    # sorting them based on the model's uncertainty
    stream = make_tasks(nlp, stream)

    return {
        "dataset": dataset, #this is the name of the dataset to be used
        "stream": stream, #this is the stream of examples to be annotated
        "view_id": "classification", #this is the view id to be used
        "config": {
            "wrap_text": True,
        },
    }
