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
    
    def compute_flood_probability(self, house_info):

        """
        Function that calculates average rain and river probability.
        Based on:
        - rain damage 1-10
        - river damage 1-12
        """

        rain_prot = house_info.get("rain_protection", 0)
        river_prot = house_info.get("river_protection", 0)

        # P(rain_damage > rain_prot)
        rain_prob = max(0.0, min((10 - rain_prot) / 10, 1.0))

        # P(river_damage > river_prot)
        river_prob = max(0.0, min((12 - river_prot) / 12, 1.0))

        # Calculate average flood probability
        return (rain_prob + river_prob) / 2 
    
    def flood_experience_factor(self):

        """
        Define flood experience agent (score [0-1]).
        """

        if not self.damage_history:
            return 0.0
        
        # Check number of rounds played
        n = len(self.damage_history)

        # Check number of experienced floods
        experienced_floods = sum(1 for d in self.damage_history if d["damage_cost"] > 0)

        # Calculate score
        return max(0.0, min(experienced_floods / n, 1.0))
    
    def threat_appraisal_reloc(self, current_house_info):

        """
        Computes the Threat Appraisal for relocation (score [0-1]).
        Threat Appraisal = (flood probability + expected damage + flood experience)
                         – (benefits of staying)
        """
        
        # Flood probability of the current house
        flood_prob = self.compute_flood_probability(current_house_info)
    
        # Expected damage
        expected_damage = flood_prob

        # Flood experience
        experience = self.flood_experience_factor()

        # Benefits of staying, (Heuristic of staying, stay benefits between [0.2 - 0.7])
        stay_benefits = 0.2 + 0.5 * max(0.0, min(self.satisfaction, 1.0))

        # Calculate threat appraisal
        threat = flood_prob + expected_damage + experience - stay_benefits

        # Standardize threat
        return max(0.0, min(threat, 1.0))
    
    def coping_appraisal_reloc(self, current_house_info, new_house_info):

        """
        Computes the Coping Appraisal for relocation (score [0-1]).
        Coping Appraisal = (belief that relocation reduces risk + self-efficacy)
                         – response costs
        """

        # Check risk current house and new house
        risk_current = self.compute_flood_probability(current_house_info)
        risk_new = self.compute_flood_probability(new_house_info)

        # Response efficacy
        risk_reduction = max(0.0, risk_current - risk_new)

        # Determine self efficiacy
        move_cost = new_house_info["value"]

        # Calculate if agent can afford house
        if self.max_mortgage >= new_house_info["value"]:
            affordability = 1.0
        else: affordability = 0.0
        
        # If the agent can afford the move, they are capable of relocating.
        self_efficacy = affordability

        # Calculate response cost
        total_budget = self.max_mortgage
        
        response_cost = move_cost / total_budget
        response_cost = max(0.0, min(response_cost, 1.0))

        # Calculate coping appraisal
        coping= risk_reduction + self_efficacy - response_cost

        # Standardize coping appraisal
        return max(0.0, min(coping, 1.0))
    
    def relocation_PM(self, current_house_info, new_house_info):
        """
        Computes overall Protection Motivation for relocation.
        Protection Motivation = average of Threat Appraisal and Coping Appraisal,
        scaled to [0–1].
        """
        threat = self.threat_appraisal_reloc(current_house_info)
        coping = self.coping_appraisal_reloc(current_house_info, new_house_info)

        # Calculate average
        return (threat + coping) / 2
    

    def buy_house(self, houses_dict, preferred_rating = 0, relocation_threshold = 0.6, current_round = None, relocation_round = 4):

        """
        Buys a house or decides to relocate using PMT.

        Case 1: Agent has no house yet
            -> buys the first available and affordable house with sufficient rating.

        Case 2: Agent already owns a house
            -> evaluates relocation options using PMT (relocation_PM).
        """

        # Case 1 : no house yet
        
        if self.house is None:
            # Find the first suitable house

            for house_id, info in houses_dict.items():
                # Skip houses that are not available yet in this round
                if info.get("available_round", 1) > current_round:
                    continue

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
        
        # Case 2: Relocation (PMT)
        #Onnly allow relocation in round 4
        if current_round is None or current_round != relocation_round:
            # Already owns a house and it's not relocation round → do nothing
            return None
        
        print(f"[DEBUG] Agent {self.ID}: relocation check in round {current_round}")
        
        current_house_info = houses_dict[self.house]
        risk_current = self.compute_flood_probability(current_house_info)

        best_house_id = None
        best_PM = 0.0

        for house_id, info in houses_dict.items():
            # Skip the current house
            if house_id == self.house:
                continue

            # Skip unavailable houses
            if not info.get("available", True):
                continue

            # Check affordability
            if info["value"] > self.max_mortgage:
                continue

            # Only consider safer houses
            risk_current = self.compute_flood_probability(current_house_info)
            risk_new = self.compute_flood_probability(info)
            if risk_new >= risk_current:
                continue

            # Compute Protection Motivation for relocation to this house
            PM = self.relocation_PM(current_house_info, info)
            print(f"Agent {self.ID} relocation candidate {house_id}: PM={PM:.2f}")

            if PM > best_PM:
                best_PM = PM
                best_house_id = house_id

        # Decide to relocate if PM exceeds threshold
        if best_house_id is not None and best_PM > relocation_threshold:
            old_house_id = self.house

            # Free old house
            houses_dict[old_house_id]["available"] = True

            # Move to new house
            self.house = best_house_id
            self.mortgage = houses_dict[best_house_id]["value"]
            houses_dict[best_house_id]["available"] = False

            # Update protection based on new house
            new_info = houses_dict[best_house_id]
            self.protection["rain_protection"] = new_info.get("rain_protection", 0)
            self.protection["river_protection"] = new_info.get("river_protection", 0)

            return best_house_id
    
        # No relocation
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

            # Skip if this measure is already adopted (based on its name)
            if any(m.name == measure.name for m in self.adopted_measures):
                continue
        
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

    def step(self, houses_dict, measures, flood_results, current_round):
        
        """
        Executes one simulation step where the agent earns income, buys a house, pays taxes, and invests in improvements.
        """

        self.get_income()
        self.buy_house(houses_dict, current_round=current_round)
        self.pay_tax()
        self.buy_improvements(measures)
        self.check_damage(flood_results)

        # Round 3 protection decay
        if current_round == 3:
            self.protection["rain_protection"] = self.protection["rain_protection"] - 1
            self.protection["river_protection"] = self.protection["river_protection"] - 2

    
    def __repr__(self):

        return (f"Agent(ID={self.ID}, Wealth={self.wealth}, "
                f"Risk={self.risk_perception}, Exp='{self.experience_level}', "
                f"Intention={self.intention})")
