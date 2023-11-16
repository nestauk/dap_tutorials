# Quarto demonstration

In this have-a-go session we will go through how to create a quarto document.

## 🛠️ To do *before* the have-a-go session
Please follow these instructions to make sure you are ready to start the session. To start, you will need to download the [Quarto CLI](https://quarto.org/docs/get-started/). Then follow the instructions below.

### Code set up 
Open your terminal and complete the following instructions:
1. **Clone this repo:** 

`git clone https://github.com/nestauk/dap_tutorials.git`

2. **Navigate to this tutorial's folder:** 
Navigate to your repos folder (the folder where you store all your local GitHub repositories) and then do:

`cd dap_tutorials`

`cd quarto_demo`

3. **Create your conda environment:** 

`conda create --name quarto_demo python=3.9`


4. **Activate your conda environment:** 

`conda activate quarto_demo`

5. **Install package dependencies:** 

`pip install -r requirements.txt`

8. **Open the quarto_basics.qmd document inside the quarto folder** 

If you use VS Code, you can install the Quarto extension. This will allow you some extra functionality such as previewing your document in VS code. 
This is sometimes a little buggy, so alternatively you can preview your document in your browser.

To do preview or render your document in your browser, you can use the following make commands:

To save as html: 

`report=quarto_basics make render-quarto`

To preview in your browser:

`report=quarto_basics make preview-quarto`


## 🤓 Tutorial 
This have-a-go session will start with a brief introduction to some Quarto basics as well as a demo on some of the interesting visualisations you can include in your quarto document.