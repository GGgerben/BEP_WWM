import matplotlib.pyplot as plt

def visualize_agent(agent):
    """
    Simple visualization of an agent's damage costs, protection, and adopted measures.
    """
    fig, axs = plt.subplots(1, 3, figsize=(14, 4))
    fig.suptitle(f"Agent {agent.ID} Overview", fontsize=14, fontweight="bold")

    # --- 1. Damage over time ---
    if agent.damage_history:
        rounds = list(range(1, len(agent.damage_history) + 1))
        costs = [d["cost"] if isinstance(d, dict) else d for d in agent.damage_history]
        axs[0].plot(rounds, costs, marker='o', color='tab:red')
        axs[0].set_title("Damage cost per round (€)")
        axs[0].set_xlabel("Round")
        axs[0].set_ylabel("Cost (€)")
    else:
        axs[0].text(0.5, 0.5, "No damage data", ha='center', va='center')

    # --- 2. Protection bars ---
    protection = agent.protection
    axs[1].bar(["Rain", "River"], 
               [protection["rain_protection"], protection["river_protection"]],
               color=['tab:blue', 'tab:green'])
    axs[1].set_title("Current protection")
    axs[1].set_ylim(0, max(protection.values()) + 1)

    # --- 3. Measures list ---
    axs[2].axis("off")
    if agent.adopted_measures:
        measures_text = "\n".join([m.name for m in agent.adopted_measures])
    else:
        measures_text = "No measures adopted"
    axs[2].text(0.5, 0.5, measures_text, ha='center', va='center', fontsize=10)
    axs[2].set_title("Implemented measures")

    plt.tight_layout()
    plt.show()