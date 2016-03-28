import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import time
import serial

class MeasurementThread(QtCore.QThread):
    newData = QtCore.Signal(object)
    measure = False
    start_time = None
    
    def start(self, port, speed, timeout):
        self.measure = True
        self.ser = serial.Serial(port, speed, timeout=timeout)
        super(MeasurementThread, self).start()

    def run(self):
        while self.measure:
            PS = ""
            while self.measure:
                byte_read = self.ser.read(1)
                if len(byte_read):
                    PS+=chr(byte_read[0])
                    if len(PS) == 2:
                        if PS == "PS":
                            b = bytearray()
                            while len(b) != 48:
                                b.append(self.ser.read(1)[0])

                            data = np.fromstring(bytes(b), dtype="<f")
                            b = bytearray()
                            while len(b) != 4:
                                b.append(self.ser.read(1)[0])
                            timestamp = int.from_bytes(bytes(b), byteorder="little")
                            timestamp = timestamp & 0xffffffff
                            if self.start_time is None:
                                self.start_time = timestamp
                              
                                
                            self.newData.emit([timestamp-self.start_time, data])
                            #self.newData.emit(data)
                            PS = ""
                            break
                        else:
                            if PS[1] == "P":
                                PS = "P"
                            else:
                                PS = ""
        self.ser.close()

    def stop(self):
        self.measure = False
        self.start_time = None


