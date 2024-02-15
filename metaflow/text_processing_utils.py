"""
Text processing functions to:
- remove URLs from text;
- remove username patterns;
- remove specific tokens/emojis from text;
- define english stopwords using NLTK and spaCy;
- lemmatise text;
- tokenise text;
"""

import pandas as pd
import logging
from typing import Union
import re
from nltk.corpus import stopwords
import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

logger = logging.getLogger(__name__)


def remove_urls(text: str) -> str:
    """
    Removes URLs from text.
    Args:
        text (str): a string, tipically one or multiple sentences long
    Returns:
        str: text without URLs
    """
    # Define a regular expression pattern for matching URLs
    url_pattern = re.compile(r"https?://\S+|www\.\S+")

    # Replace URLs with a space
    cleaned_text = url_pattern.sub(" ", text)
    return cleaned_text


def remove_text_after_patterns(text: str) -> str:
    """
    Removes patterns of the form "xxx wrote: »" and "xxx said:".

    Args:
        text (str): text to be cleaned

    Returns:
        str: cleaned text
    """
    # We use re.sub() to replace the pattern with an empty string
    result = re.sub(r"\w+ wrote: »", " ", text)
    result = re.sub(r"\w+ said:", " ", result)

    return result


def remove_tokens_in_list(
    data: Union[pd.Series, list], list_of_tokens_to_remove: list
) -> Union[pd.Series, list]:
    """
    Removes specific tokens from a pandas Series or list.

    Args:
        data (Union[pd.Series, list]): original data
        list_of_tokens_to_remove (list): list of tokens to be removed

    Returns:
        Union[pd.Series, list]: data without tokens in list
    """
    return [token for token in data if token not in list_of_tokens_to_remove]


def remove_emojis(text: str) -> str:
    """
    Removes emojis from text.

    Args:
        text (str): original text

    Returns:
        str: text with emojis removed
    """
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r"", text)


def preprocess_text(text: str) -> str:
    """
    Preprocesses text by:
        - replacing &amp/& with "and"
        - replacing ">" and "=" with space
        - removing URLs
        - transforming text to lower case
        - removing username patterns
        - removing emojis

    Args:
        text (str): text to be processed
    Returns:
        str: Preprocessed text.
    """
    # Replacing "and" symbols with keyword "and"
    text = re.sub("&amp;", " and ", text)
    text = re.sub("&", " and ", text)

    # Replacing certain symbols with space as multiple of them appear together
    # and don't disappear by deleting punctuation
    text = re.sub(">", " ", text)
    text = re.sub("=", " ", text)

    text = remove_urls(text)

    text = text.lower()

    text = remove_text_after_patterns(text)

    text = remove_emojis(text)

    return text


def english_stopwords_definition() -> list:
    """
    Defines English stopwords by putting together NLTK and SpaCy stopwords.

    Returns:
        list: a list of English stopwords.
    """
    spacy_stopwords = list(spacy.lang.en.STOP_WORDS)
    nltk_stopwrods = stopwords.words("english")

    return list(set(spacy_stopwords + nltk_stopwrods))


def lemmatise(text: str) -> list:
    """
    Applies lemmatisation sentence by sentence.
    It then removes punctuation and tokens tagged as space (e.g. "\n")

    Args:
        text (str): text to be lemmatise, might include multiple sentences

    Returns:
        list: list of lemmatised token without punctuation tokens
    """
    doc = nlp(text)
    # apply sentence by sentence lemmatisation
    processed_sentence_tokens = []
    for sentence in doc.sents:
        lemmatised_tokens = [
            token.lemma_.lower()
            for token in sentence
            if not (token.is_punct or token.pos_ == "SPACE")
        ]
        processed_sentence_tokens.extend(lemmatised_tokens)
    return processed_sentence_tokens


def tokenise(text: str) -> list:
    """
    Applies tokenisation and removes punctuation and tokens tagged as space (e.g. "\n")

    Args:
        text (str): text to be tokenised, might include multiple sentences

    Returns:
        list: list of tokens without punctuation tokens
    """
    doc = nlp(text)
    return [
        token.text.lower()
        for token in doc
        if not (token.is_punct or token.pos_ == "SPACE")
    ]
