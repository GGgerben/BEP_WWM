import pandas as pd 
import ast

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
