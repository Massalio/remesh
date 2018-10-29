import uuid
import time

from pymongo import ReturnDocument

from config.mongodb import db
from model.db.meter_switchVO import MeterSwitchVO

class MeterSwitch:

    @staticmethod
    def get(listOfIDs):
        meterSwitchesDBResponse = list(db.meter_switches.find({'ID': {'$in': listOfIDs}}))

        meterSwitchesResponse = {
            "meterSwitches": []
        }

        for meterSwitch in meterSwitchesDBResponse:
            meterSwitchesResponse["meterSwitches"].append(MeterSwitch._decodeMeterSwitch(meterSwitch))

        return meterSwitchesResponse

    @staticmethod
    def create(meterSwitchID, meterSwitchValue):
        dbResponse = db.meter_switches.find_one({'ID': meterSwitchID})

        if dbResponse is None:
            newMeterSwitch = MeterSwitchVO(meterSwitchID, meterSwitchValue)
            encodedMeterSwitch = MeterSwitch._encodeMeterSwitch(newMeterSwitch)
            db.meter_switches.insert_one(encodedMeterSwitch)

            response = {
                "meterSwitch": {
                    "ID": encodedMeterSwitch["ID"],
                    "value": encodedMeterSwitch["value"]
                }
            }
        else:
            updated_fields = {
                "value": meterSwitchValue
            }

            response = {
                "meterSwitch": None
            }

            result = db.meter_switches.find_one_and_update({"ID": meterSwitchID}, {'$set': updated_fields},
                                                  return_document=ReturnDocument.AFTER)
            
            if result is not None:
                response["meterSwitch"] = MeterSwitch._decodeMeterSwitch(result)
        
        return response

    @staticmethod
    def _encodeMeterSwitch(meterSwitch):
        return {
            "_type": "meterSwitch",
            "ID": meterSwitch.ID,
            "value": meterSwitch.value
        }

    @staticmethod
    def _decodeMeterSwitch(document):
        assert document["_type"] == "meterSwitch"
        meterSwitch = {
            "ID": document["ID"],
            "value": document["value"]
        }
        return meterSwitch