from PyQt5 import QtCore
import sys
from view.view import View
from model.simulation import Simulation
from resources.constant import Constant


class Presenter(QtCore.QObject, Constant):

    def __init__(self):
        super(Presenter, self).__init__()
        Constant.__init__(self)
        # create main window
        self.ui = View()
        self.simulation = None
        # Kontrollvariablen
        self.issimulationrunning = False
        self.pausecontrol = False
        self.startedonce = False
        self.applycounter = 0
        self.csvapplcounter = 0
        self.csvsavecounter = 0
        self.simulationspeed = 1
        # Timer für die das Zeit-Label wird jede sekunde aufgerufen
        self.currtime = QtCore.QTime(00, 00, 00)
        self.timetimer = QtCore.QTimer(self)
        self.timetimer.timeout.connect(self.timepassed)
        self.timetimer.start(1000)
        # Timer der den Mainloop alle 1000/60 ms aufruft, kann durch Speed aber verändert werden
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.mainloop)
        self.timer.start(int(1000 / self.FPS))
        # Timer der die View-Update alle 1000/60 ms aufruft
        self.viewtimer = QtCore.QTimer(self)
        self.viewtimer.timeout.connect(self.updateviewandlive)
        self.viewtimer.start(int(1000 / self.FPS))

        self._connectuielements()

    #  mainloop der die Steps ausführt
    def mainloop(self):
        if self.issimulationrunning:
            if self.simulation.getcounter() % self.ui.getgranualitaet() == 0 and self.csvapplcounter == 1:
                self.connectcsv()
            self.simulation.performstep(self.ui.getmovementchoicebox())

    #  Simulationsstart, Pause , reset und End Methode
    def startsimulation(self):
        if not self.startedonce and self.applycounter == 1:
            self.confirmsignal(self.START, 0)
            self.simulation = Simulation(self.ui.getpopuspincount(), self.ui.getinfspincount(),
                                         self.ui.getdeadchancespincount(), self.ui.getdiseasechancespincount(),
                                         self.ui.getcurechancespincount(), self.ui.checkifunmoveisactive(),
                                         self.ui.checkifdistanceset(), self.ui.getmovementchoicebox(),
                                         self.ui.checkifpeoplekeepdistance(), self.ui.checkiflivedataexport())

            self.ui.generateviewobj(self.simulation.getpopdata())
            self.issimulationrunning = True
            self.startedonce = True
        else:
            #  Error abfragen, die auf dem Systemlabel ausgegeben werden
            if self.applycounter < 1:
                self.confirmsignal(self.ERROR1, 0)
            else:
                self.confirmsignal(self.ERROR3, 0)

        if self.pausecontrol:
            self.confirmsignal(self.START, 0)
            self.issimulationrunning = True
            self.pausecontrol = False

    #  Pause, Reset und End-Metoden, die die Kontrollvariablen ändern
    def pausesimulation(self):
        self.confirmsignal(self.PAUSE, 0)
        self.pausecontrol = True
        self.issimulationrunning = False

    def resetsimulation(self):
        self.confirmsignal(self.RESET, 0)
        self.currtime = QtCore.QTime(00, 00, 00)
        self.ui.updatetime(self.currtime)
        self.timer.start(int(1000 / self.FPS))
        self.simulationspeed = 1
        self.issimulationrunning = False
        self.pausecontrol = False
        self.startedonce = False
        self.applycounter = 0
        self.csvapplcounter = 0
        self.csvsavecounter = 0

    def simulationend(self):
        if self.csvapplcounter == 1:
            self.connectcsv()
        self.issimulationrunning = False
        self.confirmsignal(self.END, self.simulation.getexportdata())

    #  CSV Methoden: Apply CDV Button und csv-save, dass nur die Datei mit den Headern erzeugt
    def confirmapplycsv(self):
        self.csvapplcounter = self.csvapplcounter + 1
        self.confirmsignal(self.CSVAPPLY, 0)

    def csv_save(self):
        if self.csvapplcounter == 0:
            self.confirmsignal(self.ERROR2, 0)
        else:
            self.ui.createcsvfile(0, 0, 0, 0, 0)
            self.csvsavecounter = 1
            self.confirmsignal(self.CSVSAVE, 0)

    def applysstaboxapply(self):
        self.applycounter = 1
        self.confirmsignal(self.STBOX, 0)

    #  time
    def timepassed(self):
        if self.issimulationrunning:
            self.currtime = self.currtime.addSecs(1)
            self.ui.updatetime(self.currtime)

    def setspeed1(self):
        self.simulationspeed = 1
        self.timer.start(int(1000 / (self.FPS * self.simulationspeed)))
        self.confirmsignal(self.SPEED, self.simulationspeed)

    def setspeed2(self):
        self.simulationspeed = 2
        self.timer.start(int(1000 / (self.FPS * self.simulationspeed)))
        self.confirmsignal(self.SPEED, self.simulationspeed)

    def setspeed3(self):
        self.simulationspeed = 3
        self.timer.start(int(1000 / (self.FPS * self.simulationspeed)))
        self.confirmsignal(self.SPEED, self.simulationspeed)

    def confirmsignal(self, key, function):
        self.ui.changeenableboxandbuttons(key, function)

    #  CSV Export writer
    def connectcsv(self):
        self.ui.createcsvfile(self.simulation.getcounter(), self.simulation.getnotinfcount(),
                              self.simulation.getinfcount(), self.simulation.getdeadcount(),
                              self.simulation.getcuredcount())

    #  Update der Labels und der Graphicview
    def updateviewandlive(self):
        if self.issimulationrunning:
            self.ui.updatelivedata(self.simulation.getnotinfcount(), self.simulation.getinfcount(),
                                   self.simulation.getcuredcount(), self.simulation.getdeadcount())
            self.ui.updateviewdata(self.simulation.getpopdata(), self.simulation.getstatedata())

    @staticmethod
    def exitsimulation():
        sys.exit()

    def _connectuielements(self) -> None:
        # elements of the main window
        self.ui.exitsignal.connect(self.exitsimulation)
        self.ui.startsignal.connect(self.startsimulation)
        self.ui.pausesignal.connect(self.pausesimulation)
        self.ui.resetsignal.connect(self.resetsimulation)
        self.ui.endsignal.connect(self.simulationend)
        self.ui.csvsignal.connect(self.csv_save)
        self.ui.csvapplysignal.connect(self.confirmapplycsv)
        self.ui.applysignal.connect(self.applysstaboxapply)
        self.ui.speed1signal.connect(self.setspeed1)
        self.ui.speed2signal.connect(self.setspeed2)
        self.ui.speed3signal.connect(self.setspeed3)
