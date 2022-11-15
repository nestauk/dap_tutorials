"""
Agents move around a grid.
The all have the same amount of wealth that never changes.
"""

import mesa
import random

def compute_mean_wealth(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    N = model.num_agents
    return sum(agent_wealths)/N


class Agent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = self.model.init_wealth

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move()


class BasicModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height, init_wealth):
        self.num_agents = N
        self.init_wealth = init_wealth

        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.datacollector = mesa.DataCollector(
            model_reporters={"Mean Wealth": compute_mean_wealth},
            agent_reporters={"Wealth": "wealth"}
        )
        # Create agents
        for i in range(self.num_agents):
            a = Agent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
