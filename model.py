from classes.environment import Environment # type: ignore
from classes.homeowner_agent import Agent # type: ignore
from classes.measures import measures # type: ignore
from classes.hazard_generator import floods # type: ignore
from classes.initialisation import initialise_agents # type: ignore

from classes.population_generator import PopulationGeneratorRandom

# Import houses
from data.houses_dict import houses_dict # type: ignore

if __name__ == "__main__":


    # Initialize test agent
    agents = initialise_agents()
    
    
    # Get flood results
    flood_results = floods()

    # Execute one simulation step
    for agent in agents:
        agent.step(houses_dict, measures, flood_results)
        print(agent.house)
        print(agent.adopted_measures)

    # Visualisations
    pop = PopulationGeneratorRandom()
    pop.agents = agents          
    pop.plot_population_size()
    pop.plot_wealth_distribution()




