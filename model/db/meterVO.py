class MeterVO:

    def __init__(self, DBID, ID, instantPower, timestamp, activePower, reactivePower, aparentPower, phase, powerFactor):
        self.DBID = DBID
        self.ID = ID
        self.instantPower = instantPower
        self.timestamp = timestamp
        self.activePower = activePower
        self.reactivePower = reactivePower
        self.aparentPower = aparentPower
        self.phase = phase
        self.powerFactor = powerFactor