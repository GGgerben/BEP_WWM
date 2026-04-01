#  ------------------------------------------------------------
# Gevoeligheidsanalyse:
# - Varieer één parameter met -10%, basis en +10%
# - Houd overige modelinstellingen constant
# - Run het model meerdere keren met verschillende random seeds
# - Rapporteer de gemiddelde output per aanpassing
#  ------------------------------------------------------------

from classes.initialisation import initialise_agents_n
from classes.measures import measures
from classes.hazard_generator import floods
from data.houses_dict import houses_dict, generate_houses_from_agents


def run_model_with_param(seed, n_agents, param_name=None, param_value=None):
    import random
    random.seed(seed)

    agents = initialise_agents_n(n=n_agents, seed=seed)

    # Parameter toepassen op alle agenten
    if param_name is not None:
        for a in agents:
            a.params[param_name] = param_value

    # woningmarkt wordt elke run opnieuw gegenereerd want elke run is zo compleet onafhankelijk
    big_houses_dict = generate_houses_from_agents( 
        houses_dict,
        agents,
        target_n_houses=2000,
        seed=seed,
        affordability_quantile=0.95,
        house_price_quantile=0.20,
        jitter=0.10
    )

    for round_nr in range(1, 5):
        flood_results = floods()
        for a in agents:
            a.step(big_houses_dict, measures, flood_results, current_round=round_nr)

    # OUTPUT: totaal aantal maatregelen per agent (gemiddelde)
    total_measures = sum(len(a.adopted_measures) for a in agents)
    return total_measures / len(agents)


def sensitivity_analysis(param_name, base_value, n_agents=100, runs=100): #gevoeligheidsanalyse met 100 agenten en 100 runs (bepaald in convergentie)
    values = {
        "-10%": base_value * 0.9,
        "0": base_value,
        "+10%": base_value * 1.1
    }

    results = {}
    for label, val in values.items():
        outputs = []
        for seed in range(runs):  #toeval stabiliseren
            out = run_model_with_param(seed, n_agents, param_name, val)
            outputs.append(out)

        results[label] = sum(outputs) / len(outputs)

    return results


if __name__ == "__main__":

    print("Measure threshold:")
    print(sensitivity_analysis("measure_threshold", 0.6))

    print("Wealth scale:")
    print(sensitivity_analysis("wealth_scale", 100000))

    print("Damage costs:")
    print(sensitivity_analysis("damage_costs", 4000))

    print("Experience weight:")
    print(sensitivity_analysis("experience_weight", 0.7))

    # EXTRA onafhankelijke variabelen (staan ook als defaults in homeowner_agent.py)
    print("Relocation threshold:")
    print(sensitivity_analysis("relocation_threshold", 0.6))

    print("Satisfaction effect bonus:")
    print(sensitivity_analysis("sat_effect_bonus", 0.5))
