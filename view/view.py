from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QFileDialog
from view.mainwindow import Ui_MainWindow
from view.graphexport import Graphexport
from resources.constant import Constant
import csv
import os


class View(QtWidgets.QMainWindow, Ui_MainWindow, Constant):
    resetsignal = QtCore.pyqtSignal()
    startsignal = QtCore.pyqtSignal()
    pausesignal = QtCore.pyqtSignal()
    exitsignal = QtCore.pyqtSignal()
    csvsignal = QtCore.pyqtSignal()
    applysignal = QtCore.pyqtSignal()
    csvapplysignal = QtCore.pyqtSignal()
    endsignal = QtCore.pyqtSignal()

    speed1signal = QtCore.pyqtSignal()
    speed2signal = QtCore.pyqtSignal()
    speed3signal = QtCore.pyqtSignal()

    def __init__(self):
        super(View, self).__init__()
        Constant.__init__(self)
        self.setupUi(self)
        self.scene = QGraphicsScene()
        QGraphicsView.setHorizontalScrollBarPolicy(self.graphicsview, QtCore.Qt.ScrollBarAlwaysOff)
        QGraphicsView.setVerticalScrollBarPolicy(self.graphicsview, QtCore.Qt.ScrollBarAlwaysOff)
        self.path = []
        self.firstopened = False
        self.symbolliste = []
        self.partikellist = []
        self.zustandlist = []
        QGraphicsView.setScene(self.graphicsview, self.scene)
        self.connectsignals()

    #  Initialisierung der Objekte
    def generateviewobj(self, data):
        self.partikellist = data
        for z in range(0, self.getpopuspincount()):
            self.symbolliste.append(self.scene.addEllipse(self.partikellist[z].spawnx, self.partikellist[z].spawny,
                                                          self.PARSIZE, self.PARSIZE, self.RAND, self.HEALTHY))

    #  scene mit Objekten wird pro step geupdatet
    def updateviewdata(self, data, zustanddata):
        self.scene.clear()
        self.partikellist = data
        self.zustandlist = zustanddata
        # Überprüfung welche Farbe Objekt hat
        for i in range(0, self.getpopuspincount()):
            if self.zustandlist[i].diseased:
                diseasecolour = self.INFE
            elif self.zustandlist[i].cured:
                diseasecolour = self.CURED
            elif self.zustandlist[i].dead:
                diseasecolour = self.DEAD
            else:
                diseasecolour = self.HEALTHY

            self.symbolliste[i] = self.scene.addEllipse(self.partikellist[i].spawnx, self.partikellist[i].spawny,
                                                        self.PARSIZE, self.PARSIZE, self.RAND, diseasecolour)

    #  Live data update
    def updatelivedata(self, datanotinf, datainf, datacured, datadead):
        self.notinfnumberlabel.setText(str(datanotinf))
        #  Endsignal senden wenn Infizierte = 0 ist
        self.infectnumberlabel.setText(str(datainf))
        self.curednumberlabel.setText(str(datacured))
        self.deadnumberlabel.setText(str(datadead))
        if datainf == 0:
            self.endofsimulation()

    #  Systemnachrichten werden hier geupdatet
    def updatesysmes(self, keyword):
        if keyword == self.ERROR1:
            self.systemlabel.setText("Error: Bestätigen-Button der Startvariablenbox muss einmal bestätigt werden.")
        elif keyword == self.STBOX:
            self.systemlabel.setText("Die Settings wurden übernommen. Die Simulation kann gestartet werden.\n"
                                     "Achtung es können noch Zusatzeinstellungen vorgenommen werden.\n"
                                     "Diese werden beim Start der Simulation gespeichert!")
        elif keyword == self.ERROR2:
            self.systemlabel.setText("Error:Der Bestätigen-Button von der CSV Box muss einmal betätigt werden!")
        elif keyword == self.START:
            self.systemlabel.setText("Simulation läuft...")
        elif keyword == self.END:
            self.systemlabel.setText("Die Simulation ist abgeschlossen. Reset für erneuten Durchlauf.")
        elif keyword == self.PAUSE:
            self.systemlabel.setText("Simulation ist pausiert.")
        elif keyword == self.RESET:
            self.systemlabel.setText("Reset der Simulation erfolgreich.")
        elif keyword == self.ERROR3:
            self.systemlabel.setText('Der Startbutton wird erst nach betätigen des CSV Speichern Button freigegeben.')

    def updatetime(self, time):
        self.timedatalabel.setText(time.toString("hh:mm:ss"))

    # Schreibt die CSV Datei
    def createcsvfile(self, step, notinfected, infi, dead, cured):
        if not self.firstopened:
            self.changeenableboxandbuttons(self.CSVSAVE, 0)
            self.path = QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('Home'), 'CSV(*.csv)')
            with open(self.path[0], 'a') as csvfile:
                fieldnames = ['Schritt', 'Gesund', 'Infiziert', 'Tot', 'Genesen']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            self.firstopened = True
            return
        else:
            with open(self.path[0], mode='a', newline='') as csvfile:
                fieldnames = ['Schritt', 'Gesund', 'Infiziert', 'Tot', 'Genesen']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'Schritt': step, 'Gesund': notinfected, 'Infiziert': infi, 'Tot': dead,
                                 'Genesen': cured})

    # Event was die Max der Startwerte beeinflusst(Infiziert, Unbeweglich, Abstandhalter)
    def maxandminchanges(self):
        maximuminfe = self.personbox.value() - 1
        self.infbox.setMaximum(maximuminfe)
        self.keeperspinBox.setMaximum(int(self.personbox.value() * 0.4))
        self.unmoveablespinbox.setMaximum(maximuminfe)

    # Enable Disable Buttons Start und Pause und Boxen und Label.Alle Funktionen die danach folgen, beeinflussen die GUI
    def changeenableboxandbuttons(self, case, function):
        if case == self.START:
            self.changestart(case)
        elif case == self.RESET:
            self.changereset(case)
        elif case == self.PAUSE:
            self.changepause(case)
        elif case == self.SPEED:
            self.changespeed(function)
        elif case == self.CSVAPPLY:
            self.changecsvapply(case)
        elif case == self.STBOX:
            self.changestartbox(case)
        elif case == self.CSVSAVE:
            self.changecsv(case)
        elif case == self.ERROR1 or case == self.ERROR2 or case == self.ERROR3:
            self.error(case)
        elif case == self.END:
            self.end(case, function)

    def changestart(self, case):
        self.updatesysmes(case)
        self.startbutton.setEnabled(False)
        self.pausebutton.setEnabled(True)
        self.extrabox.setEnabled(False)
        self.csvgroupbox.setEnabled(False)
        self.csvsavebutton.setEnabled(False)

    def changereset(self, case):
        self.updatesysmes(case)
        self.updatelivedata("", "", "", "")
        self.startbutton.setEnabled(True)
        self.pausebutton.setEnabled(False)
        self.speedbutton1x.setEnabled(False)
        self.speedbutton2x.setEnabled(True)
        self.speedbutton3x.setEnabled(True)
        self.csvsavebutton.setEnabled(True)
        self.applycsvbutton.setEnabled(True)
        self.startvariablesgroupbox.setEnabled(True)
        self.extrabox.setEnabled(True)
        self.csvgroupbox.setEnabled(True)
        self.scene.clear()
        self.firstopened = False

    def changepause(self, case):
        self.updatesysmes(case)
        self.pausebutton.setEnabled(False)
        self.startbutton.setEnabled(True)

    def changespeed(self, speed):
        if speed == 1:
            self.speedbutton1x.setEnabled(False)
            self.speedbutton2x.setEnabled(True)
            self.speedbutton3x.setEnabled(True)
        elif speed == 2:
            self.speedbutton1x.setEnabled(True)
            self.speedbutton2x.setEnabled(False)
            self.speedbutton3x.setEnabled(True)
        else:
            self.speedbutton1x.setEnabled(True)
            self.speedbutton2x.setEnabled(True)
            self.speedbutton3x.setEnabled(False)

    def changecsvapply(self, case):
        self.updatesysmes(case)
        self.applycsvbutton.setEnabled(False)
        self.startbutton.setEnabled(False)

    def changestartbox(self, case):
        self.updatesysmes(case)
        self.startvariablesgroupbox.setEnabled(False)

    def changecsv(self, case):
        self.updatesysmes(case)
        self.csvsavebutton.setEnabled(False)
        self.startbutton.setEnabled(True)

    def error(self, case):
        self.updatesysmes(case)

    def end(self, case, function):
        self.startbutton.setEnabled(False)
        self.pausebutton.setEnabled(False)
        self.updatesysmes(case)
        if self.checkiflivedataexport():
            dial = Graphexport(function)
            dial.exec_()

    # Getter Methoden für die Value der Spinboxen etc.
    def getfirstopenedcsv(self):
        return self.firstopened

    def getpopuspincount(self):
        return self.personbox.value()

    def getinfspincount(self):
        return self.infbox.value()

    def getdeadchancespincount(self):
        return self.deathbox.value()

    def getdiseasechancespincount(self):
        return self.diseasechancebox.value()

    def getcurechancespincount(self):
        return self.curebox.value()

    def getdistancespincount(self):
        return self.distancespinbox.value()

    def getunmoveablespincount(self):
        return self.unmoveablespinbox.value()

    def getgranualitaet(self):
        return self.granspinbox.value()

    def getmovementchoicebox(self):
        return self.movementbox.currentText()

    def checkifunmoveisactive(self):
        if self.extrabox.isChecked():
            return self.unmoveablespinbox.value()
        else:
            return 0

    def checkifdistanceset(self):
        if self.extrabox.isChecked():
            return self.distancespinbox.value()
        else:
            return 0

    def checkifpeoplekeepdistance(self):
        if self.extrabox.isChecked():
            return self.keeperspinBox.value()
        else:
            return 0

    def checkiflivedataexport(self):
        if self.extrabox.isChecked():
            return self.livedataexportbox.isChecked()
        else:
            return False

    # Signal emit-Methoden sowie das connecten
    def startsimulationclicked(self):
        self.startsignal.emit()

    def exitsimulationclicked(self):
        self.exitsignal.emit()

    def pausesimulationclicked(self):
        self.pausesignal.emit()

    def resetsimulationclicked(self):
        self.resetsignal.emit()

    def endofsimulation(self):
        self.endsignal.emit()

    def csvexportclicked(self):
        self.csvsignal.emit()

    def applycsvclicked(self):
        self.csvapplysignal.emit()

    def applysettingclicked(self):
        self.applysignal.emit()

    def speed1clicked(self):
        self.speed1signal.emit()

    def speed2clicked(self):
        self.speed2signal.emit()

    def speed3clicked(self):
        self.speed3signal.emit()

    def connectsignals(self):
        self.exitbutton.pressed.connect(self.exitsimulationclicked)
        self.startbutton.pressed.connect(self.startsimulationclicked)
        self.pausebutton.pressed.connect(self.pausesimulationclicked)
        self.resetbutton.pressed.connect(self.resetsimulationclicked)
        self.csvsavebutton.pressed.connect(self.csvexportclicked)
        self.applycsvbutton.pressed.connect(self.applycsvclicked)
        self.applybutton.pressed.connect(self.applysettingclicked)
        self.personbox.valueChanged.connect(self.maxandminchanges)
        self.speedbutton1x.pressed.connect(self.speed1clicked)
        self.speedbutton2x.pressed.connect(self.speed2clicked)
        self.speedbutton3x.pressed.connect(self.speed3clicked)
