# visualisations_measures.py
import matplotlib.pyplot as plt
from population_generator import PopulationGeneratorRandom
from measures import measures


class VisualisationsMeasures:
    def __init__(self, figsize=(10, 5)):
        self.figsize = figsize

    def plot_adoption_per_measure(self, agents, measures):
        adoption_counts = {m.name: 0 for m in measures}

        for agent in agents:
            adopted_list = getattr(agent, "adopted_measures", [])
            for m in adopted_list:
                name = getattr(m, "name", str(m))
                if name in adoption_counts:
                    adoption_counts[name] += 1
                else:
                    adoption_counts[name] = 1

        labels = list(adoption_counts.keys())
        values = list(adoption_counts.values())

        plt.figure(figsize=self.figsize)
        plt.bar(labels, values)
        plt.title("Adoptie per maatregel")
        plt.xlabel("Maatregel")
        plt.ylabel("Aantal agents dat het kocht")
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # populatie maken
    pop = PopulationGeneratorRandom()
    pop.create_population(100)
    agents = pop.get_agents()

    #laat iedereen kopen
    for ag in agents:
        ag.buy_improvements(measures)

    # plot
    viz = VisualisationsMeasures()
    viz.plot_adoption_per_measure(agents, measures)
