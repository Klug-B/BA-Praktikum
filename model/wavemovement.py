from model.movement import Movement
import random
import math as m
#  Die Klasse erbt von der Abstract Class Movement die, die anderen Funktionen wie makemove beinhaltet. Die hier auf-
#  geführten Methoden, überschreiben die Methoden der Abstract-Class Movement


class Wavemovement(Movement):

    def movepartikel(self, population, state, stepcounter):
        self.population = population
        self.state = state
        self.counter = stepcounter
        for i in range(0, len(self.population)):
            if self.state[i].move:
                self.proofcollisionwall(i)
                self.proofcollisonpartikel(i)
                if stepcounter % 20 == 0:
                    self.setwavedirection(i)
                self.makemove(i)

                if (self.state[i].diseased and self.counter != self.state[i].dissince) and \
                        ((self.counter - self.state[i].dissince) % 300 == 0):
                    self.makedeadorcured(i)
            else:
                if (self.state[i].diseased and self.counter != self.state[i].dissince) and \
                        ((self.counter - self.state[i].dissince) % 300 == 0):
                    self.makedeadorcured(i)

        return self.population, self.state

    #  Abfrage der Kollision mit den Wänden: Die y-Koordiante bekommt hierbei einen zufälligen sinuswert. Dies erzeugt
    #  eine beinahe sinusähnliche Bewegung der Teilchen auch bei Kontakt mit einer der Wände
    def proofcollisionwall(self, partid):
        if self.population[partid].spawnx <= self.SIMULATIONUNDERWALLX + 8:
            self.population[partid].directiony = round(m.sin(random.uniform(0, 2*m.pi)), 2)
            self.population[partid].directionx = round(random.uniform(0, 1), 2)
        # Kollision mit Upper X-Wall
        if self.population[partid].spawnx >= self.SIMULATIONUPPERWALLX - 8:
            self.population[partid].directiony = round(m.sin(random.uniform(0, 2*m.pi)), 2)
            self.population[partid].directionx = round(random.uniform(-1, 0), 2)
        # Kollision mit Under Y-Wall
        if self.population[partid].spawny <= self.SIMULATIONUNDERWALLY + 8:
            self.population[partid].directiony = round(m.sin(random.uniform(0, m.pi)), 2)
            self.population[partid].directionx = round(random.uniform(-1, 1), 2)
        # Kollision mit Upper Y-Wall
        if self.population[partid].spawny >= self.SIMULATIONUPPERWALLY - 8:
            self.population[partid].directiony = -round(m.sin(random.uniform(m.pi, 0)), 2)
            self.population[partid].directionx = round(random.uniform(-1, 1), 2)

    #  Methode die einen y-Wert einen sinuswert zuweist. Dadurch entsteht eine annährende Welle. Die Funktion wurde
    #  dabei an das Window und den Gegebenheiten angepasst.
    def setwavedirection(self, partid):
        if not self.population[partid].spawnx <= self.SIMULATIONUNDERWALLX + 8 and not\
                self.population[partid].spawnx >= self.SIMULATIONUPPERWALLX - 8 and not \
                self.population[partid].spawny <= self.SIMULATIONUNDERWALLY + 8 and not \
                self.population[partid].spawny >= self.SIMULATIONUPPERWALLY - 8:
            self.population[partid].directiony = 2 * round(m.sin(random.uniform(0, 2*m.pi)), 2)
