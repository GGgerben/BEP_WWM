# -*- coding: utf-8 -*-
import random
import matplotlib.pyplot as plt
from classes.homeowner_agent import Agent


class PopulationGeneratorRandom:
    """
    Genereert een populatie van agents met willekeurige eigenschappen
    """

    def __init__(self):
        self.agents = []

    def create_population(self, n_agents: int):
        """
        Maakt n_agents met random variatie in alle belangrijke attributen.
        """
        exp_levels = ["Nooit", "Een keer", "Vaker"]

        for i in range(1, n_agents + 1):
            wealth = random.uniform(5_000, 25_000)              # �5k�25k
            income = random.uniform(1_200, 3_000)               # �1.2k�3k
            risk_perception = random.uniform(0.1, 0.9)
            experience_level = random.choice(exp_levels)
            self_efficacy = random.uniform(0.3, 0.9)
            outcome_efficacy = random.uniform(0.3, 0.9)
            intention = random.uniform(0.1, 0.9)

            a = Agent(
                ID=i,
                wealth=wealth,
                income=income,
                risk_perception=risk_perception,
                experience_level=experience_level,
                self_efficacy=self_efficacy,
                outcome_efficacy=outcome_efficacy,
                intention=intention,
                house=f"H{i}",
            )

            self.agents.append(a)

        print(f"{len(self.agents)} agents succesvol aangemaakt.")

    def plot_population_size(self):
        """
        Maakt een staafdiagram van het aantal aangemaakte agents.
        """
        n = len(self.agents)
        plt.figure(figsize=(4, 3))
        plt.bar(["Aantal agents"], [n])
        plt.title(f"Populatiegrootte: {n} agents")
        plt.ylim(0, max(1, n + 1))
        plt.tight_layout()
        plt.show()

    def plot_wealth_distribution(self, bins: int = 10):
        """
        Maakt een histogram van de welvaart (wealth) van alle agents.
        """
        if not self.agents:
            print("Geen agents om te plotten. Maak eerst een populatie aan.")
            return

        wealth_values = [a.wealth for a in self.agents]

        plt.figure(figsize=(6, 4))
        plt.hist(wealth_values, bins=bins, edgecolor='black')
        plt.title("Verdeling van welvaart onder agenten")
        plt.xlabel("Wealth (euro)")
        plt.ylabel("Aantal agenten")
        plt.tight_layout()
        plt.show()

    def get_agents(self):
        return self.agents

    def reset(self):
        """Leeg de populatie."""
        self.agents = []


# # ====== TESTJE ======
# if __name__ == "__main__":
#     pop = PopulationGeneratorRandom()
#     pop.create_population(100)        # hier aangeven hoeveel agenten we willen
#     pop.plot_population_size()        # 1: laat zien hoeveel agenten er zijnn
#     pop.plot_wealth_distribution()    # 2: laat de verdeling van welvaart zien
