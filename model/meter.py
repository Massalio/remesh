import uuid
import time

from pymongo import ReturnDocument

from config.mongodb import db
from model.db.meterVO import MeterVO

class Meter:

    @staticmethod
    def create(meterID, meterValue):
        DBID = str(uuid.uuid4())
        timestamp = time.time()
        
        #comentar estas 3 lineas para inicializar

        allDatapoints = list(db.meters.find().sort([("timestamp", -1)]))
        lastDatapoint = allDatapoints[0]

        consumption = lastDatapoint["consumption"] + ((((lastDatapoint["value"] + meterValue) / 2) * (timestamp - lastDatapoint["timestamp"])) / 3600)

        #Para empezar
        #consumption = 0

        newMeterDatapoint = MeterVO(DBID, meterID, meterValue, consumption, timestamp)
        encodedMeter = Meter._encodeMeter(newMeterDatapoint)
        db.meters.insert_one(encodedMeter)
        response = {
            "meter": {
                "DBID": encodedMeter["DBID"],
                "ID": encodedMeter["ID"],
                "value": encodedMeter["value"],
                "consumption": encodedMeter["consumption"],
                "timestamp": encodedMeter["timestamp"]
            }
        }
        return response

    @staticmethod
    def _encodeMeter(meter):
        return {
            "_type": "meter",
            "DBID": meter.DBID,
            "ID": meter.ID,
            "value": meter.value,
            "consumption": meter.consumption,
            "timestamp": meter.timestamp
        }

    @staticmethod
    def _decodeMeter(document):
        assert document["_type"] == "meter"
        meter = {
            "DBID": document["DBID"],
            "ID": document["ID"],
            "value": document["value"],
            "consumption": document["consumption"],
            "timestamp": document["timestamp"]
        }
        return meter