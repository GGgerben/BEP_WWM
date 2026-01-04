import random

def floods(seed=None):

    """
    Simulates the occurrence of rain and river floods.

    Rain flood:  1 in 10 chance
    River flood: 1 in 12 chance
    """
    if seed is not None:
        random.seed(seed)

    rain = random.randint(1, 10)
    river = random.randint(1, 12)

    return {"rain_damage": rain, "river_damage": river}



