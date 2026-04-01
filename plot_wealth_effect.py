
# ------------------------------------------------------------
# 
# Geeft vijf staafdiagrammen voor het effect van welvaart
# Gebaseerd op ScenarioResults.xlsx
#
# ------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse

def main(excel_path, output_folder, top_k):

    os.makedirs(output_folder, exist_ok=True)

    # Uitlezen Excel sheets
    df_summary = pd.read_excel(excel_path, sheet_name="ScenarioSummary")
    df_topk = pd.read_excel(excel_path, sheet_name="MeasureTopK")

    
    # 1) Welvaart en adoptie per agent, groeperen voor welvaartscategorieen
    
    wealth_groups = {
        "Rijk": range(1, 10),
        "Gemiddeld": range(10, 19),
        "Arm": range(19, 28),
    }
    wealth_labels = ["Rijk", "Gemiddeld", "Arm"]
    wealth_means = []

    for wealth, scenarios in wealth_groups.items():
        subset = df_summary[df_summary["scenario"].isin(scenarios)]
        wealth_means.append(subset["avg_total_purchases_per_agent"].mean())

    plt.figure()
    bars = plt.bar(wealth_labels, wealth_means, color="#1f77b4")
    plt.bar(["Rijk", "Gemiddeld", "Arm"], wealth_means)
    plt.xlabel("Welvaartscategorie")
    plt.ylabel("Adoptie per agent (gem. # aankopen)")
    plt.title("Adoptie per agent per welvaartsgroep")
    for bar in bars:
        h = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            h,
            f"{h:.2f}",
            ha="center",
            va="bottom"
        )

   

    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "01_adoptie_per_agent_welvaart.png"))
    plt.close()

   
    # 2 TopK maatregelen per welvaartscategorie
 
    for wealth, scenarios in wealth_groups.items():

        subset = df_topk[df_topk["scenario"].isin(scenarios)]

        # gemiddelde intensiteit per maatregel over scenario’s
        measure_means = (
            subset.groupby("measure")["avg_purchases_per_agent"]
            .mean()
            .sort_values(ascending=False)
            .head(top_k)
        )

        plt.figure()
        plt.bar(measure_means.index, measure_means.values)
        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Maatregel")
        plt.ylabel("Gem. # keer gekozen per agent (4 rondes)")
        plt.ylim(0, 4)
        plt.title(f"Top {top_k} maatregelen – {wealth}")
        plt.tight_layout()

        filename = f"top{top_k}_maatregelen_{wealth.lower()}.png"
        plt.savefig(os.path.join(output_folder, filename))
        plt.close()

    # Nulalternatief: welke maatregelen en hoe vaak gekozen per agent
      
    NULL_SCENARIO = 11 

    null_subset = df_topk[df_topk["scenario"] == NULL_SCENARIO].copy()

    if null_subset.empty:
        raise ValueError(
            f"Geen rijen gevonden in MeasureTopK voor scenario {NULL_SCENARIO}. "
            "Check of dit scenario bestaat en of MeasureTopK is geëxporteerd."
        )

    # Sorteer op intensiteit (hoe vaak gekozen per agent)
    null_subset = null_subset.sort_values("avg_purchases_per_agent", ascending=False)

    plt.figure()
    plt.bar(null_subset["measure"], null_subset["avg_purchases_per_agent"])
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Maatregel")
    plt.ylabel("Gem. # keer gekozen per agent (4 rondes)")
    plt.title(f"Nulalternatief (scenario {NULL_SCENARIO}): maatregelen en keuze-intensiteit")
    plt.ylim(0, 4)  
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, f"05_nulalternatief_scenario_{NULL_SCENARIO}.png"))
    plt.close()

    print("Plots successfully created in:", output_folder) #opslaan in map


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--excel", default="ScenarioResults.xlsx")
    parser.add_argument("--out", default="figures_wealth_effect")
    parser.add_argument("--topk", type=int, default=5)

    args = parser.parse_args()

    main(args.excel, args.out, args.topk)
