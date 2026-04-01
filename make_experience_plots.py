
# ------------------------------------------------------------
#
# Geeft vier staafdiagrammen van effect van schade-ervaring
# Gebaseerd op ScenarioResults.xlsx
#
# ------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse # Om waarden via terminal mee te geven


def main(excel_path, output_folder, top_k):

    os.makedirs(output_folder, exist_ok=True)

    df_summary = pd.read_excel(excel_path, sheet_name="ScenarioSummary")
    df_topk = pd.read_excel(excel_path, sheet_name="MeasureTopK")

    
    # Scenario groepen per ervaringscategorie
    # 
    experience_groups = {
        "Nooit": list(range(1, 4)) + list(range(10, 13)) + list(range(19, 22)),
        "Een keer": list(range(4, 7)) + list(range(13, 16)) + list(range(22, 25)),
        "Vaker dan een keer": list(range(7, 10)) + list(range(16, 19)) + list(range(25, 28)),
    }

    
    # 1) Adoptie per welvaartsgroep
    experience_labels = ["Nooit", "Een keer", "Vaker dan een keer"]
    means = []

    for exp, scenarios in experience_groups.items():
        subset = df_summary[df_summary["scenario"].isin(scenarios)]
        means.append(subset["avg_total_purchases_per_agent"].mean())

    plt.figure()
    bars = plt.bar(experience_labels, means, color="#1f77b4")
    plt.bar(["Nooit", "Een keer", "Vaker dan een keer"], means)
    plt.xlabel("Overstromingservaring")
    plt.ylabel("Adoptie per agent (unieke maatregelen)")
    plt.ylim(0, 16)
    plt.title("Adoptie per agent per ervaringscategorie")
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
    plt.savefig(os.path.join(output_folder, "01_adoptie_per_agent_ervaring.png"))
    plt.close()

    
    # TopK maatregelen per ervaringsgroep
    
    for exp, scenarios in experience_groups.items():

        subset = df_topk[df_topk["scenario"].isin(scenarios)]

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
        plt.title(f"Top {top_k} maatregelen – {exp}")
        plt.tight_layout()

        filename = f"top{top_k}_maatregelen_{exp.lower().replace(' ', '_')}.png"
        plt.savefig(os.path.join(output_folder, filename))
        plt.close()

    print("Plots successfully created in:", output_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--excel", default="ScenarioResults.xlsx")
    parser.add_argument("--out", default="figures_experience_effect")
    parser.add_argument("--topk", type=int, default=5)

    args = parser.parse_args()

    main(args.excel, args.out, args.topk)