"""
A Flow for processing text data (including lemmatisation and removing stop words) from a sustainability and a heating sub-forum.

To run the code, use the following command:
python metaflow_tutorial_solution.py --package-suffixes=.txt --datastore=s3 run --category <category>

where <category> is one of the sub-forums:
"sustainability": A sub-forum on sustainability.
"energy-sources-for-heating": A sub-forum on energy sources for heating.
"""

import os

# Upgrading pip and installing requirements
os.system("python -m pip install --upgrade pip")
os.system(
    f"pip install -r {os.path.dirname(os.path.realpath(__file__))}/flow_requirements.txt 1> /dev/null"
)
os.system("python -m spacy download en_core_web_sm")
from metaflow import FlowSpec, step, batch, Parameter, retry
import pandas as pd
from text_processing_utils import remove_tokens_in_list

FORUM_LOCAL_RAW_FOLDER_PATH = "data/raw"
FORUM_LOCAL_PROCESSED_FOLDER_PATH = "data/processed"
CHUNKSIZE = 200


def remove_stopwords_from_specified_columns(
    data: pd.DataFrame, columns: list, stopwords: list
) -> pd.DataFrame:
    """
    Removes stopwords from certain columns in data.

    Args:
        data (pd.DataFrame): data
        columns (list): column names
        stopwords (list): list of stopwords to be removed
    Returns:
        pd.DataFrame: forum data with stopwords removed from text and titles
    """
    for col in columns:
        data[col + "_no_stopwords"] = data.apply(
            lambda x: remove_tokens_in_list(x[col], stopwords), axis=1
        )
    return data


class TextProcessingFlow(FlowSpec):
    category = Parameter(
        name="category", help="A category or sub-forum", default="sustainability",
    )
    test = Parameter(
        name="test", help="Set to True to run flow on test mode.", default=False,
    )

    @step
    def start(self):
        """
        Starts the flow and reads raw data from the local raw data folder.
        """
        import os
        import pandas as pd

        local_path = os.path.join(
            FORUM_LOCAL_RAW_FOLDER_PATH, f"forum_data_category_{self.category}.csv",
        )
        self.forum_data = pd.read_csv(local_path)

        if self.test:
            self.forum_data = self.forum_data[:100]

        self.next(self.process_text_and_titles)

    @step
    def process_text_and_titles(self):
        """
        Pre-processing text and titles (before applying lemmatisation) by
        removing URLs, putting text to lowercase and removing username patterns.
        """
        from text_processing_utils import preprocess_text

        self.forum_data["processed_text"] = self.forum_data["text"].apply(
            lambda x: preprocess_text(x)
        )
        self.forum_data["processed_title"] = self.forum_data["title"].apply(
            lambda x: preprocess_text(x)
        )

        self.next(self.prepare_chunks_of_data)

    @batch
    @step
    def prepare_chunks_of_data(self):
        """
        Chunking data to allow for parallel lemmatisation and tokenisation.
        """
        self.chunks = [
            self.forum_data[i : i + CHUNKSIZE]
            for i in range(0, len(self.forum_data), CHUNKSIZE)
        ]
        self.next(self.lemmatise_and_tokenise_text_data, foreach="chunks")

    @batch(cpu=2, memory=8000)
    @step
    def lemmatise_and_tokenise_text_data(self):
        """
        Creates columns with lemmatising and tokenised titles and text from posts and replies.
        """
        from text_processing_utils import lemmatise, tokenise

        chunk = self.input
        chunk["lemmatised_tokens_text"] = chunk["processed_text"].apply(lemmatise)
        chunk["tokens_text"] = chunk["processed_text"].apply(tokenise)
        chunk["lemmatised_tokens_title"] = chunk["processed_title"].apply(lemmatise)
        chunk["tokens_title"] = chunk["processed_title"].apply(tokenise)
        self.data = chunk

        self.next(self.join_data_from_previous_step)

    @retry
    @batch
    @step
    def join_data_from_previous_step(self, inputs):
        """
        Joining data from all batches after lemmatisation.
        """
        import pandas as pd

        self.forum_data = pd.DataFrame()
        for input in inputs:
            self.forum_data = pd.concat([self.forum_data, input.data])
        self.next(self.remove_stopwords)

    @step
    def remove_stopwords(self):
        """
        Removing stopwords and punctuation.
        """
        from text_processing_utils import english_stopwords_definition

        stopwords = english_stopwords_definition()
        self.forum_data = remove_stopwords_from_specified_columns(
            self.forum_data,
            [
                "tokens_text",
                "tokens_title",
                "lemmatised_tokens_title",
                "lemmatised_tokens_text",
            ],
            stopwords,
        )
        self.next(self.save_data)

    @step
    def save_data(self):
        """
        Saving data to your local directory/S3 bucket.
        """
        if not self.test:  # only saves data if not in test mode
            self.forum_data.to_csv(
                f"s3://dsp-tutorials/metaflow/forum_data_category_{self.category}.csv",
                index=False,
            )
        self.next(self.end)

    @step
    def end(self):
        """
        Ends the flow.
        """
        pass


if __name__ == "__main__":
    TextProcessingFlow()
