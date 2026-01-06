from classes.environment import Environment # type: ignore
from classes.homeowner_agent import Agent # type: ignore
from classes.measures import measures # type: ignore
from classes.hazard_generator import floods # type: ignore
from classes.population_generator import PopulationGeneratorRandom
from classes.initialisation import (initialise_agents_n, initialise_agents)
from classes.visualise import (plot_macro_satisfaction, plot_satisfaction_distribution, 
                                    plot_subsidy_effect_summary, plot_total_new_measures_per_round, 
                                     plot_satisfaction_over_time, plot_floods_per_round, 
                                    plot_measures_heatmap, plot_insurance_usage)

from classes.visualise import plot_adoption_over_time, plot_measure_adoption_summary, plot_insurance_repeats

from export import save_history, initialise_history, update_history, add_round_zero

import matplotlib.pyplot as plt
import numpy as np
import random

# Import houses
from data.houses_dict import houses_dict, generate_houses_from_agents # type: ignore
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":

    # --------------------------- Initialising data ---------------------------------

    history = initialise_history()

    # agents = initialise_agents() 
    agents = initialise_agents_n(n=1000, seed=42)

    big_houses_dict = generate_houses_from_agents(houses_dict, agents, target_n_houses=2000, seed=42, affordability_quantile=0.95, 
                                                  house_price_quantile=0.20, jitter=0.10)
    add_round_zero(history, agents)

    # --------------------------- Running experiment ---------------------------------

    # Run 4 rounds
    for round_nr in range(1, 5):

        flood_results = floods()

        # Agent decision making per round
        for agent in agents:
            agent.step(big_houses_dict, measures, flood_results, current_round=round_nr)
            # agent.step(houses_dict, measures, flood_results, current_round=round_nr)

            update_history(history, agent, flood_results, round_nr)
        
    save_history(history,'scenario_id', 'flood_regime', 'policy_type', 'measure', 'subsidy_level', 'insurance', 'n_agents', "seed")   
        
    # --------------------------- Visualisation --------------------------------

    # plots results
    # plot_insurance_repeats(history, insurance_name="Flood insurance") 
    plot_measure_adoption_summary(history)
    # plot_adoption_over_time(history)
   
    # Test plots
    # plot_satisfaction_over_time(agents, rounds=4)
    # plot_floods_per_round(agents)
    # plot_measures_heatmap(agents)
    # plot_total_new_measures_per_round(agents)

    # plot_insurance_usage(agents, insurance_name="Flood insurance")
    # plot_subsidy_effect_summary(agents, measures, subsidized_measure_name="Water pump")   

    # plot_macro_satisfaction(history)
    # plot_satisfaction_distribution(history)
        

    

    






