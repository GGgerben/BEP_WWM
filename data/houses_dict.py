import pandas as pd 
import ast
import random
import copy

# Read Excel file with houses
df = pd.read_excel("data/houses.xlsx")  
df["house_id"] = df["house_id"].astype(str)

# Convert active_measures strings to real lists
def safe_parse(x):
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
    affordability_quantile=0.95,   # hoeveel agents moeten minimaal "een kans" hebben
    house_price_quantile=0.20,     # kijk naar de goedkoopste 20% huizen als "instapsegment"
    jitter=0.10                    # prijsruis ±10%
):
    rng = random.Random(seed)

    base_items = list(base_houses_dict.items())
    if not base_items:
        raise ValueError("base_houses_dict is empty")

    budgets = sorted(float(a.wealth) for a in agents)
    if not budgets:
        raise ValueError("agents is empty")

    # doelbudget: budget van de agent op bv. 95% quantile
    b_idx = int(affordability_quantile * (len(budgets) - 1))
    b_q = budgets[b_idx]

    # instapprijs uit basis: prijs van goedkoopste X% huizen
    base_values = sorted(float(info["value"]) for _, info in base_items)
    p_idx = int(house_price_quantile * (len(base_values) - 1))
    p_q = base_values[p_idx]

    # schaalfactor zodat "instap-huis" matcht met "doelbudget"
    # (als p_q te duur is t.o.v. b_q => factor < 1 => huizen goedkoper)
    scale = (b_q / p_q) if p_q > 0 else 1.0

    houses = {}
    for i in range(target_n_houses):
        hid, info = rng.choice(base_items)
        new_id = f"{hid}_g{i}"

        new_info = copy.deepcopy(info)
        new_info["available"] = True

        # prijs = basisprijs * scale * ruis
        v = float(new_info["value"])
        v = v * scale * rng.uniform(1 - jitter, 1 + jitter)
        new_info["value"] = max(0.0, v)

        # (optioneel) kleine variatie in protections, zoals jij al deed
        if "rain_protection" in new_info:
            new_info["rain_protection"] = max(0, int(round(new_info["rain_protection"] + rng.choice([-1,0,1]))))
        if "river_protection" in new_info:
            new_info["river_protection"] = max(0, int(round(new_info["river_protection"] + rng.choice([-1,0,1]))))

        houses[new_id] = new_info

    return houses