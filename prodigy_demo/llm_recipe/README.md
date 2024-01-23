## 👽 LLM recipe

Now let's explore the use of LLMs in Prodigy.

Similarly, Prodigy offers built-in recipes with LLM integrations with `spacy-llm`. They have integrations with a number of LLM providers, including:

- OpenAI;
- Cohere;
- Anthropic etc. 

You can [read more about them here.](https://prodi.gy/docs/recipes#textcat-llm.correct) 

However, if you would like to make minor admendments to the recipes, you can similarly customise them, making use of libraries like `langchain`.

Let's explore a simple custom LLM recipe. 

### 👽🛫 Classifying airline tweets: LLM edition 

Let's revisit the simple **text classification task** where we would like to label tweets about airlines as `positive` or `negative` for sentiment.

Instead of using a huggingface model, let's use a LLM to classify the tweets.

In your prodigy environment, install additional libraries:

```
pip install -r llm_requirements.txt
```
Then, ensure you have the openai API key in your environment variables. 

```
echo OPENAI_KEY="YOUR_API_KEY" >> .env
```

Now you can run the recipe to see how it works:

```
prodigy textcat_llm llm_tweets_annotated \
    ./data/data_to_label_500.jsonl \
    -F llm_recipe.py
```

A few specific considerations when dealing with LLM-annotated data:

1. **LLM models are not deterministic**. This means that you could get different results each time you run the recipe. As a result, it's important to have good error handling in your recipe.

2. **LLM models are not always fast**. Depending on the size of your data to label and complexity of the task, you may need to wait longer for the model to return predictions.

**A note on ports**

By default, the recipe will run locally on the `:8080` port. You will need to either: 

1. kill this port or; 
2. change the port

If you want to see how updating the recipe changes the interface. 

To kill your port:
```
lsof -i :8080
#COPYING THE PID
kill -9 PID
```

To change the port, you can add the `--port` flag. For instance, to run on port `:8081`:

```
PRODIGY_PORT=8081 prodigy textcat_hf tweets_annotated \
    ./data/data_to_label_500.jsonl \
    -F text_classification_recipe.py 
```

### 🔍 Exploring labelled data 

After playing around with these different parameters and labelling a few examples, you should have a dataset of labelled examples. **NOTE:** Do not forget to save your annotations!

To learn about your labelled data, you can run the following commands: 

```
prodigy progress llm_tweets_annotated #for annotation progress

prodigy stats llm_tweets_annotated #for annotation statistics
```

Finally, to save the database out as a `.jsonl` file, you can run the following command:

```
prodigy db-out llm_tweets_annotated > ./data/llm_annotations.jsonl
```

You can use the `./data/llm_annotations.jsonl` file to explore labels in a notebook or use it as training data downstream. 