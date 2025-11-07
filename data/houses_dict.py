import pandas as pd # type: ignore
import ast

# Read Excel file with houses
df = pd.read_excel("data/houses.xlsx")  

# Convert active_measures strings to real lists
if "active_measures" in df.columns:
    df["active_measures"] = df["active_measures"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# Convert DataFrame to one dictionary
houses_dict = {
    int(row["house_id"]): {
        "value": row["value"],
        "rain_protection": row["rain_protection"],
        "river_protection": row["river_protection"],
        "preferred_rating": row["preferred_rating"],
        "active_measures": row["active_measures"],
        "available": row["available"],
    }
    for _, row in df.iterrows()
}
