# Weights and biases

## Setup

### Environment
Create a conda environment:
```
conda create -n wandb_demo python=3.10   
```

Activate the environment:
```
conda activate wandb_demo
```

Install pip:
```
conda install pip
```
Install requirements:
```
pip install -r requirements.txt
```

Create an ipykernel for your conda environment:
```
python -m ipykernel install --user --name=wandb_demo
```

### Set up weights and biases

### Download data
Download titanic data from Kaggle and store it in `wandb/inputs/`.
