from model.movement import Movement
import random
#  Die Klasse erbt von der Abstract Class Movement die, die anderen Funktionen wie makemove beinhaltet. Die hier auf-
#  geführten Methoden, überschreiben die Methoden der Abstract-Class Movement


class Linaermovement(Movement):
    #  Die Hauptfunktion für die Partikelbewegung. Wenn das Teilchen sich bewegen darf, so wird als erstes Wandkollision
    #  danach Partikelkollision. Erst danach wird die Bewegung ausgeführt.
    #  Weiterhin wird je nach 300 Steps, nach einer Infektion geprüft, ob ein Partikel stirbt oder gesund wird.
    #  Dies wird mit der Methode makedeadorcured gelöst
    def movepartikel(self, population, state, stepcounter):
        self.population = population
        self.state = state
        self.counter = stepcounter
        for i in range(0, len(population)):
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

    # Kollision mit Under X-Wall Die Whileschleife prüft ob das neue Quadrat der randiom zugewiesen richtung
    # nicht zu groß ist, ansonsten wird es solange verkleinert bis es funktioniert
    # Beginnt mit der UnderXWall
    def proofcollisionwall(self, partid):

        pythagoc = round(self.population[partid].directionx * self.population[partid].directionx +
                         self.population[partid].directiony * self.population[partid].directiony, 2)
        divider = 1

        if self.population[partid].spawnx <= self.SIMULATIONUNDERWALLX + 8:
            self.population[partid].directiony = round(random.uniform(-1, 1), 2)
            while pythagoc < (self.population[partid].directiony * divider) * \
                    (self.population[partid].directiony * divider):
                divider = divider - 0.1

            self.population[partid].directiony = self.population[partid].directiony * divider
            divider = 1
            self.population[partid].directionx = self.wallchangesameabs(self.population[partid].directiony,
                                                                        pythagoc)

            # Kollision mit Upper X-Wall
        if self.population[partid].spawnx >= self.SIMULATIONUPPERWALLX - 8:
            self.population[partid].directiony = round(random.uniform(-1, 1), 2)
            while pythagoc < (self.population[partid].directiony * divider) * \
                    (self.population[partid].directiony * divider):
                divider = divider - 0.1

            self.population[partid].directiony = self.population[partid].directiony * divider
            divider = 1
            self.population[partid].directionx = -self.wallchangesameabs(self.population[partid].directiony,
                                                                         pythagoc)

        # Kollision mit Under Y-Wall
        if self.population[partid].spawny <= self.SIMULATIONUNDERWALLY + 8:
            self.population[partid].directionx = round(random.uniform(-1, 1), 2)
            while pythagoc < (self.population[partid].directionx * divider) * \
                    (self.population[partid].directionx * divider):
                divider = divider - 0.1

            self.population[partid].directionx = self.population[partid].directionx * divider
            divider = 1
            self.population[partid].directiony = self.wallchangesameabs(self.population[partid].directionx,
                                                                        pythagoc)

        # Kollision mit Upper Y-Wall
        if self.population[partid].spawny >= self.SIMULATIONUPPERWALLY - 8:
            self.population[partid].directionx = round(random.uniform(-1, 1), 2)
            while pythagoc < (self.population[partid].directionx * divider) * \
                    (self.population[partid].directionx * divider):
                divider = divider - 0.1

            self.population[partid].directionx = self.population[partid].directionx * divider
            self.population[partid].directiony = -self.wallchangesameabs(self.population[partid].directionx,
                                                                         pythagoc)
