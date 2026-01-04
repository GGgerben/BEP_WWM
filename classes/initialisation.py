from classes.homeowner_agent import Agent # type: ignore
import matplotlib.pyplot as plt
import numpy as np
import random
import re
from collections import Counter


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
    Create n agents with heterogeneous properties.
    Uses simple distributions (you can later match these to your game / data).
    """
    random.seed(seed)

    agents = []
    for i in range(1, n + 1):
        # Example heterogeneity (edit as needed)
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
    Stacked bar chart of insurance usage per round:
    - bottom: first-time purchases
    - top: repeat purchases
    """

    # Dictionaries per round
    first_time = {}
    repeat = {}

    for agent in agents:
        insurance_rounds = [
            round_nr
            for (measure, round_nr) in agent.adopted_measures
            if measure.name == insurance_name
        ]

        # Sort rounds just to be safe
        insurance_rounds.sort()

        for i, r in enumerate(insurance_rounds):
            if i == 0:
                first_time[r] = first_time.get(r, 0) + 1
            else:
                repeat[r] = repeat.get(r, 0) + 1

    # All rounds where insurance was bought
    all_rounds = sorted(set(first_time.keys()) | set(repeat.keys()))

    first_counts = [first_time.get(r, 0) for r in all_rounds]
    repeat_counts = [repeat.get(r, 0) for r in all_rounds]

    plt.figure(figsize=(8, 5))

    plt.bar(
        all_rounds,
        first_counts,
        label="First-time purchase"
    )
    plt.bar(
        all_rounds,
        repeat_counts,
        bottom=first_counts,
        label="Repeat purchase"
    )

    plt.title("Flood insurance purchases per round")
    plt.xlabel("Round")
    plt.ylabel("Number of purchases")
    plt.xticks(all_rounds)
    plt.legend()
    plt.grid(axis="y", alpha=0.3)

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

def plot_total_new_measures_per_round(agents):
    """
    Plots the total number of newly adopted measures per round
    (summed over all agents).
    """

    if not agents:
        print("No agents to plot.")
        return

    purchases_per_round = {}

    # Count all adopted measures per round
    for agent in agents:
        for measure, round_nr in agent.adopted_measures:
            purchases_per_round[round_nr] = purchases_per_round.get(round_nr, 0) + 1

    if not purchases_per_round:
        print("No measures were adopted.")
        return

    # Sort rounds
    rounds = sorted(purchases_per_round.keys())
    counts = [purchases_per_round[r] for r in rounds]

    # Plot
    plt.figure(figsize=(8, 5))
    plt.bar(rounds, counts)

    plt.title("Total number of new measures adopted per round")
    plt.xlabel("Round")
    plt.ylabel("Number of new measures")

    plt.xticks(rounds)
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.show()

def plot_housing(history):
    r = history["round"]
    plt.figure()
    plt.plot(r, history["available"], marker="o", label="Available houses")
    plt.plot(r, history["unhoused"], marker="o", label="Unhoused agents")
    plt.xlabel("Round")
    plt.ylabel("Count")
    plt.title("Housing dynamics")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_macro_satisfaction(history):
    r = history["round"]
    y = history["avg_satisfaction"]

    ymin = min(y)
    ymax = max(y)
    margin = 0.1 * (ymax - ymin + 1)

    plt.figure()
    plt.plot(r, y, marker="o", linewidth=2)
    plt.xlabel("Round")
    plt.ylabel("Average satisfaction")
    plt.title("Average satisfaction over time")

    plt.ylim(ymin - margin, ymax + margin)

    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_policy_adoption(history, rounds=(1,2,3,4)):
    r = history["round"]
    plt.figure()
    plt.bar(r, history["new_measures"])
    plt.xticks(rounds)
    plt.xlabel("Round")
    plt.ylabel("New measures adopted (count)")
    plt.title("Measure adoption per round")
    plt.tight_layout()
    plt.show()

def plot_satisfaction_distribution(history):
    r = history["round"]
    mean = history["avg_satisfaction"]
    p10 = history["sat_p10"]
    p50 = history["sat_p50"]
    p90 = history["sat_p90"]

    ymin = min(p10 + mean)  # band onderkant of mean, wat lager is
    ymax = max(p90 + mean)
    
    plt.figure()
    plt.fill_between(r, p10, p90, alpha=0.2, label="P10–P90 band")
    plt.plot(r, p50, marker="o", linewidth=2, label="Median (P50)")
    plt.plot(r, mean, marker="o", linewidth=2, label="Mean")
    plt.axhline(0, linestyle="--", linewidth=1)

    plt.xlabel("Round")
    plt.ylabel("Satisfaction")
    plt.title("Satisfaction distribution over time (1000 agents)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

