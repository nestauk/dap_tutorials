
## 🛫 Metaflow have-a-go session

In this have-a-go session we will explore **Metaflow**, a framework for building and managing data pipelines.

*Have-a-go session organised by Aidan Kelly and Sofia Pinto.*

### 🛠️ Setup

Run the following on your command line before the have-a-go session:
1. If you don't have this repo in your local computer run: `git clone https://github.com/nestauk/dap_tutorials.git`; Otherwise open this repo locally and run `git fetch origin`;
2. `cd YOUR_LOCAL_PATH/dap_tutorials/metaflow/` where `YOUR_LOCAL_PATH` is your local path to your repos' folder;
2. `conda create --name metaflow_demo python=3.9`
3. `conda activate metaflow_demo`
4. `pip install -r requirements.txt`

### 💡 This *have-a-go*

In this *have-a-go session* we will cover:
- What is Metaflow? When is Metaflow used?
- Why might you need it?
- A Metaflow flow & the concept of step
- Parameters & variables in Metaflow
- Debugging your pipeline
- Scaling with Metaflow
- Organising your projects when using Metaflow
- Common issues when using Metaflow
- Tips for using Metaflow to scrape data

We will then go through an example and do some exercises.

### 🧐 What is Metaflow? And when is it used?

Metaflow is a framework for bulding and managing data pipelines. It allows to:
- Easily define complex workflows;
- Track all steps in the pipelie;
- Scale to cloud services like AWS.

You can use it to:
- Process & clean data;
- Collect data from APIs or by doing web scraping;
- Train and test machine learning models;

### ❓ Why might you need Metaflow? 
- To have nicely defined pipelines;
- To leverage cloud resources if you need more computing resources (using AWS batch with Metaflow is easier than setting up and EC2 instance and running a script on it);
- When you have complex and conflicting dependencies;
- To resume a pipeline from where it broke after you debug your code;

### ↗️ A metaflow flow & the concept of step

We call `flow` to a Metaflow pipeline. To create a `flow`:
- Create a new Python script and import the Python Metaflow library;
- Define a new flow class that inherits from the Metaflow `FlowSpec` class;
- Define a steps within the flow. Each step is a function within the flow class and it's preceded by the `@step` decorator;
    - You always need a `start` and an `end` step;
- Use `self.next()` to transition between steps.

Here's an example, from a flow script named `my_metaflow_flow.py`:

```python
from metaflow import FlowSpec, step

class MyFirstMetaflowFlow(FlowSpec):
    @step
    def start(self):
        # Add your code here
        self.next(self.another_step)

    @step
    def another_step(self):
        # Add your code here
        self.next(self.end)

    @step
    def end(self):
        # Concluding step
        print("Pipeline completed!")

if __name__ == '__main__':
    MyFirstMetaflowFlow()
```

To run the flow above you can run the following on your command line:
```bash
python my_metaflow_flow.py run
```

### 🎲 Parameters & variables in Metaflow

Metaflow allows you to define parameters to input values from the command line into your flow (similar to what we do when we use the `argparse` Python library). This is useful when you want to run the same flow with different parameters.

Here's an example, from a script named `parameter_flow.py`:

```python
from metaflow import FlowSpec, Parameter, step

class ParameterFlow(FlowSpec):
    alpha = Parameter('alpha',
                      help='Learning rate',
                      default=0.01)

    @step
    def start(self):
        print('alpha is %f' % self.alpha)
        self.next(self.doubling_alpha)
    
    @step
    def doubling_alpha(self):
        self.alpha = self.alpha * 2
        print('alpha is %f' % self.alpha)
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == '__main__':
    ParameterFlow()
```

As one can see:
- We use the `Parameter` class to define the parameters;
- We define our parameters inside our Flow class;
- We can access the parameters as attributes of the flow class, using `self.parameter_name`;

You can run the flow above with the following command, which will run the pipeline with the default `alpha` value of 0.01
```bash
python parameter_flow.py run 
```

or change the `alpha` value by running the following command:
```bash
python parameter_flow.py run --alpha 0.5
```

You can define variables in Metafaflow at each step, using `self.my_variable`. However, unlike parameters, variables are only accessible up to the next `foreach` step (we will learn about these in a section below!). See the following example:

```python
from metaflow import FlowSpec, step

class VariableFlow(FlowSpec):
    @step
    def start(self):
        self.my_variable = 1
        self.next(self.second_step)

    @step
    def second_step(self):
        print("second step", self.my_variable)
        self.next(self.end)
    
    @step
    def end(self):
        pass

if __name__ == '__main__':
    VariableFlow()
```

Small note: we're using `print` instead of `logging` in the examples above, as `logging` doesn't work in Metaflow.

### 🐛 Debugging your pipeline

Your flows will eventually break: *that's for sure❗* If your flow breaks, Metaflow will highlight where the issue occured (the specific step and line of code) and what it was (by printing an error message on the console). After you identify the error and fix it, you can use `resume` instead of `run` to continue the flow from where it broke. This avoids running the pipeline from the start.

If you run:
```bash
python parameter_flow.py run --alpha 0.5
```
and your code breaks, you can then fix the error and run:
```bash
python parameter_flow.py resume
```
This will continue the flow from where it broke, taking the same parameters as before.

### 🆙 Scaling with Metaflow

You can use Metaflow to scale your pipelines in two ways:
horizontal scaling and vertical scaling.

#### Horizontal scaling

You do horizontal scaling by paralellising a certain step (or multiple ones) in your flow. As an example, you might need to apply the same function to a large number of files or a large number of rows in a database. You can split the files/the rows into chunks and run the same function in parallel on each chunk. In addition to breaking your data into smaller chunks, you use the `foreach` argument in `self.next` as in the examples below.

Let's start with a toy example:
```python
from metaflow import FlowSpec, step

class MyToyParallelFlow(FlowSpec):

    @step
    def start(self):
        # Define your iterable (e.g., a list of numbers)
        self.list_of_numbers = [1, 2, 3, 4, 5]
        self.next(self.process_number, foreach='list_of_numbers') # note the foreach here

    @step
    def process_number(self):
        # Each branch processes one element of the iterable
        self.result = self.input * 2  # Example operation
        self.next(self.join)

    @step
    def join(self, inputs): # note the inputs here
        # Gather results from all branches
        self.results = [input.result for input in inputs]
        self.next(self.end)

    @step
    def end(self):
        # Final step - process or output the aggregated results
        print("Aggregated Results:", self.results)

if __name__ == '__main__':
    MyToyParallelFlow()
```

Now into a more real life example:

```python

from metaflow import FlowSpec, step

CHUNKSIZE = 100
S3_BUCKET = "my-s3-bucket"

class MyParallelFlow(FlowSpec):

    @step
    def start(self):
        # Read data from S3
        s3_path = f"s3://{S3_BUCKET}/path/to/data.parquet"
        with open(s3_path, "rb") as s3_file:
            self.data = pd.read_parquet(s3_file)

        self.next(self.prepare_chunks_of_data)

    @step
    def prepare_chunks_of_data(self):
        # Split data into chunks of CHUNKSIZE
        self.chunks = [
            self.data[i : i + CHUNKSIZE]
            for i in range(0, len(self.data) + 1, CHUNKSIZE)
        ]
        self.next(self.process_input, foreach='chunks') # note the foreach here

    @step
    def process_input(self):
        # self.input is one of the chunks of data defined above
        input_data = self.input

        input_data["processed_id"] = input_data["id"] * 2

        self.output_data = input_data
        self.next(self.join)

    @step
    def join(self, inputs): # note the inputs here
        import pandas as pd

        # Gather results from all parallel processes
        self.data = pd.DataFrame()
        for input in inputs:
            self.data = pd.concat([self.data, input.output_data])
        self.next(self.end)

    @step
    def end(self):
        # Final step - process or output the aggregated results
        print("Aggregated Results length:", len(self.data))

if __name__ == '__main__':
    MyParallelFlow()

```

Note that: the `join` step is not optional (you can call it whatever name you want though!). You always need to have a function calling both `self` and `inputs` after paralellising a step with `foreach`, even if the `join` step does not do anything (i.e. it's a dummy join that only points to the next step).

##### `max-workers` and `max-num-splits`

By default, Metaflow will run 16 tasks in paralell. To change this, change `max-workers` when running the flow, which defines the number of parallel workers running at a given time. For example, to run 32 tasks in parallel, run the following command:

```bash 
python my_parallel_flow.py run --max-workers 32
```

Note that, if you increase the number of workers too much, you might crash your laptop.

To make sure that the number of branches resulting from the `foreach` does not surpass a certain value, change the `max-num-splits` argument (100 by default). For example, to make sure that the number of branches does not surpass 1000, run the following command:

```bash
python my_parallel_flow.py run --max-num-splits 2000
```

When you change `max-num-splits`, nothing changes in the way your code is ran! It serves more as a sense check to make sure you haven't made a mistake when chunking your data/paralellising your code. If you know that the step you're parallelising will result into a large number of branches, it's a good idea to increase `max-num-splits` to a value that makes sense for your specific use case.

#### Vertical scaling

When you need more compute resources than your local machine can provide, you can use `batch` to run specific steps on larger AWS machines. To do that, use the `@batch` decorator in the steps you want to run on the cloud. Here's an example of a script named `batch_flow_script.py`:

```python
from metaflow import FlowSpec, step, batch

import os
os.system(
	f"pip install -r {os.path.dirname(os.path.realpath(__file__))}/flow_requirements.txt 1> /dev/null"
)

class BatchFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.processing_data)

    @step
    @batch(cpu=2, memory=4000)
    def processing_data(self):
        # This step will run on AWS Batch

        import pandas as pd
        # Add your code here
        # ...
        self.next(self.another_step)
    
    @step
    def another_step(self):
        # Add your code here
        self.next(self.end)

    @step
    def end(self):
        print("Pipeline completed! `processing_data` step ran on AWS Batch")
    
if __name__ == '__main__':
    BatchFlow()
```

In the example above, the `processing_data` step will run on AWS Batch. The `@batch` decorator takes two arguments: `cpu` and `memory`, which define the number of CPUs and the amount of memory the step will use on AWS Batch. You should start with a small number of CPUs and a small amount of memory and increase them as needed.

If you get a `Data Store Error` message, it might mean you need to increase your batch resources.

#### 📦 Python packages to be installed
As you can also see in the flow above, we are pip installing `flow_requirements.txt`. This is a workaround to install any dependencies that are not installed by default in the AWS Batch environment. Note that this specific line will run at every step and you can then import the necessary packages at every step (instead of importing them at the top of the script, as we usually do).
In fact, anything above the `class` definition will run at every step.

#### 📁 Importing configs & util files into the flow and saving metadata to S3
All configuration and utility files you might need to import need to be in the same directory as your flow script. Additionally, make sure change `package-suffixes` when running your code to account for the different types of files being imported by your Metaflow script.
```bash
python batch_flow_script.py --package-suffixes=.txt --datastore=s3 run
```

`datastore=s3` will save the metadata of your flow to S3. This is useful to keep track of your flow's progress and to debug it if it breaks.

#### 🗄️ Saving data
Note that you cannot save data locally in batch steps, so you need to save your data to S3.

As default, you cannot save data to any S3 bucket you want. You can save it to the `ds-tutorials` S3 bucket or ask the Data Engineering team to allow your outputs to be saved in a different S3 bucket.

### 📈 Organising your projects when using Metaflow
As mentioned above, when using AWS batch with Metaflow, you cannot import files in locations other than the folder your working on, so all the files you need to import: configs, utils, flow requirements, etc. need to be in the same folder as your flow script.

If you get import errors in your steps: ensure you’ve included a requirements file in the flow directory, have included the correct file types when using the `--package-suffixes=` command, and that your requirements are actually installable/don’t have clashing dependencies.

### 🤓 Tips for using Metaflow (to scrape data)
- Use `resume` to continue your flow from where it broke; this way, you don't have to request access to the website you're scraping data from again unecessarily, reducing:
    - the pressure on the website's servers;
    - the risk of being blocked by the website;
- Use `foreach` to parallelise your scraping process into small chunks, making sure you sleep in between requests;
- You might want to use `batch` - but there's some time associated to setting up the batch machines. Your code might not be faster when using batch, but it might still beneficial to use it if you're scraping a large number of pages;
- Make sure each step is very well defined and that you're only doing one thing! This will make it easier to debug your code;
- You might want to create a flow to collect the raw HTML files and another flow to extract the data from the HTML files - this way, if you decide to change how you're extracting the data, you don't have to re-scrape the pages;
- Create a parameter called `test` to enable you and your colleagues to run your code in test mode;
- All the code above your class definition will be run at every step of your flow, so if you need to define a variable with the date/time the flow started, for example, the best workaround is to define it as a parameter - if you define it above, your data will change at every step; Here's [an example of how we did it for a project](https://github.com/nestauk/asf_public_discourse_web_scraping/blob/dev/asf_public_discourse_web_scraping/pipeline/mse/scrape_mse.py#L47);

### 📚 Resources
- [Metaflow official docs](https://docs.metaflow.org/)
- Jack Vine's [DS: Guide to Writing Pipelines with Metaflow](https://docs.google.com/document/d/1r90nhSjTMhxEaly2BIQZjaTyyUOE5Aw9iOqsSIge4uk/edit#heading=h.ha6vzuxbag07)
- Example code from DS projects at Nesta:
    - [A flow to process text data](https://github.com/nestauk/asf_public_discourse_home_decarbonisation/blob/dev/asf_public_discourse_home_decarbonisation/pipeline/data_processing_flows/processing_text_data.py)
    - [A basic flow that reads and filters data](https://github.com/nestauk/afs_early_years_labour_market_analysis/blob/dev/afs_early_years_labour_market_analysis/pipeline/data_collection/refine_relevant_jobs.py)
    - [A flow that uses a foreach step](https://github.com/nestauk/ai_genomics/blob/ef4c1773dfdefc21d6a70d88567781e91353e129/ai_genomics/pipeline/entity_extraction/postprocessing_pipeline.py#L36)
    - [A flow that uses batch](https://github.com/nestauk/asf_daps/blob/05dcc4aebb0e1e2ce202605302d9dd65bf330e67/asf_daps/flows/processed/epc/process_epc_flow.py#L25)
    - [A flow that uses batch to train a model using GPU](https://github.com/nestauk/asf_floorplan_interpreter/blob/dev/asf_floorplan_interpreter/pipeline/train_yolo.py)
    - [A flow related to scraping web pages with batch and foreach](https://github.com/nestauk/asf_public_discourse_web_scraping/blob/dev/asf_public_discourse_web_scraping/pipeline/mse/scrape_mse.py)

## Exercises

You’ll see a `metaflow_tutorial.py` script which is a flow for processing text data (includes lemmatisation and removing stop words).
This was inspired by previous work we've done for our Understanding Public Discourse on Home Decarbonisation project. Here we're using it to process "synthetic" sustainability and heating forum text data (generated by ChatGPT)!

To run the script use the following command:

`python metaflow_tutorial.py run` (this will run the flow with the default parameters).

Learn more about how to change the parameters at the top of the script.

**Exercises:**
Change the existing code by:
- Adding in the capability of the Metaflow script to process the ‘title’ column like were processing the ‘text’ column (feel free to compare the raw and processed data afterwards);
- Add in AWS batch functionality on the steps where the most computational resources are required;
- Time how long it takes for the script to run with and without AWS batch (e.g. using `time python your_script_name.py run` to know how long it takes);
- Experiment with the `max-workers` and `max-num-splits` arguments as well as `CHUNKSIZE` when running the script to see how it affects the time it takes for the script to run;
- Save the processed data to an S3 bucket within the save data step;
    - Data should be stored in this path: `"s3://dsp-tutorials/metaflow/forum_data_category_{self.category}_YourName.csv"`
- Add in a `test` parameter that gives the script the functionality to only read in the first 100 entries and not saving the processed data when running the pipeline on test mode;
- Add a bug to one of your steps and run the script (e.g. print a variable that doesn't exist!). After it breaks, fix the issue and re-run with the `resume` command to see how it works - the flow should not run from the start - instead, it will run from the step it previously broke.