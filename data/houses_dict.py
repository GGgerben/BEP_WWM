"""
Utility functions for loading and scaling housing data.

This module converts the Excel-based housing input used in the
WhereWeMove serious game into a dictionary format suitable for
agent-based simulations. It also supports upscaling the housing
stock to larger synthetic populations while preserving affordability
relationships.
"""

import pandas as pd 
import ast
import random
import copy

# Read Excel file with houses
df = pd.read_excel("data/houses.xlsx")  
df["house_id"] = df["house_id"].astype(str)

# Convert active_measures strings to real lists
def safe_parse(x):
    """
    Safely convert string representations of lists into Python lists.

    Used to parse the 'active_measures' column from the Excel input,
    which may contain empty values or comma-separated strings.
    """

    if not isinstance(x, str):
        return x
    cleaned = x.strip().strip("[]")     
    if cleaned == "":
        return []
    if "," in cleaned:
        return [s.strip() for s in cleaned.split(",")]
    return [cleaned]                    

df["active_measures"] = df["active_measures"].apply(safe_parse)

# Convert DataFrame to one dictionary
houses_dict = {
    row["house_id"]: {
        "value": row["value"],
        "available_round": row["available_round"],
        "rain_protection": row["rain_protection"],
        "river_protection": row["river_protection"],
        "preferred_rating": row["preferred_rating"],
        "active_measures": row["active_measures"],
        "available": row["available"],
    }
    for _, row in df.iterrows()
}

def generate_houses_from_agents(
    base_houses_dict,
    agents,
    target_n_houses=1200,
    seed=42,
    affordability_quantile=0.95,   
    house_price_quantile=0.20,     
    jitter=0.10                    
):
    """
    Generate a synthetic housing stock scaled to agent affordability.

    Base houses are replicated and rescaled such that entry-level house
    prices match the upper affordability of the agent population.
    Random variation is added to prices and protection levels.

    Returns a dictionary of newly generated houses.
    """

    rng = random.Random(seed)

    base_items = list(base_houses_dict.items())
    if not base_items:
        raise ValueError("base_houses_dict is empty")

    budgets = sorted(float(a.wealth) for a in agents)
    if not budgets:
        raise ValueError("agents is empty")

    # Target affordability level (e.g. 95th percentile of agent wealth)
    b_idx = int(affordability_quantile * (len(budgets) - 1))
    b_q = budgets[b_idx]

    # Entry-level house price (e.g. 20th percentile of base houses)
    base_values = sorted(float(info["value"]) for _, info in base_items)
    p_idx = int(house_price_quantile * (len(base_values) - 1))
    p_q = base_values[p_idx]

    # Scale factor to align housing prices with agent affordability
    scale = (b_q / p_q) if p_q > 0 else 1.0

    houses = {}
    for i in range(target_n_houses):
        hid, info = rng.choice(base_items)
        new_id = f"{hid}_g{i}"

        new_info = copy.deepcopy(info)
        new_info["available"] = True

        # Scale and jitter house price
        v = float(new_info["value"])
        v = v * scale * rng.uniform(1 - jitter, 1 + jitter)
        new_info["value"] = max(0.0, v)

        # Optional small variation in protection levels
        if "rain_protection" in new_info:
            new_info["rain_protection"] = max(0, int(round(new_info["rain_protection"] + rng.choice([-1,0,1]))))
        if "river_protection" in new_info:
            new_info["river_protection"] = max(0, int(round(new_info["river_protection"] + rng.choice([-1,0,1]))))

        houses[new_id] = new_info

    return houses