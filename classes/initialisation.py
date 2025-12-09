from classes.homeowner_agent import Agent # type: ignore
import matplotlib.pyplot as plt


def initialise_agents():
    """
    Creates and returns 8 agents based on the game table
    Wealth = start savings
    """


    # players_data = [
    #     {"ID": "p1", "income": 35000, "max_mortgage": 110000, "start_savings": 5000,  "preferred_rating": 4},
    #     {"ID": "p2", "income": 50000, "max_mortgage": 170000, "start_savings": 30000, "preferred_rating": 6},
    #     {"ID": "p3", "income": 30000, "max_mortgage": 80000,  "start_savings": 0,     "preferred_rating": 3},
    #     {"ID": "p4", "income": 40000, "max_mortgage": 130000, "start_savings": 15000, "preferred_rating": 5},
    #     {"ID": "p5", "income": 45000, "max_mortgage": 200000, "start_savings": 50000, "preferred_rating": 7},
    #     {"ID": "p6", "income": 75000, "max_mortgage": 300000, "start_savings": 80000, "preferred_rating": 8},
    #     {"ID": "p7", "income": 50000, "max_mortgage": 170000, "start_savings": 30000, "preferred_rating": 6},
    #     {"ID": "p8", "income": 50000, "max_mortgage": 170000, "start_savings": 30000, "preferred_rating": 6},
    # ]

    # TEST 1 player
    players_data = [
        {"ID": "p1", "income": 35000, "max_mortgage": 110000, "start_savings": 5000,  "preferred_rating": 4}
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

import matplotlib.pyplot as plt
import numpy as np

# Test grafieken, gemaakt met ai
def plot_satisfaction_over_time(agents, rounds=4):
    """
    Cleaner, more readable multi-agent satisfaction plot.
    Legend outside, soft colors, thin lines, and integer axes.
    """
    if not agents:
        print("No agents to plot.")
        return

    plt.figure(figsize=(12, 6))

    # Colormap for distinct soft colors
    colors = plt.cm.tab10(np.linspace(0, 1, len(agents)))

    for idx, agent in enumerate(agents):
        history = getattr(agent, "satisfaction_history", None)
        if history is None:
            print(f"Warning: Agent {agent.ID} has no satisfaction_history attribute.")
            continue

        plt.plot(
            range(1, len(history) + 1),
            history,
            label=f"Agent {agent.ID}",
            color=colors[idx],
            linewidth=2,
            marker='o',
            markersize=6,
            markeredgecolor='black',
            alpha=0.85
        )

    # X-axis ticks: rounds
    plt.xticks(ticks=list(range(1, rounds + 1)))

    # Y-axis ticks: only integer satisfaction values
    all_values = [val for a in agents for val in getattr(a, "satisfaction_history", [])]
    if all_values:
        ymin, ymax = int(min(all_values)), int(max(all_values))
        plt.yticks(ticks=list(range(ymin, ymax + 1)))

    # Title & labels
    plt.title("Satisfaction development over time", fontsize=16)
    plt.xlabel("Round", fontsize=14)
    plt.ylabel("Satisfaction (points)", fontsize=14)

    # Soft background grid
    plt.grid(True, alpha=0.25)

    # Legend OUTSIDE plot for clarity
    plt.legend(loc='center left', bbox_to_anchor=(1.03, 0.5), fontsize=11)

    plt.tight_layout()
    plt.show()

def plot_floods_per_round(agents):
    """
    Plots, for each round, how many agents experienced flood damage.
    Uses agents' damage_history instead of a separate flood_history.
    """

    if not agents:
        print("No agents to plot.")
        return

    # Determine how many rounds there are (max length over all damage_histories)
    num_rounds = max(len(a.damage_history) for a in agents if hasattr(a, "damage_history"))

    flooded_counts = []
    total_costs = []

    for r in range(num_rounds):
        flooded_this_round = 0
        cost_this_round = 0.0

        for a in agents:
            if len(a.damage_history) > r:
                entry = a.damage_history[r]
                if entry["damage_cost"] > 0:
                    flooded_this_round += 1
                    cost_this_round += entry["damage_cost"]

        flooded_counts.append(flooded_this_round)
        total_costs.append(cost_this_round)

    rounds = list(range(1, num_rounds + 1))

    plt.figure(figsize=(8, 5))
    plt.bar(rounds, flooded_counts)
    plt.xticks(rounds)

    plt.title("Number of flooded agents per round")
    plt.xlabel("Round")
    plt.ylabel("Number of agents with flood damage")

    plt.tight_layout()
    plt.show()