import uuid
import time
import math
from pymongo import ReturnDocument

from config.mongodb import db
from model.db.meterVO import MeterVO

class Meter:
    @staticmethod
    def get(meterConsumption):
        
        meterDBResponse=list()

        for i in range(0,len(meterConsumption)):
            meterDBResponse.append(list(db.meters.find({'ID': meterConsumption[i]}).limit(1)))

        meterResponse = {
            "meter": []
        }

        for i in range(0,len(meterConsumption)):
            for meter in meterDBResponse[i]:
                meterResponse["meter"].append(Meter._decodeMeter(meter))
                
        return meterResponse

    @staticmethod
    def create(meterID, meterInstantPower, meterPhase):
        DBID = str(uuid.uuid4())
        timestamp = time.time()
        
        dbResponse = db.meters.find_one({'ID': meterID})

        if dbResponse is None:
            activePower = 0
            reactivePower = 0
            aparentPower = 0
            powerFactor = 0
            newMeterDatapoint = MeterVO(DBID, meterID, meterInstantPower, timestamp, activePower, reactivePower, aparentPower, meterPhase, powerFactor)
            encodedMeter = Meter._encodeMeter(newMeterDatapoint)
            db.meters.insert_one(encodedMeter)
            response = {
                "meter": {
                    "DBID": encodedMeter["DBID"],
                    "ID": encodedMeter["ID"],
                    "instantPower": encodedMeter["instantPower"],
                    "timestamp": encodedMeter["timestamp"],
                    "activePower" : encodedMeter["activePower"],
                    "reactivePower" : encodedMeter["reactivePower"],
                    "aparentPower" : encodedMeter["aparentPower"],
                    "phase" : encodedMeter["phase"],
                    "powerFactor" : encodedMeter["powerFactor"]
                }
            }
            
        else:

            allDatapoints = list(db.meters.find({'ID':meterID}).sort([("timestamp", -1)]))
            lastDatapoint = allDatapoints[0]
            instantActivePower = meterInstantPower*math.cos(meterPhase*math.pi/180)
            instantReactivePower = meterInstantPower*math.sin(meterPhase*math.pi/180)
            activePower = lastDatapoint["activePower"] + ((((lastDatapoint["instantPower"]*math.cos(math.pi*lastDatapoint["phase"]/180) + instantActivePower) / 2) * (timestamp - lastDatapoint["timestamp"])) / 3600)
            reactivePower = lastDatapoint["reactivePower"] + ((((lastDatapoint["instantPower"]*math.sin(math.pi*lastDatapoint["phase"]/180) + instantReactivePower) / 2) * (timestamp - lastDatapoint["timestamp"])) / 3600)
            aparentPower = (activePower**2+reactivePower**2)**(1/2)
            powerFactor = activePower/math.fabs(aparentPower)
            update_fields = {

                "instantPower": meterInstantPower,
                "timestamp": timestamp,
                "activePower" : activePower,
                "reactivePower" : reactivePower,
                "aparentPower" : aparentPower,
                "phase" : meterPhase,
                "powerFactor" : powerFactor
            }

            response = {
                "meter": None
            }
            result = db.meters.find_one_and_update({"ID": meterID}, {'$set': update_fields},
                                                  return_document=ReturnDocument.AFTER)

            if result is not None:
                response["meter"] = Meter._decodeMeter(result)

        return response

    @staticmethod
    def _encodeMeter(meter):
        return {
            "_type": "meter",
            "DBID": meter.DBID,
            "ID": meter.ID,
            "instantPower": meter.instantPower,
            "timestamp": meter.timestamp,
            "activePower" : meter.activePower,
            "reactivePower" : meter.reactivePower,
            "aparentPower" : meter.aparentPower,
            "phase" : meter.phase,
            "powerFactor" : meter.powerFactor

        }

    @staticmethod
    def _decodeMeter(document):
        assert document["_type"] == "meter"
        meter = {
            "DBID": document["DBID"],
            "ID": document["ID"],
            "instantPower": document["instantPower"],
            "timestamp": document["timestamp"],
            "activePower": document["activePower"],
            "reactivePower": document["reactivePower"],
            "aparentPower": document["aparentPower"],
            "phase": document["phase"],
            "powerFactor": document["powerFactor"]
        }
        return meter