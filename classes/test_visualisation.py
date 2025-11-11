import matplotlib.pyplot as plt
from collections import defaultdict

def plot_adoption_by_experience(agents):
    counts = defaultdict(int)
    for a in agents:
        counts[a.experience_level] += len(a.adopted_measures)

    plt.bar(counts.keys(), counts.values())
    plt.title("Aantal geadopteerde maatregelen per ervaringsniveau")
    plt.xlabel("Ervaringsniveau")
    plt.ylabel("Aantal geadopteerde maatregelen")
    plt.show()


