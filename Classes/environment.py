class Environment():
    
    def __init__(self, geo_risk_map, social_budget, policy_parameters, round_number = 0):

        """
        Represents the simulation environment for modeling risk levels, 
        social budgets, and policy effects over multiple rounds.

        Attributes:        
        geo_risk_map (dict): Maps location risk type (e.g., 'high', 'low') to base hazard probability.
        social_budget (dict): Maps social/wealth categories to their initial budget.
        policy_parameters (dict): Contains parameters for subsidy rates, insurance adjustments, etc.
        round_number (int): Current simulation round.
        """

        self.round_number = round_number
        self.geo_risk_map = geo_risk_map
        self.social_budget = social_budget
        self.policy_parameters = policy_parameters
    
    def next_round(self):
        """
        Advance the simulation by one round.
        """
        self.round_number += 1



# # Testen class
# geo_risk_map = {'laag': 0.2, 'hoog': 0.8}
# social_budget = {'arm': 1000, 'gemiddeld': 3000, 'rijk': 10000}
# policy_parameters = {'subsidie': 0.1}

# env = Environment(geo_risk_map, social_budget, policy_parameters)

# print("Start ronde:", env.round_number)
# print("Risicokaart:", env.geo_risk_map)
# print("Sociale budgetten:", env.social_budget)
# print("Beleidsparameters:", env.policy_parameters)

# env.next_round()
# print("Na next_round:", env.round_number)
        