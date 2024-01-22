import prodigy
from prodigy.components.loaders import JSONL
from prodigy.components.preprocess import add_tokens
import spacy


def sentiment_options(stream):
    # Helper function to add options to every task in a stream
    options = [
        {"id": 1, "text": "Positive 👍"},
        {"id": -1, "text": "Negative 👎"},
        {"id": 0, "text": "Neutral 😶"},
    ]
    for task in stream:
        task["options"] = options
        yield task


@prodigy.recipe(
    "multiple-tasks-recipe",
    dataset=("The dataset to use", "positional", None, str),
    source=("The source data as a JSONL file", "positional", None, str),
)

def blocks_solution(dataset, source, lang="en"):
    # Reading HTML to create checkbox
    with open("html_checkbox.html") as f:
        HTML_checkbox = f.read()

    # order of annotation blocks
    blocks = [
        {"view_id": "ner_manual"},
        {"view_id": "choice", "text": None},
        {
            "view_id": "text_input",
            "field_rows": 1,
            "field_label": "Elaborate on the above choice, if needed:",
        },
        {"view_id": "html", "html_template": HTML_checkbox},
    ]

    # Reading in JavaScript code for default label and for checkbox key binding
    with open("annotation_javascript.js") as f:
        javascript = f.read()

    nlp = spacy.blank(lang)

    stream = JSONL(source)  # load the JSONL data file
    stream = sentiment_options(stream)  # add options to task

    stream = add_tokens(nlp, stream)

    stream = list(stream)  # to show the percentage already annotated

    return {
        "dataset": dataset,  # save annotations in this dataset
        "view_id": "blocks",  # use the blocks interface
        "stream": stream,
        "config": {
            "instructions": "annotation_instructions.html", # information about the annotation setup
            "buttons": ["accept", "reject", "ignore"],
            "labels": [
                "Weather", "Location", "Date/time"
            ],  # the labels for the manual NER interface
            "blocks": blocks,
            "custom_theme": {"labels": {"Weather": "#9A1BBE", "Location": "#18A48C", "Date/time": "#FDB633",},},
            "keymap_by_label": {
                "Weather": "w",
                "Location": "l",
                "Date/time": "d",
                "0": "p",
                "1": "n",
                "2": "0",
            },
            "history_length": 20, # number of annotations to appear on the side
            "javascript": javascript,
        },
    }
