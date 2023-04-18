import datetime
import math
import os
import sqlite3

DATABASE_PATH = 'database.db'

TABLE_INIT = """
CREATE TABLE arduino_data (
id INTEGER PRIMARY KEY,
FSensor1 FLOAT,
FSensor2 FLOAT,
FSensor3 FLOAT,
FSensor4 FLOAT,
FSensor5 FLOAT,
AccelX FLOAT,
AccelY FLOAT,
AccelZ FLOAT,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);"""

class Data:
    # From scalars
    def __init__(self, id=None, F1=0.0, F2=0.0, F3=0.0, F4=0.0, F5=0.0, AX=0.0,
                 AY=0.0, AZ=0.0, timestamp=datetime.datetime.now()):
        self.F1 = F1
        self.F2 = F2
        self.F3 = F3
        self.F4 = F3
        self.F5 = F5
        self.AX = AX
        self.AY = AY
        self.AZ = AZ
        self.timestamp = timestamp
        self.force = max(F1, F2, F3, F4, F5)
        self.acceleration = math.sqrt(math.pow(AX, 2) +
                                      math.pow (AY, 2) +
                                      math.pow(AZ, 2))/0.1458
        self.high_risk = self.acceleration >= 6814.81
        self.med_risk = not self.high_risk and self.acceleration >= 6265.5
        self.low_risk = not self.med_risk and not self.high_risk and self.acceleration >= 30 #5572.35

    @staticmethod
    def from_json(self, json):
        return Data(None,
                    json['FSensor1'],
                    json['FSensor2'],
                    json['FSensor3'],
                    json['FSensor4'],
                    json['FSensor5'],
                    json['AccelX'],
                    json['AccelY'],
                    json['AccelZ'])

    def write(self):
        # Only write datum indicating risk
        if (self.low_risk or self.med_risk or self.high_risk):
            q="INSERT INTO arduino_data VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
            data = (self.F1, self.F2, self.F3, self.F4, self.F5, self.AX, self.AY,
                    self.AZ, self.timestamp)
            with sqlite3.connect(DATABASE_PATH) as conn:
                c = conn.cursor()
                c.execute(q, data)
                c.commit()

    @staticmethod
    def get_all():
        q="""
        SELECT id, FSensor1, FSensor2, FSensor3, FSensor4, FSensor5, AccelX, AccelY,
        AccelZ, timestamp from arduino_data
        """
        data=None
        with sqlite3.connect(DATABASE_PATH) as conn:
            c=conn.cursor()
            c.execute(q)
            data=c.fetchall()
            return [Data(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9])
                    for d in data]

def init_db():
    if not os.path.isfile(DATABASE_PATH):
        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            c.execute(TABLE_INIT)
            print("database.db not found, file initialized")
