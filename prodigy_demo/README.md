## 🪄 Prodigy have-a-go session

In this have-a-go session we will explore **Prodigy**, a data annotation tool by [Explosion AI](https://explosion.ai/) (the creators of [spaCy](https://spacy.io/)). Prodigy allows you to flexibly annotate data: text, images, video and audio.

In order to use Prodigy for your annotation tasks you need a license. We have 5 seats in the Data Science Practice, which are freely transferrable within the company. However, if you do need a license for a project, please join Nesta's `#dsp-prodigy` slack channel and ask for a license key.

### 🛠️ Setup

Run the following on your command line before the have-a-go session:
1. If you don't have this repo in your local computer run: `git clone https://github.com/nestauk/dap_tutorials.git`; Otherwise open this repo locally and run `git fetch origin`;
2. `cd YOUR_LOCAL_PATH/dap_tutorials/prodigy_demo/` where `YOUR_LOCAL_PATH` is your local path to your repos' folder;
2. `conda create --name prodigy_demo python=3.9`
3. `conda activate prodigy_demo`
4. `pip install -r requirements.txt`
5. `pip install -r ./llm_recipe/llm_requirements.txt` - specific requirements for the llm recipe;
6. `echo OPENAI_KEY=<YOUR_API_KEY> >> .env` where `YOUR_API_KEY` is your OpenAI API key (we will make one available for you);
6. If you do have a Prodigy license key run `python -m pip install prodigy -f https://XXXX-XXXX-XXXX-XXXX@download.prodi.gy`. If you don't, someone in your have-a-go session group will have.

### 💡 This *have-a-go*

In this *have-a-go session* we will cover:
- the basics of Prodigy: what it is, what it can be used for, the front end of a basic recipe, input and output files, handling multiple annotators and pros and cons of Prodigy;
- [enhancing a basic text annotation recipe](basic_recipe/);
- [using LLMs in a recipe](llm_recipe/);
- [creating a recipe with multiple annotation tasks and making small enhancements that improve the annotators' experience](multiple_tasks_recipe/).

### 👶 What is Prodigy?

Let's go into a bit more detail about Prodigy. 

**Prodigy** is a annotation tool, typically used to create training and test data for machine learning models. There's a Python library that enables you to customise your annotation environment: the questions you ask, the annotation labels available, how the data is loaded and saved, and the behaviour of your front end application.

The data can then be manually annotated by a group of annotators or enhanced with semi-automated processes such as **active learning** to speed up the annotation process.

It's important to note that Prodigy isn't free. Nesta's Data Science Practice purchased 5 Prodigy seats, which are transferrable within the company.

### 🤔 What can I used Prodigy for? Existing and custom recipes

You can apply Prodigy for a variety of use cases and tasks. For a [full list check the documentation](https://prodi.gy/docs/recipes). A couple worth mentioning and that we've already applied in our day to day work at Nesta:

- **Named Entity Recognition (NER)**: by tagging names and concepts in text according to a set of labels;
- **Text classification**: by assigning one of more categories to text;
- **Part-of-Speech tagging**: by tagging specific parts of speech in text;
- **Computer vision**: by annotating images;

If you want have multiple annotation tasks at once (*e.g.* NER and text classification in the same annotation), Prodigy also allows for that type of customisability.

You can also:
- Train models;
- Review annotations/resolve conflicts between annotators and compute inter-annotator agreement.

Each of the above tasks has a respective **recipe**: *"A Python function that can be executed from the command line and starts the Prodigy server for a specific task"*.

### 🧑‍🍳 Basic recipe & the respective front end

As mentioned above, you might want to use one of the existing **recipes**.

For example, if you want to manually label text data to identify person, organisation and product entities, you can run:

`prodigy ner.manual ner_news en_core_web_sm ./news_headlines.jsonl --label PERSON,ORG,PRODUCT`

(If you want to run the code above, download the data from [here](https://raw.githubusercontent.com/explosion/prodigy-recipes/master/example-datasets/news_headlines.jsonl)).
If all runs well, you can then open `http://localhost:8080` and start annotating. We'll guide you through the different parts of the front end.


### ❗ Changing a basic recipe

To change a basic recipe, all you need to do is create a Python script (e.g. `name_of_your_recipe_script.py`) which should follow the structure below:

```
...
@prodigy.recipe("name_of_your_new_recipe",
                dataset=("The dataset to use", "positional", None, str), #database name
                source=("The source data", "positional", None, str)) # relative path of the .jsonl dataset to be annotated

def function_detailing_the_annotation(dataset, source):
    # loading our data from a jsonl file
    stream = JSONL(source)

    # adding tokens to the stream
    stream = add_tokens(nlp, stream)

    ...

    return {
        "dataset": dataset, # database where annotations will be stored
        "stream": stream, # this is the stream of examples to be annotated
        "view_id": "classification", # view id i.e. annotation task to do
        "config": {
            ...
        },
    }
```

You can then run your recipe by doing:
```
prodigy name_of_your_new_recipe database_name .path_to_source_data_to_annotate  -F name_of_your_recipe_script.py
```

### 📥 Input and output files

Prodigy typically reads data from ***JSONL*** files.

JSONL or JSON lines is a text-based format that uses the `.jsonl` file extension. It's essentially the same as JSON format, except that newline character is used to delimit JSON data.
Example can be found in this [link](https://raw.githubusercontent.com/explosion/prodigy-recipes/master/example-datasets/news_headlines.jsonl).

After data has been annotated (*and saved!*) you can extract your annotated outputs by doing (for the example above):
`prodigy db-out ner_news > annotated_ner_news.jsonl`

You can also customise your output - we will cover this in the [multiple tasks recipe](multiple_tasks_recipe/).

### 🟢🔴 Pros & Cons of Prodigy

Pros:
- very easy to customise the front end (allowing for multiple types of annotations at once) and the output data;

Cons:
- Associated cost - only free for researchers;
- Initial learning curve;

### 🧑‍🤝‍🧑 Multiple annotators

What if you need multiple people to annotate data? *No problem!* The license allows for unlimited annotators. The easiest way to set that up is by:
- Creating an EC2 instance (reach out to our data engineering team if you're unsure of how to do this);
- Clone the repo where your Prodigy code lives;
- Run your Prodigy recipe inside the EC2 instance;
- Send the respective EC2 instance link to your annotators: `http://YY.YYY.YYY.YYY:8080/?session=<your_name>`
    - note the `?session=<your_name>` at the end of the URL, where each annotator should replace `<your_name>` by their name, so that we're able to 

It is also possible to have different annotators annotating different instances. Check this video: xxx

### 📚 Resources
List of Nesta repos where Prodigy has been used:
- PRINZ project:
    - [SIC industry mapping: the code doesn't work anymore because the langchain library has changed since, but you can get the idea structurally](https://github.com/nestauk/dap_prinz_green_jobs/tree/dev/dap_prinz_green_jobs/pipeline/green_measures/industries/prodigy);
- Skills Extractor Library:
    - [extracting skills for the skills extractor](https://github.com/nestauk/ojd_daps_skills/tree/dev/ojd_daps_skills/pipeline/skill_ner/prodigy);
    - [exploratory labelling for dimensions of job quality](https://github.com/nestauk/dap_job_quality/tree/dev/dap_job_quality/pipeline/prodigy);
- Floorplan project:
    - [labelling floor plan images with where rooms/doors/windows are + categorising rooms into room types](https://github.com/nestauk/asf_floorplan_interpreter/pull/2)
- Generative AI Project:
    - [getting people to evaluate the responses from vanilla GPT4 vs a retrieval-augmented GPT4](https://github.com/nestauk/discovery_generative_ai/tree/dev/src/genai/parenting_chatbot/prodigy_eval) + [corresponding blog](https://medium.com/discovery-at-nesta/how-to-evaluate-large-language-model-chatbots-experimenting-with-streamlit-and-prodigy-c82db9f7f8d9)
- Innovation Sweet Spots:
    - [Multiclass classification with GPT and Prodigy](https://github.com/nestauk/discovery_child_development/tree/dev/discovery_child_development/pipeline/labelling/taxonomy/prodigy);

Other resources:
- [Explosion AI's GitHub repository with recipe examples](https://github.com/explosion/prodigy-recipes);
- [Prodigy's support forum.](https://support.prodi.gy/);