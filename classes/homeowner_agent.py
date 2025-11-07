class Agent:
    def __init__(self, ID, wealth, income, risk_perception, experience_level,
                 self_efficacy, outcome_efficacy, intention, house):
        
        """
        Represents a household agent.

        Attributes:
            ID (int): Unique identifier per agent.
            wealth (float): Initial budget in euros (€), determined by social class ('rijk', 'gemiddeld', or 'arm').
            income (float): Income in euros (€)
            risk_perception (float): Perceived flood probability and damage risk (0–1).
            experience_level (str): Flood experience: 'Nooit', 'Een keer', or 'Vaker'.
            self_efficacy (float): Belief in own ability to implement measures (0–1).
            outcome_efficacy (float): Belief that measures effectively reduce damage (0–1).
            intention (float): Motivational level derived from PMT and MAP (0–1).
            house (string): House id.
        """

        self.ID = ID
        self.wealth = wealth
        self.income = income
        self.risk_perception = risk_perception
        self.experience_level = experience_level
        self.self_efficacy = self_efficacy
        self.outcome_efficacy = outcome_efficacy
        self.intention = intention
        self.house = house

        # Dynamic attributes updated during simulation
        self.adopted_measures = []     # List of Measure objects
        self.satisfaction = 0.0        # Updated after each round
        self.damage_history = []       # List of booleans (True = flooded)
        self.max_mortgage = self.wealth * 10
        self.mortgage = None
        self.protection = {"rain_protection": 0, "river_protection": 0}
    
    def get_income(self):

        """
        Function that allows an agent to get income.
        """
        self.wealth += self.income
    
    def buy_house(self, houses_dict, preferred_rating = 0):

        """
        Function that allows agent to buy the first available and affordable house that meets the preferred rating.
        """

        if self.house is not None:
            print(f"Agent {self.ID} already bought a house ({self.house}).")
            return None
        
        # Find the first suitable house
        for house_id, info in houses_dict.items():
            if info["available"] and info["value"] <= self.max_mortgage and info["preferred_rating"] >= preferred_rating:
                self.house = house_id
                self.mortgage = info["value"]
                houses_dict[house_id]["available"] = False

                # Update protection based on the house
                self.protection["rain_protection"] += info.get("rain_protection", 0)
                self.protection["river_protection"] += info.get("river_protection", 0)
                
                # Return suitable house
                return house_id
        
        # Return None if no suitable house is found
        return None
    
    def pay_tax(self):

        """
        Pays 10% of the current mortgage.
        """

        payment = 0.1 * self.mortgage
        self.wealth -= payment
        self.mortgage -= payment

    def buy_improvements(self, measures):
        
        """
        Buys as many affordable measures as possible from the given list.
        Each measure has a 'cost' attribute.
        """
        
        for measure in measures:
        
            if self.wealth >= measure.cost:
                # Pay for the measure
                self.wealth -= measure.cost

                # Add the measure to the agent's list
                self.adopted_measures.append(measure)

                 # Update protections cumulatively
                self.protection["rain_protection"] += getattr(measure, "protection_rain", 0)
                self.protection["river_protection"] += getattr(measure, "protection_river", 0)

                # Update satisfaction
                self.satisfaction += getattr(measure, "satisfaction", 0)

            #     print(f"Agent {self.ID} bought {measure.name} for €{measure.cost}.")
            # else:
            #     print(f"Agent {self.ID} cannot afford {measure.name}.")

    def check_damage(self, flood_results):

        """
        Calculates and applies flood damage based on the agent's protection levels.
        """

        # Fixed damage costs per damage point
        damage_costs = 4000
        
        # calculate difference between damage and protection (never negative)
        rain_diff  = max(0, flood_results.get("rain_damage", 0)  - self.protection["rain_protection"])
        river_diff = max(0, flood_results.get("river_damage", 0) - self.protection["river_protection"])
        
        # Calculate total costs
        total = damage_costs * (rain_diff + river_diff)

        # Pay total costs
        self.wealth -= total

        # Save damage history
        self.damage_history.append({"rain": rain_diff, "river": river_diff, "damage_cost": total})

    
    def __repr__(self):

        return (f"Agent(ID={self.ID}, Wealth={self.wealth}, "
                f"Risk={self.risk_perception}, Exp='{self.experience_level}', "
                f"Intention={self.intention})")
