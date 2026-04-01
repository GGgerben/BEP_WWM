import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

df = pd.read_excel("ScenarioResults.xlsx", sheet_name="ScenarioSummary")


print("\n=== CONTROLE SCENARIO -> WEALTH ===")
print(df[["scenario", "wealth"]].sort_values("scenario").to_string(index=False))

# 3. Gemiddelde adoptie per wealth-groep
# ------------------------------------------------------------
group_means = (
    df.groupby("wealth")["avg_total_purchases_per_agent"]
    .mean()
    .sort_index()
)

print("\n=== GEMIDDELDE ADOPTIE PER WELVAARTSGROEP ===")
print(group_means)

group_counts = df["wealth"].value_counts().sort_index()
print("\n=== AANTAL SCENARIO'S PER WELVAARTSGROEP ===")
print(group_counts)

# 4. One-way ANOVA
# ------------------------------------------------------------
model = ols("avg_total_purchases_per_agent ~ C(wealth)", data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)

print("\n=== ONE-WAY ANOVA: EFFECT VAN WELVAART ===")
print(anova_table)

# 5. Effectgrootte (eta squared)
# ------------------------------------------------------------
ss_between = anova_table.loc["C(wealth)", "sum_sq"]
ss_within = anova_table.loc["Residual", "sum_sq"]
eta_squared = ss_between / (ss_between + ss_within)

print("\n=== EFFECTGROOTTE ===")
print(f"Eta squared: {eta_squared:.4f}")


# 6. Tukey post-hoc test
# ------------------------------------------------------------
tukey = pairwise_tukeyhsd(
    endog=df["avg_total_purchases_per_agent"],
    groups=df["wealth"],
    alpha=0.05
)

print("\n=== TUKEY POST-HOC TEST ===")
print(tukey)

# 7. Samenvatting
# ------------------------------------------------------------
f_value = anova_table.loc["C(wealth)", "F"]
p_value = anova_table.loc["C(wealth)", "PR(>F)"]
df_between = int(anova_table.loc["C(wealth)", "df"])
df_within = int(anova_table.loc["Residual", "df"])

)

print("\nGemiddelden per groep:")
for group, mean_value in group_means.items():
    print(f"- {group}: {mean_value:.2f}")
