import requests
import json
import time
import random
import pandas as pd

endpoint_url = "https://api.twitter.com/2/tweets/search/recent"


def request_headers(bearer_token: str) -> dict:
    """
    Set up the request headers. 
    Returns a dictionary summarising the bearer token authentication details.

    Args:
        bearer_token: bearer token credentials
    """
    return {"Authorization": "Bearer {}".format(bearer_token)}


def connect_to_endpoint(endpoint_url: str, headers: dict, parameters: dict) -> json:
    """
    Connects to the endpoint and requests data.
    Returns a json with Twitter data if a 200 status code is yielded.
    Programme stops if there is a problem with the request and sleeps
    if there is a temporary problem accessing the endpoint.

    Args:
        endpoint_url: url to endpoint we are collecting data from
        headers: request headers
        parameters: query parameters
    """
    response = requests.request(
        "GET", url=endpoint_url, headers=headers, params=parameters
    )
    response_status_code = response.status_code
    if response_status_code != 200:
        if response_status_code >= 400 and response_status_code < 500:
            raise Exception(
                "Cannot get data, the program will stop!\nHTTP {}: {}".format(
                    response_status_code, response.text
                )
            )

        sleep_seconds = random.randint(5, 60)
        print(
            "Cannot get data, your program will sleep for {} seconds...\nHTTP {}: {}".format(
                sleep_seconds, response_status_code, response.text
            )
        )
        time.sleep(sleep_seconds)
        return connect_to_endpoint(endpoint_url, headers, parameters)
    return response.json()


def process_twitter_data(
    json_response: json,
    query_tag: str,
    tweets_data: pd.DataFrame,
    users_data: pd.DataFrame,
    places_data: pd.DataFrame,
) -> tuple[pd.DataFrame]:
    """
    Adds new tweet/user/place information to the table of
    tweets/users/places and saves dataframes as pickle files,
    if data is avaiable.

    Args:
        json_response: new data collected from the endpoint
        query_tag: tag/name of the query
        tweets_data: tweets info collected so far
        users_data: users info collected so far
        places_data: places info collected so far

    Returns:
        Returns the tweets, users and places updated dataframes.
    """
    if "data" in json_response.keys():
        new = pd.DataFrame(json_response["data"])
        tweets_data = pd.concat([tweets_data, new])
        tweets_data.to_pickle("tweets_" + query_tag + ".pkl")

        if "users" in json_response["includes"].keys():
            new = pd.DataFrame(json_response["includes"]["users"])
            users_data = pd.concat([users_data, new])
            users_data.drop_duplicates("id", inplace=True)
            users_data.reset_index(drop=True, inplace=True)

        if "places" in json_response["includes"].keys():
            new = pd.DataFrame(json_response["includes"]["places"])
            places_data = pd.concat([places_data, new])
            places_data.drop_duplicates("id", inplace=True)
            places_data.reset_index(drop=True, inplace=True)

        users_data.to_pickle("users_" + query_tag + ".pkl")
        places_data.to_pickle("places_" + query_tag + ".pkl")

    return tweets_data, users_data, places_data


def collect_and_process_twitter_data(
    bearer_token: str, rules: list[dict], query_params: dict
):
    """
    Collects, processes and saves twitter data following a set of rules and query parameters.

    Args:
        bearer_token: Twitter bearer token credentials
        rules: rules for collecting Twitter data. Should contain "value" and "tag" keys
        query_paramers: parameters for data collection
    """

    headers = request_headers(bearer_token)

    for i in range(len(rules)):
        tweets_data = pd.DataFrame()
        users_data = pd.DataFrame()
        places_data = pd.DataFrame()

        query_params["query"] = rules[i]["value"]
        query_tag = rules[i]["tag"]

        json_response = connect_to_endpoint(endpoint_url, headers, query_params)
        tweets_data, users_data, places_data = process_twitter_data(
            json_response, query_tag, tweets_data, users_data, places_data
        )

        time.sleep(5)

        while "next_token" in json_response["meta"]:
            query_params["next_token"] = json_response["meta"]["next_token"]

            json_response = connect_to_endpoint(endpoint_url, headers, query_params)
            tweets_data, users_data, places_data = process_twitter_data(
                json_response, query_tag, tweets_data, users_data, places_data
            )

            time.sleep(5)
