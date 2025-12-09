from classes.environment import Environment # type: ignore
from classes.homeowner_agent import Agent # type: ignore
from classes.measures import measures # type: ignore
from classes.hazard_generator import floods # type: ignore
from classes.initialisation import initialise_agents # type: ignore
from classes.initialisation import plot_satisfaction_over_time # type: ignore
from classes.initialisation import plot_floods_per_round# type: ignore

from classes.population_generator import PopulationGeneratorRandom

# Import houses
from data.houses_dict import houses_dict # type: ignore


if __name__ == "__main__":

    agents = initialise_agents()

    # Test huis dict
    # houses_dict = {
    #     "N07": {
    #         "value": 200000,
    #         "available": True,   # gekocht in ronde 1
    #         "preferred_rating": 3,
    #         "rain_protection": 9,
    #         "river_protection": 6,
    #         "available_round": 1,
    #     },
    #     "N08": {
    #         "value": 190000,
    #         "available": True,
    #         "preferred_rating": 3,
    #         "rain_protection": 9,
    #         "river_protection": 7,
    #         "available_round": 4,
    #     },
    # }

    # TEST VERHUIZEN
    # houses_dict = {
    #     "EXPENSIVE_RISKY": {
    #         "value": 105000,     
    #         "available": True,
    #         "preferred_rating": 4,  
    #         "rain_protection": 5,
    #         "river_protection": 3,   
    #         "available_round": 1,
    #     },
    #     "CHEAP_SAFE": {
    #         "value": 105000,
    #         "available": True,
    #         "preferred_rating": 3, 
    #         "rain_protection": 6,
    #         "river_protection": 4,
    #         "available_round": 4,
    #     },
    #      "CHEAP_SAFE2": {
    #         "value": 110000,
    #         "available": True,
    #         "preferred_rating": 3,  
    #         "rain_protection": 7,
    #         "river_protection": 6,
    #         "available_round": 4,
    #     },
    # }
    

    for round_nr in range(1, 5):   # rondes 1 t/m 4
        print(f"\n=== ROUND {round_nr} ===")
        flood_results = floods()
        print(f"[DEBUG] Flood results round {round_nr}: {flood_results}")
        
        for agent in agents:
            agent.step(houses_dict, measures, flood_results, current_round=round_nr)
            # print(agent.adopted_measures)
            # print(len(agent.adopted_measures))
            print(f"Agent {agent.ID} house after {round_nr}: {agent.house}, protection: {agent.protection}, wealth: {agent.wealth}, satisfaction: {agent.satisfaction},")
            print(len(agent.adopted_measures))
            # print(agent.adopted_measures)
        
    plot_satisfaction_over_time(agents)  
    plot_floods_per_round(agents) 
    

    # print(houses_dict)
    # # Visualisations
    # pop = PopulationGeneratorRandom()
    # pop.agents = agents          
    # pop.plot_population_size()
    # pop.plot_wealth_distribution()
    






