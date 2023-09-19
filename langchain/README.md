# 💅 LLM tutorials

This directory contains tutorials related to langchain. It primarily focuses on the practicalities of building LLM applications. Currently, there is one tutorial to follow along with: 

1. `basics_of_langchain.ipynb` - This tutorial introduces the basics of LangChain and how to use the library to build LLM applications. It covers prompts, chains, agents and Retrieval Augmented Generation (RAG). There are **🛸 TASK** to complete along the way.

## 🎓 Get Started

Create a conda environment and install `taltech-utils` library:

```
conda create --name langchain_tutorial python=3.9
conda activate langchain_tutorial
pip install git+https://github.com/nestauk/dap_taltech.git #install the utils library from the TalTech hackweek - we will use data from this library. 
python -m ipykernel install --user --name=langchain_tutorial #add the conda environment to jupyter notebook
```
```

Then, navigate to the tutorial and follow the instructions and code blocks.