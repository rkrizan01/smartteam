from multiprocessing import Process
import helmet_to_db
import server
import signal

BLUETOOTH_THREAD = Process(target=helmet_to_db.main)
SERVER_THREAD = Process(target=server.app.run, kwargs={'host': "0.0.0.0"})
BLUETOOTH_THREAD.start()
SERVER_THREAD.start()

def shutdown(signal, frame):
    print("Shutting down...")
    SERVER_THREAD.terminate()
    SERVER_THREAD.join()
    BLUETOOTH_THREAD.terminate()
    BLUETOOTH_THREAD.join()

signal.signal(signal.SIGINT, shutdown)
