from classes.homeowner_agent import Agent # type: ignore
import matplotlib.pyplot as plt


def initialise_agents():
    """
    Creates and returns 8 agents based on the game table
    Wealth = start savings
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

    # TEST 1 player
    # players_data = [
    #     {"ID": "p1", "income": 35000, "max_mortgage": 110000, "start_savings": 5000,  "preferred_rating": 4}
    # ]

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
    Satisfaction plot with a fixed starting point of 5 at round 0 for all agents.
    """
    if not agents:
        print("No agents to plot.")
        return

    plt.figure(figsize=(12, 6))

    # Color palette
    colors = plt.cm.tab10(np.linspace(0, 1, len(agents)))

    for idx, agent in enumerate(agents):
        history = getattr(agent, "satisfaction_history", None)
        if history is None:
            print(f"Warning: Agent {agent.ID} has no satisfaction_history attribute.")
            continue

        # 👉 Add fixed starting satisfaction point = 5 at round 0
        extended_history = [5] + history

        plt.plot(
            range(0, len(extended_history)),
            extended_history,
            label=f"Agent {agent.ID}",
            color=colors[idx],
            linewidth=2,
            marker='o',
            markersize=6,
            markeredgecolor='black',
            alpha=0.85
        )

    # X-axis ticks (starting at 0)
    plt.xticks(ticks=list(range(0, rounds + 1)))

    # Y-axis ticks: integer values
    all_values = [val for a in agents for val in getattr(a, "satisfaction_history", [])]
    all_values += [5]  # ensure 5 is included
    ymin, ymax = int(min(all_values)), int(max(all_values))
    plt.yticks(ticks=list(range(ymin, ymax + 1)))

    plt.title("Satisfaction development over time", fontsize=16)
    plt.xlabel("Round", fontsize=14)
    plt.ylabel("Satisfaction (points)", fontsize=14)

    plt.grid(True, alpha=0.25)
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

def plot_subsidy_effect(agents, subsidized_measure_name):
    """
    Plots how often the subsidized measure is purchased per round.
    agents: list of Agent objects
    subsidized_measure_name: string, name of the measure with subsidy
    """

    # Dictionary to count purchases per round
    purchases_per_round = {}

    # Loop through all agents and their adopted measures
    for agent in agents:
        for measure, round_nr in agent.adopted_measures:
            if measure.name == subsidized_measure_name:
                purchases_per_round[round_nr] = purchases_per_round.get(round_nr, 0) + 1

    # Convert to sorted lists
    rounds = sorted(purchases_per_round.keys())
    counts = [purchases_per_round[r] for r in rounds]

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(rounds, counts, marker='o', linewidth=2)

    plt.title(f"Purchases of subsidized measure: '{subsidized_measure_name}'")
    plt.xlabel("Round")
    plt.ylabel("Number of purchases")
    plt.grid(True)

    plt.xticks(rounds)  # show only rounds where something happened
    plt.tight_layout()
    plt.show()

def plot_measures_heatmap(agents):
    """
    Maakt een heatmap:
    - x-as: rondes
    - y-as: measures
    - kleur: aantal aankopen
    Verwacht dat agent.adopted_measures een lijst is van (measure, round_nr).
    """

    # Alle (measure_name, round_nr) verzamelen
    purchases = []
    for agent in agents:
        for measure, round_nr in agent.adopted_measures:
            purchases.append((measure.name, round_nr))

    if not purchases:
        print("No measures were purchased, nothing to plot.")
        return

    # Unieke rondes en measures
    all_rounds = sorted({r for (_, r) in purchases})
    all_measure_names = sorted({name for (name, _) in purchases})

    round_index = {r: i for i, r in enumerate(all_rounds)}
    measure_index = {name: i for i, name in enumerate(all_measure_names)}

    # Matrix [n_measures x n_rounds]
    data = np.zeros((len(all_measure_names), len(all_rounds)), dtype=int)

    for name, r in purchases:
        i = measure_index[name]
        j = round_index[r]
        data[i, j] += 1

    plt.figure(figsize=(10, 6))
    im = plt.imshow(data, aspect="auto")

    # As-labels
    plt.xticks(ticks=range(len(all_rounds)), labels=all_rounds)
    plt.yticks(ticks=range(len(all_measure_names)), labels=all_measure_names)

    plt.xlabel("Round")
    plt.ylabel("Measure")
    plt.title("Number of purchases per measure per round")

    # Kleurbar
    cbar = plt.colorbar(im)
    cbar.set_label("Number of purchases")

    # Optioneel: waarden in de vakjes schrijven
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            val = data[i, j]
            if val > 0:
                plt.text(j, i, str(val),
                         ha="center", va="center", fontsize=8, color="white")

    plt.tight_layout()
    plt.show()

def plot_insurance_usage(agents, insurance_name="Flood insurance"):
    """
    Plot how often the insurance measure is purchased per round.
    
    - x-axis: round
    - y-axis: number of Flood insurance purchases
    """

    # Collect (round_nr) for each time insurance is bought
    purchases_per_round = {}

    for agent in agents:
        for measure, round_nr in agent.adopted_measures:
            if measure.name == insurance_name:
                purchases_per_round[round_nr] = purchases_per_round.get(round_nr, 0) + 1

    if not purchases_per_round:
        print(f"No purchases found for measure '{insurance_name}'.")
        return

    # Sort rounds and get counts
    rounds = sorted(purchases_per_round.keys())
    counts = [purchases_per_round[r] for r in rounds]

    plt.figure(figsize=(8, 5))
    plt.plot(rounds, counts, marker="o", linewidth=2)

    plt.title(f"Purchases of '{insurance_name}' per round")
    plt.xlabel("Round")
    plt.ylabel("Number of purchases")
    plt.grid(True, alpha=0.3)
    plt.xticks(rounds)

    plt.tight_layout()
    plt.show()

def plot_subsidy_effect_summary(agents, measures, subsidized_measure_name):
    """
    Bar chart: for each measure, how many agents bought it at least once.
    The subsidized measure is highlighted in a different color.
    """

    # Voor elke measure: set van agent IDs die deze measure ooit kochten
    adopters_per_measure = {m.name: set() for m in measures}

    for agent in agents:
        for measure, round_nr in agent.adopted_measures:
            adopters_per_measure[measure.name].add(agent.ID)

    measure_names = [m.name for m in measures]
    counts = [len(adopters_per_measure[name]) for name in measure_names]

    # Kleur: gesubsidieerde measure valt op
    colors = [
        "tab:orange" if name == subsidized_measure_name else "tab:blue"
        for name in measure_names
    ]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(range(len(measure_names)), counts, color=colors)

    # Namen onder de x-as
    plt.xticks(range(len(measure_names)), measure_names, rotation=45, ha="right")

    # Waarden boven de balken
    for x, c in zip(range(len(measure_names)), counts):
        plt.text(x, c + 0.05, str(c), ha="center", va="bottom", fontsize=9)

    plt.title("Number of agents that bought each measure (subsidy highlighted)")
    plt.xlabel("Measure")
    plt.ylabel("Number of agents (bought at least once)")
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.show()
