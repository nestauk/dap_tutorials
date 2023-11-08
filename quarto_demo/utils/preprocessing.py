import pandas as pd


def preprocess_strings(strings: pd.Series) -> pd.Series:
    """Cleaning list of strings; removing punctuation and extra spaces,
    making the text lower case and placing _ for the remaining whitespace.

    Args:
        strings (pd.Series): Panda series of strings to clean.

    Returns:
        pd.Series: Pandas series of cleaned strings.
    """
    strings = (
        strings.str.replace(r"[/]", " ", regex=True)
        .str.replace(r"[:()\%']", "", regex=True)
        .str.replace("  ", " ", regex=True)
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-zA-Z0-9_]", r"_", regex=True)
        .str.replace("___", "_", regex=True)
        .str.replace("__", "_", regex=True)
    )
    return strings


def convert_range_to_list(yaml_dict: dict) -> list:
    """Converts the start, stop and step integers in a yaml file to a list comprehension of the range
    of these values.

    Args:
        yaml_dict (dict): The dictionary from the yaml file.

    Returns:
        list: List of the range of values.
    """

    value_list = [
        value
        for value in range(yaml_dict["start"], yaml_dict["stop"], yaml_dict["step"])
    ]

    return value_list
