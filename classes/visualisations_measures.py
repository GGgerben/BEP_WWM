import matplotlib.pyplot as plt

class VisualisationsMeasures:
    """
    Maakt een staafdiagram van het aantal adopties per maatregel.
    """

    def __init__(self, figsize=(10, 5)):
        self.figsize = figsize

    def plot_adoption_per_measure(self, agents, measures):
        """
        Parameters
        ----------
        agents : list[Agent]
            Elke agent heeft .adopted_measures
        measures : list[Measure]
            De originele lijst met beschikbare maatregelen (voor de labels).
        """

        # 1. start met alle bekende maatregelen op 0
        adoption_counts = {m.name: 0 for m in measures}

        # 2. loop door alle agents en door alle measures die zij hebben
        for agent in agents:
            adopted_list = getattr(agent, "adopted_measures", [])
            for m in adopted_list:
                
                name = getattr(m, "name", str(m))
                if name in adoption_counts:
                    adoption_counts[name] += 1
                else:
                    # voor het geval er een maatregel is die niet in de originele lijst stond
                    adoption_counts[name] = 1

        # 3. zet de data klaar voor matplotlib
        labels = list(adoption_counts.keys())
        values = list(adoption_counts.values())

        # 4. plotten
        plt.figure(figsize=self.figsize)
        plt.bar(labels, values)
        plt.title("Adoption per measure")
        plt.xlabel("Measure")
        plt.ylabel("Number of agents that adopted")
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()
        plt.show()



if __name__ == "__main__":
    
    from measures import measures  

    class DummyAgent:
        def __init__(self, adopted_measures):
            self.adopted_measures = adopted_measures

    # stel: agent 1 koopt de eerste 2 measures, agent 2 alleen de eerste, agent 3 niks
    a1 = DummyAgent([measures[0], measures[7]])
    a2 = DummyAgent([measures[0]])
    a3 = DummyAgent([])

    viz = VisualisationsMeasures()
    viz.plot_adoption_per_measure([a1, a2, a3], measures)
