from multiprocessing import Process
import helmet_to_db
import signal
BLUETOOTH_THREAD = Process(target=helmet_to_db.main)
BLUETOOTH_THREAD.start()
def shutdown(signal, frame):
    print("Shutting down...")
    BLUETOOTH_THREAD.terminate()
    BLUETOOTH_THREAD.join()

signal.signal(signal.SIGINT, shutdown)
