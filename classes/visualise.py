"""
Plotting utilities for the WhereWeMove Agent-Based Model.

These visualisation functions were initially drafted with the assistance
of ChatGPT and adapted to analyse simulation outputs related to
household satisfaction, flood impacts, and policy-driven adaptation behaviour.
"""

import matplotlib.pyplot as plt
import numpy as np
import random
import re
import pandas as pd


def plot_satisfaction_over_time(agents, rounds=4):
    """
    Plot satisfaction trajectories per agent over simulation rounds.

    Assumes a fixed initial satisfaction of 5 at round 0 and
    uses each agent's satisfaction_history.
    """
    if not agents:
        print("No agents to plot.")
        return

    plt.figure(figsize=(12, 6))

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
    plt.xticks(ticks=list(range(0, rounds + 1)))

    all_values = [val for a in agents for val in getattr(a, "satisfaction_history", [])]
    all_values += [5] 
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
    Plot the number of agents experiencing flood damage per round.

    Uses each agent's damage_history to identify flood events.
    """

    if not agents:
        print("No agents to plot.")
        return

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

def plot_measures_heatmap(agents):
    """
    Plot a heatmap showing how often each measure is adopted per round.

    Rows represent measures, columns represent rounds, and values indicate
    the number of adoptions.
    """

    purchases = []
    for agent in agents:
        for measure, round_nr in agent.adopted_measures:
            purchases.append((measure.name, round_nr))

    if not purchases:
        print("No measures were purchased, nothing to plot.")
        return


    all_rounds = sorted({r for (_, r) in purchases})
    all_measure_names = sorted({name for (name, _) in purchases})

    round_index = {r: i for i, r in enumerate(all_rounds)}
    measure_index = {name: i for i, name in enumerate(all_measure_names)}

    data = np.zeros((len(all_measure_names), len(all_rounds)), dtype=int)

    for name, r in purchases:
        i = measure_index[name]
        j = round_index[r]
        data[i, j] += 1

    plt.figure(figsize=(10, 6))
    im = plt.imshow(data, aspect="auto")

    plt.xticks(ticks=range(len(all_rounds)), labels=all_rounds)
    plt.yticks(ticks=range(len(all_measure_names)), labels=all_measure_names)
    plt.xlabel("Round")
    plt.ylabel("Measure")
    plt.title("Number of purchases per measure per round")

    cbar = plt.colorbar(im)
    cbar.set_label("Number of purchases")

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
    Plot first-time versus repeat insurance purchases per round.

    Distinguishes between initial adoption and renewals of flood insurance.
    """

    first_time = {}
    repeat = {}

    for agent in agents:
        insurance_rounds = [
            round_nr
            for (measure, round_nr) in agent.adopted_measures
            if measure.name == insurance_name
        ]

        insurance_rounds.sort()

        for i, r in enumerate(insurance_rounds):
            if i == 0:
                first_time[r] = first_time.get(r, 0) + 1
            else:
                repeat[r] = repeat.get(r, 0) + 1

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
    Plot how many agents adopted each measure at least once.

    Highlights the subsidised measure to visualise substitution effects.
    """

    adopters_per_measure = {m.name: set() for m in measures}

    for agent in agents:
        for measure, round_nr in agent.adopted_measures:
            adopters_per_measure[measure.name].add(agent.ID)

    measure_names = [m.name for m in measures]
    counts = [len(adopters_per_measure[name]) for name in measure_names]

    colors = [
        "tab:orange" if name == subsidized_measure_name else "tab:blue"
        for name in measure_names
    ]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(range(len(measure_names)), counts, color=colors)

    plt.xticks(range(len(measure_names)), measure_names, rotation=45, ha="right")

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
    Plot the total number of newly adopted measures per round.
    """

    if not agents:
        print("No agents to plot.")
        return

    purchases_per_round = {}

    for agent in agents:
        for measure, round_nr in agent.adopted_measures:
            purchases_per_round[round_nr] = purchases_per_round.get(round_nr, 0) + 1

    if not purchases_per_round:
        print("No measures were adopted.")
        return

    rounds = sorted(purchases_per_round.keys())
    counts = [purchases_per_round[r] for r in rounds]

    plt.figure(figsize=(8, 5))
    plt.bar(rounds, counts)
    plt.title("Total number of new measures adopted per round")
    plt.xlabel("Round")
    plt.ylabel("Number of new measures")
    plt.xticks(rounds)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()

def _to_df(history):
    """
    Convert history input to a pandas DataFrame if needed.
    """

    return history if isinstance(history, pd.DataFrame) else pd.DataFrame(history)

def _macro_by_round(history_df):
    """
    Aggregate agent-level satisfaction data to macro statistics per round.
    """

    g = history_df.groupby("round")["satisfaction"]
    macro = pd.DataFrame({
        "round": g.mean().index,
        "avg_satisfaction": g.mean().values,
        "sat_p10": g.quantile(0.10).values,
        "sat_p50": g.quantile(0.50).values,
        "sat_p90": g.quantile(0.90).values,
        "n_agents": g.size().values
    })
    return macro.sort_values("round")

def plot_macro_satisfaction(history):
    """
    Plot average satisfaction per round at the system level.
    """

    df = _to_df(history)
    macro = _macro_by_round(df)

    r = macro["round"].tolist()
    y = macro["avg_satisfaction"].tolist()

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

def plot_satisfaction_distribution(history):
    """
    Plot the distribution of satisfaction over time using percentiles.
    """

    df = _to_df(history)
    macro = _macro_by_round(df)

    r = macro["round"].tolist()
    mean = macro["avg_satisfaction"].tolist()
    p10 = macro["sat_p10"].tolist()
    p50 = macro["sat_p50"].tolist()
    p90 = macro["sat_p90"].tolist()

    plt.figure()
    plt.fill_between(r, p10, p90, alpha=0.2, label="P10–P90 band")
    plt.plot(r, p50, marker="o", linewidth=2, label="Median (P50)")
    plt.plot(r, mean, marker="o", linewidth=2, label="Mean")
    plt.axhline(0, linestyle="--", linewidth=1)

    plt.xlabel("Round")
    plt.ylabel("Satisfaction")
    plt.title("Satisfaction distribution over time")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_adoption_over_time(history):
    """
    Plot the number of agents adopting at least one measure per round.
    """

    df = _to_df(history)

    adoption = (
        df.assign(adopted=df["new_measures"].fillna("") != "")
          .groupby("round")["adopted"]
          .sum()
    )

    plt.figure(figsize=(8, 5))
    plt.plot(adoption.index, adoption.values, marker="o", linewidth=2)

    plt.xlabel("Round")
    plt.ylabel("Number of agents adopting a measure")
    plt.title("Adoption of flood measures over time")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_measure_adoption_summary(history):
    """
    Plot how many agents adopted each measure at least once.
    """

    df = _to_df(history)

    exploded = (
        df[["agent_id", "measures"]]
        .dropna()
        .assign(measure=df["measures"].str.split(";"))
        .explode("measure")
    )

    exploded = exploded[exploded["measure"] != ""]

    counts = exploded.groupby("measure")["agent_id"].nunique().sort_values()

    plt.figure(figsize=(10, 5))
    counts.plot(kind="bar")

    plt.ylabel("Number of agents (ever adopted)")
    plt.title("Adoption per flood measure")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_insurance_repeats(history, insurance_name="Flood insurance"):
    """
    Plot first-time and repeat insurance purchases using aggregated history data.
    """
    df = _to_df(history)

    df = df[df["new_measures"].fillna("").str.contains(insurance_name)]

    first = {}
    repeat = {}
    seen = {}

    for _, row in df.iterrows():
        agent = row["agent_id"]
        r = row["round"]

        seen.setdefault(agent, 0)
        first.setdefault(r, 0)
        repeat.setdefault(r, 0)

        if seen[agent] == 0:
            first[r] += 1
        else:
            repeat[r] += 1

        seen[agent] += 1

    rounds = sorted(set(first) | set(repeat))
    first_vals = [first.get(r, 0) for r in rounds]
    repeat_vals = [repeat.get(r, 0) for r in rounds]

    plt.figure(figsize=(8, 5))
    plt.bar(rounds, first_vals, label="First-time purchase")
    plt.bar(rounds, repeat_vals, bottom=first_vals, label="Repeat purchase")

    plt.xlabel("Round")
    plt.ylabel("Number of insurance purchases")
    plt.title("Flood insurance adoption dynamics")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()