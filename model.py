from classes.environment import Environment
from classes.HomeOwnerAgent import Agent
from classes.measures import Measure

# Import houses
from data.houses_dict import houses_dict

if __name__ == "__main__":

    # Initialize test agent
    test_agent = Agent(
        ID=1,
        wealth=25000.0,             
        risk_perception=1,        
        experience_level="Een keer",
        self_efficacy=1,          
        outcome_efficacy=1,       
        intention=1)
    
    print(test_agent)
    print(houses_dict)
