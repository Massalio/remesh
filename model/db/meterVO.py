class MeterVO:

    def __init__(self, DBID, ID, value, consumption, timestamp):
        self.DBID = DBID
        self.ID = ID
        self.value = value
        self.consumption = consumption
        self.timestamp = timestamp