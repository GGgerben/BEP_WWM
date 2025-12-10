class Subsidy:

    """
    Represents a one-time subsidy that increases an agent's wealth.
    """

    def __init__(self, measure, subsidy_percentage = 0.5, active_round = 2):
        # Fixed subsidy amount
        self.amount = measure.cost * subsidy_percentage
        self.active_round = active_round

    def apply(self, agent, current_round):
        # Give the subsidy to the agent
        if self.active_round == current_round:
            agent.wealth += self.amount


class Insurance:
    """
    Insurance model where premium depends on house value and damages can be paid out.
    """

    def __init__(self, agent, base_premium,):
        self.agent = agent
        self.base_premium = base_premium

    def calculate_premium(self, house_value):
        
        # Premium increases with house value
        factor = 1 + (house_value / 100_000) * 0.1
        premium = self.base_premium * factor

        return round(premium, 2)
    
    def apply(self, damage_history, damage_cost):

        # If flooding occurs pay damages once
        for damage in damage_history:
            if damage.get("river", 0) > 0:
                self.agent.wealth += damage_cost
                