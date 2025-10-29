class Measure():
    def __init__(self, name, cost, durability, protection_rain, protection_river, satisfaction, maintenance_cost=0):
        
        """
        Represents a flood protection or adaptation measure that players can buy 
        to reduce flood risk or increase satisfaction in the simulation.

        Attributes:
            name (str): Name of the measure.
            cost (float): One-time purchase or installation cost in euros.
            durability (int): Number of simulation rounds the measure remains effective.
            protection_rain (float): Effectiveness against pluvial (rain) flooding.
            protection_river (float): Effectiveness against fluvial (river) flooding.
            satisfaction (int): Satisfaction points gained by purchasing this measure.
            maintenance_cost (float): Optional recurring cost per round in euros.
            remaining_rounds (int): Remaining rounds of effectiveness before expiration.
        """

        self.name = name
        self.cost = cost
        self.durability = durability
        self.protection_rain = protection_rain
        self.protection_river = protection_river
        self.satisfaction = satisfaction
        self.maintenance_cost = maintenance_cost
        self.remaining_rounds = durability

measures = [
    Measure("Personal improvements",         cost= 8000, durability=1, protection_rain=0, protection_river=0, satisfaction=1),
    Measure("Modest house renovations",      cost= 8000, durability=1, protection_rain=0, protection_river=0, satisfaction=1),
    Measure("Structual house changes",       cost= 8000, durability=1, protection_rain=0, protection_river=0, satisfaction=1),
    Measure("Water pump",                    cost= 6000, durability=4, protection_rain=1, protection_river=0, satisfaction=0),
    Measure("Self-activating wall",          cost=12000, durability=4, protection_rain=1, protection_river=1, satisfaction=0),
    Measure("Sandbags",                      cost= 3000, durability=4, protection_rain=0, protection_river=1, satisfaction=0),
    Measure("Waterproofing walls & floors",  cost=20000, durability=4, protection_rain=1, protection_river=1, satisfaction=1),
    Measure("Green garden",                  cost=12000, durability=4, protection_rain=1, protection_river=0, satisfaction=1),
    Measure("Rain barrel",                   cost=20000, durability=4, protection_rain=1, protection_river=0, satisfaction=1),
    Measure("Flood insurance",               cost=15000, durability=4, protection_rain=1, protection_river=0, satisfaction=0),
]

# testen
# if __name__ == "__main__":
#     print(f"Number of measures: {len(measures)}")

#     for m in measures:
#         print(f"{m.name}: cost €{m.cost}, rain={m.protection_rain}, river={m.protection_river}, satisfaction={m.satisfaction}")
