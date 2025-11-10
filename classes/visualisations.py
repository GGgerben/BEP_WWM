import matplotlib.pyplot as plt

class Visualization:
    """
    Helper class for visualizing results from the ABM.
    Supports: bar chart of measure adoption counts or rates.
    """

    def __init__(self, figsize=(10, 5)):
        self.figsize = figsize

    def plot_measure_adoption(self, agents, measures, title="Adoption per measure", save_path=None):
        """
        Creates a bar chart showing adoption count (or rate) per measure.

        Parameters
        ----------
        agents : list[Agent]
            List of Agent objects from the simulation.
        measures : list[Measure]
            The original list of available measures (for labels).
        title : str
            Title above the chart.
        save_path : str | None
            If given, saves the figure to that path instead of showing it.
        """

        # 1. Initialize counter for all measures
        adoption_counts = {m.name: 0 for m in measures}

        # 2. Count adoptions from agents
        for agent in agents:
            for m in agent.adopted_measures:
                if m.name in adoption_counts:
                    adoption_counts[m.name] += 1
                else:
                    adoption_counts[m.name] = 1  # handle unknown measures safely

        # 3. Compute adoption rate (% of agents)
        total_agents = len(agents)
        adoption_rates = {name: (count / total_agents) * 100 for name, count in adoption_counts.items()}

        # 4. Plot
        plt.figure(figsize=self.figsize)
        plt.bar(adoption_rates.keys(), adoption_rates.values())
        plt.xticks(rotation=45, ha='right')
        plt.ylabel("Adoption rate (%)")
        plt.title(title)
        plt.tight_layout()

        # 5. Show or save
        if save_path:
            plt.savefig(save_path, dpi=300)
            plt.close()
        else:
            plt.show()