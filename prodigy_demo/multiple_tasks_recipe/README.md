# 🤓 Additional customisability

We're now going to explore having multiple annotation tasks in the same recipe and a few small aesthetic improvements we can do, that make the annotation process a lot faster for annotators.

## 🛠️ Setup
- Run `prodigy multiple-tasks-recipe annotated_data weather_data.jsonl  -F multiple_tasks_annotation_setup.py`
- Open `http://localhost:8080`

## 📁 Multiple tasks of the same type in the same annotation

Prodigy offers a solution for multiple tasks happening in the same annotation, the `blocks` recipe. However, this doesn't allow for multiple tasks of the same type, so we need a workaround.

***Our silly example use case***
You have collected weather related text data from a forum based on finding data that matched a set of keywords. Now you want to:
- Classify each forum post as weather related or not;
- Identifiy/label the following entities in text: weather related keywords, location and date/time.
- Allow the annotator to write free text about the annotation/piece of text;
- Identify if the user posting is being sarcastic;
- Identify if the discourse is positive, negative or neutral.

## 🟪 Changing the colours of the buttons

Changing colours of buttons, but especially labels, can completely change the annotator experience (e.g. when labelling rooms, windows and stairs in floorplans at the same time). 

## 🔠 Keybinding: assigning keys in your keyboard to specific tasks/labels

Annotators might want to use their mouse to click on labels/buttons on the screen, or they might want to use their keyboard. You can assign specific keys in your keyboard to labels and buttons. 

## ➕ Adding and removing buttons

If you're not using one or multiple buttons, you can remove them so that they don't confuse your annotators.

## ⌛ Progress bar

The progress bar typically has the infinite symbol, which is not very helpful. By changing the `stream` type, you get a percentage instead.

## 🏷️ Defining default labels (requires javascript)

When you have tasks such as NER or POS taggig, you have multiple labels available for selection. If you select a label, then use it to label text and then move on to the next instance to annotate, the label which will be highlighted will be the last one used, instead of the first label.

You can change this and always have the same label as the default label to be selected.

## 📥 Changing the contents of the output file

To generate the output file you can run
`prodigy db-out annotated_reviews > annotated_reviews.jsonl`

Alternatively you can create a python script, e.g. `extract_annotations.py` that details what your outputing:

`python extract_annotations.py annotated_reviews annotated_reviews.json`

You can remove variables you don't need or change the type of file where your output will be stored.

## 📰 A longer background info

You can use HTML and create an HTML file where you detail the annotation task, to make sure your annotators are aware of how they should annotate the data as well as the meaning of all buttons.

## ℹ️ An indicator of the instance ID being annotated