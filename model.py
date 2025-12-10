from classes.environment import Environment # type: ignore
from classes.homeowner_agent import Agent # type: ignore
from classes.measures import measures # type: ignore
from classes.hazard_generator import floods # type: ignore
from classes.initialisation import initialise_agents, plot_satisfaction_over_time, plot_floods_per_round, plot_subsidy_effect, plot_measures_heatmap, plot_insurance_usage# type: ignore
from classes.initialisation import plot_subsidy_effect_summary
from classes.population_generator import PopulationGeneratorRandom

# Import houses
from data.houses_dict import houses_dict # type: ignore


if __name__ == "__main__":

    agents = initialise_agents()    

    for round_nr in range(1, 5):   # rondes 1 t/m 4
        print(f"\n=== ROUND {round_nr} ===")
        flood_results = floods()
        print(f"[DEBUG] Flood results round {round_nr}: {flood_results}")
        
        for agent in agents:
            agent.step(houses_dict, measures, flood_results, current_round=round_nr)
            # print(agent.adopted_measures)
            # print(len(agent.adopted_measures))
            # print(f"Agent {agent.ID} house after {round_nr}: {agent.house}, protection: {agent.protection}, wealth: {agent.wealth}, satisfaction: {agent.satisfaction},")
            # print(len(agent.adopted_measures))
            # print(agent.adopted_measures)
        
    # plot_satisfaction_over_time(agents)  
    # plot_measures_heatmap(agents)
    # plot_insurance_usage(agents)

    # plot_floods_per_round(agents) 
    

    plot_subsidy_effect_summary(
    agents,
    measures,
    subsidized_measure_name="Water pump"
    )   

    






