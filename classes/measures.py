class Measure():
    def __init__(self, name, cost, repeatable, rain_protection, river_protection, satisfaction, subsidy_percentage):
        
        """
        Represents a flood protection or adaptation measure that players can buy 
        to reduce flood risk or increase satisfaction in the simulation.

        Attributes:
            name (str): Name of the measure.
            cost (float): One-time purchase or installation cost in euros.
            repeatable (int): Number of simulation rounds the measure remains effective.
            protection_rain (float): Effectiveness against pluvial (rain) flooding.
            protection_river (float): Effectiveness against fluvial (river) flooding.
            satisfaction (int): Satisfaction points gained by purchasing this measure.
            remaining_rounds (int): Remaining rounds of effectiveness before expiration.
        """

        self.name = name
        self.cost = cost
        self.repeatable = repeatable
        self.protection_rain = rain_protection
        self.protection_river = river_protection
        self.satisfaction = satisfaction
        self.remaining_rounds = repeatable
        self.subsidy_percentage =  subsidy_percentage

    def __repr__(self):
        return f"Measure({self.name!r})"


measures = [
    Measure("Personal improvements",         cost= 12000, repeatable= True, rain_protection=0, river_protection=0, satisfaction=1, subsidy_percentage=0.0),
    Measure("Modest house renovations",      cost= 12000, repeatable= True, rain_protection=0, river_protection=0, satisfaction=1, subsidy_percentage=0.0),
    Measure("Structual house changes",       cost= 12000, repeatable= True, rain_protection=0, river_protection=0, satisfaction=1, subsidy_percentage=0.0),
    Measure("Flood insurance",               cost= 6000, repeatable= True, rain_protection= 0, river_protection=0, satisfaction=1, subsidy_percentage=0.0),
    Measure("Water pump",                    cost= 6000, repeatable= False, rain_protection=1, river_protection=0, satisfaction=0, subsidy_percentage=0.5),
    Measure("Self-activating wall",          cost= 12000, repeatable= False, rain_protection=1, river_protection=1, satisfaction=0, subsidy_percentage=0.0),
    Measure("Sandbags",                      cost= 3000, repeatable= False, rain_protection=0, river_protection=1, satisfaction=0, subsidy_percentage=0.0),
    Measure("Waterproofing walls & floors",  cost=20000, repeatable= False, rain_protection=1, river_protection=1, satisfaction=1, subsidy_percentage=0.0),
    Measure("Green garden",                  cost=12000, repeatable= False, rain_protection=1, river_protection=0, satisfaction=1, subsidy_percentage=0.0),
    Measure("Rain barrel",                   cost=20000, repeatable= False, rain_protection=1, river_protection=0, satisfaction=1, subsidy_percentage=0.0),
]


