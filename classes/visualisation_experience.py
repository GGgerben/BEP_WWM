# visualisation_experience.py
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from population_generator import PopulationGeneratorRandom
from measures import measures


def plot_avg_adoption_by_experience(agents):
    total_per_exp = {}
    count_per_exp = {}

    for ag in agents:
        exp = ag.experience_level
        if exp not in total_per_exp:
            total_per_exp[exp] = 0
            count_per_exp[exp] = 0

        total_per_exp[exp] += len(ag.adopted_measures)
        count_per_exp[exp] += 1

    avg_per_exp = {
        exp: total_per_exp[exp] / count_per_exp[exp]
        for exp in total_per_exp
        if count_per_exp[exp] > 0
    }

    ordered_labels = ["Nooit", "Een keer", "Vaker"]
    labels = [lbl for lbl in ordered_labels if lbl in avg_per_exp]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, [avg_per_exp[lbl] for lbl in labels])
    plt.title("Gemiddeld aantal geadopteerde maatregelen per ervaringsniveau")
    plt.xlabel("Ervaringsniveau")
    plt.ylabel("Gemiddeld aantal maatregelen per agent")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    
    pop = PopulationGeneratorRandom()
    pop.create_population(100)  # hier aantal agenten bepalen

    agents = pop.get_agents()

    
    for ag in agents:
        ag.buy_improvements(measures)

    
    plot_avg_adoption_by_experience(agents)
