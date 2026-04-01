# ------------------------------------------------------------
#
# Controleert de convergentie van het model.
# Door meerdere onafhankelijke runs uit te voeren wordt het cumulatief gemiddelde
# van de modeloutput (satisfaction) berekend om te toetsen
# of de uitkomst stabiliseert bij toenemend aantal simulaties.
#
# ------------------------------------------------------------

from model import run_single_simulation # Hier wordt namelijk gemiddelde satisfaction bepaald
import matplotlib.pyplot as plt

N_RUNS = 200

results = []
running_mean = []

for i in range(1, N_RUNS + 1):
    out = run_single_simulation(seed=i, n_agents=100) #hier komt de gemiddelde satisfaction uit
    results.append(out)
    running_mean.append(sum(results) / len(results))

plt.figure()
plt.plot(range(1, N_RUNS + 1), running_mean)
plt.xlabel("Number of model runs")
plt.ylabel("Running mean of final satisfaction")
plt.title("Convergence of model output")
plt.grid()
plt.show()

