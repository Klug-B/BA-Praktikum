class ParticleState:
    def __init__(self, diseased, dissince, dead, cured, moveable, distancekeeper):
        self.diseased = diseased
        self.dissince = dissince
        self.dead = dead
        self.cured = cured
        self.move = moveable
        self.distancekeeper = distancekeeper

#  Initialisiert die Statusliste. Babei gilt als erstes den Startinfizierten und als nächstes weitere Startinfizierte
#  mit Einschränkungen. Danach werden die Gesunden mit Einschränkungen erstellt. Dabei Gilt als Reihenfolge:
#  Bewegungsunfähig --> Distanz-Einhaltender --> Sonstige: Wichtig dabei: Es wird immer nur eine einzelne Eigenschaft
#  gesetzt wird.
    @staticmethod
    def createstate(numbers, infecstart, moveablecount, distancekeeper):
        statlist = []
        for i in range(0, numbers):
            if i < infecstart:
                if i == 0:
                    statlist.append(ParticleState(True, 0, False, False, True, False))
                elif moveablecount > 0:
                    statlist.append(ParticleState(True, 0, False, False, False, False))
                    moveablecount = moveablecount - 1
                else:
                    statlist.append(ParticleState(True, 0, False, False, True, False))
            elif moveablecount > 0:
                statlist.append(ParticleState(False, 0, False, False, False, False))
                moveablecount = moveablecount - 1
            elif distancekeeper > 0:
                statlist.append(ParticleState(False, 0, False, False, True, True))
                distancekeeper = distancekeeper - 1
            else:
                statlist.append(ParticleState(False, 0, False, False, True, False))

        return statlist
