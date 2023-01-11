# Collect data from Twitter API v2

In this have-a-go session we explore different Twitter API v2 endpoints and collect data from Twitter using Python. Do not forget to follow the instructions below **before** the session, in order to get the most from it.


## To do *before* the have-a-go session
Please follow the instructions below prior to the have-a-go session. They shouldn't take more than 15 minutes of your time.

### Twitter account, developer account and app setup
1. Register as a [Twitter user](https://twitter.com/i/flow/signup);
2. Create a [developer account](https://developer.twitter.com/en/portal/petition/essential/basic-info);
3. Create your first app by giving it a unique name and copy your credentials (API key, API secret and Bearer Token) to a secure location.

More detail on getting access to the Twitter API is available from [Twitter’s step-by-step guide](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api).

### 🛠️ Code set up 
Open your terminal and follow the instructions:
1. **Clone this repo:** 

`git clone https://github.com/nestauk/dap_tutorials.git`

2. **Navigate to this tutorial's folder:** 

`cd collect_twitter_data`

3. **Create your conda environment:** 

`conda create --name collect_twitter_data python=3.9`

4. **Activate your conda environment:** 

`conda activate collect_twitter_data`

5. **Install package dependencies:** 

`pip3 install -r requirements.txt`

6. **Set your credentials as environment variables:** 

`export BEARER_TOKEN="ADD_YOUR_BEARER_TOKEN_HERE"` and replace `ADD_YOUR_BEARER_TOKEN_HERE` with your bearer token credentials.

7. **Add your conda environment to the notebooks:** 

`python -m ipykernel install --user --name=collect_twitter_data`

8. **Open the first notebook and make sure you have the correct kerne** 

Launch `jupyter-notebook` and make sure your kernel is the right environment, `collect_twitter_data`.


## Tutorial 🤓
This have-a-go will start with an introduction to Twitter API v2 and then we will go through a series of jupyter notebooks, where you will have exercises to help you get familiar with the API.

1. **[Your first Twitter API request](https://github.com/nestauk/dap_tutorials/blob/dev/collect_twitter_data/01.%20Your%20first%20Twitter%20API%20request.ipynb)**

On the first part of this tutorial you will learn how to make your first Twitter API request. This request will output data similar to the mock data below:

```
{'edit_history_tweet_ids': ['100'],
 'author_id': '1',
 'created_at': '2022-11-11T18:25:36.000Z',
 'text': 'I have installed a heat pump in my home!',
 'id': '100'}
```

2. **[Tweets from the past 7 days](https://github.com/nestauk/dap_medium_articles/blob/dev/collect_twitter_data/02.%20Tweets%20from%20the%20past%207%20days.ipynb)**

On the second part of this tutorial, we will collect Twitter data from the past 7 days using the recent search endpoint. This time, we are collecting additional user information, like in the mock example below:

```
{'id': '987654321',
 'name': 'Number 1 Heat Pump Fan',
 'username': 'heat_pump_fan',
 'description': 'I am a heat pump fan!',
 'location': 'My house in the UK',
 'verified': False}
```

3. **[Exercises to explore the search endpoint](https://github.com/nestauk/dap_tutorials/blob/dev/twitter_api_tutorial/Exercises%20to%20explore%20the%20search%20endpoint.ipynb)**