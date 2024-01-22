"""
A custom LLM recipe for text classification.

prodigy textcat_llm llm_tweets_annotated \
    ./data/data_to_label_500.jsonl \
    -F llm_recipe.py
"""
from typing import Iterator
import copy

import prodigy
from prodigy.components.loaders import JSONL
from prodigy.components.preprocess import add_tokens
import spacy
import os

from dotenv import load_dotenv

import langchain_core.runnables.base

import langchain_openai

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()
# here, we're loading our openai api key from a .env file
# in the /llm_recipe directory
oi_key = os.getenv('OPENAI_KEY')

# if it doesn't exist, we'll throw an error
if not oi_key:
    assert False, "OPENAI_KEY not set in .env file"

# let's instantiate our output parser so that the llm model
# returns string rather than a ChatMessage object
output_parser = StrOutputParser()

# finally, lets instantiate our llm model - we're using OpenAI's
llm = langchain_openai.ChatOpenAI(openai_api_key=oi_key)

# The below function makes use of the llm,
# output parser and prompt to make a chain of runnables
# that we will invoke to return a llm-generated label


def _make_chain(output_parser: langchain_core.output_parsers = output_parser,
                llm: langchain_openai.ChatOpenAI = llm
                ) -> langchain_core.runnables.base.RunnableSequence:
    """Make a chain of runnables for text classification.

    Args:
        output_parser (langchain_core.output_parsers): Output parser
        llm (langchain_openai.ChatOpenAI): LLM model

    Returns:
        langchain_core.runnables.base.RunnableSequence: Chain of runnables
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are world class data labeller. You will label the input sentence for sentiment as either positive or negative. Please only return the label itself."),
        ("user", "{input_sentence}")
    ])

    chain = prompt | llm | output_parser

    return chain

# This is the main function of the recipe where we define the tasks associated to each example.
# Here, we use the llm to generate an initial label for each example. If the LLM does not return
# a label, we assign a label that we can correct downstream.

# We could improve error handling here by i.e. regex matching the output of the llm to ensure
# it maps to the available labels (positive, negative).
# We could also add a timeout to the llm to deal with cases where it takes
# too long to return a label.


def make_tasks(
    nlp: spacy.language.Language,
    stream: Iterator[dict],
) -> Iterator[dict]:
    """Make tasks for text classification.

    Args:
        nlp (spacy.language.Language): spacy language model
        stream (Iterator[dict]): stream of examples

    Yields:
        Iterator[dict]: stream of examples with llm-generated labels
    """
    chain = _make_chain()
    texts = ((eg["text"], eg) for eg in stream)
    for doc, eg in nlp.pipe(texts, as_tuples=True):
        task = copy.deepcopy(eg)
        sent = str(task['text'])
        llm_label = chain.invoke({"input_sentence": sent})
        if isinstance(llm_label, str):
            task["label"] = llm_label
        else:
            # assign a random label we can correct downstream
            task["label"] = "negative"

        yield task

# Finally, we define the prodigy recipe. Much like the basic recipe, we
# follow the same structure:

# 1. Load the data to label (in this case, from a jsonl file)
# 2. define an NLP objsect and add tokens to the stream
# 3. add llm-generated labels to the stream via the make_tasks function
# 4. return the stream of examples to be annotated


@prodigy.recipe("textcat_llm",
                dataset=("The dataset to use", "positional", None, str),
                source=("The source data", "positional", None, str))
def textcat_llm(dataset, source):

    # here, we're loading our data from a jsonl file
    stream = JSONL(source)

    nlp = spacy.blank("en")
    # now we're adding tokens to the stream
    stream = add_tokens(nlp, stream)

    # finally, we can add llm-generated labels to the stream
    stream = make_tasks(nlp, stream)

    return {
        "dataset": dataset,  # this is the name of the dataset to be used
        "stream": stream,  # this is the stream of examples to be annotated
        "view_id": "classification",  # this is the view id to be used
        "config": {
            "wrap_text": True,
        },
    }
