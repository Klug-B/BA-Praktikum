from PyQt5.QtGui import QPen, QBrush, QColor


class Constant:
    def __init__(self):
        self.SIMULATIONUPPERWALLY = 315.0
        self.SIMULATIONUNDERWALLY = -315.0
        self.SIMULATIONUPPERWALLX = 290.0
        self.SIMULATIONUNDERWALLX = -290.0
        self.FPS = 60
        self.PARSIZE = 10
        self.RAND = QPen(QColor(0, 0, 0))
        self.INFE = QBrush(QColor(255, 0, 0))
        self.HEALTHY = QBrush(QColor(0, 255, 0))
        self.DEAD = QBrush(QColor(0, 0, 0))
        self.CURED = QBrush(QColor(0, 0, 255))
        self.START = "Start"
        self.RESET = "Reset"
        self.PAUSE = "Pause"
        self.SPEED = "Speed"
        self.CSVAPPLY = "CSV-Apply"
        self.STBOX = "Startboxapply"
        self.CSVSAVE = "CSV-Save"
        self.PRESET = "Preset"
        self.ERROR1 = "Error-Apply-Stat"
        self.ERROR2 = "Error-Apply-CSV"
        self.ERROR3 = "Error-Start-Free"
        self.END = "End"
        self.MOVLIN = "Linear"
        self.MOVCHALFCHAOT = "Halbchaotisch"
        self.MOVEWAVE = "Welle"
