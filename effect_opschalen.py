# plot_N_effect.py
# ------------------------------------------------------------
# Staafdiagram: adoptie per agent per populatiegrootte (N=10/100/1000)
# Gebaseerd op ScenarioResults.xlsx (ScenarioSummary)
# ------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse

def main(excel_path: str, output_folder: str):

    os.makedirs(output_folder, exist_ok=True)

    df_summary = pd.read_excel(excel_path, sheet_name="ScenarioSummary")

    n_order = [10, 100, 1000]
    means = []
    for n in n_order:
        subset = df_summary[df_summary["N"] == n]
        means.append(subset["avg_total_purchases_per_agent"].mean())

    plt.figure()
    bars = plt.bar([str(n) for n in n_order], means)
    plt.xlabel("Aantal agenten (N)")
    plt.ylabel("Adoptie per agent (gem. # aankopen)")
    plt.ylim(0, 16)
    plt.title("Adoptie per agent per populatiegrootte")

    # waarden boven balken
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, h, f"{h:.2f}", ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "01_adoptie_per_agent_N.png"))
    plt.close()

    print("Plot successfully created in:", output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--excel", default="ScenarioResults.xlsx")
    parser.add_argument("--out", default="figures_N_effect")

    args = parser.parse_args()
    main(args.excel, args.out)
