
# ------------------------------------------------------------
# Per parameter zijn drie condities/groepen (-10%, basis, +10%) met elkaar vergeleken.
# De one-way ANOVA toetst of de gemiddelde modeloutput significant verschilt tussen deze drie parameterinstellingen.
# ------------------------------------------------------------

import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

from sensitivity import run_model_with_param



def anova_one_param(param_name, base_value, n_agents=100, runs=100): # Dezelfde waarden als in de gevoeligheidsanalyse.

    values = {
        "-10pct": base_value * 0.9,
        "base": base_value,
        "+10pct": base_value * 1.1
    }

    rows = []

    for condition, val in values.items():
        for seed in range(runs): # Model wordt vaker gerund zodat de stochastische effecten worden gestabiliseerd, met verschillende seeds.
            output = run_model_with_param(seed, n_agents, param_name, val)
            rows.append({
                "Parameter": param_name,
                "Condition": condition,
                "Output": output
            })

    df = pd.DataFrame(rows)

    model = ols("Output ~ C(Condition)", data=df).fit() # one-way ANOVA wordt hier uitgevoerd als lineair regressiemodel
    anova = sm.stats.anova_lm(model, typ=2)

    ss_between = float(anova.loc["C(Condition)", "sum_sq"])
    ss_within = float(anova.loc["Residual", "sum_sq"])

    df_between = int(anova.loc["C(Condition)", "df"])
    df_within = int(anova.loc["Residual", "df"])

    f_value = float(anova.loc["C(Condition)", "F"]) # Hoge F-waarde betekent substantieel effect
    p_value = float(anova.loc["C(Condition)", "PR(>F)"]) # Waarschijnlijkheid

    
    eta_sq = ss_between / (ss_between + ss_within)

    means = (
        df.groupby("Condition")["Output"]
          .mean()
          .to_dict()
    )

    result = {
        "Parameter": param_name,
        "Mean_minus10pct": round(means.get("-10pct", 0), 2),
        "Mean_base": round(means.get("base", 0), 2),
        "Mean_plus10pct": round(means.get("+10pct", 0), 2),
        "df_between": df_between,
        "df_within": df_within,
        "F_value": round(f_value, 3),
        "p_value": round(p_value, 4),
        "eta_squared": round(eta_sq, 4)
    }

    return result


def significance(p):
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return ""


if __name__ == "__main__":

    # Hier worden de base values aangegeven
    parameters = {
        "measure_threshold": 0.6,
        "wealth_scale": 100000,
        "damage_costs": 4000,
        "experience_weight": 0.7
    }

    results = []

    for param, base in parameters.items():
        print("Running ANOVA for", param)
        row = anova_one_param(param, base, n_agents=100, runs=100)
        row["significance"] = significance(row["p_value"])
        results.append(row)

    results_df = pd.DataFrame(results)

    print("\n=== ONE WAY ANOVA RESULTS ===")
    print(results_df.to_string(index=False))

    results_df.to_excel("anova_results.xlsx", index=False) #Opgeslagen in excel
