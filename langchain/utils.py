"""
Util functions and objects for use in the LLM tutorial.
"""
from toolz import pipe
import pandas as pd
import re


def replace_characters(job_advert: str) -> str:
    """Replace characters with blank spaces in a string.

    Args:
        job_advert (str): job advert text

    Returns:
        str: job advert text with replaced characters
    """
    return job_advert.replace(
        '\n',
        ' ').replace(
        '\r',
        ' ').replace(
            '\t',
            ' ').replace(
                ' - ',
        ' ')


def get_job_text(job_advert: str) -> str:
    """Remove trailing text from job advert.

    Args:
        job_advert (str): job advert text

    Returns:
        str: Job advert text without trailing text
    """
    return job_advert.split('----------------------------------')[0].strip()


def clean_job_advert(job_advert: str) -> str:
    """Clean job advert text.

    Args:
        job_advert (str): job advert text

    Returns:
        str: cleaned job advert text
    """
    return pipe(
        job_advert,
        replace_characters,
        get_job_text
    )


def clean_date(date: str) -> pd._libs.tslibs.timestamps.Timestamp:
    """Clean date. If date does not end in a year, return None.

    Args:
        date (str): string of date

    Returns:
        pd._libs.tslibs.timestamps.Timestamp: date in timestamp format
    """
    ends_in_year = re.search(r'\b20\d{2}\b', date)
    date_clean = pd.to_datetime(
        date, format='%b %d, %Y') if ends_in_year else None
    return date_clean
