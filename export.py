import pandas as pd
from classes.homeowner_agent import Agent
from classes.measures import Measure
from pathlib import Path

def save_history(
    history,
    scenario_id,
    flood_regime,
    policy_type,
    measure,
    subsidy_level,
    insurance,
    n_agents,
    seed
):
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    filename = (
        f"history_{scenario_id}_"
        f"{flood_regime}_"
        f"{policy_type}_"
        f"{measure}_"
        f"{subsidy_level}_"
        f"{insurance}_"
        f"N{n_agents}_"
        f"seed{seed}.csv"
    )

    path = results_dir / filename
    pd.DataFrame(history).to_csv(path, index=False)

    print(f"Saved: {path}")

def initialise_history():
    return {
        "round": [],
        "agent_id": [],
        "satisfaction": [],
        "wealth": [],
        "flood_results": [],
        "flood_damages": [],
        "new_measures": [],
        "measures": []  
    }

def update_history(history, agent, flood_results, round_nr):
    history["round"].append(round_nr)
    history["agent_id"].append(agent.ID)
    history["satisfaction"].append(agent.satisfaction)
    history["wealth"].append(agent.wealth)
    history["flood_results"].append(flood_results)
    history["flood_damages"].append(agent.damage_history[-1]["damage_cost"] if agent.damage_history else 0)

    measure_names = [_measure_label(m) for m in agent.adopted_measures]

    prev_len = getattr(agent, "_prev_measures_len", 0)
    new_this_round = measure_names[prev_len:]

    history["new_measures"].append(";".join(new_this_round))
    history["measures"].append(";".join(measure_names))

    agent._prev_measures_len = len(measure_names)

def _measure_label(m):
    if isinstance(m, (tuple, list)):
        m = m[0]
    return m.name

def add_round_zero(history, agents):
    for agent in agents:
        history["round"].append(0)
        history["agent_id"].append(agent.ID)
        history["satisfaction"].append(agent.satisfaction)
        history["wealth"].append(agent.wealth)

        history["flood_results"].append(None)
        history["flood_damages"].append(0) 

        current = {_measure_label(m) for m in agent.adopted_measures}
        history["new_measures"].append("") 
        history["measures"].append(";".join(sorted(current)))

        agent._prev_measures_set = current
        agent._prev_measures_len = len(agent.adopted_measures)