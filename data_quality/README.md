# Data Profiling and Data Quality with YData-Profiling and Great Expectations

In this have-a-go session we will explore two Python packages, **YData-Profiling** and **Great Expectations**. These are super useful for quickly inspecting new data, performing exploratory data analysis, data profiling, checking if new data batches you receive from partners/collect from APIs behave as expected and for automating data quality checks.

## 🛠️ To do *before* the have-a-go session
Please follow the instructions below prior to the have-a-go session.

Open your terminal and follow the instructions. Shouldn't take longer than 5 minutes:
1. **Clone this repo:** 

`git clone https://github.com/nestauk/dap_tutorials.git`

2. **Navigate to this tutorial's folder:** 
Navigate to your repos folder (the folder where you store all your local GitHub repositories) and then do:

`cd dap_tutorials/data_quality/`

3. **Create your conda environment:** 

`conda create --name data_quality python=3.9`

(If you do not have conda installed/do not want to install it, just ignore steps 3, 4 and 7)

4. **Activate your conda environment:** 

`conda activate data_quality`

5. **Install package dependencies:** 

`pip install -r requirements.txt`

6. **Add your conda environment to the notebooks:** 

`python -m ipykernel install --user --name=data_quality`

7. **Open the first notebook and make sure you have the correct kernel selected** 

Launch `jupyter-notebook` and open notebook "01. Your first Twitter API request" make sure your kernel is the right environment, `data_quality`. Run the notebook to check if the previous setup worked for you. If all runs fine, then you're prepared for the session!

(If you do not have conda installed/do not want to install it, just use your standard Python environment)

## Data
We use slightly altered versions of the [Titanic dataset](https://github.com/adamerose/datasets/blob/master/titanic.csv) and the [Heart Failure Prediction dataset](https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction) for the purpose of this tutorial.

## 🤓 Tutorial 
This have-a-go session will start with an introduction two the two Python packages followed by a set of exercises.