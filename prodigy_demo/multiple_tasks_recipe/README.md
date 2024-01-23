# 🤓 Additional customisability

We're now going to explore having multiple annotation tasks in the same recipe and a few small aesthetic improvements we can do, that make the annotation process a lot faster for annotators.

## 🛠️ Setup
- Run `prodigy multiple-tasks-recipe annotated_data weather_data.jsonl  -F multiple_tasks_annotation_setup.py`
- Open `http://localhost:8080`

## 🗄️ The files

- `multiple_tasks_annotation_setup.py`: the new recipe we are creating which allows for multiple tasks in the same annotation and some customisation; this is the core file of this annotation;
- `annotation_instructions.html`: HTML file with annotation intructions for your annotators to follow;
- `html_checkbox`: HTML code to create a checkbox;
- `annotation_javascript.js`: javascript code for extra customisability;
- `extract_annotations.py`: script to customise your annotated/output data;
- `weather_data.jsonl`: data to annotate.

## 💡 Our silly annotation use case

We have collected text data from a forum matching on a set of weather-related keywords. Now we want to:
- Classify each forum post as weather related or not (binary classification task);
- Identifiy/label the following entities in text: weather related keywords, location and date/time (NER task).
- Allow the annotator to write free text about the annotation/piece of text (free text annotation);
- Identify if the discourse is positive, negative or neutral (multiclass classification task);
- Identify if the user posting is being sarcastic (binary classification task);

## 📁 Multiple tasks of the same type in the same annotation
Prodigy offers a solution for multiple tasks happening in the same annotation, the `blocks` recipe. However, this doesn't allow for multiple tasks of the same type, so sometimes we need a workaround.

In our case we have 3 classification tasks that we want to run at the same time, so our workaround consists of:
- Using the accept/reject buttons for classifying the forum post as weather related or not;
- using the `choice` (*i.e.* classification) recipe to classify the discourse as positive, negative or neutral;
- Creating a checkbox using HTML code to identify if the user posting is being sarcastic.

The NER task can be easily implemented using `ner_manual` and the free text by using `text_input` block.

The code for this can be found in `multiple_tasks_annotation_setup.py` and `html_checkbox.html`.

We define our blocks as
```
blocks = [
        {"view_id": "ner_manual"},
        {"view_id": "choice", "text": None},
        {
            "view_id": "text_input",
            "field_rows": 1,
            "field_label": "Elaborate on the above choice, if needed:",
        },
        {"view_id": "html", "html_template": HTML_checkbox},
    ]
```

## 🟪 Changing the colours of the buttons

Changing colours of buttons, but especially labels, can completely change the annotator experience (e.g. when labelling rooms, windows and stairs in floorplans at the same time). In our use case above, we wanted all our NER labels to have different colours, so we changed our `blocks_solution()` function in `multiple_tasks_annotation_setup.py`.

The change lives in the `return` statement, under `config`:

```
"custom_theme": {
                "labels": {
                    "Weather": "#9A1BBE",
                    "Location": "#18A48C",
                    "Date/time": "#FDB633",
                },
            },
```

## 🔠 Keybinding: assigning keys in your keyboard to specific tasks/labels

Annotators might want to use their mouse to click on labels/buttons on the screen, or they might want to use their keyboard. You can assign specific keys in your keyboard to labels and buttons. In our use case, we do that by so changing the `blocks_solution()` function in `multiple_tasks_annotation_setup.py`. Again the change lives in the `return` statement, under `config`:

```
"keymap_by_label": {
                "Weather": "w",
                "Location": "l",
                "Date/time": "d",
                "0": "p",
                "1": "n",
                "2": "0",
            },
```

To also have key binding for the sarcasm flag, we had to write some javascript code (living in `annotation_javascript`):

```
document.querySelector('#root').addEventListener('keyup', function(event) {
    if (event.keyCode === 83) {  // key code for character "s": 
        document.getElementById("sarcasm").click();
    }
})
```

## ➕ Adding and removing buttons

If you're not using one or multiple buttons, you can remove them so that they don't confuse your annotators.

In our use case,  we do that by so changing the `blocks_solution()` function in `multiple_tasks_annotation_setup.py`. Again the change lives in the `return` statement, under `config`:

```
"buttons": ["accept", "reject", "ignore"],
```

## ⌛ Progress bar

The progress bar typically has the infinite symbol, which is not very helpful. By changing the `stream` from a generator object to a list, you get a percentage instead.

In our use case, we do that by changing the the `blocks_solution()` function in `multiple_tasks_annotation_setup.py`:

```
stream = list(stream)  # to show the percentage already annotated
```

## 🏷️ Defining default labels (requires javascript)

When you have tasks such as NER or POS tagging, you have multiple labels available for selection. If you select a label, use it to label text, and then move on to the next instance to annotate, the label which will be highlighted will be the last one used, instead of the first label.

You can change this and always have the same label as the default label to be selected by writing some javascript code (see `annotation_javascript.js`):

```
let prevHash = null
document.addEventListener('prodigyupdate', v => {
    const { task } = event.detail
    // Select the label input for the given default label
    const defaultLabel = document.querySelector('input[value="Weather"]')
    if (task._task_hash !== prevHash) {  // the displayed task has changed
        defaultLabel.click()  // simulate click
        prevHash = task._task_hash
    }

})
```

## 📰 A longer background info

You can use HTML and create an HTML file (e.g. `annotation_instructions.html`) where you detail the annotation task, to make sure your annotators are aware of how they should annotate the data, as well as the meaning of all buttons.

After creating the HTML instructions you call them in your return recipe return statement:
```
"config": {
            "instructions": "annotation_instructions.html",  # information about the annotation setup
}
```

## ℹ️ An indicator of the instance ID being annotated

If you want an indication of the instance ID being annotated make sure your input data `JSONL` file has an "id" key inside the "meta" key, e.g.:

```
{"id":"1", "text":"blablabla", "meta":{"id":"1"}}
```

## 📥 Changing the contents of the output file

To generate the output file you can run
`prodigy db-out annotated_reviews > annotated_reviews.jsonl`

Alternatively you can create a python script, e.g. `extract_annotations.py` that details what your outputing:

`python extract_annotations.py annotated_data annotated_data.json`

You can remove variables you don't need or change the type of file where your output will be stored.

## 🤓 Exercises

Change the existing code by:
1. Adding a new task to the custom recipe. Perhaps you also want to do some POS tagging?
2. Removing the "ignore" button;
3. Change the colours of labels;
4. Changing the default label;
5. Changing the output file. Perhaps you want a Pandas dataframe instead?