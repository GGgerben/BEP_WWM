from classes.homeowner_agent import Agent # type: ignore
import matplotlib.pyplot as plt
import numpy as np
import random
import re
from collections import Counter


def initialise_agents():
    """
    Create the baseline population of 8 household agents.

    This function reproduces the fixed player archetypes from the
    WhereWeMove serious game, including income, savings, mortgage
    constraints and housing preferences.

    Returns:
        list[Agent]: List of 8 predefined household agents.
    """

    players_data = [
        {"ID": "p1", "income": 35000, "max_mortgage": 110000, "start_savings": 5000,  "preferred_rating": 4},
        {"ID": "p2", "income": 50000, "max_mortgage": 170000, "start_savings": 30000, "preferred_rating": 6},
        {"ID": "p3", "income": 30000, "max_mortgage": 80000,  "start_savings": 0,     "preferred_rating": 3},
        {"ID": "p4", "income": 40000, "max_mortgage": 130000, "start_savings": 15000, "preferred_rating": 5},
        {"ID": "p5", "income": 45000, "max_mortgage": 200000, "start_savings": 50000, "preferred_rating": 7},
        {"ID": "p6", "income": 75000, "max_mortgage": 300000, "start_savings": 80000, "preferred_rating": 8},
        {"ID": "p7", "income": 50000, "max_mortgage": 170000, "start_savings": 30000, "preferred_rating": 6},
        {"ID": "p8", "income": 50000, "max_mortgage": 170000, "start_savings": 30000, "preferred_rating": 6},
    ]

    agents = []

    for p in players_data:
        agent = Agent(
            ID=p["ID"],
            wealth=p["start_savings"],   # wealth = start savings
            income=p["income"],
            experience_level="Nooit",
            self_efficacy=0.5,
            house=None
        )

        agent.max_mortgage = p["max_mortgage"]
        agent.preferred_rating = p["preferred_rating"]

        agents.append(agent)

    return agents

def initialise_agents_n(n=1000, seed=42):
    """
    Create a heterogeneous population of household agents.

    This function generates a larger agent population for
    large-scale simulations by sampling income, savings,
    mortgage capacity and housing preferences from
    predefined distributions.

    Args:
        n (int): Number of agents to generate.
        seed (int): Random seed for reproducibility.

    Returns:
        list[Agent]: List of n heterogeneous household agents.
    """

    random.seed(seed)

    agents = []
    for i in range(1, n + 1):
        income = random.choice([30000, 35000, 40000, 45000, 50000, 75000])
        start_savings = random.choice([0, 2000, 5000, 15000, 30000, 50000, 80000])
        max_mortgage = random.choice([80000, 110000, 130000, 170000, 200000, 300000])
        preferred_rating = random.randint(3, 8)

        agent = Agent(
            ID=f"a{i}",
            wealth=float(start_savings),
            income=float(income),
            experience_level="Nooit",
            self_efficacy=0.5,
            house=None
        )

        agent.max_mortgage = float(max_mortgage)
        agent.preferred_rating = int(preferred_rating)

        agents.append(agent)

    return agents


