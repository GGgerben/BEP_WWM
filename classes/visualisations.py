from homeowner_agent import Agent
from measures import measures
import matplotlib.pyplot as plt

# 1️⃣  Maak een paar testagents aan
a1 = Agent(1, 1000, 1000, 0.5, "Een keer", 0.7, 0.8, 0.6, "huis1")
a2 = Agent(2, 800, 800, 0.3, "Nooit", 0.4, 0.6, 0.2, "huis2")
a3 = Agent(3, 2000, 2000, 0.9, "Vaker", 0.9, 0.9, 0.9, "huis3")

# 2️⃣  Laat ze wat maatregelen adopteren (nepdata, gewoon om te testen)
a1.adopted_measures = [measures[0]]
a2.adopted_measures = [measures[0], measures[1]]
a3.adopted_measures = [measures[1]]

agents = [a1, a2, a3]

# 3️⃣  Tel hoeveel keer elke maatregel is gekozen
adoption_counts = {m.name: 0 for m in measures}

for agent in agents:
    for adopted in getattr(agent, "adopted_measures", []):
        if adopted.name in adoption_counts:
            adoption_counts[adopted.name] += 1

# 4️⃣  Plot een simpele staafgrafiek
x = list(adoption_counts.keys())
y = list(adoption_counts.values())

plt.figure(figsize=(7, 4))
plt.bar(x, y, color="lightgreen")
plt.title("Aantal adopties per maatregel (test)")
plt.xlabel("Measures")
plt.ylabel("Aantal adopties")
plt.xticks(rotation=30, ha="right")

plt.tight_layout()
plt.show()
