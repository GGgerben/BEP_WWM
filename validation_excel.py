# ------------------------------------------------------------
# 
# Valideert het ABM door de satisfaction-verdeling uit real-life
# WhereWeMove-speelsessies te visualiseren.
# Per sessie wordt de spreiding (P10–P90), mediaan en gemiddelde
# satisfaction per ronde berekend.
# 
# ------------------------------------------------------------


import pandas as pd
import matplotlib.pyplot as plt
import os


# 1. PAD NAAR EXCEL DATA

DATA_PATH = r"C:\Users\Juliette Folkers\OneDrive - Delft University of Technology\Documents\Technische Bestuurskunde 2025-2026\BEP fase 2\Data"

files = [
    "Copy of vjcortesa_G2_Income_dist_240924.xlsx",
    "Copy of vjcortesa_G2_Income_dist_250923.xlsx",
    "Copy of vjcortesa_G2_Income_dist_251007.xlsx",
]


# 2. FUNCTIE: Satisfaction distribution per sessie net als in model.py

def plot_satisfaction_distribution_one_session(df_session, session_name):
    
    df_session = df_session.copy()
    df_session["round"] = df_session["groupround_round_number"]

    g = df_session.groupby("round")["satisfaction_total"]

    stats = pd.DataFrame({
        "round": g.mean().index,
        "mean": g.mean().values,
        "p10": g.quantile(0.10).values,
        "p50": g.quantile(0.50).values,
        "p90": g.quantile(0.90).values
    }).sort_values("round")

    plt.figure()
    plt.fill_between(stats["round"], stats["p10"], stats["p90"], alpha=0.2, label="P10-P90 band")
    plt.plot(stats["round"], stats["p50"], marker="o", linewidth=2, label="Median (P50)")
    plt.plot(stats["round"], stats["mean"], marker="o", linewidth=2, label="Mean")
    plt.axhline(0, linestyle="--", linewidth=1)

    plt.xlabel("Round")
    plt.ylabel("Satisfaction")
    plt.title(f"Satisfaction distribution over time ({session_name})")
    plt.xticks(sorted(stats["round"].unique()))
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


# 3.  KIJK NAAR DE DRIE SESSIES

for file in files:
    full_path = os.path.join(DATA_PATH, file)
    df_session = pd.read_excel(full_path, sheet_name="playerround")

    session_name = file.replace("Copy of ", "").replace(".xlsx", "")

    plot_satisfaction_distribution_one_session(df_session, session_name)
