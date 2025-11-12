from classes.environment import Environment # type: ignore
from classes.homeowner_agent import Agent # type: ignore
from classes.measures import measures # type: ignore
from classes.hazard_generator import floods # type: ignore

# Import houses
from data.houses_dict import houses_dict # type: ignore

if __name__ == "__main__":

    # Initialize test agent
    test_agent = Agent(
        ID=1,
        wealth=40000, 
        income=25000,            
        risk_perception=1,        
        experience_level="Een keer",
        self_efficacy=1,          
        outcome_efficacy=1,       
        intention=1,
        house= None)
    
    # Get flood results
    flood_results = floods()

    # Execute one simulation step
    test_agent.step(houses_dict, measures, flood_results)

  
    # print(test_agent.protection)
    # print(test_agent.satisfaction)
    # print(flood_results)
    # print(test_agent.mortgage)
    # print(test_agent.adopted_measures)
    # print(test_agent.wealth)


