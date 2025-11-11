# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

from homeowner_agent import Agent
from measures import measures


def plot_avg_adoption_by_experience(agents):
    """
    Plot de gemiddelde hoeveelheid geadopteerde maatregelen per ervaringsniveau.
    We gaan uit van agent.experience_level met waarden zoals:
    "Nooit", "Een keer", "Vaker".
    """
    total_per_exp = {}
    count_per_exp = {}

    for ag in agents:
        exp = ag.experience_level
        # init als deze ervaring nog niet voorkomt
        if exp not in total_per_exp:
            total_per_exp[exp] = 0
            count_per_exp[exp] = 0

        total_per_exp[exp] += len(ag.adopted_measures)
        count_per_exp[exp] += 1

    # gemiddelde per ervaringsniveau
    avg_per_exp = {
        exp: total_per_exp[exp] / count_per_exp[exp]
        for exp in total_per_exp
        if count_per_exp[exp] > 0
    }

    # vaste volgorde is handig
    ordered_labels = ["Nooit", "Een keer", "Vaker"]
    labels = [lbl for lbl in ordered_labels if lbl in avg_per_exp]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, [avg_per_exp[lbl] for lbl in labels])
    plt.title("Gemiddeld aantal geadopteerde maatregelen per ervaringsniveau")
    plt.xlabel("Ervaringsniveau")
    plt.ylabel("Gemiddeld aantal maatregelen per agent")
    plt.tight_layout()
    plt.show()


# ====== TESTJE ======
if __name__ == "__main__":
    # paar test-huizen, alleen nodig als je agenten een house nodig hebben
    houses = {
        "H1": {"location": "laag"},
        "H2": {"location": "hoog"},
        "H3": {"location": "hoog"},
    }

    # echte Agent uit jouw project
    a1 = Agent(
        ID=1,
        wealth=15000,
        income=2000,
        risk_perception=0.3,
        experience_level="Nooit",
        self_efficacy=0.7,
        outcome_efficacy=0.6,
        intention=0.5,
        house="H1",
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

    # laat iedereen even maatregelen kopen met jouw eigen method
    for ag in agents:
        ag.buy_improvements(measures)

    # nu plotten
    plot_avg_adoption_by_experience(agents)
