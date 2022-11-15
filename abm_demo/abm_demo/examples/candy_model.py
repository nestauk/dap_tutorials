"""
This is adapted from https://mesa.readthedocs.io/en/main/tutorials/intro_tutorial.html

A simple model of an economy where agents exchange resources ("candy") at random. Some agents
are selfish and won't give away their candy, others are sharers and will.

We calculate the Gini coefficient for inequality (of wealth) along the way.

Initial conditions:

- Agents all have init_candy units of candy.
- The probability an agent will initial share candy is init_sharer_prop - this is it's 'strategy'

Steps:

- All agents move randomly to a neighbouring location
- If the agent is a sharer it will exchange one unit of candy with a randomly selected neighbour
- If the agent isn't a sharer it won't exhange any candy, but will recieve it
- All agents switch strategies to whichever of it's neighbours has the most candy
- According to the probability mutation_rate an agent may randomly change it's strategy

Terms:

"Strategy": whether the agent is a sharer or not a sharer
"Wealth": the number of candy units an agent has


"""

import mesa
import random

def compute_gini(model):
    """
    0: equality
    1: inequality
    """
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B

def proportion_sharers(model):
    agent_strats = [agent.sharer for agent in model.schedule.agents]
    return sum(agent_strats)/len(agent_strats)

class Agent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, sharer, model):
        super().__init__(unique_id, model)
        self.wealth = self.model.init_candy
        self.sharer = sharer

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_candy(self):
        if self.sharer:
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            if len(cellmates) > 1:
                other_agent = self.random.choice(cellmates)
                other_agent.wealth += 1
                self.wealth -= 1

    def copy_strategy(self):
        """
        Copy sharer or not strategy from most wealthy around you
        """
        neighbours = self.model.grid.get_neighbors(self.pos, moore=True)
        if len(neighbours) > 1 :
            sorted_neighbours = sorted(
                [(agent.wealth, agent.sharer) for agent in neighbours],
                key=lambda x: x[0], reverse=True)
            best_neighbour_strat = sorted_neighbours[0][1]
            self.sharer = best_neighbour_strat

    def mutate(self):
        if random.uniform(0, 1) < self.model.mutation_rate:
            self.sharer = random.choice([True, False])

    def step(self):
        self.move()
        if self.wealth > 0:
            self.give_candy()
            self.copy_strategy()
            self.mutate()


class CandyModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height, init_candy, init_sharer_prop=1, mutation_rate=0):
        self.num_agents = N
        self.init_candy = init_candy
        self.init_sharer_prop = init_sharer_prop
        self.mutation_rate = mutation_rate

        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": compute_gini, "proportion_sharers" :proportion_sharers},
            agent_reporters={"Wealth": "wealth", "Sharer": "sharer"}
        )
        # Create agents
        for i in range(self.num_agents):
            if random.uniform(0, 1) <= self.init_sharer_prop:
                sharer = True
            else:
                sharer = False
            a = Agent(i, sharer, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
