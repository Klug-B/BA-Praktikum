from model.particle import Particle
from model.particlestate import ParticleState
from model.linearmovement import Linaermovement
from model.halfchaoticmovement import Halfchaoticmovement
from model.chaoticmovement import Chaoticmovement
from model.wavemovement import Wavemovement
from resources.exportdata import Exportdata
from resources.constant import Constant


class Simulation(Constant):
    #  Status-Liste/populationsliste wird initialisiert, sowie die Klasse der Bewegungsform.
    def __init__(self, population, infecstart, deadlychance, diseasechance, curechance, moveablecount, distance,
                 movementchoice, distancepersonevalue, dataexport):
        Constant.__init__(self)
        self.stepcounter = 0
        self.populationlist = Particle.createpopulation(population)
        self.statelist = ParticleState.createstate(population, infecstart, moveablecount, distancepersonevalue)
        self.dataexport = dataexport
        self.export = Exportdata()
        if movementchoice == self.MOVLIN:
            self.lin = Linaermovement(deadlychance, diseasechance, curechance, distance)
        elif movementchoice == self.MOVCHALFCHAOT:
            self.halfchaot = Halfchaoticmovement(deadlychance, diseasechance, curechance, distance)
        elif movementchoice == self.MOVEWAVE:
            self.wave = Wavemovement(deadlychance, diseasechance, curechance, distance)
        else:
            self.chaot = Chaoticmovement(deadlychance, diseasechance, curechance, distance)

    #  Schritt wird performed. Je nach Movementtype bekommt man als Rückgabe wert die geänderten Listen.
    #  Für den Graphen-Export, wird alle 50 Steps, die Methode adddatatoexportfiles ausgeführt, falls das Häkchen in der
    #  UI gesetzt wurde
    def performstep(self, movementtype):
        self.stepcounter += 1
        if movementtype == self.MOVLIN:
            self.populationlist, self.statelist = self.lin.movepartikel(self.populationlist, self.statelist,
                                                                        self.stepcounter)

        elif movementtype == self.MOVCHALFCHAOT:
            self.populationlist, self.statelist = self.halfchaot.movepartikel(self.populationlist, self.statelist,
                                                                              self.stepcounter)
        elif movementtype == self.MOVEWAVE:
            self.populationlist, self.statelist = self.wave.movepartikel(self.populationlist, self.statelist,
                                                                         self.stepcounter)
        else:
            self.populationlist, self.statelist = self.chaot.movepartikel(self.populationlist, self.statelist,
                                                                          self.stepcounter)

        if (self.stepcounter % 50 == 0 and self.dataexport) or (self.dataexport and self.getinfcount() == 0 and
                                                                self.stepcounter != 0):
            self.adddatatoexportfiles()

    # Getter Methoden für das Updaten der Labels
    def getnotinfcount(self):
        notinfcount = 0
        for i in range(0, len(self.statelist)):
            if not self.statelist[i].diseased and (not self.statelist[i].cured and not self.statelist[i].dead):
                notinfcount = notinfcount + 1
        return notinfcount

    def getinfcount(self):
        infcount = 0
        for i in range(0, len(self.statelist)):
            if self.statelist[i].diseased:
                infcount = infcount + 1

        return infcount

    def getdeadcount(self):
        deadcount = 0
        for i in range(0, len(self.statelist)):
            if self.statelist[i].dead:
                deadcount = deadcount + 1

        return deadcount

    def getcuredcount(self):
        curedcount = 0
        for i in range(0, len(self.statelist)):
            if self.statelist[i].cured:
                curedcount = curedcount + 1

        return curedcount

    #  Getter Methoden für die Listen
    def getstatedata(self):
        return self.statelist

    def getpopdata(self):
        return self.populationlist

    def getcounter(self):
        return self.stepcounter

    def adddatatoexportfiles(self):
        self.export.steplist.append(self.stepcounter)
        self.export.notinfectedlist.append(self.getnotinfcount())
        self.export.infectedlist.append(self.getinfcount())
        self.export.deadlist.append(self.getdeadcount())
        self.export.curedlist.append(self.getcuredcount())

    def getexportdata(self):
        array = self.export.returnalldata()
        return array
