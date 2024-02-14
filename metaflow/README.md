
## 🛫 Metaflow have-a-go session

In this have-a-go session we will explore **Metaflow**, a framework for building and managing data pipelines.

### 🛠️ Setup

Run the following on your command line before the have-a-go session:
1. If you don't have this repo in your local computer run: `git clone https://github.com/nestauk/dap_tutorials.git`; Otherwise open this repo locally and run `git fetch origin`;
2. `cd YOUR_LOCAL_PATH/dap_tutorials/metaflow/` where `YOUR_LOCAL_PATH` is your local path to your repos' folder;
2. `conda create --name metaflow_demo python=3.9`
3. `conda activate metaflow_demo`
4. `pip install -r requirements.txt`

### 💡 This *have-a-go*

In this *have-a-go session* we will cover:
- What is Metaflow?
- When is Metaflow used? Why might you need it?
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
- When you have complex abd conflicting dependencies;
- To resume a pipeline from where it broke after you debug your code;

### ↗️ A metaflow flow & the concept of step

We call `flow` to a Metaflow pipeline. To create a `flow`:
- Create a new Python script and import the Python Metaflow library;
- Define a new flow class that inherits from the Metaflow Flow class;
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
        print('alpha is %f' % self.alpha)

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

You can define variables in Metafaflow at each step, using `self.my_variable`. However, unlike parameters, variables can only be accessed within up to the next step. Hence, the following code will raise an error:

```python
from metaflow import FlowSpec, step

class VariableFlow(FlowSpec):
    @step
    def start(self):
        self.my_variable = 1
        self.next(self.end)

    @step
    def second_step(self):
        print("second step", self.my_variable)
        self.next(self.end)
    
    @step
    def end(self):
        print("end step", self.my_variable)
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

You do horizontal scaling by paralellising a certain step (or multiple ones) in your flow. As an example, you might need to apply the same function to a large number of files or a large number of rows in a database. You can split the files/the rows into chunks and run the same function in parallel on each chunk. In addition to breaking your data into smaller chunks, you use the `foreach` argument in `self.next` as in the example below.

```python

from metaflow import FlowSpec, step

CHUNK_SIZE = 100
S3_BUCKET = "my-s3-bucket"

class MyParallelFlow(FlowSpec):

    @step
    def start(self):
        s3_path = f"s3://{S3_BUCKET}/path/to/data.parquet"
        with open(s3_path, "rb") as s3_file:
            self.data = pd.read_parquet(s3_file)

        self.next(self.prepare_chunks_of_data)

    @step
    def prepare_chunks_of_data(self):
        self.chunks = [
            self.data[i : i + CHUNKSIZE]
            for i in range(0, len(self.data) + 1, CHUNKSIZE)
        ]
        self.next(self.process_input, foreach='chunks') # note the foreach here

    @step
    def process_input(self):
        input_data = self.input

        input_data["processed_id"] = input_data["id"] * 2

        self.output_data = input_data
        self.next(self.join)

    @step
    def join(self, inputs): # note the inputs here
        import pandas as pd

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

Note that: the `join` step is not optional (you can call it whatever name you want though!). You always need to have a function calling both `self` and `inputs` after paralellising a step with `foreach`, even if the `join` step does not do anything.

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

#### 📦 Python packages to be installed
As you can also see in the flow above, we are pip installing `flow_requirements.txt`. This is a workaround to install any dependencies that are not installed by default in the AWS Batch environment. Note that this specific line will run at every step and you can then import the necessary packages at every step (instead of importing them at the top of the script, as we usually do).

#### 📁 Importing configs & util files into the flow and saving metadata to S3
All configuration and utility files you might need to import need to be in the same directory as your flow script. Additionally, make sure change `package-suffixes` when running your code to account for the different types of files being imported by your Metaflow script.
```bash
python batch_flow_script.py --package-suffixes=.txt --datastore=s3 run
```

`datastore=s3` will save the metadata of your flow to S3. This is useful to keep track of your flow's progress and to debug it if it breaks.

#### 🗄️ Saving data
Note that you cannot save data locally in batch steps, so you need to save your data to S3.

As default, you cannot save data to any S3 bucket you want. You can save it to the `open-jobs-lake` S3 bucket or ask the Data Engineering team to allow your outputs to be saved in a different S3 bucket.

### 📈 Organising your projects when using Metaflow
As mentioned above, when using AWS batch with Metaflow, you cannot import files in locations other than the folder your working on, so all the files you need to import: configs, utils, flow requirements, etc. need to be in the same folder as your flow script.

### 🔴 Common issues when using Metaflow

### 🤓 Tips for using Metaflow to scrape data

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
    
