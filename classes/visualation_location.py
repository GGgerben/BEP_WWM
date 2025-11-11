# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from homeowner_agent import Agent
from measures import measures


def plot_avg_adoption_by_location(agents, houses_dict):
    """
    Berekent en plot de GEMIDDELDE hoeveelheid geadopteerde maatregelen
    per locatie (bijv. 'laag' en 'hoog'), op basis van:
    - agent.house   -> een house-id (string)
    - houses_dict   -> dict met o.a. 'location'
    """
    location_totals = {}   # som van maatregelen per locatie
    location_counts = {}   # aantal agents per locatie

    for ag in agents:
        house_id = ag.house
        house_info = houses_dict.get(house_id)

        # als een agent geen geldig huis heeft, slaan we 'm over
        if house_info is None:
            continue

        loc = house_info["location"]   # bv. "laag" of "hoog"

        # tel maatregelen van deze agent
        location_totals[loc] = location_totals.get(loc, 0) + len(ag.adopted_measures)
        location_counts[loc] = location_counts.get(loc, 0) + 1

    # nu gemiddelde per locatie
    avg_per_location = {
        loc: location_totals[loc] / location_counts[loc]
        for loc in location_totals
    }

    # plotten
    plt.figure(figsize=(6, 4))
    plt.bar(avg_per_location.keys(), avg_per_location.values())
    plt.title("Gemiddeld aantal geadopteerde maatregelen per locatie")
    plt.xlabel("Locatie")
    plt.ylabel("Gemiddeld aantal maatregelen per agent")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
   
    houses = {
        "H1": {
            "location": "laag",
            "available": False,
            "value": 200000,
            "preferred_rating": 1,
            "rain_protection": 0,
            "river_protection": 0,
        },
        "H2": {
            "location": "hoog",
            "available": False,
            "value": 210000,
            "preferred_rating": 1,
            "rain_protection": 0,
            "river_protection": 0,
        },
        "H3": {
            "location": "hoog",
            "available": False,
            "value": 190000,
            "preferred_rating": 1,
            "rain_protection": 0,
            "river_protection": 0,
        },
    }

    # 2. maak wat agents met jouw échte constructor
    a1 = Agent(
        ID=1,
        wealth=15000,
        income=2000,
        risk_perception=0.3,
        experience_level="Nooit",
        self_efficacy=0.7,
        outcome_efficacy=0.6,
        intention=0.5,
        house="H1",          # koppeling naar houses["H1"]
    )
    a2 = Agent(
        ID=2,
        wealth=25000,
        income=2200,
        risk_perception=0.5,
        experience_level="Een keer",
        self_efficacy=0.8,
        outcome_efficacy=0.7,
        intention=0.6,
        house="H2",
    )
    a3 = Agent(
        ID=3,
        wealth=8000,
        income=1800,
        risk_perception=0.4,
        experience_level="Vaker",
        self_efficacy=0.5,
        outcome_efficacy=0.6,
        intention=0.4,
        house="H3",
    )

    agents = [a1, a2, a3]

    
    for ag in agents:
        ag.buy_improvements(measures)

    # 4. plotten
    plot_avg_adoption_by_location(agents, houses)
