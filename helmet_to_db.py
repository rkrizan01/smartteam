'''
This file is used to populated the database. It is not used in the main program,
and should only be used for single use test purpose when adding db classes. 

NOTE: All connections use relative path
'''
import sqlite3
import datetime
import random
import serial
import json
import os
import time
import subprocess
import csv
import math
import signal

DATABASE_PATH = '../database.db'
SENSOR_DATA_PATH = '../sensor_data.csv'

def add_data_to_db(new_data=None):
    '''
    If data is being passed in, append a timestamp and query database.db to
    insert the new data. Otherwise, generate phony data that is appended to
    database.db.  
    '''
    if new_data is None:
        new_data = {
            "FSensor1" : float("{:.6}".format(random.uniform(0, 1))),
            "FSensor2" : float("{:.6}".format(random.uniform(0, 1))),
            "FSensor3" : float("{:.6}".format(random.uniform(0, 1))),
            "FSensor4" : float("{:.6}".format(random.uniform(0, 1))),
            "FSensor5" : float("{:.6}".format(random.uniform(0, 1))),

            "AccelX" : float("{:.6}".format(random.uniform(0, 1))),
            "AccelY" : float("{:.6}".format(random.uniform(0, 1))),
            "AccelZ" : float("{:.6}".format(random.uniform(0, 1))), 
            # "AccelMagn" : float("{:.6}".format(random.uniform(0, 1))), 

            "timestamp" : datetime.datetime.now()
        }
    else:
        print("Using existing (given) data")
        new_data["timestamp"] = datetime.datetime.now()

    this_query=f"INSERT INTO arduino_data (FSensor1, FSensor2, FSensor3, FSensor4, FSensor5, AccelX, AccelY, AccelZ, timestamp) VALUES ('{new_data['FSensor1']}', '{new_data['FSensor2']}', '{new_data['FSensor3']}', '{new_data['FSensor4']}', '{new_data['FSensor5']}', '{new_data['AccelX']}', '{new_data['AccelY']}', '{new_data['AccelZ']}', '{new_data['timestamp']}')"   

    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()
        c.execute(this_query)

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

    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()
        c.execute(create_table_query)
        print("database.db not found, file initialized")

# Code was written to handle shutdowns with keyboardinterrupt, so make it happy.
def shutdown (signal, frame):
    raise KeyboardInterrupt()

###################################
# MAIN LOOP
###################################
def main():
    signal.signal(signal.SIGTERM, shutdown)
    if not os.path.isfile(DATABASE_PATH):
        init_db()

    # Read data from bluetooth port 0, populate data into database.db
    try:
        ser = serial.Serial(port='/dev/rfcomm0', baudrate=9600)
    except Exception:
            print("Bluetooth device not available")
            exit()
    error_count = 0
    print("ENTERING LOOP")
    while True:
        try:
            bt_data =ser.readline().decode("utf-8").replace('\n', '')
            print(bt_data)
            with open(SENSOR_DATA_PATH,"a") as f: # writing data to csv (each data point is one row)
                writer = csv.writer(f,delimiter=",")
                writer.writerow([time.time(),bt_data])
            print("wrote to csv")
            bt_data = json.loads(bt_data)
            add_data_to_db(bt_data)

        except KeyboardInterrupt:
            print('KeyboardInterrupt found, exiting')
            exit()
        except Exception as e:
            print(f'error with reading bt_data: {e}')
            error_count += 1
            if error_count == 10:
                print('connection not found, exiting')
                exit()
