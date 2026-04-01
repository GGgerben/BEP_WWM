# -*- coding: utf-8 -*-

import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

df = pd.read_excel("ScenarioResults.xlsx", sheet_name="ScenarioSummary")

# 2. Controle: scenario's per experience groep
# ------------------------------------------------------------
print("\n=== CONTROLE SCENARIO -> EXPERIENCE ===")
print(df[["scenario", "experience"]].sort_values("scenario").to_string(index=False))

# 3. Gemiddelden per groep
# ------------------------------------------------------------
group_means = (
    df.groupby("experience")["avg_total_purchases_per_agent"]
    .mean()
    .sort_index()
)

print("\n=== GEMIDDELDE ADOPTIE PER ERVARINGSGROEP ===")
print(group_means)

# 4. One-way ANOVA
# ------------------------------------------------------------
model = ols("avg_total_purchases_per_agent ~ C(experience)", data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)

print("\n=== ONE-WAY ANOVA: EFFECT VAN ERVARING ===")
print(anova_table)

# 5. Effectgrootte (eta squared)
# ------------------------------------------------------------
ss_between = anova_table.loc["C(experience)", "sum_sq"]
ss_within = anova_table.loc["Residual", "sum_sq"]
eta_squared = ss_between / (ss_between + ss_within)

print("\n=== EFFECTGROOTTE ===")
print(f"Eta squared: {eta_squared:.4f}")

# ------------------------------------------------------------
# 6. Tukey post-hoc test
# ------------------------------------------------------------
tukey = pairwise_tukeyhsd(
    endog=df["avg_total_purchases_per_agent"],
    groups=df["experience"],
    alpha=0.05
)

print("\n=== TUKEY POST-HOC TEST ===")
print(tukey)

f_value = anova_table.loc["C(experience)", "F"]
p_value = anova_table.loc["C(experience)", "PR(>F)"]
df_between = int(anova_table.loc["C(experience)", "df"])
df_within = int(anova_table.loc["Residual", "df"])

print("\n=== SAMENVATTING VOOR VERSLAG ===")
print(
    f"Er is een effect van ervaring op de gemiddelde adoptie per agent, "
    f"F({df_between}, {df_within}) = {f_value:.3f}, p = {p_value:.6f}, η² = {eta_squared:.4f}."
)

print("\nGemiddelden per groep:")
for group, mean_value in group_means.items():
    print(f"- {group}: {mean_value:.2f}")
