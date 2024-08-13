import random
from model.movement import Movement
#  Die Klasse erbt von der Abstract Class Movement die, die anderen Funktionen wie makemove beinhaltet. Die hier auf-
#  geführten Methoden, überschreiben die Methoden der Abstract-Class Movement


class Halfchaoticmovement(Movement):
    #  Die Hauptfunktion für die Partikelbewegung. Wenn das Teilchen sich bewegen darf, so wird als erstes Wandkollision
    #  danach Partikelkollision. Erst danach wird die Bewegung ausgeführt.
    #  Weiterhin wird je nach 300 Steps, nach einer Infektion geprüft, ob ein Partikel stirbt oder gesund wird.
    #  Dies wird mit der Methode makedeadorcured gelöst
    def movepartikel(self, population, state, stepcounter):
        self.population = population
        self.state = state
        self.counter = stepcounter
        for i in range(0, len(self.population)):
            if self.state[i].move:
                self.proofcollisionwall(i)
                self.proofcollisonpartikel(i)
                self.makemove(i)
                if (self.state[i].diseased and self.counter != self.state[i].dissince) and \
                        ((self.counter - self.state[i].dissince) % 300 == 0):
                    self.makedeadorcured(i)
            else:
                if (self.state[i].diseased and self.counter != self.state[i].dissince) and \
                        ((self.counter - self.state[i].dissince) % 300 == 0):
                    self.makedeadorcured(i)
        return self.population, self.state

    #  Abfrage der Kollision mit den Wänden: Im Fall *chaotic-Movement werden den Teilchen neue x-y Richtungen
    #  zugewiesen, unabhängig davon die Geschwindigkeit konstant zu halten. Es werden die Richtungen per Zufall
    #  bestimmt
    def proofcollisionwall(self, partid):
        if self.population[partid].spawnx <= self.SIMULATIONUNDERWALLX + 8:
            self.population[partid].directiony = round(random.uniform(-1, 1), 2)
            self.population[partid].directionx = round(random.uniform(0, 1), 2)
            # Kollision mit Upper X-Wall
        if self.population[partid].spawnx >= self.SIMULATIONUPPERWALLX - 8:
            self.population[partid].directiony = round(random.uniform(-1, 1), 2)
            self.population[partid].directionx = round(random.uniform(-1, 0), 2)
            # Kollision mit Under Y-Wall
        if self.population[partid].spawny <= self.SIMULATIONUNDERWALLY + 8:
            self.population[partid].directiony = round(random.uniform(0, 1), 2)
            self.population[partid].directionx = round(random.uniform(-1, 1), 2)
            # Kollision mit Upper Y-Wall
        if self.population[partid].spawny >= self.SIMULATIONUPPERWALLY - 8:
            self.population[partid].directiony = round(random.uniform(-1, 0), 2)
            self.population[partid].directionx = round(random.uniform(-1, 1), 2)
