
## 📓 Basic recipe

As already discussed, the simplest approach to using Prodigy is to use the built-in recipes. These recipes are designed to be used with the `prodigy` command-line interface. 

However, if you would like to make minor admendments to the recipes, you can copy the recipe file and modify it to your needs. 

Let's explore small modifications you might want to make with a hypothetical example.

### 🛫 Classifying airline tweets

Let's start with a simple **text classification task** where we would like to label tweets about airlines as `positive` or `negative` for sentiment.

At its simplest, we could simply use the `textcat.manual` built-in recipe or, if we would like to train a classifier in the loop, we could use the `textcat.teach` built-in recipe.

To run the recipe:


```
prodigy textcat_hf tweets_annotated \
    ./data/data_to_label_500.jsonl \
    -F text_classification_recipe.py
```
### 🛫 Classifying airline tweets: Exercise 

We might want to make some modifications to this basic recipe. This exercise explores **3 such modifications** you might want to make.

We explore how we could:

1. **Use a different baseline model**: The simplest model to use is a spaCy model, but we might want to use a different model, for instance, a huggingface model. Read [more about this here.](https://github.com/explosion/spacy-huggingface-pipelines) 

2. **Filter data to label**: We might want to filter out some examples, for instance, by only labeling examples that contain a particular keyword or by length of text. We've added a `patterns.jsonl` file that contains a list of keywords to filter with should you want to try this out. 

3. **Sort data to label**: We might want to label examples in a particular order, for instance, by sorting the examples by model score.

As an extension, feel free to apply any additional learnings from the `llm_recipe` or aesthetics focused recipe. 

Let's experiment with how we could do play around with these parameters in the `text_classification_recipe_QUESTIONS.py` 🚀

With every change you make, run your recipe to see if/what changes:

```
prodigy textcat_hf tweets_annotated \
    ./data/data_to_label_500.jsonl \
    -F text_classification_recipe_QUESTIONS.py
```

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
prodigy progress tweets_annotated #for annotation progress

prodigy stats tweets_annotated #for annotation statistics
```

Finally, to save the database out as a `.jsonl` file, you can run the following command:

```
prodigy db-out tweets_annotated > ./data/annotations.jsonl
```

You can use the `annotations.jsonl` file to explore labels in a notebook or use it as training data downstream. 