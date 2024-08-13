import random


class Particle:
    def __init__(self, spawnx, spawny, directionx, directiony):
        # spawn, Richtung
        self.spawnx = spawnx
        self.spawny = spawny
        self.directionx = directionx
        self.directiony = directiony

    @staticmethod
    # Erzeugt eine Population von Partikeln, nur Spawn and Richtung
    def createpopulation(numbers):
        poplist = []
        for i in range(0, numbers):
            # Spawn Koordianten
            spawnx = round(random.uniform(-280, 280))
            spawny = round(random.uniform(-260, 260))
            # Direction Koordinaten/ Gleichzeitig speed
            directx = round(random.uniform(-1, 1), 2)
            directy = round(random.uniform(-1, 1), 2)
            poplist.append(Particle(spawnx, spawny, directx, directy))
        return poplist
