# ------------------------------------------------------------
#
# Initialiseert een agentpopulatie voor scenario-experimenten
# (Wealth × Experience × Aantal agenten),
# gebaseerd op 8 vaste profielen
#
# ------------------------------------------------------------

import random
from classes.initialisation import initialise_agents
from classes.homeowner_agent import Agent

# Wealth op basis van 8 vaste profielen, dus als een scenario met arm wordt gekozen is elke agent of p1 of p3
PROFILES_BY_WEALTH = {
    "Arm": ["p1", "p3"],
    "Gemiddeld": ["p2", "p4", "p5", "p7"],
    "Rijk": ["p6", "p8"],
}

# Experience = aantal keer schade geleden/ aantal rondes
EXPERIENCE_FACTOR = {
    "Nooit": 0.0,
    "Een keer": 0.25,
    "Vaker dan een keer": 0.75
}

#hier komt nu het nulalternatief

def initialise_scenario_population(
        n=100,
        seed=42,
        wealth_class="Gemiddeld",
        experience_level="Nooit"
):
    """
    Creeert specifiek scenario.
    """

    random.seed(seed)

    base_agents = initialise_agents()  #vaste 8 profielen uit de initialise class

    
    base_dict = {a.ID: a for a in base_agents}

    allowed_ids = PROFILES_BY_WEALTH[wealth_class] #neemt alleen de profielen die gekozen zijn voor in het te runnen scenario

    agents = []

    for i in range(n):
        chosen_id = random.choice(allowed_ids) #random keuze uit player profiles die voldoen aan rijk, arm, gemiddeld
        template = base_dict[chosen_id] # maak een lijst met alle profielen die van toepassing zijn

        # Maak nieuwe agent met dezelfde eigenschappen
        agent = Agent(
            ID=f"a{i+1}",
            wealth=template.wealth,
            income=template.income,
            experience_level=experience_level, #dus dit kan nog aangepast worden bij runnen van de scenario's
            self_efficacy=template.self_efficacy, #neem die van het originale player profile
            house=None,
            params={"experience_source": "scenario"}  # experience is een scenario-instelling en niet afkomstig uit eerdere runs
        )

        agent.max_mortgage = template.max_mortgage
        agent.preferred_rating = template.preferred_rating

        agents.append(agent)

    return agents
