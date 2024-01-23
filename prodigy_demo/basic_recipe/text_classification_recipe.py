"""
Custom textcat recipe (a text classification recipe).

To run this recipe:

prodigy textcat_hf tweets_annotated \
    ./data/data_to_label_500.jsonl \
    -F text_classification_recipe.py
    
"""
from typing import List, Optional, Iterator
import copy

import prodigy
from prodigy.components.loaders import JSONL
from prodigy.components.preprocess import add_tokens
import spacy

# here, we're loading a blank model
nlp = spacy.blank("en")

# now we're adding the huggingface model to the pipeline
nlp.add_pipe(
    "hf_text_pipe",
    config={"model": "finiteautomata/bertweet-base-sentiment-analysis"},
)
#The model we're using above is this hosted transformers model on huggingface: 
# https://huggingface.co/finiteautomata/bertweet-base-sentiment-analysis

# Here, we have a filtering function to exlude examples
# based on some filtering criteria.
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
            # here, we're sorting examples based on the model's uncertainty.
            # let's find examples where the model is uncertain about the label
            # i.e. between 0.4 and 0.6
            highest_score_cat = max(doc.cats, key=doc.cats.get)

            if 0.4 <= doc.cats[highest_score_cat] <= 0.6:
                eg["label"] = highest_score_cat
                eg["meta"] = {"score": doc.cats[highest_score_cat]}

                yield eg

#Below is the recipe that we use to call the functions above and
#render the annotation interface.

#here we are passing arguments like the name of the dataset to be used (aka a SQLite table)
#and the relative path of the .jsonl dataset to be annotated
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
