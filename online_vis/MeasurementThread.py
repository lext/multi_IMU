import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import time

class MeasurementThread(QtCore.QThread):
    newData = QtCore.Signal(object)
    measure = False

    def start(self):
    	self.measure = True
    	super(MeasurementThread, self).start()

    def run(self):
        while self.measure:
            data = np.random.randn(12)

            self.newData.emit([123, data])
            time.sleep(0.005)

    def stop(self):
    	self.measure = False

