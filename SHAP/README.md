# SHAP: the TL;DR 

## What is it?

At its highest level, SHAP and SHAP Values (SV) help to explain model performance. The purpose of SV is to calculate “fair contributions” of each individual to the coalition, and capture interactions. Formally, they indicate for each coalition member the average amount of contribution that a member takes to the coalition value.

SHAP values do the same thing with models: they try to calculate what are “fair contributions” of each feature in shifting the prediction from a “baseline” (mean prediction). 

Other model interpretability methods and frameworks include LIME (**L**ocal **I**nterpretability **M**odel-agnostic **E**xplanation), Counterfactual explanations for ML, Permutation Feature Importance, Interpret ML and DeepLIFT.

Graphs to learn how to interpret include: Force plot; Waterfall plot; Force plot - stacked observations; Bar plot; and Beeswarm plot.

## So what?

Calculating SHAP Values and interpreting SHAP graphs are helpful so...

* ...you can better understand 'black box' models. You get a sense of feature importance and whether feature values lower or raise predictions from a baseline. 

It can be used for a variety of models (e.g. NLP applications, neural networks, regressors, classifiers, clustering).  

## Libraries 

`pip install shap`

## Links

Link to [SHAP deck](https://docs.google.com/presentation/d/1hhddAj4pX9lXtVe9oncDQh0OwwUp6QEJ1CFx4W4_Z1I/edit#slide=id.g133d5c94db5_0_100).