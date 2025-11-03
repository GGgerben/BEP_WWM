import random

def floods():

    """
    Simulates the occurrence of rain and river floods.

    Rain flood:  1 in 10 chance
    River flood: 1 in 12 chance
    """

    rain = random.randint(1, 10)
    river = random.randint(1, 12)

    return {"rain": rain, "river": river}
