class Measure():
    """
    Flood adaptation or protection measure available to household agents.

    Measures can reduce pluvial and/or fluvial flood risk and/or
    increase household satisfaction. Some measures are repeatable,
    others can only be adopted once.
    """

    def __init__(self, name, cost, repeatable, rain_protection, river_protection, satisfaction, subsidy_percentage):
        """
        Initialise a flood adaptation measure.

        Args:
            name (str): Name of the measure.
            cost (float): Purchase or installation cost (€).
            repeatable (bool): Whether the measure can be adopted multiple times.
            rain_protection (int): Reduction in pluvial flood damage.
            river_protection (int): Reduction in fluvial flood damage.
            satisfaction (int): Satisfaction points gained when adopted.
            subsidy_percentage (float): Fraction of cost paid by the agent (0–1).
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

# List of available flood adaptation measures
measures = [
    Measure("Personal improvements",         cost= 12000, repeatable= True, rain_protection=0, river_protection=0, satisfaction=1, subsidy_percentage=0.0),
    Measure("Modest house renovations",      cost= 12000, repeatable= True, rain_protection=0, river_protection=0, satisfaction=1, subsidy_percentage=0.0),
    Measure("Structual house changes",       cost= 12000, repeatable= True, rain_protection=0, river_protection=0, satisfaction=1, subsidy_percentage=0.0),
    Measure("Flood insurance",               cost= 6000, repeatable= True, rain_protection= 0, river_protection=0, satisfaction=1, subsidy_percentage=0.0),
    Measure("Water pump",                    cost= 6000, repeatable= False, rain_protection=1, river_protection=0, satisfaction=0, subsidy_percentage=0.0),
    Measure("Self-activating wall",          cost= 12000, repeatable= False, rain_protection=1, river_protection=1, satisfaction=0, subsidy_percentage=0.0),
    Measure("Sandbags",                      cost= 3000, repeatable= False, rain_protection=0, river_protection=1, satisfaction=0, subsidy_percentage=0.0),
    Measure("Waterproofing walls & floors",  cost=20000, repeatable= False, rain_protection=1, river_protection=1, satisfaction=1, subsidy_percentage=0.0),
    Measure("Green garden",                  cost=12000, repeatable= False, rain_protection=1, river_protection=0, satisfaction=1, subsidy_percentage=0.0),
    Measure("Rain barrel",                   cost=20000, repeatable= False, rain_protection=1, river_protection=0, satisfaction=1, subsidy_percentage=0.0),
]


