import copy
import random
import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from dataclasses import dataclass
from typing import Dict, Optional, List

from classes.measures import measures
from classes.hazard_generator import floods
from classes.initialisation import initialise_agents_n, initialise_agents
from export import save_history, initialise_history, update_history, add_round_zero

# houses
from data.houses_dict import houses_dict

RESULTS_DIR = "results"
OUT_DIR = "plots"



@dataclass(frozen=True)
class Scenario:
    flood_regime: str
    scenario_id: str
    policy_type: str
    subsidised_measures: Optional[str]
    subsidy_level: Optional[float]
    insurance_available: bool
    agents: int = 1000
    rounds: int = 4
    runs: int = 40


SCENARIOS: List[Scenario] = [
    Scenario("one_shock",     "S0", "Baseline",  None,         0.0,  False),
    Scenario("one_shock",     "S2", "Subsidy",   "Self-activating wall", 0.5,  False),
    Scenario("one_shock",     "S3", "Insurance", None,         None, True),
    Scenario("random_floods", "R0", "Baseline",  None,         0.0,  False),
    Scenario("random_floods", "R2", "Subsidy",   "Self-activating wall", 0.5,  False),
    Scenario("random_floods", "R3", "Insurance", None,         None, True),
]


def set_seeds(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def floods_for_round(s: Scenario, round_nr: int):
    """
    One shock: ronde 2 vaste flood.
    Random floods: gebruik bestaande floods() generator.
    """
    if s.flood_regime == "one_shock":
        return {"rain_damage": 10, "river_damage": 12} if round_nr == 2 else {"rain_damage": 0, "river_damage": 0}

    if s.flood_regime == "random_floods":
        return floods()

    raise ValueError(f"Onbekend flood_regime: {s.flood_regime}")


def _find_measure(measures_list, name: str):
    for m in measures_list:
        if getattr(m, "name", None) == name:
            return m
    raise ValueError(f"Measure met name='{name}' niet gevonden.")


def make_policy_measures(s: Scenario):
    """
    Maak een kopie van de measures-lijst en pas scenario-instellingen toe.
    """
    policy_measures = copy.deepcopy(measures)

    insurance = _find_measure(policy_measures, "Flood insurance")

    # Insurance aan/uit (fallback: cost=inf als Measure geen available attribuut heeft)
    if hasattr(insurance, "available"):
        insurance.available = bool(s.insurance_available)
    else:
        if not s.insurance_available:
            insurance.cost = float("inf")

    if s.policy_type == "Subsidy" and s.subsidised_measures:
        m = _find_measure(policy_measures, s.subsidised_measures)
        m.subsidy_percentage = float(s.subsidy_level or 0.0)

    return policy_measures


def run_once(s: Scenario, seed: int, houses_dict: Dict) -> None:
    set_seeds(seed)

    history = initialise_history()

    try:
        agents = initialise_agents_n(n=s.agents, seed=seed)
    except Exception:
        agents = initialise_agents()

    policy_measures = make_policy_measures(s)
    add_round_zero(history, agents)

    for round_nr in range(1, s.rounds + 1):
        flood_results = floods_for_round(s, round_nr)
        for agent in agents:
            agent.step(houses_dict, policy_measures, flood_results, current_round=round_nr)
            update_history(history, agent, flood_results, round_nr)

    save_history(
        history,
        scenario_id=s.scenario_id,
        flood_regime=s.flood_regime,
        policy_type=s.policy_type,
        measure=s.subsidised_measures or "-",
        subsidy_level=s.subsidy_level if s.subsidy_level is not None else 0.0,
        insurance=s.insurance_available,
        n_agents=s.agents,
        seed=seed,
    )


def run_all_experiments(houses_dict: Dict, base_seed: int = 42) -> None:
    for s in SCENARIOS:
        for i in range(s.runs):
            seed = base_seed + i
            run_once(s, seed=seed, houses_dict=houses_dict)
            print(f"{s.scenario_id} run {i+1}/{s.runs} done (seed={seed})")

    print("\nKlaar. Alles staat in de map: results/")


def parse_filename(fp: str) -> dict:
    """
    Expected filename format (as produced by your save_history):
    history_R0_random_floods_Baseline_-_0.0_False_N1000_seed43.csv

    We extract scenario_id, flood_regime, policy_type and seed from the filename.
    """
    name = os.path.basename(fp).replace(".csv", "")
    left, right = name.split("_N", 1)  # right looks like: "1000_seed43"

    # seed
    seed = int(right.split("_seed")[1])

    # left looks like: "history_R0_random_floods_Baseline_-_0.0_False"
    parts = left.split("_")
    if len(parts) < 4 or parts[0] != "history":
        raise ValueError(f"Unexpected filename format: {os.path.basename(fp)}")

    scenario_id = parts[1]
    flood_regime = parts[2]
    policy_type = parts[3]

    return {
        "scenario_id": scenario_id,
        "flood_regime": flood_regime,
        "policy_type": policy_type,
        "seed": seed,
        "file": os.path.basename(fp),
    }


def macro_by_round_from_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute satisfaction distribution stats per round within ONE run (one CSV).
    Requires columns: 'round' and 'satisfaction'.
    """
    if "round" not in df.columns:
        raise KeyError("CSV is missing required column: 'round'")
    if "satisfaction" not in df.columns:
        raise KeyError("CSV is missing required column: 'satisfaction'")

    # Ensure round is numeric
    df = df.copy()
    df["round"] = pd.to_numeric(df["round"], errors="coerce")
    df = df.dropna(subset=["round"])
    df["round"] = df["round"].astype(int)

    out = (
        df.groupby("round")["satisfaction"]
          .agg(
              avg_satisfaction="mean",
              sat_p10=lambda x: np.percentile(x, 10),
              sat_p50=lambda x: np.percentile(x, 50),
              sat_p90=lambda x: np.percentile(x, 90),
          )
          .reset_index()
    )
    return out


def load_all_satisfaction(results_dir: str = RESULTS_DIR) -> pd.DataFrame:
    """
    Load all history_*.csv files and compute macro stats per round per run (seed).
    Returns a dataframe with columns:
    scenario_id, policy_type, flood_regime, seed, round, avg_satisfaction, sat_p10, sat_p50, sat_p90
    """
    files = sorted(glob.glob(os.path.join(results_dir, "history_*.csv")))
    if not files:
        raise FileNotFoundError(f"No history_*.csv files found in: {os.path.abspath(results_dir)}")

    macros = []
    for fp in files:
        meta = parse_filename(fp)
        df = pd.read_csv(fp)

        macro = macro_by_round_from_df(df)
        for k, v in meta.items():
            macro[k] = v

        macros.append(macro)

    return pd.concat(macros, ignore_index=True)


def average_over_runs(macro_df: pd.DataFrame) -> pd.DataFrame:
    """
    Average the per-run distribution stats over seeds, per scenario and round.
    We average the run-level stats (mean, p10, p50, p90) across runs.
    """
    return (
        macro_df
        .groupby(["scenario_id", "round"])
        .agg(
            mean=("avg_satisfaction", "mean"),
            p10=("sat_p10", "mean"),
            p50=("sat_p50", "mean"),
            p90=("sat_p90", "mean"),
            n_runs=("seed", "nunique"),
        )
        .reset_index()
        .sort_values(["scenario_id", "round"])
    )


def plot_satisfaction_by_scenario(results_dir: str = RESULTS_DIR, out_dir: str = OUT_DIR) -> None:
    os.makedirs(out_dir, exist_ok=True)

    macro_all = load_all_satisfaction(results_dir)
    avg = average_over_runs(macro_all)

    # One plot per scenario
    for scenario_id, g in avg.groupby("scenario_id"):
        r = g["round"].tolist()
        mean = g["mean"].tolist()
        p10 = g["p10"].tolist()
        p50 = g["p50"].tolist()
        p90 = g["p90"].tolist()
        n_runs = int(g["n_runs"].iloc[0])

        plt.figure()
        plt.fill_between(r, p10, p90, alpha=0.2, label="P10–P90 band (avg over runs)")
        plt.plot(r, p50, marker="o", linewidth=2, label="Median (P50)")
        plt.plot(r, mean, marker="o", linewidth=2, label="Mean")
        plt.axhline(0, linestyle="--", linewidth=1)

        plt.xlabel("Round")
        plt.ylabel("Satisfaction")
        plt.title(f"Satisfaction distribution over time — Scenario {scenario_id} (n_runs={n_runs})")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        out_path = os.path.join(out_dir, f"satisfaction_{scenario_id}.png")
        plt.savefig(out_path, dpi=200)
        plt.close()

        print("Saved:", out_path)

def _split_measures_cell(x):
    """CSV has measures as 'A;B;C' or empty/NaN."""
    if pd.isna(x) or str(x).strip() == "":
        return []
    return [m.strip() for m in str(x).split(";") if m.strip()]


def _scenario_from_filename(fp: str) -> str:
    """
    history_R0_random_floods_Baseline_-_0.0_False_N1000_seed43.csv -> "R0"
    """
    return os.path.basename(fp).split("_")[1]


def load_all_history(results_dir: str = "results") -> pd.DataFrame:
    """Load all history_*.csv files and add a 'scenario' column from the filename."""
    files = glob.glob(os.path.join(results_dir, "history_*.csv"))
    if not files:
        raise FileNotFoundError(f"No history_*.csv found in: {os.path.abspath(results_dir)}")

    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df["scenario"] = _scenario_from_filename(f)
        dfs.append(df)

    out = pd.concat(dfs, ignore_index=True)

    # safety: ensure 'round' is numeric
    out["round"] = pd.to_numeric(out["round"], errors="coerce")
    out = out.dropna(subset=["round"])
    out["round"] = out["round"].astype(int)

    return out


def get_all_measures(df: pd.DataFrame) -> list:
    """Return sorted list of all measure names that appear in df['measures']."""
    all_measures = set()
    for x in df["measures"]:
        all_measures.update(_split_measures_cell(x))
    return sorted(m for m in all_measures if m != "")


def compute_measure_adoption(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a scenario × measure table with values = share of agents that has the measure in the final round.
    Rows: scenario (S0, S2, ...)
    Cols: measures
    """
    if "measures" not in df.columns:
        raise KeyError("Missing required column: 'measures'")

    last_round = int(df["round"].max())
    final = df[df["round"] == last_round]

    scenarios = sorted(final["scenario"].unique())
    measures = get_all_measures(final)

    table = pd.DataFrame(index=scenarios, columns=measures, dtype=float)

    for s in scenarios:
        sdf = final[final["scenario"] == s]
        for m in measures:
            table.loc[s, m] = sdf["measures"].apply(lambda x: m in _split_measures_cell(x)).mean()

    return table

def plot_satisfaction_regime_with_uncertainty(results_dir="results", out_dir="plots"):
    import os
    import matplotlib.pyplot as plt

    os.makedirs(out_dir, exist_ok=True)

    # Load your macro data (per run per round)
    macro_all = load_all_satisfaction(results_dir)

    # Average across runs
    avg = average_over_runs(macro_all)

    regimes = {
        "Random floods": ["R0", "R2", "R3"],
        "One shock": ["S0", "S2", "S3"],
    }

    for regime_name, scenarios in regimes.items():
        plt.figure(figsize=(7, 5))

        for scenario in scenarios:
            g = avg[avg["scenario_id"] == scenario]

            r = g["round"]
            p10 = g["p10"]
            p50 = g["p50"]
            p90 = g["p90"]

            # Uncertainty band
            plt.fill_between(r, p10, p90, alpha=0.15)

            # Median line
            plt.plot(r, p50, marker="o", linewidth=2, label=scenario)

        plt.axhline(0, linestyle="--", linewidth=1)
        plt.xlabel("Round")
        plt.ylabel("Satisfaction")
        plt.title(f"Satisfaction over time — {regime_name}")
        plt.legend(title="Scenario")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        out = os.path.join(out_dir, f"satisfaction_{regime_name.replace(' ', '_')}_with_uncertainty.png")
        plt.savefig(out, dpi=200)
        plt.close()

        print("Saved:", out)

def plot_measure_adoption_by_scenario(results_dir="results", out_dir="plots"):
    """
    Makes 4 plots (ever adopted, per-run averaged):
    - R0 vs R2
    - R0 vs R3
    - S0 vs S2
    - S0 vs S3

    Ever-adopted is computed PER RUN (per CSV), then averaged over runs.
    Flood insurance is always included (even if adoption is 0).
    """

    os.makedirs(out_dir, exist_ok=True)

    files = glob.glob(os.path.join(results_dir, "history_*.csv"))
    if not files:
        raise FileNotFoundError(f"No history_*.csv found in {results_dir}")

    pairs = [("R0", "R2"), ("R0", "R3"), ("S0", "S2"), ("S0", "S3")]

    # detect agent id column from first file
    sample = pd.read_csv(files[0])
    agent_col = next(c for c in ["agent_id", "id", "unique_id", "agent"] if c in sample.columns)

    # Use ALL data to build the measure list (so nothing is missed)
    # (still "ever adopted" uses per-run averaging below)
    all_df = []
    for f in files:
        all_df.append(pd.read_csv(f))
    all_df = pd.concat(all_df, ignore_index=True)

    measures_list = get_all_measures(all_df)

    # ALWAYS include insurance
    if "Flood insurance" not in measures_list:
        measures_list = ["Flood insurance"] + measures_list

    for a, b in pairs:
        scenarios = [a, b]
        results = {s: [] for s in scenarios}

        for scenario in scenarios:
            scenario_files = [f for f in files if f"_{scenario}_" in os.path.basename(f)]
            if not scenario_files:
                raise FileNotFoundError(f"No files found for scenario {scenario}")

            for m in measures_list:
                per_run = []

                for f in scenario_files:
                    df = pd.read_csv(f)

                    ever_by_agent = (
                        df.groupby(agent_col)["measures"]
                          .apply(lambda series: any(m in _split_measures_cell(x) for x in series))
                          .mean()
                    )
                    per_run.append(ever_by_agent)

                results[scenario].append(np.mean(per_run) * 100)

        # ---- plot ----
        x = np.arange(len(measures_list))
        width = 0.35

        plt.figure(figsize=(12, 5))
        plt.bar(x - width/2, results[a], width, label=a)
        plt.bar(x + width/2, results[b], width, label=b)

        plt.xticks(x, measures_list, rotation=45, ha="right")
        plt.ylabel("% of agents that ever adopted")
        plt.title(f"Adoption comparison (ever adopted): {a} vs {b}")
        plt.legend()
        plt.tight_layout()

        out = os.path.join(out_dir, f"adoption_compare_{a}_vs_{b}.png")
        plt.savefig(out, dpi=200)
        plt.close()
        print("Saved:", out)


def plot_policy_comparison_adoption_bars(results_dir="results", out_dir="plots"):
    """
    Makes:
    1) Pairwise EVER-adopted comparison plots (from plot_measure_adoption_by_scenario)
    2) FINAL adoption bar plot for EACH scenario (S0,S2,S3,R0,R2,R3)
    """
    import os
    import matplotlib.pyplot as plt

    os.makedirs(out_dir, exist_ok=True)

    # 1) Ever-adopted comparison plots (your other function now makes multiple pairs)
    plot_measure_adoption_by_scenario(results_dir, out_dir)

    # 2) Final adoption after last round for EACH scenario
    df = load_all_history(results_dir)
    last_round = int(df["round"].max())

    for scenario in sorted(df["scenario"].unique()):
        final = df[(df["scenario"] == scenario) & (df["round"] == last_round)].copy()

        measures_list = get_all_measures(final)

        # ALWAYS include insurance
        if "Flood insurance" not in measures_list:
            measures_list = ["Flood insurance"] + measures_list

        vals = []
        for m in measures_list:
            vals.append(final["measures"].apply(lambda x: m in _split_measures_cell(x)).mean() * 100.0)

        plt.figure(figsize=(12, 5))
        plt.bar(measures_list, vals)
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("% of agents that adopted (final round)")
        plt.title(f"Final adoption after {last_round} rounds – scenario {scenario}")
        plt.tight_layout()

        out_path = os.path.join(out_dir, f"final_adoption_test{scenario}.png")
        plt.savefig(out_path, dpi=200)
        plt.close()
        print("Saved:", out_path)

if __name__ == "__main__":
    # 1) Run experiments (only needed if results/ is empty or you changed the model)
    # run_all_experiments(houses_dict, base_seed=42)

    # 2) Reproduce plots (reads CSVs from results/ and saves PNGs to plots/)
    plot_policy_comparison_adoption_bars("results", "plots")
    plot_satisfaction_regime_with_uncertainty("results", "plots")
