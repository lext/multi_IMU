"""
multi_IMU software measurement thread class.

(c) Aleksei Tiulpin, 2016

Center for Machine Vision and Signal Analysis,
University of Oulu, Finland

"""


import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import time
import serial
from RingBuffer import RingBuffer

class MeasurementThread(QtCore.QThread):
    newData = QtCore.Signal(object)
    measure = False
    start_time = None
    
    def start(self, port, speed, timeout):
        self.measure = True
        self.ser = serial.Serial(port, speed, timeout=timeout)
        super(MeasurementThread, self).start()

    def run(self):
        rb = RingBuffer(56)
        
        while self.measure:
            if self.ser.in_waiting > 0:
                rb.append(self.ser.read(1)[0])
                if rb[0] == ord("B") and rb[1] == ord("E") and rb[54] == ord("E") and rb[55] == ord("N"):
                    timestamp = int.from_bytes(bytes(rb[2:6]), byteorder="little")
                    timestamp = timestamp & 0xffffffff
                    data = np.fromstring(bytes(rb[6:54]), dtype="<f")
                    if self.start_time is None:
                        self.start_time = timestamp
                    self.newData.emit([timestamp-self.start_time, data])
                
        self.ser.close()

    def stop(self):
        self.measure = False
        self.start_time = None


