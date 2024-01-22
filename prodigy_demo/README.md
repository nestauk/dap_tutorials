## 🪄 Prodigy have-a-go session

In this have-a-go session we will explore **Prodigy**, a data annotation tool by [Explosion AI](https://explosion.ai/) (the creators of [spaCy](https://spacy.io/)). Prodigy allows you to flexibly annotate data: text, images, video and audio.

In order to use Prodigy for your annotation tasks you need a license. We have 5 seats in the Data Science Practice, which are freely transferrable within the company. However, if you do need a license for a project, please join Nesta's `#prodigy` slack channel and ask for a license key.

### 🛠️ Setup

Run the following on your command line before the have-a-go session:
1. If you don't have this repo in your local computer run: `git clone https://github.com/nestauk/dap_tutorials.git`; Otherwise open this repo locally and run `git fetch origin`;
2. `cd YOUR_LOCAL_PATH/dap_tutorials/prodigy_demo/` where `YOUR_LOCAL_PATH` is your local path
2. `conda create --name prodigy_demo python=3.9`
3. `conda activate prodigy_demo`
4. `pip install -r requirements.txt`
5. `pip install -r requirements.txt` - specific LLM ones
6. export open ai key
6. If you do have a Prodigy license key run `python -m pip install prodigy -f https://XXXX-XXXX-XXXX-XXXX@download.prodi.gy`. If you don't, someone in your have-a-go session group will have.

### 💡 This *have-a-go*

In this *have-a-go session* we will cover:
- the basics of Prodigy: what it is, what it can be used for, the front end of a basic recipe, input and output files, handling multiple annotators and pros and cons of Prodigy;
- enhancing a basic text annotation recipe;
- using LLMs in a recipe;
- creating a recipe with multiple annotation tasks;
- small enhancements that improve the annotators' experience.

### 👶 What is Prodigy?

Prodigy is a annotation tool, typically used to create training and test data for machine learning models. There's a Python library that enables you to customise your annotation environment: the questions you ask, the annotation labels available, how the data is loaded and saved, and the behaviour of your front end application.

The data can then be manually annotated by a group of annotators or enhanced with semi-automated processes such as active learning to speed up the annotation process.

It's important to note that Prodigy isn't free or open source. Nesta's Data Science Practice purchased 5 Prodigy seats, which are transferrable within the company.

### 🤔 What can I used Prodigy for? Existing and custom recipes

You can apply Prodigy for a variety of use cases and tasks. For a [full list check the documentation](https://prodi.gy/docs/recipes). A couple worth mentioning and that we've already applied in our day to day work at Nesta:

- **Named Entity Recognition (NER)**: by tagging names and concepts in text according to a set of labels;
- **Text classification**: by assigning one of more categories to text;
- **Part-of-Speech tagging**: by tagging specific parts of speech in text;
- **Computer vision**: by annotating images;

If you want have multiple annotation tasks at once (e.g. NER and text classification in the same annotation), Prodigy also allows for that type of customisability.

You can also:
- Train models;
- Review annotations/resolve conflicts between annotators and compute inter-annotator agreement.

Each of the above tasks has a respective **recipe**: *"A Python function that can be executed from the command line and starts the Prodigy server for a specific task"*.

### 🧑‍🍳 Basic recipe & the respective front end

As mentioned above, you might want to use one of the existing recipes.

`prodigy ner.manual ner_news en_core_web_sm ./news_headlines.jsonl --label PERSON,ORG,PRODUCT`


Missing the prints xxxxx


### 📥 Input and output files

Prodigy typically reads data from ***JSONL*** files.

JSONL or JSON lines is a text-based format that uses the `.jsonl` file extension. It's essentially the same as JSON format, except that newline character os used to delimit JSON data.
Example can be found in this [link](https://raw.githubusercontent.com/explosion/prodigy-recipes/master/example-datasets/news_headlines.jsonl)


### 🟢🔴 Pros & Cons of Prodigy

Pros:
- very easy to customise the front (allowing for multiple types of annotations at once) end and the output data;

Cons:
- Associated cost; only free for researchers;
- Initial learning curve;

### 🧑‍🤝‍🧑 Multiple annotators

What if multiple people need to annotate data?

- how to have users annotate different instances?


### 📚 Resources
- List of Nesta repos where Prodigy has been used:
    - PRINZ project:
    - Floorplan project:
    - Innovation Sweet Spots:
- Explosion AI's GitHub repository with recipe examples
- Prodigy's support forum.