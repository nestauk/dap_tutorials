# Reinforcement Learning: the TL;DR 

## What is it?

It's a type of machine learning where one or more agents learn how to behave (what actions to take) in an environment by performing actions and seeing the results. 

**Reward hypothesis:** all goals/strategies can be summarised as the maximisation of the expected return (cumulative reward)

**Markov property:** agent is focused on present information, not historical states and actions

**Reinforcement learning vs deep reinforcement learning:** an agent comes up with the best action to ‘maximise rewards’ and stores that information (the knowledge space) vs a deep neural network that predicts rewards given some input variables  

## So what?

Reinforcement learning could be helpful because...

* ...At Nesta, we may want to simulate how individuals interact with society so we can simulate coordination/collaboration issues. Helpful for policy design. 

## Libraries 

* `gym` - to develop and compare reinforcement learning algos. Also helpful for environment generation and rendering.
* `Stable_Baselines3` - implement reinforcement learning algos in PyTorch. Also has integration with other tools including Hugging Face. 
* `Baselines3 Zoo` - great library for training and evaluating RL agents

## Links

Link to [reinforcement learning deck](https://docs.google.com/presentation/d/14fKcgw7aGXNNDX9-ho0CnmOZ60FbsTHGC2iufXQaXLk/edit?usp=sharing).