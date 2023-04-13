import datetime
import math
import os
import sqlite3

DATABASE_PATH = 'database.db'

class Data:
    # From scalars
    def __init__(self, F1=0.0, F2=0.0, F3=0.0, F4=0.0, F5=0.0, AX=0.0, AY=0.0,
                 AZ=0.0, timestamp=datetime.datetime.now()):
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

    @staticmethod
    def from_json(self, json):
        return Data(json['FSensor1'],
                    json['FSensor2'],
                    json['FSensor3'],
                    json['FSensor4'],
                    json['FSensor5'],
                    json['AccelX'],
                    json['AccelY'],
                    json['AccelZ'])

    def write(self):
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
SELECT FSensor1, FSensor2, FSensor3, FSensor4, FSensor5,
        AccelX, AccelY, AccelZ, timestamp from arduino_data
        """
        data=None
        with sqlite3.connect(DATABASE_PATH) as conn:
            c=conn.cursor()
            c.execute(q)
            data=c.fetchall()
            return [Data(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8]) for d in data]

def init_db():
    create_table_query = """
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

    if not os.path.isfile(DATABASE_PATH):
        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            c.execute(create_table_query)
            print("database.db not found, file initialized")
