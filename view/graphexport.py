from view.graphdialog import Ui_Dialog
from PyQt5 import QtWidgets
from pyqtgraph import mkPen
#  Methode erzeugt die Graphen, die am Ende per Dialog sichtbar gemacht werden


class Graphexport(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, data):
        super(Graphexport, self).__init__()
        self.data = data
        self.setupUi(self)
        self.stepcounterlist = data[0]
        self.notinfectedlist = data[2]
        self.infectedlist = data[1]
        self.deadlist = data[3]
        self.curedlist = data[4]

        self.graphwidget.setLabel("left", "Anzahl der Partikel")
        self.graphwidget.setLabel("bottom", "Anzahl der Schritte")
        self.graphwidget.setBackground('w')
        self.graphwidget.addLegend()
        self.graphwidget.plot(self.stepcounterlist, self.notinfectedlist, pen=mkPen(0, 255, 0),
                              name="Nicht-Infizierte-Velauf")
        self.graphwidget.plot(self.stepcounterlist, self.infectedlist, pen=mkPen((255, 0, 0)),
                              name="Infizierte-Verlauf")
        self.graphwidget.plot(self.stepcounterlist, self.deadlist, pen=mkPen((0, 0, 0)), name="Tote-Verlauf")
        self.graphwidget.plot(self.stepcounterlist, self.curedlist, pen=mkPen((0, 0, 255)), name="Geheilte-Verlauf")
