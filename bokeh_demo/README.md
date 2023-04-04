## Bokeh Demo

... will be completed ...


### How to get started
----

Clone or update repo

- ```git clone https://github.com/nestauk/dap_tutorials.git``` OR
- ```cd dap_tutorials``` and ```git pull``` 


Create and activate conda enviroment
```
conda create --name bokeh_demo --file bokeh_demo/requirements.txt
conda activate bokeh_demo
```

Prepare ipykernel

```
conda install -c anaconda ipykernel
python -m ipykernel install --user --name=bokeh_demo
```

Test whether the code runs properly

- `cd bokeh_demo/code`
- Run intro.ipynb with Jupyter notebook
- Run `python callbacks_version.py`
- Run `bokeh serve --show 03_switch_data_source.py`