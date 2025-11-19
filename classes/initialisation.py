from classes.homeowner_agent import Agent # type: ignore

def initialise_agents():
    """
    Creates and returns 8 agents based on the game table.
    Wealth = start savings.
    Living costs and start debt are ignored.
    """

    players_data = [
        {"ID": "p1", "income": 75000,  "max_mortgage": 110000, "start_savings": 5000,  "preferred_rating": 4},
        {"ID": "p2", "income": 110000, "max_mortgage": 170000, "start_savings": 30000, "preferred_rating": 6},
        {"ID": "p3", "income": 60000,  "max_mortgage": 80000,  "start_savings": 0,     "preferred_rating": 3},
        {"ID": "p4", "income": 90000,  "max_mortgage": 130000, "start_savings": 15000, "preferred_rating": 5},
        {"ID": "p5", "income": 130000, "max_mortgage": 200000, "start_savings": 50000, "preferred_rating": 7},
        {"ID": "p6", "income": 190000, "max_mortgage": 300000, "start_savings": 80000, "preferred_rating": 8},
        {"ID": "p7", "income": 110000, "max_mortgage": 170000, "start_savings": 30000, "preferred_rating": 6},
        {"ID": "p8", "income": 110000, "max_mortgage": 170000, "start_savings": 30000, "preferred_rating": 6},
    ]

    agents = []

    for p in players_data:
        agent = Agent(
            ID=p["ID"],
            wealth=p["start_savings"],   # wealth = start savings
            income=p["income"],
            risk_perception=0.5,
            experience_level="Nooit",
            self_efficacy=0.5,
            outcome_efficacy=0.5,
            intention=0.5,
            house=None
        )

        agent.max_mortgage = p["max_mortgage"]
        agent.preferred_rating = p["preferred_rating"]

        agents.append(agent)

    return agents