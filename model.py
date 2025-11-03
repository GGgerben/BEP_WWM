from classes.environment import Environment
from classes.homeowner_agent import Agent 
from classes.measures import measures
from classes.hazard_generator import floods

# Import houses
from data.houses_dict import houses_dict

if __name__ == "__main__":

    # Initialize test agent
    test_agent = Agent(
        ID=1,
        wealth=40000,             
        risk_perception=1,        
        experience_level="Een keer",
        self_efficacy=1,          
        outcome_efficacy=1,       
        intention=1,
        house= None)
    
    test_agent.buy_house(houses_dict)
    test_agent.pay_tax()
    test_agent.buy_improvements(measures)

    flood_results = floods()
    print(flood_results)
    print(test_agent.mortgage)
    print(test_agent.wealth)

