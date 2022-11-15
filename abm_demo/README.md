# Agent-Based Modelling Demo

A demo of agent-based modelling using Mesa in Python.

To begin:

Run
```
make install
conda activate abm_demo
```

## Example models

Try out the visualisations of a basic model and a more complicated model (these are both based off [Mesa's money model example](https://mesa.readthedocs.io/en/main/tutorials/intro_tutorial.html)).

### Basic model

Watch as `N` agents move randomly around a `width` x `height` grid.

```
python abm_demo/examples/basic_model_visualisation.py --N 20 --width 10 --height 10
```

![The first two iterations of a run of the basic model example](basic_model.png)

### Candy model

Watch as agents move randomly around a grid whilst sharing candy with each other or not (based off [Mesa's money model example](https://mesa.readthedocs.io/en/main/tutorials/intro_tutorial.html)):

```
python abm_demo/examples/candy_model_visualisation.py --N 20 --width 10 --height 10 --init_candy 1 --init_sharer_prop 0.9 --mutation_rate 0.01 
```

Initial conditions to modify:
- `init_candy` - the number of pieces of candy given to every agent initially.
- `init_sharer_prop` - the proportion of agents who are sharers initially.

Plots of the Gini coefficient and the number of sharer agents at a given time step are also given.

### Candy parameter exploration

Open up the notebook `abm_demo/analysis/Trick or Treat.ipynb` to experiment with parameter combinations and model outcomes.
