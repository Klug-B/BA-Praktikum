from abc import ABC, abstractmethod
from resources.constant import Constant
import random
import math as m


class Movement(ABC, Constant):
    def __init__(self, deadchance, diseasechance, curechance, distance):
        Constant.__init__(self)
        self.population = []
        self.state = []
        self.counter = 0
        self.diseasechance = diseasechance
        self.deadchance = deadchance
        self.curechance = curechance
        self.distance = distance
        super().__init__()

        #  Einfache Abfrage der Partikelkollision mit Phytagoras

    def proofcollisonpartikel(self, partid):
        for count in range(0, len(self.population)):
            if count != partid:
                if self.state[partid].distancekeeper:
                    distance = self.PARSIZE + self.distance
                else:
                    distance = self.PARSIZE

                distancebetweenparticle = (self.population[count].spawnx - self.population[partid].spawnx) * \
                                          (self.population[count].spawnx - self.population[partid].spawnx) + \
                                          (self.population[count].spawny - self.population[partid].spawny) * \
                                          (self.population[count].spawny - self.population[partid].spawny)

                # Phytagoras für Kollision je nach Typ entweder 10 = Teilchengröße oder 10 + Abstand
                if distancebetweenparticle <= distance * distance and not self.state[count].dead:

                    if self.state[partid].distancekeeper and \
                            (self.population[partid].spawnx != self.SIMULATIONUPPERWALLX or
                             self.population[partid].spawnx != self.SIMULATIONUNDERWALLX):
                        self.population[partid].directionx = -self.population[partid].directionx
                        self.population[partid].directiony = -self.population[partid].directiony

                    if distancebetweenparticle <= self.PARSIZE * self.PARSIZE:
                        self.diseaseparticle(count, partid)

        # Erkrankungsmethode die mit einfacher Wahrscheinlichkeitsrechnung arbeitet Es wird eine pseudo Zufalsszahl
        # generiert, sollte diese Zahl < als die Ansteckungswahrscheinlichkeit * 100 sein so erkrankt das Teilchen.
        # Wenn es nicht erfüllt wird, so bleibt das Teilchen Gesund.

    def diseaseparticle(self, count, partid):
        chance = random.randint(1, 100)
        if self.state[partid].diseased and not self.state[count].cured and not self.state[count].dead and \
                chance <= self.diseasechance * 100:

            self.state[count].dissince = self.counter
            self.state[count].diseased = True

        elif self.state[count].diseased and not self.state[partid].cured and not self.state[partid].dead and \
                chance <= self.diseasechance * 100:
            self.state[partid].dissince = self.counter
            self.state[partid].diseased = True

    #  Methode, die die Teilchen sterben oder genesen lässt, arbeiten nach dem gleichem Prinzip wie diseaseparticel
    def makedeadorcured(self, partid):
        if self.state[partid].diseased:
            chance = random.randint(1, 100)
            if chance <= self.curechance * 100:
                self.state[partid].diseased = False
                self.state[partid].cured = True

            else:
                chance = random.randint(1, 100)
                if chance <= self.deadchance * 100:
                    self.state[partid].diseased = False
                    self.state[partid].dead = True
                    self.state[partid].move = False

    def makemove(self, partid):
        self.population[partid].spawnx = self.population[partid].spawnx + self.population[partid].directionx
        self.population[partid].spawny = self.population[partid].spawny + self.population[partid].directiony

    #  Abstract-Methoden die von den jeweiligen Subclasse, bei Benutzung überschrieben werden.
    @abstractmethod
    def movepartikel(self, population, state, stepcounter):
        pass

    @abstractmethod
    def proofcollisionwall(self, partid):
        pass

    @staticmethod
    def wallchangesameabs(direction, absnumber):
        return round(m.sqrt(absnumber - (direction * direction)), 2)
