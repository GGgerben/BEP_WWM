# visualation_location.py
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from population_generator import PopulationGeneratorRandom
from measures import measures


def plot_avg_adoption_by_location(agents, houses_dict):
    location_totals = {}
    location_counts = {}

    for ag in agents:
        house_id = ag.house
        house_info = houses_dict.get(house_id)
        if house_info is None:
            continue

        loc = house_info["location"]

        location_totals[loc] = location_totals.get(loc, 0) + len(ag.adopted_measures)
        location_counts[loc] = location_counts.get(loc, 0) + 1

    avg_per_location = {
        loc: location_totals[loc] / location_counts[loc]
        for loc in location_totals
    }

    plt.figure(figsize=(6, 4))
    plt.bar(avg_per_location.keys(), avg_per_location.values())
    plt.title("Gemiddeld aantal geadopteerde maatregelen per locatie")
    plt.xlabel("Locatie")
    plt.ylabel("Gemiddeld aantal maatregelen per agent")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # populatie maken
    pop = PopulationGeneratorRandom()
    pop.create_population(100)  
    agents = pop.get_agents()

    # Hier nu even huizen-dict gemaakt dat past bij aantal agents maar moet later refereren naar huizen excel!
    # helft laag, helft hoog
    houses = {}
    for idx, ag in enumerate(agents, start=1):
        houses[f"H{idx}"] = {
            "location": "laag risico" if idx <= len(agents) // 2 else "hoog risico",
            "available": False,
            "value": 200000,
            "preferred_rating": 1,
            "rain_protection": 0,
            "river_protection": 0,
        }

    # laat alle agents maatregelen kopen
    for ag in agents:
        ag.buy_improvements(measures)

    #plotten
    plot_avg_adoption_by_location(agents, houses)
