from visualisations import Visualization
from measures import measures
from homeowner_agent import Agent

# Example test agents
a1 = Agent(1, 5000, 1000, 0.5, "Nooit", 0.7, 0.8, 0.6, "A")
a2 = Agent(2, 3000, 800, 0.6, "Een keer", 0.6, 0.7, 0.5, "B")

# Let them adopt some measures
a1.adopted_measures = [measures[0], measures[3]]
a2.adopted_measures = [measures[3]]

# Create and show chart
viz = Visualization()
viz.plot_measure_adoption([a1, a2], measures)

