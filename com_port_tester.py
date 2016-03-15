import serial
import signal
import numpy as np
import time
import sys

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=4)

ser.write(b'B')
ser.flush()

print("Initializaing the measurement")

def finish_session(signal, frame):
    print("Session terminated")
    ser.write(b'E') 
    ser.flush()              
    ser.close()
    sys.exit(0)

signal.signal(signal.SIGINT, finish_session)

while True:
    PS = ""
    while True:
        byte_read = ser.read()
        if len(byte_read):
            PS+=chr(byte_read[0])
            if len(PS) == 2:
                if PS == "PS":
                    data = np.fromstring(ser.read(24*2), dtype="<f")
                    timestamp = int.from_bytes(ser.read(4), byteorder="little")/1000.
                    print(("%.4f " % timestamp) +"%.4f "*len(data) % tuple(data))
                    PS = ""
                    break
                else:
                    if PS[1] == "P":
                        PS = "P"
                    else:
                        PS = ""

