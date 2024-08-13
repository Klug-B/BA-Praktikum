class Exportdata:
    def __init__(self):
        self.steplist = []
        self.infectedlist = []
        self.notinfectedlist = []
        self.deadlist = []
        self.curedlist = []

    def returnalldata(self):
        return self.steplist, self.infectedlist, self.notinfectedlist, self.deadlist, self.curedlist
