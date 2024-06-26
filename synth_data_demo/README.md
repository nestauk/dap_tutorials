# Synthetic data have-a-go - set up


Clone/ update the dap_tutorials repo


Brew install 'ninja' and restart your terminal:

```
brew install ninja
```

After restarting your terminal, cd into the folder synth_data_demo

Create a conda environment:

```
conda create -n synth_data_demo python=3.8 
```

Activate the conda environment:

```
conda activate synth_data_demo
```

Install pip:

```
conda install pip
```

Install requirements:

```
pip install -r requirements.txt
```

Create an ipykernel: 

```
python -m ipykernel install --user --name=synth_data_demo
```

We'll use the notebook 'synth_data_demo.ipynb' for the session. 