from classes.environment import Environment # type: ignore
from classes.homeowner_agent import Agent # type: ignore
from classes.measures import measures # type: ignore
from classes.hazard_generator import floods # type: ignore
from classes.population_generator import PopulationGeneratorRandom
from classes.initialisation import (plot_housing, plot_macro_satisfaction, plot_policy_adoption, plot_satisfaction_distribution, 
                                    plot_policy_effect, plot_policy_effect, run_and_count_purchases, normalize_round_counter, 
                                    plot_measure_distribution_cdf, plot_subsidy_effect_summary, plot_total_new_measures_per_round, 
                                    initialise_agents_n, initialise_agents, plot_satisfaction_over_time, plot_floods_per_round, 
                                    plot_subsidy_effect, plot_measures_heatmap, plot_insurance_usage)
import matplotlib.pyplot as plt
import numpy as np
import random

# Import houses
from data.houses_dict import houses_dict, generate_houses_from_agents # type: ignore
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    
    agents = initialise_agents() 
    # agents = initialise_agents_n(n=1000, seed=42)

    # big_houses_dict = generate_houses_from_agents(houses_dict, agents, target_n_houses=2000, seed=42, affordability_quantile=0.95, 
    #                                               house_price_quantile=0.20, jitter=0.10)
    
    for round_nr in range(1, 5):

        flood_results = floods()

        # step agents
        for agent in agents:
            # agent.step(big_houses_dict, measures, flood_results, current_round=round_nr)
            agent.step(houses_dict, measures, flood_results, current_round=round_nr)
        
       

    # Test plots
    # plot_measure_distribution_cdf(measure_dist_per_round)
    # # plot_housing(history)
    # plot_macro_satisfaction(history)
    # plot_policy_adoption(history)
    # plot_satisfaction_distribution(history)
        
    # plot_satisfaction_over_time(agents)  
    # plot_measures_heatmap(agents)
    # plot_total_new_measures_per_round(agents)
    # plot_insurance_usage(agents)

    # plot_floods_per_round(agents) 
    

    # plot_subsidy_effect_summary(
    # agents,
    # measures,
    # subsidized_measure_name="Water pump"
    # )   

    






